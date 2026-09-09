#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download. Continues on this repo's
# PAT-VAL-LEELA validation patient (matching the original's continuation of its own
# PAT-DEMO-SURV survivorship journey), reusing the verified diagnosis/registration already
# established by pc8_leela_survivorship_execute.py -- run that script first.
#
# Field names, reqmaps, task_type strings and response shapes for refer_support_service and
# save_support_record were ported into server.py nearly verbatim from this original, so most
# assertions hold unmodified. One real privacy gap was found and fixed while porting: this
# repo's project_record() (the minimum-necessary field projection applied to every entity a
# role reads) had no rule at all for the 'psychosocial' entity type, so Medical Oncology would
# have seen the full confidential Psycho-Oncology counselling narrative (intervention_plan)
# instead of only the coded risk_level/care_team_summary fields the original test expects to
# be minimum-necessary-visible. Added a psychosocial projection rule to project_record,
# analogous to the existing consent/lab-order/documents projections for other roles, with
# Psycho-Oncology (the owning discipline) and Hospital Management / Admin excluded from the
# restriction. The UI-contract static check targets static/pc8_connected.js (where this
# repo's support-referral/support-record pages actually live) using this repo's own
# data-act names instead of PC8.0's function-naming convention.
import json,urllib.request,urllib.error,urllib.parse,pathlib,sys,os
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parent;BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765');PID='PAT-VAL-LEELA';rows=[];TOK={}
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
def action(role,a,eid='',data=None,expected='auto'):
    payload={'action':a,'patient_id':PID,'entity_id':eid,'data':data or {}}
    if expected=='auto' and eid:
        found=None
        for xs in boot(role).get('entities',{}).values():
            for x in xs:
                if x['id']==eid:found=x;break
            if found:break
        if found:payload['expected_version']=found['version']
    elif expected is not None and expected!='auto':payload['expected_version']=expected
    return http('/api/action','POST',payload,login(role))
def tasks(role,status=None):
    st,j=http('/api/tasks?patient='+PID,token=login(role));assert st==200,(role,st,j)
    xs=j.get('tasks',[])
    return [x for x in xs if not status or x.get('status')==status]
def task(role,task_type=None,source_type=None,source_id=None,status='Open'):
    for x in reversed(tasks(role)):
        if status and x.get('status')!=status:continue
        if task_type and x.get('task_type')!=task_type:continue
        if source_type and x.get('source_type')!=source_type:continue
        if source_id and x.get('source_id')!=source_id:continue
        return x
    return None
def source(role,tid):return http('/api/task-source?task='+urllib.parse.quote(tid),token=login(role))
def check(name,ok,detail=None):
    rows.append({'check':name,'pass':bool(ok),'detail':detail});print(('PASS' if ok else 'FAIL'),name,json.dumps(detail,ensure_ascii=False,default=str)[:1400] if detail is not None else '')
    if not ok:raise AssertionError(name+' '+str(detail))

def refer(target,source_type,source_id,reason,title=''):
    st,j=action('Medical Oncology','refer_support_service','',{'target_role':target,'source_type':source_type,'source_id':source_id,'reason':reason,'title':title or ('Support referral: '+target),'priority':'Routine'})
    check('REF '+target,st==200 and j.get('next_role')==target,j);return j['task_id']

def exact_task_source(role,tid,src_type,src_id,label):
    st,j=source(role,tid);check(label,st==200 and j.get('source_record_id')==src_id and j.get('source_record_type')==src_type and j.get('source_visible_to_role') is True,j);return j

# Use already-verified Leela diagnosis as the clinical source; no state reset or DB manipulation.
dx=entity('Medical Oncology','diagnosis');reg=entity('Medical Oncology','registration')
check('SUP-000 verified diagnosis source exists',dx and dx['status']=='Verified',{'id':dx and dx['id'],'status':dx and dx['status'],'version':dx and dx['version']})

# Nutrition
ntid=refer('Dietitian / Nutrition','diagnosis',dx['id'],'Post-treatment nutrition optimization during survivorship')
exact_task_source('Dietitian / Nutrition',ntid,'diagnosis',dx['id'],'SUP-NUT-001 Dietitian opens exact verified diagnosis')
nut=entity('Dietitian / Nutrition','nutrition')
st,j=action('Palliative Care','save_support_record',nut['id'],{'record_type':'nutrition','sign':True},expected=None);check('SUP-NUT-002 wrong role blocked',st==403,j)
st,j=action('Dietitian / Nutrition','save_support_record',nut['id'],{'record_type':'nutrition','sign':True,'assessment_date':'2026-09-09','weight_kg':62});check('SUP-NUT-003 mandatory fields block',st==409 and bool(j.get('missing')),j)
ndata={'record_type':'nutrition','sign':True,'assessment_date':'2026-09-09','weight_kg':62,'intake_assessment':'Adequate oral intake; mild concern about calcium/protein intake during survivorship.','nutrition_diagnosis':'Nutrition knowledge gap related to survivorship dietary goals.','intervention_plan':'Balanced protein-rich diet; calcium/vitamin-D food counselling; maintain healthy weight.','monitoring_plan':'Reassess weight, intake and treatment-related nutrition symptoms at follow-up.'}
st,j=action('Dietitian / Nutrition','save_support_record',nut['id'],ndata);check('SUP-NUT-004 signed nutrition persisted',st==200 and j.get('status')=='Signed',j);nut1=j['id']
check('SUP-NUT-005 referral task closes',next(x for x in tasks('Dietitian / Nutrition') if x['id']==ntid)['status']=='Completed',next(x for x in tasks('Dietitian / Nutrition') if x['id']==ntid))
nres=task('Medical Oncology','Support result review','nutrition',nut1);check('SUP-NUT-006 MO receives nutrition result',bool(nres),nres)
st,nsrc=source('Medical Oncology',nres['id']);check('SUP-NUT-007 MO opens exact signed nutrition provenance',st==200 and nsrc.get('source_record_id')==nut1 and nsrc.get('source_record_status')=='Signed' and bool(nsrc.get('signed_by')),nsrc)
st,j=action('Dietitian / Nutrition','save_support_record',nut1,{**ndata,'intervention_plan':'Attempt overwrite'});check('SUP-NUT-008 immutable signed overwrite blocked',st==409 and 'immutable' in j.get('error','').lower(),j)
cur=entity('Dietitian / Nutrition','nutrition',nut1);st,j=action('Dietitian / Nutrition','save_support_record',nut1,{**ndata,'amendment_reason':'QA stale update','intervention_plan':'stale'},expected=max(1,cur['version']-1));check('SUP-NUT-009 stale optimistic update blocked',st==409 and 'changed' in j.get('error','').lower(),j)
st,j=action('Dietitian / Nutrition','save_support_record',nut1,{**ndata,'amendment_reason':'Clarify calcium/protein counselling after reconciliation','intervention_plan':'Balanced protein-rich diet with calcium/vitamin-D food counselling and symptom-specific advice.'});check('SUP-NUT-010 amendment creates signed successor',st==200 and j.get('status')=='Signed',j);nut2=j['id']
old=entity('Dietitian / Nutrition','nutrition',nut1);new=entity('Dietitian / Nutrition','nutrition',nut2);check('SUP-NUT-011 old nutrition retained Superseded',old and old['status']=='Superseded' and new and new['status']=='Signed',{'old':old and old['status'],'new':new and new['status']})
oldres=next(x for x in tasks('Medical Oncology') if x['id']==nres['id']);check('SUP-NUT-012 stale MO result task cancelled',oldres['status']=='Cancelled',oldres)
newres=task('Medical Oncology','Support result review','nutrition',nut2);check('SUP-NUT-013 new MO task points to successor',bool(newres),newres)

# Psycho-Oncology restricted record
ptid=refer('Psycho-Oncology','diagnosis',dx['id'],'Survivorship distress and fear-of-recurrence assessment')
exact_task_source('Psycho-Oncology',ptid,'diagnosis',dx['id'],'SUP-PSY-001 Psycho opens exact diagnosis source')
psy=entity('Psycho-Oncology','psychosocial')
pdata={'record_type':'psychosocial','sign':True,'assessment_date':'2026-09-09','distress_score':6,'risk_level':'Moderate','intervention_plan':'CONFIDENTIAL FULL COUNSELLING CONTENT: structured fear-of-recurrence counselling and coping intervention.','care_team_summary':'Moderate distress related to fear of recurrence; no immediate safety risk. Continue psycho-oncology follow-up and reinforce escalation pathways.'}
st,j=action('Psycho-Oncology','save_support_record',psy['id'],pdata);check('SUP-PSY-002 signed restricted psychosocial record',st==200 and j.get('status')=='Signed',j);psyid=j['id']
pres=task('Medical Oncology','Support result review','psychosocial',psyid);check('SUP-PSY-003 MO receives minimum-necessary result task',bool(pres),pres)
st,psrc=source('Medical Oncology',pres['id']);pd=(psrc.get('source_record') or {}).get('data',{});check('SUP-PSY-004 full counselling hidden from MO',st==200 and 'intervention_plan' not in pd and pd.get('care_team_summary') and pd.get('risk_level')=='Moderate',pd)
mo_psy=entity('Medical Oncology','psychosocial',psyid);check('SUP-PSY-005 bootstrap projection also restricted',mo_psy and 'intervention_plan' not in mo_psy.get('data',{}) and mo_psy['data'].get('care_team_summary'),mo_psy and mo_psy['data'])

# Palliative
pal_tid=refer('Palliative Care','diagnosis',dx['id'],'Symptom/supportive-care assessment for persistent survivorship pain concern')
exact_task_source('Palliative Care',pal_tid,'diagnosis',dx['id'],'SUP-PAL-001 Palliative opens exact source')
pal=entity('Palliative Care','palliative');paldata={'record_type':'palliative','sign':True,'assessment_date':'2026-09-09','symptom_summary':'Intermittent focal discomfort, currently controlled; no crisis symptoms.','goals_of_care_status':'Curative/survivorship goals reviewed; symptom control and function prioritized.','plan':'Non-opioid symptom measures, reassess pain trajectory, urgent oncology review for red flags.'}
st,j=action('Palliative Care','save_support_record',pal['id'],paldata);check('SUP-PAL-002 palliative signed',st==200 and j.get('status')=='Signed',j);palid=j['id']
palres=task('Medical Oncology','Support result review','palliative',palid);check('SUP-PAL-003 MO receives palliative result',bool(palres),palres);exact_task_source('Medical Oncology',palres['id'],'palliative',palid,'SUP-PAL-004 MO exact palliative source')

# Clinical Trials
tr_tid=refer('Clinical Trials / Research','diagnosis',dx['id'],'Screen for applicable recurrence/survivorship research options')
exact_task_source('Clinical Trials / Research',tr_tid,'diagnosis',dx['id'],'SUP-TRIAL-001 Trials opens exact source')
tr=entity('Clinical Trials / Research','clinical_trial');trdata={'record_type':'clinical_trial','sign':True,'trial_id':'SYN-TRIAL-BR-001','protocol_version':'Synthetic v1.0','screening_status':'Not currently eligible — surveillance phase','consent_status':'Not Applicable'}
st,j=action('Clinical Trials / Research','save_support_record',tr['id'],trdata);check('SUP-TRIAL-002 screening signed',st==200 and j.get('status')=='Signed',j);trid=j['id']
trres=task('Medical Oncology','Clinical trial review','clinical_trial',trid);check('SUP-TRIAL-003 MO receives trial status',bool(trres),trres);exact_task_source('Medical Oncology',trres['id'],'clinical_trial',trid,'SUP-TRIAL-004 MO exact trial source')

# HIM minimum-necessary projection to treating team
htid=refer('Health Information Management','registration',reg['id'],'Reconcile demographic/source-document metadata for survivorship transition')
exact_task_source('Health Information Management',htid,'registration',reg['id'],'SUP-HIM-001 HIM opens exact registration source')
him=entity('Health Information Management','him');hdata={'record_type':'him','sign':True,'operation_type':'Record reconciliation','reason':'Reconcile survivorship transition metadata with signed source documents.','status':'Completed — metadata reconciled; no clinical content altered'}
st,j=action('Health Information Management','save_support_record',him['id'],hdata);check('SUP-HIM-002 HIM outcome signed',st==200 and j.get('status')=='Signed',j);himid=j['id']
hres=task('Medical Oncology','Support result review','him',himid);check('SUP-HIM-003 MO receives HIM outcome',bool(hres),hres)
st,hsrc=source('Medical Oncology',hres['id']);hd=(hsrc.get('source_record') or {}).get('data',{});check('SUP-HIM-004 MO gets HIM outcome with the fields it needs',st==200 and hsrc.get('source_record_id')==himid and hd.get('status')==hdata['status'] and hd.get('operation_type')==hdata['operation_type'],hd)

# Static UI mapping: support role-owned form + exact task operations in vanilla JS.
js=(ROOT/'static/pc8_connected.js').read_text(encoding='utf-8');needed=['refer_support_service','save_support_record','refer-support-service','support-save','support-sign','Refer to Support Service','Open Source Record','Perform My Action'];check('SUP-UI-001 vanilla-JS support task/action mapping present',all(x in js for x in needed),[x for x in needed if x not in js])

# Named audit attribution for support signs/supersede/task cancellation.
aud=boot('Medical Oncology').get('audit',[]);acts={x.get('action') for x in aud};wanted={'SUPPORT_SIGN','SUPPORT_SUPERSEDE','TASK_AUTO_CANCEL'};check('SUP-AUD-001 support audit events visible',wanted.issubset(acts),sorted(wanted & acts))

out={'patient_id':PID,'patient':'Leela Nair','build':'12.2-PC7.1-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(1 for x in rows if x['pass']),'fail':sum(1 for x in rows if not x['pass']),'results':rows}
(ROOT/'validation_evidence'/'PC8_SUPPORT_DISCIPLINES_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail']},ensure_ascii=False))
sys.exit(1 if out['fail'] else 0)
