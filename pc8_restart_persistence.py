#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download. Adapted: targets this repo's
# PAT-VAL-* validation patients (not the pre-existing PAT-DEMO-* showcase patients) and
# resolves credentials live from DEMO_USER_CREDENTIALS.txt via test_auth.py instead of
# hardcoding PINs, since this repo's ROLES ordering (and therefore generated PINs) differs
# from PC8.0's.
import json, urllib.request, urllib.error, sys, os, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_auth import creds_for_role
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765')
FULL_CASES=[
 ('PAT-VAL-ANANYA','Medical Oncology'),
 ('PAT-VAL-NEHA','Radiation Oncology'),
 ('PAT-VAL-ARJUN','Surgical Oncology'),
 ('PAT-VAL-RAVI','Inpatient Oncology Clinician'),
 ('PAT-VAL-LEELA','Medical Oncology'),
 ('PAT-VAL-LEELA','Nurse Navigator'),
]

def http(path,method='GET',data=None,token=None):
 h={'Content-Type':'application/json'}
 if token:h['Authorization']='Bearer '+token
 b=json.dumps(data).encode() if data is not None else None
 try:
  with urllib.request.urlopen(urllib.request.Request(BASE+path,data=b,headers=h,method=method),timeout=10) as r:return r.status,json.loads(r.read().decode() or '{}')
 except urllib.error.HTTPError as e:
  try:j=json.loads(e.read().decode() or '{}')
  except:j={}
  return e.code,j

def login(u,p):
 st,j=http('/api/login','POST',{'username':u,'pin':p})
 if st!=200:raise RuntimeError((u,st,j))
 return j['token']

def _accessible(pid,role):
 # Only include cases the owning role currently has patient access to (i.e. that journey
 # has been run at least far enough to receive a referral/task). Run each pc8_*_execute.py
 # first to extend coverage; this keeps the check runnable incrementally rather than
 # requiring all 5 journeys to be driven through first.
 try:
  u,p=creds_for_role(role);tok=login(u,p);st,_=http('/api/bootstrap?patient='+pid,token=tok);return st==200
 except Exception:return False
CASES=[(pid,role) for pid,role in FULL_CASES if _accessible(pid,role)]

def snap():
 out={}
 tokens={}
 for pid,role in CASES:
  u,p=creds_for_role(role)
  tok=tokens.setdefault(u,login(u,p) if u not in tokens else tokens[u])
  st,b=http('/api/bootstrap?patient='+pid,token=tok)
  if st!=200:raise RuntimeError(('bootstrap',pid,u,st,b))
  st,t=http('/api/tasks?patient='+pid,token=tok)
  if st!=200:raise RuntimeError(('tasks',pid,u,st,t))
  ents={typ:[{'id':x['id'],'status':x['status'],'version':x['version']} for x in arr] for typ,arr in sorted((b.get('entities') or {}).items())}
  tasks=[{'id':x['id'],'task_type':x['task_type'],'status':x['status'],'source_type':x.get('source_type',''),'source_id':x.get('source_id',''),'episode_id':x.get('episode_id','')} for x in t.get('tasks',[])]
  tasks.sort(key=lambda x:(x['id']))
  key=pid+'|'+u
  out[key]={'patient':{'id':b['patient']['id'],'mrn':b['patient']['mrn'],'status':b['patient']['status']},'entities':ents,'tasks':tasks}
 return out

mode=sys.argv[1] if len(sys.argv)>1 else 'capture'
path=sys.argv[2] if len(sys.argv)>2 else 'validation_evidence/PC8_RESTART_BEFORE.json'
current=snap()
if mode=='capture':
 open(path,'w').write(json.dumps(current,indent=2,sort_keys=True))
 print(json.dumps({'ok':True,'cases':len(current),'path':path,'sha256':hashlib.sha256(json.dumps(current,sort_keys=True).encode()).hexdigest()},indent=2))
elif mode=='compare':
 before=json.load(open(path))
 ok=before==current
 diff=[]
 if not ok:
  for k in sorted(set(before)|set(current)):
   if before.get(k)!=current.get(k):diff.append(k)
 result={'ok':ok,'cases':len(current),'changed_cases':diff,'before_sha256':hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest(),'after_sha256':hashlib.sha256(json.dumps(current,sort_keys=True).encode()).hexdigest()}
 print(json.dumps(result,indent=2));sys.exit(0 if ok else 1)
else:raise SystemExit('capture|compare')
