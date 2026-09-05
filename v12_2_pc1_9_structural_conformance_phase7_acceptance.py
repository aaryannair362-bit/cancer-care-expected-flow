#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.error
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parent
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9199'); PIN=os.environ.get('CCA_DEMO_PIN','2026'); PID='PAT-0001'; OUT=[]

def http(path,method='GET',data=None,token=None):
 h={'Content-Type':'application/json'}; body=json.dumps(data).encode() if data is not None else None
 if token:h['Authorization']='Bearer '+token
 req=urllib.request.Request(BASE+path,data=body,headers=h,method=method)
 try:
  with urllib.request.urlopen(req,timeout=12) as r:
   raw=r.read(); return r.status,json.loads(raw.decode()) if raw else {}
 except urllib.error.HTTPError as e:
  raw=e.read()
  try:j=json.loads(raw.decode()) if raw else {}
  except:j={'raw':raw.decode(errors='replace')}
  return e.code,j

def login(role):
 st,j=http('/api/login','POST',{'role':role,'pin':PIN}); assert st==200,(role,st,j); return j['token']
roles=['Front Desk','Nurse Navigator','Intake Nurse','Medical Oncology','Surgical Oncology','Radiation Oncology','Radiologist','Laboratory / Phlebotomy','MDT Coordinator','MDT Chair','Oncology Pharmacy','Day Care / Infusion Nurse']
T={r:login(r) for r in roles}

def boot(role):return http('/api/bootstrap?patient='+PID,token=T[role])
def latest(role,typ):
 st,b=boot(role); assert st==200,(role,st,b); return b['entities'][typ][-1]
def act(role,a,eid='',d=None,expected=None):
 payload={'action':a,'patient_id':PID,'entity_id':eid,'data':dict(d or {})}
 if expected is not None:payload['expected_version']=expected
 return http('/api/action','POST',payload,T[role])
def chk(i,ok,d=''):
 OUT.append({'id':i,'pass':bool(ok),'detail':d});print(('PASS' if ok else 'FAIL'),i,json.dumps(d,ensure_ascii=False,default=str)[:1200] if d!='' else '')

# A. Build identity + distinct roles
st,m=http('/api/meta',token=T['Medical Oncology'])
chk('PC19-ROLE-001',st==200 and m.get('product','').startswith('CCA V12.2-PC1.9'),m.get('product'))
chk('PC19-ROLE-002','Intake Nurse' in m.get('roles',[]) and 'MDT Chair' in m.get('roles',[]),m.get('roles'))
st,surf=http('/api/role-surface',token=T['Intake Nurse']);chk('PC19-ROLE-003',st==200 and surf.get('role')=='Intake Nurse' and len(surf.get('surface',{}).get('input',[]))>0,surf)
st,surf=http('/api/role-surface',token=T['MDT Chair']);chk('PC19-ROLE-004',st==200 and any('Chair' in x.get('field','') or 'Chair' in x.get('output','') for x in surf.get('surface',{}).get('input',[])+surf.get('surface',{}).get('output',[])),surf)

# B. Intake Nurse can own intake structurally; Front Desk cannot.
intake=latest('Intake Nurse','intake')
data={'sbp':118,'dbp':74,'hr':78,'rr':16,'temp':98.6,'spo2':99,'weight':154.3,'height':66.9,'ecog':'1','kps':'90','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':2,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°F','spo2':'%','weight':'lb','height':'in'},'complete':True}
st,j=act('Intake Nurse','save_intake',intake['id'],data,expected=intake['version']);chk('PC19-INT-001',st==200 and abs(j.get('bsa_m2',0)-1.8)<0.2,{'status':st,'body':j})
intake=latest('Front Desk','intake') if 'intake' in boot('Front Desk')[1].get('entities',{}) else None
# Front Desk should neither receive nor write intake.
chk('PC19-INT-002',intake is None,{'front_desk_intake_visible':bool(intake)})
st,j=act('Front Desk','save_intake','INTAKE-0001',data,expected=1);chk('PC19-INT-003',st==403,{'status':st,'body':j})

# C. Governed diagnostics + result provenance / abnormal flag / amendment
st,j=act('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','name':'Free typed unsafe test','indication':'Synthetic QA','date':str(date.today()),'priority':'Routine','decision_reason':'Synthetic QA order'});chk('PC19-INV-001',st==409 and 'catalogue' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','catalog_id':'LAB-CBC','indication':'Pre-treatment CBC','date':str(date.today()),'priority':'Routine','decision_reason':'Required before systemic treatment'});loid=j.get('id');chk('PC19-INV-002',st==200 and loid,{'status':st,'body':j})
st,j=act('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','catalog_id':'LAB-CBC','indication':'Pre-treatment CBC','date':str(date.today()),'priority':'Routine'});chk('PC19-INV-003',st==409 and 'reason' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Front Desk','record_payment',loid,{'payment_status':'Waived','amount':0,'reason':'Synthetic QA'});chk('PC19-INV-004',st==403,{'status':st})
# use an existing billing-capable login only for test via new login
bill=login('Biller');T['Biller']=bill
st,j=http('/api/action','POST',{'action':'record_payment','patient_id':PID,'entity_id':loid,'data':{'payment_status':'Waived','amount':0,'reason':'Synthetic QA'}},bill);chk('PC19-INV-005',st==200,{'status':st,'body':j})
st,j=act('Laboratory / Phlebotomy','collect_sample',loid,{'sample_id':'SMP-PC19'});labid=j.get('lab_entity_id');chk('PC19-INV-006',st==200 and labid,{'status':st,'body':j})
labdata={'finalize':True,'date':str(date.today()),'hb':12.1,'wbc':5.8,'anc':3.0,'platelets':250,'creatinine':0.8,'egfr':90,'bilirubin':0.7,'ast':22,'alt':21,'units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L'},'abnormal_flags':{'anc':'Normal','platelets':'Normal'},'reference_ranges':{'anc':{'lower':999,'upper':9999,'unit':'BAD','source':'MALICIOUS CLIENT OVERRIDE'}}}
st,j=act('Laboratory / Phlebotomy','save_lab',labid,{**labdata,'abnormal_flags':{'anc':'GREEN'}});chk('PC19-INV-007',st==409 and 'abnormal flag' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Laboratory / Phlebotomy','save_lab',labid,labdata);chk('PC19-INV-008',st==200 and j.get('status')=='Final',{'status':st,'body':j})
st,j=act('Laboratory / Phlebotomy','save_lab',labid,{**labdata,'anc':2.9});chk('PC19-INV-009',st==409 and 'amendment' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Laboratory / Phlebotomy','save_lab',labid,{**labdata,'anc':2.9,'amendment_reason':'Synthetic correction'});newlab=j.get('id');chk('PC19-INV-010',st==200 and newlab!=labid and j.get('supersedes')==labid,{'status':st,'body':j})
for q,role in enumerate(['Medical Oncology','Oncology Pharmacy','Day Care / Infusion Nurse','MDT Coordinator'],11):
 xs=boot(role)[1].get('entities',{}).get('lab',[]);z=next((x for x in xs if x['id']==newlab),None);chk(f'PC19-INV-{q:03d}',bool(z and z['data'].get('abnormal_flags',{}).get('anc')=='Normal' and z['data'].get('reference_ranges',{}).get('anc',{}).get('lower')==1.5 and 'server-owned' in z['data'].get('reference_range_source_mode','')),{'role':role,'visible':bool(z)})

# D. MDT Coordinator records/submits; MDT Chair alone finalizes.
mdtc=latest('MDT Coordinator','mdt_collab')
# attendance uses optimistic lock in action list
for name,disc in [('Dr Med','Medical Oncology'),('Dr Rad','Radiation Oncology'),('Dr Surg','Surgical Oncology')]:
 mdtc=latest('MDT Coordinator','mdt_collab');st,j=act('MDT Coordinator','mdt_attendance',mdtc['id'],{'name':name,'discipline':disc,'status':'Present'},expected=mdtc['version'])
chk('PC19-MDT-001',st==200 and j.get('quorum_status')=='Met',{'status':st,'body':j})
mdtc=latest('MDT Coordinator','mdt_collab');st,j=act('MDT Coordinator','mdt_attendance',mdtc['id'],{'name':'Dr Med','discipline':'Medical Oncology','status':'Present'},expected=mdtc['version']);chk('PC19-MDT-002',st==409 and 'Duplicate' in j.get('error',''),{'status':st,'body':j})
mdt=latest('MDT Coordinator','mdt')
rec={'meeting_at':'2026-09-05T16:00','clinical_question':'Confirm postoperative multimodality sequence','clinical_summary':'Synthetic structured MDT summary','intent':'Curative','recommendation':'Combined modality','rationale':'Synthetic MDT rationale','final_consensus':'Consensus','specialty_responsible':'Combined-Modality'}
st,j=act('MDT Coordinator','mdt_recommend',mdt['id'],rec,expected=mdt['version']);chk('PC19-MDT-003',st==200 and j.get('status')=='Pending Chair Approval',{'status':st,'body':j})
mdt=latest('Medical Oncology','mdt');st,j=act('Medical Oncology','create_plan_from_mdt',mdt['id'],{'specialty':'Combined-Modality'});chk('PC19-MDT-004',st==409 and 'Chair-approved' in j.get('error',''),{'status':st,'body':j})
mdt=latest('MDT Coordinator','mdt');st,j=act('MDT Coordinator','mdt_chair_sign',mdt['id'],{'decision':'Approve','reason':'Should fail'});chk('PC19-MDT-005',st==403,{'status':st,'body':j})
mdt=latest('MDT Chair','mdt');st,j=act('MDT Chair','mdt_chair_sign',mdt['id'],{'decision':'Approve'});chk('PC19-MDT-006',st==409 and 'reason' in j.get('error','').lower(),{'status':st,'body':j})
mdt=latest('MDT Chair','mdt');st,j=act('MDT Chair','mdt_chair_sign',mdt['id'],{'decision':'Approve','reason':'Chair confirms synthetic multidisciplinary recommendation'});chk('PC19-MDT-007',st==200 and j.get('signed_by',{}).get('role')=='MDT Chair',{'status':st,'body':j})
for q,role in enumerate(['Medical Oncology','Surgical Oncology','Radiation Oncology'],8):
 z=latest(role,'mdt');chk(f'PC19-MDT-{q:03d}',z['data'].get('signed_by',{}).get('role')=='MDT Chair',{'role':role,'signed_by':z['data'].get('signed_by')})
st,j=act('Medical Oncology','create_plan_from_mdt',latest('Medical Oncology','mdt')['id'],{'specialty':'Combined-Modality'});chk('PC19-MDT-011',st==200 and j.get('status')=='Draft',{'status':st,'body':j})

# E. Response: measurement is separate from clinician confirmation and immutable after confirm.
resp=latest('Radiologist','response')
st,j=act('Radiologist','save_response',resp['id'],{'date':str(date.today()),'criteria_set':'RECIST 1.1','criteria_version':'1.1','source_imaging_id':'RAD-0001','target_lesions':[{'id':'L1','site':'Left breast','size':3.0,'unit':'cm'}],'non_target':'Present stable/persistent','new_lesions':False});aid=j.get('assessment',{}).get('id');chk('PC19-RSP-001',st==200 and aid and abs(j['assessment']['sum_mm']-30)<1e-6 and not j['assessment'].get('response_category'),{'status':st,'body':j})
st,j=act('Radiologist','confirm_response',resp['id'],{'assessment_id':aid,'response_category':'Partial response','reason':'Radiologist should not decide'});chk('PC19-RSP-002',st==403,{'status':st,'body':j})
st,j=act('Medical Oncology','confirm_response',resp['id'],{'assessment_id':aid,'response_category':'Partial response'});chk('PC19-RSP-003',st==409 and 'reason' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Medical Oncology','confirm_response',resp['id'],{'assessment_id':aid,'response_category':'Partial response','reason':'Clinician confirms formal response after source imaging review'});chk('PC19-RSP-004',st==200 and j['assessment'].get('confirmed_by',{}).get('role')=='Medical Oncology',{'status':st,'body':j})
st,j=act('Medical Oncology','confirm_response',resp['id'],{'assessment_id':aid,'response_category':'Stable disease','reason':'Silent overwrite attempt'});chk('PC19-RSP-005',st==409 and 'immutable' in j.get('error','').lower(),{'status':st,'body':j})
for q,role in enumerate(['Medical Oncology','Surgical Oncology','Radiation Oncology','MDT Coordinator','MDT Chair'],6):
 z=latest(role,'response');x=next((x for x in z['data'].get('assessments',[]) if x.get('id')==aid),None);chk(f'PC19-RSP-{q:03d}',bool(x and x.get('confirmation_status')=='Confirmed'),{'role':role,'visible':bool(x)})

# F. Surgical pathology -> derived adjuvant review + role-scoped tasks / completion.
surg=latest('Surgical Oncology','surgery')
st,j=act('Surgical Oncology','surgery_sign_plan',surg['id'],{});chk('PC19-SUR-001',st==200,{'status':st,'body':j})
st,j=act('Surgical Oncology','surgery_preop',surg['id'],{'anesthesia_clearance':'Complete','labs':'Complete','consent':'Complete'});chk('PC19-SUR-002',st==200 and j.get('ready'),{'status':st,'body':j})
op={'actual_procedure':'Left breast-conserving surgery','operation_date_time':'2026-09-05T09:00','preop_diagnosis':'Breast cancer','postop_diagnosis':'Breast cancer','laterality':'Left','findings':'Synthetic operative findings','specimens':[{'id':'SP1','site':'Left breast'}],'estimated_blood_loss_ml':50,'operative_time_min':90,'surgeons':['Surgical Oncology User'],'postop_plan':'Await final pathology','approach_used':'Open','extent_achieved':'Complete planned extent','nodal_procedure_performed':'Sentinel node procedure','postoperative_disposition':'Ward'}
st,j=act('Surgical Oncology','surgery_performed',surg['id'],op);chk('PC19-SUR-003',st==200,{'status':st,'body':j})
st,j=act('Surgical Oncology','surgery_pathology_link',surg['id'],{'pathology_record_id':'PATH-0001','postop_stage':'Stage IIA','margin_status':'Clear','nodes_examined':3,'nodes_positive':0,'path_t':'pT2','path_n':'pN0','path_m':'pM0','staging_date':str(date.today())});adj=j.get('adjuvant_review',{});chk('PC19-SUR-004',st==200 and adj.get('status')=='Ready for adjuvant review' and len(j.get('task_ids',[]))==2,{'status':st,'body':j})
for q,role in enumerate(['Medical Oncology','Radiation Oncology','MDT Coordinator','MDT Chair'],5):
 z=latest(role,'surgery');chk(f'PC19-SUR-{q:03d}',z['data'].get('adjuvant_review',{}).get('status')=='Ready for adjuvant review',{'role':role,'state':z['data'].get('adjuvant_review')})
st,j=act('Medical Oncology','complete_adjuvant_review',surg['id'],{'reason':'Reviewed after final pathology','source_record_id':j.get('pathological_stage_record_id','DX-0001')});chk('PC19-SUR-009',st==200 and j.get('adjuvant_review',{}).get('status')=='Adjuvant review complete',{'status':st,'body':j})

# G. Front Desk consent projection is completion-only.
st,b=boot('Front Desk');cons=b.get('entities',{}).get('consent',[]);cd=cons[-1]['data'] if cons else {};blob=json.dumps(cd).lower();chk('PC19-PRIV-001',bool(cons) and 'completion_status' in cd and 'signed_by' not in blob and 'language' not in blob and 'education' not in blob,cd)

# H. Frontend build markers.
idx=(ROOT/'static/index.html').read_text();js=(ROOT/'static/pc1_9.js').read_text()
for q,m in enumerate(['V12.2-PC1.9','Intake Nurse','MDT Chair','Postoperative adjuvant-review readiness','Reference-range provenance'],1):
 chk(f'PC19-UI-{q:03d}',m in idx+js,{'marker':m})

summary={'suite':'V12.2-PC1.9 Structural Conformance Phase 7','total':len(OUT),'passed':sum(x['pass'] for x in OUT),'failed':sum(not x['pass'] for x in OUT),'results':OUT}
(ROOT/'V12_2_PC1_9_TRACK_B_PHASE7_RUN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
print(json.dumps({k:summary[k] for k in ['total','passed','failed']},indent=2));sys.exit(1 if summary['failed'] else 0)
