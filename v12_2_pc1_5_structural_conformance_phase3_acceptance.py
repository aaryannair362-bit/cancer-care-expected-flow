#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.error, urllib.parse
from pathlib import Path
from datetime import date, timedelta

ROOT=Path(__file__).resolve().parent
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9115')
PIN=os.environ.get('CCA_DEMO_PIN','2026')
PID='PAT-0001'
OUT=[]

def http(path,method='GET',data=None,token=None):
    h={'Content-Type':'application/json'}; body=json.dumps(data).encode() if data is not None else None
    if token: h['Authorization']='Bearer '+token
    req=urllib.request.Request(BASE+path,data=body,headers=h,method=method)
    try:
        with urllib.request.urlopen(req,timeout=10) as r:
            raw=r.read(); return r.status, json.loads(raw.decode()) if raw else {}
    except urllib.error.HTTPError as e:
        raw=e.read()
        try: j=json.loads(raw.decode()) if raw else {}
        except: j={'raw':raw.decode(errors='replace')}
        return e.code,j

def login(role):
    st,j=http('/api/login','POST',{'role':role,'pin':PIN}); assert st==200,(role,st,j); return j['token']

ROLES=['Nurse Navigator','Medical Oncology','Oncology Pharmacy','Day Care / Infusion Nurse','Hospital Management / Admin']
T={r:login(r) for r in ROLES}

def boot(role): return http('/api/bootstrap?patient='+PID,token=T[role])
def latest(role,etype):
    st,b=boot(role); assert st==200,(role,st,b)
    return b['entities'][etype][-1]

def chk(i,ok,d=''):
    OUT.append({'id':i,'pass':bool(ok),'detail':d})
    print(('PASS' if ok else 'FAIL'),i,json.dumps(d,ensure_ascii=False,default=str)[:1400] if d!='' else '')

def act(role,a,eid='',d=None):
    payload={'action':a,'patient_id':PID,'entity_id':eid,'data':dict(d or {})}
    optimistic={'save_intake':'intake','med_recon':'med_recon','save_treatment_plan':'treatment_plan'}
    if a in optimistic:
        st,b=boot(role)
        if st==200:
            xs=b.get('entities',{}).get(optimistic[a],[])
            target=next((x for x in xs if not eid or x['id']==eid),xs[-1] if xs else None)
            if target: payload['expected_version']=target['version']
    return http('/api/action','POST',payload,T[role])

# --- A. Current medications: governed formulary picker, explicit dose/route/frequency/status/source ---
med=latest('Nurse Navigator','med_recon'); mid=med['id']
st,j=act('Nurse Navigator','med_recon',mid,{'operation':'add_medication','formulary_id':'FREE-TEXT-DRUG','route':'PO','dose_value':5,'dose_unit':'mg','frequency':'Once daily','status':'Continue','source':'Patient'})
chk('PC15-MED-001',st==409 and 'formulary' in j.get('error','').lower(),{'status':st,'body':j})

st,meta=http('/api/meta',token=T['Nurse Navigator']); mm=meta.get('medication_master',[])
fi=next((x for x in mm if x.get('allowed_routes')),None)
chk('PC15-MED-002',bool(fi and fi.get('id') and fi.get('drug')),{'selected':fi})

bad_route='IV' if 'IV' not in fi.get('allowed_routes',[]) else 'PO'
st,j=act('Nurse Navigator','med_recon',mid,{'operation':'add_medication','formulary_id':fi['id'],'route':bad_route,'dose_value':5,'dose_unit':'mg','frequency':'Once daily','status':'Continue','source':'Patient'})
chk('PC15-MED-003',st==409 and 'route' in j.get('error','').lower(),{'status':st,'body':j})

route=fi['allowed_routes'][0]
st,j=act('Nurse Navigator','med_recon',mid,{'operation':'add_medication','formulary_id':fi['id'],'route':route,'dose_value':5,'frequency':'Once daily','status':'Continue','source':'Patient'})
chk('PC15-MED-004',st==409 and 'dose' in j.get('error','').lower(),{'status':st,'body':j})

st,j=act('Nurse Navigator','med_recon',mid,{'operation':'add_medication','formulary_id':fi['id'],'route':route,'dose_value':5,'dose_unit':'mg','frequency':'Once daily','status':'Continue','source':'Patient'})
chk('PC15-MED-005',st==200,{'status':st,'body':j})
med=latest('Nurse Navigator','med_recon'); saved=med['data']['items'][-1]
chk('PC15-MED-006',all(saved.get(k) not in [None,''] for k in ['formulary_id','drug','code','code_system','dose_value','dose_unit','route','frequency','status','source','entered_by','entered_at']),saved)

st,j=act('Nurse Navigator','med_recon',mid,{'operation':'reconcile','reconciliation_status':'Complete','source':'Patient','reason':'PC1.5 structured reconciliation after governed medication selection'})
chk('PC15-MED-007',st==200 and j.get('reconciliation_status')=='Complete',{'status':st,'body':j})

# --- B. Readiness provenance, freshness, monitoring, signed human rationale ---
ready=latest('Medical Oncology','readiness'); rid=ready['id']
st,j=act('Medical Oncology','preview_readiness','',{'template_id':'REG-CCA-TCHP-DEMO'})
rules=j.get('rule_results',[]) if st==200 else []
chk('PC15-RDY-001',st==200 and len(rules)>=6 and all(x.get('source_record_id') for x in rules if x.get('id')!='RR-TOX'),{'status':st,'rules':rules})
chk('PC15-RDY-002',st==200 and all(x.get('outcome') in ['PASS','REVIEW','HOLD','DOSE MODIFY','OMIT','DISCONTINUE'] for x in rules),{'outcomes':[x.get('outcome') for x in rules]})
chk('PC15-RDY-003',st==200 and any(x.get('freshness_status')=='Current' for x in rules) and any(x.get('id')=='RR-AGE' for x in rules),{'freshness':[(x.get('id'),x.get('freshness_status'),x.get('freshness_days')) for x in rules]})
chk('PC15-RDY-004',st==200 and len(j.get('monitoring_requirements',[]))>=4 and all(x.get('status') in ['Required','Completed','Overdue','Abnormal','Missing'] for x in j.get('monitoring_requirements',[])),j.get('monitoring_requirements',[]))

st,j=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Proceed as Planned','sign':True})
chk('PC15-RDY-005',st==409 and 'reason' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Medical Oncology','save_readiness',rid,{'template_id':'REG-CCA-TCHP-DEMO','decision':'Proceed as Planned','decision_reason':'Current regimen-specific results, freshness and toxicity review support treatment in this synthetic QA case','sign':True})
chk('PC15-RDY-006',st==200 and j.get('status')=='Signed',{'status':st,'body':j})
ready=latest('Medical Oncology','readiness')
chk('PC15-RDY-007',bool(ready['data'].get('decision_reason') and ready['data'].get('readiness_attestation') and ready['data'].get('signed_by') and ready['data'].get('signed_at')),{'decision_reason':ready['data'].get('decision_reason'),'signed_by':ready['data'].get('signed_by')})

# --- C. Systemic order: governed route/diluent/rate/rounding + explicit treatment blocks ---
plan=latest('Medical Oncology','treatment_plan')
base={'template_id':'REG-CCA-TCHP-DEMO','plan_id':plan['id'],'administration_setting':'Day Care','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'Synthetic QA','cycle':2,'day':1,'start_date':str(date.today()),'doses':{'DEMO-CARBO':600},'variance_reasons':{'DEMO-CARBO':'Synthetic patient-specific AUC dose'},'dose_decision_reasons':{'*':'Clinician accepts final ordered dose after review','DEMO-CARBO':'Clinician accepts patient-specific AUC dose'},'administration_decision_reason':'Clinician accepts route, diluent, volume, rate and duration parameters after review','schedule_decision_reason':'Clinician accepts cycle/day treatment date after review'}

st,j=act('Oncology Pharmacy','create_order','',base)
chk('PC15-ORD-000',st==403 and 'Medical Oncology' in j.get('error',''),{'status':st,'body':j})

bad={**base,'administration_parameters':{'DEMO-PER':{'route':'PO'}}}
st,j=act('Medical Oncology','create_order','',bad)
chk('PC15-ORD-001',st==409 and 'route' in j.get('error','').lower(),{'status':st,'body':j})
bad={**base,'administration_parameters':{'DEMO-PER':{'route':'IV','diluent':'D5W','volume_ml':250,'duration_min':60,'rate_ml_hr':250}}}
st,j=act('Medical Oncology','create_order','',bad)
chk('PC15-ORD-002',st==409 and 'diluent' in j.get('error','').lower(),{'status':st,'body':j})
bad={**base,'administration_parameters':{'DEMO-PER':{'route':'IV','diluent':'NS','volume_ml':250,'duration_min':60,'rate_ml_hr':999}}}
st,j=act('Medical Oncology','create_order','',bad)
chk('PC15-ORD-003',st==409 and 'rate' in j.get('error','').lower(),{'status':st,'body':j})
bad={**base,'rounding':{'DEMO-PER':'Nearest 10 mg'}}
st,j=act('Medical Oncology','create_order','',bad)
chk('PC15-ORD-004',st==409 and 'rounding' in j.get('error','').lower(),{'status':st,'body':j})

st,j=act('Medical Oncology','create_order','',base); oid=j.get('order_id'); phid=j.get('pharmacy_id'); infid=j.get('infusion_id')
chk('PC15-ORD-005',st==200 and oid and phid and infid,{'status':st,'body':j})
order=next(x for x in boot('Medical Oncology')[1]['entities']['treatment_order'] if x['id']==oid)
items=sorted(order['data']['items'],key=lambda x:x['sequence'])
chk('PC15-ORD-006',[x['sequence'] for x in items]==sorted({x['sequence'] for x in items}) and len({x['sequence'] for x in items})==len(items),[(x['sequence'],x['drug']) for x in items])
chk('PC15-ORD-007',set(x.get('treatment_block') for x in items)=={'Pre-treatment','Anti-cancer treatment','Post-treatment / supportive'},[(x['drug'],x.get('treatment_block')) for x in items])
chk('PC15-ORD-008',all(x.get('route') and x.get('dose_decision_reason') and x.get('administration_parameter_decision_reason') and x.get('schedule_decision_reason') for x in items),[(x['drug'],x.get('route'),x.get('dose_decision_reason')) for x in items])
chk('PC15-ORD-009',all((x.get('route')!='IV') or (float(x.get('volume_ml') or 0)>0 and float(x.get('duration_min') or 0)>0 and float(x.get('rate_ml_hr') or 0)>0) for x in items),[(x['drug'],x.get('volume_ml'),x.get('duration_min'),x.get('rate_ml_hr')) for x in items])
chk('PC15-ORD-010',isinstance(order['data'].get('cumulative_dose_ledger_before_order'),dict) and all('cumulative_dose_before' in x for x in items),order['data'].get('cumulative_dose_ledger_before_order'))

# --- D. Pharmacy: complete verification, server-owned prep content/BUD/concentration, independent final check ---
checks={k:True for k in ['patient_identity','allergy','regimen_version','cycle_day','dose_basis','calculated_dose','ordered_dose','dose_variance','renal_adjustment','hepatic_adjustment','cumulative_dose','interaction','duplication','route','diluent','final_concentration','stock','expiry']}
st,j=act('Oncology Pharmacy','pharmacy_decision',phid,{'decision':'Verified','verification_checks':checks})
chk('PC15-PHM-001',st==200 and j.get('status')=='Preparation Pending',{'status':st,'body':j})
ph=next(x for x in boot('Oncology Pharmacy')[1]['entities']['pharmacy'] if x['id']==phid)
snap=ph['data'].get('verification_snapshot',{})
chk('PC15-PHM-002',all(k in snap for k in ['order_id','order_version','protocol_id','protocol_version','cycle','day','readiness_id','readiness_signed_at','readiness_decision','cumulative_dose_ledger','patient_snapshot']),snap)

st,fm=http('/api/formulary',token=T['Oncology Pharmacy']); fmap={x['drug']:x for x in fm.get('items',[]) if x.get('status')=='Active'}
prep=[]
for n,it in enumerate(ph['data']['items'],1):
    fi=fmap[it['drug']]; form=fi['formulations'][0]; x=dict(it)
    x.update({'formulation':form['label'],'formulation_strength_mg':form.get('strength_mg',0),'batch':f'PC15-{n}','expiry':str(date.today()+timedelta(days=60)),'actual_volume_ml':it.get('volume_ml') or 0,'actual_volume_unit':'mL','compatibility_status':'MALICIOUS CLIENT OVERRIDE','stability_reference':'MALICIOUS CLIENT OVERRIDE','beyond_use_at':'2099-01-01T00:00:00+00:00','storage_condition':'MALICIOUS CLIENT OVERRIDE','filter_requirement':'MALICIOUS CLIENT OVERRIDE','container_requirement':'MALICIOUS CLIENT OVERRIDE','final_concentration':9999})
    prep.append(x)
waste_probe=[dict(x) for x in prep]
iv_probe=next((x for x in waste_probe if x.get('route')=='IV'),waste_probe[0])
iv_probe.update({'wastage_amount':1,'wastage_unit':'mg','wastage_reason':''})
st,j=act('Oncology Pharmacy','pharmacy_prepare',phid,{'items':waste_probe,'preparation_note':'PC1.5 wastage reason negative test'})
chk('PC15-PHM-003A',st==409 and 'wastage' in j.get('error','').lower(),{'status':st,'body':j})
# Now document the governed wastage reason and complete the preparation.
for x in prep:
    if x.get('item_id')==iv_probe.get('item_id'): x.update({'wastage_amount':1,'wastage_unit':'mg','wastage_reason':'Partial vial'})
st,j=act('Oncology Pharmacy','pharmacy_prepare',phid,{'items':prep,'preparation_note':'PC1.5 governed Pharmacy preparation test'})
chk('PC15-PHM-003',st==200 and j.get('status')=='Dispensing Pending',{'status':st,'body':j})
ph=next(x for x in boot('Oncology Pharmacy')[1]['entities']['pharmacy'] if x['id']==phid); prepared=ph['data']['items']
chk('PC15-PHM-004',all(x.get('compatibility_status')!='MALICIOUS CLIENT OVERRIDE' and x.get('stability_reference')!='MALICIOUS CLIENT OVERRIDE' and x.get('beyond_use_at')!='2099-01-01T00:00:00+00:00' and x.get('final_concentration')!=9999 for x in prepared),[(x['drug'],x.get('compatibility_status'),x.get('stability_reference'),x.get('beyond_use_at')) for x in prepared])
chk('PC15-PHM-005',all(x.get('pharmacy_content_status','').startswith('Synthetic QA') and x.get('prepared_by',{}).get('role')=='Oncology Pharmacy' for x in prepared),[(x['drug'],x.get('prepared_by'),x.get('pharmacy_content_status')) for x in prepared])
ivs=[x for x in prepared if x.get('route')=='IV']
chk('PC15-PHM-006',bool(ivs) and all(x.get('final_concentration') is not None and x.get('final_concentration_unit')=='mg/mL' for x in ivs),[(x['drug'],x.get('final_concentration'),x.get('final_concentration_unit')) for x in ivs])

same=[]
for x in prepared:
    pb=x.get('prepared_by') or {}; same.append({'item_id':x['item_id'],'second_check_by':pb.get('name'),'label_verified':True})
st,j=act('Oncology Pharmacy','pharmacy_release',phid,{'items':same,'dispensed_to':'Day Care / Infusion'})
chk('PC15-PHM-007',st==409 and 'preparer' in j.get('error','').lower(),{'status':st,'body':j})
release=[{'item_id':x['item_id'],'second_check_by':'Independent Oncology Pharmacist B','label_verified':True,'beyond_use_at':'2099-12-31T00:00:00+00:00','final_concentration':9999} for x in prepared]
st,j=act('Oncology Pharmacy','pharmacy_release',phid,{'items':release})
chk('PC15-PHM-007A',st==409 and 'destination' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Oncology Pharmacy','pharmacy_release',phid,{'items':release,'dispensed_to':'Day Care / Infusion','manifest_no':'PC15-MAN-1'})
chk('PC15-PHM-008',st==200 and j.get('status')=='Dispensed',{'status':st,'body':j})
ph=next(x for x in boot('Oncology Pharmacy')[1]['entities']['pharmacy'] if x['id']==phid); released=ph['data']['items']
chk('PC15-PHM-009',all(x.get('second_check_by')=='Independent Oncology Pharmacist B' and x.get('second_check_attestation') and x.get('beyond_use_at')!='2099-12-31T00:00:00+00:00' and x.get('final_concentration')!=9999 for x in released),[(x['drug'],x.get('beyond_use_at'),x.get('final_concentration'),x.get('second_check_by')) for x in released])

# --- E. Day Care / MAR: governed access, independent check, variance reason, post-vital units, cumulative administered-dose ledger ---
p=boot('Day Care / Infusion Nurse')[1]['patient']
start_base={'checklist':{k:True for k in ['identity','order','consent','allergy','vitals','labs','access','pharmacy']},'identity_confirmation':{'name':p['name'],'mrn':p['mrn'],'dob':p['dob']},'pre_vitals':{'bp':'118/74','hr':78,'rr':16,'temp':36.7,'spo2':99,'units':{'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'}},'bedside_verification':{'confirmed':True,'verified_by':'Independent Oncology RN B'}}
st,j=act('Day Care / Infusion Nurse','start_infusion',infid,{**start_base,'access':'PICC'})
chk('PC15-MAR-001',st==409 and 'access' in j.get('error','').lower(),{'status':st,'body':j})
st,j=act('Day Care / Infusion Nurse','start_infusion',infid,{**start_base,'access':{'type':'PICC','site':'Right upper limb','detail':'Right PICC patent'}})
chk('PC15-MAR-002',st==200,{'status':st,'body':j})

# First item full administration (premed, no independent chairside requirement).
first=items[0]
r={'item_id':first['item_id'],'actual_dose':first['ordered_dose'],'actual_dose_unit':first['ordered_unit'],'start_time':'10:00','end_time':'10:10','completion_status':'Administered','reaction':'None','variance_type':'None'}
if first.get('route')=='IV' or float(first.get('rate_ml_hr') or 0)>0: r.update({'actual_rate':first.get('rate_ml_hr'),'actual_rate_unit':'mL/h'})
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':r}); chk('PC15-MAR-003',st==200,{'status':st,'body':j})

second=items[1]
def mar_record(it,dose=None):
    rr={'item_id':it['item_id'],'actual_dose':it['ordered_dose'] if dose is None else dose,'actual_dose_unit':it['ordered_unit'],'start_time':'10:15','end_time':'11:15','completion_status':'Administered','reaction':'None','variance_type':'None'}
    if it.get('route')=='IV' or float(it.get('rate_ml_hr') or 0)>0: rr.update({'actual_rate':it.get('rate_ml_hr'),'actual_rate_unit':'mL/h'})
    return rr
r=mar_record(second)
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':r}); chk('PC15-MAR-004',st==409 and 'chairside' in j.get('error','').lower(),{'status':st,'body':j})
st_meta,dc_meta=http('/api/meta',token=T['Day Care / Infusion Nurse']); same_nurse=dc_meta.get('actor',{}).get('name')

r['chairside_verification']={'verified_by':same_nurse,'checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':r}); chk('PC15-MAR-005',st==409 and 'separately named' in j.get('error','').lower(),{'status':st,'body':j})
r['chairside_verification']['verified_by']='Independent Oncology RN B'
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':r}); chk('PC15-MAR-006',st==200,{'status':st,'body':j})

third=items[2]; half=round(float(third['ordered_dose'])/2,4); r=mar_record(third,half);r.update({'completion_status':'Partially Administered','variance_type':'Dose variance','variance_note':'Synthetic partial dose for variance workflow test','chairside_verification':{'verified_by':'Independent Oncology RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}})
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':r}); chk('PC15-MAR-007',st==409 and 'reason code' in j.get('error','').lower(),{'status':st,'body':j})
r['variance_reason_code']='Clinician instruction'
st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':r}); chk('PC15-MAR-008',st==200,{'status':st,'body':j})

# Complete remaining sequence normally.
for n,it in enumerate(items[3:],4):
    rr=mar_record(it);rr['start_time']=f'{9+n:02d}:00';rr['end_time']=f'{9+n:02d}:45'
    if it.get('group') in ['Antineoplastic','Targeted Therapy']:
        rr['chairside_verification']={'verified_by':'Independent Oncology RN B','checks':{k:True for k in ['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings']}}
    st,j=act('Day Care / Infusion Nurse','administer_item',infid,{'record':rr})
    chk(f'PC15-MAR-{n+5:03d}',st==200,{'drug':it['drug'],'status':st,'body':j})

post={'bp':'120/76','hr':80,'rr':16,'temp':36.8,'spo2':99}
st,j=act('Day Care / Infusion Nurse','complete_infusion',infid,{'post_vitals':post,'tolerance':'Good','discharge_instructions':'Synthetic PC1.5 instructions'})
chk('PC15-MAR-014',st==409 and 'unit' in j.get('error','').lower(),{'status':st,'body':j})
post['units']={'bp':'mmHg','hr':'/min','rr':'/min','temp':'°C','spo2':'%'}
st,j=act('Day Care / Infusion Nurse','complete_infusion',infid,{'post_vitals':post,'tolerance':'Good','discharge_instructions':'Synthetic PC1.5 instructions'})
chk('PC15-MAR-015',st==200 and isinstance(j.get('cumulative_dose_ledger_after'),dict),{'status':st,'body':j})
ledger=j.get('cumulative_dose_ledger_after',{})
chk('PC15-MAR-016',abs(float(ledger.get(third['code'],0))-half)<1e-6,{'code':third['code'],'expected_partial':half,'ledger':ledger})

# --- F. Frontend structural markers ---
pc=(ROOT/'static/pc1_5.js').read_text(); idx=(ROOT/'static/index.html').read_text()
markers=['Governed current-medication list:','Administration-parameter decision reason','Criterion provenance / freshness / proposed outcome','Independent verification snapshot','server loads the governed Pharmacy content','Independent chairside verifier','Post-Treatment Closure']
for q,m in enumerate(markers,1): chk(f'PC15-UI-{q:03d}',m in pc,{'marker':m})
chk('PC15-UI-008','/static/pc1_5.js' in idx and 'V12.2-PC1.5' in idx,{'index_asset':True})

summary={'suite':'V12.2-PC1.5 Structural Conformance Phase 3','total':len(OUT),'passed':sum(x['pass'] for x in OUT),'failed':sum(not x['pass'] for x in OUT),'results':OUT}
(ROOT/'V12_2_PC1_5_TRACK_B_PHASE3_RUN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
print(json.dumps({k:summary[k] for k in ['total','passed','failed']},indent=2))
sys.exit(1 if summary['failed'] else 0)
