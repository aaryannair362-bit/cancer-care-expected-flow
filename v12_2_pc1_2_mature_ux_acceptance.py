#!/usr/bin/env python3
from pathlib import Path
import os, urllib.request, sys
ROOT=Path(__file__).resolve().parent
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765')
pc=(ROOT/'static/pc1_2.js').read_text(); css=(ROOT/'static/styles.css').read_text(); idx=(ROOT/'static/index.html').read_text()
R=[]
def ck(i,ok,d=''):
 R.append((i,bool(ok),d)); print(('PASS' if ok else 'FAIL'),i,d)
ck('PC12-01-WORKFLOW-STEPPER',all(x in pc for x in ['Assessment','Investigations','MDT','Treatment Plan','Treatment Order','Readiness','Response']))
ck('PC12-02-CLEAN-INVESTIGATION-ORDERING',all(x in pc for x in ['Order Laboratory Test','Order Imaging','clinical indication','Ordered investigations']))
ck('PC12-03-MULTIDISCIPLINARY-PLAN',all(x in pc for x in ['Multidisciplinary Treatment Plan Builder','Medical oncologist','Radiation oncologist','Surgical oncologist','care_team']))
ck('PC12-04-PLAN-MODALITIES',all(x in pc for x in ['Systemic Therapy','Radiation','Surgery','Select at least one treatment modality']))
ck('PC12-05-MED-ONC-ORDER-HEADER',all(x in pc for x in ['Cancer / site','Intent / line','Regimen / version','Cycle / day','Weight / Height / BSA']))
ck('PC12-06-SEQUENCED-TREATMENT', 'pre-treatment → anti-cancer treatment → post-treatment' in pc.lower() and 'pc1TreatmentSequence' in pc)
ck('PC12-07-READINESS-DOMAINS',all(x in pc for x in ['Hematology','Renal','Hepatic','Cardiac','Toxicity','Required investigations','Drug/regimen-specific']))
ck('PC12-08-PHARMACY-WORKFLOW',all(x in pc for x in ['Verification Pending','Query Raised','Verified','Prepared','Dispensed','Compatibility / stability']))
ck('PC12-09-DAYCARE-REACTION',all(x in pc for x in ['Infusion Reaction Event','CTCAE grade','Rechallenge','restart','toxicity timeline']))
ck('PC12-10-ORAL-CONTINUOUS',all(x in pc for x in ['Separate non-infusion therapy workflow','Food instructions','Dispense quantity','Missed-dose instructions','Adherence plan']))
ck('PC12-11-RT-PLANNED-DELIVERED',all(x in pc for x in ['Planned course','fractions delivered','Physics review','RO final approval','Delivered fractions']))
ck('PC12-12-SURGERY-PLAN-VS-ACTUAL',all(x in pc for x in ['Before surgery','After surgery','Operative record','Pathology → adjuvant planning']))
ck('PC12-13-CLINICIAN-MASK',all(x in pc for x in ['CCA-approved dose/fractionation required','clinical-mask']))
ck('PC12-14-NEXUS-FRONTEND-PRESERVED','nexus' in pc.lower() and 'NEXUS' in (ROOT/'static/pc1.js').read_text())
ck('PC12-15-CLEAN-NAV',all(x in pc for x in ['Patient care','Libraries & admin','PC12_PRIMARY']))
ck('PC12-16-NO-RAW-JSON','JSON.stringify' not in pc)
ck('PC12-17-RESPONSIVE-DESIGN',all(x in css for x in ['.care-path','.order-type-grid','.readiness-groups','.surgery-columns','@media(max-width:700px)']))
ck('PC12-18-ASSET-REFERENCED','/static/pc1_2.js' in idx and ('V12.2-PC1.2' in idx or '/static/pc1_3.js' in idx))
try:
 body=urllib.request.urlopen(BASE+'/static/pc1_2.js',timeout=5).read().decode()
 ck('PC12-19-ASSET-SERVED','Mature Oncology UX' in body and len(body)>30000,str(len(body)))
except Exception as e: ck('PC12-19-ASSET-SERVED',False,str(e))
print('RESULT',sum(x[1] for x in R),'PASS',sum(not x[1] for x in R),'FAIL')
sys.exit(1 if any(not x[1] for x in R) else 0)
