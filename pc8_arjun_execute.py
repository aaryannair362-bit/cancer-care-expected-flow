#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download, targeting this repo's
# PAT-VAL-ARJUN validation patient (same "Arjun Mehta" synthetic identity, distinct id/mrn
# from the pre-existing PAT-DEMO-SURG showcase patient).
#
# Substantially rewritten versus the PC8.0 original because this repo's actual action set
# differs in ways discovered by reading server.py directly (not just field renames):
#  - save_consultation and create_diagnostic_order are hard-restricted to role=='Medical
#    Oncology' only. Surgical Oncology cannot sign the initial consultation or order pre-op
#    labs. So referral/consultation/diagnosis/pre-op-lab-ordering are done by Medical
#    Oncology (the triage oncologist), who hands off to Surgical Oncology via the MDT
#    Chair's specialty_responsible grant -- same pattern used in pc8_neha_rt_execute.py.
#  - submit_mdt_case returns no next_role key; mdt_recommend's real status string is
#    'Pending Chair Approval' (not 'Awaiting Chair Signature'); mdt_chair_sign takes
#    {'decision':'Approve'|'Return for revision','reason':...} (not {'attestation':...}) and
#    the resulting status is 'MDT Recommended' (not 'MDT Signed').
#  - surgery_sign_plan, in this repo's original (unmodified-until-this-merge) code, only
#    granted Surgical Nurse access -- it did not hand off to Patient Liaison/Anaesthetist/
#    Blood Bank the way the "connected multidisciplinary" pitch requires. Likewise
#    surgery_performed only granted 'Pathology' access, never 'Pathology Technologist' (the
#    new PRD role Phase 2 added), and never notified Stoma/Wound Nurse post-op. These were
#    genuine pre-existing wiring gaps (the same class of gap already found and fixed for
#    admit_patient/inpatient_specialty_review while porting the Ravi journey) and have been
#    fixed additively in server.py as part of this port: surgery_sign_plan now also hands off
#    to Patient Liaison ('Surgical consent'), Anaesthetist and Blood Bank / Transfusion
#    ('Support service referral'); surgery_performed now also grants Pathology Technologist
#    access + hands off 'Pathology accession', and hands off 'Support service referral' to
#    Stoma / Wound Nurse. The downstream pathology_processing -> Pathology handoff on
#    ready_for_pathologist=True already existed in save_support_record and needed no change.
#  - surgery_preop's actual readiness gate checks preop.anesthesia_clearance/labs/consent
#    (each =='Complete'), not the PC8.0 field names (identity_confirmed etc.) -- those extra
#    fields are harmless but do not drive the ready computation.
#  - surgery_pathology_link requires postop_stage/margin_status/nodes_examined/nodes_positive
#    in the SAME call (PC8.0's original omitted them) and its response key is
#    pathological_stage_record_id, not source_pathology_record_id.
#  - save_pathology in this repo did not gate finalize on prior Pathology Technologist
#    processing, and had no node-count coherence check; the latter (nodes_positive cannot
#    exceed nodes_examined) was added additively in server.py as a pure data-quality guard
#    since it can never reject genuinely valid data. The former was deliberately NOT added
#    as a hard gate (it would change existing save_pathology behavior for every patient,
#    risking the legacy regression baseline), so the "blocked before processing" negative
#    check from the PC8.0 original has no equivalent here and is omitted; processing is still
#    exercised as a real, ordered workflow step.
import json,urllib.request,urllib.error,urllib.parse,pathlib,sys,os
from datetime import date,datetime,timezone,timedelta
ROOT=pathlib.Path(__file__).resolve().parent;BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765');PID='PAT-VAL-ARJUN';TODAY='2026-09-09';rows=[];TOK={}
creds={}
for line in (ROOT/'DEMO_USER_CREDENTIALS.txt').read_text(encoding='utf-8').splitlines():
    if ' | ' in line:
        u,p,n,r=[x.strip() for x in line.split(' | ',3)];creds[r]=(u,p,n)
def http(path,method='GET',data=None,token=None):
    h={'Content-Type':'application/json'}
    if token:h['Authorization']='Bearer '+token
    body=json.dumps(data).encode() if data is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE+path,data=body,headers=h,method=method),timeout=15) as r:return r.status,json.loads(r.read().decode() or '{}')
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
OPT={'save_intake','med_recon','save_dynamic_form','save_consultation','save_diagnosis','save_appointment','queue_patient','save_care_plan','save_treatment_plan','save_radiology','save_pathology','mdt_comment','mdt_attendance','mdt_recommend','save_referral'}
def action(role,a,eid='',data=None):
    payload={'action':a,'patient_id':PID,'entity_id':eid,'data':data or {}}
    if a in OPT and eid:
        found=None
        for xs in boot(role).get('entities',{}).values():
            for x in xs:
                if x['id']==eid:found=x;break
            if found:break
        if found:payload['expected_version']=found['version']
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
def source(role,tid):
    st,j=http('/api/task-source?task='+urllib.parse.quote(tid),token=login(role));return st,j
def check(name,ok,detail=None):
    rows.append({'check':name,'pass':bool(ok),'detail':detail})
    print(('PASS' if ok else 'FAIL'),name,json.dumps(detail,ensure_ascii=False,default=str)[:900] if detail is not None else '')
    if not ok:raise AssertionError(name+' '+str(detail))

# 1 registration / referral (MO triage) / intake / consultation / diagnosis
reg=entity('Front Desk','registration');check('ARJ-001 baseline registration available',bool(reg),reg and reg['id'])
st,j=action('Front Desk','save_registration',reg['id'],{'name':'Arjun Mehta','dob':'1965-11-20','sex':'Male','phone':'917000000103','id_number':'SYN-ARJUN-01','assigned_specialty':'Surgical Oncology','complete':True});check('ARJ-002 registration complete',st==200,j)
ref=entity('Front Desk','referral');st,j=action('Front Desk','save_referral',ref['id'],{'status':'Assigned','assigned_department':'Medical Oncology','assigned_clinician':'Dr Asha Mehta','priority':'Routine'});check('ARJ-003 referral assigned to MO triage',st==200 and j.get('status')=='Assigned',j)
t=task('Medical Oncology','Referral lifecycle',source_id=ref['id']);check('ARJ-004 MO receives referral task',bool(t),t)
st,src=source('Medical Oncology',t['id']);check('ARJ-005 referral exact source/provenance',st==200 and src.get('source_record_id')==ref['id'],src)
st,j=action('Medical Oncology','save_referral',ref['id'],{'status':'Accepted'});check('ARJ-006 referral accepted by MO',st==200 and j.get('status')=='Accepted',j)
intake=entity('Intake Nurse','intake');st,j=action('Intake Nurse','save_intake',intake['id'],{'sbp':128,'dbp':76,'hr':74,'rr':16,'temp':36.7,'spo2':99,'weight':76,'height':173,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'ecog':'1','kps':'90','pain_score':1,'pain_instrument':'Numeric Rating Scale 0–10','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':1,'nkda':True,'complete':True});check('ARJ-007 intake signed',st==200 and j.get('bsa_m2',0)>0,j)
cons=entity('Medical Oncology','consultation');st,j=action('Medical Oncology','save_consultation',cons['id'],{'sign':True,'encounter_type':'New Oncology Consultation','date':TODAY,'chief_complaint':'Recently diagnosed sigmoid colon cancer for surgical evaluation','hpi':'Altered bowel habit and intermittent lower abdominal discomfort; colonoscopy biopsy confirms adenocarcinoma.','ros':'No active bleeding, fever, chest pain or dyspnea.','assessment':'Resectable sigmoid colon adenocarcinoma; clinical Stage IIIB pending multidisciplinary confirmation.','plan':'Complete staging review, MDT discussion and curative surgical planning.','physical_exam_structured':{'general':'Comfortable, ECOG 1','cardiovascular':'S1 S2 normal','respiratory':'Clear bilateral air entry','abdomen':'Soft, non-peritonitic; mild left lower quadrant tenderness','neurologic':'No focal deficit','tumor_site':'No palpable abdominal mass'}});check('ARJ-008 MO consultation signed',st==200 and j.get('status')=='Signed',j)
dx=entity('Medical Oncology','diagnosis');st,j=action('Medical Oncology','save_diagnosis',dx['id'],{'verify':True,'icd10':'C18.7','icd10_version':'ICD-10','icdo_topography':'C18.7','icdo_morphology':'8140/3','icdo_version':'ICD-O-3','cancer_type':'Colon Cancer','primary_site':'Sigmoid colon','histology':'Adenocarcinoma','grade':'2','staging_system':'AJCC','staging_version':'Colon/Rectum v8','staging_date':TODAY,'staging_basis':'Clinical','stage_t':'cT3','stage_n':'cN1','stage_m':'cM0','stage_group':'Stage IIIB','treatment_intent':'Curative','disease_status':'Newly diagnosed'});check('ARJ-009 clinical diagnosis/staging verified',st==200 and j.get('status')=='Verified',j)
clinical_dx_id=dx['id']

# 2 MDT coordinator -> chair -> plan (specialty_responsible = Surgical Oncology)
st,j=action('Medical Oncology','submit_mdt_case','',{'clinical_question':'Confirm resectability and curative surgical sequence for sigmoid colon adenocarcinoma.','clinical_summary':'Sigmoid colon adenocarcinoma, cT3 cN1 cM0 AJCC v8 Stage IIIB, ECOG 1; no distant metastatic disease identified in synthetic validation context.','meeting_mode':'Internal','meeting_at':TODAY+'T10:00:00+05:30'});check('ARJ-010 MDT submitted',st==200 and j.get('status')=='Submitted',j);mdt_id=j['mdt_id']
att=[('Dr Asha Mehta','Medical Oncology'),('Dr Neha Rao','Radiation Oncology'),('Dr Karan Shah','Surgical Oncology'),('Dr Rohan Kulkarni','Radiology'),('Dr Mira Desai','Pathology')]
collab=entity('MDT Coordinator','mdt_collab')
for idx,(name,disc) in enumerate(att,1):
    st,j=action('MDT Coordinator','mdt_attendance',collab['id'],{'name':name,'discipline':disc,'status':'Present'});check(f'ARJ-011.{idx} MDT attendance {disc}',st==200,j);collab=entity('MDT Coordinator','mdt_collab')
st,j=action('MDT Coordinator','mdt_recommend',mdt_id,{'meeting_at':TODAY+'T10:00:00+05:30','clinical_question':'Confirm resectability and curative surgical sequence for sigmoid colon adenocarcinoma.','clinical_summary':'Sigmoid colon adenocarcinoma, cT3 cN1 cM0 AJCC v8 Stage IIIB, ECOG 1.','intent':'Curative','recommendation':'Proceed with curative laparoscopic sigmoid colectomy after anaesthesia and pre-operative clearance; review final histopathology for adjuvant systemic therapy.','rationale':'Synthetic MDT consensus based on resectable disease and no distant metastasis.','final_consensus':'Consensus','specialty_responsible':'Surgical Oncology','actions':[{'description':'Arrange surgery after multidisciplinary pre-op clearance','owner_role':'Surgical Oncology','due_date':'2026-09-16','priority':'High'}]});check('ARJ-012 Coordinator recommendation awaiting Chair',st==200 and j.get('status')=='Pending Chair Approval',j)
t=task('MDT Chair','MDT case preparation',source_id=mdt_id);check('ARJ-013 Chair receives recommendation task',bool(t),t)
st,src=source('MDT Chair',t['id']);check('ARJ-014 Chair source is Coordinator record/provenance',st==200 and src.get('source_record_id')==mdt_id,src)
st,j=action('MDT Chair','mdt_chair_sign',mdt_id,{'decision':'Approve','reason':'Recommendation reflects multidisciplinary consensus and named action ownership.'});check('ARJ-015 Chair signs authoritative MDT',st==200 and j.get('status')=='MDT Recommended',j)
st,j=action('Surgical Oncology','create_plan_from_mdt',mdt_id,{'specialty':'Surgical Oncology'});check('ARJ-016 treatment plan created from signed MDT (SO now has access)',st==200 and j.get('status')=='Draft',j);plan_id=j['id']
st,j=action('Surgical Oncology','save_treatment_plan',plan_id,{'sign':True,'line_of_therapy':'Curative surgical management'});check('ARJ-017 surgical treatment plan signed',st==200 and j.get('status')=='Clinician Approved',j)

# 3 pre-op labs (MO orders; catalogue-governed name required)
st,j=action('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','catalog_id':'LAB-CMP','name':'Comprehensive metabolic panel','indication':'Pre-operative clearance before sigmoid colectomy','decision_reason':'Pre-operative renal/liver/metabolic clearance required before curative surgery','date':TODAY});check('ARJ-018 MO creates preop lab order',st==200,j);lab_order=j['id']
st,j=action('Biller','record_payment',lab_order,{'payment_status':'Waived','amount':0,'reason':'Synthetic validation pathway'});check('ARJ-019 lab payment/waiver clears',st==200,j)
st,j=action('Laboratory / Phlebotomy','collect_sample',lab_order,{'sample_id':'SMP-ARJUN-PREOP-01','collected_at':TODAY+'T11:00:00+05:30'});check('ARJ-020 preop sample collected',st==200,j);lab_id=j['lab_entity_id']
units={'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L'}
st,j=action('Laboratory / Phlebotomy','save_lab',lab_id,{'finalize':True,'date':TODAY,'hb':13.2,'wbc':6.4,'anc':3.4,'platelets':260,'creatinine':0.9,'egfr':88,'bilirubin':0.7,'ast':22,'alt':24,'units':units,'specimen':'Peripheral venous blood','collected_at':TODAY+'T11:00:00+05:30'});check('ARJ-021 final preop lab persisted',st==200 and j.get('status')=='Final',j)

# 4 surgical plan -> Patient Liaison consent + Anaesthetist + Blood Bank (all newly-wired handoffs)
surg=entity('Surgical Oncology','surgery');plan_payload={'procedure':'Laparoscopic sigmoid colectomy','indication':'Resectable sigmoid colon adenocarcinoma','intent':'Curative','site':'Sigmoid colon','laterality':'Not applicable','extent':'Segmental sigmoid colectomy with regional lymphadenectomy','approach':'Laparoscopic; convert to open if clinically required','nodal_procedure':'Regional mesenteric lymphadenectomy','reconstruction':'Primary colorectal anastomosis','planned_date':'2026-09-11','priority':'Routine','preop_requirements':['Anaesthesia fitness','Final CBC/renal/liver profile','Signed surgical consent','Blood availability'],'required_imaging_pathology':['Staging imaging reviewed','Diagnostic biopsy reviewed'],'anesthesia':'General anaesthesia','anesthesia_clearance':'Pending Anaesthetist assessment','blood_requirement':'2 units PRBC crossmatched'}
st,j=action('Surgical Oncology','surgery_sign_plan',surg['id'],plan_payload);check('ARJ-022 surgical plan signed',st==200,j)
ct=task('Patient Liaison','Surgical consent',source_id=surg['id']);check('ARJ-023 Liaison receives procedure-consent task',bool(ct),ct)
st,src=source('Patient Liaison',ct['id']);check('ARJ-024 Liaison opens signed Surgical Plan source',st==200 and src.get('source_record_id')==surg['id'],src)
consent=entity('Patient Liaison','consent');st,j=action('Patient Liaison','consent_action',consent['id'],{'operation':'sign','type':'Surgical Consent','version':'PC8-SYN-1','scope':'Laparoscopic sigmoid colectomy with possible conversion/open procedure and indicated nodal resection','signed_by':'Arjun Mehta — synthetic validation patient','valid_from':TODAY});check('ARJ-025 surgical consent signed',st==200,j)
t=task('Anaesthetist','Support service referral',source_id=surg['id']);check('ARJ-026 Anaesthetist receives surgery source',bool(t),t)
st,src=source('Anaesthetist',t['id']);check('ARJ-027 Anaesthetist can open signed Surgical Plan source',st==200 and src.get('source_record_id')==surg['id'] and src.get('source_visible_to_role') is True,src)
ana=entity('Anaesthetist','anaesthesia')
st,j=action('Surgical Oncology','save_support_record',ana['id'],{'record_type':'anaesthesia','sign':True,'assessment_date':TODAY,'asa_class':'II','airway_assessment':'Mallampati II','anesthesia_plan':'General','fitness_decision':'Fit'});check('ARJ-028 surgeon blocked from anaesthetist-owned record',st==403,j)
st,j=action('Anaesthetist','save_support_record',ana['id'],{'record_type':'anaesthesia','sign':True,'assessment_date':TODAY,'asa_class':'II','airway_assessment':'Mallampati II, adequate mouth opening, normal neck mobility','anesthesia_plan':'General anaesthesia with standard monitoring; epidural/analgesia per intra-operative assessment','fitness_decision':'Fit with conditions','restrictions':'Routine peri-operative cardiac monitoring'});check('ARJ-029 anaesthesia signed by owner',st==200 and j.get('status')=='Signed',j)
bb=entity('Blood Bank / Transfusion','blood_bank');t=task('Blood Bank / Transfusion','Support service referral',source_id=surg['id']);check('ARJ-030 Blood Bank receives readiness task',bool(t),t)
st,j=action('Blood Bank / Transfusion','save_support_record',bb['id'],{'record_type':'blood_bank','sign':True,'assessment_date':TODAY,'blood_group':'B Positive','antibody_screen':'Negative','crossmatch_status':'Crossmatched','availability_status':'Crossmatched / available','units_reserved':2});check('ARJ-031 Blood Bank signs availability',st==200 and j.get('status')=='Signed',j)

# 5 preop -> theatre -> operation
st,j=action('Surgical Nurse','surgery_preop',surg['id'],{'anesthesia_clearance':'Complete','labs':'Complete','consent':'Complete','identity_confirmed':True,'site_laterality_confirmed':True,'procedure_confirmed':True,'nurse_note':'All role-owned pre-operative prerequisites reviewed from authoritative sources.'});check('ARJ-032 preop nurse ready with source-owned clearances',st==200 and j.get('ready') is True,j)
st,j=action('Surgical Nurse','surgery_theatre_readiness',surg['id'],{'checklist':{'identity':True,'site_laterality':True,'procedure':True,'consent':True,'anaesthesia':True,'equipment':True,'blood_if_required':True,'counts_baseline':True},'theatre':'OT-2','scheduled_start':'2026-09-11T08:00:00+05:30','team_brief':'WHO Time-Out completed; specimen labelling plan reviewed.'});check('ARJ-033 theatre readiness signed',st==200 and j.get('status')=='Theatre Ready',j)
t=task('Surgical Oncology','Surgery execution',source_id=surg['id']);check('ARJ-034 surgeon receives operation task',bool(t),t)
st,j=action('Surgical Oncology','surgery_performed',surg['id'],{'actual_procedure':'Laparoscopic sigmoid colectomy with regional lymphadenectomy and primary colorectal anastomosis','operation_date_time':'2026-09-11T08:15:00+05:30','preop_diagnosis':'Sigmoid colon adenocarcinoma cT3 cN1 cM0','postop_diagnosis':'Sigmoid colon adenocarcinoma; resection completed','laterality':'Not applicable','findings':'Localized sigmoid tumor without gross peritoneal or hepatic metastasis in synthetic validation scenario.','specimens':[{'specimen_id':'SPC-ARJ-001','site':'Sigmoid colon','description':'Sigmoid colectomy specimen with mesocolic regional lymph nodes'}],'estimated_blood_loss_ml':120,'operative_time_min':155,'surgeons':['Dr Karan Shah — Surgical Oncology','Dr Demo Assistant — Synthetic'],'counts_status':'Correct','wound_closure':'Port sites and extraction incision closed in layers','disposition':'Stable to post-anaesthesia care / surgical ward','postop_plan':'ERAS pathway, VTE prophylaxis, analgesia, early mobilisation, await final histopathology','drains':[{'type':'Pelvic drain','status':'In situ'}],'stoma_created':False});check('ARJ-035 actual surgery/operative note signed',st==200,j)

# 6 pathology: technologist accession/processing, then pathologist reporting
path=entity('Pathology','pathology');path_id=path['id']
t=task('Pathology Technologist','Pathology accession',source_id=surg['id']);check('ARJ-036 technologist receives exact operative specimen task',bool(t),t)
st,src=source('Pathology Technologist',t['id']);check('ARJ-037 technologist sees surgery source/provenance',st==200 and src.get('source_record_id')==surg['id'],src)
proc=entity('Pathology Technologist','pathology_processing');st,j=action('Pathology Technologist','save_support_record',proc['id'],{'record_type':'pathology_processing','sign':True,'accession_id':'ACC-ARJ-2026-001','specimen_received_at':'2026-09-11T10:45:00+05:30','grossing_status':'Completed — specimen oriented, margins inked, tumor measured and nodes retrieved','blocks_slides_status':'18 lymph nodes submitted; representative tumor/margins blocked and slides prepared','ready_for_pathologist':True,'pathology_record_id':path_id});check('ARJ-038 technologist processing signed',st==200 and j.get('status')=='Signed',j)
t=task('Pathology','Pathology reporting','pathology',path_id);check('ARJ-039 Pathologist receives reporting task after processing',bool(t),t)
bad_path={'finalize':True,'date':'2026-09-12','site':'Sigmoid colon','specimen':'Sigmoid colectomy specimen','histology':'Moderately differentiated adenocarcinoma','pathological_stage':'Stage IIIB','path_t':'pT3','path_n':'pN1b','path_m':'pM not assessed','margin_status':'Negative (R0)','nodes_examined':18,'nodes_positive':2}
# node incoherence negative (real server-side guard added as part of this port)
path=entity('Pathology','pathology',path_id);st,j=action('Pathology','save_pathology',path_id,{**bad_path,'nodes_examined':18,'nodes_positive':20});check('ARJ-040 incoherent node counts blocked',st==409 and 'incoherent' in j.get('error','').lower(),j)
path=entity('Pathology','pathology',path_id);st,j=action('Pathology','save_pathology',path_id,bad_path);check('ARJ-041 final histopathology signed',st==200 and j.get('status')=='Final',j)
# immutable overwrite block
path=entity('Pathology','pathology',path_id);st,j=action('Pathology','save_pathology',path_id,{**bad_path,'finalize':True,'histology':'Adenocarcinoma — attempted overwrite'});check('ARJ-042 final pathology overwrite blocked',st==409 and 'immutable' in j.get('error','').lower(),j)
# amendment with reason creates new Final, old superseded
path=entity('Pathology','pathology',path_id);st,j=action('Pathology','save_pathology',path_id,{**bad_path,'finalize':True,'amendment_reason':'Addendum: clarify lymphovascular invasion wording after secondary slide review','addendum':'Lymphovascular invasion present; stage and margins unchanged.'});check('ARJ-043 pathology amendment creates superseding version',st==200 and j.get('status')=='Final' and j.get('supersedes')==path_id,j);final_path_id=j['id']
old_path=entity('Pathology','pathology',path_id);new_path=entity('Pathology','pathology',final_path_id);check('ARJ-044 old pathology retained Superseded and new Final',old_path and old_path['status']=='Superseded' and new_path and new_path['status']=='Final',{'old':old_path and (old_path['id'],old_path['status']),'new':new_path and (new_path['id'],new_path['status'])})

# 7 surgeon review derives pTNM from Pathology, not re-entry
st,j=action('Surgical Oncology','surgery_pathology_link',surg['id'],{'pathology_record_id':final_path_id,'postop_stage':'Stage IIIB','margin_status':'Negative (R0)','nodes_examined':18,'nodes_positive':2,'path_t':'pT3','path_n':'pN1b','path_m':'pM not assessed','review_note':'Final histopathology reviewed: pT3 pN1b, 2/18 nodes positive, R0 margins. Refer for adjuvant systemic therapy.'});check('ARJ-045 surgeon pathology review derives pStage',st==200 and bool(j.get('pathological_stage_record_id')),j);pdx_id=j['pathological_stage_record_id']
b=boot('Surgical Oncology');dxs=b.get('entities',{}).get('diagnosis',[]);cdx=next((x for x in dxs if x['id']==clinical_dx_id),None);pdx=next((x for x in dxs if x['id']==pdx_id),None)
check('ARJ-046 cTNM preserved separately from pTNM',cdx and pdx and cdx['data'].get('staging_basis')=='Clinical' and pdx['data'].get('staging_basis')=='Pathological' and pdx['data'].get('previous_stage_record_id')==clinical_dx_id,{'cTNM':cdx and {k:cdx['data'].get(k) for k in ['stage_t','stage_n','stage_m','stage_group','staging_basis']},'pTNM':pdx and {k:pdx['data'].get(k) for k in ['stage_t','stage_n','stage_m','stage_group','staging_basis','previous_stage_record_id']}})
wt=task('Stoma / Wound Nurse','Support service referral',source_id=surg['id']);check('ARJ-047 wound nurse receives post-op task',bool(wt),wt)
wound=entity('Stoma / Wound Nurse','stoma_wound');st,j=action('Stoma / Wound Nurse','save_support_record',wound['id'],{'record_type':'stoma_wound','sign':True,'assessment_date':'2026-09-12','wound_status':'Clean/dry/intact; no erythema','drain_status':'Pelvic drain patent; low serosanguinous output','stoma_status':'No stoma created','plan':'Daily wound review; drain output monitoring and removal per surgeon criteria','risk_flag':'Routine'});check('ARJ-048 wound assessment signed by owning role',st==200 and j.get('status')=='Signed',j)
adt=task('Medical Oncology','Adjuvant review',source_id=surg['id']);check('ARJ-049 MO automatically receives adjuvant review task',bool(adt),adt)
st,src=source('Medical Oncology',adt['id']);check('ARJ-050 MO sees exact Surgery/pathology-derived source',st==200 and src.get('source_record_id')==surg['id'],src)
st,j=action('Medical Oncology','surgery_adjuvant_decision',surg['id'],{'decision':'Adjuvant Systemic Therapy','rationale':'Stage IIIB colon adenocarcinoma after R0 resection with 2/18 nodes positive; proceed to medical oncology adjuvant planning in this synthetic validation pathway.'});check('ARJ-051 adjuvant systemic handoff recorded',st==200 and 'Medical Oncology' in j.get('next_roles',[]),j)

# audit evidence from surgeon bootstrap
b=boot('Surgical Oncology');aud=b.get('audit',[]);wanted={'SURGERY_PLAN_SIGN','SURGERY_PERFORMED','SURGERY_PATH_LINK','SURGERY_ADJUVANT_DECISION'};got=[x for x in aud if x.get('action') in wanted];check('ARJ-052 named actor audit events present',len({x.get('action') for x in got})>=3,got[:8])

out={'patient_id':PID,'patient':'Arjun Mehta','build':'12.2-PC7.1-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(1 for x in rows if x['pass']),'fail':sum(1 for x in rows if not x['pass']),'results':rows,'key_records':{'clinical_diagnosis':clinical_dx_id,'mdt':mdt_id,'treatment_plan':plan_id,'preop_lab':lab_id,'surgery':surg['id'],'pathology_original':path_id,'pathology_final_amended':final_path_id,'pathological_stage_record':pdx_id}}
(ROOT/'validation_evidence'/'PC8_ARJUN_SURGERY_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail','key_records']},ensure_ascii=False))
sys.exit(1 if out['fail'] else 0)
