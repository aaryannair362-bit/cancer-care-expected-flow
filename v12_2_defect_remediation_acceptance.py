#!/usr/bin/env python3
import json, os, urllib.request, urllib.error, urllib.parse, base64, sys
from datetime import date, datetime, timedelta

BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9077')
PIN=os.environ.get('CCA_DEMO_PIN','2026')
PID='PAT-0001'
TOK={}; RESULTS=[]
OPT={'save_intake':'intake','med_recon':'med_recon','save_dynamic_form':'dynamic_forms','save_consultation':'consultation','save_diagnosis':'diagnosis','save_appointment':'appointments','queue_patient':'queue','save_care_plan':'care_plan','save_treatment_plan':'treatment_plan','save_radiology':'radiology','save_pathology':'pathology','mdt_comment':'mdt_collab','mdt_attendance':'mdt_collab','mdt_recommend':'mdt'}

def http(path,method='GET',data=None,token=None):
    h={'Content-Type':'application/json'}
    if token: h['Authorization']='Bearer '+token
    body=json.dumps(data).encode() if data is not None else None
    req=urllib.request.Request(BASE+path,data=body,headers=h,method=method)
    try:
        with urllib.request.urlopen(req,timeout=10) as r:
            raw=r.read(); return r.status, json.loads(raw.decode()) if raw else {}, dict(r.headers)
    except urllib.error.HTTPError as e:
        raw=e.read()
        try:j=json.loads(raw.decode()) if raw else {}
        except:j={'raw':raw.decode(errors='replace')}
        return e.code,j,dict(e.headers)
    except Exception as e:
        return 599,{'error':repr(e)},{}

def login(role,force=False):
    if role in TOK and not force:return TOK[role]
    st,j,_=http('/api/login','POST',{'role':role,'pin':PIN})
    if st!=200: raise RuntimeError((role,st,j))
    TOK[role]=j['token']; return TOK[role]

def boot(role,pid=PID): return http('/api/bootstrap?patient='+urllib.parse.quote(pid),token=login(role))[:2]
def entities(role,typ,pid=PID):
    st,b=boot(role,pid); return b.get('entities',{}).get(typ,[]) if st==200 else []
def latest(role,typ,pid=PID):
    xs=entities(role,typ,pid); return xs[-1] if xs else None

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

def action(role,a,eid='',d=None,pid=PID,expected='AUTO'):
    payload={'action':a,'patient_id':pid,'entity_id':eid,'data':pc13_adapt(a,d)}
    if a in OPT and expected=='AUTO':
        xs=entities(role,OPT[a],pid)
        target=next((r for r in xs if eid and r.get('id')==eid), xs[-1] if xs else None)
        if target: payload['expected_version']=target['version']
    elif expected not in ['AUTO',None]: payload['expected_version']=expected
    return http('/api/action','POST',payload,login(role))[:2]

def check(id,cond,evidence,notes=''):
    RESULTS.append({'id':id,'pass':bool(cond),'evidence':evidence,'notes':notes})
    print(('PASS' if cond else 'FAIL'),id,json.dumps(evidence,ensure_ascii=False)[:500])

def create_patient(tag='QA',specialty='Medical Oncology'):
    st,j,_=http('/api/patient','POST',{'name':f'{tag} Synthetic Patient','dob':'1988-04-12','sex':'Female','phone':'+91'+str(abs(hash(tag))%10**10).zfill(10),'id_number':'QA-'+tag+'-'+str(abs(hash(tag))%999999),'initial_specialty':specialty,'duplicate_override_reason':'Synthetic isolated QA patient'},login('Front Desk'))
    if st!=200: raise RuntimeError(('create_patient',tag,st,j))
    return j['id']

def full_lab_payload(anc=3.5,anc_unit='×10^9/L'):
    return {'date':str(date.today()),'hb':12.2,'wbc':6.0,'anc':anc,'platelets':250,'creatinine':0.8,'egfr':90,'bilirubin':0.8,'ast':20,'alt':20,'albumin':4.0,'sodium':139,'potassium':4.0,'magnesium':2.0,'calcium':9.0,'lvef':60,'pregnancy':'Negative','units':{'hb':'g/dL','wbc':'×10^9/L','anc':anc_unit,'platelets':'×10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m²','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalize':True}

# Login core roles
for r in ['Front Desk','Nurse Navigator','Medical Oncology','Radiologist','Pathology','MDT Coordinator','Hospital Management / Admin','Biller','Laboratory / Phlebotomy','Patient Liaison','Radiology Coordinator','Oncology Pharmacy','Inpatient Oncology Nurse']:
    login(r)

# CAP-002 tasks endpoint now exists.
st,j,_=http('/api/tasks?patient='+PID,token=login('Medical Oncology'));check('CAP-002',st==200 and 'tasks' in j,{'status':st,'keys':list(j.keys())})

# CON-001 stale write rejected deterministically on a mutable draft record.
p_con=create_patient('CONCURRENCY')
co=latest('Medical Oncology','consultation',p_con);v=co['version'];eid=co['id']
st1,j1=action('Medical Oncology','save_consultation',eid,{'assessment':'Concurrent editor A'},pid=p_con,expected=v)
st2,j2=action('Medical Oncology','save_consultation',eid,{'assessment':'Concurrent editor B stale'},pid=p_con,expected=v)
check('CON-001',st1==200 and st2==409 and 'changed' in j2.get('error','').lower(),{'first':st1,'second':st2,'second_body':j2})

# DATA-001 future DOB rejected.
st,j,_=http('/api/patient','POST',{'name':'Future DOB QA','dob':'2099-01-01','phone':'+919999000001','id_number':'QA-FUTURE-DOB'},login('Front Desk'))
check('DATA-001',st==409,{'status':st,'body':j})

# DATA-NTNM-001 non-TNM disease verifies without fake TNM.
p_ntnm=create_patient('NTNM')
dx=latest('Medical Oncology','diagnosis',p_ntnm)
payload={'icd10':'C92.0','icd10_version':'ICD-10','cancer_type':'Acute Myeloid Leukemia','primary_site':'Bone marrow / blood','histology':'Acute myeloid leukemia','staging_system':'ELN','staging_version':'Synthetic QA classification v1','staging_date':str(date.today()),'staging_basis':'Clinical','classification_system':'ELN','classification_value':'Adverse-risk synthetic QA classification','treatment_intent':'Curative','verify':True}
st,j=action('Medical Oncology','save_diagnosis',dx['id'],payload,pid=p_ntnm)
check('DATA-NTNM-001',st==200 and j.get('status')=='Verified',{'status':st,'body':j})

# Nurse input failures are 4xx and do not crash; ranges enforced.
intake=latest('Nurse Navigator','intake');base={**intake['data'],'complete':True}
for did,field,val in [('DATA-NUR007','spo2',150),('REL-NUR-001','weight_kg',-5),('REL-NUR-002','height_cm',0),('DATA-NUR008','ecog','9')]:
    d={**base,field:val}; st,j=action('Nurse Navigator','save_intake',intake['id'],d);check(did,st in [409,422],{'status':st,'body':j})

# SEC-001 server-side logout revokes bearer token.
tok=login('Radiologist',force=True);st1,j1,_=http('/api/logout','POST',{},tok);st2,j2,_=http('/api/bootstrap?patient='+PID,token=tok);check('SEC-001',st1==200 and st2==401,{'logout':st1,'after_logout':st2,'body':j2}); login('Radiologist',force=True)

# SEC-HTML-001 active HTML rejected even as declared HTML.
content=base64.b64encode(b'<html><script>alert(1)</script></html>').decode();st,j,_=http('/api/document','POST',{'patient_id':PID,'filename':'qa.html','mime':'text/html','content_base64':content},login('Nurse Navigator'));check('SEC-HTML-001',st==415,{'status':st,'body':j})

# VER-001 / VER-002 final reports cannot be silently overwritten.
rad=latest('Radiologist','radiology');st,j=action('Radiologist','save_radiology',rad['id'],{'findings':'MUTATION ATTEMPT','impression':'Should block','finalize':True});check('VER-001',st==409 and 'immutable' in j.get('error','').lower(),{'status':st,'body':j})
path=latest('Pathology','pathology');st,j=action('Pathology','save_pathology',path['id'],{'histology':'MUTATION ATTEMPT','finalize':True});check('VER-002',st==409 and 'immutable' in j.get('error','').lower(),{'status':st,'body':j})

# VER-003 active content immutable.
st,j=action('Hospital Management / Admin','content_update','REG-CCA-TCHP-DEMO',{'template_id':'REG-CCA-TCHP-DEMO','name':'MUTATED ACTIVE DEMO NAME'});check('VER-003',st==409 and 'immutable' in j.get('error','').lower(),{'status':st,'body':j})

# WF-001 arbitrary queue destination rejected.
q=latest('Front Desk','queue');st,j=action('Front Desk','queue_patient',q['id'],{'to':'Mars Oncology Deck'});check('WF-001',st==409,{'status':st,'body':j})

# DATA-002 past appointment rejected; WF-002 No-show supported and creates a follow-up task.
ap=latest('Front Desk','appointments');st,j=action('Front Desk','save_appointment',ap['id'],{'operation':'create','date':'1900-01-01','department':'Medical Oncology','location':'Medical Oncology'});check('DATA-002',st==409,{'status':st,'body':j})
st,j=action('Front Desk','save_appointment',ap['id'],{'operation':'create','date':str(date.today()+timedelta(days=3)),'department':'Medical Oncology','location':'Medical Oncology','purpose':'QA no-show'});newapt=j.get('items',[])[-1] if st==200 else {};st2,j2=action('Front Desk','save_appointment',ap['id'],{'operation':'no_show','id':newapt.get('id'),'reason':'Synthetic QA no-show'})
st3,tasks,_=http('/api/tasks?patient='+PID,token=login('Patient Liaison'));has_task=any(t.get('source_id')==newapt.get('id') and t.get('task_type')=='No-show follow-up' for t in tasks.get('tasks',[])) if st3==200 else False
check('WF-002',st==200 and st2==200 and has_task,{'create':st,'no_show':st2,'task_found':has_task})

# DATA-003 / DATA-004 governed medication/allergy value sets.
med=latest('Nurse Navigator','med_recon');st,j=action('Nurse Navigator','med_recon',med['id'],{'operation':'add_medication','name':'QA Drug','route':'TELEPORT'});check('DATA-003',st==409,{'status':st,'body':j})
st,j=action('Nurse Navigator','med_recon',med['id'],{'operation':'add_allergy','substance':'QA Allergen','reaction':'Rash','severity':'EXTREMEPLUS'});check('DATA-004',st==409,{'status':st,'body':j})

# DATA-005 future staging date rejected.
dx=latest('Medical Oncology','diagnosis');d={**dx['data'],'staging_date':'2099-01-01','verify':True};st,j=action('Medical Oncology','save_diagnosis',dx['id'],d);check('DATA-005',st==409,{'status':st,'body':j})

# DATA-006 care-plan status uses exact governed state machine.
cp=latest('Nurse Navigator','care_plan');st,j=action('Nurse Navigator','save_care_plan',cp['id'],{'status':'ACTIVE'});check('DATA-006',st==409,{'status':st,'body':j})

# REL-001 duplicate payment replay is idempotent; conflicting replay is rejected.
receipt='IDEMP-QA-'+datetime.now().strftime('%H%M%S%f');st,j=action('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','name':'CBC','indication':'QA payment idempotency','date':str(date.today()),'decision_reason':'Synthetic acceptance-test investigation decision'});loid=j.get('id');st1,j1=action('Biller','record_payment',loid,{'payment_status':'Paid','amount':700,'receipt_no':receipt});st2,j2=action('Biller','record_payment',loid,{'payment_status':'Paid','amount':700,'receipt_no':receipt});st3,j3=action('Biller','record_payment',loid,{'payment_status':'Paid','amount':701,'receipt_no':receipt});check('REL-001',st1==200 and st2==200 and j2.get('idempotent') is True and st3==409,{'first':st1,'second':st2,'idempotent':j2.get('idempotent'),'conflict':st3,'receipt':receipt})

# WF-003 rejected specimen -> recollection task -> recollection.
st,j=action('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','name':'CBC','indication':'QA specimen rejection','date':str(date.today()),'decision_reason':'Synthetic acceptance-test investigation decision'});rejorder=j.get('id');action('Biller','record_payment',rejorder,{'payment_status':'Waived','amount':0,'reason':'Synthetic QA'});stc,jc=action('Laboratory / Phlebotomy','collect_sample',rejorder,{'sample_id':'SMP-QA-REJ'});strj,jrj=action('Laboratory / Phlebotomy','reject_sample',rejorder,{'reason':'Clotted synthetic specimen'});strc,jrc=action('Laboratory / Phlebotomy','recollect_sample',rejorder,{'sample_id':'SMP-QA-RECOLLECT'});check('WF-003',stc==200 and strj==200 and jrj.get('task_id') and strc==200,{'collect':stc,'reject':strj,'task_id':jrj.get('task_id'),'recollect':strc})

# Lab plausibility boundary: impossible ANC values blocked; realistic and alternate-unit values accepted.
lab=latest('Laboratory / Phlebotomy','lab')
# latest lab may be recollection draft: use it directly for finalization tests.
for tid,val,unit,should in [('LAB-PLAUS-999999',999999,'×10^9/L',False),('LAB-PLAUS-350',350,'×10^9/L',False),('LAB-PLAUS-3.5',3.5,'×10^9/L',True)]:
    st,j=action('Laboratory / Phlebotomy','save_lab',lab['id'],full_lab_payload(val,unit));check(tid,(st==200)==should,{'status':st,'body':j})
    if st==200: lab=latest('Laboratory / Phlebotomy','lab')
# Alternate unit on the now-final record requires a reason and creates a linked amendment.
p=full_lab_payload(800,'cells/µL');p['amendment_reason']='QA alternate ANC unit normalization';st,j=action('Laboratory / Phlebotomy','save_lab',lab['id'],p);check('LAB-PLAUS-800-CELLS',st==200,{'status':st,'body':j})

# WF-004 critical result creates Medical Oncology task and task can be acknowledged.
lab=latest('Laboratory / Phlebotomy','lab');p=full_lab_payload(0.2,'×10^9/L');p['amendment_reason']='QA critical ANC routing';st,j=action('Laboratory / Phlebotomy','save_lab',lab['id'],p);task_ids=j.get('critical_tasks',[]) if st==200 else []
stt,tj,_=http('/api/tasks?patient='+PID,token=login('Medical Oncology'));crit=next((x for x in tj.get('tasks',[]) if x.get('id') in task_ids),None);sta,aj,_=(http('/api/task-action','POST',{'task_id':crit['id'],'operation':'acknowledge'},login('Medical Oncology')) if crit else (0,{},{}));check('WF-004',st==200 and bool(task_ids) and crit is not None and sta==200 and aj.get('task',{}).get('status')=='Acknowledged',{'lab':st,'task_ids':task_ids,'task_status':aj.get('task',{}).get('status')})

# WF-005 finalized MDT comments require explicit addendum semantics.
coll=latest('Medical Oncology','mdt_collab');st1,j1=action('Medical Oncology','mdt_comment',coll['id'],{'comment':'Late unqualified QA comment'});st2,j2=action('Medical Oncology','mdt_comment',coll['id'],{'comment':'Late qualified QA addendum','mode':'addendum','addendum_reason':'Synthetic QA late comment'});check('WF-005',st1==409 and st2==200 and j2.get('comment',{}).get('entry_type')=='Finalized MDT Addendum',{'without_addendum':st1,'with_addendum':st2})

# CAP-001 AI patient-record search exists and is grounded.
st,j,_=http('/api/ai-search?patient='+PID+'&q='+urllib.parse.quote('latest ANC'),token=login('Medical Oncology'));check('CAP-001',st==200 and j.get('grounded') is True and 'answer' in j,{'status':st,'grounded':j.get('grounded'),'sources':len(j.get('sources',[]))})

# UX-001 server-side content search honours q.
st,j,_=http('/api/content?q=ZZZNOEXACTMATCHZZZ',token=login('Hospital Management / Admin'));check('UX-001',st==200 and len(j.get('templates',[]))==0,{'status':st,'returned_count':len(j.get('templates',[]))})

# SEC-002 new patient is not visible to an unassigned Radiologist even with guessed ID.
p_scope=create_patient('SCOPE');st,j=boot('Radiologist',p_scope);check('SEC-002',st==403,{'status':st,'body':j})

# RPT-004 historical source version selector changes derived report content.
p_rpt=create_patient('REPORT')
co=latest('Medical Oncology','consultation',p_rpt)
basec={'encounter_type':'New consultation','date':str(date.today()),'chief_complaint':'QA','hpi':'QA','ros':'QA','physical_exam_structured':{'general':'QA','cardiovascular':'QA','respiratory':'QA','abdomen':'QA','neurologic':'QA','tumor_site':'QA'},'assessment':'REPORT VERSION ONE','plan':'QA'}
st,j=action('Medical Oncology','save_consultation',co['id'],basec,pid=p_rpt);v1=latest('Medical Oncology','consultation',p_rpt)['version']
basec2={**basec,'assessment':'REPORT VERSION TWO'};st2,j2=action('Medical Oncology','save_consultation',co['id'],basec2,pid=p_rpt)
stc,cur,_=http('/api/report/render?template=RPT-ONC-CONSULT&patient='+p_rpt,token=login('Medical Oncology'));sth,hist,_=http('/api/report/render?template=RPT-ONC-CONSULT&patient='+p_rpt+'&record_version='+str(v1),token=login('Medical Oncology'))
def assess(report):
    try:return report['sections'][0]['data'].get('assessment')
    except:return None
check('RPT-004',stc==200 and sth==200 and assess(cur)=='REPORT VERSION TWO' and assess(hist)=='REPORT VERSION ONE',{'current':assess(cur),'historical':assess(hist),'requested_version':v1})

# WF-007 explicit non-death episode close/reopen exists and requires reason.
p_ep=create_patient('EPISODE');ep=latest('Medical Oncology','cancer_episode',p_ep);st1,j1=action('Medical Oncology','close_cancer_episode',ep['id'],{'episode_id':ep['id'],'reason':'Synthetic QA surveillance completion'},pid=p_ep);st2,j2=action('Medical Oncology','reopen_cancer_episode',ep['id'],{'episode_id':ep['id'],'reason':'Synthetic QA recurrence'},pid=p_ep);check('WF-007',st1==200 and st2==200 and j2.get('reopens')==ep['id'],{'close':st1,'reopen':st2,'body':j2})

# WF-008 death closes future appointments + continuous therapy.
p_death=create_patient('DEATH');cont=latest('Medical Oncology','continuous_therapy',p_death);stc,jc=action('Medical Oncology','create_continuous_therapy',cont['id'],{'therapy':'Synthetic continuous therapy','mode':'Oral systemic therapy','drug':'Synthetic agent','route':'PO','schedule':'Daily','start_date':str(date.today())},pid=p_death)
ap=latest('Front Desk','appointments',p_death);sta,ja=action('Front Desk','save_appointment',ap['id'],{'operation':'create','date':str(date.today()+timedelta(days=10)),'department':'Medical Oncology','location':'Medical Oncology','purpose':'Future QA'},pid=p_death)
std,jd=action('Medical Oncology','record_death','',{'date':str(date.today()),'reason':'Synthetic QA death closure'},pid=p_death);bst,bb=boot('Medical Oncology',p_death);courses=bb.get('entities',{}).get('continuous_therapy',[])[-1]['data'].get('courses',[]) if bst==200 else [];appts=bb.get('entities',{}).get('appointments',[])
# Medical Oncology does not read appointments; inspect as Front Desk.
_,bf=boot('Front Desk',p_death);apitems=bf.get('entities',{}).get('appointments',[])[-1]['data'].get('items',[])
check('WF-008',stc==200 and sta==200 and std==200 and courses and all(x.get('status')!='Active' for x in courses) and all(x.get('status')=='Cancelled' for x in apitems if x.get('date', '')>=str(date.today())),{'death':std,'course_statuses':[x.get('status') for x in courses],'appointment_statuses':[x.get('status') for x in apitems]})

# WF-ORDER-PLAN-001 Draft Treatment Plan cannot instantiate an executable Treatment Order.
approved_plan=next((x for x in reversed(entities('Medical Oncology','treatment_plan',PID)) if x.get('status') in ['Clinician Approved','Active']),None)
stp,jtp=action('Medical Oncology','create_plan_from_mdt','',{'specialty':'Medical Oncology'},pid=PID)
draft_plan_id=jtp.get('id') if stp==200 else ''
stbad,jbad=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':draft_plan_id,'administration_setting':'Day Care','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'Synthetic QA','cycle':97,'day':1,'start_date':str(date.today()),'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic clinician-entered AUC dose'}},pid=PID)
check('WF-ORDER-PLAN-001',stp==200 and stbad==409 and 'unsigned or inactive Treatment Plan' in jbad.get('error',''),{'draft_plan_create':stp,'draft_plan_id':draft_plan_id,'order_attempt':stbad,'body':jbad,'approved_plan_id':approved_plan.get('id') if approved_plan else None})

# WF-006 discharge is blocked while an inpatient treatment order is unresolved.
# Use seeded patient whose signed readiness/order content are already valid. Admit, create new inpatient order, try discharge.
stad,jad=action('Medical Oncology','admit_patient','',{'admission_type':'Planned','reason_code':'Treatment / procedure','ward':'Oncology Ward','bed':'QA-IPD-1','source_context':'Synthetic QA'},pid=PID);adm_id=jad.get('admission',{}).get('id') or jad.get('admission_id','');admit_ok=(stad==200 or (stad==409 and bool(adm_id)))
stord,jord=action('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':approved_plan.get('id') if approved_plan else '','administration_setting':'Inpatient','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'Synthetic QA','cycle':2,'day':1,'start_date':str(date.today()),'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic clinician-entered AUC dose'}},pid=PID)
stdc,jdc=action('Medical Oncology','discharge_patient','',{'admission_id':adm_id,'discharge_diagnosis':'QA','hospital_course':'QA','medications':'QA','follow_up':'QA','next_care_stage':'Medical Oncology'},pid=PID)
check('WF-006',admit_ok and stord==200 and stdc==409 and jdc.get('unresolved_orders'),{'admit':stad,'admission_id':adm_id,'order':stord,'discharge':stdc,'body':jdc})


# WF-ROUTE-001 queue routing grants the destination specialty case-scoped access (regression for string-iteration bug).
p_route=create_patient('ROUTE');q_route=latest('Front Desk','queue',p_route);stq,jq=action('Front Desk','queue_patient',q_route['id'],{'to':'Radiation Oncology','status':'Queued','priority':'Routine'},pid=p_route);strad,jrad=boot('Radiation Oncology',p_route);check('WF-ROUTE-001',stq==200 and strad==200,{'queue':stq,'destination_bootstrap':strad,'body':jrad if strad!=200 else {'patient':jrad.get('patient',{}).get('id')}})

# Final dedicated headline for newly reported plausibility defect.
new_checks={x['id']:x['pass'] for x in RESULTS if x['id'].startswith('LAB-PLAUS-')}
check('LAB-PLAUS-001',all(new_checks.values()),new_checks,'Plausibility regression aggregate for ANC 999999/350/3.5/800 cells per µL')

# Write evidence.
summary={'build':'CCA Cancer Care HIS + Oncology EMR V12.2 Final Defect Remediation','run_at':datetime.now().astimezone().isoformat(),'base':BASE,'pass':sum(x['pass'] for x in RESULTS),'fail':sum(not x['pass'] for x in RESULTS),'results':RESULTS}
out=os.environ.get('CCA_OUT','V12_2_DEFECT_REMEDIATION_RUN.json');open(out,'w').write(json.dumps(summary,indent=2,ensure_ascii=False))
print(f"RESULT {summary['pass']} PASS {summary['fail']} FAIL")
if summary['fail']:
    print('FAILED',[x['id'] for x in RESULTS if not x['pass']]);sys.exit(1)
