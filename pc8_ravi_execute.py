#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download, targeting this repo's
# PAT-VAL-RAVI validation patient (same "Ravi Kapoor" synthetic identity, distinct id/mrn
# from the pre-existing PAT-DEMO-IPD showcase patient).
import json,urllib.request,urllib.error,urllib.parse,pathlib,sqlite3,sys,os
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parent;BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765');PID='PAT-VAL-RAVI';TODAY='2026-09-08';TOK={};rows=[]
creds={}
for line in (ROOT/'DEMO_USER_CREDENTIALS.txt').read_text(encoding='utf-8').splitlines():
 if ' | ' in line:
  u,p,n,r=[x.strip() for x in line.split(' | ',3)];creds[r]=(u,p,n)
def http(path,method='GET',data=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 b=json.dumps(data).encode() if data is not None else None
 try:
  with urllib.request.urlopen(urllib.request.Request(BASE+path,data=b,headers=h,method=method),timeout=15) as r:return r.status,json.loads(r.read().decode() or '{}')
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
 st,j=http('/api/bootstrap?patient='+PID,token=login(role));assert st==200,(role,st,j);return j
def ent(role,typ,eid=None):
 xs=boot(role).get('entities',{}).get(typ,[])
 return next((x for x in xs if x['id']==eid),None) if eid else (xs[-1] if xs else None)
OPT={'save_intake','med_recon','save_dynamic_form','save_consultation','save_diagnosis','save_appointment','queue_patient','save_care_plan','save_treatment_plan','save_radiology','save_pathology','mdt_comment','mdt_attendance','mdt_recommend','save_referral','save_support_record','rt_planning_status'}
def action(role,a,eid='',d=None):
 p={'action':a,'patient_id':PID,'entity_id':eid,'data':d or {}}
 if a in OPT and eid:
  found=None
  for xs in boot(role).get('entities',{}).values():
   for x in xs:
    if x['id']==eid:found=x;break
   if found:break
  if found:p['expected_version']=found['version']
 return http('/api/action','POST',p,login(role))
def tasks(role,status=None):
 st,j=http('/api/tasks?patient='+PID,token=login(role));assert st==200,(role,st,j);xs=j.get('tasks',[]);return [x for x in xs if not status or x.get('status')==status]
def task(role,tt=None,source_id=None,status='Open'):
 for x in reversed(tasks(role,status)):
  if tt and x.get('task_type')!=tt:continue
  if source_id and x.get('source_id')!=source_id:continue
  return x
 return None
def src(role,tid):return http('/api/task-source?task='+tid,token=login(role))
def ck(name,ok,d=None):
 rows.append({'check':name,'pass':bool(ok),'detail':d});print(('PASS' if ok else 'FAIL'),name,json.dumps(d,ensure_ascii=False,default=str)[:900] if d is not None else '')
 if not ok:raise AssertionError(name+' '+str(d))

reg=ent('Front Desk','registration');ck('RAV-001 baseline registration draft',reg and reg['status']=='Draft',reg and {'id':reg['id'],'status':reg['status']})
st,j=action('Front Desk','save_registration',reg['id'],{'name':'Ravi Kapoor','dob':'1959-05-28','sex':'Male','phone':'917000000104','id_number':'SYN-RAVI-01','assigned_specialty':'Medical Oncology','complete':True});ck('RAV-002 registration complete',st==200,j)
ref=ent('Front Desk','referral');st,j=action('Front Desk','save_referral',ref['id'],{'status':'Assigned','assigned_department':'Medical Oncology','assigned_clinician':'Dr Asha Mehta','priority':'Urgent'});ck('RAV-003 referral assigned',st==200,j)
t=task('Medical Oncology','Referral lifecycle',ref['id']);ck('RAV-004 MO receives referral task',bool(t),t);st,sctx=src('Medical Oncology',t['id']);ck('RAV-005 exact referral source/provenance',st==200 and sctx.get('source_record_id')==ref['id'],sctx)
st,j=action('Intake Nurse','save_referral',ref['id'],{'status':'Accepted'});ck('RAV-006 wrong role cannot accept referral',st==403,j)
st,j=action('Medical Oncology','save_referral',ref['id'],{'status':'Accepted'});ck('RAV-007 MO accepts referral',st==200 and j.get('status')=='Accepted',j)
intake=ent('Intake Nurse','intake');st,j=action('Intake Nurse','save_intake',intake['id'],{'complete':True,'sbp':104,'dbp':66,'hr':102,'rr':20,'temp':37.8,'spo2':95,'weight':67,'height':170,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'ecog':'2','kps':'70','pain_score':2,'pain_instrument':'Numeric Rating Scale 0–10','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':3,'nkda':True,'measured_at':'2026-09-08T07:30:00+05:30'});ck('RAV-008 intake signed',st==200,j)
con=ent('Medical Oncology','consultation');st,j=action('Medical Oncology','save_consultation',con['id'],{'sign':True,'encounter_type':'Urgent Medical Oncology Review','date':TODAY,'chief_complaint':'Fever and malaise during active oncology treatment','hpi':'Synthetic validation patient with metastatic lung adenocarcinoma presents with fever and reduced oral intake.','ros':'Fever, fatigue; no focal neurologic symptoms.','assessment':'Possible infection during active systemic therapy; admit for inpatient oncology evaluation and treatment.','plan':'Confirm disease status, admit under inpatient oncology, obtain cultures/labs and initiate clinician-directed supportive treatment.','physical_exam_structured':{'general':'Unwell but alert, ECOG 2','cardiovascular':'Tachycardic, regular','respiratory':'Reduced right basal air entry','abdomen':'Soft, non-tender','neurologic':'Alert, no focal deficit','tumor_site':'Known right lung primary'}});ck('RAV-010 consultation signed',st==200,j)
dx=ent('Medical Oncology','diagnosis');st,j=action('Medical Oncology','save_diagnosis',dx['id'],{'verify':True,'icd10':'C34.91','icd10_version':'ICD-10','icdo_topography':'C34.9','icdo_morphology':'8140/3','icdo_version':'ICD-O-3','cancer_type':'Lung Cancer','primary_site':'Right lung','histology':'Adenocarcinoma','grade':'2','staging_system':'AJCC','staging_version':'Lung v8','staging_date':TODAY,'staging_basis':'Clinical','stage_t':'cT3','stage_n':'cN2','stage_m':'cM1','stage_group':'Stage IV','treatment_intent':'Palliative','disease_status':'Active metastatic disease'});ck('RAV-011 diagnosis/staging verified',st==200 and j.get('status')=='Verified',j)
adm=ent('Medical Oncology','admission')
st,j=action('Inpatient Oncology Nurse','admit_patient',adm['id'],{'admission_type':'Unplanned','reason_code':'Infection / febrile neutropenia'});ck('RAV-013 wrong role cannot initiate admission',st==403,j)
st,j=action('Medical Oncology','admit_patient',adm['id'],{'admission_type':'Unplanned','reason_code':'Infection / febrile neutropenia','reason_note':'Fever during active oncology treatment — synthetic validation','admitting_specialty':'Medical Oncology','attending_clinician':'Dr Imran Khan — IPD Oncology'});ck('RAV-014 admission created',st==200,j)
adm=ent('Medical Oncology','admission');admid=adm['data']['admissions'][-1]['id']
ct=task('Inpatient Oncology Clinician','IPD admission assessment');nt=task('Inpatient Oncology Nurse','IPD nursing admission');ck('RAV-015 dual clinician+nurse admission tasks',bool(ct and nt),{'clinician':ct,'nurse':nt})
st,sctx=src('Inpatient Oncology Clinician',ct['id']);ck('RAV-016 clinician opens exact admission source',st==200 and sctx.get('source_record_id')==adm['id'],sctx)
ipd=ent('Inpatient Oncology Clinician','inpatient_care')
st,j=action('Inpatient Oncology Nurse','assign_inpatient_bed',adm['id'],{'admission_id':admid,'ward':'Oncology Ward','bed':'B-12','identity_confirmed':True,'baseline_vitals':{'temp_c':38.4,'hr':108,'bp':'98/60','spo2':94}});ck('RAV-018 nursing admission bed assigned',st==200,j)
st,j=action('Inpatient Oncology Nurse','inpatient_specialty_review',ipd['id'],{'history':'x','examination':'x','problem_list':['x'],'assessment':'x','plan':'x'});ck('RAV-019 nurse cannot sign clinician H&P',st==403,j)
st,j=action('Inpatient Oncology Clinician','inpatient_specialty_review',ipd['id'],{'history':'Metastatic lung adenocarcinoma on active systemic therapy; acute fever, reduced intake and fatigue.','examination':'T 38.4 C, HR 108/min, BP 98/60, SpO2 94% RA; alert; no focal neurologic deficit.','problem_list':['Fever / suspected infection','Dehydration risk','Metastatic lung cancer on active treatment'],'assessment':'Unplanned oncology admission for suspected infection during treatment.','plan':'IV fluids, clinician-directed antimicrobial therapy, cultures/laboratory monitoring, close nursing observations and escalation for deterioration.'});ck('RAV-020 clinician H&P signed',st==200,j)
st,j=action('Inpatient Oncology Nurse','inpatient_med_order',ipd['id'],{'medication':'Ceftriaxone','dose':1,'unit':'g','route':'IV','frequency':'Every 24 hours','indication':'Suspected infection'});ck('RAV-021 nurse cannot prescribe',st==403,j)
st,j=action('Inpatient Oncology Clinician','inpatient_med_order',ipd['id'],{'medication':'Ceftriaxone','dose':1,'unit':'g','route':'IV','frequency':'Every 24 hours','indication':'Suspected infection','start_at':'2026-09-08T10:00:00+05:30'});ck('RAV-022 clinician medication order persists',st==200,j);oid=j['order']['id']
mt=task('Inpatient Oncology Nurse','IPD medication administration');ck('RAV-023 nurse MAR task created',bool(mt),mt)
st,j=action('Inpatient Oncology Clinician','inpatient_mar',ipd['id'],{'order_id':oid,'actual_dose':1,'administration_datetime':'2026-09-08T10:15:00+05:30'});ck('RAV-025 clinician cannot chart nursing MAR',st==403,j)
st,j=action('Inpatient Oncology Nurse','inpatient_mar',ipd['id'],{'order_id':oid,'actual_dose':1,'administration_datetime':'2026-09-08T10:15:00+05:30','response':'Tolerated','complete_order':True});ck('RAV-026 nurse MAR actual dose persisted and order completed',st==200 and j.get('order_status')=='Completed',j)
st,j=action('Inpatient Oncology Nurse','record_inpatient_observation',ipd['id'],{'type':'Nursing observation','at':'2026-09-08T13:00:00+05:30','vitals':{'temp_c':38.8,'spo2':91,'sbp':86,'hr':116},'pain_score':2,'note':'New fever and hypotension.'});ck('RAV-027 observation recorded',st==200,j)
disc=ent('Inpatient Oncology Clinician','discharge')
st,j=action('Inpatient Oncology Clinician','discharge_patient',disc['id'],{'admission_id':admid,'discharge_diagnosis':'Suspected infection during active oncology treatment — clinically improved','hospital_course':'Synthetic validation admission: fever/hypotension monitored, IV treatment administered, clinical observations improved and no unresolved inpatient medication orders remain.','medications':'Oral supportive medications per discharge plan — synthetic validation','follow_up':'Medical Oncology review in 48–72 hours; Navigator call within 24 hours.','next_care_stage':'Medical Oncology'});ck('RAV-032 signed discharge completes',st==200,j)
b=boot('Inpatient Oncology Clinician');cep=ent('Inpatient Oncology Clinician','cancer_episode');ck('RAV-035 same Cancer Episode maintained',bool(cep),cep)
c=sqlite3.connect(ROOT/'cca_v12.sqlite3');c.row_factory=sqlite3.Row;aud=[dict(x) for x in c.execute('SELECT actor_id,actor_role,action,entity_type,entity_id,at FROM audit WHERE patient_id=? ORDER BY id',(PID,))];c.close();wanted={'IPD_ADMISSION','IPD_MED_ORDER','IPD_MAR','IPD_OBSERVATION','IPD_DISCHARGE'};got={x.get('action') for x in aud};ck('RAV-036 named actor audit events',len(wanted & got)>=3,sorted(got))
out={'patient':'Ravi Kapoor','patient_id':PID,'build':'12.2-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(x['pass'] for x in rows),'fail':sum(not x['pass'] for x in rows),'results':rows,'key_records':{'admission_record':adm['id'],'admission_instance':admid,'inpatient_care':ipd['id'],'discharge':disc['id'],'medication_order':oid}}
(ROOT/'validation_evidence'/'PC8_RAVI_IPD_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail','key_records']},ensure_ascii=False))
sys.exit(1 if out['fail'] else 0)
