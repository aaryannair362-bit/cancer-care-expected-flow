#!/usr/bin/env python3
import json, os, urllib.request, urllib.error, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9495'); PIN=os.environ.get('CCA_DEMO_PIN','2026'); OUT=[]
def http(path,method='GET',data=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 body=json.dumps(data).encode() if data is not None else None
 try:
  with urllib.request.urlopen(urllib.request.Request(BASE+path,data=body,headers=h,method=method),timeout=20) as r:return r.status,json.loads(r.read().decode() or '{}')
 except urllib.error.HTTPError as e:
  try:j=json.loads(e.read().decode() or '{}')
  except:j={}
  return e.code,j
def chk(i,ok,d=''):OUT.append({'id':i,'pass':bool(ok),'detail':d});print(('PASS' if ok else 'FAIL'),i,str(d)[:400])
def login(role):
 st,j=http('/api/login','POST',{'role':role,'pin':PIN});assert st==200,(st,j);return j['token']
MO=login('Medical Oncology'); FD=login('Front Desk'); ADM=login('Hospital Management / Admin')
st,j=http('/api/cca-validation/summary',token=MO);chk('CCA-VAL-001-summary-endpoint',st==200 and j.get('count',0)==0,j)
st,j=http('/api/cca-validation/feedback','POST',{'screen_id':'SCR-MO-002','patient_id':'PAT-0001','target_type':'Field','target_id':'assessment','target_label':'Assessment','dimension':'Field completeness','verdict':'Correct — Freeze','severity':'None','expected':'Assessment present','actual':'Assessment present','suggestion':''},MO);fid=j.get('id');chk('CCA-VAL-002-field-feedback',st==201 and fid,j)
st,j=http('/api/cca-validation/feedback?screen=SCR-MO-002',token=MO);chk('CCA-VAL-003-feedback-read',st==200 and j.get('count')==1 and j['feedback'][0]['target_type']=='Field',j)
st,j=http('/api/cca-validation/feedback','POST',{'screen_id':'SCR-MO-002','patient_id':'PAT-0001','target_type':'Screen','target_id':'SCR-MO-002','target_label':'Initial Oncology Consultation','dimension':'Overall screen / workflow','verdict':'Change Required','severity':'S2 — Major','expected':'Expected behavior','actual':'Actual observation','suggestion':'Required correction'},MO);chk('CCA-VAL-004-gap-feedback',st==201,j)
st,j=http('/api/cca-validation/feedback','POST',{'screen_id':'SCR-MO-002','patient_id':'PAT-0001','target_type':'Field','target_id':'x','target_label':'x','dimension':'Field completeness','verdict':'Missing','severity':'S2 — Major','expected':'','actual':'','suggestion':''},MO);chk('CCA-VAL-005-gap-requires-detail',st==409,j)
st,j=http('/api/cca-validation/feedback','POST',{'screen_id':'SCR-SO-009','patient_id':'PAT-0001','target_type':'Screen','target_id':'SCR-SO-009','target_label':'Detailed Operative Note','dimension':'Overall screen / workflow','verdict':'Correct — Freeze','severity':'None'},FD);chk('CCA-VAL-006-role-screen-guard',st==403,j)
st,j=http('/api/cca-validation/signoff','POST',{'specialty_role':'Medical Oncology','decision':'Accepted with required changes','what_to_freeze':'Correct items','required_changes':'Issue register items','content_needed':'CCA regimen master','integration_needed':'LIS/RIS'},MO);chk('CCA-VAL-007-specialty-signoff',st==201,j)
st,j=http('/api/cca-validation/signoff?specialty=Medical%20Oncology',token=MO);chk('CCA-VAL-008-signoff-read',st==200 and j.get('latest',{}).get('decision')=='Accepted with required changes',j)
st,j=http('/api/cca-validation/summary',token=MO);chk('CCA-VAL-009-summary-counts',st==200 and j.get('count')==2 and j.get('verdicts',{}).get('Correct — Freeze')==1 and j.get('severity',{}).get('S2 — Major')==1,j)
assets=(ROOT/'static'/'cca_validation.js').read_text(encoding='utf-8')+(ROOT/'static'/'pc4.js').read_text(encoding='utf-8')+(ROOT/'static'/'app.js').read_text(encoding='utf-8');chk('CCA-VAL-010-ui-instrumentation','CCA Validation Center' in assets and 'Validate this screen' in assets and 'data-cca-review' in assets)
pack=ROOT/'CCA_VALIDATION_PACK';chk('CCA-VAL-011-validation-pack',all((pack/x).exists() for x in ['CCA_Clinician_Stakeholder_Validation_Workbook.xlsx','07_SCREEN_BY_SCREEN_VALIDATION_MATRIX.csv','08_FIELD_BY_FIELD_VALIDATION_MATRIX.csv','11_IN_PRODUCT_VALIDATION_MODE.md']))
fail=[x for x in OUT if not x['pass']];res={'suite':'CCA Clinician Validation Mode','pass':len(OUT)-len(fail),'fail':len(fail),'details':OUT};(ROOT/'validation_evidence'/'CCA_VALIDATION_MODE_RESULTS.json').write_text(json.dumps(res,indent=2));print(json.dumps({'pass':len(OUT)-len(fail),'fail':len(fail)},indent=2));sys.exit(1 if fail else 0)
