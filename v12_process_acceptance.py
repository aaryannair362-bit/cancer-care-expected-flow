#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.error
from datetime import date,timedelta
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9062'); PIN=os.environ.get('CCA_DEMO_PIN','2026'); PID='PAT-0001'
P=[];F=[]
def http(path,method='GET',data=None,token=None):
 h={'Content-Type':'application/json'};body=json.dumps(data).encode() if data is not None else None
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
roles=['Front Desk','Nurse Navigator','Medical Oncology','Surgical Oncology','Radiation Oncology','MDT Coordinator','Oncology Pharmacy','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Radiation Technologist','Radiation Physicist','Hospital Management / Admin']
T={r:login(r) for r in roles}
def boot(role,pid=PID):return http('/api/bootstrap?patient='+pid,token=T[role])
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
def check(n,c,d=''):
 (P if c else F).append((n,d));print(('PASS' if c else 'FAIL'),n,d)

st,h=http('/api/health');check('health-v12',st==200 and h.get('version')=='12.2',h)
# Every role including IPD nurse has a populated role surface.
st,meta=http('/api/meta',token=T['Hospital Management / Admin']); gaps=[]
for r in meta.get('roles',[]):
 st2,j=http('/api/role-surface?role='+urllib.parse.quote(r),token=T['Hospital Management / Admin']) if False else (None,None)
# use quote-free because role endpoint accepts parse_qs after URL encoding via urllib below
import urllib.parse
for r in meta.get('roles',[]):
 st2,j=http('/api/role-surface?role='+urllib.parse.quote(r),token=T['Hospital Management / Admin'])
 if st2!=200 or not all(j.get('surface',{}).get(k) for k in ['input','view','output']):gaps.append(r)
check('all-roles-input-view-output-including-ipd',not gaps,gaps)

# Visibility seam fixes.
st,ph=boot('Oncology Pharmacy');check('pharmacy-sees-nurse-intake-patient-variables',st==200 and 'intake' in ph['entities'] and ph['entities']['intake'][-1]['data'].get('bsa_m2') is not None,ph['entities'].get('intake',[{}])[-1].get('data',{}).get('bsa_m2'))
st,rad=boot('Radiation Oncology');check('rad-onc-sees-active-systemic-order-not-pharmacy',st==200 and 'treatment_order' in rad['entities'] and 'pharmacy' not in rad['entities'] and 'infusion' not in rad['entities'],sorted(rad['entities']))
st,su=boot('Surgical Oncology');check('surg-onc-sees-active-systemic-order-not-pharmacy',st==200 and 'treatment_order' in su['entities'] and 'pharmacy' not in su['entities'] and 'infusion' not in su['entities'],sorted(su['entities']))

# Dedicated journey is real and department-level.
st,mo=boot('Medical Oncology');j=one(mo,'journey');events=j['data'].get('events',[]);check('dedicated-patient-journey-exists',len(events)>=3 and all('department' in x and 'care_stage' in x for x in events),[(x['department'],x['care_stage']) for x in events])

# T1 execution: seed signed order → pharmacy → Day Care MAR completion.
order=one(mo,'treatment_order');oid=order['id'];phrec=next(x for x in ph['entities']['pharmacy'] if x['data'].get('order_id')==oid)
checks={k:True for k in ['allergy','interaction','dose_method','calculated_dose','dose','organ_function','diluent','volume','stock','expiry']}
st,x=act('Oncology Pharmacy','pharmacy_decision',phrec['id'],{'decision':'Verified','verification_checks':checks});check('t1-pharmacy-verify',st==200 and x.get('status')=='Preparation Pending',x)
st,ph2=boot('Oncology Pharmacy');phrec=next(x for x in ph2['entities']['pharmacy'] if x['data'].get('order_id')==oid); fm=http('/api/formulary',token=T['Oncology Pharmacy'])[1]['items']; fmap={x['drug']:x for x in fm if x['status']=='Active'};prep=[];expiry=(date.today()+timedelta(days=90)).isoformat()
for n,it in enumerate(phrec['data']['items'],1):
 fi=fmap[it['drug']];form=fi['formulations'][0];z=dict(it);z.update({'formulation':form['label'],'formulation_strength_mg':form['strength_mg'],'batch':f'T1-{n:02d}','expiry':expiry,'prepared_by':'Oncology Pharmacist A','prep_start':'09:00','prep_finish':'09:15','actual_volume_ml':it.get('volume_ml') or 0,'waste':'0','barcode':f'T1BC{n}'});prep.append(z)
st,x=act('Oncology Pharmacy','pharmacy_prepare',phrec['id'],{'items':prep});check('t1-pharmacy-prepare',st==200 and x.get('status')=='Dispensing Pending',x)
release=[{**z,'second_check_by':'Oncology Pharmacist B','label_verified':True} for z in prep]
st,x=act('Oncology Pharmacy','pharmacy_release',phrec['id'],{'items':release,'dispensed_to':'Day Care / Infusion','manifest_no':'T1-MAN'});check('t1-pharmacy-release',st==200 and x.get('status')=='Dispensed',x)
st,dc=boot('Day Care / Infusion Nurse');inf=next(x for x in dc['entities']['infusion'] if x['data'].get('order_id')==oid)
p=S=dc['patient'];start={'checklist':{k:True for k in ['identity','order','consent','allergy','vitals','labs','access','pharmacy']},'identity_confirmation':{'name':p['name'],'mrn':p['mrn'],'dob':p['dob']},'pre_vitals':{'bp':'118/74','hr':78,'rr':16,'temp':36.7,'spo2':99},'access':'Right PICC — patent','bedside_verification':{'confirmed':True,'verified_by':'Oncology RN B'}}
st,x=act('Day Care / Infusion Nurse','start_infusion',inf['id'],start);check('t1-daycare-start',st==200,x)
for n,it in enumerate(order['data']['items'],1):
 r={'item_id':it['item_id'],'actual_dose':it['ordered_dose'],'unit':it['ordered_unit'],'access':'Right PICC','start_time':f'{9+n:02d}:00','end_time':f'{9+n:02d}:20','actual_rate':it.get('rate_ml_hr',0),'completion_status':'Administered','reaction':'None','variance_note':''}
 if it.get('group') in ['Antineoplastic','Targeted Therapy']:r['chairside_verification']={'verified_by':'Oncology RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
 st,x=act('Day Care / Infusion Nurse','administer_item',inf['id'],{'record':r});
 if st!=200: break
check('t1-all-mar-items-recorded',st==200,x)
st,x=act('Day Care / Infusion Nurse','complete_infusion',inf['id'],{'post_vitals':{'bp':'120/76','hr':80,'rr':16,'temp':36.8,'spo2':99},'tolerance':'Good','discharge_instructions':'Routine treatment-day instructions','next_cycle':str(date.today()+timedelta(days=21))});check('t1-cycle-completed',st==200,x)
st,dc=boot('Day Care / Infusion Nurse');inf=next(x for x in dc['entities']['infusion'] if x['data'].get('order_id')==oid);check('t1-order-admin-reconciliation',inf['status']=='Completed' and len(inf['data']['mar'])==len(order['data']['items']) and all(float(m['actual_dose'])==float(next(q for q in order['data']['items'] if q['item_id']==m['item_id'])['ordered_dose']) for m in inf['data']['mar']),len(inf['data']['mar']))

# Low-count hold propagates to care plan/journey/scheduler, using final lab units.
st,mo=boot('Medical Oncology');lab=one(mo,'lab'); labd=dict(lab['data']); labd.update({'anc':800,'units':{**labd.get('units',{}),'anc':'cells/uL'},'finalize':True,'amendment_reason':'V12 process test low ANC'})
# Lab role token not in T - login now
T['Laboratory / Phlebotomy']=login('Laboratory / Phlebotomy')
st,x=act('Laboratory / Phlebotomy','save_lab',lab['id'],labd);check('low-anc-amendment-finalized',st==200 and x.get('status')=='Final',x); low_lab_id=x.get('id')
st,mo=boot('Medical Oncology');rid=one(mo,'readiness')['id'];st,x=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Hold','decision_reason':'ANC below protocol threshold','reevaluation_date':str(date.today()+timedelta(days=2)),'sign':True});check('signed-hold-allowed-with-blocker',st==200 and x.get('status')=='Signed',x)
st,mo=boot('Medical Oncology');cp=one(mo,'care_plan');jj=one(mo,'journey');check('hold-propagates-careplan-journey',cp['data'].get('current_exception',{}).get('type')=='Hold' and any(e.get('care_stage')=='Treatment Hold' for e in jj['data'].get('events',[])),cp['data'].get('current_exception'))
# restore normal ANC with a new final amendment and proceed
lab=one(mo,'lab');ld=dict(lab['data']);ld.update({'anc':3.2,'units':{**ld.get('units',{}),'anc':'10^9/L'},'finalize':True,'amendment_reason':'V12 process test restore normal count'})
st,x=act('Laboratory / Phlebotomy','save_lab',lab['id'],ld);check('normal-anc-restored-versioned',st==200,x);st,mo=boot('Medical Oncology');rid=one(mo,'readiness')['id'];st,x=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Proceed as Planned','sign':True});check('proceed-clears-hold',st==200,x)

# IPD infrastructure: inpatient order blocked without admission, then allowed after governed admission.
seed=one(mo,'treatment_order');doses={i['code']:i['ordered_dose'] for i in seed['data']['items']};rounding={i['code']:'No rounding' for i in seed['data']['items']}; reasons={i['code']:'' for i in seed['data']['items']}
st,x=act('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','cycle':2,'day':1,'administration_setting':'Inpatient','doses':doses,'rounding':rounding,'variance_reasons':reasons});check('ipd-order-blocked-without-admission',st==409 and 'admission' in x.get('error','').lower(),x)
st,mo=boot('Medical Oncology');adm=one(mo,'admission');episode=one(mo,'cancer_episode')
st,x=act('Medical Oncology','admit_patient',adm['id'],{'episode_id':episode['id'],'admission_type':'Planned','reason_code':'Treatment / procedure','admitting_specialty':'Medical Oncology','attending_clinician':'Medical Oncology User','ward':'Oncology Ward','bed':'ONC-01','source_context':'Planned inpatient systemic therapy'});check('ipd-admission-created',st==200 and x['admission']['episode_id']==episode['id'],x);admid=x['admission']['id']
st,x=act('Medical Oncology','create_order','',{'template_id':'REG-CCA-TCHP-DEMO','cycle':2,'day':1,'administration_setting':'Inpatient','doses':doses,'rounding':rounding,'variance_reasons':reasons});check('inpatient-systemic-order-created',st==200,x);ioid=x.get('order_id');iphid=x.get('pharmacy_id');iinfid=x.get('infusion_id')
# pharmacy same chain
st,x=act('Oncology Pharmacy','pharmacy_decision',iphid,{'decision':'Verified','verification_checks':checks});check('ipd-pharmacy-same-verification-chain',st==200,x)
st,phb=boot('Oncology Pharmacy');iph=next(z for z in phb['entities']['pharmacy'] if z['id']==iphid);prep=[]
for n,it in enumerate(iph['data']['items'],1):
 fi=fmap[it['drug']];form=fi['formulations'][0];z=dict(it);z.update({'formulation':form['label'],'formulation_strength_mg':form['strength_mg'],'batch':f'IPD-{n:02d}','expiry':expiry,'prepared_by':'Oncology Pharmacist A','prep_start':'12:00','prep_finish':'12:15','actual_volume_ml':it.get('volume_ml') or 0,'waste':'0','barcode':f'IPDBC{n}'});prep.append(z)
st,x=act('Oncology Pharmacy','pharmacy_prepare',iphid,{'items':prep});check('ipd-pharmacy-preparation',st==200,x);release=[{**z,'second_check_by':'Oncology Pharmacist B','label_verified':True} for z in prep]
st,x=act('Oncology Pharmacy','pharmacy_release',iphid,{'items':release,'dispensed_to':'Inpatient Oncology Ward','manifest_no':'IPD-MAN'});check('ipd-release-to-ward',st==200,x)
# Day Care nurse cannot administer inpatient; IPD nurse can.
st,x=act('Day Care / Infusion Nurse','start_infusion',iinfid,start);check('daycare-cannot-administer-inpatient-order',st==403,x)
st,inpb=boot('Inpatient Oncology Nurse');p=inpb['patient'];istart={**start,'identity_confirmation':{'name':p['name'],'mrn':p['mrn'],'dob':p['dob']},'access':'Central line — patent'}
st,x=act('Inpatient Oncology Nurse','start_infusion',iinfid,istart);check('inpatient-nurse-starts-same-mar-chain',st==200,x)
# observation + toxicity then MAR
ipd=one(inpb,'inpatient_care');st,x=act('Inpatient Oncology Nurse','record_inpatient_observation',ipd['id'],{'type':'Nursing observation','vitals':{'bp':'116/72','hr':84,'rr':18,'temp':37.0,'spo2':98},'pain_score':2,'intake_ml':500,'output_ml':350,'note':'Stable on ward'});check('ipd-nursing-observation',st==200,x)
st,x=act('Inpatient Oncology Nurse','record_inpatient_toxicity',ipd['id'],{'term':'Nausea','grade':'2','attribution':'Probably related','outcome':'Ongoing','intervention':'Antiemetic'});check('ipd-toxicity-recorded',st==200,x)
st,mob=boot('Medical Oncology');ipdmo=one(mob,'inpatient_care');st,x=act('Medical Oncology','inpatient_specialty_review',ipdmo['id'],{'assessment':'Reviewed during inpatient systemic treatment','plan':'Continue monitoring and protocol care'});check('cross-specialty-ipd-review',st==200,x)
io=next(z for z in mob['entities']['treatment_order'] if z['id']==ioid)
for n,it in enumerate(io['data']['items'],1):
 r={'item_id':it['item_id'],'actual_dose':it['ordered_dose'],'unit':it['ordered_unit'],'access':'Central line','start_time':f'{13+n:02d}:00','end_time':f'{13+n:02d}:20','actual_rate':it.get('rate_ml_hr',0),'completion_status':'Administered','reaction':'None','variance_note':''}
 if it.get('group') in ['Antineoplastic','Targeted Therapy']:r['chairside_verification']={'verified_by':'Inpatient Oncology RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
 st,x=act('Inpatient Oncology Nurse','administer_item',iinfid,{'record':r})
 if st!=200:break
check('inpatient-mar-all-items',st==200,x)
st,x=act('Inpatient Oncology Nurse','complete_infusion',iinfid,{'post_vitals':{'bp':'118/74','hr':82,'rr':16,'temp':36.9,'spo2':99},'tolerance':'Good','discharge_instructions':'Continue ward monitoring'});check('inpatient-treatment-completed',st==200,x)
# Toxicity feeds readiness automatically.
st,mob=boot('Medical Oncology');rid=one(mob,'readiness')['id'];st,x=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Proceed as Planned','sign':False});st,mob=boot('Medical Oncology');rr=one(mob,'readiness');check('ipd-toxicity-feeds-readiness',st==200 and 'Nausea G2' in rr['data'].get('toxicity_summary',''),rr['data'].get('toxicity_summary'))
# discharge + same episode + appointment continuity
st,x=act('Medical Oncology','discharge_patient',one(mob,'discharge')['id'],{'admission_id':admid,'discharge_diagnosis':'Completed planned inpatient treatment','hospital_course':'Treatment administered with ward monitoring.','medications':'Continue reconciled medications','follow_up':'Medical Oncology follow-up','treatment_delay_reason':'','next_cycle':str(date.today()+timedelta(days=21)),'next_care_stage':'Medical Oncology'});check('ipd-discharge-summary',st==200 and x['summary']['episode_id']==episode['id'],x)
st,mob=boot('Medical Oncology');aps=one(mob,'appointments')['data'].get('items',[]);check('discharge-to-opd-continuity-appointment',any(a.get('source_discharge_id')==x['summary']['id'] for a in aps),aps[-1] if aps else None)
# Readmission must same episode.
st,x=act('Medical Oncology','admit_patient',one(mob,'admission')['id'],{'episode_id':episode['id'],'admission_type':'Unplanned','reason_code':'Treatment toxicity','ward':'Oncology Ward','bed':'ONC-02','source_context':'Readmission'});check('readmission-same-cancer-episode',st==200 and x['admission']['episode_id']==episode['id'],x)
# discharge it so future DayCare escalation can create emergency admission
st,mob=boot('Medical Oncology');active=[a for a in one(mob,'admission')['data']['admissions'] if a['status']=='Active'][-1]
st,_=act('Medical Oncology','discharge_patient',one(mob,'discharge')['id'],{'admission_id':active['id'],'discharge_diagnosis':'Treatment toxicity improved','hospital_course':'Observed and improved.','medications':'Continue as instructed','follow_up':'Oncology review','next_care_stage':'Medical Oncology'})
check('readmission-discharge',st==200)

# Continuous/non-cyclical therapy supports open-ended course.
st,x=act('Medical Oncology','create_continuous_therapy',one(mob,'continuous_therapy')['id'],{'therapy':'Synthetic oral targeted therapy — process test','mode':'Oral systemic therapy','drug':'Synthetic oral agent','route':'PO','schedule':'Once daily','start_date':str(date.today()),'end_date':None,'intent':'Palliative','monitoring_plan':'Periodic clinical/laboratory assessment','episode_id':episode['id']});check('continuous-therapy-no-end-date',st==200 and x['course']['end_date'] is None and x['course'].get('day_care_required') is False and x['course'].get('compounding_required') is False,x)

# Treatment-plan phase cancellation/amendment preserves the prior version.
st,mob=boot('Medical Oncology');tp=one(mob,'treatment_plan');phases=tp['data'].get('phases',[]);idx=next((i for i,p in enumerate(phases) if p.get('modality')=='Radiation'),len(phases)-1)
st,x=act('Medical Oncology','amend_treatment_phase',tp['id'],{'phase_index':idx,'operation':'cancel','reason':'Synthetic process test — patient declined planned phase'});check('phase-cancellation-creates-new-plan-version',st==200 and x.get('supersedes')==tp['id'] and x.get('new_phase',{}).get('status')=='Cancelled',x)
st,mob=boot('Medical Oncology');plans=mob['entities']['treatment_plan'];check('prior-treatment-plan-preserved-after-phase-cancel',any(p['id']==tp['id'] for p in plans) and any(p['data'].get('supersedes')==tp['id'] for p in plans),[(p['id'],p['data'].get('supersedes'),p['status']) for p in plans[-3:]])

# Second cancer episode remains distinct.
st,x=act('Medical Oncology','create_cancer_episode','',{'kind':'New primary cancer','label':'Synthetic second primary colon cancer','started_at':str(date.today())});ep2=x.get('id');check('second-cancer-episode-created',st==200 and ep2 and ep2!=episode['id'],x)
st,mob=boot('Medical Oncology');eps=mob['entities']['cancer_episode'];check('two-cancer-episodes-preserved',len(eps)>=2 and len({e['id'] for e in eps})>=2,[(e['id'],e['data'].get('label')) for e in eps])
st,x=act('Medical Oncology','create_continuous_therapy',one(mob,'continuous_therapy')['id'],{'therapy':'Synthetic second-episode endocrine course','mode':'Hormonal therapy','drug':'Synthetic endocrine agent','route':'PO','schedule':'Continuous','start_date':str(date.today()),'end_date':None,'intent':'Adjuvant','episode_id':ep2});check('second-episode-treatment-stays-episode-scoped',st==200 and x['course']['episode_id']==ep2 and x['course']['day_care_required'] is False,x)

# RT interruption: sign/QA and record delivered then missed/rescheduled without corrupting cumulative dose.
st,rb=boot('Radiation Oncology');rt=one(rb,'radiation');rx=rt['data']['prescription'];
if rx.get('status')!='RT Oncologist Approved': st,_=act('Radiation Oncology','rt_save_prescription',rt['id'],{**rx,'sign':True})
st,_=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':1,'simulation_status':'Completed','contouring_status':'Completed','planning_status':'Planning Complete','status':'Planning'})
st,_=act('Radiation Physicist','rt_planning_status',rt['id'],{'plan_version':1,'physics_qa':'Approved','physics_qa_note':'V12 process QA'})
st,_=act('Radiation Oncology','rt_planning_status',rt['id'],{'plan_version':1,'physician_final_approval':'Approved','status':'Ready for Treatment'})
st,x=act('Radiation Technologist','rt_deliver_fraction',rt['id'],{'fraction_number':1,'status':'Delivered','delivered_dose_gy':rx.get('dose_per_fraction_gy',2),'image_guidance_performed':True});check('rt-fraction-delivered',st==200,x)
st,x=act('Radiation Technologist','rt_deliver_fraction',rt['id'],{'fraction_number':2,'status':'Missed','reason':'Hospital admission'});check('rt-missed-fraction-recorded-zero-dose',st==200,x)
st,x=act('Radiation Technologist','rt_deliver_fraction',rt['id'],{'fraction_number':2,'status':'Rescheduled','reason':'Return after admission','rescheduled_to':str(date.today()+timedelta(days=6))});check('rt-reschedule-recorded',st==200,x)
st,rb=boot('Radiation Oncology');fr=one(rb,'radiation')['data']['fractions'];cum=sum(float(z.get('delivered_dose_gy',0)) for z in fr);check('rt-cumulative-dose-excludes-missed-rescheduled',abs(cum-float(rx.get('dose_per_fraction_gy',2)))<1e-9,cum)

# Journey reflects process milestones and remains major-stage oriented.
st,mob=boot('Medical Oncology');jev=one(mob,'journey')['data']['events'];check('journey-updated-across-opd-ipd-treatment',any(x['department']=='Inpatient Care' for x in jev) and any('Cycle Completed' in x['care_stage'] for x in jev) and len(jev)<80,[(x['department'],x['care_stage']) for x in jev[-10:]])
# audit
st,a=http('/api/audit/verify',token=T['Hospital Management / Admin']);check('audit-chain-v12',st==200 and a.get('ok') is True,a)
print(f'\nRESULT {len(P)} PASS {len(F)} FAIL')
if F:
 for x in F:print('FAILED',x)
 sys.exit(1)
