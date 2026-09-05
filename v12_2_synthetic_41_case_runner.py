#!/usr/bin/env python3
"""V12.2 synthetic institutional 41-case product-process acceptance.
Clinical numbers/templates are synthetic QA content and are NOT patient-care guidance.
The suite validates product workflow/state/persistence/reconciliation only.
"""
import json, os, sys, urllib.request, urllib.error, urllib.parse
from datetime import date, datetime, timedelta

BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9077')
PIN=os.environ.get('CCA_DEMO_PIN','2026')
OUT=os.environ.get('CCA_OUT','V12_2_41_CASE_SCENARIO_RUN.json')
TOK={}
OPT={'save_intake':'intake','med_recon':'med_recon','save_dynamic_form':'dynamic_forms','save_consultation':'consultation','save_diagnosis':'diagnosis','save_appointment':'appointments','queue_patient':'queue','save_care_plan':'care_plan','save_treatment_plan':'treatment_plan','save_radiology':'radiology','save_pathology':'pathology','mdt_comment':'mdt_collab','mdt_attendance':'mdt_collab','mdt_recommend':'mdt'}

CASES=[
 ('T1','Breast, HER2+, node-positive','Stage IIB',['Med','Surg','Rad'],'Planned','Neoadjuvant systemic -> surgery -> adjuvant RT -> continuation'),
 ('T2','Breast, ER+, breast-conserving','Stage IIA',['Surg','Med','Rad'],'Day-surgery','Surgery -> adjuvant systemic -> RT -> endocrine'),
 ('T3','Head & neck, oral cavity','T3N1',['Surg','Med','Rad'],'Extended IPD','Surgery -> concurrent systemic + RT'),
 ('T4','Rectal cancer','cT3N1',['Med','Rad','Surg'],'IPD surgery','Neoadjuvant systemic + RT -> surgery -> adjuvant systemic'),
 ('T5','Cervix, locally advanced','Stage IIIB',['Med','Rad'],'Repeated short IPD','Concurrent systemic + RT -> brachytherapy'),
 ('T6','Oesophagus','T3N1',['Med','Rad','Surg'],'Prolonged IPD','Neoadjuvant systemic + RT -> surgery -> surveillance'),
 ('T7','Soft tissue sarcoma, thigh','High grade, deep',['Rad','Surg','Med'],'IPD surgery','RT -> limb-sparing surgery -> systemic'),
 ('T8','Lung NSCLC stage IIIA','Resectable after induction',['Med','Surg','Rad'],'IPD lobectomy','Induction systemic -> surgery -> conditional RT'),
 ('B1','Colon cancer, right-sided','Stage IIIB',['Surg','Med'],'IPD surgery','Surgery -> adjuvant systemic'),
 ('B2','Gastric cancer','Stage IIIA',['Med','Surg'],'IPD surgery','Perioperative systemic -> surgery -> post-op systemic'),
 ('B3','Ovarian cancer, advanced','Stage IIIC',['Med','Surg'],'IPD surgery','NACT -> interval surgery -> systemic'),
 ('B4','Kidney RCC','Stage III',['Surg','Med'],'IPD surgery','Surgery -> adjuvant systemic'),
 ('B5','Testicular germ cell','Stage IIA',['Surg','Med'],'Day-surgery','Surgery -> systemic -> marker response'),
 ('B6','Pancreatic head','Resectable',['Surg','Med'],'Prolonged IPD','Surgery -> delayed adjuvant systemic'),
 ('M1','Nasopharyngeal carcinoma','Stage III',['Med','Rad'],'Unplanned IPD','Concurrent systemic + RT -> systemic'),
 ('M2','NSCLC stage III unresectable','Stage III',['Med','Rad'],'IPD toxicity','Concurrent systemic + RT -> continuous consolidation'),
 ('M3','Diffuse large B-cell lymphoma','Bulky stage II',['Med','Rad'],'IPD toxicity','Systemic -> RT'),
 ('M4','Anal canal SCC','Stage II',['Med','Rad'],'IPD toxicity','Definitive concurrent systemic + RT'),
 ('M5','Glioblastoma','Post-biopsy',['Med','Rad'],'IPD seizures','RT + oral systemic -> continuous oral therapy'),
 ('M6','Prostate high risk','Synthetic high-risk classification',['Med','Rad'],'None','Definitive RT + long-course hormonal therapy'),
 ('S1','Early breast, elderly ER+','Stage I',['Surg','Rad'],'Day surgery','Surgery -> RT; systemic omitted'),
 ('S2','Endometrial carcinoma','Stage IB grade 2',['Surg','Rad'],'IPD surgery','Surgery -> brachytherapy'),
 ('S3','Skin SCC facial','Recurrent, close margins',['Surg','Rad'],'Day surgery','Surgery -> RT'),
 ('S4','Meningioma atypical','Subtotal resection',['Surg','Rad'],'IPD neurosurgical','Surgery -> RT'),
 ('U1','CML chronic phase','No TNM',['Med'],'None','Continuous oral therapy'),
 ('U2','Metastatic breast ER+','Bone-only',['Med'],'None','Continuous oral + endocrine therapy'),
 ('U3','Basal cell carcinoma','Nodular trunk',['Surg'],'Day surgery','Excision only'),
 ('U4','Painful bone metastasis','Known lung primary',['Rad'],'None','Palliative single-fraction RT'),
 ('U5','AML induction','Newly diagnosed',['Med'],'Prolonged IPD','Inpatient systemic therapy'),
 ('E1','Breast HER2+ progression mid-NACT','Stage IIB -> progression',['Med','Surg'],'None','Plan amended mid-treatment'),
 ('E2','Breast adjuvant RT declined','Post-surgery',['Rad'],'None','Planned RT phase cancelled'),
 ('E3','Breast HER2+ pharmacy query','Stage IIB',['Med'],'None','Pharmacy query -> oncologist response -> reverify'),
 ('E4','Breast HER2+ toxicity','Stage IIB',['Med'],'None','Toxicity -> modification -> next order'),
 ('E5','Breast HER2+ low counts','Stage IIB',['Med'],'None','Low ANC -> signed hold; no order'),
 ('E6','Breast HER2+ infusion reaction','Stage IIB',['Med'],'Emergency IPD','Partial administration -> emergency IPD'),
 ('E7','RT interruption by admission','25-fraction RT',['Rad'],'Unplanned IPD','Missed/rescheduled fraction -> resume'),
 ('E8','External referral with plan','Existing outside plan',['Med'],'None','External-origin clinician-approved plan; no internal MDT'),
 ('E9','Second cancer episode','Breast survivor + new colon primary',['Med','Surg'],'None','Two episode isolation'),
 ('E10','Metastatic recurrence','Prior breast -> metastatic recurrence',['Med'],'None','New episode/line; prior history retained'),
 ('E11','Patient declines treatment','Breast HER2+',['Med'],'None','Consent withdrawal -> discontinue'),
 ('E12','Death during treatment','Breast HER2+ cycle 4',['Med'],'None','Death -> close episode/future work'),
]

REG={
 'T1':'REG-CCA-TCHP-DEMO','T2':'REG-QA-BREAST-ER','T3':'REG-QA-HN','T4':'REG-QA-RECTAL','T5':'REG-QA-CERVIX','T6':'REG-QA-OESOPHAGUS','T7':'REG-QA-SARCOMA','T8':'REG-QA-NSCLC',
 'B1':'REG-QA-COLON','B2':'REG-QA-GASTRIC','B3':'REG-QA-OVARIAN','B4':'REG-QA-KIDNEY','B5':'REG-QA-TESTICULAR','B6':'REG-QA-PANCREAS','M1':'REG-QA-NPC','M2':'REG-QA-NSCLC','M3':'REG-QA-LYMPHOMA','M4':'REG-QA-ANAL','M5':'REG-QA-GBM','M6':'REG-QA-PROSTATE','U5':'REG-QA-AML',
 'E1':'REG-CCA-TCHP-DEMO','E3':'REG-CCA-TCHP-DEMO','E4':'REG-CCA-TCHP-DEMO','E5':'REG-CCA-TCHP-DEMO','E6':'REG-CCA-TCHP-DEMO','E8':'REG-QA-BREAST-ER','E9':'REG-QA-BREAST-ER','E10':'REG-QA-MET-BREAST','E11':'REG-CCA-TCHP-DEMO','E12':'REG-CCA-TCHP-DEMO'
}
RT={
 'T1':'RT-QA-BREAST','T2':'RT-QA-BREAST','T3':'RT-QA-HN','T4':'RT-QA-RECTAL','T5':'RT-QA-CERVIX','T6':'RT-QA-OESOPHAGUS','T7':'RT-QA-SARCOMA','T8':'RT-QA-NSCLC','M1':'RT-QA-NPC','M2':'RT-QA-NSCLC','M3':'RT-QA-LYMPHOMA','M4':'RT-QA-ANAL','M5':'RT-QA-GBM','M6':'RT-QA-PROSTATE','S1':'RT-QA-BREAST','S2':'RT-QA-ENDOMETRIAL','S3':'RT-QA-SKIN-SCC','S4':'RT-QA-MENINGIOMA','U4':'RT-QA-BONE-PALL','E2':'RT-QA-BREAST','E7':'RT-QA-BREAST'
}
SURG={
 'T1':'SURG-QA-BREAST','T2':'SURG-QA-BREAST','T3':'SURG-QA-BREAST','T4':'SURG-QA-COLORECTAL','T6':'SURG-QA-OESOPHAGUS','T7':'SURG-QA-SARCOMA','T8':'SURG-QA-LUNG','B1':'SURG-QA-COLORECTAL','B2':'SURG-QA-GASTRIC','B3':'SURG-QA-OVARIAN','B4':'SURG-QA-KIDNEY','B5':'SURG-QA-TESTICULAR','B6':'SURG-QA-PANCREAS','S1':'SURG-QA-BREAST','S2':'SURG-QA-ENDOMETRIAL','S3':'SURG-QA-SKIN-SCC','S4':'SURG-QA-MENINGIOMA','U3':'SURG-QA-BCC','E1':'SURG-QA-BREAST','E9':'SURG-QA-COLORECTAL'
}
NON_TNM={'M3','M5','S4','U1','U5'}
NO_MDT={'U1','U2','U3','U4','E8'}

content=json.load(open(os.path.join(os.path.dirname(__file__),'clinical_content','synthetic_institutional_test_content.json')))
TPL={x['id']:x for x in content['templates']}


def http(path,method='GET',data=None,token=None,timeout=12):
    h={'Content-Type':'application/json'}
    if token:h['Authorization']='Bearer '+token
    req=urllib.request.Request(BASE+path,data=None if data is None else json.dumps(data).encode(),headers=h,method=method)
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            raw=r.read(); return r.status,json.loads(raw.decode()) if raw else {}
    except urllib.error.HTTPError as e:
        raw=e.read()
        try:j=json.loads(raw.decode()) if raw else {}
        except:j={'raw':raw.decode(errors='replace')}
        return e.code,j
    except Exception as e:return 599,{'error':repr(e)}

def login(role):
    if role in TOK:return TOK[role]
    st,j=http('/api/login','POST',{'role':role,'pin':PIN})
    if st!=200:raise RuntimeError(('login',role,st,j))
    TOK[role]=j['token']; return TOK[role]

def boot(role,pid):return http('/api/bootstrap?patient='+urllib.parse.quote(pid),token=login(role))
def recs(b,t):return b.get('entities',{}).get(t,[]) if isinstance(b,dict) else []
def one(b,t):
    x=recs(b,t);return x[-1] if x else None

def latest(role,pid,t):
    st,b=boot(role,pid);return one(b,t) if st==200 else None

def pc13_adapt(a,d):
    d=dict(d or {})
    if a=='save_intake' and 'sbp' not in d:
        original=dict(d); bp=str(d.get('bp','120/80')).split('/')
        try:
            if len(bp)!=2: raise ValueError('malformed bp')
            sbp,dbp=float(bp[0]),float(bp[1]); d.pop('bp',None)
            d={'sbp':sbp,'dbp':dbp,'hr':d.pop('hr',78),'rr':d.pop('rr',16),'temp':d.pop('temp_c',36.7),'spo2':d.pop('spo2',99),'weight':d.pop('weight_kg',70),'height':d.pop('height_cm',170),'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'pain_instrument':d.get('pain_instrument') or 'Numeric Rating Scale 0–10',**d}
        except Exception:
            d=original
    if a=='save_intake':
        d.setdefault('fall_risk_scale','CCA Demo Fall-Risk Scale — Synthetic QA')
    if a=='save_readiness' and d.get('sign') and not (d.get('decision_reason') or d.get('reason')):
        d['decision_reason']='Synthetic clinician readiness rationale for regression compatibility'
    if a=='create_order':
        dr=dict(d.get('dose_decision_reasons') or {});dr.setdefault('*','Synthetic clinician acceptance of final ordered dose after review');d['dose_decision_reasons']=dr
        d.setdefault('administration_decision_reason','Synthetic clinician acceptance of regimen administration parameters after review')
        d.setdefault('schedule_decision_reason','Synthetic clinician acceptance of treatment administration date/time after review')
    if a=='med_recon':
        op=d.get('operation')
        if op=='add_allergy':
            d.setdefault('code','ALG-PEN');d.setdefault('reaction','Rash');d.setdefault('source','Patient')
            if d.get('source') not in ['Patient','Caregiver','Prior record','External clinician','Observed at CCA','Integrated record']:d['source']='Patient'
        elif op=='add_medication':
            if d.get('source') not in [None,'','Patient','Caregiver','Prior record','External clinician','Observed at CCA','Integrated record']:d['source']='Patient'
            d.setdefault('source','Patient');d.setdefault('formulary_id','FORM-CCA-001');d.setdefault('dose_value',4);d.setdefault('dose_unit','mg');d.setdefault('frequency','Once daily');d.setdefault('status','Continue')
        elif op=='reconcile':
            d.setdefault('reconciliation_status','Complete');d.setdefault('source','Patient');
            if d.get('source') not in ['Patient','Caregiver','Prior record','External clinician','Observed at CCA','Integrated record']:d['source']='Patient'
    if a=='rt_planning_status':
        d.setdefault('plan_version',1)
    if a=='pharmacy_decision' and d.get('decision')=='Verified':
        ck=d.get('verification_checks') or {}; ok=all(bool(v) for v in ck.values()) if ck else True
        keys=['patient_identity','allergy','regimen_version','cycle_day','dose_basis','calculated_dose','ordered_dose','dose_variance','renal_adjustment','hepatic_adjustment','cumulative_dose','interaction','duplication','route','diluent','final_concentration','stock','expiry']
        d['verification_checks']={k:bool(ck.get(k,ok)) for k in keys}
    if a=='pharmacy_prepare':
        from datetime import datetime,timedelta
        bud=(datetime.now().astimezone()+timedelta(hours=4)).isoformat(timespec='minutes')
        items=[]
        for x in d.get('items') or []:
            y=dict(x); y.setdefault('actual_volume_unit','mL'); y.setdefault('compatibility_status','Compatible'); y.setdefault('stability_reference','Synthetic QA stability reference — NOT CLINICAL'); y.setdefault('beyond_use_at',bud); y.setdefault('storage_condition','Synthetic QA storage condition — NOT CLINICAL'); y.setdefault('light_protection','Not required'); y.setdefault('filter_requirement','Synthetic QA filter status — NOT CLINICAL'); y.setdefault('container_requirement','Synthetic QA container — NOT CLINICAL'); items.append(y)
        d['items']=items
    if a=='start_infusion':
        acc=d.get('access')
        if isinstance(acc,str):
            at='PICC' if 'picc' in acc.lower() else ('Port' if 'port' in acc.lower() else 'Peripheral IV')
            site='Right upper limb' if 'right' in acc.lower() else ('Left upper limb' if 'left' in acc.lower() else ('Chest central access' if at=='Port' else 'Right upper limb'))
            d['access']={'type':at,'site':site,'detail':acc}
        pv=dict(d.get('pre_vitals') or {})
        if pv:pv.setdefault('units',{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'});d['pre_vitals']=pv
    if a=='administer_item':
        r=dict(d.get('record') or {}); r.setdefault('actual_dose_unit',r.get('unit') or 'mg')
        if r.get('actual_rate') is not None: r.setdefault('actual_rate_unit','mL/h')
        if r.get('completion_status') not in [None,'Administered'] or r.get('variance_note'):
            r.setdefault('variance_type','Dose variance' if r.get('completion_status') in ['Partially Administered','Stopped'] else 'Other')
            r.setdefault('variance_reason_code','Infusion reaction' if str(r.get('reaction','')).lower() not in ['','none'] else 'Clinician instruction')
        d['record']=r
    if a=='complete_infusion':
        pv=dict(d.get('post_vitals') or {})
        if pv:pv.setdefault('units',{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'});d['post_vitals']=pv
    return d

def act(role,pid,a,eid='',d=None,expected='AUTO'):
    payload={'action':a,'patient_id':pid,'entity_id':eid,'data':pc13_adapt(a,d)}
    if a in OPT and expected=='AUTO':
        t=OPT[a];st,b=boot(role,pid);xs=recs(b,t) if st==200 else [];target=next((z for z in xs if eid and z.get('id')==eid),xs[-1] if xs else None)
        if target:payload['expected_version']=target['version']
    elif expected not in ['AUTO',None]:payload['expected_version']=expected
    return http('/api/action','POST',payload,login(role))

def step(c,name,st,j,expect=200,extra=None):
    ok = st==expect if isinstance(expect,int) else st in expect
    c['steps'].append({'name':name,'ok':ok,'http':st,'response':j if not ok else ({'ok':j.get('ok',True),'status':j.get('status','')} if isinstance(j,dict) else j)})
    if extra:c['steps'][-1].update(extra)
    if not ok:c['failures'].append({'step':name,'http':st,'response':j,'expected':expect})
    return ok

def require(c,name,st,j,expect=200):
    if not step(c,name,st,j,expect):raise RuntimeError(f'{name}: HTTP {st} {j}')
    return j

def patient(c,idx):
    sex='Female' if any(x in c['cancer'].lower() for x in ['breast','ovarian','cervix','endometrial']) else 'Male'
    phone='+9178'+str(10000000+idx).zfill(8)
    st,j=http('/api/patient','POST',{'name':f"Synthetic {c['id']} Product Test",'dob':'1985-01-01','sex':sex,'phone':phone,'id_number':f'QA41-{c["id"]}-{idx}','initial_specialty':'Medical Oncology','duplicate_override_reason':'Synthetic isolated 41-case QA'},login('Front Desk'));require(c,'patient registration create',st,j);pid=j['id'];c['pid']=pid
    reg=latest('Front Desk',pid,'registration');q=latest('Front Desk',pid,'queue');cons=latest('Front Desk',pid,'consent');ap=latest('Front Desk',pid,'appointments')
    require(c,'registration complete',*act('Front Desk',pid,'save_registration',reg['id'],{'name':f"Synthetic {c['id']} Product Test",'dob':'1985-01-01','sex':sex,'phone':phone,'id_number':f'QA41-{c["id"]}-{idx}','assigned_specialty':'Medical Oncology','clinician_assignment':'Synthetic QA Oncology','route_rule':'Manual QA routing','referral_doctor_name':'Synthetic Referrer','referral_facility':'Synthetic Facility','referral_network_level3':'Synthetic Network','referral_reason':'Product workflow test','address':'Synthetic','complete':True}))
    require(c,'general consent',*act('Front Desk',pid,'consent_action',cons['id'],{'operation':'sign','type':'General Consent','version':'QA-v1','scope':'Synthetic product test','signed_by':f'Synthetic {c["id"]}','valid_from':str(date.today())}))
    require(c,'appointment create',*act('Front Desk',pid,'save_appointment',ap['id'],{'operation':'create','date':str(date.today()),'department':'Medical Oncology','location':'OPD','purpose':'41-case product acceptance'}))
    require(c,'queue nurse',*act('Front Desk',pid,'queue_patient',q['id'],{'to':'Nurse Intake','status':'Queued','care_stage':'Intake'}))
    intake=latest('Nurse Navigator',pid,'intake');mr=latest('Nurse Navigator',pid,'med_recon');wt=66+(idx%8);ht=164+(idx%6)
    require(c,'nurse intake',*act('Nurse Navigator',pid,'save_intake',intake['id'],{'bp':'120/80','hr':78,'rr':16,'temp_c':36.7,'spo2':99,'weight_kg':wt,'height_cm':ht,'ecog':'1','kps':'90','pain_score':2,'pain_site':'Synthetic site','fall_risk_setting':'OPD','fall_risk_score':1,'fall_risk_level':'Low','past_medical':'Synthetic history','past_surgical':'Synthetic history','family_history':'Reviewed','hormonal_history':'Reviewed','reproductive_history':'Reviewed','social_history':'No tobacco','complete':True}))
    require(c,'allergy capture',*act('Nurse Navigator',pid,'med_recon',mr['id'],{'operation':'add_allergy','substance':'Synthetic QA Allergen','reaction':'Rash','severity':'Moderate','status':'Active','source':'Synthetic'}))
    require(c,'med reconciliation',*act('Nurse Navigator',pid,'med_recon',mr['id'],{'operation':'reconcile','source':'Synthetic QA','note':'Reconciled'}))
    require(c,'queue medical oncology',*act('Front Desk',pid,'queue_patient',q['id'],{'to':'Medical Oncology','status':'Queued','care_stage':'Consultation'}))
    con=latest('Medical Oncology',pid,'consultation')
    require(c,'consultation signed',*act('Medical Oncology',pid,'save_consultation',con['id'],{'encounter_type':'New diagnosis / treatment planning','date':str(date.today()),'chief_complaint':'Synthetic oncology presentation','hpi':c['cancer']+' '+c['stage'],'ros':'Synthetic review','physical_exam_structured':{'general':'Stable','cardiovascular':'Normal','respiratory':'Clear','abdomen':'Soft','neurologic':'No focal deficit','tumor_site':'Synthetic finding'},'assessment':'Synthetic product-test assessment','plan':'Diagnostics and treatment planning','sign':True}))
    # Baseline final lab through the real order/payment/collection/result loop.
    st,j=act('Medical Oncology',pid,'create_diagnostic_order','',{'type':'Laboratory','name':'CBC','indication':'Synthetic baseline treatment readiness','date':str(date.today()),'decision_reason':'Synthetic acceptance-test investigation decision'});require(c,'lab order',st,j);loid=j['id']
    require(c,'lab payment waiver',*act('Biller',pid,'record_payment',loid,{'payment_status':'Waived','amount':0,'reason':'Synthetic QA'}))
    st,j=act('Laboratory / Phlebotomy',pid,'collect_sample',loid,{'sample_id':f'QA41-{c["id"]}-S1'});require(c,'lab collection',st,j);labid=j['lab_entity_id']
    require(c,'final lab',*act('Laboratory / Phlebotomy',pid,'save_lab',labid,lab_payload()))
    # Grant all scenario-specialty surfaces explicitly via governed queues.
    if c['id'] not in NO_MDT: require(c,'queue MDT',*act('Front Desk',pid,'queue_patient',q['id'],{'to':'MDT / Tumour Board','status':'Queued','care_stage':'MDT'}))
    if 'Surg' in c['mods']: require(c,'queue surgery',*act('Front Desk',pid,'queue_patient',q['id'],{'to':'Surgical Oncology','status':'Queued','care_stage':'Surgery'}))
    if 'Rad' in c['mods']: require(c,'queue radiation',*act('Front Desk',pid,'queue_patient',q['id'],{'to':'Radiation Oncology','status':'Queued','care_stage':'Radiation'}))
    dx=latest('Medical Oncology',pid,'diagnosis');require(c,'diagnosis verified',*act('Medical Oncology',pid,'save_diagnosis',dx['id'],dx_payload(c)))
    # Verify intake persisted after handoff.
    mi=latest('Medical Oncology',pid,'intake'); step(c,'intake downstream persistence',200,{'ok':bool(mi and mi['data'].get('bsa_m2') and mi['data'].get('measured_at'))})
    return pid

def lab_payload(anc=3.2,unit='×10^9/L',amendment_reason=None):
    p={'date':str(date.today()),'hb':12.2,'wbc':6.0,'anc':anc,'platelets':250,'creatinine':0.8,'egfr':90,'bilirubin':0.8,'ast':20,'alt':20,'albumin':4.0,'sodium':139,'potassium':4.0,'magnesium':2.0,'calcium':9.0,'lvef':60,'pregnancy':'Negative','units':{'hb':'g/dL','wbc':'×10^9/L','anc':unit,'platelets':'×10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m²','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalize':True}
    if amendment_reason:p['amendment_reason']=amendment_reason
    return p

def dx_payload(c):
    if c['id'] in NON_TNM:
        return {'icd10':'QA-NONTNM','icd10_version':'ICD-10','cancer_type':c['cancer'],'primary_site':'Synthetic disease site','histology':c['cancer'],'staging_system':'Disease-specific classification','staging_version':'Synthetic QA v1','staging_date':str(date.today()),'staging_basis':'Clinical','classification_system':'Disease-specific classification','classification_value':c['stage'],'treatment_intent':'Curative','verify':True}
    return {'icd10':'QA-SOLID','icd10_version':'ICD-10','icdo_topography':'QA-TOP','icdo_morphology':'QA-MORPH','icdo_version':'ICD-O-3','cancer_type':c['cancer'],'primary_site':'Synthetic disease site','histology':'Synthetic malignant neoplasm','stage_t':'cT2','stage_n':'cN1','stage_m':'cM0','stage_group':c['stage'],'staging_system':'TNM synthetic QA','staging_version':'Synthetic QA v1','staging_date':str(date.today()),'staging_basis':'Clinical','treatment_intent':'Palliative' if any(x in c['stage'].lower() for x in ['metast','bone-only']) else 'Curative','verify':True}

def phases_for(c):
    out=[]
    if 'Med' in c['mods']:out.append({'modality':'Systemic Therapy','description':'Synthetic systemic phase','status':'Planned','responsible':'Medical Oncology'})
    if 'Surg' in c['mods']:out.append({'modality':'Surgery','description':'Synthetic surgery phase','status':'Planned','responsible':'Surgical Oncology'})
    if 'Rad' in c['mods']:out.append({'modality':'Radiation','description':'Synthetic radiation phase','status':'Planned','responsible':'Radiation Oncology'})
    return out or [{'modality':'Other','description':'Synthetic follow-up','status':'Planned','responsible':'Care Team'}]

def plan(c,external=False):
    pid=c['pid'];ph=phases_for(c);signer='Medical Oncology' if 'Med' in c['mods'] else ('Surgical Oncology' if 'Surg' in c['mods'] else 'Radiation Oncology')
    if external or c['id'] in NO_MDT:
        p=latest(signer,pid,'treatment_plan')
        data={'external_origin':True,'external_source':'Synthetic external plan for product testing','diagnosis':c['cancer'],'stage':c['stage'],'intent':'Palliative' if 'palliative' in c['pathway'].lower() else 'Curative','line_of_therapy':'Synthetic QA line','sequence':[x['modality'] for x in ph],'phases':ph,'sign':True}
        st,j=act(signer,pid,'save_treatment_plan',p['id'],data);require(c,'external/direct treatment plan approved',st,j);return j.get('id') or p['id']
    m=latest('MDT Coordinator',pid,'mdt');coll=latest('MDT Coordinator',pid,'mdt_collab')
    require(c,'MDT attendance med',*act('MDT Coordinator',pid,'mdt_attendance',coll['id'],{'name':'Synthetic Medical Oncologist','discipline':'Medical Oncology','status':'Present'}))
    require(c,'MDT attendance surgery',*act('MDT Coordinator',pid,'mdt_attendance',coll['id'],{'name':'Synthetic Surgical Oncologist','discipline':'Surgical Oncology','status':'Present'}))
    require(c,'MDT attendance radiation',*act('MDT Coordinator',pid,'mdt_attendance',coll['id'],{'name':'Synthetic Radiation Oncologist','discipline':'Radiation Oncology','status':'Present'}))
    require(c,'MDT comment',*act('Medical Oncology',pid,'mdt_comment',coll['id'],{'comment':'Synthetic multidisciplinary discussion for product testing.'}))
    specialty='Combined-Modality' if len(c['mods'])>1 else {'Med':'Medical Oncology','Rad':'Radiation Oncology','Surg':'Surgical Oncology'}[c['mods'][0]]
    require(c,'MDT recommendation submission',*act('MDT Coordinator',pid,'mdt_recommend',m['id'],{'meeting_at':datetime.now().astimezone().isoformat(),'clinical_question':'Confirm synthetic product-test sequence','clinical_summary':c['cancer']+' '+c['stage'],'intent':'Palliative' if 'palliative' in c['pathway'].lower() else 'Curative','recommendation':c['pathway'],'rationale':'Synthetic process acceptance','final_consensus':'Consensus','specialty_responsible':specialty,'attendees':['Medical Oncology','Surgical Oncology','Radiation Oncology'],'outstanding_investigations':[]}))
    m=latest('MDT Chair',pid,'mdt');require(c,'MDT Chair approval',*act('MDT Chair',pid,'mdt_chair_sign',m['id'],{'decision':'Approve','reason':'Synthetic acceptance-test Chair approval'}))
    m=latest('MDT Coordinator',pid,'mdt');st,j=act('MDT Coordinator',pid,'create_plan_from_mdt',m['id'],{'specialty':specialty});require(c,'draft plan from MDT',st,j);pidplan=j['id']
    st,j=act(signer,pid,'save_treatment_plan',pidplan,{'source_mdt_id':m['id'],'diagnosis':c['cancer'],'stage':c['stage'],'intent':'Palliative' if 'palliative' in c['pathway'].lower() else 'Curative','line_of_therapy':'Synthetic QA line','sequence':[x['modality'] for x in ph],'phases':ph,'sign':True});require(c,'treatment plan clinician approval',st,j);return j.get('id') or pidplan

def treatment_consent(c):
    co=latest('Patient Liaison',c['pid'],'consent');return require(c,'treatment consent',*act('Patient Liaison',c['pid'],'consent_action',co['id'],{'operation':'sign','type':'Treatment Consent','version':'QA-TX-v1','scope':'Synthetic systemic product test','signed_by':f'Synthetic {c["id"]}','valid_from':str(date.today())}))

def regimen(c):return REG.get(c['id'])
def inpatient_case(c):return c['id']=='U5'

def ensure_admission(c,admission_type='Planned',reason='Treatment / procedure'):
    st,j=act('Medical Oncology',c['pid'],'admit_patient','',{'admission_type':admission_type,'reason_code':reason,'ward':'Oncology Ward','bed':f'QA-{c["id"]}','source_context':'Synthetic 41-case product test'})
    if st==409 and j.get('admission_id'):
        step(c,'admission already active',200,{'ok':True,'admission_id':j['admission_id']});return j['admission_id']
    require(c,'IPD admission',st,j);return j.get('admission',{}).get('id') or j.get('admission_id')

def readiness(c,tid,decision='Proceed as Planned',reason='Synthetic product test readiness'):
    r=latest('Medical Oncology',c['pid'],'readiness');st,j=act('Medical Oncology',c['pid'],'save_readiness',r['id'],{'template_id':tid,'decision':decision,'reason':reason,'sign':True});require(c,'signed readiness '+decision,st,j);return j

def systemic(c,planid,query=False,partial_reaction=False,setting=None,cycle=1):
    tid=regimen(c)
    if not tid:raise RuntimeError('No systemic template map')
    setting=setting or ('Inpatient' if inpatient_case(c) else 'Day Care')
    if setting=='Inpatient':ensure_admission(c)
    readiness(c,tid)
    payload={'template_id':tid,'plan_id':planid,'administration_setting':setting,'diagnosis':c['cancer'],'intent':'Curative','line_of_therapy':'Synthetic QA line','cycle':cycle,'day':1,'start_date':str(date.today())}
    if tid=='REG-CCA-TCHP-DEMO':payload.update({'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic clinician-entered AUC product-test dose'}})
    st,j=act('Medical Oncology',c['pid'],'create_order','',payload);require(c,'treatment order created',st,j);oid,phid,infid=j['order_id'],j['pharmacy_id'],j['infusion_id'];c.setdefault('orders',[]).append(oid)
    # Persistence + plan linkage.
    o=next(x for x in recs(boot('Medical Oncology',c['pid'])[1],'treatment_order') if x['id']==oid)
    step(c,'order links exact approved plan',200,{'ok':o['data'].get('plan_id')==planid,'plan_id':o['data'].get('plan_id')})
    checks={k:True for k in ['allergy','interaction','dose_method','calculated_dose','dose','organ_function','diluent','volume','stock','expiry']}
    if query:
        require(c,'pharmacy query',*act('Oncology Pharmacy',c['pid'],'pharmacy_decision',phid,{'decision':'Query','verification_checks':checks,'query_reason':'Dose requires clarification','message':'Synthetic QA clarification request'}))
        require(c,'oncologist query response',*act('Medical Oncology',c['pid'],'oncologist_query_response',oid,{'response_action':'Confirm as ordered','response_note':'Synthetic reviewed response'}))
    require(c,'pharmacy verified',*act('Oncology Pharmacy',c['pid'],'pharmacy_decision',phid,{'decision':'Verified','verification_checks':checks}))
    pb=boot('Oncology Pharmacy',c['pid'])[1];ph=next(x for x in recs(pb,'pharmacy') if x['id']==phid);fst,fm=http('/api/formulary',token=login('Oncology Pharmacy'));require(c,'institution formulary available to pharmacy',fst,fm);fmap={x['drug']:x for x in fm.get('items',[]) if x.get('status')=='Active'};pre=[]
    for n,it in enumerate(ph['data']['items'],1):
        fi=fmap.get(it['drug']);form=(fi.get('formulations') or [{}])[0] if fi else {}
        x=dict(it);x.update({'formulation':form.get('label',''),'formulation_strength_mg':form.get('strength_mg',0),'batch':f'QA-{c["id"]}-{n}','expiry':str(date.today()+timedelta(days=60)),'prepared_by':'Oncology Pharmacist A','actual_volume_ml':it.get('volume_ml',0),'waste':'0'});pre.append(x)
    require(c,'pharmacy prepared',*act('Oncology Pharmacy',c['pid'],'pharmacy_prepare',phid,{'items':pre,'preparation_note':'Synthetic product-test preparation'}))
    rel=[{**x,'second_check_by':'Oncology Pharmacist B','label_verified':True} for x in pre];dest='Inpatient Oncology Ward' if setting=='Inpatient' else 'Day Care / Infusion'
    require(c,'pharmacy released',*act('Oncology Pharmacy',c['pid'],'pharmacy_release',phid,{'items':rel,'dispensed_to':dest,'manifest_no':f'QA-MAN-{c["id"]}-{cycle}'}))
    treatment_consent(c)
    nurse='Inpatient Oncology Nurse' if setting=='Inpatient' else 'Day Care / Infusion Nurse';nb=boot(nurse,c['pid'])[1];pat=nb['patient']
    start={'checklist':{k:True for k in ['identity','order','consent','allergy','vitals','labs','access','pharmacy']},'identity_confirmation':{'name':pat['name'],'mrn':pat['mrn'],'dob':pat['dob']},'pre_vitals':{'bp':'118/74','hr':78,'rr':16,'temp':36.7,'spo2':99},'access':'Synthetic patent venous access','bedside_verification':{'confirmed':True,'verified_by':'Synthetic RN B'}}
    require(c,'administration started',*act(nurse,c['pid'],'start_infusion',infid,start))
    order=next(x for x in recs(boot('Medical Oncology',c['pid'])[1],'treatment_order') if x['id']==oid);items=sorted(order['data']['items'],key=lambda z:z['sequence'])
    for n,it in enumerate(items):
        actual=float(it['ordered_dose']);status='Administered';reason='';variance=''
        if partial_reaction and n==len(items)-1:
            actual=round(actual/2,4);status='Stopped';reason='Synthetic acute infusion reaction';variance='Stopped after partial dose due to synthetic reaction'
        rr={'item_id':it['item_id'],'actual_dose':actual,'unit':it['ordered_unit'],'access':'Synthetic venous access','start_time':f'{10+n:02d}:00','end_time':f'{10+n:02d}:20','actual_rate':it.get('rate_ml_hr',0),'completion_status':status,'reason':reason,'reaction':'Synthetic reaction' if status=='Stopped' else 'None','intervention':'Emergency management' if status=='Stopped' else 'None','variance_note':variance}
        if it.get('group') in ['Antineoplastic','Targeted Therapy']:
            rr['chairside_verification']={'verified_by':'Synthetic RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
        require(c,f'MAR item {n+1}',*act(nurse,c['pid'],'administer_item',infid,{'record':rr}))
    if partial_reaction:
        return {'order_id':oid,'pharmacy_id':phid,'infusion_id':infid,'nurse':nurse}
    require(c,'cycle completed',*act(nurse,c['pid'],'complete_infusion',infid,{'post_vitals':{'bp':'120/76','hr':80,'rr':16,'temp':36.8,'spo2':99},'tolerance':'Good','discharge_instructions':'Synthetic product-test instructions','next_cycle':str(date.today()+timedelta(days=21))}))
    ib=boot(nurse,c['pid'])[1];inf=next(x for x in recs(ib,'infusion') if x['id']==infid);mar={x['item_id']:x for x in inf['data']['mar']};matches=all(float(mar[i['item_id']]['actual_dose'])==float(i['ordered_dose']) for i in items)
    step(c,'order-pharmacy-MAR reconciliation',200,{'ok':matches,'item_count':len(items)})
    return {'order_id':oid,'pharmacy_id':phid,'infusion_id':infid,'nurse':nurse}

def radiation(c,interrupt=False):
    tid=RT[c['id']];td=dict(TPL[tid]['data']);rt=latest('Radiation Oncology',c['pid'],'radiation');td.update({'content_template_id':tid,'content_template_version':TPL[tid]['version'],'planned_start':str(date.today()),'sign':True})
    # Ensure arithmetic exact if source uses floats.
    td['total_dose_gy']=float(td['dose_per_fraction_gy'])*int(td['fractions'])
    require(c,'RT prescription approved',*act('Radiation Oncology',c['pid'],'rt_save_prescription',rt['id'],td))
    require(c,'RT plan preparation before physics',*act('Radiation Oncology',c['pid'],'rt_planning_status',rt['id'],{'plan_version':1,'simulation_status':'Completed','contouring_status':'Completed','planning_status':'Planning Complete','status':'Planning'}))
    require(c,'RT physics QA',*act('Radiation Physicist',c['pid'],'rt_planning_status',rt['id'],{'plan_version':1,'physics_qa':'Approved','physics_qa_note':'Synthetic QA physics review'}))
    require(c,'RT physician final approval',*act('Radiation Oncology',c['pid'],'rt_planning_status',rt['id'],{'plan_version':1,'physician_final_approval':'Approved','status':'Ready for Treatment'}))
    per=float(td['dose_per_fraction_gy']);nfr=int(td['fractions'])
    if interrupt:
        target=min(12,nfr)
        for n in range(1,target):
            require(c,f'RT fraction {n} delivered',*act('Radiation Technologist',c['pid'],'rt_deliver_fraction',rt['id'],{'fraction_number':n,'status':'Delivered','date_time':(datetime.now()+timedelta(days=n-1)).isoformat(),'delivered_dose_gy':per,'verified_by':'Synthetic RTT','image_guidance_performed':True}))
        require(c,'RT fraction missed',*act('Radiation Technologist',c['pid'],'rt_deliver_fraction',rt['id'],{'fraction_number':target,'status':'Missed','date_time':(datetime.now()+timedelta(days=target)).isoformat(),'reason':'Synthetic admission interruption'}))
        require(c,'RT fraction rescheduled',*act('Radiation Technologist',c['pid'],'rt_deliver_fraction',rt['id'],{'fraction_number':target,'status':'Rescheduled','date_time':(datetime.now()+timedelta(days=target+5)).isoformat(),'reason':'Resumed after synthetic interruption'}))
        require(c,'RT fraction resumed',*act('Radiation Technologist',c['pid'],'rt_deliver_fraction',rt['id'],{'fraction_number':target,'status':'Delivered','date_time':(datetime.now()+timedelta(days=target+6)).isoformat(),'delivered_dose_gy':per,'verified_by':'Synthetic RTT','image_guidance_performed':True}))
    else:
        require(c,'RT fraction 1 delivered',*act('Radiation Technologist',c['pid'],'rt_deliver_fraction',rt['id'],{'fraction_number':1,'status':'Delivered','date_time':datetime.now().isoformat(),'delivered_dose_gy':per,'verified_by':'Synthetic RTT','image_guidance_performed':True}))
    rb=boot('Radiation Oncology',c['pid'])[1];r=latest('Radiation Oncology',c['pid'],'radiation');deliv=[x for x in r['data'].get('fractions',[]) if x.get('status')=='Delivered'];cum=sum(float(x.get('delivered_dose_gy') or 0) for x in deliv)
    step(c,'RT cumulative dose derives delivered fractions',200,{'ok':abs(cum-len(deliv)*per)<1e-8,'delivered':len(deliv),'cumulative':cum,'per_fraction':per})
    return rt['id']

def surgery(c,positive_margin=False):
    tid=SURG[c['id']];td=dict(TPL[tid]['data']);s=latest('Surgical Oncology',c['pid'],'surgery');td.update({'content_template_id':tid,'content_template_version':TPL[tid]['version'],'planned_date':str(date.today())})
    # Fill any deliberately descriptive empty fields required by executable surface.
    defaults={'procedure':'Synthetic oncologic procedure','indication':'Definitive treatment','intent':'Curative','site':'Synthetic disease site','laterality':'Not applicable','extent':'Synthetic oncologic extent','approach':'Open','nodal_procedure':'As configured','reconstruction':'None','priority':'Routine','preop_requirements':['Labs','Anesthesia','Consent'],'required_imaging_pathology':['Synthetic staging record'],'anesthesia':'General','anesthesia_clearance':'Pending','blood_requirement':'Type and screen'}
    for k,v in defaults.items():td.setdefault(k,v)
    require(c,'surgical plan signed',*act('Surgical Oncology',c['pid'],'surgery_sign_plan',s['id'],td))
    require(c,'surgical preop ready',*act('Surgical Nurse',c['pid'],'surgery_preop',s['id'],{'anesthesia_clearance':'Complete','labs':'Complete','consent':'Complete'}))
    op={'actual_procedure':td['procedure']+' — performed','operation_date_time':datetime.now().astimezone().isoformat(),'preop_diagnosis':c['cancer'],'postop_diagnosis':c['cancer'],'laterality':td['laterality'],'findings':'Synthetic operative findings','specimens':['Synthetic specimen'],'estimated_blood_loss_ml':50,'operative_time_min':120,'surgeons':['Synthetic Surgical Oncologist'],'postop_plan':'Final pathology and adjuvant review'}
    require(c,'surgery performed',*act('Surgical Oncology',c['pid'],'surgery_performed',s['id'],op))
    p=latest('Pathology',c['pid'],'pathology');pdata={'date':str(date.today()),'site':'Synthetic surgical specimen','specimen':'Resection specimen','histology':'Synthetic final histopathology','margin_status':'Positive' if positive_margin else 'Negative','nodes_examined':3,'nodes_positive':1 if positive_margin else 0,'finalize':True}
    st,j=act('Pathology',c['pid'],'save_pathology',p['id'],pdata)
    # New patient may carry a pre-finalized seed pathology only in some seeded contexts; use amendment semantics if needed.
    if st==409 and 'immutable' in j.get('error','').lower():
        pdata['amendment_reason']='Synthetic postoperative pathology replaces prior demo final';st,j=act('Pathology',c['pid'],'save_pathology',p['id'],pdata)
    require(c,'postoperative pathology final',st,j);pf=latest('Surgical Oncology',c['pid'],'pathology')
    require(c,'surgery pathology linked',*act('Surgical Oncology',c['pid'],'surgery_pathology_link',s['id'],{'pathology_record_id':pf['id'],'postop_stage':'Synthetic pathological stage','margin_status':'Positive' if positive_margin else 'Negative','nodes_examined':3,'nodes_positive':1 if positive_margin else 0,'path_t':'pT2','path_n':'pN1' if positive_margin else 'pN0','path_m':'cM0','staging_date':str(date.today())}))
    ss=latest('Surgical Oncology',c['pid'],'surgery');step(c,'planned-vs-actual laterality reconciliation',200,{'ok':ss['data']['plan']['laterality']==ss['data']['outcome']['laterality'],'planned':ss['data']['plan']['laterality'],'actual':ss['data']['outcome']['laterality']})
    return s['id']

def generic_ipd(c,reason='Treatment toxicity'):
    aid=ensure_admission(c,'Unplanned',reason)
    require(c,'IPD observation',*act('Inpatient Oncology Nurse',c['pid'],'record_inpatient_observation','',{'admission_id':aid,'type':'Nursing observation','vitals':{'bp':'116/72','hr':84,'rr':18,'temp':37.0,'spo2':98},'pain_score':2,'intake_ml':500,'output_ml':350,'note':'Synthetic stable observation'}))
    require(c,'IPD specialty review',*act('Medical Oncology',c['pid'],'inpatient_specialty_review','',{'admission_id':aid,'specialty':'Medical Oncology','assessment':'Synthetic inpatient review','plan':'Continue synthetic monitoring'}))
    st,j=act('Medical Oncology',c['pid'],'discharge_patient','',{'admission_id':aid,'discharge_diagnosis':'Synthetic resolved inpatient issue','hospital_course':'Synthetic monitored inpatient course','medications':'Continue reconciled medications','follow_up':'Oncology follow-up','next_care_stage':'Medical Oncology'})
    require(c,'IPD discharge',st,j)

def continuous(c,mode='Oral systemic therapy',therapy='Synthetic continuous systemic therapy'):
    e=latest('Medical Oncology',c['pid'],'continuous_therapy');return require(c,'continuous therapy created',*act('Medical Oncology',c['pid'],'create_continuous_therapy',e['id'],{'therapy':therapy,'mode':mode,'drug':'Synthetic QA continuous agent','route':'PO','schedule':'Continuous / protocol-defined','start_date':str(date.today()),'monitoring_plan':'Synthetic periodic monitoring','intent':'Palliative' if c['id']=='U2' else 'Curative'}))

def special(c,planid,base_sys=None):
    cid=c['id']
    if cid=='E1':
        p=latest('Medical Oncology',c['pid'],'treatment_plan');idx=next((i for i,x in enumerate(p['data'].get('phases',[])) if x.get('modality')=='Surgery'),0)
        require(c,'plan amendment after progression',*act('Medical Oncology',c['pid'],'amend_treatment_phase',p['id'],{'phase_index':idx,'changes':{'status':'Planned','description':'Surgery added/advanced after synthetic progression'},'reason':'Synthetic progression changes sequence'}))
        ps=recs(boot('Medical Oncology',c['pid'])[1],'treatment_plan');step(c,'plan history preserved after amendment',200,{'ok':len(ps)>=2 and ps[-1]['data'].get('supersedes'),'count':len(ps)})
    elif cid=='E2':
        p=latest('Radiation Oncology',c['pid'],'treatment_plan');idx=next(i for i,x in enumerate(p['data']['phases']) if x.get('modality')=='Radiation')
        require(c,'RT phase cancelled with reason',*act('Radiation Oncology',c['pid'],'amend_treatment_phase',p['id'],{'phase_index':idx,'operation':'cancel','reason':'Synthetic patient decline'}))
    elif cid=='E4' and base_sys:
        tox=latest('Medical Oncology',c['pid'],'toxicity');require(c,'toxicity Grade 3 recorded',*act('Medical Oncology',c['pid'],'record_toxicity',tox['id'],{'term':'Mucositis','grade':'3','onset_date':str(date.today()),'attribution':'Probably related','outcome':'Persistent','intervention':'Dose reduction'}))
        mod=latest('Medical Oncology',c['pid'],'modification');st,j=act('Medical Oncology',c['pid'],'create_modification',mod['id'],{'original_order_id':base_sys['order_id'],'reason':'Toxicity','modification_type':'Dose reduction','clinical_justification':'Synthetic Grade 3 toxicity','drug':'Docetaxel','original_dose':'Snapshot','modified_percent':-20});require(c,'modification order linked',st,j)
        readiness(c,REG[cid],'Proceed with Modification','Synthetic toxicity modification')
        payload={'template_id':REG[cid],'plan_id':planid,'diagnosis':c['cancer'],'intent':'Curative','line_of_therapy':'Synthetic QA','cycle':2,'day':1,'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic AUC dose'}}
        # reduce DEMO-DOC using original calculated dose
        order=next(x for x in recs(boot('Medical Oncology',c['pid'])[1],'treatment_order') if x['id']==base_sys['order_id']);doc=next(x for x in order['data']['items'] if x['code']=='DEMO-DOC');payload['doses']['DEMO-DOC']=round(float(doc['calculated_dose'])*0.8,4);payload['variance_reasons']['DEMO-DOC']='Synthetic 20% reduction after toxicity'
        st,j=act('Medical Oncology',c['pid'],'create_order','',payload);require(c,'modified next-cycle order created',st,j);no=next(x for x in recs(boot('Medical Oncology',c['pid'])[1],'treatment_order') if x['id']==j['order_id']);step(c,'modified order links modification record',200,{'ok':bool(no['data'].get('modification_id')),'modification_id':no['data'].get('modification_id')})
    elif cid=='E6' and base_sys:
        tox=latest('Day Care / Infusion Nurse',c['pid'],'toxicity');require(c,'infusion reaction toxicity',*act('Day Care / Infusion Nurse',c['pid'],'record_toxicity',tox['id'],{'term':'Other','grade':'3','onset_date':str(date.today()),'attribution':'Definitely related','outcome':'Persistent','intervention':'Emergency management'}))
        st,j=act('Day Care / Infusion Nurse',c['pid'],'escalate_to_ipd',base_sys['infusion_id'],{'reason_code':'Adverse drug reaction','reason_note':'Synthetic acute infusion reaction','ward':'Oncology Ward','bed':'QA-E6'});require(c,'Day Care emergency escalation to IPD',st,j)
    elif cid=='E9':
        first=latest('Medical Oncology',c['pid'],'cancer_episode');require(c,'first episode closed',*act('Medical Oncology',c['pid'],'close_cancer_episode',first['id'],{'episode_id':first['id'],'reason':'Synthetic prior cancer surveillance transition'}))
        st,j=act('Medical Oncology',c['pid'],'create_cancer_episode','',{'kind':'New primary cancer','label':'Synthetic second colon primary','started_at':str(date.today())});require(c,'second cancer episode created',st,j);ep2=j['id']
        require(c,'episode-2 continuous test treatment',*act('Medical Oncology',c['pid'],'create_continuous_therapy',latest('Medical Oncology',c['pid'],'continuous_therapy')['id'],{'episode_id':ep2,'therapy':'Synthetic episode-2 therapy','mode':'Hormonal therapy','drug':'Synthetic agent','route':'PO','schedule':'Continuous','start_date':str(date.today())}))
        eps=recs(boot('Medical Oncology',c['pid'])[1],'cancer_episode');courses=latest('Medical Oncology',c['pid'],'continuous_therapy')['data']['courses'];step(c,'two episode isolation',200,{'ok':len(eps)>=2 and courses[-1]['episode_id']==ep2,'episodes':[(x['id'],x['status']) for x in eps],'course_episode':courses[-1]['episode_id']})
    elif cid=='E10':
        old=latest('Medical Oncology',c['pid'],'cancer_episode');require(c,'prior episode close before recurrence',*act('Medical Oncology',c['pid'],'close_cancer_episode',old['id'],{'episode_id':old['id'],'reason':'Synthetic recurrence transition'}));st,j=act('Medical Oncology',c['pid'],'create_cancer_episode','',{'kind':'Recurrence / metastatic progression','label':'Synthetic metastatic recurrence','started_at':str(date.today())});require(c,'recurrence episode',st,j)
        hist=latest('Medical Oncology',c['pid'],'treatment_history');step(c,'prior treatment history retained',200,{'ok':bool(hist is not None),'history_entries':len(hist['data'].get('episodes',[]))})
    elif cid=='E11':
        cons=latest('Patient Liaison',c['pid'],'consent');signed=[x for x in cons['data']['items'] if x.get('type')=='Treatment Consent' and x.get('status')=='Signed']
        if signed:require(c,'treatment consent withdrawn',*act('Patient Liaison',c['pid'],'consent_action',cons['id'],{'operation':'withdraw','id':signed[-1]['id'],'reason':'Synthetic patient decline'}))
        p=latest('Medical Oncology',c['pid'],'treatment_plan');require(c,'treatment discontinued',*act('Medical Oncology',c['pid'],'discontinue_treatment',p['id'],{'reason':'Synthetic patient declined treatment'}))
    elif cid=='E12':
        require(c,'death closes episode/future work',*act('Medical Oncology',c['pid'],'record_death','',{'date':str(date.today()),'reason':'Synthetic product-test death'}));b=boot('Medical Oncology',c['pid'])[1];step(c,'patient marked deceased',200,{'ok':b['patient']['status']=='Deceased','status':b['patient']['status']})

def run(meta,idx):
    cid,cancer,stage,mods,ipd,pathway=meta;c={'id':cid,'cancer':cancer,'stage':stage,'mods':mods,'ipd':ipd,'pathway':pathway,'steps':[],'failures':[],'verdict':'PASS'}
    try:
        patient(c,idx);planid=plan(c,external=(cid=='E8'));c['plan_id']=planid;base=None
        # Primary execution choices. Special continuous/oral cases deliberately bypass Day Care.
        if cid=='E5':
            lab=latest('Laboratory / Phlebotomy',c['pid'],'lab');require(c,'low ANC final amendment',*act('Laboratory / Phlebotomy',c['pid'],'save_lab',lab['id'],lab_payload(0.8,'×10^9/L','Synthetic low-count hold test')));r=readiness(c,REG[cid],'Hold','Synthetic ANC below regimen threshold');step(c,'hold contains blocker',200,{'ok':bool(r.get('evaluation',{}).get('blockers')),'blockers':r.get('evaluation',{}).get('blockers')});st,j=act('Medical Oncology',c['pid'],'create_order','',{'template_id':REG[cid],'plan_id':planid,'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic AUC dose'}});step(c,'held cycle cannot create order',st,j,409)
        elif cid in ['U1','U2']:
            continuous(c,'Oral systemic therapy' if cid=='U1' else 'Hormonal therapy', 'Synthetic CML continuous therapy' if cid=='U1' else 'Synthetic metastatic breast continuous therapy')
        elif cid=='M5':
            require(c,'oral systemic therapy created',*act('Medical Oncology',c['pid'],'create_oral_therapy',latest('Medical Oncology',c['pid'],'continuous_therapy')['id'],{'drug':'Synthetic QA oral agent','schedule':'Daily during RT','start_date':str(date.today()),'monitoring_plan':'Synthetic monitoring'}));radiation(c)
        elif cid=='M6':
            continuous(c,'Hormonal therapy','Synthetic long-course hormonal therapy');radiation(c)
        elif cid=='U3': surgery(c)
        elif cid=='U4': radiation(c)
        elif cid=='E2': special(c,planid)
        elif cid=='E7': radiation(c,interrupt=True)
        else:
            # Run modalities in a broadly scenario-appropriate order while preserving each independent authoritative record.
            if cid in ['T2','T3','B1','B4','B5','B6','S1','S2','S3','S4'] and 'Surg' in mods:surgery(c,positive_margin=(cid=='T8'))
            if 'Med' in mods:
                base=systemic(c,planid,query=(cid=='E3'),partial_reaction=(cid=='E6'),setting='Inpatient' if cid=='U5' else None)
            if cid in ['T1','T4','T6','T7','T8','B2','B3'] and 'Surg' in mods:surgery(c,positive_margin=(cid=='T8'))
            if 'Rad' in mods:radiation(c)
            if cid=='T2':continuous(c,'Hormonal therapy','Synthetic adjuvant endocrine phase')
            if cid=='M2':continuous(c,'Other continuous systemic therapy','Synthetic consolidation phase')
            if cid=='B5':require(c,'tumor marker response',*act('Medical Oncology',c['pid'],'record_tumor_marker',latest('Medical Oncology',c['pid'],'tumor_marker')['id'],{'date':str(date.today()),'context':'Synthetic response monitoring','AFP':10,'bHCG':2,'LDH':180}))
            if cid=='T8':require(c,'conditional RT phase evaluation',*act('Surgical Oncology',c['pid'],'evaluate_conditional_phase','',{'condition':'positive margins','activate':'Radiation','condition_met':True}))
            if cid in ['E1','E4','E6','E9','E10','E11','E12']:special(c,planid,base)
        # Generic IPD continuity for scenarios explicitly containing inpatient care and not already handled as active U5/E6.
        if c['ipd']!='None' and cid not in ['U5','E6']:
            # Avoid colliding with a still-active admission; generic path closes its own admission.
            generic_ipd(c,'Treatment toxicity' if any(x in c['ipd'].lower() for x in ['tox','unplanned','emergency']) else 'Treatment / procedure')
        # Response object / longitudinal linkage in multi-modality treatment cases.
        if cid in ['T1','T4','B3','E1']:
            resp=latest('Medical Oncology',c['pid'],'response');st,j=act('Medical Oncology',c['pid'],'save_response',resp['id'],{'date':str(date.today()),'target_lesions':[{'id':'QA-L1','site':'Synthetic lesion','size_mm':30}],'non_target':'Synthetic stable','new_lesions':False,'notes':'Synthetic product-test response'});step(c,'response assessment',st,j)
        # Journey and audit must exist after actual events.
        jb=boot('Medical Oncology',c['pid'])[1];jour=one(jb,'journey');step(c,'patient journey populated',200,{'ok':bool(jour and jour['data'].get('events')),'count':len(jour['data'].get('events',[])) if jour else 0});step(c,'patient audit populated',200,{'ok':bool(jb.get('audit')),'count':len(jb.get('audit',[]))})
    except Exception as e:
        c['failures'].append({'step':'runner exception','error':repr(e)});c['verdict']='FAIL'
    if c['failures']:c['verdict']='FAIL'
    print(('PASS' if c['verdict']=='PASS' else 'FAIL'),cid,'steps',len(c['steps']),'failures',len(c['failures']), c['failures'][:1])
    return c

# Preflight synthetic content must remain unmistakably QA-only and active/orderable where needed.
pre=[]
st,h=http('/api/health');pre.append({'name':'health','ok':st==200 and h.get('version')=='12.2' and h.get('synthetic_test_content') is True,'detail':h})
stc,rc=http('/api/content',token=login('Medical Oncology'))
runtime_templates={x.get('id'):x for x in (rc.get('templates',[]) if stc==200 else [])}
for tid in sorted(set(REG.values())):
    t=runtime_templates.get(tid) or TPL.get(tid);pre.append({'name':'content '+tid,'ok':bool(t and t.get('status')=='Active' and t.get('orderable') is True and (t.get('source_id') in ['SRC-CCA-QA','SRC-CCA-DEMO'] or tid=='REG-CCA-TCHP-DEMO')),'detail':{'status':t.get('status') if t else None,'orderable':t.get('orderable') if t else None,'source_id':t.get('source_id') if t else None}})

results=[]
for i,m in enumerate(CASES,1):
    print(f'RUN {i}/41 {m[0]}',flush=True);results.append(run(m,i))
sta,aud=http('/api/audit/verify',token=login('Hospital Management / Admin'))
summary={'build':'CCA Cancer Care HIS + Oncology EMR V12.2 Final Defect Remediation','version':'12.2','run_at':datetime.now().astimezone().isoformat(),'clinical_content':'Synthetic QA institutional content only — product testing/demo; not patient care','supplied_case_count':41,'executed_case_count':len(results),'preflight':pre,'cases':results,'global_audit_verify':{'http':sta,'result':aud}}
summary['pass']=sum(x['verdict']=='PASS' for x in results);summary['fail']=len(results)-summary['pass'];summary['preflight_fail']=sum(not x['ok'] for x in pre)
open(OUT,'w').write(json.dumps(summary,indent=2,ensure_ascii=False))
print(f"RESULT {summary['pass']} CASE PASS {summary['fail']} CASE FAIL; PREFLIGHT_FAIL {summary['preflight_fail']}; AUDIT_HTTP {sta} AUDIT_ERRORS {len(aud.get('errors',[])) if isinstance(aud,dict) else 'n/a'}")
if summary['fail'] or summary['preflight_fail'] or sta!=200 or aud.get('errors'):sys.exit(1)
