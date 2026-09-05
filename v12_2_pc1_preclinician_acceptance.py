#!/usr/bin/env python3
import json, os, urllib.request, urllib.error, urllib.parse
from datetime import date
from pathlib import Path

BASE=os.environ.get('CCA_BASE','http://127.0.0.1:9088')
PIN=os.environ.get('CCA_DEMO_PIN','2026')
PID='PAT-0001'
ROOT=Path(__file__).resolve().parent
TOK={}; RESULTS=[]

def http(path,method='GET',data=None,token=None):
    h={'Content-Type':'application/json'}
    if token:h['Authorization']='Bearer '+token
    body=json.dumps(data).encode() if data is not None else None
    req=urllib.request.Request(BASE+path,data=body,headers=h,method=method)
    try:
        with urllib.request.urlopen(req,timeout=10) as r:
            raw=r.read(); ct=r.headers.get('Content-Type','')
            if 'json' in ct:return r.status,json.loads(raw.decode()) if raw else {}
            return r.status,raw.decode(errors='replace')
    except urllib.error.HTTPError as e:
        raw=e.read()
        try:j=json.loads(raw.decode()) if raw else {}
        except:j={'raw':raw.decode(errors='replace')}
        return e.code,j

def login(role):
    if role in TOK:return TOK[role]
    st,j=http('/api/login','POST',{'role':role,'pin':PIN})
    if st!=200:raise RuntimeError((role,st,j))
    TOK[role]=j['token'];return TOK[role]

def boot(role='Medical Oncology'):
    return http('/api/bootstrap?patient='+urllib.parse.quote(PID),token=login(role))

def action(role,a,eid='',d=None):
    return http('/api/action','POST',{'action':a,'patient_id':PID,'entity_id':eid,'data':d or {}},login(role))

def check(cid,cond,evidence):
    RESULTS.append({'id':cid,'pass':bool(cond),'evidence':evidence})
    print(('PASS' if cond else 'FAIL'),cid,json.dumps(evidence,ensure_ascii=False)[:700])

def data_of(t): return t.get('data',{})

# API + package content
st,content=http('/api/content',token=login('Hospital Management / Admin'))
templates=content.get('templates',[]) if st==200 else []
regs=[x for x in templates if x.get('category')=='Regimen' and x.get('source_id')=='SRC-CCA-QA']
rts=[x for x in templates if x.get('category')=='Radiation Template' and x.get('source_id')=='SRC-CCA-QA']
surg=[x for x in templates if x.get('category')=='Surgical Template' and x.get('source_id')=='SRC-CCA-QA']
cont=[x for x in templates if x.get('category')=='Continuous Therapy Template' and x.get('source_id')=='SRC-CCA-QA']

# 1 — regimen-specific readiness-rule architecture
r0=data_of(regs[0]) if regs else {}
rr=r0.get('readiness_rule_schema',{})
check('PC1-01-READINESS-ARCH', bool(regs) and isinstance(rr,list) and len(rr)>=5 and {'Hematology','Renal','Hepatic'}.issubset({x.get('category') for x in rr}),
      {'regimens':len(regs),'rule_categories':sorted({x.get('category') for x in rr}) if isinstance(rr,list) else []})

# 2 — first-class sequence sections
sections=r0.get('sequence_sections',[]); groups={str(i.get('group','')).lower() for i in r0.get('items',[])}
check('PC1-02-TREATMENT-SEQUENCE', bool(sections) and any('pre' in str(x).lower() for x in sections) and any('anti' in str(x).lower() for x in sections) and any('post' in str(x).lower() for x in sections),
      {'sequence_sections':sections,'source_groups':sorted(groups)})

# 3 — structured dose modification tables
mods=r0.get('dose_modification_rules',[])
check('PC1-03-DOSE-MODIFICATION', len(mods)>=4 and all('domain' in x and 'action_options' in x for x in mods),
      {'count':len(mods),'domains':[x.get('domain') for x in mods]})

# 4 — monitoring/investigation requirements
mon=r0.get('monitoring_requirements',[])
check('PC1-04-MONITORING', len(mon)>=4 and all('phase' in x and 'category' in x and 'requirement' in x for x in mon),
      {'count':len(mon),'categories':[x.get('category') for x in mon]})

# 5 — RT planned versus delivered
rt0=data_of(rts[0]) if rts else {}; pd=rt0.get('planned_delivered_schema',{})
check('PC1-05-RT-PLANNED-DELIVERED', bool(rts) and {'planned','delivered'}.issubset(pd.keys()) and bool(pd.get('planned')) and bool(pd.get('delivered')),
      {'rt_templates':len(rts),'planned_fields':pd.get('planned',[]),'delivered_fields':pd.get('delivered',[])})

# 6 — RT approval/physics/version chain
chain=rt0.get('approval_chain',[])
check('PC1-06-RT-APPROVAL-CHAIN', len(chain)>=5 and any('Physics' in str(x) for x in chain) and any('RO' in str(x) or 'Oncologist' in str(x) for x in chain),
      {'approval_chain':chain})

# 7 — disease-specific configurable surgical templates
scopes=[data_of(x).get('template_scope') for x in surg]
diseases=[x.get('disease') for x in surg]
check('PC1-07-SURGICAL-SUBTEMPLATES', len(surg)>=10 and len(set(diseases))>=10 and all(scopes),
      {'templates':len(surg),'unique_diseases':len(set(diseases)),'sample':diseases[:6]})

# 8 — surgical plan separated from operative record
s0=data_of(surg[0]) if surg else {}; op=s0.get('operative_record_fields',[])
check('PC1-08-PLAN-VS-OPERATIVE', bool(s0.get('plan_and_outcome_separation')) and len(op)>=8,
      {'separation':s0.get('plan_and_outcome_separation'),'operative_fields':op})

# 9 — rich infusion-reaction record frontend fields
pc1=(ROOT/'static'/'pc1.js').read_text(encoding='utf-8')
reaction_markers=['Reaction onset time','Severity','CTCAE grade','Infusion stopped?','Clinician contacted?','Rechallenge','Restart rate','Outcome']
check('PC1-09-INFUSION-REACTION', all(x.lower() in pc1.lower() for x in reaction_markers),
      {'required_markers':reaction_markers})

# 10 — stronger oral/continuous therapy schema + actual state transition persistence
c0=data_of(cont[0]) if cont else {}; wf=c0.get('workflow_fields',[]); sm=c0.get('state_machine',[])
st,b=boot('Medical Oncology'); cent=(b.get('entities',{}).get('continuous_therapy') or [{}])[-1] if st==200 else {}
create_data={
 'therapy':'Synthetic PC1 oral workflow acceptance','mode':'Oral systemic therapy','drug':'Synthetic PC1 oral agent',
 'dose':'100','dose_unit':'mg','frequency':'Once daily','route':'PO','schedule':'Continuous / protocol-defined',
 'food_instructions':'Synthetic QA instruction','start_date':str(date.today()),'dispense_quantity':'30',
 'refill_interval_days':30,'monitoring_plan':'Synthetic scheduled monitoring','required_labs':['CBC','Renal function'],
 'patient_education':'Synthetic education record','missed_dose_instructions':'Synthetic missed-dose rule',
 'adherence_plan':'Review at each visit','next_review':str(date.today()),'intent':'Synthetic QA'
}
st1,j1=action('Medical Oncology','create_continuous_therapy',cent.get('id',''),create_data)
cid=j1.get('course',{}).get('id') if st1==200 else ''
st2,j2=action('Medical Oncology','update_continuous_therapy',cent.get('id',''),{'course_id':cid,'status':'Held','reason':'Synthetic PC1 acceptance hold','adherence_status':'Reviewed','toxicity_review':'Synthetic toxicity review'}) if cid else (0,{})
course=j2.get('course',{}) if st2==200 else {}
check('PC1-10-ORAL-CONTINUOUS', len(wf)>=10 and len(sm)>=5 and st1==200 and st2==200 and course.get('status')=='Held' and len(course.get('state_history',[]))>=2,
      {'template_fields':len(wf),'states':sm,'create_http':st1,'update_http':st2,'status':course.get('status'),'history':len(course.get('state_history',[]))})

# 11 — pharmacy stability/compatibility structure
syn=json.loads((ROOT/'clinical_content'/'synthetic_institutional_test_content.json').read_text())
phis=[x.get('pharmacy_handling',{}) for x in syn.get('formulary_items',[])]
needed={'compatibility','stability','beyond_use_time','storage','light_protection','filter_requirement','container_requirement'}
check('PC1-11-PHARMACY-HANDLING', bool(phis) and all(needed.issubset(set(x.keys())) for x in phis),
      {'items':len(phis),'fields':sorted(needed)})

# 12 — clinician-facing masking of synthetic clinical values
mask_markers=['Clinician Review Mode','CCA-approved value required','clinical-mask','Product Test Mode']
check('PC1-12-CLINICIAN-MASK', all(x.lower() in pc1.lower() for x in mask_markers),
      {'markers':mask_markers})

# 13 — NEXUS frontend shell only, with explicit non-execution language
nexus_markers=['RUN NEXUS','Current Guideline Position','Applicable Options','Missing Information','Why NEXUS Reached This Position','no NCCN engine']
check('PC1-13-NEXUS-FRONTEND-ONLY', all(x.lower() in pc1.lower() for x in nexus_markers),
      {'markers':nexus_markers})

# 14 — richer clinician summary and CCA event-level journey remain represented
summary_markers=['Oncology Patient Summary','Readiness','Pending investigations','MDT / plan','Recommendation']
check('PC1-14-CLINICIAN-SUMMARY', all(x.lower() in pc1.lower() for x in summary_markers),
      {'markers':summary_markers})

# 15 — no browser-facing JS syntax defect in layered frontend (external command checked by release runner too)
stjs,js=http('/static/pc1.js')
check('PC1-15-PC1-ASSET-SERVED', stjs==200 and 'V.nexus' in js and 'V.radiation' in js and 'V.surgery' in js,
      {'http':stjs,'bytes':len(js) if isinstance(js,str) else 0})

fails=[x for x in RESULTS if not x['pass']]
print(f"RESULT {len(RESULTS)-len(fails)} PASS {len(fails)} FAIL")
if fails:
    print('FAILED',','.join(x['id'] for x in fails));raise SystemExit(1)
