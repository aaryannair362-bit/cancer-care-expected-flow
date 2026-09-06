#!/usr/bin/env python3
import os,json,urllib.request,urllib.error,datetime,sys
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765')
PIN='2026';PASS=0;FAIL=0;DETAIL=[]
def req(path,method='GET',data=None,token=''):
 b=json.dumps(data).encode() if data is not None else None
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 r=urllib.request.Request(BASE+path,data=b,headers=h,method=method)
 try:
  with urllib.request.urlopen(r,timeout=10) as z:return z.status,json.loads(z.read().decode() or '{}')
 except urllib.error.HTTPError as e:
  try:x=json.loads(e.read().decode() or '{}')
  except:x={'error':str(e)}
  return e.code,x
def login(role):
 st,j=req('/api/login','POST',{'role':role,'pin':PIN});
 if st!=200:raise RuntimeError(f'login {role} {st} {j}')
 return j['token']
def check(name,ok,detail=''):
 global PASS,FAIL
 if ok:PASS+=1;print('PASS',name)
 else:FAIL+=1;print('FAIL',name,detail)
 DETAIL.append({'name':name,'pass':bool(ok),'detail':str(detail)})
def synth_field(f):
 if f.get('readonly') or f.get('type')=='readonly':return None
 typ=f.get('type');opts=f.get('options') or []
 label=(f.get('label') or '').lower()
 if typ=='select':return opts[0] if opts else 'Synthetic option'
 if typ=='multiselect':return [opts[0]] if opts else ['Synthetic option']
 if typ=='number':
  if 'height' in label:return 170
  if label=='weight' or 'weight today' in label:return 70
  if 'fraction' in label:return 5
  if 'dose' in label:return 10
  if 'nodes examined' in label:return 10
  if 'nodes positive' in label:return 1
  return 1
 if typ=='date':return datetime.date.today().isoformat()
 if typ=='datetime-local':return datetime.datetime.now().replace(microsecond=0).isoformat(timespec='minutes')
 if typ=='time':return '10:00'
 if 'final diagnosis' in label:return 'Synthetic oncology pathology diagnosis for product testing only'
 if 'clinician-confirmed response' in label:return 'Stable disease'
 return 'Synthetic QA value'
def synth_values(s):
 v={}
 for f in s.get('fields') or []:
  z=synth_field(f)
  if z is not None:v[f['id']]=z
 for t in s.get('tables') or []:
  # One synthetic row exercises every table column; required or not.
  row={}
  for c in t.get('columns') or []:
   z=synth_field(c)
   if z is not None:row[c['id']]=z
  v['table__'+t['id']]=[row] if row else []
 return v

def main():
 st,h=req('/api/health');check('PC4-001-health-build',st==200 and 'PC4.0' in h.get('product',''),h)
 admin=login('Hospital Management / Admin');st,cat=req('/api/pc4/screens',token=admin)
 # Admin only sees assigned admin screens, so load canonical catalog from local file for exhaustive list.
 local=json.load(open(os.path.join(os.path.dirname(__file__),'clinical_content','pc4_screen_catalog.json'),encoding='utf-8'))
 screens=local['screens']
 check('PC4-002-246-screen-catalog',len(screens)==246,len(screens))
 check('PC4-003-26-modules',local.get('module_count')==26,local.get('module_count'))
 check('PC4-004-202-forms-44-worklists',local.get('form_count')==202 and local.get('worklist_count')==44,(local.get('form_count'),local.get('worklist_count')))
 check('PC4-005-all-screens-have-role-visibility',all(s.get('roles') for s in screens))
 check('PC4-006-all-forms-have-author-role-or-are-explicit-view',all(s.get('author_roles') is not None for s in screens if s.get('kind')=='form'))
 check('PC4-007-atomic-field-coverage',local.get('field_requirement_count',0)>=4000,local.get('field_requirement_count'))
 # Role visibility for every screen, using one listed visible role.
 visible_fail=[]
 role_tokens={};role_visible={}
 for role in sorted({(s.get('roles') or [''])[0] for s in screens if s.get('roles')}):
  try:
   role_tokens[role]=login(role);st,j=req('/api/pc4/screens',token=role_tokens[role]);role_visible[role]={x['id'] for x in j.get('screens',[])} if st==200 else set()
  except Exception as ex:role_visible[role]=set();visible_fail.append((role,str(ex)))
 for s in screens:
  role=(s.get('roles') or [None])[0]
  if not role:visible_fail.append((s['id'],'no role'));continue
  if s['id'] not in role_visible.get(role,set()):visible_fail.append((s['id'],role))
 check('PC4-008-owning-role-visibility-246',not visible_fail,visible_fail[:10])
 # Exhaustive authoring round-trip for every authorable form.
 forms=[s for s in screens if s.get('kind')=='form' and s.get('author_roles')]
 create_fail=[];signed=[];field_count=0
 for i,s in enumerate(forms):
  role=s['author_roles'][0]
  if role not in role_tokens:role_tokens[role]=login(role)
  vals=synth_values(s);field_count+=sum(1 for f in s.get('fields',[]) if not f.get('readonly'))+sum(sum(1 for c in t.get('columns',[]) if not c.get('readonly')) for t in s.get('tables',[]))
  pid='' if s.get('module_code')=='C.26' else 'PAT-0001'
  st,j=req('/api/pc4/record','POST',{'op':'create','screen_id':s['id'],'patient_id':pid,'values':vals},role_tokens[role])
  if st!=201:create_fail.append((s['id'],'create',st,j));continue
  r=j['record'];
  st,j=req('/api/pc4/record','POST',{'op':'update','screen_id':s['id'],'patient_id':pid,'record_id':r['id'],'expected_version':r['version'],'values':vals},role_tokens[role])
  if st!=200:create_fail.append((s['id'],'update',st,j));continue
  r=j['record'];st,j=req('/api/pc4/record','POST',{'op':'sign','screen_id':s['id'],'patient_id':pid,'record_id':r['id'],'expected_version':r['version'],'values':vals,'attestation':'Synthetic QA sign-off only'},role_tokens[role])
  if st!=200:create_fail.append((s['id'],'sign',st,j));continue
  signed.append((s,j['record'],role,pid,vals))
 check('PC4-009-all-authorable-forms-create-update-sign',not create_fail,create_fail[:15])
 check('PC4-010-executable-field-table-roundtrip',field_count>=2500,field_count)
 # Signed record immutable through update operation.
 if signed:
  s,r,role,pid,vals=signed[0];st,j=req('/api/pc4/record','POST',{'op':'update','screen_id':s['id'],'patient_id':pid,'record_id':r['id'],'expected_version':r['version'],'values':vals},role_tokens[role]);check('PC4-011-signed-record-update-blocked',st==409,(st,j))
  st,j=req('/api/pc4/record','POST',{'op':'amend','screen_id':s['id'],'patient_id':pid,'record_id':r['id'],'expected_version':r['version'],'values':vals,'reason':'Synthetic QA amendment'},role_tokens[role]);check('PC4-012-amendment-creates-new-draft',st==201 and j.get('record',{}).get('status')=='Draft',(st,j))
 # RBAC: Admin cannot author a Surgical Oncology clinical record.
 surg=next(x for x in screens if x['id']=='SCR-SO-002');st,j=req('/api/pc4/record','POST',{'op':'create','screen_id':surg['id'],'patient_id':'PAT-0001','values':synth_values(surg)},admin);check('PC4-013-admin-clinical-authoring-rejected',st==403,(st,j))
 # View-but-not-author: Pharmacy can view dosing panel but must not author it.
 pharm=role_tokens.get('Oncology Pharmacy') or login('Oncology Pharmacy');ord2=next(x for x in screens if x['id']=='SCR-ORD-002');st,j=req('/api/pc4/screens',token=pharm);vis=ord2['id'] in {x['id'] for x in j.get('screens',[])};st2,j2=req('/api/pc4/record','POST',{'op':'create','screen_id':ord2['id'],'patient_id':'PAT-0001','values':synth_values(ord2)},pharm);check('PC4-014-view-without-authoring-enforced',vis and st2==403,(vis,st2,j2))
 # BSA/BMI calculation on intake master.
 intake=next(x for x in screens if x['id']=='SCR-INT-002');tok=role_tokens.get('Intake Nurse') or login('Intake Nurse');vals=synth_values(intake)
 for f in intake['fields']:
  if f['label']=='Weight':vals[f['id']]=70
  if f['label']=='Height':vals[f['id']]=170
 st,j=req('/api/pc4/record','POST',{'op':'create','screen_id':intake['id'],'patient_id':'PAT-0001','values':vals},tok);dv=j.get('record',{}).get('data',{}).get('derived_values',{}) if st==201 else {};check('PC4-015-bmi-bsa-derived',st==201 and abs(dv.get('bmi_kg_m2',0)-24.22)<0.01 and abs(dv.get('bsa_m2',0)-1.818)<0.002,(st,dv))
 # NEXUS must not expose a server reasoning endpoint in PC4.
 st,j=req('/api/nexus/evaluate',token=role_tokens.get('Medical Oncology') or login('Medical Oncology'));check('PC4-016-nexus-backend-deferred',st==404,(st,j))
 # Full audit chain remains internally coherent.
 st,j=req('/api/audit/verify',token=admin);check('PC4-017-audit-chain-integrity',st==200 and j.get('ok') is True,j)
 # Source boundaries are explicit rather than falsely claiming recovered prose.
 b=local.get('source_boundary',{});check('PC4-018-source-boundary-explicit','C.1-C.18' in b and 'C.19-C.26' in b,b)
 # Clinical content masters are software structures but institutional values remain configured/approved.
 adm5=next(x for x in screens if x['id']=='SCR-ADM-005');check('PC4-019-configurable-clinical-master-structure',len(adm5.get('tables',[]))>=4 and any('CCA Approved' in (f.get('options') or []) for f in adm5['fields']),adm5.get('tables'))
 out={'suite':'V12.2-PC4.0 PRD Conformance','pass':PASS,'fail':FAIL,'details':DETAIL,'screens':len(screens),'forms_exercised':len(forms),'editable_atomic_requirements_exercised':field_count,'generated_at':datetime.datetime.now().isoformat()}
 open(os.path.join(os.path.dirname(__file__),'validation_evidence','V12_2_PC4_0_PRD_CONFORMANCE_RESULTS.json'),'w',encoding='utf-8').write(json.dumps(out,indent=2,ensure_ascii=False))
 print(f'\nRESULT: {PASS} PASS / {FAIL} FAIL; forms exercised {len(forms)}; editable atomic requirements {field_count}')
 return 1 if FAIL else 0
if __name__=='__main__':sys.exit(main())
