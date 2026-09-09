#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download, targeting this repo's
# PAT-VAL-NEHA validation patient (same "Neha Kulkarni" synthetic identity, distinct
# id/mrn from the pre-existing PAT-DEMO-RT showcase patient).
#
# Substantially rewritten (not just field-renamed) versus the PC8.0 original because this
# repo's actual RT action set is a different, more mature architecture than PC8.0 assumed:
#  - save_consultation is hard-restricted to role=='Medical Oncology' only (WRITE['consultation']
#    = {'Medical Oncology'}); Radiation Oncology cannot sign it. So the entry consult/diagnosis/
#    MDT submission is done by Medical Oncology, who then hands off to Radiation Oncology via
#    the MDT Chair's specialty_responsible grant -- mirroring how a real cancer centre routes a
#    new referral through a triage oncologist before a specialty (RT) takes over.
#  - rt_planning_status is hard-restricted to role in ['Radiation Oncology','Radiation Physicist']
#    only -- there is no 'Radiation Dosimetrist / Planner' action wired into the radiation record
#    itself (that role's real surface in this repo is the generic support-referral pathway added
#    in Phase 2, a parallel channel, not a mutator of the radiation record). RO performs
#    simulation/contouring/plan-prep status fields directly; Physicist performs independent
#    Physics QA only. This action does not dispatch on an 'operation' key -- every call is a
#    generic versioned PATCH of the planning sub-object, gated by an explicit plan_version field
#    (not the generic expected_version/OPTIMISTIC_LOCK_ACTIONS mechanism).
#  - There is no rt_treatment_release action: RO combines physician_final_approval='Approved' and
#    status='Ready for Treatment' in the same rt_planning_status call once physics_qa is current
#    for the same plan/prescription version -- functionally the "release" step.
#  - There is no rt_amend_prescription/rt_complete_course action: an "amendment" after an
#    interruption is simply calling rt_save_prescription again with sign:True and changed material
#    fields on the SAME radiation record (not a new superseding record) -- the server auto-bumps
#    prescription_version, pushes the old prescription into prescription_history, and resets
#    contouring_status/planning_status/physics_qa/physician_final_approval to Pending (carrying
#    simulation_status forward), which naturally proves old approvals do not carry over. Course
#    completion is likewise automatic: rt_deliver_fraction sets status to 'Completed' once
#    delivered fraction count reaches the (possibly amended) prescribed fraction count.
#  - No task/handoff is auto-created at prescription-sign or plan-ready time (rt_save_prescription
#    and rt_planning_status only grant_patient_access/journey_add; they don't call handoff()), so
#    there are no "Planner simulation task" / "Physicist QA task" / "RTT delivery task" /
#    "post-treatment Navigator handoff" task-inbox entries to assert on for those steps -- this
#    reflects this repo's actual (unmodified, deliberately not reworked) RT action bodies, not a
#    porting gap. The two RT actions that WERE newly ported in this merge (rt_record_otv,
#    rt_record_interruption) do use handoff()/complete_open_tasks(), so those ARE asserted below.
import json,urllib.request,urllib.error,urllib.parse,pathlib,sqlite3,sys,os
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parent;BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765');PID='PAT-VAL-NEHA';TOK={};rows=[]
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
OPT={'save_intake','med_recon','save_dynamic_form','save_consultation','save_diagnosis','save_appointment','queue_patient','save_care_plan','save_treatment_plan','save_radiology','save_pathology','mdt_comment','mdt_attendance','mdt_recommend','save_referral'}
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
def src(role,tid):return http('/api/task-source?task='+urllib.parse.quote(tid),token=login(role))
def ck(name,ok,d=None):
 rows.append({'check':name,'pass':bool(ok),'detail':d});print(('PASS' if ok else 'FAIL'),name,json.dumps(d,ensure_ascii=False,default=str)[:900] if d is not None else '')
 if not ok:raise AssertionError(name+' '+str(d))

TODAY='2026-09-09'

# --- Registration / referral / intake --------------------------------------------------
reg=ent('Front Desk','registration');ck('RT-001 baseline registration draft',reg and reg['status']=='Draft',reg and {'id':reg['id'],'status':reg['status']})
st,j=action('Front Desk','save_registration',reg['id'],{'name':'Neha Kulkarni','dob':'1979-11-03','sex':'Female','phone':'917000000102','id_number':'SYN-NEHA-02','assigned_specialty':'Radiation Oncology','complete':True});ck('RT-002 registration complete',st==200,j)
ref=ent('Front Desk','referral');st,j=action('Front Desk','save_referral',ref['id'],{'status':'Assigned','assigned_department':'Medical Oncology','assigned_clinician':'Dr Asha Mehta','priority':'Routine'});ck('RT-003 referral assigned to MO triage',st==200,j)
t=task('Medical Oncology','Referral lifecycle',ref['id']);ck('RT-004 MO referral task',bool(t),t)
st,sctx=src('Medical Oncology',t['id']);ck('RT-005 MO opens exact referral source',st==200 and sctx.get('source_record_id')==ref['id'],sctx)
st,j=action('Medical Oncology','save_referral',ref['id'],{'status':'Accepted'});ck('RT-006 referral accepted',st==200 and j.get('status')=='Accepted',j)
intake=ent('Intake Nurse','intake');st,j=action('Intake Nurse','save_intake',intake['id'],{'sbp':122,'dbp':74,'hr':76,'rr':16,'temp':36.6,'spo2':99,'weight':61,'height':160,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'ecog':'1','kps':'90','pain_score':2,'pain_instrument':'Numeric Rating Scale 0–10','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':2,'nkda':True,'complete':True});ck('RT-007 intake signed',st==200 and j.get('bsa_m2',0)>0,j)

# --- MO consultation + diagnosis (consultation write is MO-only in this repo) ----------
cons=ent('Medical Oncology','consultation');st,j=action('Medical Oncology','save_consultation',cons['id'],{'sign':True,'encounter_type':'New Oncology Consultation','date':TODAY,'chief_complaint':'Locally advanced cervical cancer referred for definitive radiotherapy planning','hpi':'Biopsy-proven cervical squamous cell carcinoma with parametrial involvement; no distant metastasis on staging.','ros':'No active infection; mild pelvic pain; no acute cardiopulmonary complaint.','assessment':'Cervical squamous cell carcinoma, FIGO 2018 Stage IIB, cT2b cN0 cM0.','plan':'Multidisciplinary review followed by definitive external-beam radiotherapy planning in synthetic validation workflow.','physical_exam_structured':{'general':'ECOG 1, clinically stable','cardiovascular':'Normal heart sounds','respiratory':'Clear bilateral air entry','abdomen':'Soft, non-tender','neurologic':'No focal deficit','tumor_site':'Synthetic pelvic exam: parametrial involvement without pelvic sidewall fixation'}});ck('RT-008 MO consultation signed',st==200 and j.get('status')=='Signed',j)
dx=ent('Medical Oncology','diagnosis');st,j=action('Medical Oncology','save_diagnosis',dx['id'],{'verify':True,'icd10':'C53.9','icd10_version':'ICD-10','icdo_topography':'C53.9','icdo_morphology':'8070/3','icdo_version':'ICD-O-3','cancer_type':'Cervical Cancer','primary_site':'Cervix uteri','histology':'Squamous cell carcinoma','grade':'2','staging_system':'FIGO','staging_version':'2018','staging_date':TODAY,'staging_basis':'Clinical','stage_t':'cT2b','stage_n':'cN0','stage_m':'cM0','stage_group':'Stage IIB','classification_value':'FIGO Stage IIB','classification_system':'FIGO 2018','treatment_intent':'Definitive','disease_status':'Newly diagnosed','biomarkers':[]});ck('RT-009 diagnosis verified',st==200 and j.get('status')=='Verified',j)

# --- MDT -> Chair -> RO plan -------------------------------------------------------------
st,j=action('Medical Oncology','submit_mdt_case','',{'clinical_question':'Confirm definitive Radiation Oncology strategy for FIGO IIB cervical cancer.','clinical_summary':'Cervical squamous cell carcinoma, cT2b cN0 cM0, FIGO 2018 Stage IIB, ECOG 1.','meeting_mode':'Internal','meeting_at':TODAY+'T10:00:00+05:30'});ck('RT-010 MDT submitted',st==200,j);mdt=j['mdt_id']
collab=ent('MDT Coordinator','mdt_collab')
for idx,(name,disc) in enumerate([('Dr Asha Mehta','Medical Oncology'),('Dr Neha Rao','Radiation Oncology'),('Dr Karan Shah','Surgical Oncology'),('Dr Rohan Kulkarni','Radiology'),('Dr Mira Desai','Pathology')],1):
    st,j=action('MDT Coordinator','mdt_attendance',collab['id'],{'name':name,'discipline':disc,'status':'Present'});ck(f'RT-011.{idx} attendance {disc}',st==200,j);collab=ent('MDT Coordinator','mdt_collab')
st,j=action('MDT Coordinator','mdt_recommend',mdt,{'meeting_at':TODAY+'T10:00:00+05:30','clinical_question':'Confirm definitive Radiation Oncology strategy for FIGO IIB cervical cancer.','clinical_summary':'FIGO IIB cervical squamous carcinoma, non-metastatic, ECOG 1.','intent':'Definitive','recommendation':'Proceed with governed synthetic pelvic external-beam radiotherapy workflow with staged simulation, contouring, planning, Physics QA and RO release.','rationale':'Multidisciplinary consensus for synthetic RT validation pathway.','final_consensus':'Consensus','specialty_responsible':'Radiation Oncology','actions':[{'description':'Create and authorize radiation Treatment Plan','owner_role':'Radiation Oncology','due_date':'2026-09-10','priority':'High'}]});ck('RT-012 Coordinator recommendation',st==200 and j.get('status')=='Pending Chair Approval',j)
t=task('MDT Chair','MDT case preparation');ck('RT-013 Chair task',bool(t),t)
st,j=action('MDT Chair','mdt_chair_sign',mdt,{'decision':'Approve','reason':'Recommendation accurately reflects multidisciplinary discussion.'});ck('RT-014 Chair signs',st==200 and j.get('status')=='MDT Recommended',j)
st,j=action('Radiation Oncology','create_plan_from_mdt',mdt,{'specialty':'Radiation Oncology'});ck('RT-015 RO treatment plan created',st==200,j);plan_id=j['id']
st,j=action('Radiation Oncology','save_treatment_plan',plan_id,{'sign':True,'line_of_therapy':'Definitive first-line Radiation Oncology treatment'});ck('RT-016 RO treatment plan signed',st==200 and j.get('status')=='Clinician Approved',j)

# --- RT course: negative before prescription, then signed prescription -----------------
rt=ent('Radiation Oncology','radiation');ck('RT-017 radiation record available',bool(rt),rt and {'id':rt['id'],'status':rt['status']})
rtid=rt['id']
st,j=action('Medical Oncology','rt_save_prescription',rtid,{'sign':True});ck('RT-018 wrong-role prescription blocked',st==403,j)
st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered','delivered_dose_gy':2.0,'image_guidance_performed':True});ck('RT-019 RTT has no access before prescription signed',st==403,j)
rx={'site':'Pelvis / cervix','laterality':'Midline','intent':'Definitive','modality':'External Beam','technique':'VMAT','energy':'6 MV','treatment_phase':'Pelvic phase','total_dose_gy':50.0,'dose_per_fraction_gy':2.0,'fractions':25,'frequency':'Daily, 5 fractions/week','planned_start':'2026-09-10','target_volumes':[{'name':'GTV cervix','volume_type':'GTV','prescription_dose_gy':50.0},{'name':'CTV pelvis','volume_type':'CTV','prescription_dose_gy':50.0},{'name':'PTV pelvis','volume_type':'PTV','margin_mm':5,'prescription_dose_gy':50.0}],'organs_at_risk':['Bladder','Rectum','Bowel','Femoral heads'],'oar_constraints':[{'organ':'Bladder','metric':'V45Gy','operator':'<','value':35,'unit':'%'},{'organ':'Rectum','metric':'V45Gy','operator':'<','value':60,'unit':'%'}],'simulation_requirement':'CT simulation','image_guidance':'Daily CBCT','bolus':'None','special_instructions':'Synthetic validation prescription only','sign':True}
st,j=action('Radiation Oncology','rt_save_prescription',rtid,rx);ck('RT-020 RT prescription signed',st==200 and j.get('status')=='RT Oncologist Approved',j)

# --- Physics QA before simulation/contour/plan complete must block ---------------------
st,j=action('Radiation Physicist','rt_planning_status',rtid,{'plan_version':1,'physics_qa':'Approved','physics_qa_note':'premature','qa_method':'Independent calculation'});ck('RT-021 QA before plan complete blocked',st==409,j)

# --- RO performs simulation / contouring / plan preparation (own-model: RO, not Planner) -
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'simulation_status':'Completed','status':'Simulation Complete'});ck('RT-022 simulation recorded',st==200 and j.get('status')=='Simulation Complete',j)
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'contouring_status':'Completed','status':'Contouring Approved'});ck('RT-023 contouring recorded',st==200 and j.get('status')=='Contouring Approved',j)
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'planning_status':'Planning Complete','status':'Plan Ready for Physics QA'});ck('RT-024 plan ready for Physics QA',st==200 and j.get('status')=='Plan Ready for Physics QA',j)

# --- RO cannot silently grant its own Physics QA (field is outside RO's material whitelist) -
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'physics_qa':'Approved','physics_qa_note':'wrong role attempt'})
chk=ent('Radiation Oncology','radiation',rtid);ck('RT-025 RO cannot self-approve Physics QA',st==200 and chk['data']['planning'].get('physics_qa')=='Pending',{'status':st,'physics_qa':chk['data']['planning'].get('physics_qa')})

# --- Independent Physics QA ---------------------------------------------------------------
st,j=action('Radiation Physicist','rt_planning_status',rtid,{'plan_version':1,'physics_qa':'Approved','physics_qa_note':'Independent plan/geometry/dose QA passed for synthetic validation.','qa_method':'Independent secondary calculation + checklist','qa_completed_at':TODAY+'T13:00:00+05:30'});ck('RT-026 Physics QA approved',st==200,j)
chk=ent('Radiation Oncology','radiation',rtid);ck('RT-027 physics_qa recorded at current plan version',chk['data']['planning'].get('physics_qa')=='Approved' and chk['data']['planning'].get('physics_qa_plan_version')==1,chk['data']['planning'])

# --- Delivery before RO final approval must still block ---------------------------------
st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered','delivered_dose_gy':2.0,'image_guidance_performed':True});ck('RT-028 delivery before RO final approval blocked',st==409,j)

# --- RO final approval + release (combined, since this repo has no separate release action) -
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'physician_final_approval':'Approved','status':'Ready for Treatment'});ck('RT-029 RO final approval + release',st==200 and j.get('status')=='Ready for Treatment',j)

# --- Hard overdose, first five fractions, duplicate blocked -----------------------------
st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered','date_time':'2026-09-10T09:00:00+05:30','delivered_dose_gy':25.0,'image_guidance_performed':True});ck('RT-030 25Gy vs 2Gy blocked',st==409 and 'dose safety' in j.get('error','').lower(),j)
for n in range(1,6):
    st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':n,'status':'Delivered','date_time':f'2026-09-{9+n:02d}T09:00:00+05:30','delivered_dose_gy':2.0,'image_guidance_performed':True,'setup_variation':'Within synthetic tolerance','toxicity':'Mild fatigue' if n==5 else ''});ck(f'RT-031.{n} fraction {n} delivered',st==200,j)
    if n==1:
        st2,j2=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered','delivered_dose_gy':2.0,'image_guidance_performed':True});ck('RT-032 duplicate fraction blocked',st2==409 and 'duplicate' in j2.get('error','').lower(),j2)
st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':6,'status':'Delivered','delivered_dose_gy':42.0,'image_guidance_performed':True});ck('RT-033 cumulative overdose blocked',st==409,j)

# --- OTV after fraction 5 (newly ported action) ------------------------------------------
st,j=action('Radiation Oncology','rt_record_otv',rtid,{'after_fraction':5,'assessment':'Clinically stable after first five fractions.','toxicity_summary':'Mild Grade 1 fatigue; no treatment-limiting toxicity.','plan':'Continue RT and monitor symptoms.','weight_kg':61,'performance_status':'ECOG 1'});ck('RT-034 OTV signed',st==200,j)

# --- Interruption (newly ported action) -> RO task via handoff --------------------------
st,j=action('Radiation Technologist','rt_record_interruption',rtid,{'start_at':'2026-09-15T09:00:00+05:30','reason':'Synthetic setup/anatomy change requiring RO review and adaptive replanning','category':'Clinical','compensation_plan':'RO review and adaptive replanning before further delivery'});ck('RT-035 interruption recorded',st==200 and j.get('next_role')=='Radiation Oncology',j)
t=task('Radiation Oncology','RT interruption review',rtid);ck('RT-036 RO interruption task',bool(t),t)
st,sctx=src('Radiation Oncology',t['id']);ck('RT-037 RO opens exact interrupted-course source',st==200 and sctx.get('source_record_id')==rtid,sctx)

# --- Amendment: re-sign the SAME record with changed material fields --------------------
rx2={**rx,'total_dose_gy':20.0,'dose_per_fraction_gy':2.0,'fractions':10,'treatment_phase':'Adaptive validation phase — shortened course','planned_start':'2026-09-15','special_instructions':'Superseding adaptive synthetic validation prescription','sign':True}
st,j=action('Radiation Oncology','rt_save_prescription',rtid,rx2);ck('RT-038 amended prescription signed (in place)',st==200 and j.get('status')=='RT Oncologist Approved',j)
chk=ent('Radiation Oncology','radiation',rtid);pl=chk['data']['planning'];ck('RT-039 amendment bumped version and reset approvals',chk['data']['prescription'].get('prescription_version')==2 and pl.get('plan_version')==2 and pl.get('contouring_status')=='Pending' and pl.get('physics_qa')=='Pending' and pl.get('physician_final_approval')=='Pending' and pl.get('simulation_status')=='Completed',pl)

# --- Old approvals invalidated: delivery of fraction 6 must now block -------------------
st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':6,'status':'Delivered','delivered_dose_gy':2.0,'image_guidance_performed':True});ck('RT-040 stale approvals block delivery after amendment',st==409,j)

# --- Re-contour / re-plan / re-QA / re-approve at the new version -----------------------
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':2,'contouring_status':'Completed','status':'Contouring Approved'});ck('RT-041 adaptive contouring',st==200,j)
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':2,'planning_status':'Planning Complete','status':'Plan Ready for Physics QA'});ck('RT-042 adaptive plan ready',st==200,j)
st,j=action('Radiation Physicist','rt_planning_status',rtid,{'plan_version':2,'physics_qa':'Approved','physics_qa_note':'Adaptive plan independently QA checked.','qa_method':'Independent secondary calculation','qa_completed_at':'2026-09-15T13:00:00+05:30'});ck('RT-043 adaptive Physics QA',st==200,j)
st,j=action('Radiation Oncology','rt_planning_status',rtid,{'plan_version':2,'physician_final_approval':'Approved','status':'Ready for Treatment'});ck('RT-044 adaptive RO approval + release',st==200 and j.get('status')=='Ready for Treatment',j)

# --- Deliver remaining 5 fractions (6-10) -> auto-completes course ----------------------
for n in range(6,11):
    st,j=action('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':n,'status':'Delivered','date_time':f'2026-09-{15+(n-5):02d}T09:00:00+05:30','delivered_dose_gy':2.0,'image_guidance_performed':True,'setup_variation':'Within tolerance'});ck(f'RT-045.{n} adaptive fraction {n} delivered',st==200,j)
ck('RT-046 course auto-completed at prescribed fraction count',j.get('status')=='Completed' and j.get('delivered_count')==10,j)
st,j=action('Radiation Oncology','rt_record_otv',rtid,{'after_fraction':10,'assessment':'Adaptive shortened course completed clinically stable.','toxicity_summary':'Mild fatigue only.','plan':'Complete course and arrange follow-up.','weight_kg':60.8,'performance_status':'ECOG 1'});ck('RT-047 final OTV',st==200,j)

# --- Record completed RT course into treatment history, triggering EOT completion review -
st,j=action('Radiation Oncology','record_treatment_history_event','',{'type':'Radiation Therapy','date':'2026-09-24','status':'Completed','description':'Definitive pelvic radiotherapy course (adaptive, 20 Gy in 10 fractions after replanning) completed as prescribed.','source_record_id':rtid,'trigger_completion_review':True});ck('RT-048 RT course recorded into treatment history',st==200 and bool(j.get('task_id')),j)
t=task('Radiation Oncology','Treatment completion review');ck('RT-049 EOT completion-review task created',bool(t),t)

# --- audit chain --------------------------------------------------------------------------
conn=sqlite3.connect(ROOT/'cca_v12.sqlite3');conn.row_factory=sqlite3.Row;aud=[dict(x) for x in conn.execute('SELECT actor_id,actor_role,action,entity_type,entity_id,at FROM audit WHERE patient_id=? ORDER BY id',(PID,))];conn.close()
wanted={'RT_PRESCRIPTION','RT_PLANNING','RT_FRACTION','RT_OTV_SIGN','RT_INTERRUPTION','TREATMENT_HISTORY_EVENT'};got={x['action'] for x in aud};ck('RT-050 named audit chain',wanted.issubset(got),sorted(got & wanted))

out={'patient_id':PID,'patient':'Neha Kulkarni','build':'12.2-PC7.1-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(1 for x in rows if x['pass']),'fail':sum(1 for x in rows if not x['pass']),'results':rows,'key_records':{'mdt':mdt,'treatment_plan':plan_id,'radiation':rtid}}
(ROOT/'validation_evidence'/'PC8_NEHA_RT_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail','key_records']},ensure_ascii=False))
sys.exit(1 if out['fail'] else 0)
