#!/usr/bin/env python3
import json, os, urllib.request, urllib.error, urllib.parse
from datetime import date
from pathlib import Path
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9104'); PIN=os.environ.get('CCA_DEMO_PIN','2026'); PID='PAT-0001'; T={}; OUT=[]
ROOT=Path(__file__).resolve().parent

def http(path,method='GET',data=None,token=None):
    h={'Content-Type':'application/json'}
    if token:h['Authorization']='Bearer '+token
    body=json.dumps(data).encode() if data is not None else None
    req=urllib.request.Request(BASE+path,data=body,headers=h,method=method)
    try:
        with urllib.request.urlopen(req,timeout=10) as r:
            raw=r.read();return r.status,json.loads(raw.decode()) if raw else {}
    except urllib.error.HTTPError as e:
        raw=e.read()
        try:j=json.loads(raw.decode()) if raw else {}
        except:j={'raw':raw.decode(errors='replace')}
        return e.code,j

def login(role):
    if role in T:return T[role]
    st,j=http('/api/login','POST',{'role':role,'pin':PIN})
    if st!=200:raise RuntimeError((role,st,j))
    T[role]=j['token'];return T[role]

def boot(role):return http('/api/bootstrap?patient='+urllib.parse.quote(PID),token=login(role))
def listt(role,t):
    st,b=boot(role);return b.get('entities',{}).get(t,[]) if st==200 else []
def latest(role,t):
    xs=listt(role,t);return xs[-1] if xs else None

def act(role,a,eid='',d=None):
    payload={'action':a,'patient_id':PID,'entity_id':eid,'data':d or {}}
    if a in ['save_intake','med_recon']:
        typ={'save_intake':'intake','med_recon':'med_recon'}[a];xs=listt(role,typ);target=next((x for x in xs if x['id']==eid),xs[-1] if xs else None)
        if target:payload['expected_version']=target['version']
    return http('/api/action','POST',payload,login(role))

def chk(i,cond,ev):
    OUT.append({'id':i,'pass':bool(cond),'evidence':ev});print(('PASS' if cond else 'FAIL'),i,json.dumps(ev,ensure_ascii=False)[:700])

for r in ['Nurse Navigator','Medical Oncology','Oncology Pharmacy','Day Care / Infusion Nurse','Radiation Oncology','Radiation Physicist','Radiation Technologist']:login(r)

# 1) Fall risk score must be tied to an explicit governed scale and level is derived.
intake=latest('Nurse Navigator','intake')
base={'sbp':120,'dbp':80,'hr':80,'rr':16,'temp':36.8,'spo2':99,'weight':70,'height':170,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%','weight':'kg','height':'cm'},'ecog':'1','kps':'90','pain_instrument':'Numeric Rating Scale 0–10','pain_score':2,'pain_site':'Synthetic','fall_risk_setting':'OPD','fall_risk_score':4,'fall_risk_level':'Low','complete':True}
st,j=act('Nurse Navigator','save_intake',intake['id'],base);chk('INT-FALL-001',st==409 and 'scale' in j.get('error','').lower(),{'status':st,'body':j})
base['fall_risk_scale']='CCA Demo Fall-Risk Scale — Synthetic QA'
st,j=act('Nurse Navigator','save_intake',intake['id'],base);chk('INT-FALL-002',st==200,{'status':st,'body':j})
st,b=boot('Medical Oncology');idata=b['entities']['intake'][-1]['data'];chk('INT-FALL-003',idata.get('fall_risk_level')=='Moderate' and idata.get('fall_risk_level')!='Low' and idata.get('fall_risk_scale')==base['fall_risk_scale'],{'stored_scale':idata.get('fall_risk_scale'),'stored_score':idata.get('fall_risk_score'),'derived_level':idata.get('fall_risk_level')})

# 2) Allergy structure + medication reconciliation status are governed and attested.
med=latest('Nurse Navigator','med_recon')
st,j=act('Nurse Navigator','med_recon',med['id'],{'operation':'add_allergy','substance':'Carboplatin','reaction':'Rash','severity':'Moderate','source':'Patient'});chk('MED-ALG-001',st==409 and 'governed allergen' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Nurse Navigator','med_recon',med['id'],{'operation':'add_allergy','code':'ALG-CARBO','reaction':'Unstructured reaction text','severity':'Moderate','source':'Patient'});chk('MED-ALG-002',st==409 and 'reaction' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Nurse Navigator','med_recon',med['id'],{'operation':'add_allergy','code':'ALG-CARBO','reaction':'Urticaria','severity':'Moderate','source':'Patient','status':'Active'});chk('MED-ALG-003',st==200 and j.get('allergy_status')=='Allergy present',{'status':st,'body':j})
med=latest('Nurse Navigator','med_recon')
st,j=act('Nurse Navigator','med_recon',med['id'],{'operation':'reconcile','source':'Patient'});chk('MED-REC-004',st==409 and 'status' in j.get('error','').lower(),{'status':st,'body':j})
med=latest('Nurse Navigator','med_recon')
st,j=act('Nurse Navigator','med_recon',med['id'],{'operation':'reconcile','reconciliation_status':'Incomplete','source':'Patient'});chk('MED-REC-005',st==409 and 'reason' in j.get('error','').lower(),{'status':st,'body':j})
med=latest('Nurse Navigator','med_recon')
st,j=act('Nurse Navigator','med_recon',med['id'],{'operation':'reconcile','reconciliation_status':'Complete','source':'Patient','reason':'Synthetic full review'});chk('MED-REC-006',st==200 and j.get('reconciliation_status')=='Complete',{'status':st,'body':j})
m=latest('Medical Oncology','med_recon')['data'];ev=(m.get('reconciliation_events') or [])[-1];chk('MED-REC-007',ev.get('reconciliation_status')=='Complete' and isinstance(ev.get('reconciled_by'),dict) and bool(ev.get('at')) and bool(ev.get('attestation')),{'event':ev})

# 3) Every final ordered dose is an explicit clinician decision with reason + signature context.
plan=latest('Medical Oncology','treatment_plan')
base_order={'template_id':'REG-CCA-TCHP-DEMO','administration_decision_reason':'Synthetic clinician acceptance of regimen administration parameters after review','schedule_decision_reason':'Synthetic clinician acceptance of treatment administration date/time after review','plan_id':plan['id'],'administration_setting':'Day Care','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'Synthetic QA','cycle':2,'day':1,'start_date':str(date.today()),'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic clinician-entered AUC product-test dose'}}
st,j=act('Medical Oncology','create_order','',base_order);chk('ORD-DEC-001',st==409 and 'decision reason' in j.get('error','').lower(),{'status':st,'body':j})
base_order['dose_decision_reasons']={'*':'Accept calculated/protocol dose after review','DEMO-CARBO':'Patient-specific dose per protocol method'}
st,j=act('Medical Oncology','create_order','',base_order);chk('ORD-DEC-002',st==200,{'status':st,'body':j});oid=j.get('order_id');phid=j.get('pharmacy_id');infid=j.get('infusion_id')
o=next(x for x in listt('Medical Oncology','treatment_order') if x['id']==oid);chk('ORD-DEC-003',all(bool(x.get('dose_decision_reason')) and bool(x.get('dose_decided_by')) and bool(x.get('dose_decided_at')) for x in o['data']['items']) and bool(o['data'].get('signed_at')),{'order':o['id'],'signed_at':o['data'].get('signed_at'),'reasons':[(x['drug'],x.get('dose_decision_reason'),x.get('dose_decided_by',{}).get('role')) for x in o['data']['items']]})

# 4) Duplicate current order blocked; explicit supersession preserves old order and blocks stale downstream action.
st,j=act('Medical Oncology','create_order','',base_order);chk('ORD-STALE-001',st==409 and 'active Treatment Order' in j.get('error',''),{'status':st,'body':j})
replacement={**base_order,'supersedes_order_id':oid,'supersession_reason':'Synthetic correction before Pharmacy verification'}
st,j=act('Medical Oncology','create_order','',replacement);chk('ORD-STALE-002',st==200 and j.get('supersedes_order_id')==oid,{'status':st,'body':j});new_oid=j.get('order_id');new_phid=j.get('pharmacy_id');new_infid=j.get('infusion_id')
old_o=next(x for x in listt('Medical Oncology','treatment_order') if x['id']==oid);old_ph=next(x for x in listt('Oncology Pharmacy','pharmacy') if x['id']==phid);old_inf=next(x for x in listt('Day Care / Infusion Nurse','infusion') if x['id']==infid);chk('ORD-STALE-003',old_o['status']=='Superseded' and old_ph['status']=='Superseded' and old_inf['status']=='Superseded' and old_o['data'].get('superseded_by_order_id')==new_oid,{'order_status':old_o['status'],'pharmacy_status':old_ph['status'],'infusion_status':old_inf['status'],'superseded_by':old_o['data'].get('superseded_by_order_id')})
checks={k:True for k in ['patient_identity','allergy','regimen_version','cycle_day','dose_basis','calculated_dose','ordered_dose','dose_variance','renal_adjustment','hepatic_adjustment','cumulative_dose','interaction','duplication','route','diluent','final_concentration','stock','expiry']}
st,j=act('Oncology Pharmacy','pharmacy_decision',phid,{'decision':'Verified','verification_checks':checks});chk('ORD-STALE-004',st==409 and ('stale' in j.get('error','').lower() or 'superseded' in j.get('error','').lower()),{'status':st,'body':j})
st,j=act('Oncology Pharmacy','pharmacy_decision',new_phid,{'decision':'Verified','verification_checks':checks});chk('ORD-STALE-005',st==200,{'status':st,'body':j})

# 5) RT approvals are bound to explicit prescription/plan versions, and replan invalidates old approvals.
rt=latest('Radiation Oncology','radiation');rx=dict(rt['data'].get('prescription',{}));rx['sign']=True
st,j=act('Radiation Oncology','rt_save_prescription',rt['id'],rx);chk('RT-VERSION-001',st==200,{'status':st,'body':j})
rt=latest('Radiation Oncology','radiation');pl=rt['data']['planning'];planv=pl.get('plan_version',1);rxv=rt['data']['prescription'].get('prescription_version',1)
st,j=act('Radiation Physicist','rt_planning_status',rt['id'],{'plan_version':planv,'physics_qa':'Approved','physics_qa_note':'Too early'});chk('RT-VERSION-002',st==409 and 'before Physics QA' in j.get('error',''),{'status':st,'body':j})
st,j=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':planv,'simulation_status':'Completed','contouring_status':'Completed','planning_status':'Planning Complete','plan_note':'Synthetic plan ready','status':'Planning'});chk('RT-VERSION-003',st==200 and j.get('plan_version')==planv,{'status':st,'body':j})
st,j=act('Radiation Physicist','rt_planning_status',rt['id'],{'physics_qa':'Approved','physics_qa_note':'Missing version'});chk('RT-VERSION-004',st==409 and 'plan_version' in j.get('error',''),{'status':st,'body':j})
st,j=act('Radiation Physicist','rt_planning_status',rt['id'],{'plan_version':planv,'physics_qa':'Approved','physics_qa_note':'Physics QA for current plan'});chk('RT-VERSION-005',st==200,{'status':st,'body':j})
st,j=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':planv+99,'physician_final_approval':'Approved','status':'Ready for Treatment'});chk('RT-VERSION-006',st==409 and 'version changed' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':planv,'physician_final_approval':'Approved','status':'Ready for Treatment'});chk('RT-VERSION-007',st==200 and j.get('status')=='Ready for Treatment',{'status':st,'body':j})
st,j=act('Radiation Technologist','rt_deliver_fraction',rt['id'],{'fraction_number':1,'status':'Delivered','date_time':'2026-09-04T10:00:00+05:30','delivered_dose_gy':rx.get('dose_per_fraction_gy'),'verified_by':'RT Tech B','image_guidance_performed':True});chk('RT-VERSION-008',st==200 and j.get('plan_version')==planv and j.get('prescription_version')==rxv,{'status':st,'body':j})
# material plan note change after approvals creates v2 and resets approval state
st,j=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':planv,'plan_note':'Synthetic adaptive/replan revision','planning_status':'Planning Complete','status':'Planning'});chk('RT-VERSION-009',st==200 and j.get('approvals_reset') and j.get('plan_version')==planv+1,{'status':st,'body':j});planv2=planv+1
st,j=act('Radiation Technologist','rt_deliver_fraction',rt['id'],{'fraction_number':2,'status':'Delivered','date_time':'2026-09-05T10:00:00+05:30','delivered_dose_gy':rx.get('dose_per_fraction_gy'),'verified_by':'RT Tech B','image_guidance_performed':True});chk('RT-VERSION-010',st==409 and 'current RT plan' in j.get('error',''),{'status':st,'body':j})
st,j=act('Radiation Physicist','rt_planning_status',rt['id'],{'plan_version':planv,'physics_qa':'Approved','physics_qa_note':'stale plan attempt'});chk('RT-VERSION-011',st==409 and 'version changed' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Radiation Physicist','rt_planning_status',rt['id'],{'plan_version':planv2,'physics_qa':'Approved','physics_qa_note':'Physics QA for revised plan'});chk('RT-VERSION-012',st==200,{'status':st,'body':j})
st,j=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':planv2,'physician_final_approval':'Approved','status':'Ready for Treatment'});chk('RT-VERSION-013',st==200,{'status':st,'body':j})
st,j=act('Radiation Technologist','rt_deliver_fraction',rt['id'],{'fraction_number':2,'status':'Delivered','date_time':'2026-09-05T10:00:00+05:30','delivered_dose_gy':rx.get('dose_per_fraction_gy'),'verified_by':'RT Tech B','image_guidance_performed':True});chk('RT-VERSION-014',st==200 and j.get('plan_version')==planv2,{'status':st,'body':j})
rt=latest('Radiation Oncology','radiation');fra=rt['data'].get('fractions',[]);chk('RT-VERSION-015',len(fra)>=2 and fra[-2].get('plan_version')==planv and fra[-1].get('plan_version')==planv2,{'fractions':[(x.get('fraction_number'),x.get('prescription_version'),x.get('plan_version')) for x in fra]})

# Static UX markers for the new structural controls.
js=(ROOT/'static'/'pc1_4.js').read_text()
for i,marker in [('PC14-STATIC-001','Final-dose decision reason'),('PC14-STATIC-002','Set Allergy Status'),('PC14-STATIC-003','Fall-risk scale'),('PC14-STATIC-004','Replace Current Order'),('PC14-STATIC-005','Version-bound RT release')]:chk(i,marker in js,{'marker':marker})

out={'product':'V12.2-PC1.4 Structural Conformance Phase 2','total':len(OUT),'passed':sum(x['pass'] for x in OUT),'failed':sum(not x['pass'] for x in OUT),'results':OUT}
(ROOT/'V12_2_PC1_4_TRACK_B_PHASE2_RUN.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:out[k] for k in ['total','passed','failed']},indent=2))
raise SystemExit(0 if out['failed']==0 else 1)
