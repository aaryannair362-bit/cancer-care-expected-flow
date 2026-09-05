#!/usr/bin/env python3
import json, urllib.request, urllib.error, urllib.parse, os
from datetime import date, datetime, timedelta
from pathlib import Path
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9103'); PIN=os.environ.get('CCA_DEMO_PIN','2026'); PID='PAT-0001'; T={}; OUT=[]
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
 st,j=http('/api/login','POST',{'role':role,'pin':PIN});
 if st!=200:raise RuntimeError((role,st,j))
 T[role]=j['token'];return T[role]
def boot(role):return http('/api/bootstrap?patient='+urllib.parse.quote(PID),token=login(role))
def latest(role,t):
 st,b=boot(role);xs=b.get('entities',{}).get(t,[]);return xs[-1] if xs else None
def act(role,a,eid='',d=None):
 payload={'action':a,'patient_id':PID,'entity_id':eid,'data':d or {}}
 if a=='save_intake':
  st,b=boot(role);xs=b.get('entities',{}).get('intake',[]) if st==200 else [];target=next((x for x in xs if x.get('id')==eid),xs[-1] if xs else None)
  if target:payload['expected_version']=target.get('version')
 return http('/api/action','POST',payload,login(role))
def chk(i,cond,ev):OUT.append({'id':i,'pass':bool(cond),'evidence':ev});print(('PASS' if cond else 'FAIL'),i,json.dumps(ev,ensure_ascii=False)[:550])

roles=['Oncology Pharmacy','Day Care / Infusion Nurse','MDT Coordinator','Pathology','Radiation Technologist','Radiation Physicist','Radiation Oncology','Surgical Oncology','Nurse Navigator','Medical Oncology']
for r in roles:login(r)

# Visibility gaps closed at API/read-scope level.
for i,role,need in [
 ('VG-001-004','Oncology Pharmacy',{'lab','readiness','toxicity','treatment_history','infusion'}),
 ('VG-005-006','Day Care / Infusion Nurse',{'intake','toxicity','treatment_history'}),
 ('VG-007-009','MDT Coordinator',{'treatment_history','toxicity','response'}),
 ('VG-010-011','Pathology',{'diagnosis','cancer_episode','pathology','treatment_history'}),
 ('VG-015','Radiation Oncology',{'intake','toxicity'}),('VG-016','Surgical Oncology',{'intake','toxicity','treatment_history'})]:
 st,b=boot(role);keys=set(b.get('entities',{}));chk(i,st==200 and need.issubset(keys),{'role':role,'required':sorted(need),'visible':sorted(keys)})

# Intake measured units: missing units rejected; alternate units normalize; derived BSA ignores malicious client BSA.
intake=latest('Nurse Navigator','intake')
base={'sbp':120,'dbp':80,'hr':80,'rr':16,'temp':98.6,'spo2':99,'weight':154.324,'height':66.929,'ecog':'1','kps':'90','pain_instrument':'Numeric Rating Scale 0–10','pain_score':2,'pain_site':'Synthetic','fall_risk_setting':'OPD','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':1,'fall_risk_level':'Low','complete':True,'bsa_m2':99}
st,j=act('Nurse Navigator','save_intake',intake['id'],base);chk('INT-UNIT-001',st==409 and bool(j.get('missing_units')),{'status':st,'body':j})
base['units']={'bp':'mmHg','hr':'/min','rr':'/min','temp':'°F','spo2':'%','weight':'lb','height':'in'}
st,j=act('Nurse Navigator','save_intake',intake['id'],base);chk('INT-UNIT-002',st==200 and abs(j.get('bsa_m2',0)-1.82)<0.02 and j.get('canonical_units',{}).get('weight_kg')=='kg',{'status':st,'body':j})
mo_int=latest('Medical Oncology','intake');chk('INT-DERIVED-003',abs(mo_int['data'].get('bsa_m2',0)-1.82)<0.02 and mo_int['data'].get('bsa_m2')!=99 and bool(mo_int['data'].get('source_measurements')),{'stored_bsa':mo_int['data'].get('bsa_m2'),'sources':mo_int['data'].get('source_measurements')})

# Create a fresh signed cycle order and prove dosing snapshot carries measurement provenance.
plan=latest('Medical Oncology','treatment_plan');ready=latest('Medical Oncology','readiness')
st,j=act('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan['id'],'administration_setting':'Day Care','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'Synthetic QA','cycle':2,'day':1,'start_date':str(date.today()),'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic clinician-entered AUC product-test dose'},'dose_decision_reasons':{'*':'Synthetic clinician acceptance of final ordered dose after review','DEMO-CARBO':'Patient-specific AUC product-test dose accepted after clinician review'},'administration_decision_reason':'Synthetic clinician acceptance of regimen administration parameters after review','schedule_decision_reason':'Synthetic clinician acceptance of treatment administration date/time after review'});chk('ORD-SNAPSHOT-001',st==200,{'status':st,'body':j});oid=j.get('order_id');phid=j.get('pharmacy_id');infid=j.get('infusion_id')
o=next((x for x in boot('Medical Oncology')[1]['entities']['treatment_order'] if x['id']==oid),None);ps=o['data'].get('patient_snapshot',{}) if o else {};chk('ORD-SNAPSHOT-002',bool(ps.get('source_measurements')) and ps.get('bsa_formula') and ps.get('measured_at'),{'snapshot':ps})

# Pharmacy: verification then missing preparation governance fields must block.
checks={k:True for k in ['patient_identity','allergy','regimen_version','cycle_day','dose_basis','calculated_dose','ordered_dose','dose_variance','renal_adjustment','hepatic_adjustment','cumulative_dose','interaction','duplication','route','diluent','final_concentration','stock','expiry']}
st,j=act('Oncology Pharmacy','pharmacy_decision',phid,{'decision':'Verified','verification_checks':checks});chk('PHM-VERIFY-001',st==200,{'status':st,'body':j})
ph=next(x for x in boot('Oncology Pharmacy')[1]['entities']['pharmacy'] if x['id']==phid);st,fm=http('/api/formulary',token=login('Oncology Pharmacy'));fmap={x['drug']:x for x in fm.get('items',[]) if x.get('status')=='Active'}
pre=[]
for n,it in enumerate(ph['data']['items'],1):
 fi=fmap[it['drug']];form=fi['formulations'][0];x=dict(it);x.update({'formulation':form['label'],'formulation_strength_mg':form['strength_mg'],'batch':f'PC13-{n}','expiry':str(date.today()+timedelta(days=60)),'prepared_by':'Oncology Pharmacist A'});pre.append(x)
st,j=act('Oncology Pharmacy','pharmacy_prepare',phid,{'items':pre});chk('PHM-PREP-002',st==409 and ('volume' in j.get('error','').lower() or 'compatibility' in j.get('error','').lower()),{'status':st,'body':j})
bud=(datetime.now().astimezone()+timedelta(hours=4)).isoformat(timespec='minutes')
for x in pre:x.update({'actual_volume_ml':x.get('volume_ml') or 0,'actual_volume_unit':'mL','compatibility_status':'Compatible','stability_reference':'Synthetic QA stability reference — NOT CLINICAL','beyond_use_at':bud,'storage_condition':'Synthetic QA storage condition — NOT CLINICAL','light_protection':'Not required','filter_requirement':'Synthetic QA filter status — NOT CLINICAL','container_requirement':'Synthetic QA container — NOT CLINICAL'})
st,j=act('Oncology Pharmacy','pharmacy_prepare',phid,{'items':pre,'preparation_note':'Synthetic structural-conformance test'});chk('PHM-PREP-003',st==200,{'status':st,'body':j})
rel=[{**x,'second_check_by':'Oncology Pharmacist B','label_verified':True} for x in pre];st,j=act('Oncology Pharmacy','pharmacy_release',phid,{'items':rel,'dispensed_to':'Day Care / Infusion','manifest_no':'PC13-MAN'});chk('PHM-RELEASE-004',st==200,{'status':st,'body':j})

# MAR: explicit actual-dose unit and IV rate unit enforced.
p=boot('Day Care / Infusion Nurse')[1]['patient'];start={'checklist':{k:True for k in ['identity','order','consent','allergy','vitals','labs','access','pharmacy']},'identity_confirmation':{'name':p['name'],'mrn':p['mrn'],'dob':p['dob']},'pre_vitals':{'bp':'118/74','hr':78,'rr':16,'temp':36.7,'spo2':99,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'}},'access':{'type':'PICC','site':'Right upper limb','detail':'Right PICC — patent'},'bedside_verification':{'confirmed':True,'verified_by':'Oncology RN B'}}
st,j=act('Day Care / Infusion Nurse','start_infusion',infid,start);chk('MAR-START-001',st==200,{'status':st,'body':j})
inf=next(x for x in boot('Day Care / Infusion Nurse')[1]['entities']['infusion'] if x['id']==infid);order=next(x for x in boot('Day Care / Infusion Nurse')[1]['entities']['treatment_order'] if x['id']==oid);it=sorted(order['data']['items'],key=lambda z:z['sequence'])[0]
rec={'item_id':it['item_id'],'actual_dose':it['ordered_dose'],'access':'Right PICC','start_time':'10:00','end_time':'10:10','actual_rate':it.get('rate_ml_hr',0),'completion_status':'Administered','reaction':'None','variance_note':''}
if it.get('group') in ['Antineoplastic','Targeted Therapy']:rec['chairside_verification']={'verified_by':'Oncology RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':rec});chk('MAR-UNIT-002',st==409 and 'unit' in j.get('error','').lower(),{'status':st,'body':j})
rec['actual_dose_unit']=it['ordered_unit']
if it.get('route')=='IV' or float(it.get('rate_ml_hr') or 0)>0:rec['actual_rate_unit']='mL/h'
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':rec});chk('MAR-UNIT-003',st==200,{'status':st,'body':j})

# Advance to the first IV item and prove an explicit actual-rate unit is mandatory.
order=next(x for x in boot('Day Care / Infusion Nurse')[1]['entities']['treatment_order'] if x['id']==oid)
next_iv=next((x for x in sorted(order['data']['items'],key=lambda z:z['sequence']) if x['sequence']>it['sequence'] and (x.get('route')=='IV' or float(x.get('rate_ml_hr') or 0)>0)),None)
if next_iv:
 ivrec={'item_id':next_iv['item_id'],'actual_dose':next_iv['ordered_dose'],'actual_dose_unit':next_iv['ordered_unit'],'access':'Right PICC','start_time':'10:15','end_time':'11:15','actual_rate':next_iv.get('rate_ml_hr') or 250,'completion_status':'Administered','reaction':'None','variance_note':''}
 if next_iv.get('group') in ['Antineoplastic','Targeted Therapy']:
  ivrec['chairside_verification']={'verified_by':'Oncology RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
 st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':ivrec});chk('MAR-RATE-004',st==409 and 'rate' in j.get('error','').lower() and 'unit' in j.get('error','').lower(),{'status':st,'body':j,'item':next_iv.get('drug')})
 ivrec['actual_rate_unit']='mL/h'
 st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':ivrec});chk('MAR-RATE-005',st==200,{'status':st,'body':j,'item':next_iv.get('drug')})
else:
 chk('MAR-RATE-004',False,{'error':'No IV item available in synthetic QA regimen'})
 chk('MAR-RATE-005',False,{'error':'No IV item available in synthetic QA regimen'})

# Static clinician-facing evidence for remaining visibility items.
js=(ROOT/'static/pc1_3.js').read_text()
markers={
 'VG-012-013':'Today\'s delivery context:', 'VG-014':'Plan-version approval context:',
 'VG-017':'Vitals & Intake (Intake Nurse workflow)', 'VG-018':'source_measurements',
 'VG-019':'Prior treatment / response / toxicity', 'VG-020':'Signed order dosing snapshot'
}
for cid,mark in markers.items():chk(cid,mark in js,{'marker':mark,'file':'static/pc1_3.js'})

# JS syntax and structural files.
chk('PC13-STATIC-001',(ROOT/'static/pc1_3.js').exists() and 'pc1_3.js' in (ROOT/'static/index.html').read_text(),{'pc1_3_exists':(ROOT/'static/pc1_3.js').exists()})

summary={'suite':'V12.2-PC1.3 Structural Conformance Phase 1','total':len(OUT),'passed':sum(x['pass'] for x in OUT),'failed':sum(not x['pass'] for x in OUT),'results':OUT}
(ROOT/'V12_2_PC1_3_TRACK_B_PHASE1_RUN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
print(json.dumps({k:summary[k] for k in ['total','passed','failed']},indent=2))
raise SystemExit(1 if summary['failed'] else 0)
