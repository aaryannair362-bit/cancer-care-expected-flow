#!/usr/bin/env python3
from pathlib import Path
import urllib.request, os, sys
ROOT=Path(__file__).resolve().parent
BASE=os.environ.get('CCA_BASE','http://127.0.0.1:8765')
app=(ROOT/'static/app.js').read_text(); pc=(ROOT/'static/pc1.js').read_text(); css=(ROOT/'static/styles.css').read_text(); idx=(ROOT/'static/index.html').read_text()
R=[]
def check(i,ok,d=''):
    R.append((i,bool(ok),d)); print(('PASS' if ok else 'FAIL'),i,d)
check('UX-01-NO-RAW-TEMPLATE-JSON', 'Structured template data' not in app+pc and 'JSON.stringify(d,null,2)' not in app+pc)
check('UX-02-HUMAN-TEMPLATE-RENDERERS', all(x in pc for x in ['renderTemplateHuman','Prescription structure','Surgical plan','Operative record — captured separately','Therapy structure']))
check('UX-03-ROLE-FOCUSED-NAV', all(x in pc for x in ['PC11_PRIMARY','Clinical workspace','More tools']) and '.nav-more' in css)
check('UX-04-SUMMARY-NEXT-STEP', all(x in pc for x in ['Current cancer state','What happens next','pc11NextStep','Treatment readiness']))
check('UX-05-REPORT-HUMAN-VIEW', 'renderHumanObject(sec.data)' in pc and 'Download JSON' not in pc[-25000:])
check('UX-06-READINESS-HUMAN-VIEW', 'renderReadinessResult' in pc and 'Treatment Readiness Preview' in pc)
check('UX-07-CLINICIAN-MASK-PRESERVED', all(x in pc for x in ['Clinician Review Mode','clinical-mask','CCA-approved value required']))
check('UX-08-PC11-ASSETS', '/static/pc1.js' in idx and 'clinician ux remediation' in css.lower() and 'V12.2-PC1.' in idx)
try:
    body=urllib.request.urlopen(BASE+'/static/pc1.js',timeout=5).read().decode()
    check('UX-09-ASSET-SERVED', 'PC1.1' in body and len(body)>80000, str(len(body)))
except Exception as e: check('UX-09-ASSET-SERVED',False,str(e))
fail=[x for x in R if not x[1]]
print(f'RESULT {len(R)-len(fail)} PASS {len(fail)} FAIL')
sys.exit(1 if fail else 0)
