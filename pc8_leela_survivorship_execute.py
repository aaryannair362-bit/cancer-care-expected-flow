#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download, targeting this repo's
# PAT-VAL-LEELA validation patient (same "Leela Nair" synthetic identity, distinct id/mrn
# from the pre-existing PAT-DEMO-SURV showcase patient).
#
# This journey needed far less rework than the RT/surgery ports: request_treatment_history_
# confirmation, record_treatment_history_event, save_treatment_completion, save_survivorship_
# plan, record_surveillance and confirm_progression were all ported into server.py in this
# merge FROM the PC8.0 original almost verbatim (field names, response keys, task_type
# strings), so most of the original script's assertions hold unmodified. Two adaptations were
# required after reading the actual save_consultation body: this repo's save_consultation has
# no dependency on save_intake's status at all (no "sign consultation before intake" gate
# exists), so the PC8.0 original's LEE-008/LEE-010 negative/task checks for that gate have no
# equivalent here and are omitted; intake is still performed first for narrative realism, just
# not asserted as a hard prerequisite. save_intake itself needs this repo's actual field
# shape (split sbp/dbp/temp/weight/height + explicit units + complete:True, matching every
# other ported journey script) rather than PC8.0's combined bp/temp_c/weight_kg field names.
# The UI-contract static check targets static/pc8_connected.js (where this repo's survivorship
# page actually lives) rather than static/app.js, using this repo's own action/data-act names.
import json,urllib.request,urllib.error,urllib.parse,pathlib,sys,os
from datetime import date,datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parent;BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765');PID='PAT-VAL-LEELA';TODAY='2026-09-09';rows=[];TOK={}
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
OPT={'save_registration','save_referral','save_intake','save_consultation','save_diagnosis','save_survivorship_plan'}
def action(role,a,eid='',data=None,expected=None):
    payload={'action':a,'patient_id':PID,'entity_id':eid,'data':data or {}}
    if a in OPT and eid:
        if expected is None:
            found=None
            for xs in boot(role).get('entities',{}).values():
                for x in xs:
                    if x['id']==eid:found=x;break
                if found:break
            if found:expected=found['version']
        if expected is not None:payload['expected_version']=expected
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

# Establish credible treating-clinician source state via normal workflow.
reg=entity('Front Desk','registration');check('LEE-001 baseline registration task/source',bool(reg),reg and reg['id'])
st,j=action('Front Desk','save_registration',reg['id'],{'name':'Leela Nair','dob':'1970-04-17','sex':'Female','phone':'917000000105','id_number':'SYN-LEELA-01','assigned_specialty':'Medical Oncology','complete':True});check('LEE-002 registration completed',st==200,j)
ref=entity('Front Desk','referral');st,j=action('Front Desk','save_referral',ref['id'],{'status':'Assigned','assigned_department':'Medical Oncology','assigned_clinician':'Dr Asha Mehta','priority':'Routine','reason':'Post-treatment survivorship transition review'});check('LEE-003 referral assigned',st==200 and j.get('status')=='Assigned',j)
rt=task('Medical Oncology','Referral lifecycle',source_id=ref['id']);check('LEE-004 MO receives referral task',bool(rt),rt)
st,src=source('Medical Oncology',rt['id']);check('LEE-005 exact referral source/provenance',st==200 and src.get('source_record_id')==ref['id'],src)
st,j=http('/api/action','POST',{'action':'save_referral','patient_id':PID,'entity_id':ref['id'],'data':{'status':'Accepted'}},login('Surgical Oncology'));check('LEE-006 wrong-role referral acceptance blocked',st==403,j)
st,j=action('Medical Oncology','save_referral',ref['id'],{'status':'Accepted'});check('LEE-007 referral accepted',st==200 and j.get('status')=='Accepted',j)
intake=entity('Intake Nurse','intake');st,j=action('Intake Nurse','save_intake',intake['id'],{'sbp':122,'dbp':74,'hr':70,'rr':15,'temp':36.6,'spo2':99,'weight':62,'height':160,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'ecog':'0','kps':'100','pain_score':0,'pain_instrument':'Numeric Rating Scale 0–10','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':0,'nkda':True,'complete':True});check('LEE-008 intake signed',st==200 and j.get('bsa_m2',0)>0,j)
cons=entity('Medical Oncology','consultation');st,j=action('Medical Oncology','save_consultation',cons['id'],{'sign':True,'encounter_type':'Follow-up Medical Oncology Consultation','date':TODAY,'chief_complaint':'Post-treatment follow-up','hpi':'Completed prior curative breast cancer therapy and transitioning to survivorship.','ros':'No new systemic symptoms.','assessment':'Clinically stable after completed curative therapy.','plan':'End-of-treatment review and survivorship planning.','physical_exam_structured':{'general':'Well appearing','cardiovascular':'Normal','respiratory':'Clear','abdomen':'Soft','neurologic':'No focal deficit','tumor_site':'No new breast/chest wall concern'}});check('LEE-009 consultation signed',st==200 and j.get('status')=='Signed',j)
dx=entity('Medical Oncology','diagnosis');st,j=action('Medical Oncology','save_diagnosis',dx['id'],{'verify':True,'icd10':'C50.9','icd10_version':'ICD-10','icdo_topography':'C50.9','icdo_morphology':'8500/3','icdo_version':'ICD-O-3','cancer_type':'Breast Cancer','primary_site':'Right breast','histology':'Invasive carcinoma of no special type / ductal carcinoma','grade':'2','staging_system':'AJCC','staging_version':'Breast v8','staging_date':TODAY,'staging_basis':'Clinical','stage_t':'cT2','stage_n':'cN0','stage_m':'cM0','stage_group':'Stage IIA','treatment_intent':'Curative','disease_status':'Post-treatment follow-up'});check('LEE-010 diagnosis/staging verified',st==200 and j.get('status')=='Verified',j)
episode_before=entity('Medical Oncology','cancer_episode')['id'];check('LEE-011 active Cancer Episode established',episode_before=='EP-SYN-VAL-05',episode_before)

# Historical treatment reconciliation is task-driven: each specialty receives a responsibility before it can enter its own prior-treatment fact.
th=entity('Medical Oncology','treatment_history')
st,j=action('Medical Oncology','request_treatment_history_confirmation','',{'target_role':'Surgical Oncology','type':'Surgery','reason':'Synthetic survivorship validation: confirm prior completed surgery within this Cancer Episode.'});check('LEE-012 Surgery confirmation responsibility created',st==200 and j.get('next_role')=='Surgical Oncology',j)
sht=task('Surgical Oncology','Historical treatment confirmation');check('LEE-013 Surgical Oncology receives history-confirmation task',bool(sht),sht)
st,src=source('Surgical Oncology',sht['id']);check('LEE-014 Surgeon opens exact provenance',st==200 and bool(src.get('source_record_id')),src)
st,j=action('Surgical Oncology','record_treatment_history_event',th['id'],{'type':'Surgery','date':'2026-03-12','status':'Completed','description':'Right breast-conserving surgery with sentinel-node procedure — synthetic historical treatment entered for survivorship validation','entered_reason':'Synthetic validation historical treatment confirmed by treating Surgical Oncologist','trigger_completion_review':False});check('LEE-015 Surgery treatment history entered by owning treating role',st==200,j)
st,j=action('Medical Oncology','request_treatment_history_confirmation','',{'target_role':'Radiation Oncology','type':'Radiation Therapy','reason':'Synthetic survivorship validation: confirm prior completed RT within this Cancer Episode.'});check('LEE-016 RT confirmation responsibility created',st==200 and j.get('next_role')=='Radiation Oncology',j)
rht=task('Radiation Oncology','Historical treatment confirmation');check('LEE-017 Radiation Oncology receives history-confirmation task',bool(rht),rht)
st,j=action('Radiation Oncology','record_treatment_history_event',th['id'],{'type':'Radiation Therapy','date':'2026-05-20','status':'Completed','description':'Adjuvant right-breast radiation course completed — synthetic historical treatment','entered_reason':'Synthetic validation historical RT completion confirmed by Radiation Oncologist','trigger_completion_review':False});check('LEE-018 RT treatment history entered by treating RO',st==200,j)
st,j=action('Medical Oncology','record_treatment_history_event',th['id'],{'type':'Systemic Therapy','date':'2026-07-30','status':'Completed','description':'Adjuvant systemic/endocrine treatment phase completed for end-of-treatment review — synthetic validation','entered_reason':'Synthetic validation completion entered by Medical Oncologist','trigger_completion_review':True});check('LEE-019 completed treatment creates EOT responsibility',st==200 and j.get('task_id'),j);eot_task_id=j['task_id']
t=task('Medical Oncology','Treatment completion review','treatment_history',th['id']);check('LEE-020 MO sees End-of-Treatment Review task',t and t['id']==eot_task_id,t)
st,src=source('Medical Oncology',t['id']);check('LEE-021 EOT task opens exact treatment-history source',st==200 and src.get('source_record_id')==th['id'] and src.get('episode',{}).get('id')==episode_before,src)
# wrong role and mandatory negative
st,j=action('Nurse Navigator','save_treatment_completion','',{'sign':True});check('LEE-022 Navigator cannot sign clinician treatment summary',st==403,j)
tc=entity('Medical Oncology','treatment_completion')
st,j=action('Medical Oncology','save_treatment_completion',tc['id'],{'sign':True,'treatment_completed':True});check('LEE-023 incomplete EOT summary blocked',st==409 and j.get('missing'),j)
completion={'sign':True,'treatment_completed':True,'completion_date':'2026-07-30','diagnosis_at_completion':'Right breast invasive ductal carcinoma, AJCC Breast v8 Stage IIA','treatment_received':'Breast-conserving surgery, adjuvant radiation, and systemic/endocrine treatment — synthetic validation history','current_disease_status':'No evidence of active disease; survivorship transition','late_effect_risks':'Lymphedema, bone health effects, endocrine symptoms, radiation late effects','follow_up_recommendations':'Survivorship plan, clinical surveillance, breast imaging and symptom-triggered evaluation.'}
st,j=action('Medical Oncology','save_treatment_completion',tc['id'],completion);check('LEE-024 treatment summary signed',st==200 and j.get('status')=='Signed' and j.get('next_role')=='Nurse Navigator',j);tc_id=j['id']
t=task('Medical Oncology','Treatment completion review',status='Open');check('LEE-025 EOT review task closed',t is None,t)
nt=task('Nurse Navigator','Survivorship planning','treatment_completion',tc_id);check('LEE-026 Navigator automatically receives Survivorship task',bool(nt),nt)
st,src=source('Nurse Navigator',nt['id']);check('LEE-027 Navigator opens exact signed Treatment Summary/provenance',st==200 and src.get('source_record_id')==tc_id and src.get('source_record_status')=='Signed' and src.get('signed_by'),src)
# immutable + superseding amendment
st,j=action('Medical Oncology','save_treatment_completion',tc_id,{**completion,'follow_up_recommendations':'Attempt overwrite'});check('LEE-028 signed Treatment Summary overwrite blocked',st==409 and 'immutable' in j.get('error','').lower(),j)
st,j=action('Medical Oncology','save_treatment_completion',tc_id,{**completion,'follow_up_recommendations':'Updated surveillance recommendation after multidisciplinary record reconciliation.','amendment_reason':'Clarify surveillance recommendation without changing treatment history'});check('LEE-029 Treatment Summary amendment creates superseding signed version',st==200 and j.get('status')=='Signed' and j.get('supersedes')==tc_id,j);tc2=j['id']
old_tc=entity('Medical Oncology','treatment_completion',tc_id);new_tc=entity('Medical Oncology','treatment_completion',tc2);check('LEE-030 previous signed summary retained as Superseded',old_tc and old_tc['status']=='Superseded' and new_tc and new_tc['status']=='Signed',{'old':old_tc and old_tc['status'],'new':new_tc and new_tc['status']})
nt=task('Nurse Navigator','Survivorship planning','treatment_completion',tc2);check('LEE-031 Navigator receives superseding Treatment Summary task',bool(nt),nt)
# plan draft consumption negative/wrong role
sp=entity('Nurse Navigator','survivorship')
st,j=action('Medical Oncology','save_survivorship_plan',sp['id'],{'treatment_completion_id':tc2,'sign':True});check('LEE-032 wrong-role survivorship plan blocked',st==403,j)
plan={'treatment_completion_id':tc2,'surveillance_schedule':'Clinical oncology review every 3–6 months initially; annual disease-appropriate breast imaging in this synthetic validation plan.','late_effect_monitoring':'Monitor lymphedema, bone health, cardiopulmonary/radiation late effects and endocrine treatment effects.','health_promotion':'Exercise, healthy weight, smoking avoidance, vaccination and bone-health measures.','red_flags':'New breast/chest wall mass, persistent bone pain, unexplained weight loss, dyspnea or neurologic symptoms.','contact_plan':'Nurse Navigator contact plus direct oncology escalation for red flags.','next_surveillance_at':'2026-12-09','sign':True}
st,j=action('Nurse Navigator','save_survivorship_plan',sp['id'],plan);check('LEE-033 Survivorship Plan signed',st==200 and j.get('status')=='Signed',j);sp_id=j['id']
svtask=task('Nurse Navigator','Surveillance encounter','survivorship',sp_id);check('LEE-034 Navigator gets surveillance task',bool(svtask),svtask)
st,src=source('Nurse Navigator',svtask['id']);check('LEE-035 surveillance task exact signed plan source',st==200 and src.get('source_record_id')==sp_id and src.get('source_record_status')=='Signed',src)
# amendment behavior
st,j=action('Nurse Navigator','save_survivorship_plan',sp_id,{**plan,'red_flags':'Attempt overwrite'});check('LEE-036 signed plan overwrite blocked',st==409 and 'immutable' in j.get('error','').lower(),j)
st,j=action('Nurse Navigator','save_survivorship_plan',sp_id,{**plan,'red_flags':'Updated: new breast/chest wall mass, persistent focal bone pain, unexplained weight loss, dyspnea, persistent headache/neurologic symptoms.','amendment_reason':'Clarify red-flag wording after patient education review'});check('LEE-037 Survivorship amendment creates superseding signed plan',st==200 and j.get('status')=='Signed' and j.get('supersedes')==sp_id,j);sp2=j['id']
old_sp=entity('Nurse Navigator','survivorship',sp_id);new_sp=entity('Nurse Navigator','survivorship',sp2);check('LEE-038 previous plan preserved Superseded',old_sp and old_sp['status']=='Superseded' and new_sp and new_sp['status']=='Signed',{'old':old_sp and old_sp['status'],'new':new_sp and new_sp['status']})
svtask=task('Nurse Navigator','Surveillance encounter','survivorship',sp2);check('LEE-039 new plan creates surveillance responsibility',bool(svtask),svtask)
sv=entity('Nurse Navigator','surveillance')
st,j=action('Nurse Navigator','record_surveillance',sv['id'],{'date':'2026-12-09','assessment':'New persistent right chest-wall nodularity and focal rib discomfort; synthetic surveillance concern requiring oncologist confirmation.','disease_status':'Suspected Recurrence','symptoms':['New right chest-wall nodularity','Persistent focal rib discomfort'],'investigations':['Synthetic surveillance imaging flagged suspicious chest-wall lesion'],'suspected_progression':True});check('LEE-040 suspected recurrence surveillance recorded',st==200 and j.get('next_role')=='Medical Oncology',j);enc_id=j['encounter']['id']
pt=task('Medical Oncology','Progression confirmation','surveillance',sv['id']);check('LEE-041 MO receives progression confirmation task',bool(pt),pt)
st,src=source('Medical Oncology',pt['id']);check('LEE-042 MO opens exact surveillance source/provenance',st==200 and src.get('source_record_id')==sv['id'] and src.get('episode',{}).get('id')==episode_before,src)
st,j=action('Nurse Navigator','confirm_progression',sv['id'],{'disease_status':'Confirmed Recurrence','evidence_summary':'test'});check('LEE-043 wrong role progression confirmation blocked',st==403,j)
st,j=action('Medical Oncology','confirm_progression',sv['id'],{'disease_status':'Confirmed Recurrence','evidence_summary':''});check('LEE-044 missing progression evidence blocked',st==409,j)
st,j=action('Medical Oncology','confirm_progression',sv['id'],{'disease_status':'Confirmed Recurrence','evidence_summary':'Synthetic surveillance imaging plus clinical chest-wall finding supports confirmed recurrence for workflow validation.','evidence_source_ids':[sv['id'],enc_id]});check('LEE-045 recurrence confirmed + new line + MDT task',st==200 and j.get('episode_id_before')==episode_before and j.get('episode_id_after')==episode_before and j.get('next_role')=='MDT Coordinator',j);mdt_id=j['mdt_id'];line_no=j['line_number']
b=boot('Medical Oncology');ep_after=entity('Medical Oncology','cancer_episode')['id'];hist=entity('Medical Oncology','treatment_history');line=[x for x in hist['data'].get('episodes',[]) if x.get('type')=='Line of Therapy' and x.get('source_status_event_id')==j['status_event']['id']]
check('LEE-046 Cancer Episode unchanged across recurrence',episode_before==ep_after=='EP-SYN-VAL-05',{'before':episode_before,'after':ep_after})
check('LEE-047 new Line of Therapy appended in same episode',len(line)==1 and line[0].get('episode_id')==episode_before and line[0].get('line_number')==line_no,line)
mt=task('MDT Coordinator','MDT case preparation','mdt',mdt_id);check('LEE-048 MDT Coordinator receives recurrence planning task',bool(mt),mt)
st,src=source('MDT Coordinator',mt['id']);check('LEE-049 MDT task exact submitted recurrence source',st==200 and src.get('source_record_id')==mdt_id and src.get('episode',{}).get('id')==episode_before,src)
aud=boot('Medical Oncology').get('audit',[]);wanted={'TREATMENT_HISTORY_EVENT','TREATMENT_COMPLETION_SIGN','SURVEILLANCE_ENCOUNTER','DISEASE_STATUS_CONFIRM','NEW_LINE_OF_THERAPY','MDT_CASE_SUBMIT'};present={x.get('action') for x in aud};check('LEE-050 named-user audit covers longitudinal transitions',len(wanted & present)>=5,sorted(wanted & present))

# UI contract static check (vanilla JS; this repo's survivorship page lives in pc8_connected.js)
js=(ROOT/'static/pc8_connected.js').read_text(encoding='utf-8')
ui_need=['Treatment Completion / Survivorship','record_treatment_history_event','tc-sign','sp-sign','record-surveillance','confirm-progression','Open Source Record','Perform My Action','Refresh Worklist']
check('LEE-051 vanilla-JS worklist/action mappings present',all(x in js for x in ui_need),[x for x in ui_need if x not in js])

out={'patient_id':PID,'patient':'Leela Nair','build':'12.2-PC7.1-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(x['pass'] for x in rows),'fail':sum(not x['pass'] for x in rows),'episode_before':episode_before,'episode_after':ep_after,'new_line_number':line_no,'mdt_id':mdt_id,'results':rows}
(ROOT/'validation_evidence'/'PC8_LEELA_SURVIVORSHIP_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail','episode_before','episode_after','new_line_number','mdt_id']},ensure_ascii=False))
sys.exit(1 if out['fail'] else 0)
