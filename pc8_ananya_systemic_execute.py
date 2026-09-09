#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download, targeting this repo's
# PAT-VAL-ANANYA validation patient (distinct id/mrn from the pre-existing PAT-DEMO-CHEMO
# showcase patient; same "Ananya Shah" synthetic identity). BASE is env-overridable to match
# this repo's own acceptance-script convention. All action names below were confirmed present
# in this repo's server.py under the same names before porting.
import json, urllib.request, urllib.error, urllib.parse, pathlib, sys, sqlite3, os
from datetime import date, datetime, timezone, timedelta
ROOT=pathlib.Path(__file__).resolve().parent
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765'); PID='PAT-VAL-ANANYA'; TODAY='2026-09-08'
rows=[];TOK={}
creds={}
for line in (ROOT/'DEMO_USER_CREDENTIALS.txt').read_text(encoding='utf-8').splitlines():
    if ' | ' in line:
        u,p,n,r=[x.strip() for x in line.split(' | ',3)];creds[r]=(u,p,n)

def http(path,method='GET',data=None,token=None):
    h={'Content-Type':'application/json'}
    if token:h['Authorization']='Bearer '+token
    body=json.dumps(data).encode() if data is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE+path,data=body,headers=h,method=method),timeout=20) as r:
            raw=r.read().decode();return r.status,json.loads(raw or '{}')
    except urllib.error.HTTPError as e:
        raw=e.read().decode()
        try:j=json.loads(raw or '{}')
        except:j={'raw':raw}
        return e.code,j

def login(role):
    if role not in TOK:
        u,p,n=creds[role];st,j=http('/api/login','POST',{'username':u,'pin':p});assert st==200,(role,st,j);TOK[role]=j['token']
    return TOK[role]
def boot(role):
    st,j=http('/api/bootstrap?patient='+urllib.parse.quote(PID),token=login(role));assert st==200,(role,st,j);return j
def entity(role,typ,eid=None):
    xs=boot(role).get('entities',{}).get(typ,[])
    if eid:return next((x for x in xs if x['id']==eid),None)
    return xs[-1] if xs else None
OPT={'save_intake','med_recon','save_dynamic_form','save_consultation','save_diagnosis','save_appointment','queue_patient','save_care_plan','save_treatment_plan','save_radiology','save_pathology','mdt_comment','mdt_attendance','mdt_recommend','save_referral','save_support_record','rt_planning_status'}
def action(role,a,eid='',data=None,expect=None):
    payload={'action':a,'patient_id':PID,'entity_id':eid,'data':data or {}}
    if a in OPT:
        if expect is None:
            b=boot(role);found=None
            for xs in b.get('entities',{}).values():
                for x in xs:
                    if x['id']==eid:found=x;break
                if found:break
            if found is None:raise RuntimeError(f'{role} cannot load optimistic source {eid} for {a}')
            expect=found['version']
        payload['expected_version']=expect
    return http('/api/action','POST',payload,login(role))
def task(role,task_type=None,source_type=None,source_id=None,status='Open'):
    st,j=http('/api/tasks?patient='+PID,token=login(role));assert st==200,(role,st,j)
    for x in reversed(j.get('tasks',[])):
        if status and x.get('status')!=status:continue
        if task_type and x.get('task_type')!=task_type:continue
        if source_type and x.get('source_type')!=source_type:continue
        if source_id and x.get('source_id')!=source_id:continue
        return x
    return None
def source(role,tid):return http('/api/task-source?task='+urllib.parse.quote(tid),token=login(role))
def check(name,ok,detail=None):
    rows.append({'check':name,'pass':bool(ok),'detail':detail});print(('PASS' if ok else 'FAIL'),name,json.dumps(detail,ensure_ascii=False,default=str)[:900] if detail is not None else '')
    if not ok:raise AssertionError(name+' '+str(detail))

def diagnostic_radiology(label,findings,impression,dt,catalog_name='CT chest/abdomen/pelvis'):
    st,j=action('Medical Oncology','create_diagnostic_order','',{'type':'Radiology','name':catalog_name,'indication':'Synthetic RECIST assessment','decision_reason':'Baseline/interval RECIST imaging for synthetic validation','date':TODAY});check('AN-RAD-order-'+label,st==200,j);oid=j['id']
    st,j=action('Biller','record_payment',oid,{'payment_status':'Waived','amount':0,'reason':'Synthetic validation'});check('AN-RAD-pay-'+label,st==200,j)
    st,j=action('Radiology Coordinator','schedule_radiology',oid,{'schedule':dt});check('AN-RAD-schedule-'+label,st==200,j)
    st,j=action('Radiology Technician','perform_radiology',oid,{'performed_at':dt});check('AN-RAD-perform-'+label,st==200,j);rid=j['radiology_entity_id']
    st,j=action('Radiologist','save_radiology',rid,{'finalize':True,'study':label,'date':TODAY,'findings':findings,'impression':impression});check('AN-RAD-final-'+label,st==200 and j.get('status')=='Final',j)
    return rid

def lab_result(tag,anc=3.2,egfr=94,lvef=60):
    st,j=action('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','name':'Comprehensive metabolic panel','indication':'Systemic treatment readiness '+tag,'decision_reason':'Pre-cycle readiness labs for synthetic validation','date':TODAY});check('AN-LAB-order-'+tag,st==200,j);oid=j['id']
    st,j=action('Biller','record_payment',oid,{'payment_status':'Waived','amount':0,'reason':'Synthetic validation'});check('AN-LAB-pay-'+tag,st==200,j)
    st,j=action('Laboratory / Phlebotomy','collect_sample',oid,{'sample_id':'SMP-'+tag,'collected_at':TODAY+'T07:30:00+05:30'});check('AN-LAB-collect-'+tag,st==200,j);rid=j['lab_entity_id']
    units={'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','lvef':'%'}
    st,j=action('Laboratory / Phlebotomy','save_lab',rid,{'finalize':True,'date':TODAY,'hb':11.8,'wbc':5.5,'anc':anc,'platelets':235,'creatinine':0.8,'egfr':egfr,'bilirubin':0.6,'ast':23,'alt':25,'lvef':lvef,'pregnancy':'Negative','units':units,'specimen':'Peripheral venous blood','collected_at':TODAY+'T07:30:00+05:30'});check('AN-LAB-final-'+tag,st==200 and j.get('status')=='Final',j);return rid

def prepare_release(order_id,phid,cycle):
    st,fm=http('/api/formulary',token=login('Oncology Pharmacy'));check(f'AN-C{cycle}-formulary',st==200 and fm.get('items'),{'count':len(fm.get('items',[]))});fmap={x.get('drug'):x for x in fm['items'] if x.get('status')=='Active'}
    ph=entity('Oncology Pharmacy','pharmacy',phid);prep=[]
    for idx,src in enumerate(ph['data']['items'],1):
        fi=fmap[src['drug']];form=fi['formulations'][0]
        prep.append({**src,'formulation':form['label'],'formulation_strength_mg':form['strength_mg'],'prepared_dose':src['final_approved_dose'],'route':src['route'],'diluent':src.get('diluent'),'batch':f'PC8-C{cycle}-{idx}','expiry':'2027-03-31','prepared_by':'Priya Nair — Oncology Pharmacist','actual_volume_ml':(src.get('volume_ml') or 0) if src['route']=='IV' else 0,'actual_volume_unit':'mL'})
    st,j=action('Oncology Pharmacy','pharmacy_prepare',phid,{'items':prep,'preparation_note':f'Synthetic cycle {cycle} preparation'});check(f'AN-C{cycle}-pharmacy-prepare',st==200 and j.get('status')=='Dispensing Pending',j)
    rel=[{**x,'second_check_by':'Demo Independent Pharmacist B','label_verified':True} for x in prep]
    st,j=action('Oncology Pharmacy','pharmacy_release',phid,{'items':rel,'dispensed_to':'Day Care / Infusion','manifest_no':f'MAN-PC8-C{cycle}'});check(f'AN-C{cycle}-pharmacy-release',st==200 and j.get('status')=='Dispensed',j)

def administer_cycle(order_id,infid,cycle,base_dt,delayed_hours,docetaxel_variance=False):
    pat=boot('Day Care / Infusion Nurse')['patient'];checks={k:True for k in ['identity','order','consent','allergy','vitals','labs','access','pharmacy']}
    st,j=action('Day Care / Infusion Nurse','start_infusion',infid,{'checklist':checks,'identity_confirmation':{'name':pat['name'],'mrn':pat['mrn'],'dob':pat['dob']},'pre_vitals':{'bp':'118/72','hr':76,'rr':16,'temp':36.7,'spo2':99,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'}},'access':{'type':'Port','site':'Chest central access'},'bedside_verification':{'confirmed':True}});check(f'AN-C{cycle}-start-infusion',st==200,j)
    order=entity('Day Care / Infusion Nurse','treatment_order',order_id);items=sorted(order['data']['items'],key=lambda x:x['sequence']);cyt_end=None;peg=next((x for x in items if x.get('min_hours_after_cytotoxic')),None)
    check(f'AN-C{cycle}-peg-present',bool(peg),peg and {'drug':peg['drug'],'min_h':peg.get('min_hours_after_cytotoxic')})
    for idx,it in enumerate(items):
        at=base_dt+timedelta(minutes=idx*45);ended=at+timedelta(minutes=max(10,int(it.get('duration_min') or 10)))
        rec={'item_id':it['item_id'],'actual_dose':it['ordered_dose'],'actual_dose_unit':it.get('ordered_unit','mg'),'completion_status':'Administered','administration_datetime':at.isoformat(),'ended_at':ended.isoformat()}
        if it.get('route')=='IV':rec['actual_rate']=it.get('rate_ml_hr') or 0;rec['actual_rate_unit']='mL/h'
        if it.get('group') in ['Antineoplastic','Targeted Therapy']:
            rec['chairside_verification']={'verified_by':'Second RN — Synthetic','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
            cyt_end=ended if cyt_end is None or ended>cyt_end else cyt_end
        st,j=action('Day Care / Infusion Nurse','administer_item',infid,{'record':rec});check(f'AN-C{cycle}-MAR-{it["sequence"]}-{it["drug"]}',st==200,j)
    st,j=action('Day Care / Infusion Nurse','complete_infusion',infid,{'post_vitals':{'bp':'116/70','hr':78,'rr':16,'temp':36.8,'spo2':99,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'}},'tolerance':'Treatment completed without serious reaction','discharge_instructions':'Return for next cycle per readiness; call for fever or urgent symptoms.','next_cycle':f'Cycle {cycle+1} review'});check(f'AN-C{cycle}-main-complete',st==200,j)
    inf=entity('Day Care / Infusion Nurse','infusion',infid);check(f'AN-C{cycle}-infusion-completed',inf['status']=='Completed' and len(inf['data'].get('mar',[]))==len(items),{'status':inf['status'],'mar':len(inf['data'].get('mar',[])),'items':len(items)})
    t=task('Medical Oncology','Next-cycle decision','infusion',infid);check(f'AN-C{cycle}-MO-next-cycle-task',bool(t),t);st,src=source('Medical Oncology',t['id']);check(f'AN-C{cycle}-MO-opens-MAR-provenance',st==200 and src.get('source_record_id')==infid and src.get('source_record',{}).get('status')=='Completed',src)
    mar=inf['data']['mar'];carb=next(x for x in mar if x.get('drug')=='Carboplatin');check(f'AN-C{cycle}-actual-dose-recorded',carb.get('actual_dose') is not None,carb)
    return inf,cyt_end

# Clinical spine
reg=entity('Front Desk','registration');check('AN-001 baseline registration',bool(reg),reg and reg['id'])
st,j=action('Front Desk','save_registration',reg['id'],{'name':'Ananya Shah','dob':'1987-04-18','sex':'Female','phone':'917000000101','id_number':'SYN-ANANYA-01','assigned_specialty':'Medical Oncology','complete':True});check('AN-002 registration complete',st==200,j)
ref=entity('Front Desk','referral');st,j=action('Front Desk','save_referral',ref['id'],{'status':'Assigned','assigned_department':'Medical Oncology','assigned_clinician':'Dr Asha Mehta','priority':'Routine'});check('AN-003 referral assigned',st==200,j)
t=task('Medical Oncology','Referral lifecycle','referral',ref['id']);check('AN-004 MO referral task',bool(t),t);st,src=source('Medical Oncology',t['id']);check('AN-005 referral exact source',st==200 and src.get('source_record_id')==ref['id'],src)
st,j=action('Medical Oncology','save_referral',ref['id'],{'status':'Accepted'});check('AN-006 referral accepted',st==200 and j.get('status')=='Accepted',j)
intake=entity('Intake Nurse','intake');st,j=action('Intake Nurse','save_intake',intake['id'],{'complete':True,'sbp':118,'dbp':72,'hr':74,'rr':16,'temp':36.7,'spo2':99,'weight':68,'height':165,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'ecog':'1','kps':'90','pain_score':1,'pain_instrument':'Numeric Rating Scale 0–10','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':1,'nkda':True,'measured_at':TODAY+'T08:00:00+05:30'});check('AN-007 intake signed',st==200,j)
cons=entity('Medical Oncology','consultation');st,j=action('Medical Oncology','save_consultation',cons['id'],{'sign':True,'encounter_type':'New Medical Oncology Consultation','date':TODAY,'chief_complaint':'New HER2-positive left breast cancer for neoadjuvant systemic therapy planning','hpi':'Core biopsy confirms invasive breast carcinoma; staging evaluation shows clinically node-positive, non-metastatic disease.','ros':'No fever, dyspnoea, active infection or cardiac symptoms.','assessment':'HER2-positive left breast cancer, cT2 cN1 cM0, AJCC Breast v8 Stage IIB.','plan':'Complete MDT review and proceed with governed synthetic neoadjuvant systemic therapy after readiness checks.','physical_exam_structured':{'general':'ECOG 1, clinically stable','cardiovascular':'Normal heart sounds','respiratory':'Clear bilateral air entry','abdomen':'Soft, non-tender','neurologic':'No focal deficit','tumor_site':'Left upper-outer breast lesion with ipsilateral axillary adenopathy'}});check('AN-008 consultation signed',st==200,j)
dx=entity('Medical Oncology','diagnosis');st,j=action('Medical Oncology','save_diagnosis',dx['id'],{'verify':True,'icd10':'C50.4','icd10_version':'ICD-10','icdo_topography':'C50.4','icdo_morphology':'8500/3','icdo_version':'ICD-O-3','cancer_type':'Breast Cancer','primary_site':'Left breast upper-outer quadrant','histology':'Invasive carcinoma of no special type','grade':'3','staging_system':'AJCC','staging_version':'Breast v8','staging_date':TODAY,'staging_basis':'Clinical','stage_t':'cT2','stage_n':'cN1','stage_m':'cM0','stage_group':'Stage IIB','treatment_intent':'Neoadjuvant','disease_status':'Newly diagnosed','biomarkers':[{'name':'ER','value':'Negative','method':'IHC','date':TODAY},{'name':'PR','value':'Negative','method':'IHC','date':TODAY},{'name':'HER2','value':'3+ Positive','method':'IHC','date':TODAY}]});check('AN-009 diagnosis verified',st==200 and j.get('status')=='Verified',j)
conrec=entity('Front Desk','consent');st,j=action('Front Desk','consent_action',conrec['id'],{'operation':'sign','type':'General Consent','version':'PC8-SYN-1','scope':'Synthetic diagnostic evaluation and imaging','signed_by':'Ananya Shah — synthetic validation patient','valid_from':TODAY});check('AN-010 general diagnostic consent signed',st==200,j)
base_rad=diagnostic_radiology('Baseline CT chest/abdomen/pelvis','Left breast lesion 40 mm; left axillary target node short axis 18 mm; no distant metastasis.','Measurable left breast primary and axillary nodal disease; no distant metastatic disease.',TODAY+'T09:00:00+05:30')
resp=entity('Radiologist','response');st,j=action('Radiologist','save_response_baseline',resp['id'],{'date':TODAY,'source_study_id':base_rad,'target_lesions':[{'id':'L1','organ':'Breast','site':'Left breast primary','lesion_type':'Non-nodal','size_mm':40},{'id':'L2','organ':'Lymph nodes','site':'Left axillary node short axis','lesion_type':'Lymph node','size_mm':18}],'non_target':'No unequivocal non-target progression'});check('AN-011 RECIST baseline frozen',st==200 and j.get('baseline',{}).get('sum_mm')==58.0,j)
st,j=action('Medical Oncology','submit_mdt_case','',{'clinical_question':'Confirm neoadjuvant systemic treatment strategy for HER2-positive Stage IIB breast cancer.','clinical_summary':'Left breast invasive carcinoma, ER-/PR-/HER2 IHC 3+, cT2 cN1 cM0 AJCC Breast v8 Stage IIB, ECOG 1.','meeting_mode':'Internal','meeting_at':TODAY+'T10:00:00+05:30'});check('AN-012 MDT submitted',st==200,j);mdt_id=j['mdt_id']
collab=entity('MDT Coordinator','mdt_collab')
for idx,(name,disc) in enumerate([('Dr Asha Mehta','Medical Oncology'),('Dr Neha Rao','Radiation Oncology'),('Dr Karan Shah','Surgical Oncology'),('Dr Rohan Kulkarni','Radiology'),('Dr Mira Desai','Pathology')],1):
    st,j=action('MDT Coordinator','mdt_attendance',collab['id'],{'name':name,'discipline':disc,'status':'Present'});check(f'AN-013.{idx} MDT attendance {disc}',st==200,j);collab=entity('MDT Coordinator','mdt_collab')
st,j=action('MDT Coordinator','mdt_recommend',mdt_id,{'meeting_at':TODAY+'T10:00:00+05:30','clinical_question':'Confirm neoadjuvant systemic treatment strategy for HER2-positive Stage IIB breast cancer.','clinical_summary':'HER2-positive cT2 cN1 cM0 left breast cancer, ECOG 1.','intent':'Neoadjuvant','recommendation':'Proceed with governed synthetic HER2-targeted neoadjuvant systemic regimen with cycle-specific readiness and multidisciplinary reassessment.','rationale':'Multidisciplinary consensus for product-validation pathway.','final_consensus':'Consensus','specialty_responsible':'Medical Oncology'});check('AN-014 MDT coordinator recommendation',st==200 and j.get('status')=='Pending Chair Approval',j)
t=task('MDT Chair','MDT case preparation','mdt',mdt_id);check('AN-015 Chair task',bool(t),t);st,j=action('MDT Chair','mdt_chair_sign',mdt_id,{'decision':'Approve','reason':'Recommendation reflects multidisciplinary consensus.'});check('AN-016 Chair signs MDT',st==200 and j.get('status')=='MDT Recommended',j)
st,j=action('Medical Oncology','create_plan_from_mdt',mdt_id,{'specialty':'Medical Oncology'});check('AN-017 plan created',st==200,j);plan_id=j['id']
st,j=action('Medical Oncology','save_treatment_plan',plan_id,{'sign':True,'line_of_therapy':'Neoadjuvant first-line systemic therapy'});check('AN-018 plan signed',st==200 and j.get('status')=='Clinician Approved',j)
conrec=entity('Front Desk','consent');st,j=action('Front Desk','consent_action',conrec['id'],{'operation':'sign','type':'Treatment Consent','version':'PC8-SYN-1','scope':'Synthetic neoadjuvant systemic treatment','signed_by':'Ananya Shah — synthetic validation patient','valid_from':TODAY});check('AN-018B systemic Treatment Consent signed',st==200,j)
medrec=entity('Medical Oncology','med_recon');st,j=action('Medical Oncology','med_recon',medrec['id'],{'operation':'set_allergy_status','allergy_status':'No known allergy'});check('AN-018C allergy status set',st==200,j)
medrec=entity('Medical Oncology','med_recon');st,j=action('Medical Oncology','med_recon',medrec['id'],{'operation':'reconcile','reconciliation_status':'Complete','source':'Patient'});check('AN-018D medication reconciliation complete',st==200,j)
lab1=lab_result('AN-C1',3.2,94,60)
ready=entity('Medical Oncology','readiness');st,j=action('Medical Oncology','save_readiness',ready['id'],{'template_id':'REG-CCA-TCHP-DEMO','cycle':1,'day':1,'decision':'Proceed as Planned','decision_reason':'All configured readiness criteria met','sign':True,'evaluation_as_of_date':TODAY,'toxicity_summary':'No treatment-limiting toxicity'});check('AN-019 C1 readiness signed without renal dose context',st==200,j)
st,j=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan_id,'cycle':1,'day':1,'start_date':TODAY,'administration_setting':'Day Care'});check('AN-020 unresolved AUC fails closed',st==409,j)
ready2=entity('Medical Oncology','readiness');st,j=action('Medical Oncology','save_readiness',ready2['id'],{'template_id':'REG-CCA-TCHP-DEMO','cycle':1,'day':1,'decision':'Proceed as Planned','decision_reason':'All configured readiness criteria met with renal dosing context','sign':True,'evaluation_as_of_date':TODAY,'renal_dosing_method':'CCA-approved renal dosing value','renal_dosing_value_ml_min':94,'renal_dosing_source_id':lab1,'renal_dosing_measured_at':TODAY+'T08:00:00+05:30','toxicity_summary':'No treatment-limiting toxicity'});check('AN-021 C1 readiness with renal context',st==200,j)
st,j=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan_id,'cycle':1,'day':1,'start_date':TODAY,'administration_setting':'Day Care','doses':{'DEMO-CARBO':6000},'variance_reasons':{'DEMO-CARBO':'Deliberate overdose attack'}});check('AN-022 6000mg Carboplatin blocked',st==409,j)
st,j=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan_id,'cycle':1,'day':1,'start_date':TODAY,'administration_setting':'Day Care','renal_dosing':{'DEMO-CARBO':{'method':'CCA-approved renal dosing value','value_ml_min':94,'source_id':lab1,'measured_at':TODAY+'T08:00:00+05:30'}},'administration_decision_reason':'Clinician accepts protocol route/diluent/volume/rate/duration as configured','schedule_decision_reason':'Clinician accepts protocol-derived administration schedule','dose_decision_reasons':{'*':'Clinician accepts calculated dose after independent review'}});check('AN-023 C1 safe order created',st==200,j);order1,ph1,inf1=j['order_id'],j['pharmacy_id'],j['infusion_id']
o1=entity('Medical Oncology','treatment_order',order1);carb=next(x for x in o1['data']['items'] if x['drug']=='Carboplatin');check('AN-024 Calvert AUC calculated 714mg',abs(float(carb['calculated_dose'])-714.0)<0.01,carb)
st,j=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan_id,'cycle':1,'day':1,'start_date':TODAY});check('AN-025 duplicate C1 order blocked',st==409,j)
st,j=action('Biller','create_order','',{'cycle':1,'day':1});check('AN-026 wrong role order blocked',st==403,j)
checks={k:True for k in ['patient_identity','allergy','regimen_version','cycle_day','dose_basis','calculated_dose','ordered_dose','dose_variance','renal_adjustment','hepatic_adjustment','cumulative_dose','interaction','duplication','route','diluent','final_concentration','stock','expiry']}
st,j=action('Oncology Pharmacy','pharmacy_decision',ph1,{'decision':'Verified','verification_checks':checks});check('AN-027 pharmacy independent recalculation',st==200,j)
prepare_release(order1,ph1,1)
inf,c1_end=administer_cycle(order1,inf1,1,datetime.fromisoformat(TODAY+'T09:00:00+05:30'),24)
tex=entity('Day Care / Infusion Nurse','toxicity');st,j=action('Day Care / Infusion Nurse','record_toxicity',tex['id'],{'term':'Peripheral sensory neuropathy','grade':'2','onset_date':'2026-09-09','attribution':'Probable','suspected_agents':['Docetaxel'],'seriousness':{},'outcome':'Ongoing','action_taken':'Clinical review before next cycle','cycle':1});check('AN-028 CTCAE G2 toxicity recorded',st==200,j);toxid=j['id']
st,j=action('Medical Oncology','post_cycle_review',inf1,{'decision':'Modify','clinical_reason':'Grade 2 peripheral sensory neuropathy; reduce Docetaxel 10% for next cycle.','toxicity_event_ids':[toxid],'next_cycle':2});check('AN-029 post-cycle Modify decision',st==200,j)
mod=entity('Medical Oncology','modification');st,j=action('Medical Oncology','create_modification',mod['id'],{'original_order_id':order1,'reason':'CTCAE Grade 2 peripheral sensory neuropathy','modification_type':'Dose reduction','clinical_justification':'Reduce Docetaxel 10% for Cycle 2 while continuing other agents per synthetic protocol.'});check('AN-030 modification linked to C1 order',st==200,j);modid=j['id']
lab2=lab_result('AN-C2',2.8,94,60)
ready=entity('Medical Oncology','readiness');st,j=action('Medical Oncology','save_readiness',ready['id'],{'template_id':'REG-CCA-TCHP-DEMO','cycle':2,'day':1,'decision':'Proceed with Modification','decision_reason':'Approved Docetaxel 10% reduction for Grade 2 neuropathy','sign':True,'evaluation_as_of_date':TODAY,'renal_dosing_method':'CCA-approved renal dosing value','renal_dosing_value_ml_min':94,'renal_dosing_source_id':lab2,'renal_dosing_measured_at':TODAY+'T08:00:00+05:30'});check('AN-031 C2 modified readiness signed',st==200 and j.get('status')=='Signed',j)
st,j=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan_id,'cycle':2,'day':1,'start_date':TODAY,'administration_setting':'Day Care','doses':{'DEMO-DOC':119.17},'variance_reasons':{'DEMO-DOC':'Approved 10% reduction for CTCAE Grade 2 neuropathy'},'renal_dosing':{'DEMO-CARBO':{'method':'CCA-approved renal dosing value','value_ml_min':94,'source_id':lab2,'measured_at':TODAY+'T08:00:00+05:30'}},'modification_id':modid,'administration_decision_reason':'Clinician accepts protocol route/diluent/volume/rate/duration as configured','schedule_decision_reason':'Clinician accepts protocol-derived administration schedule','dose_decision_reasons':{'*':'Clinician accepts calculated/modified dose after independent review'}});check('AN-032 C2 modified order created',st==200,j);order2,ph2,inf2=j['order_id'],j['pharmacy_id'],j['infusion_id']
o2=entity('Medical Oncology','treatment_order',order2);doc=next(x for x in o2['data']['items'] if x['drug']=='Docetaxel');carb2=next(x for x in o2['data']['items'] if x['drug']=='Carboplatin');check('AN-033 C2 Docetaxel reduction',abs(float(doc['ordered_dose'])-119.17)<0.01,{'docetaxel':doc})
st,j=action('Oncology Pharmacy','pharmacy_decision',ph2,{'decision':'Verified','verification_checks':checks});check('AN-034 C2 pharmacy independent recalculation',st==200,j);prepare_release(order2,ph2,2)
inf2rec,c2_end=administer_cycle(order2,inf2,2,datetime.fromisoformat('2026-09-10T09:00:00+05:30'),25)
st,j=action('Medical Oncology','post_cycle_review',inf2,{'decision':'Proceed','clinical_reason':'Cycle 2 completed; neuropathy stable after dose reduction; assess counts for Cycle 3.','next_cycle':3});check('AN-035 C2 post-cycle Proceed',st==200,j)
lab3=lab_result('AN-C3-LOWANC',0.9,94,60)
ready=entity('Medical Oncology','readiness');st,j=action('Medical Oncology','save_readiness',ready['id'],{'template_id':'REG-CCA-TCHP-DEMO','cycle':3,'day':1,'decision':'Delay','decision_reason':'ANC below governed synthetic readiness threshold; repeat CBC before treatment.','reevaluation_date':'2026-09-10','sign':True,'evaluation_as_of_date':TODAY,'renal_dosing_method':'CCA-approved renal dosing value','renal_dosing_value_ml_min':94,'renal_dosing_source_id':lab3,'renal_dosing_measured_at':TODAY+'T08:00:00+05:30'});check('AN-036 C3 low ANC Delay signed',st==200 and j.get('status')=='Signed',j)
st,j=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan_id,'cycle':3,'day':1,'start_date':TODAY});check('AN-037 C3 order blocked by delayed readiness',st==409,j)
fu_rad=diagnostic_radiology('Follow-up CT response assessment','Left breast target lesion 26 mm; left axillary node short axis 12 mm; no new lesion.','Interval reduction in measurable disease; RECIST assessment recommended.',TODAY+'T16:00:00+05:30')
resp=entity('Radiologist','response');st,j=action('Radiologist','save_response',resp['id'],{'date':TODAY,'source_study_id':fu_rad,'target_lesions':[{'id':'L1','organ':'Breast','site':'Left breast primary','lesion_type':'Non-nodal','size_mm':26},{'id':'L2','organ':'Lymph nodes','site':'Left axillary node short axis','lesion_type':'Lymph node','size_mm':12}],'new_lesions':False,'non_target':'Non-target disease: non-CR/non-PD','notes':'Synthetic follow-up response assessment'});check('AN-038 Radiologist proposes RECIST',st==200,j);assid=j['assessment']['id']
t=task('Medical Oncology','Response confirmation','response',resp['id']);check('AN-039 MO response confirmation task',bool(t),t);st,src=source('Medical Oncology',t['id']);check('AN-040 MO opens exact response source',st==200 and src.get('source_record_id')==resp['id'],src)
st,j=action('Medical Oncology','confirm_response',resp['id'],{'assessment_id':assid,'response_category':'Partial response','reason':'Continue multidisciplinary systemic strategy after count recovery; delayed Cycle 3 requires repeat CBC.'});check('AN-041 MO confirms response',st==200,j)
c=sqlite3.connect(ROOT/'cca_v12.sqlite3');c.row_factory=sqlite3.Row;aud=[dict(x) for x in c.execute('SELECT actor_id,actor_role,action,entity_type,entity_id,at FROM audit WHERE patient_id=? ORDER BY id',(PID,))];c.close();wanted={'CONSULTATION_SIGN','DIAGNOSIS_VERIFY','MDT_CHAIR_APPROVE','PLAN_SIGN','READINESS_SIGN','ORDER_EXECUTION_COMPLETE','POST_CYCLE_REVIEW','RESPONSE_CONFIRM'};got={x.get('action') for x in aud};check('AN-042 named audit chain contains systemic milestones',wanted.issubset(got),sorted(got))
task_all=http('/api/tasks?patient='+PID,token=login('Medical Oncology'))[1].get('tasks',[]);completed_next=[x for x in task_all if x.get('task_type')=='Next-cycle decision'];check('AN-043 next-cycle tasks persisted',len(completed_next)>=2,[{k:x.get(k) for k in ['id','status','source_type','source_id']} for x in completed_next])
out={'patient_id':PID,'patient':'Ananya Shah','build':'12.2-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(1 for x in rows if x['pass']),'fail':sum(1 for x in rows if not x['pass']),'results':rows,'key_records':{'mdt':mdt_id,'treatment_plan':plan_id,'baseline_radiology':base_rad,'cycle1_order':order1,'cycle1_infusion':inf1,'cycle2_order':order2,'cycle2_infusion':inf2,'cycle3_lab':lab3,'followup_radiology':fu_rad,'response_assessment':assid}}
(ROOT/'validation_evidence'/'PC8_ANANYA_SYSTEMIC_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail','key_records']},ensure_ascii=False));sys.exit(1 if out['fail'] else 0)
