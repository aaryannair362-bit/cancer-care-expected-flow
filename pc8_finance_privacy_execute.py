#!/usr/bin/env python3
# Ported from PC8.0 Connected Multidisciplinary download, targeting this repo's
# PAT-VAL-ANANYA validation patient (same "Ananya Shah" identity, distinct id/mrn from the
# pre-existing PAT-DEMO-CHEMO showcase patient). Adapted for this repo's actual
# fundraising_approve/fundraising_release model: production requires the SAME role
# ('Finance / Billing') to both draft and independently approve a letter, using individual
# named-user identity (not a shared role id) to prevent self-approval -- rather than routing
# approval through Hospital Management / Admin as the PC8.0 original assumed. The generator
# uses the named finance.demo account; the independent approver uses the legacy shared-role
# login (a different actor id for the same role), which production's server.py supports for
# exactly this kind of validation. Task/handoff wiring for the fundraising letter workflow
# was added to production's fundraising_letter/fundraising_approve/fundraising_release
# actions as part of this port so the "auto-created task" checks below hold.
import json, urllib.request, urllib.error, urllib.parse, pathlib, sys, os
from datetime import date, timedelta, datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parent;BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765');PID='PAT-VAL-ANANYA';rows=[];TOK={}
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
def login_legacy(role):
    # A second, distinct actor identity for the SAME role, via the legacy shared-role login
    # path (gated by CCA_ALLOW_SHARED_ROLE_LOGIN, on by default) -- used here purely to prove
    # independent-approval-by-a-different-person within one role.
    key='legacy:'+role
    if key not in TOK:
        st,j=http('/api/login','POST',{'role':role,'pin':os.environ.get('CCA_DEMO_PIN','2026')});assert st==200,(role,st,j);TOK[key]=j['token']
    return TOK[key]
def boot(role):
    st,j=http('/api/bootstrap?patient='+urllib.parse.quote(PID),token=login(role));assert st==200,(role,st,j);return j
def entity(role,typ):
    xs=boot(role).get('entities',{}).get(typ,[]);return xs[-1] if xs else None
def action(role,a,eid='',data=None,token=None):return http('/api/action','POST',{'action':a,'patient_id':PID,'entity_id':eid,'data':data or {}},token or login(role))
def tasks(role,token=None):
    st,j=http('/api/tasks?patient='+PID,token=token or login(role));assert st==200,(role,st,j);return j.get('tasks',[])
def task(role,typ,status='Open',token=None):
    for x in reversed(tasks(role,token)):
        if x.get('task_type')==typ and (not status or x.get('status')==status):return x
    return None
def source(role,tid,token=None):return http('/api/task-source?task='+urllib.parse.quote(tid),token=token or login(role))
def ck(name,ok,detail=None):
    rows.append({'check':name,'pass':bool(ok),'detail':detail});print(('PASS' if ok else 'FAIL'),name,json.dumps(detail,ensure_ascii=False,default=str)[:1300] if detail is not None else '')
    if not ok:raise AssertionError(name+' '+str(detail))

conv=entity('Finance / Billing','conversion');ck('FIN-001 conversion source available',bool(conv),{'id':conv and conv['id']})
st,j=action('Finance / Billing','finance_estimate',conv['id'],{});ck('FIN-002 dose-vial estimate calculated',st==200 and j.get('total',0)>0 and len(j.get('lines',[]))>0,j)
st,j=http('/api/finance/schemes',token=login('Finance / Billing'));ck('FIN-004 finance scheme master exposed',st==200 and any(x['id']=='SCH-PMJAY' for x in j.get('schemes',[])),j)
st,j=action('Finance / Billing','finance_scheme_assessment',conv['id'],{'scheme_id':'SCH-PMJAY','evidence':{'beneficiary_or_card_id':'SYN-PMJAY-001','supporting_evidence':'Synthetic eligibility document reference'}});ass=j.get('assessment',{});ck('FIN-005 PMJAY assessment non-definitive',st==200 and ass.get('definitive_eligibility') is False and 'external' in ass.get('result','').lower(),ass)
# identifiable draft must fail without disclosure consent
st,j=action('Finance / Billing','fundraising_letter',conv['id'],{'recipient':'Synthetic NGO','purpose':'Treatment support','redacted':False});ck('FIN-006 identifiable letter blocked without consent',st==409 and 'consent' in j.get('error','').lower(),j)
# redacted mode must reject custom free text that could reintroduce PII
st,j=action('Finance / Billing','fundraising_letter',conv['id'],{'recipient':'Synthetic NGO','purpose':'Treatment support','redacted':True,'text':'Ananya Shah CCA-SYN-VAL-CHEMO-01'});ck('FIN-007 redacted custom-PII injection blocked',st==409,j)
# server-generated redacted draft -> Finance approval task -> exact conversion source -> independent approval -> release
st,j=action('Finance / Billing','fundraising_letter',conv['id'],{'recipient':'Synthetic NGO','purpose':'Treatment support','redacted':True});letter=j.get('letter',{});ck('FIN-008 redacted server draft created',st==200 and letter.get('status')=='Draft — Approval Required' and 'Ananya Shah' not in letter.get('text','') and j.get('next_role')=='Finance / Billing',j)
at=task('Finance / Billing','External disclosure approval');ck('FIN-009 Finance approval task auto-created',bool(at),at)
st,src=source('Finance / Billing',at['id']);ck('FIN-010 Finance opens exact conversion source',st==200 and src.get('source_record_id')==conv['id'] and src.get('source_visible_to_role') is True,src)
# Production requires an active disclosure consent before ANY approval (redacted or not) --
# stricter than the original PC8.0 model, which only gated identifiable-letter creation.
cons=entity('Front Desk','consent');st,j=action('Front Desk','consent_action',cons['id'],{'operation':'sign','type':'External Financial Assistance Disclosure Consent','version':'CCA-PC8-FIN-1','scope':'Disclosure to synthetic financial-assistance recipient for validation only','signed_by':'Synthetic patient — Ananya Shah','valid_from':date.today().isoformat(),'valid_until':(date.today()+timedelta(days=30)).isoformat()});ck('FIN-017 disclosure consent signed',st==200,j)
st,j=action('Biller','fundraising_approve',conv['id'],{});ck('FIN-011 wrong role approval blocked',st==403,j)
st,j=action('Finance / Billing','fundraising_approve',conv['id'],{});ck('FIN-012 author self-approval blocked',st==409 and 'independent' in j.get('error','').lower(),j)
st,j=action('Finance / Billing','fundraising_approve',conv['id'],{},token=login_legacy('Finance / Billing'));ck('FIN-013 independent Finance approval succeeds',st==200 and j.get('letter',{}).get('status')=='Approved for Release' and j.get('next_role')=='Finance / Billing',j)
rt=task('Finance / Billing','External disclosure release');ck('FIN-014 Finance release task auto-created',bool(rt),rt)
st,src=source('Finance / Billing',rt['id']);ck('FIN-015 Finance opens exact approved conversion source',st==200 and src.get('source_record_id')==conv['id'] and src.get('source_record_status')=='Active',src)
st,j=action('Finance / Billing','fundraising_release',conv['id'],{});ck('FIN-016 redacted approved letter released',st==200 and j.get('letter',{}).get('status')=='Released',j)
st,j=action('Finance / Billing','fundraising_letter',conv['id'],{'recipient':'Synthetic NGO 2','purpose':'Treatment support','redacted':False});ck('FIN-018 identifiable draft allowed with consent',st==200 and j.get('letter',{}).get('redacted') is False and 'Ananya Shah' in j.get('letter',{}).get('text',''),j)
st,j=action('Finance / Billing','fundraising_approve',conv['id'],{},token=login_legacy('Finance / Billing'));ck('FIN-019 identifiable draft independently approved',st==200 and j.get('letter',{}).get('status')=='Approved for Release',j)
st,j=action('Finance / Billing','fundraising_release',conv['id'],{});ck('FIN-020 identifiable approved disclosure released',st==200 and j.get('letter',{}).get('status')=='Released',j)
# audit attribution visible via direct verify endpoint
st,av=http('/api/audit/verify',token=login('Hospital Management / Admin'));ck('FIN-023 audit chain remains valid',st==200 and av.get('ok') is True,av)
out={'patient':'Ananya Shah','patient_id':PID,'build':'12.2-PC8.0','generated_at':datetime.now(timezone.utc).isoformat(),'checks':len(rows),'pass':sum(x['pass'] for x in rows),'fail':sum(not x['pass'] for x in rows),'results':rows};(ROOT/'validation_evidence'/'PC8_FINANCE_PRIVACY_EXECUTION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False));print('SUMMARY',json.dumps({k:out[k] for k in ['checks','pass','fail']}));sys.exit(1 if out['fail'] else 0)
