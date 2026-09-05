#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timedelta, date
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9012'); PIN=os.environ.get('CCA_DEMO_PIN','2026'); PID='PAT-0001'
P=[];F=[]
def http(path,method='GET',data=None,token=None):
 h={'Content-Type':'application/json'}; body=json.dumps(data).encode() if data is not None else None
 if token:h['Authorization']='Bearer '+token
 q=urllib.request.Request(BASE+path,data=body,headers=h,method=method)
 try:
  with urllib.request.urlopen(q,timeout=10) as r:
   raw=r.read();return r.status,json.loads(raw.decode()) if raw else {}
 except urllib.error.HTTPError as e:
  raw=e.read()
  try:j=json.loads(raw.decode()) if raw else {}
  except:j={'raw':raw.decode(errors='replace')}
  return e.code,j
def login(role):
 st,j=http('/api/login','POST',{'role':role,'pin':PIN});assert st==200,(role,st,j);return j['token']
T={r:login(r) for r in ['Front Desk','Nurse Navigator','Medical Oncology','Biller','Laboratory / Phlebotomy','PRE / Patient Relations Executive','Radiology Technician','Radiologist','MDT Coordinator','External Consultant','Oncology Pharmacy','Day Care / Infusion Nurse','Radiation Oncology','Radiation Physicist','Radiation Technologist','Surgical Oncology','Surgical Nurse','Finance / Billing','Hospital Management / Admin']}
def check(n,cond,d=''):
 (P if cond else F).append((n,d));print(('PASS' if cond else 'FAIL'),n,d)
def boot(role,pid=PID):
 st,j=http('/api/bootstrap?patient='+pid,token=T[role]);return st,j
OPT={'save_intake':'intake','med_recon':'med_recon','save_dynamic_form':'dynamic_forms','save_consultation':'consultation','save_diagnosis':'diagnosis','save_appointment':'appointments','queue_patient':'queue','save_care_plan':'care_plan','save_treatment_plan':'treatment_plan','save_radiology':'radiology','save_pathology':'pathology','mdt_comment':'mdt_collab','mdt_attendance':'mdt_collab','mdt_recommend':'mdt'}
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

def act(role,a,eid='',d=None,pid=PID):
 payload={'action':a,'patient_id':pid,'entity_id':eid,'data':pc13_adapt(a,d)}
 if a in OPT:
  st,b=boot(role,pid)
  if st==200:
   candidates=b.get('entities',{}).get(OPT[a],[])
   target=next((r for r in candidates if not eid or r.get('id')==eid),candidates[-1] if candidates else None)
   if target: payload['expected_version']=target.get('version')
 return http('/api/action','POST',payload,T[role])
def one(b,t):return b.get('entities',{}).get(t,[])[-1]

st,h=http('/api/health');check('health-v12',st==200 and h.get('version')=='12.2',h)
# Every configured role has an explicit INPUT / VIEW / OUTPUT working-surface contract.
admin_token=T['Hospital Management / Admin'];st,meta=http('/api/meta',token=admin_token);surface_gaps=[]
for rr in meta.get('roles',[]):
 st2,surf=http('/api/role-surface?role='+urllib.parse.quote(rr),token=admin_token)
 if st2!=200 or not surf.get('surface',{}).get('input') or not surf.get('surface',{}).get('view') or not surf.get('surface',{}).get('output'):surface_gaps.append(rr)
check('all-roles-have-input-view-output-contracts',not surface_gaps,surface_gaps)
# read scope
st,fd=boot('Front Desk');check('frontdesk-minimum-read',st==200 and 'treatment_order' not in fd['entities'] and 'pathology' not in fd['entities'],sorted(fd['entities']))
st,bi=boot('Biller');check('biller-minimum-read',st==200 and set(bi['entities']).issubset({'registration','lab_order','radiology_order','finance'}),sorted(bi['entities']))
st,x=http('/api/bootstrap?patient='+PID,token=T['External Consultant']);check('external-no-general-emr',st==403,x)
# duplicate gate
p={'name':'Maya Iyer','dob':'1980-02-11','sex':'Female','phone':'+91 90000 01001','id_number':'NEW-TEST-1','abha':'91-1111-2222-3333','initial_specialty':'Medical Oncology'}
st,x=http('/api/patient','POST',p,T['Front Desk']);check('duplicate-precreate-gate',st==409 and bool(x.get('matches')),x)
newp={'name':'Acceptance New Patient','dob':'1992-04-05','sex':'Female','phone':'+91 97777 12345','id_number':'ACC-NEW-100','abha':'91-9000-8000-7000','initial_specialty':'Medical Oncology'}
st,x=http('/api/patient','POST',newp,T['Front Desk']);npid=x.get('id');check('fresh-patient-create',st==200 and npid,x)
st,np=http('/api/bootstrap?patient='+npid,token=T['Medical Oncology']);needed={'intake','med_recon','consultation','diagnosis','mdt','mdt_collab','care_plan','treatment_plan','protocol_library','formulary','readiness','toxicity','modification','response','radiation','surgery','treatment_history'};check('fresh-patient-full-workspace-scaffold',st==200 and needed.issubset(set(np.get('entities',{}))),sorted(np.get('entities',{})))
# intake calc real write
st,nb=boot('Nurse Navigator');iid=one(nb,'intake')['id'];st,x=act('Nurse Navigator','save_intake',iid,{'bp':'120/80','hr':80,'rr':16,'temp_c':36.7,'spo2':99,'weight_kg':72,'height_cm':170,'ecog':'1','kps':'90','pain_score':2,'pain_site':'Breast','fall_risk_setting':'OPD','fall_risk_score':1,'fall_risk_level':'Low','past_medical':'Hypertension','past_surgical':'None','social_history':'No tobacco','complete':True});check('server-bmi-bsa',st==200 and abs(x['bsa_m2']-1.84)<.03,x)
# wrong role write direct
st,x=act('Front Desk','save_intake',iid,{'bp':'1'});check('wrong-role-intake-blocked',st==403,x)
# readiness safety: client values ignored; authoritative finalized Lab record + explicit units drive rules
st,mb=boot('Medical Oncology');rid=one(mb,'readiness')['id']
st,lb=boot('Laboratory / Phlebotomy');base_lab=one(lb,'lab');ld=base_lab['data']
unitset={'hb':'g/dL','wbc':'10^9/L','anc':'cells/uL','platelets':'cells/uL','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'}
vals={k:ld.get(k) for k in ['date','hb','wbc','creatinine','egfr','bilirubin','ast','alt','albumin','sodium','potassium','magnesium','calcium','lvef','pregnancy']}
st,x=act('Laboratory / Phlebotomy','save_lab',base_lab['id'],{**vals,'anc':800,'platelets':276000,'units':unitset,'amendment_reason':'V11.1 acceptance: explicit cells/uL neutropenia unit test','finalize':True});low_lab_id=x.get('id');check('authoritative-low-anc-lab-amendment',st==200 and low_lab_id and x.get('supersedes')==base_lab['id'],x)
# lie in client request: server must ignore these numbers/units and use the final lab amendment
fake={'template_id':'REG-CCA-TCHP-DEMO','anc':5.0,'platelets':500,'egfr':120,'bilirubin':0.1,'lab_units':{'anc':'10^9/L','platelets':'10^9/L','bilirubin':'mg/dL'},'hold_parameters':{}}
st,x=act('Medical Oncology','preview_readiness',rid,fake);check('server-owned-anc-block-0.8',st==200 and x.get('lab_source_id')==low_lab_id and any('ANC' in z for z in x['blockers']),x['blockers'])
check('unit-normalization-anc-800',st==200 and x['normalized']['anc_10e9_L']==.8 and any('ANC' in z for z in x['blockers']),x)
# proceed remains blocked while authoritative final lab is unsafe
st,x=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Proceed as Planned','sign':True});check('unsafe-proceed-blocked',st==409,x)
# restore good authoritative lab as another linked final amendment, then sign readiness
st,lb=boot('Laboratory / Phlebotomy');cur=one(lb,'lab');good_units={**unitset,'anc':'10^9/L','platelets':'10^9/L'}
st,x=act('Laboratory / Phlebotomy','save_lab',cur['id'],{**vals,'anc':3.2,'platelets':276,'units':good_units,'amendment_reason':'V11.1 acceptance: restore normal synthetic baseline','finalize':True});good_lab_id=x.get('id');check('authoritative-normal-lab-amendment',st==200 and good_lab_id,x)
st,x=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Proceed as Planned','reason':'Latest finalized lab with explicit units reviewed','sign':True});check('safe-readiness-signed',st==200 and x['status']=='Signed' and x.get('evaluation',{}).get('lab_source_id')==good_lab_id,x)
st,mb=boot('Medical Oncology');seed_order=one(mb,'treatment_order');check('signed-order-linked-to-exact-content-master-version',seed_order['data'].get('content_template_id')=='REG-CCA-TCHP-DEMO' and bool(seed_order['data'].get('content_template_version')) and bool(seed_order['data'].get('content_source_id')), {k:seed_order['data'].get(k) for k in ['content_template_id','content_template_version','content_source_id']})
# diagnostic lab/rad flows
st,x=act('Medical Oncology','create_diagnostic_order','',{'type':'Laboratory','name':'CBC','indication':'Pre-cycle CBC','date':str(date.today()),'decision_reason':'Synthetic acceptance-test investigation decision'});loid=x.get('id');check('lab-order-created',st==200 and loid,x)
st,x=act('Laboratory / Phlebotomy','collect_sample',loid,{'sample_id':'NO-PAY'});check('lab-collection-payment-gate',st==409,x)
st,x=act('Biller','record_payment',loid,{'payment_status':'Paid','amount':700,'receipt_no':'LAB-100'});check('lab-payment',st==200,x)
st,x=act('Laboratory / Phlebotomy','collect_sample',loid,{'sample_id':'SMP-100'});labid=x.get('lab_entity_id');check('lab-collection-after-payment',st==200 and labid,x)
st,x=act('Laboratory / Phlebotomy','save_lab',labid,{'date':str(date.today()),'hb':12,'wbc':6,'anc':3,'platelets':250,'creatinine':.8,'egfr':90,'bilirubin':.8,'ast':20,'alt':20,'albumin':4,'sodium':139,'potassium':4,'magnesium':2,'calcium':9,'lvef':60,'pregnancy':'Negative','units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalize':True});check('lab-finalize',st==200 and x['status']=='Final',x)
st,x=act('Medical Oncology','create_diagnostic_order','',{'type':'Radiology','name':'Breast MRI','indication':'Response assessment','date':str(date.today()),'decision_reason':'Synthetic acceptance-test investigation decision'});roid=x.get('id');check('radiology-order-created',st==200 and roid,x)
st,x=act('Biller','record_payment',roid,{'payment_status':'Paid','amount':5000,'receipt_no':'RAD-100'});check('radiology-payment',st==200,x)
st,x=act('PRE / Patient Relations Executive','schedule_radiology',roid,{'schedule':(datetime.now()+timedelta(days=1)).astimezone().isoformat()});check('radiology-schedule',st==200,x)
st,x=act('Radiology Technician','perform_radiology',roid,{'performed_at':datetime.now().astimezone().isoformat()});radid=x.get('radiology_entity_id');check('radiology-procedure-consent-payment',st==200 and radid,x)
st,x=act('Radiologist','save_radiology',radid,{'study':'Breast MRI','date':str(date.today()),'findings':'Interval reduction in index lesion','impression':'Treatment response','finalize':True});check('radiology-report-final',st==200 and x['status']=='Final',x)
# MDT + external de-id
st,md=boot('MDT Coordinator');coll=one(md,'mdt_collab')['id'];mdtid=one(md,'mdt')['id']
st,x=act('Medical Oncology','mdt_comment',coll,{'comment':'Systemic treatment perspective recorded.','mode':'addendum','addendum_reason':'Acceptance regression: late clinical perspective added after finalization'});check('mdt-multiuser-comment',st==200,x)
st,x=act('MDT Coordinator','mdt_attendance',coll,{'name':'Medical Oncology','discipline':'Medical Oncology','status':'Present'});check('mdt-attendance',st==200,x)
st,x=act('MDT Coordinator','invite_external_mdt',coll,{'name':'External Reviewer','discipline':'Medical Oncology','expires_at':(datetime.now().astimezone()+timedelta(days=2)).isoformat()});tok=x.get('access_token');check('external-case-token',st==200 and tok,x)
st,view=http('/api/mdt/external-view?access='+urllib.parse.quote(tok),token=T['External Consultant']);raw=json.dumps(view).lower();check('external-case-deidentified',st==200 and 'maya iyer' not in raw and 'mrn' not in raw and view.get('case_code'),view)
# systemic therapy chain query -> resolve -> verify -> prepare -> release -> MAR
st,mo=boot('Medical Oncology');oid=one(mo,'treatment_order')['id'];st,phb=boot('Oncology Pharmacy');ph=one(phb,'pharmacy');phid=ph['id'];checks={k:True for k in ['allergy','interaction','dose_method','calculated_dose','dose','organ_function','diluent','volume','stock','expiry']}
st,x=act('Medical Oncology','pharmacy_decision',phid,{'decision':'Verified','verification_checks':checks});check('prescriber-cannot-pharmacy-verify',st==403,x)
st,x=act('Oncology Pharmacy','pharmacy_decision',phid,{'decision':'Query','verification_checks':checks,'query_reason':'Dose requires clarification','message':'Confirm dose.'});check('pharmacy-query',st==200 and x['status']=='Queried',x)
st,x=act('Medical Oncology','oncologist_query_response',oid,{'response_action':'Confirm as ordered','response_note':'Reviewed and confirmed.'});check('oncologist-query-response',st==200,x)
st,x=act('Oncology Pharmacy','pharmacy_decision',phid,{'decision':'Verified','verification_checks':checks});check('pharmacy-verified',st==200 and x['status']=='Preparation Pending',x)
st,phb=boot('Oncology Pharmacy');ph=one(phb,'pharmacy');fm=one(phb,'formulary')['data']['items'];fmap={q['drug']:q for q in fm};prep=[]
for i,q in enumerate(ph['data']['items']):
 fi=fmap[q['drug']];fo=fi['formulations'][0];z=dict(q);z.update({'formulation':fo['label'],'formulation_strength_mg':fo.get('strength_mg',0),'batch':f'LOT-{i+1}','expiry':str(date.today()+timedelta(days=60)),'prepared_by':'Pharmacist A','actual_volume_ml':q.get('volume_ml',0),'barcode':f'BC-{i+1}' });prep.append(z)
st,x=act('Oncology Pharmacy','pharmacy_prepare',phid,{'items':prep,'preparation_note':'Acceptance test'});check('pharmacy-prepare',st==200 and x['status']=='Dispensing Pending',x)
st,phb=boot('Oncology Pharmacy');prepared=one(phb,'pharmacy')['data']['items'];same=[]
for q in prepared:
 pb=q.get('prepared_by') or {}; pname=pb.get('name') if isinstance(pb,dict) else str(pb); same.append({'item_id':q['item_id'],'second_check_by':pname,'label_verified':True})
st,x=act('Oncology Pharmacy','pharmacy_release',phid,{'items':same,'dispensed_to':'Day Care'});check('independent-check-separation',st==409,x)
rel=[{'item_id':q['item_id'],'second_check_by':'Pharmacist B','label_verified':True} for q in prepared];st,x=act('Oncology Pharmacy','pharmacy_release',phid,{'items':rel,'dispensed_to':'Day Care / Infusion','manifest_no':'MAN-1'});check('pharmacy-release',st==200 and x['status']=='Dispensed',x)
st,db=boot('Day Care / Infusion Nurse');inf=one(db,'infusion');infid=inf['id']
st,x=act('Day Care / Infusion Nurse','start_infusion',infid,{'checklist':{'identity':True},'access':'PICC'});check('eight-check-gate',st==409,x)
allchecks={k:True for k in ['identity','order','consent','allergy','vitals','labs','access','pharmacy']};st,x=act('Day Care / Infusion Nurse','start_infusion',infid,{'checklist':allchecks,'identity_confirmation':{'name':'Maya Iyer','mrn':'CCA-DEMO-0001','dob':'1980-02-11'},'pre_vitals':{'bp':'118/74','hr':78,'rr':16,'temp':36.7,'spo2':99},'access':'Right PICC','bedside_verification':{'verified_by':'RN B'}});check('infusion-start',st==200,x)
st,db=boot('Day Care / Infusion Nurse');inf=one(db,'infusion');ordr=one(db,'treatment_order');items=sorted(ordr['data']['items'],key=lambda z:z['sequence'])
# out-of-sequence
it=items[1];rec={'item_id':it['item_id'],'actual_dose':it['ordered_dose'],'unit':it['ordered_unit'],'access':'PICC','start_time':'10:00','end_time':'10:20','completion_status':'Administered','reaction':'None','chairside_verification':{'verified_by':'RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}};st,x=act('Day Care / Infusion Nurse','administer_item',infid,{'record':rec});check('out-of-sequence-block',st==409,x)
for n,it in enumerate(items):
 rec={'item_id':it['item_id'],'actual_dose':it['ordered_dose'],'unit':it['ordered_unit'],'access':'Right PICC','start_time':f'{10+n:02d}:00','end_time':f'{10+n:02d}:20','actual_rate':it.get('rate_ml_hr',0),'completion_status':'Administered','reaction':'None'}
 if it['group'] in ['Antineoplastic','Targeted Therapy']:rec['chairside_verification']={'verified_by':'RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
 st,x=act('Day Care / Infusion Nurse','administer_item',infid,{'record':rec});
 if st!=200:check('mar-item-'+str(n+1),False,x);break
else:check('all-mar-items',True,len(items))
st,x=act('Day Care / Infusion Nurse','administer_item',infid,{'record':{'item_id':items[0]['item_id'],'actual_dose':items[0]['ordered_dose']}});check('duplicate-mar-block',st==409,x)
st,x=act('Day Care / Infusion Nurse','complete_infusion',infid,{'post_vitals':{'bp':'120/76','hr':80,'rr':16,'temp':36.8,'spo2':99},'tolerance':'Good','discharge_instructions':'Call for red flags','next_cycle':str(date.today()+timedelta(days=21))});check('cycle-completed',st==200,x)
st,dc=boot('Day Care / Infusion Nurse');inf2=one(dc,'infusion');ord2=one(dc,'treatment_order');st,phx=boot('Oncology Pharmacy');ph2=one(phx,'pharmacy');omap={i['item_id']:i for i in ord2['data']['items']};pmap={i['item_id']:i for i in ph2['data']['items']};amap={i['item_id']:i for i in inf2['data']['mar']};recon=all(iid in pmap and iid in amap and float(oi['ordered_dose'])==float(pmap[iid]['ordered_dose'])==float(amap[iid]['actual_dose']) and oi['route']==pmap[iid]['route']==amap[iid]['route'] for iid,oi in omap.items());check('order-pharmacy-mar-dose-route-reconciliation',recon,[(oi['drug'],oi['ordered_dose'],pmap.get(iid,{}).get('ordered_dose'),amap.get(iid,{}).get('actual_dose')) for iid,oi in omap.items()])
# toxicity + response
st,mo=boot('Medical Oncology');toxid=one(mo,'toxicity')['id'];st,x=act('Medical Oncology','record_toxicity',toxid,{'term':'Nausea','grade':'2','onset_date':str(date.today()),'attribution':'Probably related','intervention':'Supportive care','outcome':'Resolving','notes':'Acceptance test'});check('ctcae-toxicity',st==200,x)
resid=one(mo,'response')['id'];st,x=act('Medical Oncology','save_response',resid,{'date':str(date.today()),'target_lesions':[{'id':'L1','site':'Left breast','size_mm':30}],'new_lesions':False,'non_target':'Improved'});check('response-pr-calculated',st==200 and x.get('proposed_category')=='Partial response',x)
# V12 content master + role-surface governance
st,x=http('/api/content',token=T['Medical Oncology']);regs=[r for r in x.get('templates',[]) if r.get('category')=='Regimen'];check('content-master-regimen-library',st==200 and len(regs)>=4 and any(r['id']=='REG-OMRS-AC' and not r['orderable'] for r in regs),[(r['id'],r['status'],r['orderable']) for r in regs])
st,x=http('/api/role-surface?role=Medical%20Oncology',token=T['Medical Oncology']);check('medical-oncology-input-view-output-contract',st==200 and len(x['surface']['input'])>=20 and len(x['surface']['view'])>=10 and len(x['surface']['output'])>=4,x.get('status'))
st,x=http('/api/role-surface?role=Oncology%20Pharmacy',token=T['Medical Oncology']);check('cross-role-surface-admin-gate',st==403,x)
st,x=http('/api/role-surface?role=Oncology%20Pharmacy',token=T['Hospital Management / Admin']);check('admin-can-review-role-contracts',st==200 and x['surface']['input'] and x['surface']['view'] and x['surface']['output'],x.get('role'))
# External historical content is immutable. Local activation must follow import -> clone -> localize -> formulary -> independent reviews -> Admin activation.
st,x=act('Medical Oncology','content_regimen_safety_rules','REG-OMRS-AC',{'template_id':'REG-OMRS-AC','hold_parameters':{'ANC_min':1.5,'platelets_min':100,'eGFR_min':50,'bilirubin_max':1.5,'LVEF_min':0,'lab_max_age_days':7}});check('imported-source-direct-edit-blocked',st==409 and 'immutable' in x.get('error','').lower(),x)
st,x=act('Hospital Management / Admin','content_approve','REG-OMRS-AC',{'template_id':'REG-OMRS-AC'});check('imported-source-direct-activation-blocked',st==409 and 'clone' in x.get('error','').lower(),x)
st,x=act('Hospital Management / Admin','content_clone','REG-OMRS-AC',{'template_id':'REG-OMRS-AC','name':'AC — CCA Working Copy Acceptance','version':'1.0-cca-draft'});clone=x.get('template',{}) if st==200 else {};clone_id=clone.get('id','');check('historical-regimen-cloned-with-provenance',st==200 and clone.get('source_id')=='SRC-CCA-DEMO' and clone.get('data',{}).get('origin_template_id')=='REG-OMRS-AC',clone.get('data',{}).get('origin_source_ref'))
# Regimen sequence can be localized only on the CCA working copy. Edit one code-system field and verify review reset.
st,x=act('Medical Oncology','content_regimen_item_edit',clone_id,{'template_id':clone_id,'operation':'update','item':{'sequence':4,'group':'Antineoplastic','drug':'Doxorubicin','code':'OMRS-DOX60','code_system':'Historical OpenMRS mapping — local terminology review pending','dose_basis':'mg/m²','protocol_dose':60,'protocol_unit':'mg/m²','route':'IV','relative_start_days':[1],'timing':'Historical source timing retained for review','diluent':'NS','volume_ml':None,'duration_min':15,'special_instructions':'Historical source reference — local validation required.'}});check('working-copy-structured-regimen-item-edit',st==200 and x.get('template',{}).get('status')=='Draft',x.get('template',{}).get('governance_status'))
# Institution formulary is now a separate governed master. Create missing mappings as acceptance-test drafts, pharmacy review, then Admin activate.
st,fx=http('/api/formulary',token=T['Oncology Pharmacy']);check('institution-formulary-api',st==200 and fx.get('active_count',0)>=6,fx.get('active_count'))
missing_forms=[
 ('Sodium chloride 0.9%','ACC-NS','IV',500),('Ondansetron','ACC-OND','PO',8),('Doxorubicin','ACC-DOX','IV',50),('Cyclophosphamide','ACC-CYC','IV',1000)]
for drug,code,route,strength in missing_forms:
 st,x=act('Oncology Pharmacy','formulary_save','',{'drug':drug,'display_name':drug+' — acceptance-test local product','code_system':'CCA acceptance-test dictionary','code':code,'version':'1.0-acceptance','allowed_routes':[route],'allowed_diluents':['NS'] if route=='IV' else [],'formulations':[{'label':drug+' acceptance-test formulation','strength_mg':strength}],'rounding_policy':'No rounding','notes':'Acceptance-test local mapping only; not prescribing content.','source_ref':'V12 acceptance test'});fid=x.get('item',{}).get('id','');check('formulary-draft-'+code,st==200 and x.get('item',{}).get('status')=='Draft',x)
 st,x=act('Oncology Pharmacy','formulary_review',fid,{'formulary_id':fid,'status':'Approved','note':'Acceptance-test pharmacy governance.'});check('formulary-review-'+code,st==200 and x.get('item',{}).get('pharmacy_review',{}).get('status')=='Approved',x)
 st,x=act('Hospital Management / Admin','formulary_approve',fid,{'formulary_id':fid});check('formulary-activate-'+code,st==200 and x.get('item',{}).get('status')=='Active',x)
# Server-owned safety criteria plus independent Medical Oncology and Pharmacy content reviews.
st,x=act('Medical Oncology','content_regimen_safety_rules',clone_id,{'template_id':clone_id,'hold_parameters':{'ANC_min':1.5,'platelets_min':100,'eGFR_min':50,'bilirubin_max':1.5,'LVEF_min':0,'lab_max_age_days':7}});check('working-copy-safety-rules-governed',st==200,x.get('ok'))
st,x=act('Medical Oncology','content_clinical_review',clone_id,{'template_id':clone_id,'status':'Approved','note':'Acceptance-test clinical governance only; not a production clinical approval.'});check('working-copy-clinical-review',st==200,x.get('ok'))
st,x=act('Oncology Pharmacy','content_pharmacy_review',clone_id,{'template_id':clone_id,'status':'Approved','note':'Acceptance-test pharmacy governance only; not a production clinical approval.'});check('working-copy-pharmacy-review',st==200,x.get('ok'))
st,x=act('Hospital Management / Admin','content_approve',clone_id,{'template_id':clone_id});check('working-copy-activation-after-formulary-and-reviews',st==200 and x.get('template',{}).get('orderable') is True,x)
# Report-template engine: role-authorized templates bind to authoritative patient records and keep source records read-only.
st,x=http('/api/report/render?template=RPT-TX-ORDER&patient=PAT-0001',token=T['Medical Oncology']);check('report-template-signed-order-render',st==200 and x.get('header',{}).get('template_id')=='RPT-TX-ORDER' and any(z.get('title')=='Signed Treatment Order' for z in x.get('sections',[])),x.get('header'))
st,x=http('/api/report/render?template=RPT-PHARM-PREP&patient=PAT-0001',token=T['Oncology Pharmacy']);check('report-template-pharmacy-render',st==200 and any(z.get('title')=='Preparation / Dispensing' for z in x.get('sections',[])),x.get('header'))
st,x=http('/api/report/render?template=RPT-MAR&patient=PAT-0001',token=T['Front Desk']);check('report-template-role-access-block',st==403,x)
# MDT output creates Draft plan only, not order
st,md=boot('MDT Coordinator');mdtid=one(md,'mdt')['id'];before_orders=len((boot('Medical Oncology')[1]['entities'].get('treatment_order') or []));st,x=act('MDT Coordinator','create_plan_from_mdt',mdtid,{'specialty':'Combined-Modality'});check('mdt-creates-draft-plan-only',st==200 and x.get('status')=='Draft',x)
after=boot('Medical Oncology')[1];check('mdt-plan-does-not-auto-create-order',len(after['entities'].get('treatment_order') or [])==before_orders,before_orders)
# RT with separate Physicist QA and Radiation Oncologist final approval
st,rb=boot('Radiation Oncology');rtid=one(rb,'radiation')['id'];rx=one(rb,'radiation')['data']['prescription'];st,x=act('Radiation Oncology','rt_save_prescription',rtid,{**rx,'sign':True});check('rt-sign',st==200 and x['status']=='RT Oncologist Approved',x)
st,x=act('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered'});check('rt-block-before-qa',st==409,x)
st,x=act('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'simulation_status':'Completed','contouring_status':'Completed','planning_status':'Planning Complete','status':'Planning'});check('rt-plan-prepared-before-physics',st==200,x)
st,x=act('Radiation Physicist','rt_planning_status',rtid,{'plan_version':1,'physics_qa':'Approved','physics_qa_note':'Independent physics QA completed'});check('rt-physics-qa-independent-role',st==200,x)
st,x=act('Radiation Physicist','rt_planning_status',rtid,{'plan_version':1,'physician_final_approval':'Approved','physics_qa':'Approved','physics_qa_note':'Attempt'});check('physicist-cannot-physician-approve',st==403,x)
st,x=act('Radiation Oncology','rt_planning_status',rtid,{'plan_version':1,'physician_final_approval':'Approved','status':'Ready for Treatment'});check('rt-physician-final-approval',st==200 and x.get('status')=='Ready for Treatment',x)
st,x=act('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered','delivered_dose_gy':rx['dose_per_fraction_gy'],'date_time':datetime.now().astimezone().isoformat(),'image_guidance_performed':True,'verified_by':'RTT second verifier','setup_variation':'Within tolerance','toxicity':'None'});check('rt-fraction-delivery',st==200,x)
st,x=act('Radiation Technologist','rt_deliver_fraction',rtid,{'fraction_number':1,'status':'Delivered','delivered_dose_gy':rx['dose_per_fraction_gy']});check('rt-duplicate-fraction-block',st==409,x)
# Surgery
st,sb=boot('Surgical Oncology');sid=one(sb,'surgery')['id'];sp=one(sb,'surgery')['data']['plan'];st,x=act('Surgical Oncology','surgery_sign_plan',sid,sp);check('surgery-plan-sign',st==200,x)
st,x=act('Surgical Oncology','surgery_performed',sid,{'actual_procedure':'Left lumpectomy'});check('surgery-block-before-preop',st==409,x)
st,x=act('Surgical Nurse','surgery_preop',sid,{'anesthesia_clearance':'Complete','labs':'Complete','consent':'Complete'});check('surgery-preop',st==200 and x['ready'],x)
su={'actual_procedure':'Left lumpectomy + sentinel node biopsy','operation_date_time':datetime.now().astimezone().isoformat(),'preop_diagnosis':'Breast cancer','postop_diagnosis':'Breast cancer','laterality':'Left','findings':'Localized residual tumor','specimens':['Lumpectomy specimen','Sentinel nodes'],'estimated_blood_loss_ml':50,'operative_time_min':120,'surgeons':['Surgical Oncology User'],'postop_plan':'Final pathology and adjuvant review'}
st,x=act('Surgical Oncology','surgery_performed',sid,su);check('surgery-performed',st==200,x)
# link final pathology and verify new pathological stage does not overwrite historical clinical stage
st,sb=boot('Surgical Oncology');pathid=one(sb,'pathology')['id'];before_dx=len(sb['entities'].get('diagnosis',[]));st,x=act('Surgical Oncology','surgery_pathology_link',sid,{'pathology_record_id':pathid,'margin_status':'Negative','nodes_examined':3,'nodes_positive':0,'path_t':'ypT1','path_n':'ypN0','path_m':'cM0','postop_stage':'ypStage IA','staging_date':str(date.today())});check('surgery-pathology-new-path-stage',st==200 and x.get('pathological_stage_record_id'),x)
st,sb2=boot('Surgical Oncology');dxs=sb2['entities'].get('diagnosis',[]);check('clinical-stage-preserved-and-path-stage-appended',len(dxs)==before_dx+1 and dxs[0]['data'].get('stage_group')=='Stage IIB' and dxs[-1]['data'].get('staging_basis')=='Pathological',[(z['id'],z['data'].get('stage_group'),z['data'].get('staging_basis')) for z in dxs])
# finance cannot clinical write; estimate can
st,x=act('Finance / Billing','save_treatment_plan',one(mo,'treatment_plan')['id'],{'sign':True});check('finance-cannot-treatment-plan',st==403,x)
st,fb=boot('Finance / Billing');cid=one(fb,'conversion')['id'];st,x=act('Finance / Billing','finance_estimate',cid,{});check('finance-estimate',st==200 and x['total']>0,x.get('total'))
# audit hash
st,x=http('/api/audit/verify',token=T['Hospital Management / Admin']);check('audit-hash-chain',st==200 and x.get('ok'),x)
st,mo2=boot('Medical Oncology');ridv=one(mo2,'readiness')['id'];st,v=http('/api/record-versions?record='+ridv,token=T['Medical Oncology']);check('record-version-history',st==200 and len(v.get('versions',[]))>=2,[z.get('version') for z in v.get('versions',[])])
print('\nRESULT',len(P),'PASS',len(F),'FAIL')
if F:
 for z in F:print('FAILED',z)
 sys.exit(1)
