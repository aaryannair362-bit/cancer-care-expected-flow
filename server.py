#!/usr/bin/env python3
import os, json, sqlite3, uuid, hashlib, hmac, secrets, base64, mimetypes, re, math, threading, traceback, sys
from difflib import SequenceMatcher
from datetime import datetime, timedelta, date
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from pc7_safety import *

ROOT=Path(__file__).resolve().parent

def _load_dotenv():
 p=ROOT/'.env'
 if not p.exists():return
 for line in p.read_text(encoding='utf-8').splitlines():
  line=line.strip()
  if not line or line.startswith('#') or '=' not in line:continue
  k,v=line.split('=',1);os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
_load_dotenv()

# CCA_DB_PATH selects the local sqlite file; it is ignored once TURSO_DATABASE_URL is set,
# since db() prefers the remote Turso store whenever that env var is present.
STATIC=ROOT/'static'; DB=Path(os.environ.get('CCA_DB_PATH',str(ROOT/'cca_v12.sqlite3')))
PORT=int(os.environ.get('PORT') or 8765)
HOST=os.environ.get('HOST','127.0.0.1')
# PC8.0 connected-multidisciplinary auth/deployment config. Individual named-user + PIN
# login (see seed_user_accounts) is now primary; the legacy shared role+PIN login used by
# the existing acceptance/regression suites keeps working by default (ALLOW_SHARED_ROLE_LOGIN
# defaults on) and is refused automatically if CCA_DEPLOYMENT_MODE=production.
DEMO_PIN=os.environ.get('CCA_DEMO_PIN','2026')
DEPLOYMENT_MODE=os.environ.get('CCA_DEPLOYMENT_MODE','validation').lower()
ALLOW_SHARED_ROLE_LOGIN=os.environ.get('CCA_ALLOW_SHARED_ROLE_LOGIN','1')=='1'
REQUEST_CTX=threading.local()
SESSION_HOURS=12

ROLES=['Front Desk','Patient Attender','PRE / Patient Relations Executive','Nurse Navigator','Intake Nurse','Medical Oncology','Surgical Oncology','Radiation Oncology','Radiology Coordinator','Radiology Technician','Radiologist','Laboratory / Phlebotomy','Pathology','MDT Coordinator','MDT Chair','External Consultant','Oncology Pharmacy','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Radiation Technologist','Radiation Physicist','Surgical Nurse','Biller','Finance / Billing','Patient Liaison','Hospital Management / Admin','Anaesthetist','Stoma / Wound Nurse','Blood Bank / Transfusion','Dietitian / Nutrition','Psycho-Oncology','Palliative Care','Clinical Trials / Research','Health Information Management','Radiation Dosimetrist / Planner','Pathology Technologist','Inpatient Oncology Clinician']
USERS={r:{'id':'USR-'+re.sub(r'[^A-Z]','',r.upper())[:8]+'-001','name':r if 'Oncology' not in r else r+' User','role':r} for r in ROLES}

READ={
'Front Desk':{'registration','consent','appointments','queue','journey','documents'},'Patient Attender':{'registration','consent','appointments','documents'},'PRE / Patient Relations Executive':{'registration','appointments','queue','lab_order','radiology_order','documents'},
'Nurse Navigator':{'registration','intake','med_recon','documents','appointments','queue','journey','diagnosis','care_plan','dynamic_forms','toxicity','cancer_episode','admission','inpatient_care','discharge'},
'Intake Nurse':{'registration','intake','med_recon','documents','appointments','queue','journey','diagnosis','care_plan','dynamic_forms','toxicity','cancer_episode','admission','inpatient_care','discharge'},
'Medical Oncology':{'registration','consent','intake','med_recon','documents','appointments','queue','journey','consultation','diagnosis','lab_order','lab','radiology_order','radiology','pathology','mdt','mdt_collab','mdt_followup','care_plan','treatment_plan','protocol_library','formulary','readiness','treatment_order','pharmacy','infusion','toxicity','modification','response','radiation','surgery','treatment_history','visit_summary','cancer_episode','admission','inpatient_care','discharge','continuous_therapy','tumor_marker'},
'Surgical Oncology':{'registration','intake','med_recon','documents','queue','journey','diagnosis','lab','radiology','pathology','mdt','care_plan','treatment_plan','treatment_order','surgery','response','treatment_history','toxicity','cancer_episode','admission','inpatient_care','discharge'},
'Radiation Oncology':{'registration','intake','med_recon','documents','queue','journey','diagnosis','lab','radiology','pathology','mdt','care_plan','treatment_plan','treatment_order','radiation','surgery','response','treatment_history','toxicity','cancer_episode','admission','inpatient_care','discharge','continuous_therapy'},
'Radiology Coordinator':{'registration','radiology_order','appointments','queue','documents'},'Radiology Technician':{'registration','radiology_order','documents'},'Radiologist':{'registration','diagnosis','radiology_order','radiology','response','documents'},
'Laboratory / Phlebotomy':{'registration','lab_order','lab','documents'},'Pathology':{'registration','pathology','documents','diagnosis','cancer_episode','treatment_history'},
'MDT Coordinator':{'registration','queue','journey','diagnosis','lab','radiology','pathology','mdt','mdt_collab','mdt_followup','care_plan','treatment_plan','documents','cancer_episode','treatment_history','toxicity','response','surgery'},
'MDT Chair':{'registration','queue','journey','diagnosis','lab','radiology','pathology','mdt','mdt_collab','mdt_followup','care_plan','treatment_plan','documents','cancer_episode','treatment_history','toxicity','response','surgery'},
'External Consultant':set(),
'Oncology Pharmacy':{'registration','intake','med_recon','diagnosis','lab','treatment_plan','readiness','treatment_order','pharmacy','protocol_library','formulary','documents','cancer_episode','admission','toxicity','treatment_history','infusion'},
'Day Care / Infusion Nurse':{'registration','intake','med_recon','diagnosis','lab','readiness','treatment_order','pharmacy','infusion','toxicity','consent','documents','cancer_episode','admission','treatment_history'},
'Inpatient Oncology Nurse':{'registration','intake','med_recon','diagnosis','lab','readiness','treatment_order','pharmacy','infusion','toxicity','consent','journey','cancer_episode','admission','inpatient_care','discharge','continuous_therapy'},
'Radiation Technologist':{'registration','radiation','admission'},'Radiation Physicist':{'registration','diagnosis','radiology','radiation','documents','admission'},'Surgical Nurse':{'registration','surgery','admission','inpatient_care'},
'Biller':{'registration','lab_order','radiology_order','finance'},'Finance / Billing':{'registration','lab_order','radiology_order','finance','conversion','treatment_plan','appointments','queue','journey'},
'Patient Liaison':{'registration','consent','appointments','queue','journey','care_plan','documents','discharge'},'Hospital Management / Admin':{'registration','appointments','queue','journey','finance','conversion','protocol_library','formulary','dynamic_forms','standards','cca_requirements','admission'} }

PAT_FIELDS={
'Front Desk':['id','mrn','name','dob','sex','phone','abha','current_department','status','photo_document_id'], 'Patient Attender':['id','mrn','name','dob','sex','phone','abha','current_department','status','photo_document_id'],
'PRE / Patient Relations Executive':['id','mrn','name','dob','sex','phone','current_department','status'], 'Biller':['id','mrn','name','dob','phone','current_department','status'], 'Finance / Billing':['id','mrn','name','dob','phone','current_department','status'],
'Laboratory / Phlebotomy':['id','mrn','name','dob','sex','current_department','status'], 'Radiology Coordinator':['id','mrn','name','dob','sex','phone','current_department','status'], 'Radiology Technician':['id','mrn','name','dob','sex','current_department','status'],
'Radiologist':['id','mrn','name','dob','sex','current_department','status'], 'Intake Nurse':['id','mrn','name','dob','sex','phone','current_department','status'], 'MDT Chair':['id','mrn','name','dob','sex','current_department','status'], 'Inpatient Oncology Nurse':['id','mrn','name','dob','sex','allergies','current_department','status'], 'Radiation Physicist':['id','mrn','name','dob','sex','current_department','status'], 'Oncology Pharmacy':['id','mrn','name','dob','sex','allergies','current_department','status'], 'Day Care / Infusion Nurse':['id','mrn','name','dob','sex','allergies','current_department','status'], 'Hospital Management / Admin':['id','mrn','current_department','status']}

# PC4.0 minimum-necessary patient projections for newly introduced PRD roles.
_PC4_CLIN_PAT=['id','mrn','name','dob','sex','allergies','current_department','status']
_PC4_OPS_PAT=['id','mrn','name','dob','sex','current_department','status']
for _r in ['Anaesthetist','Stoma / Wound Nurse','Dietitian / Nutrition','Psycho-Oncology','Palliative Care','Clinical Trials / Research','Radiation Dosimetrist / Planner','Pathology Technologist','Inpatient Oncology Clinician']:
 PAT_FIELDS.setdefault(_r,list(_PC4_CLIN_PAT))
for _r in ['Blood Bank / Transfusion','Health Information Management']:
 PAT_FIELDS.setdefault(_r,list(_PC4_OPS_PAT))

WRITE={
'registration':{'Front Desk','Patient Attender'},'consent':{'Front Desk','Patient Attender','Patient Liaison'},'appointments':{'Front Desk','Patient Attender','PRE / Patient Relations Executive','Radiology Coordinator','Finance / Billing'},'queue':{'Front Desk','PRE / Patient Relations Executive','Nurse Navigator','Radiology Coordinator','Laboratory / Phlebotomy','Finance / Billing','Oncology Pharmacy','Day Care / Infusion Nurse','MDT Coordinator'},
'intake':{'Nurse Navigator','Intake Nurse'},'med_recon':{'Nurse Navigator','Intake Nurse','Medical Oncology'},'dynamic_forms':{'Hospital Management / Admin','Nurse Navigator'},'consultation':{'Medical Oncology'},'diagnosis':{'Medical Oncology','Surgical Oncology','Radiation Oncology'},
'lab_order':{'Medical Oncology'},'radiology_order':{'Medical Oncology'},'lab':{'Laboratory / Phlebotomy'},'radiology':{'Radiologist','Radiology Technician'},'pathology':{'Pathology'},'mdt':{'MDT Coordinator','MDT Chair','Medical Oncology','Surgical Oncology','Radiation Oncology'},'mdt_collab':{'MDT Coordinator','MDT Chair','Medical Oncology','Surgical Oncology','Radiation Oncology'},'mdt_followup':{'MDT Coordinator','MDT Chair'},
'journey':{'Front Desk','Patient Attender','PRE / Patient Relations Executive','Nurse Navigator','Intake Nurse','Medical Oncology','Surgical Oncology','Radiation Oncology','MDT Coordinator','Oncology Pharmacy','Day Care / Infusion Nurse'},'cancer_episode':{'Medical Oncology','Surgical Oncology','Radiation Oncology'},'admission':{'Medical Oncology','Surgical Oncology','Radiation Oncology','Day Care / Infusion Nurse'},'inpatient_care':{'Nurse Navigator','Medical Oncology','Surgical Oncology','Radiation Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Surgical Nurse'},'discharge':{'Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator'},'continuous_therapy':{'Medical Oncology'},'tumor_marker':{'Medical Oncology','Laboratory / Phlebotomy'},'care_plan':{'Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator','Patient Liaison'},'treatment_plan':{'Medical Oncology','Surgical Oncology','Radiation Oncology'},'readiness':{'Medical Oncology'},'treatment_order':{'Medical Oncology'},'pharmacy':{'Oncology Pharmacy'},'infusion':{'Day Care / Infusion Nurse'},'toxicity':{'Medical Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Nurse Navigator'},'modification':{'Medical Oncology'},'response':{'Medical Oncology','Radiologist'},'radiation':{'Radiation Oncology','Radiation Technologist','Radiation Physicist'},'surgery':{'Surgical Oncology','Surgical Nurse'},'finance':{'Finance / Billing','Biller'},'conversion':{'Finance / Billing'},'visit_summary':{'Medical Oncology'},'protocol_library':{'Hospital Management / Admin'},'formulary':{'Hospital Management / Admin'},'standards':{'Hospital Management / Admin'},'cca_requirements':{'Hospital Management / Admin'}}

# PC6.1/PC7.1 connected core oncology flow -- referral lifecycle entity (additive; does not change any existing entity type).
WRITE['referral']={'Front Desk','Patient Attender','PRE / Patient Relations Executive','Nurse Navigator','Medical Oncology','Surgical Oncology','Radiation Oncology'}
REFERRAL_TRANSITIONS={'Created':{'Assigned','Cancelled'},'Assigned':{'Accepted','Scheduled','Cancelled'},'Accepted':{'Scheduled','Seen','Closed','Cancelled'},'Scheduled':{'Seen','Cancelled'},'Seen':{'Closed'},'Closed':set(),'Cancelled':set()}
READ['Front Desk'].add('referral');READ['Patient Attender'].add('referral');READ['PRE / Patient Relations Executive'].add('referral');READ['Nurse Navigator'].add('referral');READ['Medical Oncology'].add('referral')
READ['Medical Oncology'].add('survivorship');READ['Nurse Navigator'].add('survivorship');READ['Patient Liaison'].add('survivorship')
for _r in ['Medical Oncology','Nurse Navigator','Surgical Oncology','Radiation Oncology']:
 READ[_r].add('treatment_completion');READ[_r].add('surveillance')
READ['Medical Oncology'].add('psychosocial')

# PC8.0 connected-multidisciplinary RBAC: real read/write surfaces for the 11 PC4.0-era
# PRD roles (previously wired only through the PC4 JSON screen engine, which is untouched
# and remains available alongside this). Additive only -- no existing role/entity changes.
READ['Radiation Dosimetrist / Planner']={'registration','diagnosis','radiology','radiation','rt_planning','documents','cancer_episode'}
READ['Anaesthetist']={'registration','diagnosis','lab','radiology','surgery','anaesthesia','consent','documents','cancer_episode'}
READ['Blood Bank / Transfusion']={'registration','lab','surgery','blood_bank','documents','cancer_episode'}
READ['Stoma / Wound Nurse']={'registration','surgery','stoma_wound','inpatient_care','documents','cancer_episode'}
READ['Dietitian / Nutrition']={'registration','intake','diagnosis','nutrition','documents','cancer_episode'}
READ['Psycho-Oncology']={'registration','intake','diagnosis','psychosocial','documents','cancer_episode'}
READ['Palliative Care']={'registration','diagnosis','toxicity','palliative','documents','cancer_episode'}
READ['Clinical Trials / Research']={'registration','diagnosis','treatment_plan','clinical_trial','documents','cancer_episode'}
READ['Health Information Management']={'registration','documents','him','cancer_episode'}
READ['Pathology Technologist']={'registration','pathology','pathology_processing','documents','cancer_episode'}
READ['Inpatient Oncology Clinician']={'registration','intake','med_recon','diagnosis','lab','radiology','pathology','treatment_plan','readiness','treatment_order','pharmacy','infusion','toxicity','journey','cancer_episode','admission','inpatient_care','discharge','documents'}
WRITE['navigation']={'Nurse Navigator'};WRITE['anaesthesia']={'Anaesthetist'};WRITE['blood_bank']={'Blood Bank / Transfusion'};WRITE['stoma_wound']={'Stoma / Wound Nurse'};WRITE['nutrition']={'Dietitian / Nutrition'};WRITE['psychosocial']={'Psycho-Oncology'};WRITE['palliative']={'Palliative Care'};WRITE['clinical_trial']={'Clinical Trials / Research'};WRITE['him']={'Health Information Management'};WRITE['pathology_processing']={'Pathology Technologist'};WRITE['rt_planning']={'Radiation Dosimetrist / Planner'}
for _r in ['Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator','Inpatient Oncology Clinician']:
 READ.setdefault(_r,set()).update({'navigation','nutrition','palliative'});READ.setdefault(_r,set()).add('him')
READ.setdefault('Medical Oncology',set()).update({'psychosocial','clinical_trial'})
READ.setdefault('Nurse Navigator',set()).add('radiation')
READ.setdefault('Surgical Oncology',set()).update({'anaesthesia','blood_bank','stoma_wound','pathology_processing'})
READ.setdefault('Surgical Nurse',set()).update({'anaesthesia','blood_bank','stoma_wound'})
READ.setdefault('Pathology',set()).add('pathology_processing')
READ.setdefault('Radiation Oncology',set()).add('rt_planning');READ.setdefault('Radiation Physicist',set()).add('rt_planning');READ.setdefault('Radiation Technologist',set()).add('rt_planning')
WRITE.setdefault('inpatient_care',set()).add('Inpatient Oncology Clinician');WRITE.setdefault('discharge',set()).add('Inpatient Oncology Clinician')
SUPPORT_TYPE_BY_ROLE={'Anaesthetist':'anaesthesia','Blood Bank / Transfusion':'blood_bank','Stoma / Wound Nurse':'stoma_wound','Dietitian / Nutrition':'nutrition','Psycho-Oncology':'psychosocial','Palliative Care':'palliative','Clinical Trials / Research':'clinical_trial','Health Information Management':'him','Pathology Technologist':'pathology_processing','Radiation Dosimetrist / Planner':'rt_planning','Nurse Navigator':'navigation'}

VALUE_SETS={'ecog':['0','1','2','3','4'],'kps':[str(x) for x in range(0,101,10)],'intent':['Curative','Palliative','Neoadjuvant','Adjuvant','Definitive','Maintenance','Diagnostic','Other'],'route':['IV','PO','IM','SQ','Intrathecal','CIV','Other'],'allergy_severity':['Mild','Moderate','Severe','Life-threatening','Unknown'],'allergy_status':['No known allergy','Allergy present','Unable to verify'],'allergy_source':['Patient','Caregiver','Prior record','External clinician','Observed at CCA','Integrated record'],'allergy_reaction':['Rash','Urticaria','Pruritus','Angioedema','Anaphylaxis','Bronchospasm','Nausea / vomiting','Other','Unknown'],'med_reconciliation_status':['Complete','Incomplete','Unable to verify'],'care_plan_status':['Draft','Proposed','Active','Blocked','On Hold','Completed','Superseded','Cancelled'],'appointment_status':['Scheduled','Rescheduled','No-show','Cancelled','Completed'],'dose_basis':['Fixed','mg/kg','mg/m²','AUC','Other'],'decision':['Proceed as Planned','Proceed with Modification','Hold','Delay','Omit','Substitute','Stop'],'toxicity':['Nausea','Vomiting','Diarrhea','Mucositis','Neutropenia','Thrombocytopenia','Anemia','Fatigue','Neuropathy','Alopecia','Cardiotoxicity','Nephrotoxicity','Hepatotoxicity','Other'],'ctcae_grade':['1','2','3','4','5'],'laterality':['Left','Right','Bilateral','Midline','Not applicable'],'treatment_line':['Neoadjuvant','Adjuvant','1st line','2nd line','3rd line','Subsequent line','Maintenance','Consolidation','Salvage','Other'],'pharmacy_decision':['Verified','Query','Reject'],'completion_status':['Administered','Partially Administered','Held','Stopped'],'rt_frequency':['Daily','5x/week','3x/week','Weekly','Other'],'surgery_priority':['Routine','Urgent','Emergency'],'admission_type':['Planned','Emergency','Unplanned'],'admission_reason':['Treatment / procedure','Treatment toxicity','Infection / febrile neutropenia','Adverse drug reaction','Post-operative care','Brachytherapy procedure','Seizure / neurologic event','Nutrition / dehydration','Other'],'admission_status':['Active','Transferred','Discharged','Deceased'],'care_setting':['OPD','Day Care','IPD'],'continuous_mode':['Oral systemic therapy','Hormonal therapy','Other continuous systemic therapy'],'task_status':['Open','Acknowledged','Completed','Cancelled'],'task_priority':['Routine','High','Critical'],'medication_status':['Continue','Hold','Stopped'],'medication_frequency':['Once daily','Twice daily','Three times daily','Every other day','Weekly','As needed','Other prescribed schedule'],'medication_dose_unit':['mg','mcg','g','mL','tablet','capsule','unit'],'access_type':['Peripheral IV','PICC','Central venous catheter','Port','Oral / no vascular access','Other'],'access_site':['Left upper limb','Right upper limb','Left lower limb','Right lower limb','Chest central access','Not applicable','Other'],'mar_variance_type':['None','Dose variance','Rate variance','Route variance','Timing variance','Sequence variance','Other'],'mar_variance_reason':['Clinician instruction','Infusion reaction','Access issue','Patient condition','Operational delay','Product issue','Other'],'pharmacy_wastage_reason':['Partial vial','Dose rounding','Preparation error','Spill / breakage','Cancelled treatment','Expired / BUD exceeded','Return not reusable','Other']}
VALUE_SETS['referral_priority']=['Routine','Urgent','Emergency']
VALUE_SETS['referral_status']=['Created','Assigned','Accepted','Scheduled','Seen','Closed','Cancelled']

# Product-test governed masters exercise the SELECTED-control contract only. They are not CCA clinical content.
ALLERGEN_MASTER=[
 {'code':'ALG-PEN','label':'Penicillin','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-LATEX','label':'Latex','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-CONTRAST','label':'Iodinated contrast media','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-CARBO','label':'Carboplatin','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-DOC','label':'Docetaxel','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-TRA','label':'Trastuzumab','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-PER','label':'Pertuzumab','code_system':'Synthetic QA allergen master'},
 {'code':'ALG-OTHER','label':'Other governed allergen — CCA master required','code_system':'Synthetic QA allergen master'}]
ALLERGEN_BY_CODE={x['code']:x for x in ALLERGEN_MASTER}
FALL_RISK_SCALES={
 'CCA Demo Fall-Risk Scale — Synthetic QA':{'min':0,'max':10,'bands':[{'max':2,'level':'Low'},{'max':5,'level':'Moderate'},{'max':10,'level':'High'}],'clinical_content_status':'Synthetic QA — CCA must approve/configure the actual scale and cut-offs'}
}

# Synthetic QA Pharmacy preparation rules exercise server-governed compatibility/stability/BUD derivation only.
# CCA Pharmacy must replace/approve every value before patient-care use.
PHARMACY_PREP_RULES={
 'DEMO-DEX':{'compatibility_status':'Not applicable','stability_hours':24,'stability_reference':'Synthetic QA oral product handling — CCA Pharmacy configuration required','storage_condition':'Synthetic QA storage — CCA Pharmacy configuration required','light_protection':'Not applicable','filter_requirement':'Not applicable','container_requirement':'Original labelled pack'},
 'DEMO-PER':{'compatibility_status':'Compatible','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'DEMO-TRA':{'compatibility_status':'Compatible','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'DEMO-DOC':{'compatibility_status':'Compatible','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'DEMO-CARBO':{'compatibility_status':'Compatible','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'DEMO-PEG':{'compatibility_status':'Not applicable','stability_hours':24,'stability_reference':'Synthetic QA syringe handling — CCA Pharmacy configuration required','storage_condition':'Synthetic QA storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'Not applicable','container_requirement':'Prefilled syringe — Synthetic QA'},
 'QA-SUPPORT':{'compatibility_status':'Not applicable','stability_hours':24,'stability_reference':'Synthetic QA oral product handling — CCA Pharmacy configuration required','storage_condition':'Synthetic QA storage — CCA Pharmacy configuration required','light_protection':'Not applicable','filter_requirement':'Not applicable','container_requirement':'Original labelled pack — Synthetic QA'},
 'QA-BSA':{'compatibility_status':'Compatible — Synthetic QA only','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'QA-WT':{'compatibility_status':'Compatible — Synthetic QA only','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'QA-AUC':{'compatibility_status':'Compatible — Synthetic QA only','stability_hours':4,'stability_reference':'Synthetic QA infusion stability — CCA Pharmacy configuration required','storage_condition':'Synthetic QA controlled storage — CCA Pharmacy configuration required','light_protection':'Not required — Synthetic QA','filter_requirement':'No filter — Synthetic QA','container_requirement':'Infusion bag — Synthetic QA'},
 'QA-ORAL':{'compatibility_status':'Not applicable','stability_hours':24,'stability_reference':'Synthetic QA oral product handling — CCA Pharmacy configuration required','storage_condition':'Synthetic QA storage — CCA Pharmacy configuration required','light_protection':'Not applicable','filter_requirement':'Not applicable','container_requirement':'Original labelled pack — Synthetic QA'}
}


LAB_UNIT_OPTIONS={
 'hb':['g/dL'],
 'wbc':['10^9/L','×10^9/L','x10^9/L','cells/uL','cells/µL','cells/μL'],
 'anc':['10^9/L','×10^9/L','x10^9/L','cells/uL','cells/µL','cells/μL'],
 'platelets':['10^9/L','×10^9/L','x10^9/L','cells/uL','cells/µL','cells/μL'],
 'creatinine':['mg/dL','umol/L','µmol/L','μmol/L'],
 'egfr':['mL/min/1.73m2','mL/min/1.73m²'],
 'bilirubin':['mg/dL','umol/L','µmol/L','μmol/L'],
 'ast':['U/L'],'alt':['U/L'],'albumin':['g/dL'],
 'sodium':['mmol/L'],'potassium':['mmol/L'],'magnesium':['mg/dL','mmol/L'],'calcium':['mg/dL','mmol/L'],
 'lvef':['%']
}
LAB_NUMERIC_FIELDS=list(LAB_UNIT_OPTIONS.keys())
READINESS_REQUIRED_UNIT_FIELDS=['anc','platelets','bilirubin']

# Institution-controlled operational location master used by queue routing.

# PC1.9 Phase 7 governed structural masters. Values are product-test/demo structure, not CCA clinical content.
DIAGNOSTIC_CATALOG={
 'LAB-CBC':{'type':'Laboratory','name':'CBC','code':'57021-8','code_system':'LOINC','active':True},
 'LAB-CMP':{'type':'Laboratory','name':'Comprehensive metabolic panel','code':'24323-8','code_system':'LOINC','active':True},
 'RAD-BREAST-MRI':{'type':'Radiology','name':'Breast MRI','code':'CCA-RAD-BREAST-MRI','code_system':'Synthetic QA diagnostic catalogue','active':True},
 'RAD-CT-CAP':{'type':'Radiology','name':'CT chest/abdomen/pelvis','code':'CCA-RAD-CT-CAP','code_system':'Synthetic QA diagnostic catalogue','active':True},
}
LAB_ABNORMAL_FLAGS=['Normal','Low','High','Critical low','Critical high','Abnormal non-numeric','Unknown']
LAB_REFERENCE_RANGE_MASTER={
 'hb':{'lower':12.0,'upper':17.5,'unit':'g/dL','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'wbc':{'lower':4.0,'upper':11.0,'unit':'10^9/L','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'anc':{'lower':1.5,'upper':7.5,'unit':'10^9/L','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'platelets':{'lower':150.0,'upper':450.0,'unit':'10^9/L','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'creatinine':{'lower':0.5,'upper':1.3,'unit':'mg/dL','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'egfr':{'lower':60.0,'upper':None,'unit':'mL/min/1.73m2','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'bilirubin':{'lower':0.2,'upper':1.2,'unit':'mg/dL','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'ast':{'lower':0.0,'upper':40.0,'unit':'U/L','source':'Synthetic QA LIS/assay master — CCA integration required'},
 'alt':{'lower':0.0,'upper':45.0,'unit':'U/L','source':'Synthetic QA LIS/assay master — CCA integration required'},
}
RESPONSE_CATEGORIES=['Complete response','Partial response','Stable disease','Progressive disease','Not evaluable','Criteria-specific immune response category']
MDT_DISCIPLINES=['Medical Oncology','Radiation Oncology','Surgical Oncology','Radiology','Pathology','Nursing','Pharmacy','Palliative Care','Genetics','Other']
MDT_CONSENSUS=['Consensus','Majority agreement','No consensus','Deferred pending information']
MDT_RECOMMENDATIONS=['Systemic therapy','Radiation therapy','Surgery','Combined modality','Observation/surveillance','Further investigation','Supportive/palliative care','Referral','Other']

LOCATION_MASTER=['Front Desk','Nurse Intake','Medical Oncology','Surgical Oncology','Radiation Oncology','Laboratory / Phlebotomy','Radiology','Pathology','MDT / Tumour Board','Oncology Pharmacy','Day Care / Infusion','Inpatient Care','Finance / Billing','Patient Liaison','Follow-up','Episode Closure']
LOCATION_ROLE_MAP={'Nurse Intake':'Nurse Navigator','Medical Oncology':'Medical Oncology','Surgical Oncology':'Surgical Oncology','Radiation Oncology':'Radiation Oncology','Laboratory / Phlebotomy':'Laboratory / Phlebotomy','Radiology':'Radiology Coordinator','Pathology':'Pathology','MDT / Tumour Board':'MDT Coordinator','Oncology Pharmacy':'Oncology Pharmacy','Day Care / Infusion':'Day Care / Infusion Nurse','Inpatient Care':'Inpatient Oncology Nurse','Finance / Billing':'Finance / Billing','Patient Liaison':'Patient Liaison'}
GLOBAL_PATIENT_ACCESS_ROLES={'Front Desk','Patient Attender','Hospital Management / Admin'}

# Plausibility ranges are data-quality guards, not treatment thresholds. Values are
# converted to the canonical unit shown here before validation. They deliberately use
# wide humanly plausible envelopes so transcription slips are caught without turning
# the prototype into a diagnostic engine.
LAB_PLAUSIBLE_RANGES={
 'hb':(1.0,30.0,'g/dL'),'wbc':(0.01,300.0,'10^9/L'),'anc':(0.0,100.0,'10^9/L'),
 'platelets':(1.0,3000.0,'10^9/L'),'creatinine':(0.05,30.0,'mg/dL'),'egfr':(0.0,250.0,'mL/min/1.73m2'),
 'bilirubin':(0.0,80.0,'mg/dL'),'ast':(0.0,20000.0,'U/L'),'alt':(0.0,20000.0,'U/L'),
 'albumin':(0.5,8.0,'g/dL'),'sodium':(90.0,200.0,'mmol/L'),'potassium':(1.0,10.0,'mmol/L'),
 'magnesium':(0.1,10.0,'mg/dL'),'calcium':(3.0,20.0,'mg/dL'),'lvef':(1.0,100.0,'%')}

# Synthetic product-test critical-result routing thresholds. These exercise closed-loop alerting only;
# CCA must replace/approve them before any patient-care deployment.
LAB_CRITICAL_ROUTING_RULES={'hb':{'lt':6.5,'unit':'g/dL'},'anc':{'lt':0.5,'unit':'×10^9/L'},'platelets':{'lt':20,'unit':'×10^9/L'},'potassium':{'lt':2.5,'gt':6.5,'unit':'mmol/L'}}

SAFE_UPLOAD_MIME={'application/pdf','image/jpeg','image/png','image/webp','text/plain','application/dicom','application/octet-stream'}
ACTIVE_CONTENT_MIME={'text/html','application/xhtml+xml','image/svg+xml','application/javascript','text/javascript','application/xml','text/xml'}

# Stale-write protection is mandatory for mutable draft/working records. The UI sends
# the current record version automatically; direct clients must do the same.
OPTIMISTIC_LOCK_ACTIONS={'save_intake','med_recon','save_dynamic_form','save_consultation','save_diagnosis','save_appointment','queue_patient','save_care_plan','save_treatment_plan','save_radiology','save_pathology','mdt_comment','mdt_attendance','mdt_recommend'}
CARE_PLAN_TRANSITIONS={
 'Draft':{'Draft','Proposed','Active','Cancelled'},'Proposed':{'Proposed','Active','Blocked','On Hold','Cancelled'},
 'Active':{'Active','Blocked','On Hold','Completed','Superseded','Cancelled'},'Blocked':{'Blocked','Active','On Hold','Cancelled'},
 'On Hold':{'On Hold','Active','Cancelled'},'Completed':{'Completed','Superseded'},'Superseded':{'Superseded'},'Cancelled':{'Cancelled'}}

PROTOCOL={
'id':'CCA-DEMO-TCHP','version':'1.0-demo','name':'Synthetic HER2+ Breast Neoadjuvant Demo Regimen','indication':'HER2-positive breast cancer — synthetic demo only','intent':'Neoadjuvant','cycle_length_days':21,'planned_cycles':6,'approved_by':'Synthetic demo governance — NOT clinical content','effective_date':'2026-09-01','orderable':True,
'hold_parameters':{'ANC_min':1.5,'platelets_min':100,'eGFR_min':50,'bilirubin_max':1.5,'LVEF_min':50,'lab_max_age_days':7},
'clinical_safety':{'dose_variance_limit_pct':20,'bsa_rounding_policy':'Mosteller raw 4dp; display/order 2dp','renal_dosing_requires_method_source_time':True,'max_dose_policy':'Per-drug master only; no platform-invented universal cap'},
'items':[
 {'sequence':1,'group':'Premedication','drug':'Dexamethasone','code':'DEMO-DEX','dose_basis':'Fixed','protocol_dose':8,'protocol_unit':'mg','route':'PO','frequency':'BID','relative_start_days':[-1,0,1],'timing':'Synthetic showcase: 8 mg twice daily for 3 days starting 1 day before docetaxel','special_instructions':'Synthetic demonstration schedule; local CCA supportive-care master governs production.'},
 {'sequence':2,'group':'Targeted Therapy','drug':'Pertuzumab','code':'DEMO-PER','dose_basis':'Fixed','protocol_dose':840,'protocol_unit':'mg','route':'IV','diluent':'NS','volume_ml':250,'duration_min':60,'max_variance_pct':20},
 {'sequence':3,'group':'Targeted Therapy','drug':'Trastuzumab','code':'DEMO-TRA','dose_basis':'mg/kg','protocol_dose':8,'protocol_unit':'mg/kg','route':'IV','diluent':'NS','volume_ml':250,'duration_min':90,'max_variance_pct':20},
 {'sequence':4,'group':'Antineoplastic','drug':'Docetaxel','code':'DEMO-DOC','dose_basis':'mg/m²','protocol_dose':75,'protocol_unit':'mg/m²','route':'IV','diluent':'NS','volume_ml':250,'duration_min':60,'max_variance_pct':20},
 {'sequence':5,'group':'Antineoplastic','drug':'Carboplatin','code':'DEMO-CARBO','dose_basis':'AUC','protocol_dose':6,'protocol_unit':'AUC','route':'IV','diluent':'D5W','volume_ml':250,'duration_min':60,'renal_dosing':{'allowed_methods':['Measured GFR','Validated nuclear medicine GFR','Cockcroft-Gault creatinine clearance','CCA-approved renal dosing value'],'gfr_cap_ml_min':None,'cap_policy':'No synthetic cap configured; CCA governance required for production'},'max_variance_pct':20,'max_dose_mg':1000,'max_dose_source':'Synthetic QA hard ceiling to exercise blocker — NOT CCA production policy'},
 {'sequence':6,'group':'Supportive','drug':'Pegfilgrastim','code':'DEMO-PEG','dose_basis':'Fixed','protocol_dose':6,'protocol_unit':'mg','route':'SQ','relative_start_days':[2],'timing':'Synthetic showcase: ≥24 hours after cytotoxic chemotherapy; not within 14 days before next cytotoxic cycle','min_hours_after_cytotoxic':24,'not_within_days_before_next_cytotoxic':14}
]}
# V12.2-PC1: clinician-review metadata extends the synthetic demo protocol without changing
# the validated dose/readiness behavior used by the executable acceptance suites.
PROTOCOL.update({
 'clinical_content_status':'Synthetic demo — product testing only; CCA specialist approval required',
 'clinician_review_mode':'Hide synthetic clinical dose values; preserve workflow structure',
 'readiness_rule_schema':[
  {'id':'RR-ANC','category':'Hematology','source_field':'anc','operator':'>=','threshold_key':'ANC_min','unit':'×10^9/L','failure_action':'HOLD / clinician review'},
  {'id':'RR-PLT','category':'Hematology','source_field':'platelets','operator':'>=','threshold_key':'platelets_min','unit':'×10^9/L','failure_action':'HOLD / clinician review'},
  {'id':'RR-EGFR','category':'Renal','source_field':'egfr','operator':'>=','threshold_key':'eGFR_min','unit':'mL/min/1.73m²','failure_action':'REVIEW / dose modification as configured'},
  {'id':'RR-BILI','category':'Hepatic','source_field':'bilirubin','operator':'<=','threshold_key':'bilirubin_max','unit':'mg/dL','failure_action':'REVIEW / HOLD as configured'},
  {'id':'RR-LVEF','category':'Cardiac','source_field':'lvef','operator':'>=','threshold_key':'LVEF_min','unit':'%','failure_action':'REVIEW as configured'},
  {'id':'RR-AGE','category':'Freshness','source_field':'lab_date','operator':'age_days<=','threshold_key':'lab_max_age_days','unit':'days','failure_action':'REPEAT investigation'}],
 'monitoring_requirements':[
  {'phase':'Before treatment / cycle','category':'Hematology','requirement':'CBC with ANC and platelets','clinical_value_status':'CCA-approved protocol required'},
  {'phase':'Before treatment / cycle','category':'Renal','requirement':'Renal function assessment','clinical_value_status':'CCA-approved protocol required'},
  {'phase':'Before treatment / cycle','category':'Hepatic','requirement':'Hepatic function assessment','clinical_value_status':'CCA-approved protocol required'},
  {'phase':'Before treatment / cycle','category':'Toxicity','requirement':'Current toxicity/CTCAE assessment','clinical_value_status':'CCA-approved protocol required'},
  {'phase':'Periodic / drug-specific','category':'Other','requirement':'Drug-specific monitoring where applicable','clinical_value_status':'CCA-approved protocol required'}],
 'dose_modification_rules':[
  {'domain':'Hematologic','trigger':'CCA-approved regimen threshold / toxicity condition','action_options':['Proceed','Hold','Delay','Dose reduce','Omit'],'new_dose_rule':'Protocol-specific','clinical_value_status':'CCA configuration required'},
  {'domain':'Renal','trigger':'CCA-approved renal function rule','action_options':['Proceed','Dose reduce','Substitute','Hold'],'new_dose_rule':'Protocol-specific','clinical_value_status':'CCA configuration required'},
  {'domain':'Hepatic','trigger':'CCA-approved hepatic function rule','action_options':['Proceed','Dose reduce','Hold','Omit'],'new_dose_rule':'Protocol-specific','clinical_value_status':'CCA configuration required'},
  {'domain':'Toxicity','trigger':'CTCAE grade / drug-specific adverse effect','action_options':['Proceed','Hold','Delay','Dose reduce','Omit','Discontinue'],'new_dose_rule':'Protocol-specific','clinical_value_status':'CCA configuration required'}],
 'sequence_sections':['Pre-treatment / Premedication / Hydration','Anticancer Treatment','Post-treatment / Supportive / Rescue']
})

FORMULARY={'items':[
 {'drug':'Dexamethasone','drug_code':'DEMO-DEX','formulations':[{'label':'Dexamethasone 4 mg tablet','strength_mg':4}],'allowed_routes':['PO'],'allowed_diluents':[]},
 {'drug':'Pertuzumab','drug_code':'DEMO-PER','formulations':[{'label':'Pertuzumab 420 mg vial','strength_mg':420}],'allowed_routes':['IV'],'allowed_diluents':['NS']},
 {'drug':'Trastuzumab','drug_code':'DEMO-TRA','formulations':[{'label':'Trastuzumab 150 mg vial','strength_mg':150}],'allowed_routes':['IV'],'allowed_diluents':['NS']},
 {'drug':'Docetaxel','drug_code':'DEMO-DOC','formulations':[{'label':'Docetaxel 80 mg vial','strength_mg':80},{'label':'Docetaxel 20 mg vial','strength_mg':20}],'allowed_routes':['IV'],'allowed_diluents':['NS']},
 {'drug':'Carboplatin','drug_code':'DEMO-CARBO','formulations':[{'label':'Carboplatin 450 mg vial','strength_mg':450},{'label':'Carboplatin 150 mg vial','strength_mg':150}],'allowed_routes':['IV'],'allowed_diluents':['D5W','NS']},
 {'drug':'Pegfilgrastim','drug_code':'DEMO-PEG','formulations':[{'label':'Pegfilgrastim 6 mg syringe','strength_mg':6}],'allowed_routes':['SQ'],'allowed_diluents':[]}]}

# PC7 oncology terminology / standards catalogs are intentionally small local demo catalogs.
# Production terminology should be connected to CCA's approved terminology service/master.
ONCOLOGY_TERMINOLOGY=TERMINOLOGY
MDT_QUORUM={'version':'CCA-SYNTHETIC-QA-1','required_roles':['Medical Oncology','Radiologist','Pathology'],'chair_required':True,'minimum_present':4,'note':'Synthetic tumor-board quorum for product testing only; CCA configures production quorum.'}
INTEGRATION_ADAPTER_DEFAULTS=[
 {'id':'HMIS-ADT','name':'HMIS / ADT','standard':'HL7/FHIR','status':'Not connected'}, {'id':'LIS','name':'Laboratory Information System','standard':'HL7/FHIR','status':'Not connected'},
 {'id':'RIS-PACS','name':'RIS / PACS','standard':'DICOM/HL7/FHIR','status':'Not connected'}, {'id':'PATH-LIS','name':'Pathology LIS','standard':'HL7/FHIR','status':'Not connected'},
 {'id':'TPS-OIS','name':'TPS / OIS / Record & Verify','standard':'DICOM-RT / vendor API','status':'Not connected'}, {'id':'PHARM-ERP','name':'Pharmacy ERP / Inventory','standard':'API/HL7','status':'Not connected'},
 {'id':'FHIR','name':'FHIR Interoperability','standard':'FHIR R4+ mapping boundary','status':'Not connected'}, {'id':'ABDM','name':'ABDM / ABHA','standard':'ABDM APIs','status':'Not connected'},
 {'id':'VOICE','name':'OPD Voice Documentation Adapter','standard':'External adapter','status':'Not connected — excluded from this clinical-safety build'}, {'id':'OCR','name':'OCR / Document Extraction Adapter','standard':'External adapter','status':'Not connected — manual/source-fact review available'}]



# -----------------------------------------------------------------------------
# V11 institution-level clinical content master.
# Imported historical/open-source content is deliberately NOT automatically
# orderable. It must pass local clinical + pharmacy governance before activation.
# -----------------------------------------------------------------------------
CONTENT_SOURCES=[
 {'id':'SRC-CCA-DEMO','name':'CCA V12 Synthetic Demo Clinical Content','source_url':'local://cca-v12','license_status':'Internal synthetic demo','license_name':'CCA demo content','commercial_use':'Internal demonstration only until clinically approved','status':'Active','notes':'Synthetic content exists to exercise the workflow engine; not prescribing advice.'},
 {'id':'SRC-OPENMRS-ONC','name':'OpenMRS Oncology Historical Regimen Templates','source_url':'https://github.com/openmrs/openmrs-module-oncology/tree/master/regimens','license_status':'Repository LICENSE is Mozilla Public License 2.0 with an OpenMRS Healthcare Disclaimer; preserve notices and review distribution obligations before commercial release','license_name':'Mozilla Public License 2.0 + OpenMRS Healthcare Disclaimer','commercial_use':'Source-derived content is imported as historical reference under the source license; it remains non-orderable until local clinical/pharmacy governance. Legal review still recommended before commercial distribution.','status':'Reference','notes':'The historical YAML library provides regimen/cycle/day/sequence structure. V12 imports all 12 historical regimen files as non-orderable drafts; no imported regimen is treated as current prescribing guidance.'},
 {'id':'SRC-OPENMRS-ORDEREXT','name':'OpenMRS Order Extension','source_url':'https://github.com/openmrs/openmrs-module-orderextension','license_status':'MPL-2.0 + healthcare disclaimer in repository','license_name':'Mozilla Public License 2.0','commercial_use':'Use subject to license obligations and clinical validation','status':'Reference','notes':'Used as a workflow/reference source for cyclical order sets, chemotherapy calendars and administration-plan concepts.'},
 {'id':'SRC-OPENEMR','name':'OpenEMR Document Template Infrastructure','source_url':'https://github.com/openemr/openemr','license_status':'GPL-3.0 repository','license_name':'GNU GPL v3','commercial_use':'Reference architecture only unless license obligations are intentionally adopted','status':'Reference','notes':'Used as a reference for centrally managed document/report template infrastructure, not copied UI.'}
]

def _item(seq,group,drug,code,basis,dose,unit,route,**kw):
 return {'sequence':seq,'group':group,'drug':drug,'code':code,'dose_basis':basis,'protocol_dose':dose,'protocol_unit':unit,'route':route,**kw}

OPENMRS_AC_ITEMS=[
 _item(1,'Premedication','Sodium chloride 0.9%','OMRS-NS1000','Fixed',1000,'mL','IV',timing='Once prior to chemotherapy'),
 _item(2,'Premedication','Dexamethasone','OMRS-DEX','Fixed',16,'mg','PO',timing='60 minutes prior'),
 _item(3,'Premedication','Ondansetron','OMRS-OND','Fixed',8,'mg','PO',timing='60 minutes prior'),
 _item(4,'Antineoplastic','Doxorubicin','OMRS-DOX','mg/m²',60,'mg/m²','IV',special_instructions='Historical OpenMRS source describes IV push with free-flowing saline'),
 _item(5,'Antineoplastic','Cyclophosphamide','OMRS-CYC','mg/m²',600,'mg/m²','IV',special_instructions='Historical OpenMRS source includes dilution/infusion instructions')]
OPENMRS_CHOP_ITEMS=[
 _item(1,'Premedication','Sodium chloride 0.9%','OMRS-NS1000','Fixed',1000,'mL','IV',timing='Once prior to chemotherapy'),
 _item(2,'Premedication','Ondansetron','OMRS-OND','Fixed',8,'mg','PO',timing='60 minutes prior'),
 _item(3,'Antineoplastic','Prednisone','OMRS-PRED','Fixed',100,'mg','PO',timing='Daily x5 days per historical source'),
 _item(4,'Antineoplastic','Doxorubicin','OMRS-DOX50','mg/m²',50,'mg/m²','IV'),
 _item(5,'Antineoplastic','Vincristine','OMRS-VCR','mg/m²',1.4,'mg/m²','IV'),
 _item(6,'Antineoplastic','Cyclophosphamide','OMRS-CYC750','mg/m²',750,'mg/m²','IV')]
OPENMRS_CARBOTAXOL_ITEMS=[
 _item(1,'Premedication','Sodium chloride 0.9%','OMRS-NS500','Fixed',500,'mL','IV'),
 _item(2,'Premedication','Dexamethasone','OMRS-DEX16','Fixed',16,'mg','PO'),
 _item(3,'Premedication','Cimetidine','OMRS-CIM','Fixed',600,'mg','PO'),
 _item(4,'Premedication','Diphenhydramine','OMRS-DPH','Fixed',50,'mg','PO'),
 _item(5,'Premedication','Ondansetron','OMRS-OND','Fixed',8,'mg','PO'),
 _item(6,'Antineoplastic','Paclitaxel','OMRS-PAC175','mg/m²',175,'mg/m²','IV',volume_ml=500,duration_min=180),
 _item(7,'Antineoplastic','Carboplatin','OMRS-CARBO','AUC',None,'AUC','IV',volume_ml=250,duration_min=60,special_instructions='Historical source does not specify the AUC value; patient-specific order requires a governed local calculator/rule')]

CONTENT_TEMPLATES=[
 {'id':'REG-CCA-TCHP-DEMO','category':'Regimen','name':PROTOCOL['name'],'subtype':'Systemic therapy regimen','disease':'Breast Cancer','setting':'HER2-positive, demo','intent':'Neoadjuvant','line_of_therapy':'Neoadjuvant','version':PROTOCOL['version'],'status':'Active','governance_status':'Demo Approved','orderable':True,'source_id':'SRC-CCA-DEMO','source_ref':'local synthetic master','effective_date':'2026-09-01','review_due':'2026-12-01','clinical_owner':'Medical Oncology','pharmacy_owner':'Oncology Pharmacy','data':PROTOCOL},
 {'id':'REG-OMRS-AC','category':'Regimen','name':'AC — historical OpenMRS reference','subtype':'Systemic therapy regimen','disease':'Breast Cancer','setting':'Non-metastatic / locally advanced (historical source wording)','intent':'Pending CCA review','line_of_therapy':'Pending CCA review','version':'OpenMRS-2018-import-1','status':'Imported Draft','governance_status':'Clinical + Pharmacy Review Required','orderable':False,'source_id':'SRC-OPENMRS-ONC','source_ref':'regimens/AC.yaml','effective_date':'','review_due':'','clinical_owner':'Pending','pharmacy_owner':'Pending','data':{'id':'REG-OMRS-AC','version':'OpenMRS-2018-import-1','name':'AC — OpenMRS historical reference','cycle_length_days':21,'planned_cycles':4,'items':OPENMRS_AC_ITEMS,'hold_parameters':{},'references':['OpenMRS Oncology AC.yaml'],'limitations':['Historical template; local antiemetic, preparation, maximum-dose, supportive-care and readiness rules must be re-authored and approved before ordering.']}},
 {'id':'REG-OMRS-CHOP','category':'Regimen','name':'CHOP — historical OpenMRS reference','subtype':'Systemic therapy regimen','disease':'Non-Hodgkin Lymphoma','setting':'Historical OpenMRS regimen','intent':'Pending CCA review','line_of_therapy':'Pending CCA review','version':'OpenMRS-2018-import-1','status':'Imported Draft','governance_status':'Clinical + Pharmacy Review Required','orderable':False,'source_id':'SRC-OPENMRS-ONC','source_ref':'regimens/CHOP.yaml','effective_date':'','review_due':'','clinical_owner':'Pending','pharmacy_owner':'Pending','data':{'id':'REG-OMRS-CHOP','version':'OpenMRS-2018-import-1','name':'CHOP — OpenMRS historical reference','cycle_length_days':21,'planned_cycles':6,'items':OPENMRS_CHOP_ITEMS,'hold_parameters':{},'references':['OpenMRS Oncology CHOP.yaml'],'limitations':['Historical template; no automatic assumption of current guideline appropriateness, vincristine cap, readiness rules or local preparation policy.']}},
 {'id':'REG-OMRS-CARBOTAXOL','category':'Regimen','name':'Carboplatin + Paclitaxel — historical OpenMRS reference','subtype':'Systemic therapy regimen','disease':'Solid Tumor — disease mapping pending','setting':'Historical OpenMRS regimen','intent':'Pending CCA review','line_of_therapy':'Pending CCA review','version':'OpenMRS-2018-import-1','status':'Imported Draft','governance_status':'Clinical + Pharmacy Review Required','orderable':False,'source_id':'SRC-OPENMRS-ONC','source_ref':'regimens/CarboTaxol.yaml','effective_date':'','review_due':'','clinical_owner':'Pending','pharmacy_owner':'Pending','data':{'id':'REG-OMRS-CARBOTAXOL','version':'OpenMRS-2018-import-1','name':'Carboplatin + Paclitaxel — OpenMRS historical reference','cycle_length_days':21,'planned_cycles':6,'items':OPENMRS_CARBOTAXOL_ITEMS,'hold_parameters':{},'references':['OpenMRS Oncology CarboTaxol.yaml'],'limitations':['Historical source leaves carboplatin dose basis incomplete; AUC/Calvert logic and indication must be locally validated before activation.']}},
 {'id':'WF-NEW-ONC','category':'Workflow','name':'New Oncology Patient','subtype':'Process template','disease':'All','setting':'New patient','intent':'','line_of_therapy':'','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA shared workflow diagrams','data':{'trigger':'Patient arrival','stages':['Registration','Consent','Nurse Intake','Medical Oncology','Diagnostics if required','Diagnosis/Staging','MDT if required','Treatment Plan','Follow-up'],'required_roles':['Front Desk','Nurse Navigator','Medical Oncology'],'completion_criteria':['Current location recorded','Required clinical record created','Next handoff assigned']}},
 {'id':'WF-SYSTEMIC-CYCLE','category':'Workflow','name':'Systemic Therapy Cycle','subtype':'Process template','disease':'All','setting':'Treatment day','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA golden flow + OpenMRS order/admin workflow pattern','data':{'stages':['Cycle Readiness','Treatment Order','Pharmacy Verification','Preparation','Independent Release','Day Care Pre-check','MAR','Post-treatment','Toxicity','Next-cycle Readiness'],'required_roles':['Medical Oncology','Oncology Pharmacy','Day Care / Infusion Nurse'],'hard_gates':['Signed readiness','Signed order','Pharmacy verified/released','8 pre-administration checks']}},
 {'id':'WF-RT-COURSE','category':'Workflow','name':'Radiation Treatment Course','subtype':'Process template','disease':'All','setting':'Radiation Oncology','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA RT flow','data':{'stages':['RT Prescription','Simulation','Contouring','Planning','Physics QA','Physician Approval','Treatment Ready','Fraction Delivery','Treatment Complete']}},
 {'id':'WF-SURGICAL','category':'Workflow','name':'Surgical Oncology Episode','subtype':'Process template','disease':'All','setting':'Surgical Oncology','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA surgery flow','data':{'stages':['Recommended','Surgeon Reviewed','Planned','Pre-op Ready','Scheduled','Performed','Post-op','Histopathology Available','Adjuvant Review']}},
 {'id':'RPT-MDT','category':'Report','name':'MDT Recommendation Summary','subtype':'Clinical report','disease':'All','setting':'MDT','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA MDT specification','data':{'sections':['Patient/cancer context','Stage/performance status','Pathology/biomarkers','Clinical question','Discussion','Alternatives','Formal recommendation','Consensus','Participants','Outstanding investigations','Signatures'],'signatures':['MDT Coordinator','Contributing specialties']}},
 {'id':'RPT-TX-ORDER','category':'Report','name':'Signed Systemic Treatment Order','subtype':'Clinical report','disease':'All','setting':'Medical Oncology','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA order specification','data':{'sections':['Patient identifiers','Diagnosis/intent/line','Regimen/version/cycle/day','Patient variables','Eligibility criteria','Ordered sequence','Protocol vs calculated vs ordered dose','Supportive therapy','Authorization','Version history']}},
 {'id':'RPT-MAR','category':'Report','name':'Medication Administration Record','subtype':'Clinical report','disease':'All','setting':'Day Care','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA MAR specification','data':{'sections':['Patient/order identity','Pharmacy release','Pre-administration checklist','Per-drug actual administration','Reaction/intervention','Post-treatment vitals','Tolerance','Discharge/next cycle']}},
 {'id':'RPT-RT-COMPLETE','category':'Report','name':'Radiation Course Summary','subtype':'Clinical report','disease':'All','setting':'Radiation Oncology','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA RT specification','data':{'sections':['Prescription','Planning approvals','Fraction-by-fraction delivery','Cumulative dose','Interruptions','On-treatment reviews','Completion status','DICOM-RT references']}},
 {'id':'RPT-SURGERY','category':'Report','name':'Surgical Oncology Operative Outcome','subtype':'Clinical report','disease':'All','setting':'Surgical Oncology','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA surgical specification','data':{'sections':['Planned procedure','Actual procedure','Pre/post-op diagnosis','Site/laterality','Findings','Specimens','Complications','EBL','Operative time','Team','Post-op plan','Histopathology link']}},
 {'id':'RT-TPL-BREAST-ADJ','category':'Radiation Template','name':'Breast Adjuvant RT Prescription Skeleton','subtype':'RT prescription template','disease':'Breast Cancer','setting':'Adjuvant','version':'1.0','status':'Draft','governance_status':'Radiation Oncology Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA RT field specification','data':{'site':'Breast / chest wall','laterality':'Select','intent':'Adjuvant','modality':'External Beam','technique':'Select','energy':'Select','target_volumes':[],'organs_at_risk':['Heart','Ipsilateral lung'],'oar_constraints':[],'simulation_requirement':'Yes','immobilisation':'Breast board / institution-defined','image_guidance':'Institution-defined','bolus':'As clinically indicated','note':'Dose/fractionation deliberately not prefilled until Radiation Oncology governance approves local templates.'}},
 {'id':'SURG-TPL-BREAST','category':'Surgical Template','name':'Breast Surgery Planning Skeleton','subtype':'Surgical plan template','disease':'Breast Cancer','setting':'Definitive surgery','version':'1.0','status':'Draft','governance_status':'Surgical Oncology Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA surgical field specification','data':{'procedures':['Breast-conserving surgery / lumpectomy','Mastectomy','Other'],'laterality':['Left','Right','Bilateral'],'approaches':['Open'],'nodal_procedures':['Sentinel lymph node biopsy','Axillary lymph node dissection','None','Other'],'reconstruction':['None','Immediate reconstruction — type to be selected','Delayed reconstruction','Other'],'preop_requirements':['Anesthesia assessment','Required labs','Relevant imaging/pathology reviewed','Consent'],'note':'Procedure vocabulary requires local surgeon review before activation.'}},
 {'id':'WF-SECOND-OPINION','category':'Workflow','name':'Oncology Second Opinion','subtype':'Process template','disease':'All','setting':'Second opinion','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA workflow architecture','data':{'stages':['Registration','Outside document intake','Nurse reconciliation','Specialist review','Pathology/Radiology re-review if required','Diagnosis/staging confirmation','Recommendation','Visit summary'],'required_roles':['Front Desk','Nurse Navigator','Oncology specialist'],'completion_criteria':['Source records linked','Differences from outside diagnosis/plan documented','Recommendation signed']}},
 {'id':'WF-TREATMENT-CLEARANCE','category':'Workflow','name':'Treatment Patient / Cycle Clearance','subtype':'Process template','disease':'All','setting':'Pre-cycle','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA Medical Oncology flow','data':{'stages':['Toxicity review','Vitals/performance status','Lab review','Protocol readiness evaluation','Proceed/Modify/Hold/Delay/Stop','Treatment Order or Hold record'],'required_roles':['Medical Oncology'],'hard_gates':['Signed readiness decision before systemic order']}},
 {'id':'WF-RECURRENCE','category':'Workflow','name':'Recurrence / Progression Episode','subtype':'Process template','disease':'All','setting':'Recurrence / progression','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA longitudinal oncology requirement','data':{'stages':['New disease-status event','Restaging','Biomarker/pathology update if required','Response/progression evidence','MDT / specialist decision','New treatment phase'],'completion_criteria':['Prior episode preserved','New stage/disease status stored as new record','New line linked to prior history']}},
 {'id':'WF-SURVIVORSHIP','category':'Workflow','name':'End-of-Treatment / Survivorship Follow-up','subtype':'Process template','disease':'All','setting':'Follow-up','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'Oncology longitudinal follow-up requirement','data':{'stages':['Treatment completion summary','Residual toxicity review','Surveillance plan','Late-effect / supportive care needs','Follow-up scheduling'],'required_roles':['Oncology specialist','Nurse Navigator','Patient Liaison']}},
 {'id':'RPT-ONC-CONSULT','category':'Report','name':'Oncology Consultation Note','subtype':'Clinical report','disease':'All','setting':'OPD','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA OPD specification','data':{'sections':['Patient/cancer context','Chief complaint/HPI','Review of systems','Structured examination','Assessment','Decision branch','Plan','Orders','Signature']}},
 {'id':'RPT-READINESS','category':'Report','name':'Treatment Readiness / Clearance Record','subtype':'Clinical report','disease':'All','setting':'Medical Oncology','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA readiness specification','data':{'sections':['Cycle/day','Current weight/BSA/performance status','Vitals','Protocol-required labs','Toxicities','Allergy/medication review','Server-evaluated criteria','Proceed/modify/hold/delay/stop decision','Clinical rationale','Signature']}},
 {'id':'RPT-PHARM-VERIFY','category':'Report','name':'Oncology Pharmacy Verification Record','subtype':'Clinical report','disease':'All','setting':'Oncology Pharmacy','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA pharmacy specification','data':{'sections':['Patient/order identity','Allergy/interaction review','Protocol vs calculated vs ordered dose','Organ function','Formulation/stock/expiry','Verification decision','Query/reject thread','Pharmacist identity/time']}},
 {'id':'RPT-PHARM-PREP','category':'Report','name':'Antineoplastic Preparation / Dispensing Record','subtype':'Clinical report','disease':'All','setting':'Oncology Pharmacy','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA preparation/dispensing specification','data':{'sections':['Source order','Formulation/strength','Batch/lot/expiry','Diluent/actual volume','Wastage','Preparation start/finish','Prepared by','Independent checker','Barcode/label','Release/destination/manifest']}},
 {'id':'RPT-SYSTEMIC-COMPLETE','category':'Report','name':'Systemic Therapy Course / Cycle Summary','subtype':'Clinical report','disease':'All','setting':'Medical Oncology / Day Care','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA order-to-delivery specification','data':{'sections':['Regimen/version','Cycle/day','Signed order','Pharmacy verification/preparation/release','MAR actual doses/times','Variances','Toxicity','Readiness for next cycle']}},
 {'id':'RPT-RESPONSE','category':'Report','name':'Treatment Response Assessment','subtype':'Clinical report','disease':'All','setting':'Response assessment','version':'1.0','status':'Active','governance_status':'CCA Operational Draft','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA response specification','data':{'sections':['Baseline reference','Imaging date','Target lesions','Non-target lesions','New lesions','Response category','Disease status','Markers/biomarkers','Clinical correlation']}},
 {'id':'RT-TPL-HN-DEFINITIVE','category':'Radiation Template','name':'Head & Neck Definitive RT Prescription Skeleton','subtype':'RT prescription template','disease':'Head & Neck Cancer','setting':'Definitive','version':'1.0','status':'Draft','governance_status':'Radiation Oncology + Physics Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA RT field specification','data':{'site':'Head / Neck','laterality':'Select','intent':'Definitive','modality':'External Beam','technique':'Select','energy':'Select','target_volumes':[],'organs_at_risk':['Spinal cord','Brainstem','Parotids','Oral cavity','Larynx','Esophagus'],'oar_constraints':[],'simulation_requirement':'Yes','immobilisation':'Thermoplastic mask / institution-defined','image_guidance':'Institution-defined','note':'Dose, fractionation and constraints deliberately blank pending local approval.'}},
 {'id':'RT-TPL-CERVIX-DEFINITIVE','category':'Radiation Template','name':'Cervix Definitive RT Prescription Skeleton','subtype':'RT prescription template','disease':'Cervical Cancer','setting':'Definitive','version':'1.0','status':'Draft','governance_status':'Radiation Oncology + Physics Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA RT field specification','data':{'site':'Pelvis / Cervix','laterality':'Not applicable','intent':'Definitive','modality':'External Beam / Brachytherapy link','technique':'Select','target_volumes':[],'organs_at_risk':['Bladder','Rectum','Bowel','Femoral heads','Kidneys if extended field'],'oar_constraints':[],'simulation_requirement':'Yes','immobilisation':'Institution-defined','image_guidance':'Institution-defined','note':'No dose/fractionation preset; brachytherapy remains a separately governed prescription/delivery workflow.'}},
 {'id':'RT-TPL-PALL-BONE','category':'Radiation Template','name':'Palliative Bone RT Prescription Skeleton','subtype':'RT prescription template','disease':'Metastatic Solid Tumor','setting':'Palliative','version':'1.0','status':'Draft','governance_status':'Radiation Oncology + Physics Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA RT field specification','data':{'site':'Bone / Spine — select','laterality':'Select','intent':'Palliative','modality':'External Beam','technique':'Select','target_volumes':[],'organs_at_risk':[],'oar_constraints':[],'simulation_requirement':'Select','image_guidance':'Institution-defined','note':'No dose/fractionation preset; local palliative pathways must be reviewed before use.'}},
 {'id':'SURG-TPL-COLORECTAL','category':'Surgical Template','name':'Colorectal Cancer Surgery Planning Skeleton','subtype':'Surgical plan template','disease':'Colorectal Cancer','setting':'Definitive surgery','version':'1.0','status':'Draft','governance_status':'Surgical Oncology Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA surgical field specification','data':{'procedures':['Segmental colectomy','Anterior resection','Abdominoperineal resection','Other'],'laterality':['Not applicable'],'approaches':['Open','Laparoscopic','Robotic','Hybrid'],'nodal_procedures':['Regional lymphadenectomy / specimen-based nodal assessment','Other'],'reconstruction':['Primary anastomosis','Stoma — type to be selected','Other'],'preop_requirements':['Anesthesia assessment','Required labs','Imaging reviewed','Pathology reviewed','Consent'],'note':'Procedure and extent vocabulary requires local surgeon review.'}},
 {'id':'SURG-TPL-KIDNEY','category':'Surgical Template','name':'Kidney Cancer Surgery Planning Skeleton','subtype':'Surgical plan template','disease':'Kidney Cancer','setting':'Definitive surgery','version':'1.0','status':'Draft','governance_status':'Surgical Oncology Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA surgical field specification','data':{'procedures':['Partial nephrectomy','Radical nephrectomy','Other'],'laterality':['Left','Right','Bilateral'],'approaches':['Open','Laparoscopic','Robotic','Hybrid'],'nodal_procedures':['None','Regional node dissection if indicated','Other'],'reconstruction':['Not applicable','Other'],'preop_requirements':['Anesthesia assessment','Required labs','Renal function','Imaging reviewed','Consent'],'note':'Procedure/approach selection remains surgeon-controlled.'}},
 {'id':'SURG-TPL-GASTRIC','category':'Surgical Template','name':'Gastric Cancer Surgery Planning Skeleton','subtype':'Surgical plan template','disease':'Gastric Cancer','setting':'Definitive surgery','version':'1.0','status':'Draft','governance_status':'Surgical Oncology Review Required','orderable':False,'source_id':'SRC-CCA-DEMO','source_ref':'CCA surgical field specification','data':{'procedures':['Distal gastrectomy','Total gastrectomy','Other'],'laterality':['Not applicable'],'approaches':['Open','Laparoscopic','Robotic','Hybrid'],'nodal_procedures':['Regional lymphadenectomy — extent to be selected','Other'],'reconstruction':['Procedure-specific reconstruction — select','Other'],'preop_requirements':['Anesthesia assessment','Required labs','Nutrition assessment','Imaging reviewed','Pathology reviewed','Consent'],'note':'Extent and nodal procedure require local surgical governance.'}}
]

def _f(field,data_type='text',mandatory=False,value_set='',code_system='',source='',notes=''):
 # Never leave the field contract visually ambiguous: unknown clinical selectors are explicitly pending review rather than silently invented.
 dt=str(data_type or '').lower();structured=any(k in dt for k in ['select','coded','structured','checklist','verification','template','list'])
 if not value_set:value_set='Pending specialist value-set review' if structured else 'Not applicable / field-format constrained'
 if not code_system:code_system='Pending terminology mapping' if any(k in dt for k in ['select','coded','structured']) else 'Not applicable'
 return {'field':field,'data_type':data_type,'mandatory':bool(mandatory),'value_set':value_set,'code_system':code_system,'source':source or 'Role workflow / local master','notes':notes}
def _v(field,source,notes=''):
 return {'field':field,'source':source,'notes':notes,'read_only':True,'timestamp_visible':True}
def _o(record,handoff,notes=''):
 return {'record':record,'handoff':handoff,'notes':notes}

ROLE_SURFACES={
 'Medical Oncology':{
  'input':[
   _f('Regimen / protocol','search-select',True,'Approved Regimen Master','Institution regimen ID','Clinical Content Master'),_f('Protocol version','read-only from selection',True,'Selected version','Versioned master','Clinical Content Master'),_f('Treatment intent','select',True,'intent','SNOMED CT/local mapping','Treatment Plan'),_f('Line of therapy','select',True,'treatment_line','Structured oncology line','Treatment Plan'),_f('Cycle number','integer',True),_f('Day number','integer',True),_f('Planned cycles','integer',True),_f('Start date','date',True),
   _f('Generic drug','coded select',True,'Regimen ordered item','RxNorm/SNOMED/local formulary','Regimen Master'),_f('Sequence number','integer/read-only',True,'Regimen sequence','','Regimen Master'),_f('Dose basis','select',True,'dose_basis','UCUM dose expression','Regimen Master'),_f('Protocol dose','number/read-only',True,'Template value','UCUM','Regimen Master'),_f('Patient-calculated dose','number/read-only',True,'Calculated','UCUM','Order engine'),_f('Final ordered dose','number',True,'Clinician-entered/confirmed','UCUM'),_f('Dose rounding','select',False,'Institution rounding rule','Local pharmacy policy'),_f('Dose reduction %','number',False),_f('Dose modification reason','select',False,'Toxicity|Organ function|Tolerance|Clinical judgment|Other','SNOMED CT/local'),_f('Route','select',True,'route','SNOMED CT'),_f('Diluent','select',False,'Formulary allowed diluents','Local formulary'),_f('Diluent volume','number + mL',False,'','UCUM'),_f('Final concentration','calculated/read-only',False,'','UCUM'),_f('Infusion rate','number',False,'','UCUM'),_f('Infusion duration','duration',False,'','UCUM'),_f('Administration date/time','datetime',True),_f('Special instructions','text',False,'',''),
   _f('Premedications / hydration / antiemetics / growth factors / rescue / emergency standby','template sections',False,'Approved regimen items','Drug terminology','Regimen Master')],
  'view':[_v('Allergies with reaction/severity','Medication reconciliation'),_v('Current reconciled medications','Medication reconciliation'),_v('Height/weight/BSA + formula + measurement date','Nurse Intake'),_v('Renal function + result date','Final Lab'),_v('Hepatic function + result date','Final Lab'),_v('Pregnancy status where applicable','Final Lab'),_v('Performance status','Nurse Intake / Diagnosis'),_v('Cumulative dose tracking','Treatment History / prior administrations'),_v('CBC/ANC/platelets and regimen criteria','Readiness engine'),_v('Protocol vs calculated vs ordered vs administered dose','Canonical order/admin chain'),_v('MDT recommendation and originating meeting','MDT'),_v('Treatment Plan phase / intent / line','Treatment Plan')],
  'output':[_o('Signed Treatment Order','Oncology Pharmacy','Locked patient-specific order linked to exact regimen version'),_o('Modification Order','Pharmacy / Day Care','Original order preserved'),_o('Treatment Readiness Decision','Treatment Order','Proceed/modify/hold/delay/stop with reviewed evidence'),_o('Treatment Plan version','Pharmacy/RT/Surgery as applicable','Plan remains separate from MDT and executable orders')]},
 'Radiation Oncology':{
  'input':[_f('Diagnosis','read-only link',True,'','ICD/SNOMED','Cancer record'),_f('Treatment site','coded select',True,'Institution RT site master','SNOMED CT'),_f('Laterality','select',True,'laterality','SNOMED CT'),_f('Intent','select',True,'intent'),_f('Modality','select',True,'External Beam|Brachytherapy|Stereotactic|Particle|Other'),_f('Technique','select',True,'3D Conformal|IMRT|VMAT|Proton|Brachytherapy|Stereotactic|Other'),_f('Energy / radioisotope','select/text from machine master',True,'TPS/OIS machine/energy master'),_f('Treatment phase','integer',True),_f('Total prescribed dose','number Gy',True,'','UCUM'),_f('Dose per fraction','number Gy',True,'','UCUM'),_f('Number of fractions','integer',True),_f('Frequency','select',True,'rt_frequency'),_f('Planned start date','date',True),_f('Concurrent systemic treatment','linked order/select',False,'Active Medical Oncology orders'),_f('Target volumes','structured list',True,'RT structure reference','DICOM-RT / SNOMED'),_f('Organs at risk','multi-select',True,'Institution OAR master'),_f('OAR constraints','structured constraint list',True,'Institution RT constraint master'),_f('Simulation requirement','select',True,'Yes|No'),_f('Immobilisation','select',False,'Institution immobilisation master'),_f('Image guidance','select',False,'Institution IGRT master'),_f('Bolus','select',False,'None|Custom|Other'),_f('Special instructions','text',False)],
  'view':[_v('Cancer diagnosis/stage','Cancer record'),_v('MDT recommendation','MDT'),_v('Concurrent systemic order','Medical Oncology'),_v('Prior radiation exposure / overlapping course','Treatment History / OIS integration'),_v('Relevant imaging','Radiology/PACS references'),_v('TPS/OIS plan references','DICOM-RT integration boundary')],
  'output':[_o('Signed RT Prescription','Simulation / Planning','Locks prescription'),_o('RT Planning/QA Approval','Radiation Technologist','Simulation→contouring→planning→physics QA→physician approval'),_o('Fraction Delivery Record','RT Course Summary','Per fraction actual dose/date/verification'),_o('RT Course Summary','Cancer record / follow-up','Prescribed vs delivered totals + interruptions')]},
 'Surgical Oncology':{
  'input':[_f('Procedure','coded select',True,'Surgical procedure master','SNOMED CT/ICD-PCS/local'),_f('Indication','select',True,'Diagnostic|Definitive treatment|Palliative|Debulking|Re-section for recurrence|Other'),_f('Intent','select',True,'Curative|Palliative|Diagnostic|Other'),_f('Anatomical site','coded select',True,'Anatomical site master','SNOMED CT'),_f('Laterality','select',True,'laterality'),_f('Proposed extent','select',True,'Procedure-specific extent master'),_f('Approach','select',True,'Open|Laparoscopic|Robotic|Hybrid|Other'),_f('Nodal procedure','select',False,'Procedure-specific nodal master'),_f('Reconstruction','select',False,'Procedure-specific reconstruction master'),_f('Planned date','date',True),_f('Priority','select',True,'surgery_priority'),_f('Pre-operative requirements','checklist',True,'Procedure template checklist'),_f('Required imaging/pathology','multi-select',True,'Order/result references'),_f('Anaesthesia type','select',True,'General|Regional|Local|Monitored sedation|Other'),_f('Anaesthesia clearance','select',True,'Pending|Complete|Not cleared'),_f('Blood product requirement','select',False,'Local transfusion/pre-op master'),_f('Special instructions','text',False)],
  'view':[_v('Diagnosis/stage','Cancer record'),_v('MDT recommendation','MDT'),_v('Response after neoadjuvant therapy','Response Assessment'),_v('Pre-op clearances','Surgical Nurse / Anaesthesia interface'),_v('Imaging/pathology','Radiology/Pathology')],
  'output':[_o('Signed Surgical Plan','Surgical Nurse / Scheduling'),_o('Pre-op Readiness','Operating pathway'),_o('Operative Record','Pathology / post-op'),_o('Final histopathology linkage + new pathological stage','Cancer record / MDT/adjuvant planning','Clinical stage is not overwritten')]},
 'Oncology Pharmacy':{
  'input':[_f('Verification checklist','boolean checklist',True,'Allergy|Interaction|Dose method|Calculated dose|Dose|Organ function|Diluent|Volume|Stock|Expiry'),_f('Verification decision','select',True,'pharmacy_decision'),_f('Query/reject reason','select',False,'Dose clarification|Allergy|Interaction|Formulation|Stock|Expiry|Other'),_f('Message to oncologist','text',False,'Required for Query/Reject'),_f('Formulation / strength','governed select',True,'Formulary Master'),_f('Batch / lot','text',True),_f('Expiry','date',True),_f('Actual measured volume','number',True,'','UCUM'),_f('Wastage','number + reason',False),_f('Preparation start / finish','datetime',True),_f('Prepared by','authenticated actor',True),_f('Independent checker','authenticated actor',True),_f('Barcode / label match','boolean',True),_f('Dispense destination','select',True,'Day Care / Other approved destination'),_f('Dispense time','datetime',True),_f('Manifest','identifier',True)],
  'view':[_v('Patient + 2 identifiers','Registration'),_v('Allergies','Medication reconciliation'),_v('Signed regimen/cycle/day/order sequence','Treatment Order'),_v('Protocol vs calculated vs ordered dose','Treatment Order / Regimen Master'),_v('Route/diluent/volume/concentration/rate/duration','Treatment Order'),_v('Prescriber + authorization timestamp','Treatment Order'),_v('Renal/hepatic function','Readiness/Lab'),_v('Current medication list','Medication reconciliation')],
  'output':[_o('Verification Record','Prescriber thread / Preparation'),_o('Query/Reject Thread','Medical Oncology','Requires prescriber resolution before re-verification'),_o('Preparation Record','Final checker'),_o('Dispensing/Release Record','Day Care','Carries exact order values and pharmacist authorization')]},
 'Day Care / Infusion Nurse':{
  'input':[_f('Two patient identifiers','verification',True,'Name+MRN/DOB'),_f('Order vs prepared medication check','boolean',True),_f('Consent current','boolean',True),_f('Allergies verified with patient','boolean',True),_f('Pre-treatment vitals','structured vitals',True),_f('Required labs in range/current','boolean + evidence',True),_f('Venous access type/site/patency','structured select/text',True,'Central line|PICC|Port|Peripheral IV|Other'),_f('Pharmacy-prepared medication/label match','boolean',True),_f('Actual administered dose','number',True,'','UCUM'),_f('Route / access site','read-only route + selected access',True),_f('Actual rate','number',False,'','UCUM'),_f('Start / end time','time',True),_f('Reaction','select',True,'None|Flushing|Rash|Hypotension|Tachycardia|Chest pain|Dyspnea|Allergic|Other'),_f('Intervention','text',False),_f('Completion status','select',True,'completion_status'),_f('Reason if incomplete','select/text',False),_f('Post-treatment vitals','structured vitals',True),_f('Tolerance','select',True,'Good|Mild symptoms|Significant reaction'),_f('Discharge instructions','template/text',True),_f('Next cycle date','date',False)],
  'view':[_v('Signed locked Treatment Order','Medical Oncology'),_v('Pharmacy verification/release','Oncology Pharmacy'),_v('Allergies','Medication reconciliation'),_v('Consent status','Consent'),_v('Readiness labs + hold criteria','Readiness'),_v('Administration sequence','Treatment Order')],
  'output':[_o('Pre-administration Verification','MAR'),_o('Per-drug Medication Administration Record','Treatment history / Toxicity'),_o('Variance / reaction record','Medical Oncology'),_o('Treatment-day Completion Record','Next-cycle readiness')]},
 'Nurse Navigator':{'input':[_f('Vitals','structured',True),_f('Height/weight','number',True,'','UCUM'),_f('ECOG/Karnofsky','select',True,'ecog/kps'),_f('Pain assessment','structured',True),_f('Fall risk','structured',True),_f('Medication reconciliation','structured',True),_f('Allergies/adverse reactions','structured',True),_f('Oncology history','dynamic structured form',True),_f('Old document upload','file + metadata',False)],'view':[_v('Registration/queue','Front Desk'),_v('Prior documents','Document store'),_v('Current care plan','Care Plan')],'output':[_o('Completed Intake','Medical Oncology'),_o('Reconciled Medication/Allergy List','All clinical roles'),_o('Updated Care Plan tasks','Care team')]},
 'Front Desk':{'input':[_f('Name/DOB/contact/ID','structured registration',True),_f('ABHA association','identifier',False),_f('Clinician/specialty routing','select',True),_f('Referral hierarchy','structured',False),_f('Appointment','structured',False),_f('Queue destination','select',True)],'view':[_v('Administrative identity','Patient master'),_v('Appointment/queue state','Scheduling/Queue')],'output':[_o('Registration Record','Nurse Intake / specialty'),_o('Queue Handoff','Next location'),_o('Appointment','Department worklist')]},
 'Patient Attender':{'input':[_f('Registration form demographics','structured',True),_f('Consent artefact','file/signature',True),_f('Patient photograph','file',False)],'view':[_v('Registration status','Patient master'),_v('Consent status','Consent register')],'output':[_o('Completed Registration Form','Front Desk / Intake'),_o('Signed Consent','Clinical workflow')]},
 'Biller':{'input':[_f('Payment status','select',True,'Paid|Waived'),_f('Amount','number',False),_f('Receipt number','identifier',True),_f('Waiver reason','text',False)],'view':[_v('Billable service order only','Lab/Radiology order')],'output':[_o('Payment/waiver event','Lab/Radiology gate')]},
 'PRE / Patient Relations Executive':{'input':[_f('Patient movement/escort status','select',True),_f('Radiology appointment scheduling','datetime/location',False)],'view':[_v('Queue destination','Queue'),_v('Payment-cleared diagnostic order','Billing/Order')],'output':[_o('Movement event','Receiving department'),_o('Scheduled diagnostic appointment','Radiology worklist')]},
 'Laboratory / Phlebotomy':{'input':[_f('Sample/accession ID','identifier',True),_f('Collection time','datetime',True),_f('Laboratory result value','number',True,'Test-specific result entry','LOINC observation mapping'),_f('Laboratory result unit','mandatory coded select',True,'Governed test-specific unit set; no implicit/default unit','UCUM mapping'),_f('Final-result amendment reason','text',False,'Required when correcting a finalized result')],'view':[_v('Paid/waived lab order','Medical Oncology/Billing'),_v('Two patient identifiers','Registration'),_v('Prior finalized result + units when creating an amendment','Longitudinal Lab Record')],'output':[_o('Sample Collection Record','Partner/Lab processing'),_o('Final Laboratory Result with explicit unit metadata','EMR/Readiness'),_o('Linked Laboratory Amendment','EMR/Readiness','Original final result is never overwritten')]},
 'Radiology Coordinator':{'input':[_f('Scheduled date/time','datetime',True),_f('Location / modality room','select',True,'Radiology location master'),_f('Scheduling note','text',False),_f('Relevant document checklist','checklist',False)],'view':[_v('Physician radiology order and indication','Medical Oncology'),_v('Payment/waiver status','Biller / Finance'),_v('Patient identifiers','Registration'),_v('Relevant prior imaging/documents','EMR documents')],'output':[_o('Radiology Schedule Record','PRE / Radiology Technician'),_o('Queue / location handoff','Radiology Technician')]},
 'Radiology Technician':{'input':[_f('Procedure performed time','datetime',True),_f('Consent verified','boolean',True),_f('Technical note','text',False)],'view':[_v('Paid/waived scheduled imaging order','Medical Oncology/Billing/PRE'),_v('Relevant documents','Document store')],'output':[_o('Procedure Completion Record','Radiologist')]},
 'Radiologist':{'input':[_f('Findings','structured/text report',True),_f('Impression','text',True),_f('eSignature','authenticated sign',True)],'view':[_v('Imaging order/indication','Medical Oncology'),_v('Prior imaging','Radiology record')],'output':[_o('Final Radiology Report','Cancer record/MDT/OPD')]},
 'Pathology':{'input':[_f('Specimen/site','coded',True),_f('Histology/grade','coded',True,'','ICD-O/SNOMED'),_f('Biomarkers','structured',False),_f('Margin/node data','structured',False),_f('Pathology sign-off','authenticated sign',True)],'view':[_v('Procedure/specimen context','Surgery/Order')],'output':[_o('Final Pathology Report','Diagnosis/Staging/MDT'),_o('Post-op pathology facts','Pathological staging/adjuvant review')]},
 'MDT Coordinator':{'input':[_f('Meeting date/time/mode','structured',True),_f('Case list','patient/case references',True),_f('Attendance','structured',True),_f('Discussion/comments','attributed entries',True),_f('Formal recommendation','structured/text',True),_f('Consensus','select/text',True),_f('Outstanding investigations','task list',False)],'view':[_v('Diagnosis/stage/performance status','Cancer record'),_v('Pathology/biomarkers','Pathology'),_v('Imaging/labs','Diagnostics')],'output':[_o('Signed MDT Recommendation','Specialty plan creation'),_o('MDT Follow-up Tasks','Care team'),_o('De-identified external case token','External Consultant')]},
 'Radiation Physicist':{'input':[_f('Physics QA decision','select',True,'Approved|Rejected / Replan Required'),_f('Physics QA note','textarea',True),_f('QA completion time','datetime',True)],'view':[_v('Signed RT prescription','Radiation Oncology'),_v('Simulation / contouring / plan references','RT workflow / TPS-OIS references'),_v('OAR constraints and planned dose','RT prescription / plan references'),_v('Prior overlapping radiation','Treatment History / OIS reference')],'output':[_o('Physics QA Record','Radiation Oncology / Radiation Technologist','Treatment-ready remains blocked until physics QA and physician approval are both complete')]},
 'Radiation Technologist':{'input':[_f('Fraction number/status','structured',True),_f('Delivery date/time','datetime',True),_f('Delivered dose','number Gy',True,'','UCUM'),_f('Image guidance performed','boolean',True),_f('Setup variation','structured/text',False),_f('Toxicity noted','structured',False)],'view':[_v('Approved RT prescription','Radiation Oncology'),_v('Physics QA/physician approval','RT planning record')],'output':[_o('Fraction Delivery Record','RT Course Summary')]},
 'Surgical Nurse':{'input':[_f('Pre-op checklist','structured',True),_f('Consent/labs/anesthesia clearance','status',True),_f('Scheduling/OR readiness note','structured',False)],'view':[_v('Signed Surgical Plan','Surgical Oncology'),_v('Patient identity/allergy/consent','EMR')],'output':[_o('Pre-op Readiness Record','Surgical Oncology/OR')]},
 'Finance / Billing':{'input':[_f('Financial counselling status','select',True),_f('Payer/funding category','select',True),_f('Estimate adjustment','structured',False),_f('Funding letter recipient/purpose','structured',False)],'view':[_v('Signed treatment plan/order cost basis only','Treatment/Cost master')],'output':[_o('Estimate','Patient/Management'),_o('Counselling Record','Patient record'),_o('Funding Support Letter','Patient/External recipient')]},
 'Patient Liaison':{'input':[_f('Consent/education status','structured',True),_f('Care-plan task update','structured',False),_f('Appointment coordination','structured',False)],'view':[_v('Care plan tasks','Care Plan'),_v('Upcoming appointments','Scheduling')],'output':[_o('Education/coordination update','Care team')]},
 'Hospital Management / Admin':{'input':[_f('Content-template governance','approve/retire/version',True),_f('Form/workflow/report master configuration','structured master data',False)],'view':[_v('Operational queues/volumes','De-identified/limited operational data'),_v('Clinical content governance status','Content Master'),_v('Audit integrity','Audit ledger')],'output':[_o('Approved Institution Content Version','Clinical roles'),_o('Operational configuration','Workflow engine'),_o('Governance/audit evidence','Authorized reviewers')]},
 'External Consultant':{'input':[_f('Case-scoped token','token',True)],'view':[_v('De-identified MDT case only','MDT external projection')],'output':[_o('External opinion/comment','MDT record when supported')]}
}

# V12 process/IPD hardening: surface contracts for newly visible patient variables,
# concurrent modality context and inpatient oncology work.
ROLE_SURFACES['Oncology Pharmacy']['view'].extend([
 _v('Height / weight / BSA + formula + measurement date','Nurse Intake','Required for independent dose-calculation verification'),
 _v('Intake assessor / provenance','Nurse Intake','Shows who measured the variables and when')])
ROLE_SURFACES['Oncology Pharmacy']['view'].extend([
 _v('Full regimen-specific readiness evidence + signed decision','Readiness','ANC/platelets/other criteria, result units/dates/freshness and clinician signature must be visible before preparation'),
 _v('Relevant active toxicity / prior infusion reaction','Toxicity / MAR','Explains holds/modifications and supports independent verification'),
 _v('Cumulative administered-dose ledger + configured limit','Treatment History / Regimen','Uses verified administrations, never planned/ordered doses')])
ROLE_SURFACES['Day Care / Infusion Nurse']['view'].extend([
 _v('Order weight / height / BSA snapshot + measurement provenance','Signed Treatment Order','Read-only dosing context used by the signed order'),
 _v('Relevant prior infusion reactions / active toxicity','Toxicity / Treatment History','Supports treatment-day monitoring and escalation')])
ROLE_SURFACES['MDT Coordinator']['view'].extend([
 _v('Prior systemic / radiation / surgical treatment history','Treatment History'),
 _v('Active toxicity','Toxicity'),
 _v('Latest formal response assessment','Response Assessment')])
ROLE_SURFACES['Pathology']['view'].extend([
 _v('Cancer episode / primary diagnosis / site','Cancer Record'),
 _v('Prior pathology / biomarker / treatment context','Pathology / Diagnosis / Treatment History')])
ROLE_SURFACES['Radiation Technologist']['view'].extend([
 _v('Current fraction number + planned fraction dose','Approved RT course'),
 _v('Image-guidance requirement for current plan/fraction','Approved RT prescription / plan')])
ROLE_SURFACES['Radiation Physicist']['view'].append(_v('RO final approval state for current plan version','RT planning approval chain'))
ROLE_SURFACES['Radiation Oncology']['view'].extend([_v('Current ECOG/KPS','Nurse Intake'),_v('Active toxicity / recent treatment reaction','Toxicity')])
ROLE_SURFACES['Surgical Oncology']['view'].extend([_v('Current ECOG/KPS','Nurse Intake'),_v('Active toxicity / systemic-treatment recovery state','Toxicity / Treatment History')])
ROLE_SURFACES['Radiation Oncology']['view'].append(_v('Active signed systemic order / cycle-day','Medical Oncology','Read-only concurrent-modality context; Radiation Oncology cannot change systemic orders'))
ROLE_SURFACES['Surgical Oncology']['view'].append(_v('Active signed systemic order / cycle-day','Medical Oncology','Read-only peri-operative/concurrent systemic context; Surgical Oncology cannot change systemic orders'))
ROLE_SURFACES['Nurse Navigator']['view'].append(_v('Active admission / ward / bed','Inpatient record','Supports OPD↔IPD continuity'))
ROLE_SURFACES['Medical Oncology']['input'].extend([_f('Admission decision','select',False,'admission_type'),_f('Admission reason','select',False,'admission_reason'),_f('Continuous/oral therapy plan','structured',False,'continuous_mode')])
ROLE_SURFACES['Medical Oncology']['view'].extend([_v('Cancer episode selector / longitudinal episode history','Cancer Episode'),_v('Active admission and inpatient observations','IPD Record')])
ROLE_SURFACES['Medical Oncology']['output'].extend([_o('Admission / Discharge clinical handoff','Inpatient/OPD continuity'),_o('Continuous Therapy Course','Longitudinal treatment record')])
ROLE_SURFACES['Inpatient Oncology Nurse']={
 'input':[_f('Ward/bed confirmation','structured',True),_f('Inpatient vitals / nursing observations','structured',True),_f('Pain score','number',False),_f('Intake/output','number mL',False,'','UCUM'),_f('Inpatient toxicity','CTCAE structured',False,'toxicity','CTCAE'),_f('Two patient identifiers','verification',True),_f('MAR actual administered dose','number',True,'','UCUM'),_f('MAR start/end/rate/access','structured',True)],
 'view':[_v('Diagnosis / cancer episode','Cancer record'),_v('Active admission / ward / bed','Admission'),_v('Allergies / reconciled medications','Medication reconciliation'),_v('Nurse Intake weight/BSA','Nurse Intake'),_v('Signed inpatient treatment order','Medical Oncology'),_v('Pharmacy verification/release','Oncology Pharmacy'),_v('Treatment readiness/labs','Readiness'),_v('Prior toxicity','Toxicity')],
 'output':[_o('Inpatient Nursing Observation','Inpatient clinical team'),_o('Inpatient CTCAE Toxicity','Next-cycle readiness / oncology team'),_o('Inpatient MAR','Treatment history'),_o('Inpatient Treatment Completion','Discharge / next-cycle planning')]}

# PC1.9: distinct configurable Intake Nurse and MDT Chair surfaces. CCA may later map Intake Nurse to Nurse Navigator without redesigning RBAC.
ROLE_SURFACES['Intake Nurse']={
 'input':list(ROLE_SURFACES['Nurse Navigator']['input']),
 'view':list(ROLE_SURFACES['Nurse Navigator']['view']),
 'output':list(ROLE_SURFACES['Nurse Navigator']['output'])
}
ROLE_SURFACES['MDT Chair']={
 'input':[_f('MDT final decision','select',True,'Approve|Return for revision'),_f('Chair decision reason','text',True),_f('Chair attestation','signature',True)],
 'view':list(ROLE_SURFACES['MDT Coordinator']['view'])+[_v('Submitted MDT recommendation and derived quorum','MDT Coordinator'),_v('Latest formal response assessment','Response Assessment'),_v('Post-operative adjuvant-review readiness','Surgical Oncology')],
 'output':[_o('Chair-approved MDT recommendation','Participating oncologists / Treatment Plan'),_o('Returned MDT recommendation','MDT Coordinator')]
}

# PC4.0 role-surface contracts for roles introduced by the target-state PRD.
for _r in ['Anaesthetist', 'Stoma / Wound Nurse', 'Blood Bank / Transfusion', 'Dietitian / Nutrition', 'Psycho-Oncology', 'Palliative Care', 'Clinical Trials / Research', 'Health Information Management', 'Radiation Dosimetrist / Planner', 'Pathology Technologist', 'Inpatient Oncology Clinician']:
 ROLE_SURFACES.setdefault(_r,{
   'input':[_f('PRD structured clinical / operational input','structured',False,'pc4_workflow')],
   'view':[_v('Role-authorized PRD patient / workflow context','PC4 PRD Complete Workflows')],
   'output':[_o('Signed / attributed PRD workflow record','Downstream role-specific workflow')]
 })


def now(): return datetime.now().astimezone().isoformat(timespec='seconds')
def jdump(x): return json.dumps(x,separators=(',',':'),ensure_ascii=False)
def jload(s,d=None):
    try:return json.loads(s)
    except:return {} if d is None else d

# PC8.0 named-user PIN auth. Salted PBKDF2 digest; never store/compare raw PINs.
def _pin_digest(pin,salt_hex):
 salt=bytes.fromhex(salt_hex);return hashlib.pbkdf2_hmac('sha256',str(pin).encode(),salt,210000).hex()
def _new_pin_hash(pin):
 salt=secrets.token_bytes(16).hex();return salt,_pin_digest(pin,salt)

def current_request_actor(role=''):
 a=getattr(REQUEST_CTX,'actor',None)
 if a and (not role or a.get('role')==role):return a
 return None

class _Row:
 def __init__(self,cols,vals):
  self._cols=cols; self._vals=vals
 def __getitem__(self,k):
  return self._vals[k] if isinstance(k,int) else self._vals[self._cols.index(k)]
 def get(self,k,default=None):
  try:return self[k]
  except (KeyError,ValueError,IndexError):return default
 def keys(self):return self._cols
 def __iter__(self):return iter(self._vals)

class _TursoCursor:
 def __init__(self,raw):
  self._raw=raw; self._cols=[d[0] for d in raw.description] if raw.description else []
 def fetchone(self):
  row=self._raw.fetchone(); return _Row(self._cols,row) if row is not None else None
 def __iter__(self):
  for row in self._raw:yield _Row(self._cols,row)

class _TursoConn:
 def __init__(self,raw):self._raw=raw
 def execute(self,sql,params=()):return _TursoCursor(self._raw.execute(sql,params))
 def executescript(self,script):
  for stmt in script.split(';'):
   s=stmt.strip()
   if s:self._raw.execute(s)
 def commit(self):self._raw.commit()
 def close(self):self._raw.close()

def db():
 turso_url=os.environ.get('TURSO_DATABASE_URL')
 if turso_url:
  import turso_serverless
  return _TursoConn(turso_serverless.connect(turso_url,auth_token=os.environ.get('TURSO_AUTH_TOKEN')))
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init_db():
 c=db(); c.executescript('''
 CREATE TABLE IF NOT EXISTS patients(id TEXT PRIMARY KEY,mrn TEXT UNIQUE,name TEXT,dob TEXT,sex TEXT,phone TEXT,abha TEXT,id_number TEXT,current_department TEXT,status TEXT,photo_document_id TEXT,created_at TEXT,updated_at TEXT);
 CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY,patient_id TEXT,entity_type TEXT,status TEXT,version INTEGER,data_json TEXT,created_at TEXT,updated_at TEXT,created_by TEXT,updated_by TEXT);
 CREATE INDEX IF NOT EXISTS idx_records_patient_type ON records(patient_id,entity_type,created_at);
 CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,patient_id TEXT,actor_id TEXT,actor_role TEXT,action TEXT,entity_type TEXT,entity_id TEXT,detail TEXT,at TEXT,prev_hash TEXT,hash TEXT);
 CREATE TABLE IF NOT EXISTS record_versions(id INTEGER PRIMARY KEY AUTOINCREMENT,record_id TEXT,patient_id TEXT,entity_type TEXT,version INTEGER,status TEXT,data_json TEXT,actor_id TEXT,actor_role TEXT,reason TEXT,at TEXT);
 CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id TEXT,role TEXT,expires_at TEXT);
 CREATE TABLE IF NOT EXISTS user_accounts(id TEXT PRIMARY KEY,username TEXT UNIQUE,display_name TEXT,role TEXT,professional_id TEXT,pin_salt TEXT,pin_hash TEXT,active INTEGER,demo_account INTEGER,failed_attempts INTEGER,locked_until TEXT,created_at TEXT,updated_at TEXT);
 CREATE INDEX IF NOT EXISTS idx_user_accounts_role ON user_accounts(role,active);
 CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY,patient_id TEXT,title TEXT,filename TEXT,mime TEXT,category TEXT,document_type TEXT,source_institution TEXT,document_date TEXT,content BLOB,uploaded_by TEXT,uploaded_at TEXT);
 CREATE TABLE IF NOT EXISTS document_facts(id TEXT PRIMARY KEY,patient_id TEXT,document_id TEXT,fact_name TEXT,fact_value TEXT,code_system TEXT,code TEXT,page_ref TEXT,section_ref TEXT,source_snippet TEXT,extraction_method TEXT,confidence REAL,status TEXT,validated_by TEXT,validated_at TEXT,created_at TEXT);
 CREATE INDEX IF NOT EXISTS idx_document_facts_patient ON document_facts(patient_id,document_id,status);
 CREATE TABLE IF NOT EXISTS integration_adapters(id TEXT PRIMARY KEY,name TEXT,standard TEXT,status TEXT,last_checked_at TEXT,notes TEXT);
 CREATE TABLE IF NOT EXISTS finance_schemes(id TEXT PRIMARY KEY,name TEXT,version TEXT,status TEXT,verification_mode TEXT,required_fields_json TEXT,package_model_json TEXT,source_ref TEXT,updated_at TEXT);
 CREATE TABLE IF NOT EXISTS finance_tariffs(id TEXT PRIMARY KEY,drug_code TEXT,drug TEXT,formulation_strength_mg REAL,pack_size INTEGER,unit_price_inr REAL,version TEXT,status TEXT,source_ref TEXT,updated_at TEXT);
 CREATE TABLE IF NOT EXISTS external_tokens(token TEXT PRIMARY KEY,patient_id TEXT,consultant_name TEXT,discipline TEXT,expires_at TEXT,created_by TEXT,created_at TEXT);
 CREATE TABLE IF NOT EXISTS content_sources(id TEXT PRIMARY KEY,name TEXT,source_url TEXT,license_status TEXT,license_name TEXT,commercial_use TEXT,status TEXT,notes TEXT,created_at TEXT,updated_at TEXT);
 CREATE TABLE IF NOT EXISTS content_templates(id TEXT PRIMARY KEY,category TEXT,name TEXT,subtype TEXT,disease TEXT,setting TEXT,intent TEXT,line_of_therapy TEXT,version TEXT,status TEXT,governance_status TEXT,orderable INTEGER,source_id TEXT,source_ref TEXT,effective_date TEXT,review_due TEXT,clinical_owner TEXT,pharmacy_owner TEXT,data_json TEXT,created_at TEXT,updated_at TEXT,approved_by TEXT,approved_at TEXT,retired_at TEXT);
 CREATE TABLE IF NOT EXISTS content_formulary(id TEXT PRIMARY KEY,drug TEXT,display_name TEXT,code_system TEXT,code TEXT,version TEXT,status TEXT,source_id TEXT,source_ref TEXT,routes_json TEXT,diluents_json TEXT,formulations_json TEXT,rounding_policy TEXT,notes TEXT,pharmacy_review_json TEXT,created_at TEXT,updated_at TEXT,approved_by TEXT,approved_at TEXT,retired_at TEXT);
 CREATE TABLE IF NOT EXISTS role_surface_reviews(id TEXT PRIMARY KEY,role_surface TEXT,reviewer_role TEXT,reviewer_actor_id TEXT,verdict TEXT,note TEXT,at TEXT);
 CREATE TABLE IF NOT EXISTS patient_access(patient_id TEXT,role TEXT,scope_type TEXT,source_id TEXT,active INTEGER,granted_at TEXT,granted_by TEXT,PRIMARY KEY(patient_id,role,scope_type,source_id));
 CREATE INDEX IF NOT EXISTS idx_patient_access_role ON patient_access(role,patient_id,active);
 CREATE TABLE IF NOT EXISTS cca_validation_feedback(id TEXT PRIMARY KEY,build TEXT,patient_id TEXT,reviewer_role TEXT,reviewer_actor_id TEXT,screen_id TEXT,module TEXT,target_type TEXT,target_id TEXT,target_label TEXT,dimension TEXT,verdict TEXT,severity TEXT,expected TEXT,actual TEXT,suggestion TEXT,freeze_correct INTEGER,status TEXT,created_at TEXT,updated_at TEXT);
 CREATE INDEX IF NOT EXISTS idx_cca_validation_screen ON cca_validation_feedback(screen_id,reviewer_role,created_at);
 CREATE TABLE IF NOT EXISTS cca_validation_signoff(id TEXT PRIMARY KEY,build TEXT,specialty_role TEXT,reviewer_role TEXT,reviewer_actor_id TEXT,decision TEXT,what_to_freeze TEXT,required_changes TEXT,content_needed TEXT,integration_needed TEXT,created_at TEXT,updated_at TEXT);
 CREATE INDEX IF NOT EXISTS idx_cca_validation_signoff_role ON cca_validation_signoff(specialty_role,created_at);
 CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,patient_id TEXT,episode_id TEXT,task_type TEXT,title TEXT,status TEXT,priority TEXT,owner_role TEXT,owner_user_id TEXT,source_type TEXT,source_id TEXT,due_at TEXT,acknowledged_at TEXT,acknowledged_by TEXT,completed_at TEXT,completed_by TEXT,escalation_level INTEGER,reason TEXT,data_json TEXT,created_at TEXT,created_by TEXT,updated_at TEXT,updated_by TEXT);
 CREATE INDEX IF NOT EXISTS idx_tasks_patient_owner ON tasks(patient_id,owner_role,status,due_at);
 '''); c.commit(); seed_content_master(c); seed_pc7_masters(c); seed_user_accounts(c); c.commit(); c.close(); seed()

def actor(role):
 a=current_request_actor(role)
 if a:return a
 return USERS.get(role,{'id':'USR-UNKNOWN','name':role,'role':role})
def audit(c,pid,role,action,etype='',eid='',detail=''):
 last=c.execute('SELECT hash FROM audit ORDER BY id DESC LIMIT 1').fetchone(); prev=last['hash'] if last else 'GENESIS'; at=now(); raw='|'.join([prev,pid or '',actor(role)['id'],role,action,etype or '',eid or '',detail or '',at]); h=hashlib.sha256(raw.encode()).hexdigest(); c.execute('INSERT INTO audit(patient_id,actor_id,actor_role,action,entity_type,entity_id,detail,at,prev_hash,hash) VALUES(?,?,?,?,?,?,?,?,?,?)',(pid,actor(role)['id'],role,action,etype,eid,detail,at,prev,h))

def new_record(c,pid,typ,data,status='Draft',role='System',rid=None):
 rid=rid or f'{typ.upper()}-{uuid.uuid4().hex[:10].upper()}'; t=now(); c.execute('INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?)',(rid,pid,typ,status,1,jdump(data),t,t,actor(role)['id'],actor(role)['id'])); c.execute('INSERT INTO record_versions(record_id,patient_id,entity_type,version,status,data_json,actor_id,actor_role,reason,at) VALUES(?,?,?,?,?,?,?,?,?,?)',(rid,pid,typ,1,status,jdump(data),actor(role)['id'],role,'Created',t)); audit(c,pid,role,'CREATE',typ,rid,status); return rid

def parse_dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00'))
 except:return None

def normalize_abha(v):
 digits=re.sub(r'\D','',str(v or ''))
 if not digits:return ''
 return f'{digits[:2]}-{digits[2:6]}-{digits[6:10]}-{digits[10:14]}' if len(digits)==14 else str(v).strip()
def valid_abha(v):
 if not str(v or '').strip():return True
 return len(re.sub(r'\D','',str(v)))==14

def active_disclosure_consent(c,pid):
 con=latest(c,pid,'consent');today=date.today()
 for x in ((con or {}).get('data',{}).get('items',[])):
  if x.get('type')!='External Financial Assistance Disclosure Consent' or x.get('status')!='Signed':continue
  vf=parse_iso_date(x.get('valid_from'));vu=parse_iso_date(x.get('valid_until')) if x.get('valid_until') else None
  if vf and vf>today:continue
  if vu and vu<today:continue
  return x
 return None

def seed_user_accounts(c):
 # PC8.0 connected-multidisciplinary individual accountability: one named synthetic
 # validation account per role, PIN-protected. Idempotent — only inserts missing usernames.
 named={
 'Front Desk':('front.desk.demo','Kavya Rao — Front Desk','DEMO-FD-001'),'Intake Nurse':('intake.demo','Asha Menon — Intake Nurse','DEMO-IN-001'),'Nurse Navigator':('navigator.demo','Meera Joseph — Nurse Navigator','DEMO-NN-001'),'Medical Oncology':('mo.demo','Dr Asha Mehta','DEMO-MO-001'),'Surgical Oncology':('surgery.demo','Dr Karan Shah','DEMO-SO-001'),'Radiation Oncology':('ro.demo','Dr Neha Rao','DEMO-RO-001'),'MDT Coordinator':('mdt.coordinator.demo','Riya Kapoor — MDT Coordinator','DEMO-MDT-CO-001'),'MDT Chair':('mdt.chair.demo','Dr Vikram Menon — MDT Chair','DEMO-MDT-CHAIR-001'),'Radiologist':('radiologist.demo','Dr Rohan Kulkarni','DEMO-RAD-001'),'Radiology Coordinator':('radiology.coordinator.demo','Isha Verma — Radiology Coordinator','DEMO-RC-001'),'Radiology Technician':('radiology.tech.demo','Dev Patel — Radiology Technician','DEMO-RTCH-001'),'Laboratory / Phlebotomy':('laboratory.demo','Nisha Das — Laboratory','DEMO-LAB-001'),'Pathology Technologist':('path.tech.demo','Amit Das — Pathology Technologist','DEMO-PT-001'),'Pathology':('pathology.demo','Dr Mira Desai','DEMO-PATH-001'),'Oncology Pharmacy':('pharmacy.demo','Priya Nair — Oncology Pharmacist','DEMO-PH-001'),'Day Care / Infusion Nurse':('daycare.demo','Anita Paul — Infusion Nurse','DEMO-DC-001'),'Radiation Dosimetrist / Planner':('planner.demo','Arvind Shah — RT Planner','DEMO-PLAN-001'),'Radiation Physicist':('physics.demo','Arvind Iyer — Medical Physicist','DEMO-PHY-001'),'Radiation Technologist':('rtt.demo','Meera Joshi — RTT','DEMO-RTT-001'),'Anaesthetist':('anaesthesia.demo','Dr Nitin Rao — Anaesthetist','DEMO-AN-001'),'Surgical Nurse':('surgical.nurse.demo','Sonia Bhat — Surgical Nurse','DEMO-SN-001'),'Blood Bank / Transfusion':('bloodbank.demo','Rahul Nair — Blood Bank','DEMO-BB-001'),'Stoma / Wound Nurse':('wound.demo','Latha Mary — Wound Nurse','DEMO-WN-001'),'Inpatient Oncology Clinician':('ipd.clinician.demo','Dr Imran Khan — IPD Oncology','DEMO-IPDC-001'),'Inpatient Oncology Nurse':('ipd.nurse.demo','Neha Paul — IPD Nurse','DEMO-IPDN-001'),'Dietitian / Nutrition':('dietitian.demo','Sara Thomas — Dietitian','DEMO-DIET-001'),'Psycho-Oncology':('psycho.demo','Dr Ritu Shah — Psycho-Oncology','DEMO-PSY-001'),'Palliative Care':('palliative.demo','Dr Aman Bose — Palliative Care','DEMO-PAL-001'),'Clinical Trials / Research':('trials.demo','Ira Sen — Trials Coordinator','DEMO-CTR-001'),'Health Information Management':('him.demo','Arun Iyer — HIM','DEMO-HIM-001'),'Finance / Billing':('finance.demo','CCA Finance Reviewer','DEMO-FIN-001'),'Biller':('biller.demo','CCA Biller','DEMO-BIL-001'),'Patient Liaison':('liaison.demo','Pooja Shah — Patient Liaison','DEMO-PL-001'),'Hospital Management / Admin':('admin.demo','CCA System Administrator','DEMO-ADM-001'),'PRE / Patient Relations Executive':('pre.patient.relations.executive.demo','Demo PRE / Patient Relations Executive','DEMO-PRE-001'),'Patient Attender':('patient.attender.demo','Demo Patient Attender','DEMO-PA-001'),'External Consultant':('external.consultant.demo','Demo External Consultant','DEMO-EXT-001')}
 creds=[]
 for idx,role in enumerate(ROLES,1):
  username,display,prof=named.get(role,(re.sub(r'[^a-z0-9]+','.',role.lower()).strip('.')+'.demo','Demo '+role,'DEMO-'+str(idx).zfill(3)))
  pin=f'CCA{idx:02d}#71';uid='UA-'+hashlib.sha256((role+'|'+username).encode()).hexdigest()[:12].upper()
  if not c.execute('SELECT 1 FROM user_accounts WHERE username=?',(username,)).fetchone():
   salt,dig=_new_pin_hash(pin);t=now();c.execute('INSERT INTO user_accounts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(uid,username,display,role,prof,salt,dig,1,1,0,'',t,t))
  creds.append((username,pin,display,role))
 try:(ROOT/'DEMO_USER_CREDENTIALS.txt').write_text('CCA V12.2-PC8.0 SYNTHETIC VALIDATION USERS — NOT FOR REAL-PATIENT PRODUCTION\n\n'+'\n'.join(f'{u} | {pin} | {d} | {r}' for u,pin,d,r in creds)+'\n',encoding='utf-8')
 except Exception:pass

def seed_finance_schemes(c):
 t=now();rows=[
  ('SCH-PMJAY','PM-JAY / Ayushman Bharat','demo-1.0','Active','External beneficiary/package verification required',['beneficiary_or_card_id','supporting_evidence'],{'package_source':'CCA/payer configuration required','definitive_eligibility':False},'Synthetic workflow structure only — verify against current official payer systems'),
  ('SCH-CGHS','CGHS','demo-1.0','Active','External entitlement/package verification required',['beneficiary_or_card_id','supporting_evidence'],{'package_source':'CCA/payer configuration required','definitive_eligibility':False},'Synthetic workflow structure only'),
  ('SCH-ESI','ESI / ESIC','demo-1.0','Active','External entitlement verification required',['beneficiary_or_card_id','supporting_evidence'],{'package_source':'CCA/payer configuration required','definitive_eligibility':False},'Synthetic workflow structure only'),
  ('SCH-STATE','State Government Scheme','demo-1.0','Active','State portal / payer verification required',['scheme_name','beneficiary_or_card_id','supporting_evidence'],{'package_source':'CCA/state configuration required','definitive_eligibility':False},'Institution-configurable state scheme workflow'),
  ('SCH-PRIVATE','Private Insurance / TPA','demo-1.0','Active','Policy / pre-authorisation verification required',['payer_name','policy_number','supporting_evidence'],{'package_source':'Payer contract configuration required','definitive_eligibility':False},'Institution-configurable insurance workflow')]
 for r in rows:c.execute('INSERT OR IGNORE INTO finance_schemes VALUES(?,?,?,?,?,?,?,?,?)',(r[0],r[1],r[2],r[3],r[4],jdump(r[5]),jdump(r[6]),r[7],t))

def seed_pc7_masters(c):
 t=now();seed_finance_schemes(c)
 for x in INTEGRATION_ADAPTER_DEFAULTS:
  c.execute('INSERT OR IGNORE INTO integration_adapters VALUES(?,?,?,?,?,?)',(x['id'],x['name'],x['standard'],x['status'],t,x.get('notes','')))
 # Synthetic financial tariff for display testing only; separate from clinical dose master.
 tariffs=[('TAR-DEMO-PER','DEMO-PER','Pertuzumab',420,1,85000),('TAR-DEMO-TRA','DEMO-TRA','Trastuzumab',150,1,35000),('TAR-DEMO-DOC80','DEMO-DOC','Docetaxel',80,1,6000),('TAR-DEMO-DOC20','DEMO-DOC','Docetaxel',20,1,1800),('TAR-DEMO-CAR450','DEMO-CARBO','Carboplatin',450,1,4500),('TAR-DEMO-CAR150','DEMO-CARBO','Carboplatin',150,1,1900),('TAR-DEMO-PEG','DEMO-PEG','Pegfilgrastim',6,1,9000),('TAR-DEMO-DEX','DEMO-DEX','Dexamethasone',4,10,50)]
 for r in tariffs:c.execute('INSERT OR IGNORE INTO finance_tariffs VALUES(?,?,?,?,?,?,?,?,?,?)',(*r,'1.0-synthetic','Active','Synthetic demo tariff — not CCA commercial tariff',t))

def age_years(dob):
 try:
  d=date.fromisoformat(str(dob)[:10]);today=date.today();return today.year-d.year-((today.month,today.day)<(d.month,d.day))
 except:return None

def renal_context_from_readiness(ready):
 d=(ready or {}).get('data',{}) if isinstance(ready,dict) else (ready or {})
 return {'method':d.get('renal_dosing_method'),'value_ml_min':d.get('renal_dosing_value_ml_min'),'source_id':d.get('renal_dosing_source_id'),'measured_at':d.get('renal_dosing_measured_at')}

def actual_cumulative_exposure(c,pid,drug):
 total=0.0;events=[]
 for inf in many(c,pid,'infusion'):
  for m in inf.get('data',{}).get('mar',[]):
   if str(m.get('drug','')).lower()==str(drug).lower() and m.get('completion_status') in ['Administered','Partially Administered']:
    try:v=float(m.get('actual_dose') or 0)
    except:v=0
    total+=v;events.append({'infusion_id':inf['id'],'dose':v,'unit':m.get('unit') or m.get('ordered_unit'),'at':m.get('recorded_at') or m.get('start_time')})
 return {'drug':drug,'actual_administered_total':round(total,4),'events':events}

def order_safety_recalculation(c,pid,order,protocol):
 snap=order.get('data',{}).get('patient_snapshot',{});default_renal=snap.get('renal_dosing') or {};allergies=snap.get('coded_allergies') or []
 bycode={x.get('code'):x for x in protocol.get('items',[])};results=[];errors=[]
 for oi in order.get('data',{}).get('items',[]):
  master=bycode.get(oi.get('code')) or oi;renal=oi.get('renal_dosing') or default_renal
  res=calculate_dose(master,snap.get('weight_kg'),snap.get('bsa_raw_m2') or snap.get('bsa_m2'),order.get('data',{}).get('cycle',1),renal)
  if res.get('ok'):
   chk=safety_check(master,oi.get('ordered_dose'),res,oi.get('variance_reason',''))
  else:
   # No independent cross-check is possible without governed renal-dosing provenance
   # (e.g. AUC items ordered via clinician manual entry). This is a warning, not a
   # blocker: the pharmacist's own manual verification checklist still applies.
   chk={'ok':True,'errors':[],'warnings':[f"Independent recalculation unavailable: {res.get('error')}"],'variance_pct':None,'max_dose_mg':safe_float(master.get('max_dose_mg'))}
  allergy=allergy_conflicts(allergies,master);cum=actual_cumulative_exposure(c,pid,oi.get('drug'))
  if allergy:chk['errors'].append('Direct coded allergy conflict: '+', '.join(x.get('substance','') for x in allergy));chk['ok']=False
  lim=master.get('cumulative_limit_mg')
  if lim not in [None,''] and cum['actual_administered_total']+float(oi.get('ordered_dose') or 0)>float(lim):chk['errors'].append('Projected cumulative exposure exceeds configured limit');chk['ok']=False
  row={'item_id':oi.get('item_id'),'code':oi.get('code'),'drug':oi.get('drug'),'independent_calculation':res,'safety':chk,'allergy_conflicts':allergy,'prior_actual_cumulative_exposure':cum};results.append(row);errors += [f"{oi.get('drug')}: {x}" for x in chk['errors']]
 return {'ok':not errors,'items':results,'errors':errors,'verified_at':now()}

def lab_observations(data):
 meta={'hb':('718-7','LOINC','Hemoglobin','g/dL'),'wbc':('6690-2','LOINC','Leukocytes','10^9/L'),'anc':('751-8','LOINC','Neutrophils absolute','10^9/L'),'platelets':('777-3','LOINC','Platelets','10^9/L'),'creatinine':('2160-0','LOINC','Creatinine','mg/dL'),'egfr':('98979-8','LOINC','Estimated GFR','mL/min/1.73m²'),'bilirubin':('1975-2','LOINC','Total bilirubin','mg/dL'),'ast':('1920-8','LOINC','AST','U/L'),'alt':('1742-6','LOINC','ALT','U/L')}
 units=data.get('units') or {};ranges=data.get('reference_ranges') or {};obs=[]
 for k,(code,sys,display,default_unit) in meta.items():
  if data.get(k) in [None,'']:continue
  v=data.get(k);lohi=ranges.get(k) or {};flag='Normal';
  try:
   fv=float(v);lo=safe_float(lohi.get('low'));hi=safe_float(lohi.get('high'))
   if lo is not None and fv<lo:flag='Low'
   if hi is not None and fv>hi:flag='High'
  except:pass
  crit=next((x for x in critical_lab_flags(data,units) if x.get('field')==k),None)
  if crit:flag='Critical'
  obs.append({'analyte_key':k,'code_system':sys,'code':code,'display':display,'value':v,'unit':units.get(k) or default_unit,'reference_low':lohi.get('low'),'reference_high':lohi.get('high'),'interpretation':flag,'critical':bool(crit),'specimen':data.get('specimen') or 'Blood','collected_at':data.get('collected_at') or data.get('date'),'finalized_at':data.get('finalized_at'),'source_order_id':data.get('source_order_id')})
 return obs

def mdt_quorum(c,pid):
 co=latest(c,pid,'mdt_collab');att=(co or {}).get('data',{}).get('attendance',[]);present=[x for x in att if x.get('status','Present')=='Present'];roles={x.get('discipline') or x.get('role') for x in present};chair=any(x.get('is_chair') or x.get('discipline')=='MDT Chair' for x in present);missing=[r for r in MDT_QUORUM['required_roles'] if r not in roles];ok=len(present)>=MDT_QUORUM['minimum_present'] and not missing and chair
 return {'ok':ok,'present_count':len(present),'roles':sorted(x for x in roles if x),'missing_required_roles':missing,'chair_present':chair,'rule':MDT_QUORUM}

def tariff_estimate(c,order):
 lines=[];total=0
 for i in order.get('data',{}).get('items',[]):
  dose=float(i.get('ordered_dose') or 0);rows=c.execute("SELECT * FROM finance_tariffs WHERE drug_code=? AND status='Active' ORDER BY formulation_strength_mg DESC",(i.get('code'),)).fetchall()
  candidates=[dict(r) for r in rows if float(r['formulation_strength_mg'] or 0)>0]
  if not candidates:lines.append({'drug':i.get('drug'),'ordered_dose_mg':dose,'status':'No active tariff mapping'});continue
  # Greedy vial count demo; tariff is financial only and never changes clinical dose.
  remain=dose;used=[];cost=0
  for r in candidates:
   strength=float(r['formulation_strength_mg']);n=int(remain//strength)
   if n:used.append({'strength_mg':strength,'count':n,'unit_price_inr':r['unit_price_inr']});cost+=n*float(r['unit_price_inr']);remain-=n*strength
  if remain>1e-9:
   r=candidates[-1];used.append({'strength_mg':float(r['formulation_strength_mg']),'count':1,'unit_price_inr':r['unit_price_inr']});cost+=float(r['unit_price_inr'])
  lines.append({'drug':i.get('drug'),'drug_code':i.get('code'),'ordered_dose_mg':dose,'vial_plan':used,'estimated_amount_inr':round(cost,2)});total+=cost
 return {'currency':'INR','lines':lines,'total':round(total,2),'basis':'Synthetic dose/vial-driven tariff master — not CCA commercial tariff'}

def get_rec(c,rid):
 r=c.execute('SELECT * FROM records WHERE id=?',(rid,)).fetchone();
 if not r:return None
 d=dict(r); d['data']=jload(d.pop('data_json'),{});return d

def latest(c,pid,typ):
 r=c.execute('SELECT * FROM records WHERE patient_id=? AND entity_type=? ORDER BY created_at DESC LIMIT 1',(pid,typ)).fetchone();
 if not r:return None
 d=dict(r);d['data']=jload(d.pop('data_json'),{});return d

def many(c,pid,typ):
 out=[]
 for r in c.execute('SELECT * FROM records WHERE patient_id=? AND entity_type=? ORDER BY created_at',(pid,typ)):
  d=dict(r);d['data']=jload(d.pop('data_json'),{});out.append(d)
 return out

def latest_usable(c,pid,typ,statuses):
 good=[x for x in many(c,pid,typ) if x.get('status') in set(statuses) and not x.get('data',{}).get('superseded_by_record_id')]
 return good[-1] if good else None

def update_rec(c,rid,patch,status=None,role='System',action='UPDATE',detail=''):
 r=get_rec(c,rid)
 if not r:return None
 data={**r['data'],**patch}; ver=r['version']+1; st=status or r['status']; t=now(); c.execute('UPDATE records SET status=?,version=?,data_json=?,updated_at=?,updated_by=? WHERE id=?',(st,ver,jdump(data),t,actor(role)['id'],rid)); c.execute('INSERT INTO record_versions(record_id,patient_id,entity_type,version,status,data_json,actor_id,actor_role,reason,at) VALUES(?,?,?,?,?,?,?,?,?,?)',(rid,r['patient_id'],r['entity_type'],ver,st,jdump(data),actor(role)['id'],role,detail or action,t)); audit(c,r['patient_id'],role,action,r['entity_type'],rid,detail or st); return get_rec(c,rid)


def current_episode(c,pid):
 rows=many(c,pid,'cancer_episode');active=[x for x in rows if x.get('status') in ['Active','Open']]
 return active[-1] if active else None

def ensure_episode(c,pid,role='System',kind='Primary cancer',label='Oncology episode'):
 ep=current_episode(c,pid)
 if ep:return ep
 rid=new_record(c,pid,'cancer_episode',{'episode_no':'EP-'+uuid.uuid4().hex[:6].upper(),'kind':kind,'label':label,'started_at':now(),'ended_at':'','closure_reason':'','primary_diagnosis_id':'','status':'Active'},'Active',role)
 return get_rec(c,rid)

def journey_add(c,pid,department,care_stage,status,role,source_type='',source_id='',note='',force=False):
 j=latest(c,pid,'journey')
 if not j:
  jid=new_record(c,pid,'journey',{'current_location':department,'current_care_stage':care_stage,'events':[]},'Active',role)
  j=get_rec(c,jid)
 events=list(j['data'].get('events',[])); last=events[-1] if events else None
 same=last and last.get('department')==department and last.get('care_stage')==care_stage and last.get('status')==status
 if force or not same:
  events.append({'id':'JNY-'+uuid.uuid4().hex[:8].upper(),'at':now(),'department':department,'care_stage':care_stage,'clinician':actor(role)['name'],'actor_role':role,'status':status,'source_type':source_type,'source_id':source_id,'note':note})
 update_rec(c,j['id'],{'current_location':department,'current_care_stage':care_stage,'events':events},'Active',role,'JOURNEY_STAGE',f'{department} • {care_stage} • {status}')
 c.execute('UPDATE patients SET current_department=?,updated_at=? WHERE id=?',(department,now(),pid))
 return get_rec(c,j['id'])

def close_future_work(c,pid,role,reason):
 # Cancel future appointments and stop active downstream work without deleting history.
 ap=latest(c,pid,'appointments')
 if ap:
  items=[]
  for x in ap['data'].get('items',[]):
   y=dict(x)
   if y.get('status') in ['Scheduled','Rescheduled','Pending']:
    y.update({'status':'Cancelled','reason':reason,'cancelled_at':now(),'cancelled_by':actor(role)})
   items.append(y)
  update_rec(c,ap['id'],{'items':items},'Active',role,'FUTURE_WORK_CANCEL',reason)
 for typ in ['treatment_order','pharmacy','infusion','radiation','surgery','continuous_therapy']:
  for e in many(c,pid,typ):
   if typ=='continuous_therapy':
    courses=[];changed=False
    for q in e['data'].get('courses',[]):
     z=dict(q)
     if z.get('status') not in ['Completed','Cancelled','Discontinued','Stopped']:
      z.update({'status':'Discontinued','closure_reason':reason,'closed_at':now(),'closed_by':actor(role)});changed=True
     courses.append(z)
    if changed:update_rec(c,e['id'],{'courses':courses,'closure_reason':reason,'closed_at':now(),'closed_by':actor(role)},'Discontinued',role,'EPISODE_WORK_CLOSE',reason)
   elif e['status'] not in ['Completed','Delivered','Performed','Final','Cancelled','Discontinued','Retired']:
    update_rec(c,e['id'],{'closure_reason':reason,'closed_at':now(),'closed_by':actor(role)},'Cancelled',role,'EPISODE_WORK_CLOSE',reason)
 c.execute("UPDATE tasks SET status='Cancelled',reason=?,updated_at=?,updated_by=? WHERE patient_id=? AND status IN ('Open','Acknowledged')",(reason,now(),actor(role)['id'],pid))

def external_historical_regimen_templates():
 path=ROOT/'clinical_content'/'openmrs_historical_regimens.json'
 if not path.exists():return []
 try: payload=json.loads(path.read_text(encoding='utf-8'))
 except Exception:return []
 out=[]
 for r in payload.get('regimens',[]):
  rid=r.get('id')
  if not rid:continue
  d={'id':rid,'version':'OpenMRS-historical-import-1','name':r.get('name',rid),'cycle_length_days':r.get('cycle_length_days'),'planned_cycles':r.get('planned_cycles'),'items':r.get('items',[]),'hold_parameters':{},'references':[r.get('source_ref','')],'source_blob_sha':r.get('source_blob_sha',''),'source_repository':payload.get('source_repository',''),'source_branch':payload.get('source_branch',''),'license':payload.get('license',''),'limitations':['Historical source reference only; current indication, intent, line, maximum-dose rules, supportive care, preparation, readiness and dose-modification rules require local review before activation.']}
  out.append({'id':rid,'category':'Regimen','name':r.get('name',rid),'subtype':'Systemic therapy regimen','disease':r.get('disease','Historical source — mapping pending'),'setting':'Historical OpenMRS regimen','intent':'Pending CCA review','line_of_therapy':'Pending CCA review','version':'OpenMRS-historical-import-1','status':'Imported Draft','governance_status':'Clinical + Pharmacy Review Required','orderable':False,'source_id':'SRC-OPENMRS-ONC','source_ref':r.get('source_ref',''),'effective_date':'','review_due':'','clinical_owner':'Pending','pharmacy_owner':'Pending','data':d})
 return out

def seed_content_master(c):
 if c.execute('SELECT COUNT(*) n FROM content_sources').fetchone()['n']==0:
  t=now()
  for x in CONTENT_SOURCES:
   c.execute('INSERT INTO content_sources VALUES(?,?,?,?,?,?,?,?,?,?)',(x['id'],x['name'],x['source_url'],x['license_status'],x['license_name'],x['commercial_use'],x['status'],x['notes'],t,t))
 if c.execute('SELECT COUNT(*) n FROM content_templates').fetchone()['n']==0:
  t=now(); merged={x['id']:x for x in CONTENT_TEMPLATES}
  # Imported historical content is loaded from a separate source-attributed file and stays non-orderable.
  for x in external_historical_regimen_templates():merged[x['id']]=x
  for x in merged.values():
   c.execute('INSERT INTO content_templates VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(x['id'],x['category'],x['name'],x.get('subtype',''),x.get('disease',''),x.get('setting',''),x.get('intent',''),x.get('line_of_therapy',''),x.get('version','1.0'),x.get('status','Draft'),x.get('governance_status','Review Required'),1 if x.get('orderable') else 0,x.get('source_id',''),x.get('source_ref',''),x.get('effective_date',''),x.get('review_due',''),x.get('clinical_owner',''),x.get('pharmacy_owner',''),jdump(x.get('data',{})),t,t,'','',''))
 # Institution formulary is an institution-level master, not patient-owned data.
 if c.execute('SELECT COUNT(*) n FROM content_formulary').fetchone()['n']==0:
  t=now()
  for i,x in enumerate(FORMULARY.get('items',[]),1):
   fid='FORM-CCA-'+str(i).zfill(3); review={'status':'Approved','by':actor('Oncology Pharmacy'),'at':t,'note':'Synthetic demo formulary seed for workflow testing only.'}
   c.execute('INSERT INTO content_formulary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(fid,x.get('drug',''),x.get('drug',''),'Local demo code system',x.get('drug_code',''), '1.0-demo','Active','SRC-CCA-DEMO','CCA V12 synthetic demo formulary',jdump(x.get('allowed_routes',[])),jdump(x.get('allowed_diluents',[])),jdump(x.get('formulations',[])),x.get('rounding_policy','No rounding'), 'Synthetic demo formulary entry — local pharmacy validation required before production.',jdump(review),t,t,'Hospital Management / Admin',t,''))
 # Synthetic institutional content pack exists solely to exercise product workflows end-to-end.
 # It is deliberately segregated by source_id and is never represented as patient-care guidance.
 qa_path=ROOT/'clinical_content'/'synthetic_institutional_test_content.json'
 if qa_path.exists():
  try:qa=json.loads(qa_path.read_text(encoding='utf-8'))
  except Exception:qa={}
  src=qa.get('source') or {}
  if src.get('id'):
   t=now();c.execute('INSERT OR REPLACE INTO content_sources VALUES(?,?,?,?,?,?,?,?,?,?)',(src['id'],src.get('name','CCA Synthetic Institutional Product-Test Content'),src.get('source_url','local://synthetic-test-content'),src.get('license_status','Synthetic / locally generated'),src.get('license_name','Not applicable — synthetic'),src.get('commercial_use','Product testing only'),src.get('status','Active — Test Only'),src.get('notes',qa.get('disclaimer','Product testing only')),t,t))
  for x in qa.get('templates',[]):
   t=now();c.execute('INSERT OR REPLACE INTO content_templates VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(x['id'],x['category'],x['name'],x.get('subtype',''),x.get('disease',''),x.get('setting',''),x.get('intent',''),x.get('line_of_therapy',''),x.get('version','1.0-synthetic-qa'),x.get('status','Active'),x.get('governance_status','Synthetic QA Activated — Product Testing Only'),1 if x.get('orderable') else 0,x.get('source_id','SRC-CCA-QA'),x.get('source_ref','Synthetic institutional test content'),x.get('effective_date',''),x.get('review_due',''),x.get('clinical_owner','Synthetic QA Reviewer'),x.get('pharmacy_owner','Synthetic QA Reviewer'),jdump(x.get('data',{})),t,t,'Synthetic QA activation',t,''))
  for x in qa.get('formulary_items',[]):
   t=now();review={'status':'Approved','by':{'name':'Synthetic QA Pharmacy Reviewer','role':'Oncology Pharmacy'},'at':t,'note':'Synthetic product-test content only.'};c.execute('INSERT OR REPLACE INTO content_formulary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(x['id'],x.get('drug',''),x.get('display_name',x.get('drug','')),x.get('code_system','CCA-SYNTHETIC-QA'),x.get('code',''),x.get('version','1.0-synthetic-qa'),x.get('status','Active'),'SRC-CCA-QA','Synthetic institutional test content',jdump(x.get('allowed_routes',[])),jdump(x.get('allowed_diluents',[])),jdump(x.get('formulations',[])),x.get('rounding_policy','No rounding'),'Synthetic product-test formulary item; not patient care.',jdump(review),t,t,'Synthetic QA activation',t,''))

def formulary_rows(c,active_only=False):
 q='SELECT * FROM content_formulary';args=[]
 if active_only:q+=' WHERE status=\'Active\''
 q+=' ORDER BY drug,version'
 out=[]
 for r in c.execute(q,args):
  d=dict(r);d['allowed_routes']=jload(d.pop('routes_json'),[]);d['allowed_diluents']=jload(d.pop('diluents_json'),[]);d['formulations']=jload(d.pop('formulations_json'),[]);d['pharmacy_review']=jload(d.pop('pharmacy_review_json'),{});out.append(d)
 return out

def formulary_one(c,fid):
 r=c.execute('SELECT * FROM content_formulary WHERE id=?',(fid,)).fetchone()
 if not r:return None
 d=dict(r);d['allowed_routes']=jload(d.pop('routes_json'),[]);d['allowed_diluents']=jload(d.pop('diluents_json'),[]);d['formulations']=jload(d.pop('formulations_json'),[]);d['pharmacy_review']=jload(d.pop('pharmacy_review_json'),{});return d

def active_formulary_map(c):
 rows=formulary_rows(c,True);m={}
 for x in rows:
  m[x.get('drug')]=x
  if x.get('code'):m[x.get('code')]=x
 return m

def content_rows(c,category=''):
 q='SELECT * FROM content_templates';args=[]
 if category:q+=' WHERE category=?';args=[category]
 q+=' ORDER BY category,disease,name,version'
 out=[]
 for r in c.execute(q,args):
  d=dict(r);d['data']=jload(d.pop('data_json'),{});d['orderable']=bool(d['orderable']);out.append(d)
 return out

def content_one(c,tid):
 r=c.execute('SELECT * FROM content_templates WHERE id=?',(tid,)).fetchone()
 if not r:return None
 d=dict(r);d['data']=jload(d.pop('data_json'),{});d['orderable']=bool(d['orderable']);return d

def content_update(c,tid,patch,role):
 x=content_one(c,tid)
 if not x:return None
 cols=['name','subtype','disease','setting','intent','line_of_therapy','version','status','governance_status','source_id','source_ref','effective_date','review_due','clinical_owner','pharmacy_owner']
 vals=[];sets=[]
 for k in cols:
  if k in patch:sets.append(k+'=?');vals.append(patch[k])
 if 'orderable' in patch:sets.append('orderable=?');vals.append(1 if patch['orderable'] else 0)
 if 'data' in patch:sets.append('data_json=?');vals.append(jdump(patch['data']))
 if 'approved_by' in patch:sets.append('approved_by=?');vals.append(patch['approved_by'])
 if 'approved_at' in patch:sets.append('approved_at=?');vals.append(patch['approved_at'])
 if 'retired_at' in patch:sets.append('retired_at=?');vals.append(patch['retired_at'])
 sets.append('updated_at=?');vals.append(now());vals.append(tid)
 c.execute('UPDATE content_templates SET '+','.join(sets)+' WHERE id=?',vals)
 audit(c,'',role,'CONTENT_TEMPLATE_UPDATE','content_template',tid,patch.get('governance_status') or patch.get('status') or 'updated')
 return content_one(c,tid)

def regimen_from_template(c,tid):
 t=content_one(c,tid)
 if not t or t['category']!='Regimen':return None
 return t

REPORT_REQUIREMENTS={
 'RPT-MDT':['mdt'],
 'RPT-TX-ORDER':['treatment_order'],
 'RPT-MAR':['treatment_order','pharmacy','infusion'],
 'RPT-RT-COMPLETE':['radiation'],
 'RPT-SURGERY':['surgery'],
 'RPT-ONC-CONSULT':['consultation'],
 'RPT-READINESS':['readiness'],
 'RPT-PHARM-VERIFY':['treatment_order','pharmacy'],
 'RPT-PHARM-PREP':['treatment_order','pharmacy'],
 'RPT-SYSTEMIC-COMPLETE':['treatment_order','pharmacy','infusion'],
 'RPT-RESPONSE':['response']}

def role_can_render_report(role,tid):
 req=REPORT_REQUIREMENTS.get(tid,[])
 return bool(req) and all(x in READ.get(role,set()) for x in req)

def _display_actor(x):
 if isinstance(x,dict):return x.get('name') or x.get('role') or x.get('id') or ''
 return x or ''

def render_report(c,pid,tid,role,record_version=''):
 tpl=content_one(c,tid)
 if not tpl or tpl.get('category')!='Report':return None,404,{'error':'Report template not found'}
 if not role_can_render_report(role,tid):return None,403,{'error':'Role is not authorized for the clinical records required by this report template'}
 pat=patient(c,pid)
 if not pat:return None,404,{'error':'Patient not found'}
 dx=latest(c,pid,'diagnosis');dxdata=dx['data'] if dx else {}
 header={'patient_name':pat.get('name'),'mrn':pat.get('mrn'),'dob':pat.get('dob'),'generated_at':now(),'generated_by':actor(role),'template_id':tpl['id'],'template_name':tpl['name'],'template_version':tpl['version'],'diagnosis':dxdata.get('cancer_type'),'stage':dxdata.get('stage_group'),'requested_record_version':record_version or 'current'}
 sections=[]
 def sec(title,data):sections.append({'title':title,'data':data if data is not None else {}})
 if tid=='RPT-MDT':
  m=latest_snapshot(c,pid,'mdt',record_version);co=latest(c,pid,'mdt_collab');sec('Cancer Context',{'diagnosis':dxdata.get('cancer_type'),'primary_site':dxdata.get('primary_site'),'histology':dxdata.get('histology'),'stage':dxdata.get('stage_group'),'performance_status_ECOG':dxdata.get('ecog'),'biomarkers':dxdata.get('biomarkers',[])});sec('MDT Recommendation',(m or {}).get('data',{}));sec('Attendance / Discussion',(co or {}).get('data',{}))
 elif tid=='RPT-TX-ORDER':
  o=latest_snapshot(c,pid,'treatment_order',record_version);sec('Signed Treatment Order',(o or {}).get('data',{}));sec('Record State',{'status':(o or {}).get('status'),'version':(o or {}).get('version')})
 elif tid=='RPT-MAR':
  o=latest_snapshot(c,pid,'treatment_order',record_version);ph=latest(c,pid,'pharmacy');inf=latest(c,pid,'infusion');sec('Signed Order Reference',(o or {}).get('data',{}));sec('Pharmacy Release',(ph or {}).get('data',{}));sec('Medication Administration Record',(inf or {}).get('data',{}))
 elif tid=='RPT-RT-COMPLETE':
  rt=latest_snapshot(c,pid,'radiation',record_version);sec('Radiation Prescription / Planning / Delivery',(rt or {}).get('data',{}));sec('TPS / OIS Boundary',{'statement':'CCA EMR records/reconciles prescription, QA, fraction delivery evidence and DICOM-RT references. It is not the treatment-planning or treatment-delivery system.'})
 elif tid=='RPT-SURGERY':
  su=latest_snapshot(c,pid,'surgery',record_version);pa=latest(c,pid,'pathology');sec('Surgical Plan / Actual Procedure',(su or {}).get('data',{}));sec('Linked Pathology',(pa or {}).get('data',{}))
 elif tid=='RPT-ONC-CONSULT':
  co=latest_snapshot(c,pid,'consultation',record_version);sec('Oncology Consultation',(co or {}).get('data',{}));sec('Cancer Context',dxdata)
 elif tid=='RPT-READINESS':
  r=latest_snapshot(c,pid,'readiness',record_version);sec('Treatment Readiness / Clearance',(r or {}).get('data',{}));sec('Record State',{'status':(r or {}).get('status'),'version':(r or {}).get('version')})
 elif tid=='RPT-PHARM-VERIFY':
  o=latest_snapshot(c,pid,'treatment_order',record_version);ph=latest(c,pid,'pharmacy');sec('Signed Order Reference',(o or {}).get('data',{}));sec('Pharmacy Verification',{'status':(ph or {}).get('status'),**((ph or {}).get('data',{}))})
 elif tid=='RPT-PHARM-PREP':
  o=latest(c,pid,'treatment_order');ph=latest(c,pid,'pharmacy');sec('Signed Order Reference',(o or {}).get('data',{}));sec('Preparation / Dispensing',{'status':(ph or {}).get('status'),**((ph or {}).get('data',{}))})
 elif tid=='RPT-SYSTEMIC-COMPLETE':
  o=latest_snapshot(c,pid,'treatment_order',record_version);ph=latest(c,pid,'pharmacy');inf=latest(c,pid,'infusion');tox=latest(c,pid,'toxicity');sec('Signed Order',(o or {}).get('data',{}));sec('Pharmacy',(ph or {}).get('data',{}));sec('Administration / MAR',(inf or {}).get('data',{}));sec('Toxicity Context',(tox or {}).get('data',{}))
 elif tid=='RPT-RESPONSE':
  r=latest_snapshot(c,pid,'response',record_version);sec('Response Assessment',(r or {}).get('data',{}))
 audit(c,pid,role,'GENERATE_REPORT','report_template',tid,tpl['name']+' v'+tpl['version'])
 source_versions=[]
 for z in sections:
  data=z.get('data') if isinstance(z,dict) else None
  if isinstance(data,dict) and data.get('version') is not None:source_versions.append({'section':z.get('title'),'version':data.get('version')})
 return {'header':header,'sections':sections,'source_versions':source_versions,'template_sections':tpl.get('data',{}).get('sections',[]),'status':'Generated from the requested authorized record version where supplied; source records remain authoritative.'},200,None

def norm_text(v):
 return re.sub(r'\s+',' ',str(v or '').strip().lower())

def duplicate_candidates(c,name='',dob='',phone='',abha='',id_number='',mrn=''):
 name=norm_text(name);phone=re.sub(r'\D','',str(phone or ''));abha=norm_text(abha);id_number=norm_text(id_number);mrn=norm_text(mrn);out=[]
 for r in c.execute('SELECT * FROM patients'):
  score=0;reasons=[]
  rn=norm_text(r['name']); rp=re.sub(r'\D','',str(r['phone'] or ''))
  if mrn and norm_text(r['mrn'])==mrn:score+=120;reasons.append('MRN exact match')
  if abha and norm_text(r['abha'])==abha:score+=120;reasons.append('ABHA exact match')
  if id_number and norm_text(r['id_number'])==id_number:score+=110;reasons.append('Government/ID exact match')
  if dob and r['dob']==dob:score+=35;reasons.append('DOB match')
  if phone and rp==phone:score+=45;reasons.append('Phone match')
  sim=SequenceMatcher(None,name,rn).ratio() if name and rn else 0
  if name and rn and name==rn:score+=55;reasons.append('Name exact match')
  elif sim>=0.88:score+=30;reasons.append(f'Name similarity {sim:.0%}')
  risk='High' if score>=100 else ('Possible' if score>=65 else 'Low')
  if score>=65:out.append({'patient_id':r['id'],'mrn':r['mrn'],'name':r['name'],'dob':r['dob'],'phone':r['phone'],'score':score,'risk':risk,'reasons':reasons})
 return sorted(out,key=lambda x:(-x['score'],x['name']))

def referral_owner_role(department):
 return {'Medical Oncology':'Medical Oncology','Surgical Oncology':'Surgical Oncology','Radiation Oncology':'Radiation Oncology'}.get(str(department or '').strip(),'Medical Oncology')

def cycle_readiness_rows(c,pid):
 return many(c,pid,'readiness')

def chemo_drug_chart(c,pid):
 plan=latest(c,pid,'treatment_plan'); orders=many(c,pid,'treatment_order'); pharmacies=many(c,pid,'pharmacy'); infusions=many(c,pid,'infusion'); readies=cycle_readiness_rows(c,pid)
 pd=plan['data'] if plan else {}; systemic=next((x for x in pd.get('phases',[]) if x.get('modality')=='Systemic Therapy' and x.get('status')!='Cancelled'),{})
 tid=systemic.get('regimen_template_id') or ((orders[-1]['data'].get('content_template_id')) if orders else '') or 'REG-CCA-TCHP-DEMO'
 tpl=content_one(c,tid) or content_one(c,'REG-CCA-TCHP-DEMO'); prot=(tpl or {}).get('data',{})
 planned=int(prot.get('planned_cycles') or 6); cycle_count=max(1,min(planned,12)); cycle_len=int(prot.get('cycle_length_days') or 21)
 start=str(systemic.get('start_target') or (orders[0]['data'].get('start_date') if orders else date.today()))[:10]
 try:start_date=date.fromisoformat(start)
 except:start_date=date.today()
 items=prot.get('items',[]) or []
 rows=[];cycles=[]
 for cy in range(1,cycle_count+1):
  ords=[o for o in orders if int(o['data'].get('cycle') or 0)==cy]; order=ords[-1] if ords else None
  ready=next((r for r in reversed(readies) if int(r['data'].get('cycle') or 0)==cy),None)
  ph=next((p for p in reversed(pharmacies) if order and p['data'].get('order_id')==order['id']),None)
  inf=next((i for i in reversed(infusions) if order and i['data'].get('order_id')==order['id']),None)
  cycle_state='Planned'
  if ready and ready['status']=='Signed':cycle_state='Readiness: '+str(ready['data'].get('decision') or 'Signed')
  if order:cycle_state='Ordered — '+order['status']
  if ph:
   cycle_state={'Verification Pending':'Pharmacy Verification Pending','Queried':'Pharmacy Query','Preparation Pending':'Pharmacy Verified / Preparation Pending','Dispensing Pending':'Prepared / Release Pending','Dispensed':'Released to '+str(ph['data'].get('dispensed_to') or 'Day Care')}.get(ph['status'],ph['status'])
  if inf:
   cycle_state={'Awaiting Pharmacy':'Awaiting Pharmacy','Ready for Verification':'Ready for Day Care','In Progress':'Administration In Progress','Completed':'Administered'}.get(inf['status'],inf['status'])
  if inf and inf['data'].get('mar'):
   adverse=[x for x in inf['data']['mar'] if x.get('completion_status') in ['Partially Administered','Held','Stopped']]
   if adverse:cycle_state=adverse[-1].get('completion_status')
  planned_date=(start_date+timedelta(days=(cy-1)*cycle_len)).isoformat()
  cycles.append({'cycle':cy,'planned_date':planned_date,'readiness':(ready or {}).get('status','Not started'),'readiness_decision':(ready or {}).get('data',{}).get('decision',''),'order_id':(order or {}).get('id',''),'order_status':(order or {}).get('status','Not ordered'),'pharmacy_status':(ph or {}).get('status','Not started'),'administration_status':(inf or {}).get('status','Not started'),'status':cycle_state})
  src_items=(order['data'].get('items',[]) if order else items)
  for q in src_items:
   mar=next((x for x in ((inf or {}).get('data',{}).get('mar',[]) if inf else []) if x.get('item_id')==q.get('item_id')),None)
   rows.append({'cycle':cy,'day':int(q.get('day') or 1),'planned_date':planned_date,'sequence':q.get('sequence'),'group':q.get('group','Treatment'),'drug':q.get('drug'),'standard_dose':q.get('protocol_dose'),'dose_basis':q.get('dose_basis'),'calculated_dose':q.get('calculated_dose'),'final_ordered_dose':q.get('ordered_dose') or q.get('final_approved_dose'),'unit':q.get('ordered_unit') or q.get('protocol_unit',''),'route':q.get('route'),'supportive_medication':q.get('group') not in ['Antineoplastic','Targeted Therapy'],'actual_administered_dose':(mar or {}).get('actual_dose'),'administration_status':(mar or {}).get('completion_status') or cycle_state})
 return {'regimen_template_id':tid,'regimen':(tpl or {}).get('name') or prot.get('name',''),'planned_cycles':cycle_count,'cycle_length_days':cycle_len,'cycles':cycles,'rows':rows}

def core_flow_snapshot(c,pid):
 reg=latest(c,pid,'registration');ref=latest(c,pid,'referral');con=latest(c,pid,'consultation');dx=latest(c,pid,'diagnosis');mdt=latest(c,pid,'mdt');plan=latest(c,pid,'treatment_plan');readies=many(c,pid,'readiness');orders=many(c,pid,'treatment_order');phs=many(c,pid,'pharmacy');infs=many(c,pid,'infusion');tox=latest(c,pid,'toxicity');rt=latest(c,pid,'radiation');su=latest(c,pid,'surgery');pa=latest(c,pid,'pathology');jour=latest(c,pid,'journey');tasks=[task_row(r) for r in c.execute("SELECT * FROM tasks WHERE patient_id=? AND status IN ('Open','Acknowledged') ORDER BY created_at",(pid,))]
 chart=chemo_drug_chart(c,pid);latest_order=orders[-1] if orders else None;latest_ph=next((p for p in reversed(phs) if latest_order and p['data'].get('order_id')==latest_order['id']),None);latest_inf=next((i for i in reversed(infs) if latest_order and i['data'].get('order_id')==latest_order['id']),None);latest_ready=readies[-1] if readies else None
 rtd=(rt or {}).get('data',{});rx=rtd.get('prescription',{});pl=rtd.get('planning',{});fx=rtd.get('fractions',[]);delivered=sum(1 for x in fx if x.get('status')=='Delivered')
 sud=(su or {}).get('data',{});ad=sud.get('adjuvant_decision') or {}
 tox_events=(tox or {}).get('data',{}).get('events',[]);last_completed_cycle=max([int(o['data'].get('cycle') or 0) for o in orders if o.get('status')=='Completed'] or [0]);next_cycle_ready=next((r for r in reversed(readies) if r.get('status')=='Signed' and int(r.get('data',{}).get('cycle') or 0)>last_completed_cycle),None)
 steps=[
  {'n':1,'name':'Registration + Referral','owner':'Front Desk','status':(ref or {}).get('status') or (reg or {}).get('status','Missing'),'source_id':(ref or {}).get('id') or (reg or {}).get('id',''),'complete':bool(reg and ref and ref['status'] in ['Assigned','Accepted','Scheduled','Seen','Closed'])},
  {'n':2,'name':'Medical Oncology Consultation + Diagnosis/Staging','owner':'Medical Oncology','status':f"{(con or {}).get('status','Missing')} / {(dx or {}).get('status','Missing')}",'source_id':(dx or {}).get('id',''),'complete':bool(con and con['status']=='Signed' and dx and dx['status']=='Verified')},
  {'n':3,'name':'MDT Decision','owner':'MDT Coordinator','status':(mdt or {}).get('status','Missing'),'source_id':(mdt or {}).get('id',''),'complete':bool(mdt and mdt['status']=='MDT Recommended')},
  {'n':4,'name':'Complete Treatment Plan','owner':(plan or {}).get('data',{}).get('responsible_specialty','Medical Oncology'),'status':(plan or {}).get('status','Missing'),'source_id':(plan or {}).get('id',''),'complete':bool(plan and plan['status'] in ['Clinician Approved','Active'])},
  {'n':5,'name':'Chemotherapy Drug Chart','owner':'Medical Oncology','status':f"{chart['planned_cycles']} cycles / {len(chart['rows'])} drug rows",'source_id':chart.get('regimen_template_id',''),'complete':bool(chart.get('rows'))},
  {'n':6,'name':'Treatment Readiness','owner':'Medical Oncology','status':(latest_ready or {}).get('data',{}).get('decision') or (latest_ready or {}).get('status','Not started'),'source_id':(latest_ready or {}).get('id',''),'complete':bool(latest_ready and latest_ready['status']=='Signed')},
  {'n':7,'name':'Pharmacy Verification → Preparation → Day Care','owner':'Oncology Pharmacy','status':(latest_ph or {}).get('status','Not started'),'source_id':(latest_ph or {}).get('id',''),'complete':bool(latest_ph and latest_ph['status']=='Dispensed')},
  {'n':8,'name':'Actual Chemotherapy Administration','owner':'Day Care / Infusion Nurse','status':(latest_inf or {}).get('status','Not started'),'source_id':(latest_inf or {}).get('id',''),'complete':bool(latest_inf and latest_inf['status']=='Completed')},
  {'n':9,'name':'Toxicity → Next-Cycle Decision','owner':'Medical Oncology','status':(('Toxicity reviewed / Cycle '+str((next_cycle_ready or {}).get('data',{}).get('cycle',''))+' readiness '+str((next_cycle_ready or {}).get('data',{}).get('decision',''))) if tox_events and next_cycle_ready else ('Toxicity recorded / next-cycle readiness pending' if tox_events else 'Awaiting toxicity review')),'source_id':(next_cycle_ready or tox or {}).get('id',''),'complete':bool(tox_events and next_cycle_ready)},
  {'n':10,'name':'Radiation Approval + Delivery','owner':'Radiation Oncology / Physics / RTT','status':f"{(rt or {}).get('status','Not started')} • {delivered}/{rx.get('fractions',0)} fractions",'source_id':(rt or {}).get('id',''),'complete':bool(rt and rt['status']=='Completed')},
  {'n':11,'name':'Surgery → Pathology → Adjuvant Decision','owner':'Surgical Oncology','status':('Adjuvant decision: '+str(ad.get('decision')) if ad else (su or {}).get('status','Not started')),'source_id':(su or {}).get('id',''),'complete':bool(su and sud.get('histopathology_link') and ad.get('decision'))},
  {'n':12,'name':'Patient Journey + Active Treatment Summary','owner':'Care Team','status':'Available','source_id':(jour or {}).get('id',''),'complete':bool(jour)},
 ]
 next_step=next((x for x in steps if not x['complete']),{'n':0,'name':'Core oncology demo flow complete','owner':'Care Team','status':'Complete','complete':True});pat=patient(c,pid);ep=current_episode(c,pid);current_cycle=max([int(o['data'].get('cycle') or 0) for o in orders] or [0])
 return {'patient':pat,'episode':(ep or {}).get('data',{}),'steps':steps,'next_step':next_step,'current_treatment':{'phase':(jour or {}).get('data',{}).get('current_care_stage',''),'location':(jour or {}).get('data',{}).get('current_location',''),'regimen':chart.get('regimen',''),'current_cycle':current_cycle,'latest_order':(latest_order or {}).get('data',{}).get('order_no',''),'latest_readiness':(latest_ready or {}).get('data',{}).get('decision',''),'pharmacy_status':(latest_ph or {}).get('status',''),'administration_status':(latest_inf or {}).get('status',''),'rt_status':(rt or {}).get('status',''),'surgery_status':(su or {}).get('status','')},'drug_chart':chart,'journey':(jour or {}).get('data',{}),'open_tasks':tasks,'latest_toxicities':tox_events[-10:]}


DEMO_SHOWCASE_CASES=[
 {'patient_id':'PAT-DEMO-CHEMO','title':'Systemic Therapy — Six-Cycle Chemotherapy','focus':'Six-cycle drug chart, readiness decisions, pharmacy preparation/release, actual MAR administration, toxicity and next-cycle decision','recommended_roles':['Medical Oncology','Oncology Pharmacy','Day Care / Infusion Nurse','Nurse Navigator']},
 {'patient_id':'PAT-DEMO-RT','title':'Radiation Oncology — Active Fraction Course','focus':'Prescription, simulation/planning, independent Physics QA, RO approval, fraction-by-fraction delivery and cumulative dose','recommended_roles':['Radiation Oncology','Radiation Physicist','Radiation Technologist','Radiology Coordinator']},
 {'patient_id':'PAT-DEMO-SURG','title':'Surgical Oncology — Surgery to Pathology to Adjuvant','focus':'Surgical plan, pre-op readiness, actual operative record, final histopathology, pStage and adjuvant handoff','recommended_roles':['Surgical Oncology','Surgical Nurse','Pathology','Medical Oncology','Stoma / Wound Nurse']},
 {'patient_id':'PAT-DEMO-IPD','title':'Inpatient Oncology — Deterioration / Multidisciplinary Support','focus':'Admission, nursing observations, critical labs, toxicity, inpatient notes, transfusion/blood-bank and discharge planning workflows','recommended_roles':['Medical Oncology','Inpatient Oncology Nurse','Laboratory / Phlebotomy','Blood Bank / Transfusion','Palliative Care','Dietitian / Nutrition']},
 {'patient_id':'PAT-DEMO-SURV','title':'Treatment Completion / Oral Therapy / Survivorship','focus':'Completed treatment summary, active oral/continuous therapy, surveillance, late effects, financial counselling and survivorship handoff','recommended_roles':['Medical Oncology','Nurse Navigator','Patient Liaison','Finance / Billing','Psycho-Oncology']},
]

def _demo_insert_patient(c,p):
 t=now();c.execute('INSERT INTO patients VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(p['id'],p['mrn'],p['name'],p['dob'],p['sex'],p.get('phone',''),p.get('abha',''),p.get('id_number',''),p.get('current_department','Medical Oncology'),'Active','',t,t))

def _demo_common(c,p,dx,stage,site,histology,focus_dept='Medical Oncology'):
 pid=p['id'];today=date.today()
 new_record(c,pid,'registration',{'arrival_type':'Synthetic showcase','assigned_specialty':focus_dept,'clinician_assignment':focus_dept+' Demo Service','route_rule':'Synthetic showcase routing','referral_doctor_name':'Dr Demo Referrer','referral_facility':'Synthetic Outside Centre','referral_network_level3':'Synthetic referral','referral_reason':'CCA product demonstration','address':'Demo City','general_consent':'Signed','photo_status':'Not required'},'Completed','System')
 new_record(c,pid,'referral',{'referral_no':'REF-'+pid[-5:],'source_type':'External clinician','referring_doctor':'Dr Demo Referrer','referring_facility':'Synthetic Outside Centre','reason':'CCA product demonstration','priority':'Routine','assigned_department':focus_dept,'assigned_clinician':focus_dept+' Demo Service','status':'Seen','history':[{'at':now(),'from':'Created','to':'Seen','by':actor('System'),'reason':'Synthetic showcase lifecycle'}]},'Seen','System')
 new_record(c,pid,'consent',{'items':[{'id':'CONS-'+pid[-5:],'type':'General Consent','version':'SYN-DEMO-v1','scope':'Synthetic demonstration only','status':'Signed','signed_by':p['name'],'signed_at':now(),'valid_from':str(today),'valid_until':str(today+timedelta(days=180))}]},'Active','System')
 new_record(c,pid,'appointments',{'items':[{'id':'APT-'+pid[-5:],'date':(datetime.now()+timedelta(days=2)).isoformat(timespec='minutes'),'department':focus_dept,'clinician':focus_dept+' Demo Service','location':'CCA Demo','purpose':'Synthetic follow-up','status':'Scheduled'}]},'Active','System')
 new_record(c,pid,'queue',{'current_location':focus_dept,'current_status':'In Service','priority':'Routine','token':'DEMO-'+pid[-3:],'history':[{'at':now(),'from':'Registration','to':focus_dept,'status':'Completed','actor':'System'}]},'Active','System')
 new_record(c,pid,'journey',{'current_location':focus_dept,'current_care_stage':'Active Oncology Care','events':[{'id':'J-'+pid[-5:],'at':now(),'department':focus_dept,'care_stage':'Active Oncology Care','clinician':'System','actor_role':'System','status':'Current','source_type':'registration','source_id':'','note':'Synthetic showcase journey'}]},'Active','System')
 new_record(c,pid,'cancer_episode',{'episode_no':'EP-'+pid[-5:],'kind':'Primary cancer','label':dx+' synthetic episode','started_at':str(today-timedelta(days=90)),'ended_at':'','closure_reason':'','primary_diagnosis_id':'','status':'Active'},'Active','System')
 new_record(c,pid,'intake',{'bp':'120/78','hr':76,'rr':16,'temp_c':36.7,'spo2':99,'weight_kg':68,'height_cm':165,'bmi':25.0,'bsa_m2':1.76,'bsa_formula':'Mosteller: sqrt(height_cm × weight_kg / 3600)','measured_at':now(),'ecog':'1','kps':'90','pain_score':1,'pain_site':site,'fall_risk_setting':'OPD','fall_risk_score':1,'fall_risk_level':'Low','past_medical':'Synthetic hypertension history','past_surgical':'Synthetic prior procedure history','family_history':'Reviewed','hormonal_history':'Reviewed','reproductive_history':'Reviewed','social_history':'No current tobacco'},'Completed','System')
 new_record(c,pid,'med_recon',{'items':[{'id':'MED-'+pid[-3:],'name':'Synthetic supportive medication','dose':'1 tablet','route':'PO','frequency':'Once daily','status':'Continue','source':'Synthetic demo'}],'allergies':[{'id':'ALG-'+pid[-3:],'substance':'Synthetic allergy example','reaction':'Rash','severity':'Mild','status':'Active','source':'Synthetic demo'}],'reconciliation_events':[{'at':now(),'reconciled_by':'Nurse Navigator','medication_count':1,'allergy_count':1,'note':'Synthetic showcase reconciliation'}]},'Active','System')
 new_record(c,pid,'consultation',{'encounter_type':'Synthetic oncology review','date':now(),'chief_complaint':'Cancer treatment review','hpi':'Synthetic longitudinal oncology history for product demonstration','ros':'No acute red flags in showcase record','physical_exam_structured':{'general':'Stable','tumor_site':site+' findings documented'},'decision_flow':{'diagnosed':'Yes','treatable':'Yes','tumor_board_required':'Yes','treatment_clearance':'Reviewed'},'assessment':dx+' — '+stage,'plan':'Continue stage-appropriate synthetic showcase workflow','signed_by':'Medical Oncology','signed_at':now()},'Signed','System')
 new_record(c,pid,'diagnosis',{'icd10':'SYN-DEMO','icd10_version':'Synthetic demo','icdo_topography':'SYN','icdo_morphology':'SYN','icdo_version':'Synthetic demo','snomed':'SYN-DEMO','cancer_type':dx,'primary_site':site,'histology':histology,'grade':'Synthetic Grade 2','stage_t':'cT2','stage_n':'cN1','stage_m':'cM0','stage_group':stage,'staging_system':'AJCC / disease-specific demo','staging_version':'Synthetic showcase','staging_basis':'Clinical','staging_date':str(today-timedelta(days=80)),'ecog':'1','disease_status':'Active treatment','treatment_intent':'Curative / disease-control showcase','biomarkers':[{'name':'Synthetic biomarker','value':'Positive','method':'Demo','date':str(today-timedelta(days=82))}]},'Verified','System')
 new_record(c,pid,'lab',{'date':str(today),'hb':11.8,'wbc':5.4,'anc':2.7,'platelets':245,'creatinine':0.8,'egfr':95,'bilirubin':0.6,'ast':24,'alt':26,'albumin':4.0,'sodium':138,'potassium':4.0,'magnesium':1.9,'calcium':9.1,'pregnancy':'Not applicable / Negative as appropriate','lvef':60,'units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalized_at':now(),'synthetic_showcase':True},'Final','System')
 new_record(c,pid,'pathology',{'date':str(today-timedelta(days=82)),'site':site,'specimen':'Synthetic diagnostic specimen','histology':histology,'grade':'2','margin_status':'Not applicable to diagnostic specimen','signed_by':'Pathology','signed_at':now(),'synthetic_showcase':True},'Final','System')
 new_record(c,pid,'radiology',{'study':'Synthetic staging imaging','date':str(today-timedelta(days=78)),'findings':'Measurable index lesion documented for showcase','impression':dx+' — '+stage+' synthetic imaging impression','esigned':True,'radiologist':'Radiologist','signed_at':now(),'synthetic_showcase':True},'Final','System')
 new_record(c,pid,'mdt',{'case_no':'MDT-'+pid[-5:],'meeting_at':(datetime.now()-timedelta(days=70)).isoformat(timespec='minutes'),'clinical_question':'Confirm multimodality sequence','clinical_summary':dx+' '+stage,'intent':'Curative / disease-control showcase','recommendation':'Proceed with documented multimodality showcase plan','alternatives':['Alternative sequence discussed'],'rationale':'Synthetic MDT consensus for product demonstration','final_consensus':'Consensus reached','specialty_responsible':focus_dept,'attendees':[{'name':'Medical Oncology','discipline':'Medical Oncology','status':'Present'},{'name':'Surgical Oncology','discipline':'Surgical Oncology','status':'Present'},{'name':'Radiation Oncology','discipline':'Radiation Oncology','status':'Present'}],'signed_by':'MDT Coordinator','signed_at':now()},'MDT Recommended','System')
 new_record(c,pid,'mdt_collab',{'comments':[{'at':now(),'role':'Radiologist','comment':'Synthetic imaging reviewed'}],'attendance':[{'role':'Pathology','status':'Present'}],'external_consultants':[]},'Active','System')
 new_record(c,pid,'mdt_followup',{'action_items':[{'id':'ACT-'+pid[-3:],'action':'Continue showcase treatment pathway','owner':focus_dept,'due':str(today+timedelta(days=3)),'status':'Open'}]},'Active','System')
 new_record(c,pid,'care_plan',{'status':'Active','goals':['Complete planned treatment','Monitor toxicity','Assess response'],'milestones':[{'id':'M1','name':'Active treatment','owner':focus_dept,'status':'In Progress'},{'id':'M2','name':'Response assessment','owner':'Medical Oncology','status':'Planned'}],'dependencies':['Signed source records','Current labs','Role handoffs']},'Active','System')
 new_record(c,pid,'toxicity',{'events':[]},'Active','System')
 new_record(c,pid,'modification',{'items':[]},'Active','System')
 new_record(c,pid,'response',{'baseline':{'date':str(today-timedelta(days=78)),'target_lesions':[{'id':'L1','site':site,'size_mm':40}],'non_target':'None significant','status':'Measurable disease'},'assessments':[]},'Active','System')
 new_record(c,pid,'finance',{'payer':'Synthetic insurance / self-pay example','payment_events':[],'estimated_total':125000,'actual_total':84000,'funding_source_status':'Counselled'},'Active','System')
 new_record(c,pid,'conversion',{'counselling_status':'Completed','payer_category':'Synthetic payer','mo_drug_estimate':{'currency':'INR','lines':[],'total':125000,'basis':'Synthetic demo estimate only'},'estimate_status':'Calculated','estimate_no':'EST-'+pid[-4:],'valid_until':str(today+timedelta(days=15)),'financial_status':'Counselled','counselled_by':{'name':'Demo Financial Counsellor'},'tracking':[]},'Active','System')
 new_record(c,pid,'treatment_history',{'episodes':[]},'Active','System')
 new_record(c,pid,'visit_summary',{'visit_date':str(today),'diagnosis_summary':dx+' '+stage,'decisions':['Continue synthetic showcase pathway'],'patient_instructions':'Synthetic instructions for UI demonstration only','next_appointment':str(today+timedelta(days=14)),'next_department':focus_dept,'signed_by':focus_dept,'signed_at':now()},'Signed','System')
 new_record(c,pid,'standards',{'items':['FHIR/mCODE mapping reference','DICOM/DICOM-RT integration boundary','CTCAE/response structures'],'note':'Synthetic product demonstration only.'},'Active','System')
 new_record(c,pid,'cca_requirements',{'note':'Showcase patient for CCA validation; values are synthetic, not clinical policy.','rows':[{'area':'Showcase','requirement':'Demonstrate connected workflow and presentation','status':'Synthetic data loaded'}]},'Active','System')
 new_record(c,pid,'admission',{'admissions':[]},'Active','System')
 new_record(c,pid,'inpatient_care',{'daily_notes':[],'nursing_observations':[],'intake_output':[],'pain_assessments':[],'toxicity_events':[],'specialty_reviews':[],'inpatient_medication_orders':[]},'Active','System')
 new_record(c,pid,'discharge',{'summaries':[]},'Active','System')
 new_record(c,pid,'continuous_therapy',{'courses':[]},'Active','System')
 new_record(c,pid,'tumor_marker',{'measurements':[]},'Active','System')
 for rr in ROLES:
  if rr!='External Consultant':grant_patient_access(c,pid,rr,'synthetic_showcase',pid,'System')


def _demo_protocol_items(weight,bsa,cycle,reduction_pct=0):
 items=[]
 for q in PROTOCOL['items']:
  calc=q['protocol_dose']
  if q['dose_basis']=='mg/kg':calc=round(q['protocol_dose']*weight,2)
  elif q['dose_basis']=='mg/m²':calc=round(q['protocol_dose']*bsa,2)
  elif q['dose_basis']=='AUC':calc=600.0
  final=calc
  reason=''
  if reduction_pct and q.get('drug')=='Docetaxel':
   final=round(calc*(1-reduction_pct/100),2);reason=f'Synthetic {reduction_pct}% dose reduction for demonstration'
  items.append({**q,'item_id':f'C{cycle}-OI-{q["sequence"]}','calculated_dose':calc,'calculated_unit':'mg','ordered_dose':final,'ordered_unit':'mg','final_approved_dose':final,'variance_pct':round((final-calc)/calc*100,1) if calc else 0,'variance_reason':reason,'rounding':'No rounding','rate_ml_hr':round(q.get('volume_ml',0)/(q.get('duration_min',60)/60),2) if q.get('volume_ml') else 0})
 return items


def _seed_chemo_case(c):
 p={'id':'PAT-DEMO-CHEMO','mrn':'CCA-SYN-CHEMO-01','name':'Ananya Shah','dob':'1979-05-18','sex':'Female','phone':'+91 90000 02001','abha':'99-0000-0000-0001','id_number':'SYN-CHEMO-ID','current_department':'Medical Oncology'};_demo_insert_patient(c,p);_demo_common(c,p,'Breast Cancer','Stage IIB','Left breast','Invasive carcinoma','Medical Oncology');pid=p['id'];today=date.today()
 biomarkers=[{'name':'ER','value':'Negative','method':'IHC','date':str(today-timedelta(days=85))},{'name':'PR','value':'Negative','method':'IHC','date':str(today-timedelta(days=85))},{'name':'HER2','value':'3+','method':'IHC','date':str(today-timedelta(days=85))}]
 dx=latest(c,pid,'diagnosis');update_rec(c,dx['id'],{'biomarkers':biomarkers,'treatment_intent':'Neoadjuvant'},'Verified','System','SHOWCASE_DX')
 new_record(c,pid,'treatment_plan',{'plan_no':'TP-SYN-CHEMO','version':1,'source_mdt_id':latest(c,pid,'mdt')['id'],'diagnosis':'Breast Cancer','stage':'Stage IIB','histology':'Invasive carcinoma','biomarkers':biomarkers,'intent':'Neoadjuvant','line_of_therapy':'1st line / neoadjuvant','disease_status':'Active treatment','sequence':['Systemic therapy x6 cycles','Response assessment','Surgery','Adjuvant review'],'phases':[{'modality':'Systemic Therapy','regimen':PROTOCOL['name'],'regimen_template_id':'REG-CCA-TCHP-DEMO','start_target':str(today-timedelta(days=63)),'duration':'6 cycles q21d','status':'Clinician Approved','responsible':'Medical Oncology'},{'modality':'Surgery','regimen':'Post-systemic reassessment','status':'Planned','responsible':'Surgical Oncology'},{'modality':'Radiation','regimen':'Post-operative review if indicated','status':'Planned','responsible':'Radiation Oncology'}]},'Clinician Approved','System')
 new_record(c,pid,'protocol_library',{'protocols':[PROTOCOL]},'Active','System');new_record(c,pid,'formulary',FORMULARY,'Active','System')
 # Cycles 1-4 readiness: proceed, proceed, modify, delay. 5/6 stay planned in chart.
 decisions={1:('Proceed as Planned',3.2,''),2:('Proceed as Planned',2.8,''),3:('Proceed with Modification',2.1,'Synthetic Grade 2 peripheral neuropathy reviewed; 10% docetaxel reduction'),4:('Delay',0.9,'Synthetic neutropenia example — repeat CBC before treatment')}
 for cy,(decision,anc,reason) in decisions.items():
  labid=f'LAB-CHEMO-C{cy}';new_record(c,pid,'lab',{'date':str(today-timedelta(days=max(0,(4-cy)*21))),'hb':11.6,'wbc':4.8 if cy<4 else 2.2,'anc':anc,'platelets':230,'creatinine':0.8,'egfr':94,'bilirubin':0.6,'ast':23,'alt':25,'albumin':4.0,'sodium':139,'potassium':4.1,'magnesium':1.9,'calcium':9.2,'pregnancy':'Negative','lvef':60,'units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalized_at':now(),'synthetic_showcase':True},'Final','System',labid)
  rd={'cycle':cy,'day':1,'ecog':'1','height_cm':165,'weight_kg':68,'bsa_m2':1.76,'vitals':{'bp':'120/78','hr':76,'rr':16,'temp':36.7,'spo2':99},'lab_date':str(today-timedelta(days=max(0,(4-cy)*21))),'lab_source_id':labid,'anc':anc,'platelets':230,'hb':11.6,'egfr':94,'bilirubin':0.6,'lvef':60,'lab_units':{'anc':'10^9/L','platelets':'10^9/L','bilirubin':'mg/dL','egfr':'mL/min/1.73m2'},'pregnancy':'Negative','infection':'No','consent':'Current','allergy_review':'Reviewed','medication_review':'Reviewed','toxicity_summary':reason or 'No treatment-limiting toxicity','decision':decision,'decision_reason':reason or 'Synthetic criteria met','signed_by':'Medical Oncology','signed_at':now(),'protocol_id':PROTOCOL['id'],'protocol_version':PROTOCOL['version'],'content_template_id':'REG-CCA-TCHP-DEMO','content_template_version':PROTOCOL['version']}
  rd['protocol_evaluation']=readiness_eval(rd,PROTOCOL);new_record(c,pid,'readiness',rd,'Signed','System',f'READY-CHEMO-C{cy}')
  if cy<=3:
   red=10 if cy==3 else 0;items=_demo_protocol_items(68,1.76,cy,red);oid=f'ORDER-CHEMO-C{cy}';order={'order_no':f'ORD-SYN-C{cy}D1','plan_id':'TP-SYN-CHEMO','protocol_id':PROTOCOL['id'],'protocol_version':PROTOCOL['version'],'regimen':PROTOCOL['name'],'content_template_id':'REG-CCA-TCHP-DEMO','content_template_version':PROTOCOL['version'],'content_source_id':'SRC-CCA-DEMO','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'1st line / neoadjuvant','cycle':cy,'day':1,'planned_cycles':6,'start_date':str(today-timedelta(days=(3-cy)*21)),'patient_snapshot':{'name':p['name'],'dob':p['dob'],'mrn':p['mrn'],'weight_kg':68,'height_cm':165,'bsa_m2':1.76,'allergies':['Synthetic allergy example — rash'],'lab_date':rd['lab_date']},'items':items,'readiness_id':f'READY-CHEMO-C{cy}','signed_by':'Medical Oncology','signed_at':now(),'locked':True}
   new_record(c,pid,'treatment_order',order,'Completed','System',oid)
   phitems=[]
   for it in items:
    phitems.append({**it,'prepared_dose':it['ordered_dose'],'prepared_unit':it['ordered_unit'],'lot_no':f'SYN-LOT-{cy}-{it["sequence"]}','expiry':'2027-01-31','prepared_volume_ml':it.get('volume_ml',0),'prepared_concentration':round(it['ordered_dose']/it.get('volume_ml',1),3) if it.get('volume_ml') else '', 'beyond_use_time':'Synthetic same-day BUD for display only'})
   ph={'order_id':oid,'decision':'Verified','verification_checks':{'identity':'Pass','regimen':'Pass','dose':'Pass','route':'Pass','allergy':'Pass','labs':'Pass','interactions':'Pass','readiness':'Pass'},'verified_actor':{'name':'Demo Oncology Pharmacist','role':'Oncology Pharmacy'},'verified_at':now(),'items':phitems,'query_history':([{'decision':'Clarification resolved','reason':'Dose modification','at':now(),'by':{'name':'Demo Pharmacist'},'message':'Cycle 3 reduction verified against signed modification','resolved':True,'response_action':'Proceed per revised order','response_note':'Signed by Medical Oncology','resolved_at':now()}] if cy==3 else []),'prepared_at':now(),'independent_check':{'status':'Passed','checked_by':'Second Demo Pharmacist','at':now()},'dispensed_to':'Day Care','manifest_no':f'MAN-SYN-C{cy}' }
   new_record(c,pid,'pharmacy',ph,'Dispensed','System',f'PHARM-CHEMO-C{cy}')
   mar=[];base=datetime.now()-timedelta(days=(3-cy)*21)
   for it in items:
    st=(base.replace(hour=9,minute=0,second=0,microsecond=0)+timedelta(minutes=(it['sequence']-1)*45));en=st+timedelta(minutes=max(10,int(it.get('duration_min') or 10)))
    mar.append({'item_id':it['item_id'],'sequence':it['sequence'],'drug':it['drug'],'ordered_dose':it['ordered_dose'],'ordered_unit':it['ordered_unit'],'actual_dose':it['ordered_dose'],'unit':it['ordered_unit'],'route':it.get('route'),'start_time':st.isoformat(timespec='minutes'),'end_time':en.isoformat(timespec='minutes'),'completion_status':'Administered','administered_by':{'name':'Demo Infusion Nurse','role':'Day Care / Infusion Nurse'},'reaction':'None' if cy!=2 else ('Mild transient flushing — resolved' if it['sequence']==2 else 'None')})
   inf={'order_id':oid,'care_setting':'Day Care','checklist':{'patient_identity':'Pass','consent':'Pass','order_match':'Pass','pharmacy_release':'Pass','access':'Pass','labs':'Pass','allergy':'Pass','readiness':'Pass'},'pre_vitals':{'bp':'118/74','hr':78,'temp_c':36.8,'spo2':99},'access':'Implanted port — patent','mar':mar,'post_vitals':{'bp':'116/72','hr':80,'temp_c':36.9,'spo2':99},'tolerance':'Completed with no serious reaction' if cy!=2 else 'Mild flushing during targeted therapy; resolved with observation','discharge_instructions':'Synthetic treatment-day instructions','next_cycle':str(today+timedelta(days=(cy)*21))}
   new_record(c,pid,'infusion',inf,'Completed','System',f'INF-CHEMO-C{cy}')
 tox=latest(c,pid,'toxicity');events=[
  {'id':'TOX-C1','toxicity_type':'Nausea','grade':1,'relationship':'Probably treatment related','onset_date':str(today-timedelta(days=55)),'intervention':'Supportive medication','outcome':'Resolved'},
  {'id':'TOX-C2','toxicity_type':'Peripheral neuropathy','grade':2,'relationship':'Probably treatment related','onset_date':str(today-timedelta(days=30)),'intervention':'Clinical review before Cycle 3','outcome':'Ongoing / stable'},
  {'id':'TOX-C4','toxicity_type':'Neutropenia','grade':2,'relationship':'Treatment related — synthetic example','onset_date':str(today),'intervention':'Cycle 4 delayed; repeat CBC planned','outcome':'Under review'}]
 update_rec(c,tox['id'],{'events':events},'Active','System','SHOWCASE_TOXICITY')
 mod=latest(c,pid,'modification');update_rec(c,mod['id'],{'items':[{'id':'MOD-C3','linked_order':'ORDER-CHEMO-C3','modification_type':'Dose Reduction','reason':'Grade 2 peripheral neuropathy — synthetic showcase','clinical_justification':'Demonstrate planned vs calculated vs final ordered dose','approved_at':now(),'approved_by':{'name':'Demo Medical Oncologist'}},{'id':'MOD-C4','linked_cycle':4,'modification_type':'Delay','reason':'ANC 0.9 ×10^9/L — synthetic showcase','clinical_justification':'Demonstrate fail-closed readiness and next-cycle decision','approved_at':now(),'approved_by':{'name':'Demo Medical Oncologist'}}]},'Active','System','SHOWCASE_MODIFICATION')
 resp=latest(c,pid,'response');update_rec(c,resp['id'],{'assessments':[{'date':str(today-timedelta(days=7)),'framework':'Synthetic RECIST-like presentation only','sum_mm':28,'baseline_sum_mm':40,'nadir_sum_mm':28,'response_category':'Partial Response — clinician confirmed','radiologist_proposal':'Partial Response','confirmed_by':'Medical Oncology','decision':'Continue planned systemic therapy after recovery'}]},'Active','System','SHOWCASE_RESPONSE')
 new_record(c,pid,'radiation',{'prescription':{'status':'Planned','site':'Left breast / regional nodes','laterality':'Left','intent':'Adjuvant','modality':'External Beam','technique':'Pending post-operative decision','total_dose_gy':'','dose_per_fraction_gy':'','fractions':'','planned_start':'','signed_by':'','signed_at':''},'planning':{'simulation_status':'Not started','contouring_status':'Not started','planning_status':'Not started','physics_qa':'Not started','physician_final_approval':'Not started','dicom_refs':{}},'fractions':[],'interruptions':[]},'Planned','System')
 new_record(c,pid,'surgery',{'plan':{'status':'Planned after systemic therapy','procedure':'Breast surgery after response assessment','intent':'Curative','site':'Breast','laterality':'Left','planned_date':str(today+timedelta(days=50))},'preop':{'anesthesia_clearance':'Pending','labs':'Pending','consent':'Pending','ready':False},'outcome':{},'histopathology_link':''},'Planned','System')
 j=latest(c,pid,'journey')
 if j: update_rec(c,j['id'],{'current_location':'Medical Oncology','current_care_stage':'Cycle 4 Delayed — Repeat CBC','events':[{'id':'J1','at':(datetime.now()-timedelta(days=85)).isoformat(),'department':'Registration','care_stage':'Registered / Referred','clinician':'System','actor_role':'System','status':'Completed','source_type':'registration','source_id':'','note':'Synthetic showcase'},{'id':'J2','at':(datetime.now()-timedelta(days=72)).isoformat(),'department':'MDT','care_stage':'MDT Recommended','clinician':'MDT Coordinator','actor_role':'MDT Coordinator','status':'Completed','source_type':'mdt','source_id':'','note':'Multimodality plan agreed'},{'id':'J3','at':(datetime.now()-timedelta(days=63)).isoformat(),'department':'Day Care','care_stage':'Cycle 1 Administered','clinician':'Demo Infusion Nurse','actor_role':'Day Care / Infusion Nurse','status':'Completed','source_type':'infusion','source_id':'INF-CHEMO-C1','note':''},{'id':'J4','at':(datetime.now()-timedelta(days=42)).isoformat(),'department':'Day Care','care_stage':'Cycle 2 Administered','clinician':'Demo Infusion Nurse','actor_role':'Day Care / Infusion Nurse','status':'Completed','source_type':'infusion','source_id':'INF-CHEMO-C2','note':'Mild transient flushing resolved'},{'id':'J5','at':(datetime.now()-timedelta(days=21)).isoformat(),'department':'Day Care','care_stage':'Cycle 3 Administered with Modification','clinician':'Demo Infusion Nurse','actor_role':'Day Care / Infusion Nurse','status':'Completed','source_type':'infusion','source_id':'INF-CHEMO-C3','note':'Docetaxel final ordered dose reduced 10% for synthetic demonstration'},{'id':'J6','at':now(),'department':'Medical Oncology','care_stage':'Cycle 4 Readiness','clinician':'Demo Medical Oncologist','actor_role':'Medical Oncology','status':'Delayed','source_type':'readiness','source_id':'READY-CHEMO-C4','note':'ANC 0.9 ×10^9/L synthetic delay example'}]},'Active','System','SHOWCASE_JOURNEY')
 create_task(c,pid,'Medical Oncology','Repeat CBC and reassess Cycle 4 readiness','Cycle Readiness','High','readiness','READY-CHEMO-C4',str(datetime.now()+timedelta(days=3)),'','Synthetic delayed cycle','', 'System')


def _seed_rt_case(c):
 p={'id':'PAT-DEMO-RT','mrn':'CCA-SYN-RT-01','name':'Neha Kulkarni','dob':'1986-03-10','sex':'Female','phone':'+91 90000 02002','abha':'99-0000-0000-0002','id_number':'SYN-RT-ID','current_department':'Radiation Oncology'};_demo_insert_patient(c,p);_demo_common(c,p,'Cervical Cancer','Stage IIB','Cervix','Squamous cell carcinoma','Radiation Oncology');pid=p['id'];today=date.today()
 new_record(c,pid,'treatment_plan',{'plan_no':'TP-SYN-RT','version':1,'source_mdt_id':latest(c,pid,'mdt')['id'],'diagnosis':'Cervical Cancer','stage':'Stage IIB','histology':'Squamous cell carcinoma','biomarkers':[],'intent':'Definitive','line_of_therapy':'Primary treatment','disease_status':'Active treatment','sequence':['External beam radiation','Brachytherapy review / local pathway'],'phases':[{'modality':'Radiation','regimen':'Synthetic definitive pelvic RT course','status':'Active','responsible':'Radiation Oncology'}]},'Active','System')
 start=today-timedelta(days=12);fractions=[]
 for n in range(1,9):
  dt=datetime.combine(start+timedelta(days=n-1),datetime.min.time()).replace(hour=11,minute=0)
  fractions.append({'fraction_number':n,'status':'Delivered','date_time':dt.isoformat(timespec='minutes'),'delivered_dose_gy':2.0,'verified_by':{'name':'Demo RTT','role':'Radiation Technologist'},'image_guidance_performed':True,'setup_variation':'Within local synthetic tolerance','toxicity':'Grade 1 fatigue' if n>=6 else 'None','reason':''})
 rt={'prescription':{'status':'RT Oncologist Approved','site':'Pelvis / cervix','laterality':'Midline','intent':'Definitive','modality':'External Beam','technique':'VMAT','energy':'6 MV','treatment_phase':1,'total_dose_gy':50.0,'dose_per_fraction_gy':2.0,'fractions':25,'frequency':'5x/week','planned_start':str(start),'concurrent_systemic_order':'None in this showcase patient','target_volumes':[{'name':'GTVp','volume_type':'GTV','margin_mm':0,'prescription_dose_gy':50.0},{'name':'CTV pelvis','volume_type':'CTV','margin_mm':0,'prescription_dose_gy':50.0},{'name':'PTV pelvis','volume_type':'PTV','margin_mm':5,'prescription_dose_gy':50.0}],'organs_at_risk':['Bladder','Rectum','Bowel','Femoral heads'],'oar_constraints':[{'organ':'Bladder','metric':'V45Gy','operator':'<','value':35,'unit':'%'},{'organ':'Rectum','metric':'V45Gy','operator':'<','value':60,'unit':'%'}],'simulation_requirement':'Completed','immobilisation':'Vacuum immobilisation — synthetic','image_guidance':'Daily CBCT — synthetic','bolus':'Not applicable','special_instructions':'Synthetic RT course for workflow/presentation validation','signed_by':{'name':'Demo Radiation Oncologist','role':'Radiation Oncology'},'signed_at':(datetime.now()-timedelta(days=20)).isoformat()},'planning':{'simulation_status':'Completed','simulation_date':str(today-timedelta(days=22)),'contouring_status':'Completed','planning_status':'Completed','physics_qa':'Approved','physics_qa_by':{'name':'Demo Radiation Physicist','role':'Radiation Physicist'},'physics_qa_at':(datetime.now()-timedelta(days=14)).isoformat(),'physician_final_approval':'Approved','physician_approved_by':{'name':'Demo Radiation Oncologist','role':'Radiation Oncology'},'physician_approved_at':(datetime.now()-timedelta(days=13)).isoformat(),'dicom_refs':{'RTSTRUCT':'SYN-RTSTRUCT-001','RTPLAN':'SYN-RTPLAN-001','RTDOSE':'SYN-RTDOSE-001','RTIMAGE':'SYN-RTIMG-001','RTRECORD':'SYN-RTRCD-001'}},'fractions':fractions,'interruptions':[],'on_treatment_reviews':[{'date':str(today-timedelta(days=5)),'toxicity':'Grade 1 fatigue','assessment':'Continue treatment','reviewed_by':'Radiation Oncology'}]}
 new_record(c,pid,'radiation',rt,'In Treatment','System','RT-SHOWCASE-001')
 j=latest(c,pid,'journey');update_rec(c,j['id'],{'current_location':'Radiation Oncology','current_care_stage':'Fraction 9 Due','events':[{'id':'RTJ1','at':(datetime.now()-timedelta(days=22)).isoformat(),'department':'Radiation Oncology','care_stage':'CT Simulation','clinician':'Demo RTT','actor_role':'Radiation Technologist','status':'Completed','source_type':'radiation','source_id':'RT-SHOWCASE-001','note':''},{'id':'RTJ2','at':(datetime.now()-timedelta(days=14)).isoformat(),'department':'Radiation Physics','care_stage':'Physics QA','clinician':'Demo Radiation Physicist','actor_role':'Radiation Physicist','status':'Completed','source_type':'radiation','source_id':'RT-SHOWCASE-001','note':'Independent QA passed'},{'id':'RTJ3','at':now(),'department':'Radiation Oncology','care_stage':'Fraction 9 Due','clinician':'Demo RTT','actor_role':'Radiation Technologist','status':'Current','source_type':'radiation','source_id':'RT-SHOWCASE-001','note':'8/25 fractions delivered'}]},'Active','System','SHOWCASE_RT_JOURNEY')
 create_task(c,pid,'Radiation Technologist','Deliver Fraction 9 after daily verification','RT Fraction','Routine','radiation','RT-SHOWCASE-001',str(datetime.now()+timedelta(days=1)),'','Active RT course','', 'System')


def _seed_surgery_case(c):
 p={'id':'PAT-DEMO-SURG','mrn':'CCA-SYN-SURG-01','name':'Arjun Mehta','dob':'1968-11-04','sex':'Male','phone':'+91 90000 02003','abha':'99-0000-0000-0003','id_number':'SYN-SURG-ID','current_department':'Surgical Oncology'};_demo_insert_patient(c,p);_demo_common(c,p,'Colon Cancer','Stage III','Sigmoid colon','Adenocarcinoma','Surgical Oncology');pid=p['id'];today=date.today()
 new_record(c,pid,'treatment_plan',{'plan_no':'TP-SYN-SURG','version':1,'source_mdt_id':latest(c,pid,'mdt')['id'],'diagnosis':'Colon Cancer','stage':'Stage III','histology':'Adenocarcinoma','intent':'Curative','line_of_therapy':'Definitive surgery','disease_status':'Post-operative','sequence':['Surgery','Final pathology','Adjuvant Medical Oncology review'],'phases':[{'modality':'Surgery','regimen':'Sigmoid colectomy — synthetic showcase','status':'Completed','responsible':'Surgical Oncology'},{'modality':'Systemic Therapy','regimen':'Adjuvant decision pending CCA-approved regimen','status':'Planned','responsible':'Medical Oncology'}]},'Active','System')
 surg={'plan':{'status':'Signed','procedure':'Laparoscopic sigmoid colectomy','indication':'Resectable sigmoid colon cancer','intent':'Curative','site':'Sigmoid colon','laterality':'Not applicable','extent':'Segmental colectomy','approach':'Laparoscopic','nodal_procedure':'Regional lymphadenectomy','reconstruction':'Primary colorectal anastomosis','planned_date':str(today-timedelta(days=12)),'priority':'Routine','preop_requirements':['Anaesthesia clearance','CBC/CMP','Imaging review','Consent','Blood availability review'],'required_imaging_pathology':['Staging CT reviewed','Diagnostic biopsy reviewed'],'anesthesia':'General','anesthesia_clearance':'Cleared','blood_requirement':'Group & save','special_instructions':'Enhanced recovery pathway — synthetic','signed_by':{'name':'Demo Surgical Oncologist'},'signed_at':(datetime.now()-timedelta(days=20)).isoformat()},'preop':{'anesthesia_clearance':'Cleared','labs':'Acceptable','consent':'Signed','site_verification':'Completed','blood_availability':'Available if required','ready':True},'outcome':{'actual_procedure':'Laparoscopic sigmoid colectomy with primary anastomosis','laterality':'Not applicable','findings':'Localized sigmoid lesion; no gross peritoneal disease in synthetic operative record','estimated_blood_loss_ml':120,'operative_time_min':165,'surgeons':['Demo Surgical Oncologist','Demo Assistant Surgeon'],'specimens':['Sigmoid colon resection — oriented','Regional lymph nodes'],'counts':'Correct','complications':'None','drains':['Pelvic drain — removed POD3'],'postop_plan':'ERAS, analgesia, DVT prophylaxis, diet advancement, pathology review','performed_at':(datetime.now()-timedelta(days=12)).isoformat(),'signed_by':{'name':'Demo Surgical Oncologist'}},'histopathology_link':'PATH-SURG-001','margin_status':'Negative / clear — synthetic','node_status':'2 / 18 positive — synthetic','postop_stage':'pT3 pN1b cM0 — Stage IIIB synthetic','adjuvant_decision':{'decision':'Adjuvant Systemic Therapy Review','rationale':'Final pathology and pathological stage reviewed; refer to Medical Oncology for CCA-approved adjuvant plan','decided_by':{'name':'Demo Surgical Oncologist'},'decided_at':now(),'receiving_role':'Medical Oncology','acknowledgement':'Pending'}}
 new_record(c,pid,'surgery',surg,'Adjuvant Review','System','SURG-SHOWCASE-001')
 new_record(c,pid,'pathology',{'date':str(today-timedelta(days=6)),'accession':'SYN-PATH-SURG-001','site':'Sigmoid colon','specimen':'Colectomy specimen + regional nodes','histology':'Adenocarcinoma','grade':'2','tumour_size_mm':42,'tumour_extent':'Invades through muscularis propria into pericolonic tissue — synthetic','margin_status':'All assessed margins negative — synthetic','closest_margin_mm':35,'nodes_examined':18,'nodes_positive':2,'lymphovascular_invasion':'Present — synthetic','perineural_invasion':'Absent — synthetic','path_t':'pT3','path_n':'pN1b','path_m':'Not pathologically assessed','stage_group':'Stage IIIB — synthetic','final_diagnosis':'Resected sigmoid colon adenocarcinoma with 2/18 regional nodes positive — synthetic product demo','signed_by':'Pathology','signed_at':now(),'synthetic_showcase':True},'Final','System','PATH-SURG-001')
 new_record(c,pid,'discharge',{'summaries':[{'admission_date':str(today-timedelta(days=12)),'discharge_date':str(today-timedelta(days=7)),'reason':'Planned cancer surgery','hospital_course':'Uncomplicated synthetic postoperative recovery','medications':'Analgesia and thromboprophylaxis per local policy — synthetic','wound_status':'Clean/dry','followup':'Surgical review + Medical Oncology adjuvant review','red_flags':'Fever, wound concerns, bowel obstruction symptoms — demo only','signed_by':'Surgical Oncology'}]},'Active','System')
 j=latest(c,pid,'journey');update_rec(c,j['id'],{'current_location':'Medical Oncology','current_care_stage':'Adjuvant Treatment Decision','events':[{'id':'SJ1','at':(datetime.now()-timedelta(days=20)).isoformat(),'department':'Surgical Oncology','care_stage':'Surgical Plan Signed','clinician':'Demo Surgical Oncologist','actor_role':'Surgical Oncology','status':'Completed','source_type':'surgery','source_id':'SURG-SHOWCASE-001','note':''},{'id':'SJ2','at':(datetime.now()-timedelta(days=12)).isoformat(),'department':'Operating Theatre','care_stage':'Surgery Performed','clinician':'Demo Surgical Oncologist','actor_role':'Surgical Oncology','status':'Completed','source_type':'surgery','source_id':'SURG-SHOWCASE-001','note':'Actual vs planned operation recorded'},{'id':'SJ3','at':(datetime.now()-timedelta(days=6)).isoformat(),'department':'Pathology','care_stage':'Final Histopathology','clinician':'Pathology','actor_role':'Pathology','status':'Completed','source_type':'pathology','source_id':'PATH-SURG-001','note':'pStage available'},{'id':'SJ4','at':now(),'department':'Medical Oncology','care_stage':'Adjuvant Review','clinician':'System','actor_role':'System','status':'Current','source_type':'surgery','source_id':'SURG-SHOWCASE-001','note':'Awaiting Medical Oncology acknowledgement'}]},'Active','System','SHOWCASE_SURG_JOURNEY')
 create_task(c,pid,'Medical Oncology','Review final surgical pathology and create adjuvant plan','Adjuvant Handoff','High','surgery','SURG-SHOWCASE-001',str(datetime.now()+timedelta(days=3)),'','Post-op adjuvant decision','', 'System')


def _seed_ipd_case(c):
 p={'id':'PAT-DEMO-IPD','mrn':'CCA-SYN-IPD-01','name':'Ravi Kapoor','dob':'1959-07-22','sex':'Male','phone':'+91 90000 02004','abha':'99-0000-0000-0004','id_number':'SYN-IPD-ID','current_department':'Inpatient Oncology'};_demo_insert_patient(c,p);_demo_common(c,p,'Diffuse Large B-cell Lymphoma','Stage III','Lymph nodes','Diffuse large B-cell lymphoma','Medical Oncology');pid=p['id'];today=date.today()
 # Replace/latest lab with a deliberately critical synthetic ANC to demonstrate closed-loop inpatient handling.
 new_record(c,pid,'lab',{'date':str(today),'hb':8.9,'wbc':1.2,'anc':0.4,'platelets':72,'creatinine':1.0,'egfr':78,'bilirubin':0.8,'ast':27,'alt':29,'albumin':3.4,'sodium':136,'potassium':3.5,'magnesium':1.7,'calcium':8.6,'pregnancy':'Not applicable','lvef':58,'units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalized_at':now(),'critical_result':{'status':'Acknowledged','finding':'ANC 0.4 ×10^9/L — synthetic critical-result showcase','communicated_to':'Inpatient Oncology','communicated_at':now(),'acknowledged_by':'Medical Oncology','acknowledged_at':now()}},'Final','System','LAB-IPD-CRIT')
 adm=latest(c,pid,'admission');update_rec(c,adm['id'],{'admissions':[{'id':'ADM-SYN-1','status':'Active','admission_date':str(today-timedelta(days=2)),'source':'Emergency / clinic','reason':'Synthetic febrile neutropenia demonstration','ward':'Oncology Ward A','bed':'A-12','responsible_consultant':'Medical Oncology','isolation':'Neutropenic precautions — synthetic','oxygen':'Room air','expected_discharge':str(today+timedelta(days=2))}]},'Active','System','SHOWCASE_ADMISSION')
 ipd=latest(c,pid,'inpatient_care');update_rec(c,ipd['id'],{'daily_notes':[{'date':str(today-timedelta(days=1)),'interval_events':'Afebrile overnight after initial supportive care — synthetic','active_problems':['Febrile neutropenia','Anaemia','Thrombocytopenia'],'exam':'Hemodynamically stable','results_reviewed':'Critical ANC acknowledged','assessment':'Improving clinically; counts remain low','plan':'Continue monitoring, repeat CBC, supportive care, discharge when clinically appropriate','signed_by':'Medical Oncology'}],'nursing_observations':[{'at':(datetime.now()-timedelta(hours=8)).isoformat(),'bp':'110/68','hr':92,'rr':18,'temp_c':37.8,'spo2':98,'oxygen':'Room air','pain':2,'ews':'Synthetic score 2','escalation':'Medical team aware'},{'at':(datetime.now()-timedelta(hours=4)).isoformat(),'bp':'116/70','hr':84,'rr':16,'temp_c':37.1,'spo2':99,'oxygen':'Room air','pain':1,'ews':'Synthetic score 1','escalation':'Continue observations'}],'intake_output':[{'shift':'Day','oral_ml':900,'iv_ml':1000,'urine_ml':1500,'other_output_ml':0,'net_ml':400}],'pain_assessments':[{'at':now(),'score':1,'site':'Generalised','intervention':'No additional analgesia required'}],'toxicity_events':[{'event':'Febrile neutropenia — synthetic','grade':'3 showcase only','status':'Improving','treatment_relationship':'Recent systemic therapy'}],'specialty_reviews':[{'service':'Dietitian / Nutrition','assessment':'Reduced appetite; high-protein oral intake plan — synthetic','date':str(today)},{'service':'Palliative Care','assessment':'Symptom support only; goals remain active treatment — synthetic','date':str(today)}],'inpatient_medication_orders':[{'medication':'Synthetic broad-spectrum antimicrobial example','dose':'Per CCA-approved protocol — not embedded','route':'IV','status':'Active'},{'medication':'IV fluids','dose':'As clinically ordered','route':'IV','status':'Active'}]},'Active','System','SHOWCASE_IPD')
 dis=latest(c,pid,'discharge');update_rec(c,dis['id'],{'summaries':[{'status':'Draft / discharge planning','target_date':str(today+timedelta(days=2)),'clinical_stability':'Improving','med_recon':'Pending final review','pending_results':['Repeat CBC'],'follow_up':'Medical Oncology within 48–72 h after discharge','red_flags':'Fever or deterioration — synthetic patient instruction'}]},'Active','System','SHOWCASE_DISCHARGE')
 tox=latest(c,pid,'toxicity');update_rec(c,tox['id'],{'events':[{'id':'IPD-TOX-1','toxicity_type':'Febrile neutropenia','grade':3,'relationship':'Treatment related — synthetic example','onset_date':str(today-timedelta(days=2)),'intervention':'Admission and supportive management','outcome':'Improving'}]},'Active','System','SHOWCASE_IPD_TOX')
 j=latest(c,pid,'journey');update_rec(c,j['id'],{'current_location':'Inpatient Oncology','current_care_stage':'Admitted — Count Recovery / Discharge Planning','events':[{'id':'IJ1','at':(datetime.now()-timedelta(days=2)).isoformat(),'department':'Inpatient Oncology','care_stage':'Admission','clinician':'Medical Oncology','actor_role':'Medical Oncology','status':'Completed','source_type':'admission','source_id':adm['id'],'note':'Synthetic febrile neutropenia admission'},{'id':'IJ2','at':now(),'department':'Inpatient Oncology','care_stage':'Count Recovery / Discharge Planning','clinician':'Medical Oncology','actor_role':'Medical Oncology','status':'Current','source_type':'inpatient_care','source_id':ipd['id'],'note':'Critical ANC acknowledged; repeat CBC pending'}]},'Active','System','SHOWCASE_IPD_JOURNEY')
 create_task(c,pid,'Laboratory / Phlebotomy','Repeat CBC for count recovery','Lab Follow-up','High','lab','LAB-IPD-CRIT',str(datetime.now()+timedelta(hours=12)),'','Inpatient monitoring','', 'System')


def _seed_survivorship_case(c):
 p={'id':'PAT-DEMO-SURV','mrn':'CCA-SYN-SURV-01','name':'Leela Nair','dob':'1972-01-14','sex':'Female','phone':'+91 90000 02005','abha':'99-0000-0000-0005','id_number':'SYN-SURV-ID','current_department':'Medical Oncology'};_demo_insert_patient(c,p);_demo_common(c,p,'Breast Cancer','Stage I','Right breast','Invasive carcinoma','Medical Oncology');pid=p['id'];today=date.today()
 # Mark active episode in surveillance phase rather than active chemotherapy.
 ep=current_episode(c,pid);update_rec(c,ep['id'],{'label':'Right breast cancer — post-treatment surveillance'},'Active','System','SHOWCASE_EPISODE')
 ct=latest(c,pid,'continuous_therapy');update_rec(c,ct['id'],{'courses':[{'id':'ORAL-SYN-1','therapy':'Synthetic oral endocrine therapy example','mode':'Oral / continuous','route':'PO','schedule':'Once daily — illustrative only','start_date':str(today-timedelta(days=180)),'end_date':'','status':'Active','episode_id':ep['id'],'prescriber':'Medical Oncology','monitoring':'Routine follow-up per CCA-approved pathway','adherence':'Good by patient report — synthetic'}]},'Active','System','SHOWCASE_ORAL')
 hist=latest(c,pid,'treatment_history');update_rec(c,hist['id'],{'episodes':[{'modality':'Surgery','treatment':'Breast-conserving surgery — synthetic','start_date':str(today-timedelta(days=300)),'end_date':str(today-timedelta(days=300)),'status':'Completed'},{'modality':'Radiation','treatment':'Adjuvant RT — synthetic','start_date':str(today-timedelta(days=250)),'end_date':str(today-timedelta(days=220)),'status':'Completed'},{'modality':'Systemic / oral','treatment':'Ongoing oral therapy — synthetic','start_date':str(today-timedelta(days=180)),'end_date':'','status':'Active'}]},'Active','System','SHOWCASE_HISTORY')
 resp=latest(c,pid,'response');update_rec(c,resp['id'],{'baseline':{'date':str(today-timedelta(days=330)),'target_lesions':[{'id':'L1','site':'Right breast','size_mm':18}],'non_target':'None','status':'Localised disease'},'assessments':[{'date':str(today-timedelta(days=30)),'framework':'Post-treatment surveillance — synthetic','sum_mm':0,'baseline_sum_mm':18,'nadir_sum_mm':0,'response_category':'No evidence of active disease in showcase record','confirmed_by':'Medical Oncology','decision':'Continue surveillance / oral therapy'}]},'Active','System','SHOWCASE_SURV_RESPONSE')
 new_record(c,pid,'treatment_plan',{'plan_no':'TP-SYN-SURV','version':3,'diagnosis':'Breast Cancer','stage':'Stage I','histology':'Invasive carcinoma','intent':'Surveillance / recurrence risk reduction','line_of_therapy':'Post-treatment follow-up','disease_status':'No evidence of active disease — synthetic','sequence':['Oral therapy monitoring','Surveillance imaging','Late-effect review'],'phases':[{'modality':'Continuous / Oral Therapy','regimen':'Synthetic oral endocrine therapy example','status':'Active','responsible':'Medical Oncology'},{'modality':'Surveillance','regimen':'Clinical follow-up and approved imaging schedule','status':'Active','responsible':'Nurse Navigator / Medical Oncology'}]},'Active','System')
 new_record(c,pid,'survivorship',{'treatment_summary':{'diagnosis':'Breast Cancer Stage I — synthetic','completed_treatments':['Surgery','Radiation'],'ongoing_treatment':'Synthetic oral therapy'},'surveillance_plan':[{'item':'Medical Oncology follow-up','interval':'Every 3–6 months — synthetic placeholder pending CCA approval','next_due':str(today+timedelta(days=90))},{'item':'Surveillance imaging','interval':'Per CCA-approved pathway','next_due':str(today+timedelta(days=120))}],'late_effects':[{'effect':'Mild fatigue','severity':'1','status':'Improving','owner':'Nurse Navigator'}],'health_maintenance':'Primary care coordination documented','patient_education':'Red flags and late-effect information issued — synthetic','signed_by':'Medical Oncology','signed_at':now()},'Signed','System')
 new_record(c,pid,'psychosocial',{'distress_score':3,'concerns':['Fear of recurrence — mild'],'intervention':'Psycho-oncology information offered','privacy_class':'Restricted clinical note — synthetic','status':'Stable'},'Active','System')
 conv=latest(c,pid,'conversion');update_rec(c,conv['id'],{'counselling_status':'Completed','payer_category':'Synthetic insurance','estimate_status':'Not applicable — surveillance','financial_status':'No current barrier','counselled_by':{'name':'Demo Financial Counsellor'}},'Active','System','SHOWCASE_FINANCE')
 j=latest(c,pid,'journey');update_rec(c,j['id'],{'current_location':'Survivorship / Follow-up','current_care_stage':'Surveillance','events':[{'id':'SVJ1','at':(datetime.now()-timedelta(days=220)).isoformat(),'department':'Radiation Oncology','care_stage':'Radiation Completed','clinician':'Radiation Oncology','actor_role':'Radiation Oncology','status':'Completed','source_type':'treatment_history','source_id':hist['id'],'note':''},{'id':'SVJ2','at':(datetime.now()-timedelta(days=180)).isoformat(),'department':'Medical Oncology','care_stage':'Oral Therapy Started','clinician':'Medical Oncology','actor_role':'Medical Oncology','status':'Completed','source_type':'continuous_therapy','source_id':ct['id'],'note':''},{'id':'SVJ3','at':now(),'department':'Survivorship / Follow-up','care_stage':'Surveillance','clinician':'Nurse Navigator','actor_role':'Nurse Navigator','status':'Current','source_type':'survivorship','source_id':'','note':'Next surveillance milestones visible'}]},'Active','System','SHOWCASE_SURV_JOURNEY')
 create_task(c,pid,'Nurse Navigator','Confirm next surveillance appointment and patient education','Survivorship Follow-up','Routine','survivorship','',str(datetime.now()+timedelta(days=14)),'','Surveillance plan','', 'System')



def _delete_seed_entity(c,pid,entity_type):
 rows=c.execute('SELECT id FROM records WHERE patient_id=? AND entity_type=?',(pid,entity_type)).fetchall()
 for r in rows:
  c.execute('DELETE FROM record_versions WHERE record_id=?',(r['id'],))
 c.execute('DELETE FROM records WHERE patient_id=? AND entity_type=?',(pid,entity_type))


def _update_showcase_diagnosis(c,pid,patch):
 r=latest(c,pid,'diagnosis')
 if r:update_rec(c,r['id'],patch,'Verified','System','PC7_SHOWCASE_DIAGNOSIS','Clinically coherent synthetic coding for showcase')


def _update_showcase_intake(c,pid):
 r=latest(c,pid,'intake')
 if not r:return
 b=bsa_values(165,68);bmi=round(68/((1.65)**2),2)
 update_rec(c,r['id'],{'weight_kg':68,'height_cm':165,'bmi':bmi,'bsa_raw_m2':b['raw'],'bsa_m2':b['ordering'],'bsa_display_m2':b['display'],'bsa_formula':b['formula_text'],'bsa_rounding_policy':{'raw_precision':b['raw_precision'],'display_precision':b['display_precision'],'ordering_precision':b['ordering_precision']},'measured_at':r['data'].get('measured_at') or now()},'Completed','System','PC7_SHOWCASE_BSA','Mosteller source measurements + explicit rounding policy')


def _rebuild_chemo_showcase(c):
 pid='PAT-DEMO-CHEMO';today=date.today();start=today-timedelta(days=63);p=patient(c,pid)
 if not p:return
 _update_showcase_intake(c,pid)
 biomarkers=[
  {'name':'ER','code_system':'LOINC / local pathology mapping','code':'ER-IHC','value':'Negative','method':'IHC','interpretation':'Negative','date':str(start-timedelta(days=22)),'source_record_id':(latest(c,pid,'pathology') or {}).get('id'),'specimen':'Core biopsy'},
  {'name':'PR','code_system':'LOINC / local pathology mapping','code':'PR-IHC','value':'Negative','method':'IHC','interpretation':'Negative','date':str(start-timedelta(days=22)),'source_record_id':(latest(c,pid,'pathology') or {}).get('id'),'specimen':'Core biopsy'},
  {'name':'HER2','code_system':'ASCO/CAP interpretation / local pathology mapping','code':'HER2-IHC','value':'3+','method':'IHC','interpretation':'Positive (IHC 3+)','date':str(start-timedelta(days=22)),'source_record_id':(latest(c,pid,'pathology') or {}).get('id'),'specimen':'Core biopsy','confirmatory_test_required':False,'confirmatory_test_reason':'IHC 3+ is represented as positive in this synthetic pathology example; production interpretation follows CCA-approved pathology policy.'}
 ]
 _update_showcase_diagnosis(c,pid,{'icd10':'C50.4','icd10_version':'ICD-10','icdo_topography':'C50.4','icdo_morphology':'8500/3','icdo_version':'ICD-O-3','snomed':'254837009','cancer_type':'Breast Cancer','primary_site':'Left breast, upper-outer quadrant','histology':'Invasive carcinoma of no special type / ductal carcinoma','grade':'3','stage_t':'cT2','stage_n':'cN1','stage_m':'cM0','stage_group':'Stage IIB','staging_system':'AJCC','staging_version':'Breast v8','staging_basis':'Clinical','staging_date':str(start-timedelta(days=20)),'disease_status':'Active treatment','treatment_intent':'Neoadjuvant','terminology_validation_status':'Validated by bundled oncology demo terminology set','terminology_service_reference':'PC7 bundled terminology v1','stage_derivation_status':'Derived and clinician confirmed','biomarkers':biomarkers})
 med=latest(c,pid,'med_recon')
 if med:update_rec(c,med['id'],{'items':[{'id':'MED-CHEMO-1','name':'Amlodipine','generic_name':'Amlodipine','code_system':'Local demo medication terminology','code':'DEMO-AMLODIPINE','dose':'5 mg','route':'PO','frequency':'Once daily','status':'Continue','source':'Patient + chart review'}],'allergies':[{'id':'ALG-CHEMO-1','substance':'Penicillin','generic_ingredient':'Penicillin','code_system':'Local demo allergy terminology','code':'DEMO-PENICILLIN','reaction':'Rash','severity':'Moderate','status':'Active','source':'Patient + chart review'}],'reconciliation_events':[{'at':now(),'reconciled_by':'Nurse Navigator','medication_count':1,'allergy_count':1,'note':'Synthetic showcase reconciliation using coded demo objects'}]},'Active','System','PC7_SHOWCASE_MEDREC')
 # Named MDT attendance / quorum: disciplines rather than anonymous role labels.
 mdt=latest(c,pid,'mdt');collab=latest(c,pid,'mdt_collab')
 attendance=[
  {'name':'Dr Meera Rao','discipline':'Medical Oncology','registration_number':'SYN-MO-001','status':'Present'},
  {'name':'Dr Arjun Sen','discipline':'Surgical Oncology','registration_number':'SYN-SO-001','status':'Present'},
  {'name':'Dr Nisha Patel','discipline':'Radiation Oncology','registration_number':'SYN-RO-001','status':'Present'},
  {'name':'Dr Kabir Shah','discipline':'Radiologist','registration_number':'SYN-RAD-001','status':'Present'},
  {'name':'Dr Tara Iyer','discipline':'Pathology','registration_number':'SYN-PATH-001','status':'Present'},
  {'name':'Dr Vikram Menon','discipline':'MDT Chair','registration_number':'SYN-MDT-CHAIR-001','status':'Present','is_chair':True}
 ]
 if collab:update_rec(c,collab['id'],{'attendance':attendance,'comments':[{'at':now(),'role':'Radiologist','comment':'Index imaging reviewed with lesion-level comparison.'},{'at':now(),'role':'Pathology','comment':'Core biopsy and biomarker interpretation reviewed.'}],'external_consultants':[]},'Active','System','PC7_SHOWCASE_MDT_ATTENDANCE')
 if mdt:update_rec(c,mdt['id'],{'clinical_summary':'HER2-positive left breast carcinoma, cT2 cN1 cM0, AJCC Breast v8 Stage IIB; ER-/PR-/HER2 IHC 3+; ECOG 1. Imaging and pathology reviewed.','attendees':attendance,'quorum_snapshot':mdt_quorum(c,pid),'signed_by':'Dr Vikram Menon — MDT Chair','signed_at':now()},'MDT Recommended','System','PC7_SHOWCASE_MDT')
 # Remove old cycle-specific order/readiness/pharmacy/MAR records and recreate coherent point-in-time history.
 for typ in ['readiness','treatment_order','pharmacy','infusion']:
  for r in many(c,pid,typ):
   if str(r['id']).startswith(('READY-CHEMO-C','ORDER-CHEMO-C','PHARM-CHEMO-C','INF-CHEMO-C')):
    c.execute('DELETE FROM record_versions WHERE record_id=?',(r['id'],));c.execute('DELETE FROM records WHERE id=?',(r['id'],))
 decisions={1:('Proceed as Planned',3.2,''),2:('Proceed as Planned',2.8,''),3:('Proceed with Modification',2.1,'CTCAE v5.0 Grade 2 peripheral sensory neuropathy reviewed; 10% docetaxel dose reduction'),4:('Delay',0.9,'ANC below synthetic governed readiness threshold; repeat CBC before treatment')}
 b=bsa_values(165,68);renal_value=94.0
 for cy,(decision,anc,reason) in decisions.items():
  cycle_date=start+timedelta(days=(cy-1)*21);lab_date=cycle_date-timedelta(days=1);labid=f'LAB-CHEMO-C{cy}'
  old=get_rec(c,labid)
  ld={'date':str(lab_date),'collected_at':(datetime.combine(lab_date,datetime.min.time()).replace(hour=8,minute=0)).isoformat(timespec='minutes'),'specimen':'Peripheral blood','source_order_id':f'LABORD-CHEMO-C{cy}','hb':11.6,'wbc':4.8 if cy<4 else 2.2,'anc':anc,'platelets':230,'creatinine':0.8,'egfr':94,'bilirubin':0.6,'ast':23,'alt':25,'albumin':4.0,'sodium':139,'potassium':4.1,'magnesium':1.9,'calcium':9.2,'pregnancy':'Negative','lvef':60,'units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'reference_ranges':{'hb':{'low':12,'high':16},'wbc':{'low':4,'high':11},'anc':{'low':1.5,'high':7.5},'platelets':{'low':150,'high':450},'creatinine':{'low':0.5,'high':1.1}},'finalized_at':(datetime.combine(lab_date,datetime.min.time()).replace(hour=10)).isoformat(timespec='minutes'),'synthetic_showcase':True}
  ld['observations']=lab_observations(ld)
  if old:update_rec(c,labid,ld,'Final','System','PC7_SHOWCASE_LAB')
  else:new_record(c,pid,'lab',ld,'Final','System',labid)
  eval_at=datetime.combine(cycle_date,datetime.min.time()).replace(hour=8,minute=30).isoformat(timespec='minutes')
  rd={'cycle':cy,'day':1,'ecog':'1','height_cm':165,'weight_kg':68,'bsa_raw_m2':b['raw'],'bsa_m2':b['ordering'],'bsa_formula':b['formula_text'],'bsa_rounding_policy':{'raw_precision':b['raw_precision'],'display_precision':b['display_precision'],'ordering_precision':b['ordering_precision']},'vitals':{'bp':'120/78','hr':76,'rr':16,'temp':36.7,'spo2':99},'lab_date':str(lab_date),'lab_source_id':labid,'anc':anc,'platelets':230,'hb':11.6,'egfr':94,'bilirubin':0.6,'lvef':60,'lab_units':{'anc':'10^9/L','platelets':'10^9/L','bilirubin':'mg/dL','egfr':'mL/min/1.73m2'},'pregnancy':'Negative','infection':'No','consent':'Current','allergy_review':'Reviewed','medication_review':'Reviewed','toxicity_summary':reason or 'No treatment-limiting toxicity','decision':decision,'decision_reason':reason or 'All synthetic governed readiness criteria met','evaluation_as_of_date':str(cycle_date),'evaluated_at':eval_at,'renal_dosing_method':'CCA-approved renal dosing value','renal_dosing_value_ml_min':renal_value,'renal_dosing_source_id':labid,'renal_dosing_measured_at':ld['finalized_at'],'signed_by':'Dr Meera Rao — Medical Oncology','signed_at':eval_at,'protocol_id':PROTOCOL['id'],'protocol_version':PROTOCOL['version'],'content_template_id':'REG-CCA-TCHP-DEMO','content_template_version':PROTOCOL['version']}
  rd['protocol_evaluation']=readiness_eval(rd,PROTOCOL,cycle_date)
  new_record(c,pid,'readiness',rd,'Signed','System',f'READY-CHEMO-C{cy}')
  if cy<=3:
   items=[];red=10 if cy==3 else 0;renal={'method':rd['renal_dosing_method'],'value_ml_min':renal_value,'source_id':labid,'measured_at':ld['finalized_at']}
   for q in PROTOCOL['items']:
    cr=calculate_dose(q,68,b['raw'],cy,renal);calc=cr['calculated_dose'];final=calc;vr=''
    if red and q.get('drug')=='Docetaxel':final=round(calc*0.90,2);vr='CTCAE v5.0 Grade 2 peripheral sensory neuropathy; synthetic 10% docetaxel reduction'
    chk=safety_check(q,final,cr,vr)
    items.append({**q,'item_id':f'C{cy}-OI-{q["sequence"]}','protocol_effective_dose':cr['trace'].get('protocol_dose'),'cycle_phase':cr['trace'].get('cycle_phase'),'calculation_trace':cr['trace'],'calculated_dose':calc,'calculated_unit':'mg','ordered_dose':final,'ordered_unit':'mg','final_approved_dose':final,'variance_pct':chk.get('variance_pct') or 0,'variance_reason':vr,'rounding':'No rounding','rate_ml_hr':round(q.get('volume_ml',0)/(q.get('duration_min',60)/60),2) if q.get('volume_ml') else 0})
   oid=f'ORDER-CHEMO-C{cy}';order={'order_no':f'ORD-SYN-C{cy}D1','plan_id':'TP-SYN-CHEMO','protocol_id':PROTOCOL['id'],'protocol_version':PROTOCOL['version'],'regimen':PROTOCOL['name'],'content_template_id':'REG-CCA-TCHP-DEMO','content_template_version':PROTOCOL['version'],'content_source_id':'SRC-CCA-DEMO','diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'1st line / neoadjuvant','cycle':cy,'day':1,'planned_cycles':6,'start_date':str(cycle_date),'patient_snapshot':{'name':p['name'],'dob':p['dob'],'mrn':p['mrn'],'weight_kg':68,'height_cm':165,'bsa_raw_m2':b['raw'],'bsa_m2':b['ordering'],'bsa_rounding_policy':BSA_POLICY,'coded_allergies':(latest(c,pid,'med_recon') or {}).get('data',{}).get('allergies',[]),'lab_date':str(lab_date),'renal_dosing':renal,'readiness_snapshot':rd['protocol_evaluation']},'items':items,'readiness_id':f'READY-CHEMO-C{cy}','signed_by':'Dr Meera Rao — Medical Oncology','signed_at':eval_at,'locked':True}
   new_record(c,pid,'treatment_order',order,'Completed','System',oid)
   orderrec=get_rec(c,oid);independent=order_safety_recalculation(c,pid,orderrec,PROTOCOL)
   phitems=[]
   for it in items:
    phitems.append({**it,'prepared_dose':it['ordered_dose'],'prepared_unit':it['ordered_unit'],'lot_no':f'SYN-LOT-{cy}-{it["sequence"]}','expiry':'2027-01-31','prepared_volume_ml':it.get('volume_ml',0),'prepared_concentration':round(it['ordered_dose']/it.get('volume_ml',1),3) if it.get('volume_ml') else '', 'beyond_use_time':'Synthetic same-day display value — production BUD from CCA pharmacy master'})
   ph={'order_id':oid,'decision':'Verified','verification_checks':{'identity':'Pass','regimen':'Pass','dose':'Pass','route':'Pass','allergy':'Pass','labs':'Pass','interactions':'Pass','readiness':'Pass'},'independent_recalculation':independent,'verified_actor':{'name':'Demo Oncology Pharmacist','role':'Oncology Pharmacy'},'verified_at':eval_at,'items':phitems,'query_history':([{'decision':'Clarification resolved','reason':'Dose modification','at':eval_at,'by':{'name':'Demo Oncology Pharmacist'},'message':'Cycle 3 dose reduction verified against signed clinician modification','resolved':True,'response_action':'Proceed per revised order','response_note':'Signed by Medical Oncology','resolved_at':eval_at}] if cy==3 else []),'prepared_at':eval_at,'independent_check':{'status':'Passed','checked_by':'Second Demo Pharmacist','at':eval_at},'dispensed_to':'Day Care','manifest_no':f'MAN-SYN-C{cy}'}
   new_record(c,pid,'pharmacy',ph,'Dispensed','System',f'PHARM-CHEMO-C{cy}')
   mar=[];base=datetime.combine(cycle_date,datetime.min.time()).replace(hour=9,minute=0)
   for it in items:
    st=(base+timedelta(days=1,hours=1)) if it.get('drug')=='Pegfilgrastim' else (base+timedelta(minutes=(it['sequence']-1)*45));en=st+timedelta(minutes=max(10,int(it.get('duration_min') or 10)))
    mar.append({'item_id':it['item_id'],'sequence':it['sequence'],'drug':it['drug'],'drug_code':it.get('code'),'ordered_dose':it['ordered_dose'],'ordered_unit':it['ordered_unit'],'actual_dose':it['ordered_dose'],'unit':it['ordered_unit'],'route':it.get('route'),'start_time':st.isoformat(timespec='minutes'),'end_time':en.isoformat(timespec='minutes'),'completion_status':'Administered','administered_by':{'name':'Demo Infusion Nurse','role':'Day Care / Infusion Nurse'},'reaction':'None' if cy!=2 else ('Mild transient flushing — resolved' if it['sequence']==2 else 'None')})
   inf={'order_id':oid,'care_setting':'Day Care','checklist':{'patient_identity':'Pass','consent':'Pass','order_match':'Pass','pharmacy_release':'Pass','access':'Pass','labs':'Pass','allergy':'Pass','readiness':'Pass'},'pre_vitals':{'bp':'118/74','hr':78,'temp_c':36.8,'spo2':99},'access':'Implanted port — patent','mar':mar,'post_vitals':{'bp':'116/72','hr':80,'temp_c':36.9,'spo2':99},'tolerance':'Completed with no serious reaction' if cy!=2 else 'Mild transient flushing during targeted therapy; resolved with observation','discharge_instructions':'Synthetic treatment-day instructions','next_cycle':str(cycle_date+timedelta(days=21))}
   new_record(c,pid,'infusion',inf,'Completed','System',f'INF-CHEMO-C{cy}')
 # CTCAE v5.0 structured toxicity and RECIST 1.1 response.
 tox=latest(c,pid,'toxicity')
 if tox:update_rec(c,tox['id'],{'events':[
  {'id':'TOX-C1','ctcae_version':'5.0','term':'Nausea','grade':1,'attribution':'Probable','suspected_agents':['Docetaxel','Carboplatin'],'seriousness':'Non-serious','sae':False,'onset_date':str(start+timedelta(days=3)),'intervention':'Supportive medication','outcome':'Resolved'},
  {'id':'TOX-C2','ctcae_version':'5.0','term':'Peripheral sensory neuropathy','grade':2,'attribution':'Probable','suspected_agents':['Docetaxel'],'seriousness':'Non-serious','sae':False,'onset_date':str(start+timedelta(days=30)),'intervention':'Clinical review before Cycle 3','outcome':'Ongoing / stable'},
  {'id':'TOX-C4','ctcae_version':'5.0','term':'Neutrophil count decreased','grade':2,'attribution':'Probable','suspected_agents':['Docetaxel','Carboplatin'],'seriousness':'Non-serious','sae':False,'onset_date':str(today),'intervention':'Cycle 4 delayed; repeat CBC planned','outcome':'Under review'}]},'Active','System','PC7_SHOWCASE_CTCAE')
 resp=latest(c,pid,'response')
 if resp:
  baseline=[{'id':'L1','organ':'Breast','site':'Left breast index lesion','lesion_type':'Non-nodal','size_mm':40,'baseline_selected':True},{'id':'L2','organ':'Lymph nodes','site':'Left axillary node short axis','lesion_type':'Lymph node','size_mm':18,'baseline_selected':True}]
  curr=[{'id':'L1','organ':'Breast','site':'Left breast index lesion','lesion_type':'Non-nodal','size_mm':26},{'id':'L2','organ':'Lymph nodes','site':'Left axillary node short axis','lesion_type':'Lymph node','size_mm':12}]
  ev=recist_evaluate(curr,baseline,[],False,'Non-target disease: non-CR/non-PD')
  update_rec(c,resp['id'],{'baseline':{'date':str(start-timedelta(days=15)),'framework':'RECIST 1.1','target_lesions':baseline,'non_target':'Non-target disease present','status':'Measurable disease'},'assessments':[{'date':str(today-timedelta(days=7)),'framework':'RECIST 1.1','target_lesions':curr,'sum_mm':ev.get('sum_mm'),'baseline_sum_mm':ev.get('baseline_sum_mm'),'nadir_sum_mm':ev.get('nadir_sum_mm'),'radiologist_proposal':ev.get('category'),'clinician_confirmed_response':ev.get('category'),'response_category':ev.get('category'),'confirmed_by':'Medical Oncology','decision':'Continue planned systemic therapy after count recovery','calculation':ev}]},'Active','System','PC7_SHOWCASE_RECIST')
 # Demonstrate source-linked document facts without pretending OCR/voice is connected.
 docid='DOC-CHEMO-PATH-001';doccontent='SYNTHETIC SOURCE DOCUMENT — product demonstration only.\nPatient: Ananya Shah\nSpecimen: Left breast core biopsy\nHistology: Invasive carcinoma of no special type.\nER: Negative by IHC.\nPR: Negative by IHC.\nHER2: IHC 3+, interpreted positive for this synthetic example.\n'.encode('utf-8')
 if not c.execute('SELECT 1 FROM documents WHERE id=?',(docid,)).fetchone():c.execute('INSERT INTO documents VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(docid,pid,'Synthetic external pathology summary','synthetic_chemo_pathology_summary.txt','text/plain','Pathology','External pathology summary','Synthetic Outside Centre',str(start-timedelta(days=22)),doccontent,actor('Pathology')['id'],now()))
 for fid,name,val,code,section,snip in [('DF-CHEMO-HIST','Histology','Invasive carcinoma of no special type','8500/3','Histology','Histology: Invasive carcinoma of no special type.'),('DF-CHEMO-HER2','HER2','IHC 3+ / Positive','HER2-IHC','Biomarkers','HER2: IHC 3+, interpreted positive for this synthetic example.')]:
  if not c.execute('SELECT 1 FROM document_facts WHERE id=?',(fid,)).fetchone():c.execute('INSERT INTO document_facts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(fid,pid,docid,name,val,'ICD-O-3' if name=='Histology' else 'Local pathology mapping',code,'1',section,snip,'Manual clinician abstraction',1.0,'Validated',actor('Pathology')['id'],now(),now()))
 # Remove the old one-of-everything empty records that make the patient clinically incoherent.
 for typ in ['admission','inpatient_care','discharge','continuous_therapy','tumor_marker','pc4_prd']:_delete_seed_entity(c,pid,typ)



def pc7_reconcile_base_patient(c):
 pid='PAT-0001';intake=get_rec(c,'INTAKE-0001');lab=get_rec(c,'LAB-0001');ready=get_rec(c,'READY-0001');order=get_rec(c,'ORDER-0001')
 if not intake or not lab or not ready or not order:return
 b=bsa_values(170,70);bmi=round(70/((1.70)**2),2)
 update_rec(c,intake['id'],{'bmi':bmi,'bsa_raw_m2':b['raw'],'bsa_m2':b['ordering'],'bsa_display_m2':b['display'],'bsa_formula':b['formula_text'],'bsa_rounding_policy':{'raw_precision':b['raw_precision'],'display_precision':b['display_precision'],'ordering_precision':b['ordering_precision']}},'Completed','System','PC7_BASE_BSA')
 ld=dict(lab['data']);ld.update({'collected_at':ld.get('collected_at') or ld.get('date'),'specimen':'Peripheral blood','source_order_id':'LABORDER-DEMO-0001','reference_ranges':{'hb':{'low':12,'high':16},'wbc':{'low':4,'high':11},'anc':{'low':1.5,'high':7.5},'platelets':{'low':150,'high':450},'creatinine':{'low':0.5,'high':1.1}},'renal_dosing_method':'CCA-approved renal dosing value','renal_dosing_value_ml_min':92.0,'renal_dosing_source_note':'Synthetic validated renal-dosing value stored separately from indexed eGFR; production source/method is CCA governed.'});ld['observations']=lab_observations(ld);update_rec(c,lab['id'],ld,'Final','System','PC7_BASE_LAB')
 rd={**ready['data'],'bsa_raw_m2':b['raw'],'bsa_m2':b['ordering'],'bsa_rounding_policy':BSA_POLICY,'evaluation_as_of_date':str(date.today()),'evaluated_at':now(),'lab_date':ld['date'],'lab_source_id':lab['id'],'renal_dosing_method':'CCA-approved renal dosing value','renal_dosing_value_ml_min':92.0,'renal_dosing_source_id':lab['id'],'renal_dosing_measured_at':ld.get('finalized_at') or ld['date']}
 rd['protocol_evaluation']=readiness_eval(rd,PROTOCOL,rd['evaluation_as_of_date']);update_rec(c,ready['id'],rd,'Signed','System','PC7_BASE_READINESS')
 renal={'method':rd['renal_dosing_method'],'value_ml_min':rd['renal_dosing_value_ml_min'],'source_id':rd['renal_dosing_source_id'],'measured_at':rd['renal_dosing_measured_at']};items=[];safety=[]
 for q in PROTOCOL['items']:
  cr=calculate_dose(q,70,b['raw'],1,renal);calc=cr['calculated_dose'];chk=safety_check(q,calc,cr,'')
  items.append({**q,'item_id':'OI-'+str(q['sequence']),'effective_protocol_dose':cr['trace'].get('protocol_dose'),'cycle_dose_phase':cr['trace'].get('cycle_phase'),'calculated_dose':calc,'calculation_trace':cr['trace'],'calculated_unit':'mg','ordered_dose':calc,'ordered_unit':'mg','final_approved_dose':calc,'variance_pct':0,'variance_reason':'','rounding':'No rounding','prior_actual_cumulative_exposure':actual_cumulative_exposure(c,pid,q['drug']),'rate_ml_hr':round(q.get('volume_ml',0)/(q.get('duration_min',60)/60),2) if q.get('volume_ml') else 0,'administration_at':datetime.now().replace(hour=10,minute=0,second=0,microsecond=0).isoformat()})
  safety.append({'drug':q['drug'],'calculation':cr,'safety':chk,'prior_actual_cumulative_exposure':actual_cumulative_exposure(c,pid,q['drug'])})
 od={**order['data'],'items':items,'dose_safety_snapshot':safety,'patient_snapshot':{**order['data'].get('patient_snapshot',{}),'weight_kg':70,'height_cm':170,'bsa_raw_m2':b['raw'],'bsa_m2':b['ordering'],'bsa_rounding_policy':BSA_POLICY,'coded_allergies':(get_rec(c,'MEDREC-0001') or {}).get('data',{}).get('allergies',[]),'readiness_id':ready['id'],'readiness_evaluation_snapshot':rd['protocol_evaluation'],'renal_dosing':renal}}
 update_rec(c,order['id'],od,'Verification Pending','System','PC7_BASE_ORDER_RECALC')
 ph=get_rec(c,'PHARM-0001')
 if ph:update_rec(c,ph['id'],{'items':[dict(x) for x in items],'independent_recalculation':None},'Verification Pending','System','PC7_BASE_PHARMACY_SYNC')


def pc7_reconcile_showcase(c):
 _rebuild_chemo_showcase(c)
 # Other showcase patients: replace obviously invalid synthetic coding with clinically recognisable structure while keeping values explicitly demonstrative.
 _update_showcase_intake(c,'PAT-DEMO-RT');_update_showcase_diagnosis(c,'PAT-DEMO-RT',{'icd10':'C53.9','icd10_version':'ICD-10','icdo_topography':'C53.9','icdo_morphology':'8070/3','icdo_version':'ICD-O-3','snomed':'','cancer_type':'Cervical Cancer','primary_site':'Cervix','histology':'Squamous cell carcinoma','grade':'2','stage_t':'cT2b','stage_n':'cN0','stage_m':'cM0','stage_group':'Stage IIB','staging_system':'FIGO','staging_version':'2018','staging_basis':'Clinical','terminology_validation_status':'Validated by synthetic showcase master','terminology_service_reference':'PC7 curated demo code set','biomarkers':[]})
 _update_showcase_intake(c,'PAT-DEMO-SURG');_update_showcase_diagnosis(c,'PAT-DEMO-SURG',{'icd10':'C18.7','icd10_version':'ICD-10','icdo_topography':'C18.7','icdo_morphology':'8140/3','icdo_version':'ICD-O-3','snomed':'','cancer_type':'Colon Cancer','primary_site':'Sigmoid colon','histology':'Adenocarcinoma','grade':'2','stage_t':'pT3','stage_n':'pN1b','stage_m':'cM0','stage_group':'Stage IIIB','staging_system':'AJCC','staging_version':'Colon/Rectum v8','staging_basis':'Pathological','terminology_validation_status':'Validated by synthetic showcase master','terminology_service_reference':'PC7 curated demo code set','biomarkers':[]})
 _update_showcase_intake(c,'PAT-DEMO-IPD');_update_showcase_diagnosis(c,'PAT-DEMO-IPD',{'icd10':'C83.3','icd10_version':'ICD-10','icdo_topography':'','icdo_morphology':'9680/3','icdo_version':'ICD-O-3','snomed':'','cancer_type':'Diffuse Large B-cell Lymphoma','primary_site':'Lymph nodes','histology':'Diffuse large B-cell lymphoma','grade':'Not applicable / high-grade lymphoma','stage_t':'','stage_n':'','stage_m':'','stage_group':'Stage III','staging_system':'Lugano / Ann Arbor','staging_version':'2014','staging_basis':'Clinical','terminology_validation_status':'Validated by synthetic showcase master','terminology_service_reference':'PC7 curated demo code set','biomarkers':[]})
 _update_showcase_intake(c,'PAT-DEMO-SURV');_update_showcase_diagnosis(c,'PAT-DEMO-SURV',{'icd10':'C50.9','icd10_version':'ICD-10','icdo_topography':'C50.9','icdo_morphology':'8500/3','icdo_version':'ICD-O-3','snomed':'254837009','cancer_type':'Breast Cancer','primary_site':'Right breast','histology':'Invasive carcinoma of no special type / ductal carcinoma','grade':'2','stage_t':'cT1','stage_n':'cN0','stage_m':'cM0','stage_group':'Stage I','staging_system':'AJCC','staging_version':'Breast v8','staging_basis':'Clinical','terminology_validation_status':'Validated by synthetic showcase master','terminology_service_reference':'PC7 curated demo code set'})
 # Keep each showcase coherent by removing unrelated empty generic modules.
 for pid,types in {
  'PAT-DEMO-RT':['admission','inpatient_care','discharge','continuous_therapy','tumor_marker'],
  'PAT-DEMO-SURG':['continuous_therapy','tumor_marker'],
  'PAT-DEMO-IPD':['continuous_therapy','tumor_marker'],
  'PAT-DEMO-SURV':['admission','inpatient_care','discharge','tumor_marker'],
 }.items():
  for typ in types:
   for r in list(many(c,pid,typ)):
    d=r.get('data',{});is_empty=not any(v for v in d.values() if v not in [[],{},'',None,False])
    if is_empty or typ in ['continuous_therapy','tumor_marker'] and pid!='PAT-DEMO-SURV':
     c.execute('DELETE FROM record_versions WHERE record_id=?',(r['id'],));c.execute('DELETE FROM records WHERE id=?',(r['id'],))
 # Update IPD toxicity into CTCAE v5 format.
 tox=latest(c,'PAT-DEMO-IPD','toxicity')
 if tox:update_rec(c,tox['id'],{'events':[{'id':'IPD-TOX-1','ctcae_version':'5.0','term':'Febrile neutropenia','grade':3,'attribution':'Probable','suspected_agents':['Recent systemic therapy — source order outside showcase'], 'seriousness':'Serious — inpatient admission','sae':True,'onset_date':str(date.today()-timedelta(days=2)),'intervention':'Admission and supportive management','outcome':'Improving'}]},'Active','System','PC7_SHOWCASE_IPD_CTCAE')


def _pc4_synth_value(f):
 typ=f.get('type');opts=f.get('options') or [];lab=f.get('label','')
 if f.get('readonly'):return None
 if typ=='select':return opts[0] if opts else 'Synthetic demo value'
 if typ=='multiselect':return opts[:1] if opts else ['Synthetic demo value']
 if typ=='number':return 1
 if typ=='date':return str(date.today())
 if typ=='datetime-local':return now()[:16]
 if typ=='time':return '10:00'
 if typ=='checkbox':return True
 return 'Synthetic showcase — '+lab[:80]

def _seed_pc4_module_examples(c,pid='PAT-DEMO-CHEMO'):
 cat=pc4_catalog();chosen={}
 for sc in cat.get('screens',[]):
  mc=sc.get('module_code');
  if mc in chosen or sc.get('kind')=='worklist':continue
  if not sc.get('author_roles'):continue
  chosen[mc]=sc
 for mc,sc in chosen.items():
  target_pid='' if mc=='C.26' else pid
  vals={}
  for f in sc.get('fields') or []:
   z=_pc4_synth_value(f)
   if z is not None:vals[f['id']]=z
  for t in sc.get('tables') or []:
   row={}
   for col in t.get('columns') or []:
    z=_pc4_synth_value(col)
    if z is not None:row[col['id']]=z
   vals['table__'+t.get('id','table')]=[row] if row else []
  data={'screen_id':sc['id'],'screen_name':sc['name'],'module':sc.get('module'),'module_code':mc,'values':vals,'derived_values':{},'source_context':{'synthetic_showcase':True,'patient_id':target_pid},'source_document':sc.get('source_document'),'requirement_ids':sc.get('requirement_ids',[]),'authored_by':actor(sc.get('author_roles',["System"])[0] if sc.get('author_roles') else 'System'),'authored_at':now(),'signed_by':actor(sc.get('author_roles',["System"])[0] if sc.get('author_roles') else 'System'),'signed_at':now(),'signature_attestation':'Synthetic showcase record for CCA product validation only','frozen_values':{'values':vals},'synthetic_showcase':True}
  new_record(c,target_pid,'pc4_prd',data,'Signed','System',f'SHOW-{mc.replace(".","")}-001')


def seed_showcase_cases(c):
 if c.execute("SELECT 1 FROM patients WHERE id='PAT-DEMO-CHEMO'").fetchone():return
 _seed_chemo_case(c);_seed_rt_case(c);_seed_surgery_case(c);_seed_ipd_case(c);_seed_survivorship_case(c);pc7_reconcile_showcase(c)

# PC8.0 connected-multidisciplinary validation patients. Distinct PAT-VAL-* ids so these
# never collide with the pre-advanced PAT-DEMO-* showcase patients above (left untouched).
# Unlike the showcase patients, these are deliberately seeded bare-registration-only --
# nothing downstream is pre-completed -- so the full role-owned handoff chain (task/handoff
# engine) has to be exercised through the UI/API to advance them, exactly as PC8.0 intended.
def seed_pc8_validation_cases(c):
 if c.execute("SELECT 1 FROM patients WHERE id='PAT-VAL-ANANYA'").fetchone():return
 disclaimer='SYNTHETIC VALIDATION DATA — NOT FOR CLINICAL USE'
 cases=[
  {'id':'PAT-VAL-ANANYA','mrn':'CCA-SYN-VAL-CHEMO-01','name':'Ananya Shah','dob':'1984-02-03','sex':'Female','phone':'917000000101','id_number':'SYN-ANANYA-01','specialty':'Medical Oncology','case_type':'Systemic Therapy','label':'HER2-positive breast cancer systemic-therapy validation','case_summary':'Synthetic Stage IIB HER2-positive breast cancer case for Registration -> MDT -> systemic treatment -> response execution.','hints':{'chief_complaint':'Left breast lump','assessment':'HER2-positive breast cancer','cancer_type':'Breast Cancer','site':'Left breast','histology':'Invasive ductal carcinoma','stage':'Stage IIB','stage_t':'cT2','stage_n':'cN1','stage_m':'cM0','intent':'Neoadjuvant','regimen':'Synthetic HER2+ Breast Neoadjuvant Demo Regimen'}},
  {'id':'PAT-VAL-NEHA','mrn':'CCA-SYN-VAL-RT-01','name':'Neha Kulkarni','dob':'1972-07-14','sex':'Female','phone':'917000000102','id_number':'SYN-NEHA-01','specialty':'Radiation Oncology','case_type':'Radiation Oncology','label':'Breast/chest-wall radiotherapy validation','case_summary':'Synthetic radiotherapy case for prescription -> simulation -> contouring -> planning -> physics QA -> release -> fraction delivery -> OTV/completion.','hints':{'cancer_type':'Breast Cancer','site':'Left chest wall / regional nodes','histology':'Invasive carcinoma','stage':'Stage IIIA','intent':'Adjuvant','rt_total_gy':50,'rt_fraction_gy':2,'rt_fractions':25}},
  {'id':'PAT-VAL-ARJUN','mrn':'CCA-SYN-VAL-SURG-01','name':'Arjun Mehta','dob':'1965-11-20','sex':'Male','phone':'917000000103','id_number':'SYN-ARJUN-01','specialty':'Surgical Oncology','case_type':'Surgery / Pathology','label':'Colorectal surgical-oncology validation','case_summary':'Synthetic surgical case for plan -> anaesthesia -> pre-op/blood readiness -> theatre -> operation -> specimen -> pathology -> pTNM -> adjuvant handoff.','hints':{'cancer_type':'Colorectal Cancer','site':'Sigmoid colon','histology':'Adenocarcinoma','stage':'Stage IIIB','stage_t':'cT3','stage_n':'cN1','stage_m':'cM0','intent':'Curative','procedure':'Laparoscopic sigmoid colectomy'}},
  {'id':'PAT-VAL-RAVI','mrn':'CCA-SYN-VAL-IPD-01','name':'Ravi Kapoor','dob':'1959-05-28','sex':'Male','phone':'917000000104','id_number':'SYN-RAVI-01','specialty':'Medical Oncology','case_type':'Inpatient Oncology','label':'Inpatient oncology validation','case_summary':'Synthetic inpatient case for admission -> nursing/clinician assessment -> orders/MAR -> deterioration escalation -> discharge -> outpatient follow-up.','hints':{'cancer_type':'Lung Cancer','site':'Right lung','histology':'Adenocarcinoma','stage':'Stage IV','intent':'Palliative','admission_reason':'Fever during active oncology treatment'}},
  {'id':'PAT-VAL-LEELA','mrn':'CCA-SYN-VAL-SURV-01','name':'Leela Nair','dob':'1977-09-09','sex':'Female','phone':'917000000105','id_number':'SYN-LEELA-01','specialty':'Medical Oncology','case_type':'Survivorship / Recurrence','label':'Treatment completion and recurrence validation','case_summary':'Synthetic survivorship case for end-of-treatment summary -> surveillance -> suspected progression -> MO confirmation -> new line -> MDT within same Cancer Episode.','hints':{'cancer_type':'Breast Cancer','site':'Right breast','histology':'Invasive ductal carcinoma','stage':'Stage IIA','intent':'Curative','surveillance_interval':'3 months'}}
 ]
 common_workspace=[
  ('consent',{'items':[]},'Active'),('appointments',{'items':[]},'Active'),('queue',{'current_location':'Front Desk','current_status':'Registered','priority':'Routine','token':'','history':[]},'Active'),('journey',{'current_location':'Front Desk','current_care_stage':'Registration','events':[]},'Active'),
  ('admission',{'admissions':[]},'Active'),('inpatient_care',{'daily_notes':[],'nursing_observations':[],'intake_output':[],'pain_assessments':[],'toxicity_events':[],'specialty_reviews':[],'medication_orders':[],'mar':[]},'Active'),('discharge',{'summaries':[]},'Active'),('continuous_therapy',{'courses':[]},'Active'),('tumor_marker',{'measurements':[]},'Active'),
  ('intake',{'nkda':True,'bp':'','hr':'','rr':'','temp_c':'','spo2':'','weight_kg':'','height_cm':'','ecog':'','kps':'','pain_score':''},'Draft'),('med_recon',{'items':[],'allergies':[],'reconciliation_events':[]},'Active'),('dynamic_forms',{'definitions':[],'responses':{}},'Active'),
  ('consultation',{},'Draft'),('diagnosis',{},'Draft'),('lab',{},'Draft'),('pathology',{},'Draft'),('radiology',{},'Draft'),('mdt',{'attendees':[]},'Draft'),('mdt_collab',{'comments':[],'attendance':[],'external_consultants':[]},'Active'),('mdt_followup',{'action_items':[]},'Active'),('care_plan',{'status':'Draft','goals':[],'milestones':[],'dependencies':[]},'Draft'),('treatment_plan',{'phases':[]},'Draft'),
  ('protocol_library',{},'Active'),('formulary',{},'Active'),('readiness',{},'Draft'),('treatment_order',{},'Draft'),('pharmacy',{},'Draft'),('infusion',{'mar':[]},'Draft'),('toxicity',{'ctcae_version':'5.0','events':[]},'Active'),('modification',{'items':[]},'Active'),('response',{'framework':'RECIST 1.1','assessments':[]},'Active'),
  ('radiation',{'prescription':{'status':'Draft'},'planning':{'simulation_status':'Pending','contouring_status':'Pending','planning_status':'Pending','physics_qa':'Pending','physician_final_approval':'Pending','dicom_refs':{}},'fractions':[],'interruptions':[],'otv':[]},'Draft'),
  ('surgery',{'plan':{'status':'Draft'},'preop':{'ready':False},'theatre_readiness':{},'outcome':{}},'Draft'),('anaesthesia',{},'Draft'),('blood_bank',{},'Draft'),('stoma_wound',{'assessments':[]},'Draft'),('pathology_processing',{},'Draft'),
  ('navigation',{},'Draft'),('nutrition',{},'Draft'),('psychosocial',{},'Draft'),('palliative',{},'Draft'),('clinical_trial',{},'Draft'),('him',{},'Draft'),('rt_planning',{},'Draft'),
  ('treatment_history',{'episodes':[]},'Active'),('visit_summary',{'items':[]},'Active'),('finance',{},'Active'),('conversion',{'counselling_status':'Not Started','scheme_assessments':[]},'Active'),('treatment_completion',{},'Draft'),('survivorship',{},'Draft'),('surveillance',{'encounters':[]},'Active')
 ]
 for i,q in enumerate(cases,1):
  t=now();c.execute('INSERT INTO patients VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(q['id'],q['mrn'],q['name'],q['dob'],q['sex'],q['phone'],'',q['id_number'],'Front Desk','Active','',t,t));pid=q['id']
  ep_id=new_record(c,pid,'cancer_episode',{'episode_no':f'SYN-EP-VAL-{i:02d}','kind':'Primary cancer','label':q['label'],'started_at':t,'ended_at':'','closure_reason':'','primary_diagnosis_id':'','status':'Active','synthetic_validation':True,'disclaimer':disclaimer},'Active','System',f'EP-SYN-VAL-{i:02d}')
  reg_id=new_record(c,pid,'registration',{'arrival_type':'Synthetic validation','assigned_specialty':q['specialty'],'clinician_assignment':'','route_rule':'CCA connected-workflow validation','referral_reason':q['case_summary'],'address':'Synthetic validation address','general_consent':'Pending','photo_status':'Not required','synthetic_validation':True,'disclaimer':disclaimer},'Draft','System',f'REG-SYN-VAL-{i:02d}')
  ref_id=new_record(c,pid,'referral',{'status':'Created','reason':q['case_summary'],'assigned_department':'','assigned_clinician':'','priority':'Routine','history':[{'status':'Created','at':t,'by':{'name':'System','role':'System'},'reason':'Synthetic validation baseline'}],'synthetic_validation':True,'disclaimer':disclaimer},'Created','System',f'REF-SYN-VAL-{i:02d}')
  new_record(c,pid,'validation_case',{'case_type':q['case_type'],'intended_specialty':q['specialty'],'case_summary':q['case_summary'],'hints':q['hints'],'disclaimer':disclaimer,'proof_rule':'Seed establishes starting state only; completed workflow evidence must be created through normal UI/API actions.'},'Active','System',f'VALCASE-SYN-VAL-{i:02d}')
  for typ,data0,st in common_workspace:
   dd=dict(data0);dd.update({'synthetic_validation':True,'disclaimer':disclaimer,'episode_id':ep_id}) if typ not in ['queue','journey'] else dd.update({'synthetic_validation':True,'disclaimer':disclaimer})
   new_record(c,pid,typ,dd,st,'System',f'{typ.upper()}-SYN-VAL-{i:02d}')
  # Initial real responsibility begins with Registration. Nothing downstream is pre-completed.
  handoff(c,pid,'Front Desk','Complete registration and assign oncology referral','Registration / referral','registration',reg_id,'System','High','Synthetic validation case awaiting role-owned registration',{'referral_id':ref_id,'validation_case_id':f'VALCASE-SYN-VAL-{i:02d}','disclaimer':disclaimer},episode_id=ep_id)
  grant_patient_access(c,pid,'Intake Nurse','synthetic-baseline',ref_id,'System')
  journey_add(c,pid,'Front Desk','Registration','Draft','System','registration',reg_id,disclaimer,True)


def seed():
 c=db()
 if c.execute('SELECT COUNT(*) n FROM patients').fetchone()['n']:
  c.close();return
 p={'id':'PAT-0001','mrn':'CCA-DEMO-0001','name':'Maya Iyer','dob':'1980-02-11','sex':'Female','phone':'+91 90000 01001','abha':'91-1111-2222-3333','id_number':'AADHAAR-DEMO-1001','current_department':'Medical Oncology','status':'Active','photo_document_id':''}
 t=now(); c.execute('INSERT INTO patients VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(p['id'],p['mrn'],p['name'],p['dob'],p['sex'],p['phone'],p['abha'],p['id_number'],p['current_department'],p['status'],p['photo_document_id'],t,t))
 pid=p['id']
 new_record(c,pid,'registration',{'arrival_type':'Clinician specified','assigned_specialty':'Medical Oncology','clinician_assignment':'Medical Oncology Clinic','route_rule':'Clinician assignment','referral_doctor_name':'Dr External Referrer','referral_facility':'Outside Hospital','referral_network_level3':'External referral source','referral_reason':'Breast cancer opinion','address':'Hyderabad','general_consent':'Signed','photo_status':'Pending'},'Completed','System','REG-0001')
 new_record(c,pid,'referral',{'referral_no':'REF-DEMO-0001','source_type':'External clinician','referring_doctor':'Dr External Referrer','referring_facility':'Outside Hospital','reason':'Breast cancer opinion','priority':'Routine','assigned_department':'Medical Oncology','assigned_clinician':'Medical Oncology Clinic','status':'Assigned','history':[{'at':now(),'from':'Created','to':'Assigned','by':actor('System'),'reason':'Initial referral routing'}]},'Assigned','System','REF-0001')
 new_record(c,pid,'consent',{'items':[{'id':'CONS-GEN-1','type':'General Consent','version':'CCA-GEN-v1','scope':'General care and record use','status':'Signed','signed_by':'Maya Iyer','signed_at':now(),'valid_from':str(date.today()),'valid_until':str(date.today()+timedelta(days=365))},{'id':'CONS-TX-1','type':'Treatment Consent','version':'CCA-TX-v1','scope':'Systemic antineoplastic treatment for current signed plan','status':'Signed','signed_by':'Maya Iyer','signed_at':now(),'valid_from':str(date.today()),'valid_until':str(date.today()+timedelta(days=180))}]},'Active','System','CONS-0001')
 new_record(c,pid,'appointments',{'items':[{'id':'APT-1','date':(datetime.now()+timedelta(days=1)).isoformat(timespec='minutes'),'department':'Medical Oncology','clinician':'Medical Oncology Clinic','location':'OPD','purpose':'Treatment planning','status':'Scheduled'}]},'Active','System','APT-0001')
 new_record(c,pid,'queue',{'current_location':'Medical Oncology','current_status':'In Service','priority':'Routine','token':'MO-041','history':[{'at':now(),'from':'Registration','to':'Nurse Intake','status':'Completed','actor':'System'},{'at':now(),'from':'Nurse Intake','to':'Medical Oncology','status':'Queued','actor':'System'}]},'Active','System','QUEUE-0001')
 new_record(c,pid,'journey',{'current_location':'Medical Oncology','current_care_stage':'Treatment Planning','events':[{'id':'JNY-1','at':now(),'department':'Registration','care_stage':'Registered','clinician':'System','actor_role':'System','status':'Completed','source_type':'registration','source_id':'REG-0001','note':''},{'id':'JNY-2','at':now(),'department':'Nurse Intake','care_stage':'Intake Completed','clinician':'System','actor_role':'System','status':'Completed','source_type':'intake','source_id':'INTAKE-0001','note':''},{'id':'JNY-3','at':now(),'department':'Medical Oncology','care_stage':'Treatment Planning','clinician':'System','actor_role':'System','status':'Current','source_type':'consultation','source_id':'CONSULT-0001','note':''}]},'Active','System','JOURNEY-0001')
 new_record(c,pid,'cancer_episode',{'episode_no':'EP-BR-2026-01','kind':'Primary cancer','label':'Left breast primary cancer','started_at':'2026-08-25','ended_at':'','closure_reason':'','primary_diagnosis_id':'DX-0001','status':'Active'},'Active','System','EPISODE-0001')
 new_record(c,pid,'admission',{'admissions':[]},'Active','System','ADMIT-0001')
 new_record(c,pid,'inpatient_care',{'daily_notes':[],'nursing_observations':[],'intake_output':[],'pain_assessments':[],'toxicity_events':[],'specialty_reviews':[],'inpatient_medication_orders':[]},'Active','System','IPDCARE-0001')
 new_record(c,pid,'discharge',{'summaries':[]},'Active','System','DISCH-0001')
 new_record(c,pid,'continuous_therapy',{'courses':[]},'Active','System','CONT-0001')
 new_record(c,pid,'tumor_marker',{'measurements':[]},'Active','System','MARKER-0001')
 new_record(c,pid,'intake',{'bp':'118/76','hr':78,'rr':16,'temp_c':36.8,'spo2':99,'weight_kg':70,'height_cm':170,'bmi':24.22,'bsa_m2':1.82,'bsa_formula':'Mosteller: sqrt(height_cm × weight_kg / 3600)','measurement_units':{'bp':'mmHg','hr':'/min','rr':'/min','temp_c':'°C','spo2':'%','weight_kg':'kg','height_cm':'cm'},'source_measurements':{'sbp':{'value':118,'unit':'mmHg'},'dbp':{'value':76,'unit':'mmHg'},'hr':{'value':78,'unit':'/min'},'rr':{'value':16,'unit':'/min'},'temp':{'value':36.8,'unit':'°C'},'spo2':{'value':99,'unit':'%'},'weight':{'value':70,'unit':'kg'},'height':{'value':170,'unit':'cm'}},'measured_at':now(),'assessor':{'id':'USR-NURSE-001','name':'Nurse Navigator','role':'Nurse Navigator'},'ecog':'1','kps':'90','pain_instrument':'Numeric Rating Scale 0–10','pain_score':2,'pain_site':'Left breast','fall_risk_setting':'OPD','fall_risk_scale':'CCA Demo Fall-Risk Scale — Synthetic QA','fall_risk_score':1,'fall_risk_level':'Low','fall_risk_scale_status':'Synthetic QA — CCA must approve/configure the actual scale and cut-offs','past_medical':'Hypertension','past_surgical':'None','family_history':'Mother breast cancer','hormonal_history':'Reviewed','reproductive_history':'Reviewed','social_history':'No tobacco'},'Completed','System','INTAKE-0001')
 new_record(c,pid,'med_recon',{'items':[{'id':'MED-1','name':'Amlodipine','dose':'5 mg','route':'PO','frequency':'Once daily','status':'Continue','source':'Patient'}],'allergy_status':'Allergy present','allergies':[{'id':'ALG-1','substance':'Penicillin','code':'ALG-PEN','code_system':'Synthetic QA allergen master','reaction':'Rash','reaction_detail':'','severity':'Moderate','status':'Active','source':'Patient','clinical_content_status':'Synthetic QA allergen/reaction masters — CCA configuration required'}],'reconciliation_events':[{'at':now(),'reconciled_by':{'id':'USR-NURSE-001','name':'Nurse Navigator','role':'Nurse Navigator'},'medication_count':1,'allergy_count':1,'allergy_status':'Allergy present','reconciliation_status':'Complete','source':'Patient','reason':'Seeded synthetic complete reconciliation','attestation':'Medication and allergy reconciliation reviewed to the stated status.'}]},'Active','System','MEDREC-0001')
 new_record(c,pid,'dynamic_forms',{'definitions':[{'id':'FORM-ONC-INTAKE','name':'Oncology Intake','version':1,'status':'Active','fields':[{'id':'fh_cancer','label':'Family history of cancer','type':'select','options':['No','Yes','Unknown'],'required':True},{'id':'fh_detail','label':'Family cancer details','type':'textarea','show_if':{'field':'fh_cancer','equals':'Yes'}},{'id':'social','label':'Social history','type':'textarea'}]}],'responses':{}},'Active','System','FORM-0001')
 new_record(c,pid,'consultation',{'encounter_type':'New diagnosis / treatment planning','date':now(),'chief_complaint':'Left breast lump','hpi':'Biopsy-confirmed malignancy, referred for multidisciplinary planning','ros':'No acute systemic symptoms','physical_exam_structured':{'general':'Stable','cardiovascular':'Normal','respiratory':'Clear','abdomen':'Soft','neurologic':'No focal deficit','tumor_site':'Left breast mass'},'decision_flow':{'diagnosed':'Yes','treatable':'Yes','tumor_board_required':'Yes','treatment_clearance':'N/A'},'assessment':'HER2-positive breast cancer','plan':'MDT and neoadjuvant systemic therapy planning','signed_by':'Medical Oncology','signed_at':now()},'Signed','System','CONSULT-0001')
 biomarkers=[{'name':'ER','value':'Negative','method':'IHC','date':'2026-08-25'},{'name':'PR','value':'Negative','method':'IHC','date':'2026-08-25'},{'name':'HER2','value':'3+','method':'IHC','date':'2026-08-25'}]
 new_record(c,pid,'diagnosis',{'icd10':'C50.4','icd10_version':'ICD-10','icdo_topography':'C50.4','icdo_morphology':'8500/3','icdo_version':'ICD-O-3','snomed':'254837009','cancer_type':'Breast Cancer','primary_site':'Left breast','histology':'Invasive ductal carcinoma','grade':'3','stage_t':'cT2','stage_n':'cN1','stage_m':'cM0','stage_group':'Stage IIB','staging_system':'AJCC','staging_version':'Breast v8','staging_effective_date':'2018-01-01','staging_basis':'Clinical','staging_date':'2026-08-26','ecog':'1','disease_status':'New diagnosis','treatment_intent':'Neoadjuvant','biomarkers':biomarkers},'Verified','System','DX-0001')
 new_record(c,pid,'lab',{'date':str(date.today()),'hb':12.2,'wbc':6.1,'anc':3.2,'platelets':276,'creatinine':0.8,'egfr':92,'bilirubin':0.7,'ast':22,'alt':24,'albumin':4.1,'sodium':139,'potassium':4.1,'magnesium':1.9,'calcium':9.2,'pregnancy':'Negative','lvef':61,'units':{'hb':'g/dL','wbc':'10^9/L','anc':'10^9/L','platelets':'10^9/L','creatinine':'mg/dL','egfr':'mL/min/1.73m2','bilirubin':'mg/dL','ast':'U/L','alt':'U/L','albumin':'g/dL','sodium':'mmol/L','potassium':'mmol/L','magnesium':'mg/dL','calcium':'mg/dL','lvef':'%'},'finalized_at':now()},'Final','System','LAB-0001')
 new_record(c,pid,'pathology',{'date':'2026-08-25','site':'Left breast','specimen':'Core biopsy','histology':'Invasive ductal carcinoma','grade':'3','er':'Negative','pr':'Negative','her2':'3+','signed_by':'Pathology','signed_at':now()},'Final','System','PATH-0001')
 new_record(c,pid,'radiology',{'study':'Breast MRI','date':'2026-08-26','findings':'Left breast lesion with suspicious regional node','impression':'Locoregional disease; no distant disease shown in this synthetic study','esigned':True,'radiologist':'Radiologist','signed_at':now()},'Final','System','RAD-0001')
 new_record(c,pid,'mdt',{'case_no':'MDT-BR-041','meeting_at':'2026-08-28T16:00','clinical_question':'Confirm multimodality sequence','clinical_summary':'HER2-positive left breast cancer, cT2N1M0','intent':'Curative','recommendation':'Neoadjuvant systemic therapy → response assessment → surgery → adjuvant review','alternatives':['Upfront surgery discussed','Alternative systemic sequencing discussed'],'rationale':'Multidisciplinary consensus for synthetic demo','final_consensus':'Consensus reached','specialty_responsible':'Medical Oncology','attendees':[{'name':'Medical Oncology','discipline':'Medical Oncology','status':'Present'},{'name':'Surgical Oncology','discipline':'Surgical Oncology','status':'Present'},{'name':'Radiation Oncology','discipline':'Radiation Oncology','status':'Present'}],'recommendation_submitted_by':actor('MDT Coordinator'),'recommendation_submitted_at':now(),'chair_decision':'Approved','chair_reason':'Seeded synthetic MDT Chair approval','chair_signed_by':actor('MDT Chair'),'chair_signed_at':now(),'signed_by':actor('MDT Chair'),'signed_at':now()},'MDT Recommended','System','MDT-0001')
 new_record(c,pid,'mdt_collab',{'comments':[],'attendance':[],'external_consultants':[]},'Active','System','MDTC-0001')
 new_record(c,pid,'mdt_followup',{'action_items':[{'id':'MDTA-1','action':'Create Medical Oncology treatment plan','owner':'Medical Oncology','due':str(date.today()+timedelta(days=1)),'status':'Open'}]},'Active','System','MDTF-0001')
 new_record(c,pid,'care_plan',{'status':'Active','goals':['Complete neoadjuvant systemic therapy safely','Response assessment','Surgical reassessment'],'milestones':[{'id':'CP-1','name':'Cycle 1 systemic therapy','owner':'Medical Oncology / Day Care','status':'Ready'},{'id':'CP-2','name':'Response imaging','owner':'Radiology','status':'Planned'},{'id':'CP-3','name':'Surgical reassessment','owner':'Surgical Oncology','status':'Planned'}],'dependencies':['Current labs','Treatment consent','Pharmacy verification']},'Active','System','CARE-0001')
 new_record(c,pid,'treatment_plan',{'plan_no':'TP-0001','version':1,'source_mdt_id':'MDT-0001','diagnosis':'Breast Cancer','stage':'Stage IIB','histology':'Invasive ductal carcinoma','biomarkers':biomarkers,'intent':'Neoadjuvant','line_of_therapy':'1st line / neoadjuvant','disease_status':'New diagnosis','sequence':['Neoadjuvant systemic therapy','Surgery','Adjuvant radiation review'],'phases':[{'modality':'Systemic Therapy','regimen':'Synthetic HER2+ Breast Neoadjuvant Demo Regimen','regimen_template_id':'REG-CCA-TCHP-DEMO','start_target':str(date.today()),'duration':'6 cycles q21d','status':'Clinician Approved','responsible':'Medical Oncology'},{'modality':'Surgery','regimen':'Procedure to be determined after response assessment','status':'Planned','responsible':'Surgical Oncology'},{'modality':'Radiation','regimen':'Post-operative prescription if indicated','status':'Planned','responsible':'Radiation Oncology'}]},'Clinician Approved','System','TP-0001')
 new_record(c,pid,'protocol_library',{'protocols':[PROTOCOL]},'Active','System','PROT-0001')
 new_record(c,pid,'formulary',FORMULARY,'Active','System','FORMULARY-0001')
 template=content_one(c,'REG-CCA-TCHP-DEMO'); protocol=template['data'] if template else PROTOCOL
 ready={'cycle':1,'day':1,'ecog':'1','height_cm':170,'weight_kg':70,'bsa_m2':1.82,'vitals':{'bp':'118/76','hr':78,'rr':16,'temp':36.8,'spo2':99},'lab_date':str(date.today()),'anc':3.2,'platelets':276,'hb':12.2,'egfr':92,'bilirubin':0.7,'lvef':61,'lab_units':{'anc':'10^9/L','platelets':'10^9/L','bilirubin':'mg/dL'},'pregnancy':'Negative','infection':'No','consent':'Current','allergy_review':'Reviewed','medication_review':'Reviewed','toxicity_summary':'None','decision':'Proceed as Planned','decision_reason':'All configured demo criteria met','signed_by':'Medical Oncology','signed_at':now(),'protocol_id':protocol['id'],'protocol_version':protocol['version'],'content_template_id':template['id'] if template else 'REG-CCA-TCHP-DEMO','content_template_version':template['version'] if template else protocol['version']}
 ready['protocol_evaluation']=readiness_eval(ready,protocol)
 new_record(c,pid,'readiness',ready,'Signed','System','READY-0001')
 # Treatment order frozen from protocol
 items=[]
 for q in protocol['items']:
  calc=q['protocol_dose']
  if q['dose_basis']=='mg/kg':calc=round(q['protocol_dose']*70,2)
  elif q['dose_basis']=='mg/m²':calc=round(q['protocol_dose']*1.81,2)
  elif q['dose_basis']=='AUC':calc=600.0  # synthetic demo placeholder; clinician-authorized, not a dosing calculator claim
  items.append({**q,'item_id':'OI-'+str(q['sequence']),'calculated_dose':calc,'calculated_unit':'mg' if q['dose_basis']!='AUC' else 'mg','ordered_dose':calc,'ordered_unit':'mg' if q['dose_basis']!='AUC' else 'mg','final_approved_dose':calc,'dose_decision_reason':'Accept calculated/protocol dose after clinician review' if q['dose_basis']!='AUC' else 'Patient-specific AUC product-test dose accepted after clinician review','dose_decided_by':{'id':'USR-MEDICALO-001','name':'Medical Oncology User','role':'Medical Oncology'},'dose_decided_at':now(),'variance_pct':0,'variance_reason':'','rounding':'No rounding','rate_ml_hr':round(q.get('volume_ml',0)/(q.get('duration_min',60)/60),2) if q.get('volume_ml') else 0,'administration_at':datetime.now().replace(hour=10,minute=0,second=0,microsecond=0).isoformat()})
 order={'order_no':'ORD-C1D1','plan_id':'TP-0001','protocol_id':protocol['id'],'protocol_version':protocol['version'],'regimen':protocol['name'],'content_template_id':template['id'],'content_template_version':template['version'],'content_source_id':template['source_id'],'diagnosis':'Breast Cancer','intent':'Neoadjuvant','line_of_therapy':'1st line / neoadjuvant','cycle':1,'day':1,'planned_cycles':6,'start_date':str(date.today()),'patient_snapshot':{'name':'Maya Iyer','dob':'1980-02-11','mrn':'CCA-DEMO-0001','weight_kg':70,'height_cm':170,'bsa_m2':1.82,'bsa_formula':'Mosteller: sqrt(height_cm × weight_kg / 3600)','measurement_units':{'weight_kg':'kg','height_cm':'cm'},'source_measurements':{'weight':{'value':70,'unit':'kg'},'height':{'value':170,'unit':'cm'}},'measured_at':now(),'assessor':{'id':'USR-NURSE-001','name':'Nurse Navigator','role':'Nurse Navigator'},'allergies':['Penicillin — rash'],'lab_date':str(date.today())},'items':items,'readiness_id':'READY-0001','signed_by':'Medical Oncology','signed_at':now(),'locked':True}
 new_record(c,pid,'treatment_order',order,'Verification Pending','System','ORDER-0001')
 new_record(c,pid,'pharmacy',{'order_id':'ORDER-0001','verification_checks':{},'items':[dict(x) for x in items],'query_history':[],'dispensed_to':'','manifest_no':''},'Verification Pending','System','PHARM-0001')
 new_record(c,pid,'infusion',{'order_id':'ORDER-0001','checklist':{},'pre_vitals':{},'access':'','mar':[],'post_vitals':{},'tolerance':'','discharge_instructions':'','next_cycle':''},'Awaiting Pharmacy','System','INF-0001')
 new_record(c,pid,'toxicity',{'events':[]},'Active','System','TOX-0001')
 new_record(c,pid,'modification',{'items':[]},'Active','System','MOD-0001')
 new_record(c,pid,'response',{'baseline':{'date':'2026-08-26','target_lesions':[{'id':'L1','site':'Left breast','size_mm':45}],'non_target':'Regional nodes present','status':'Measurable disease'},'assessments':[]},'Active','System','RESP-0001')
 new_record(c,pid,'radiation',{'prescription':{'status':'Draft','site':'Left breast','laterality':'Left','intent':'Adjuvant','modality':'External Beam','technique':'VMAT','energy':'6 MV','treatment_phase':1,'total_dose_gy':40.05,'dose_per_fraction_gy':2.67,'fractions':15,'frequency':'5x/week','planned_start':str(date.today()+timedelta(days=60)),'concurrent_systemic_order':'None','target_volumes':['Left breast','Regional nodes if indicated after final planning'],'organs_at_risk':['Heart','Ipsilateral lung'],'oar_constraints':['Pending Radiation Oncology / Physics local constraint review'],'simulation_requirement':'Yes','immobilisation':'Breast board','image_guidance':'Daily image guidance per local policy','bolus':'As clinically indicated','special_instructions':'Synthetic demo prescription; final RT planning remains TPS/OIS boundary','signed_by':'','signed_at':'','prescription_version':1},'prescription_history':[],'planning':{'plan_version':1,'prescription_version':1,'simulation_status':'Pending','contouring_status':'Pending','planning_status':'Pending','physics_qa':'Pending','physics_qa_plan_version':None,'physics_qa_prescription_version':None,'physician_final_approval':'Pending','physician_approval_plan_version':None,'physician_approval_prescription_version':None,'dicom_refs':{'RTSTRUCT':'','RTPLAN':'','RTDOSE':'','RTIMAGE':'','RTRECORD':''}},'planning_history':[],'fractions':[],'interruptions':[]},'Draft','System','RT-0001')
 new_record(c,pid,'surgery',{'plan':{'status':'Recommended','procedure':'Left breast-conserving surgery','indication':'Definitive treatment','intent':'Curative','site':'Breast','laterality':'Left','extent':'Wide local excision','approach':'Open','nodal_procedure':'Sentinel lymph node biopsy','reconstruction':'Primary closure','planned_date':str(date.today()+timedelta(days=50)),'priority':'Routine','preop_requirements':['Anesthesia consultation','CBC/CMP','Imaging review','Pathology review'],'required_imaging_pathology':['Breast imaging reviewed','Core biopsy pathology reviewed'],'anesthesia':'General','anesthesia_clearance':'Pending','blood_requirement':'None anticipated','special_instructions':'Final procedure depends on response assessment','signed_by':'','signed_at':''},'preop':{'anesthesia_clearance':'Pending','labs':'Pending','consent':'Pending','ready':False},'outcome':{},'histopathology_link':''},'Recommended','System','SURG-0001')
 new_record(c,pid,'treatment_history',{'episodes':[]},'Active','System','HIST-0001')
 new_record(c,pid,'visit_summary',{'visit_date':str(date.today()),'diagnosis_summary':'HER2-positive left breast cancer, Stage IIB','decisions':['Proceed to MDT-recommended neoadjuvant plan'],'patient_instructions':'Bring current medication list and report fever/infection symptoms','next_appointment':str(date.today()+timedelta(days=21)),'next_department':'Medical Oncology','signed_by':'Medical Oncology','signed_at':now()},'Signed','System','VISIT-0001')
 new_record(c,pid,'finance',{'payer':'Self-pay / insurance review','payment_events':[],'estimated_total':0,'actual_total':0,'funding_source_status':'Pending'},'Active','System','FIN-0001')
 new_record(c,pid,'conversion',{'counselling_status':'Pending','payer_category':'Self-pay','mo_drug_estimate':{'source_order_id':'ORDER-0001','currency':'INR','lines':[],'total':0},'estimate_status':'Draft','fundraising_letter':{'status':'Not required','recipient':'','purpose':'Treatment support','text':''},'tracking':[]},'Active','System','CONV-0001')
 new_record(c,pid,'standards',{'items':['HL7 FHIR R4 mapping-ready','mCODE modeling reference','DICOM/DICOM RT link boundary','CTCAE structured toxicity','RECIST response structure','ABDM architecture/interface boundary','MOSAIQ standards-based integration boundary'],'note':'Prototype architecture; no external conformance claim.'},'Active','System','STD-0001')
 new_record(c,pid,'cca_requirements',{'note':'Runtime status only; live external integrations remain external.','rows':[{'area':'Registration','requirement':'Registration / routing / consent / scheduling / queue','status':'Runtime functional'},{'area':'Nurse EMR','requirement':'Vitals / BSA / medication reconciliation / forms','status':'Runtime functional'},{'area':'Doctor EMR','requirement':'Structured OPD / diagnosis / staging / diagnostic orders','status':'Runtime functional'},{'area':'MDT','requirement':'Case / comments / attendance / recommendation / specialty-plan separation','status':'Runtime functional'},{'area':'Systemic therapy','requirement':'Plan → order → pharmacy → Day Care MAR','status':'Runtime functional'},{'area':'Radiation','requirement':'Prescription → planning status → fraction tracking','status':'Runtime functional prototype'},{'area':'Surgery','requirement':'Plan → pre-op → procedure → histopathology/adjuvant handoff','status':'Runtime functional prototype'},{'area':'ABDM / MOSAIQ / PACS / LIS / TPS','requirement':'Live external integration','status':'Interface boundary only'}]},'Active','System','REQ-0001')
 pc7_reconcile_base_patient(c)
 seed_showcase_cases(c)
 seed_pc8_validation_cases(c)
 # Seeded demo patient is intentionally assigned to every internal role so every demo surface can be exercised.
 for rr in ROLES:
  if rr!='External Consultant':grant_patient_access(c,pid,rr,'seed_demo','PAT-0001','System')
 c.commit();c.close()


def patient(c,pid):
 r=c.execute('SELECT * FROM patients WHERE id=?',(pid,)).fetchone();return dict(r) if r else None

def parse_iso_date(v):
 try:return date.fromisoformat(str(v)[:10])
 except:return None

def valid_dob(v):
 d=parse_iso_date(v)
 if not d:return False,'DOB must be a valid ISO date'
 if d>date.today():return False,'Date of birth cannot be in the future'
 if d<date.today()-timedelta(days=130*366):return False,'Date of birth is outside the configured plausibility range'
 return True,''

def future_or_today(v):
 d=parse_iso_date(v)
 return bool(d and d>=date.today())

def grant_patient_access(c,pid,role,scope_type='workflow',source_id='',granted_by='System'):
 if not pid or role not in ROLES:return
 c.execute('INSERT OR REPLACE INTO patient_access(patient_id,role,scope_type,source_id,active,granted_at,granted_by) VALUES(?,?,?,?,?,?,?)',(pid,role,scope_type,source_id or '',1,now(),actor(granted_by)['id'] if granted_by in ROLES else str(granted_by)))

def revoke_patient_access(c,pid,role,scope_type=None,source_id=None):
 q='UPDATE patient_access SET active=0 WHERE patient_id=? AND role=?';args=[pid,role]
 if scope_type is not None:q+=' AND scope_type=?';args.append(scope_type)
 if source_id is not None:q+=' AND source_id=?';args.append(source_id)
 c.execute(q,args)

def can_access_patient(c,role,pid):
 if role in GLOBAL_PATIENT_ACCESS_ROLES:return True
 r=c.execute('SELECT 1 FROM patient_access WHERE patient_id=? AND role=? AND active=1 LIMIT 1',(pid,role)).fetchone()
 return bool(r)

def task_row(r):
 d=dict(r);d['data']=jload(d.pop('data_json'),{});return d

def create_task(c,pid,owner_role,title,task_type='Follow-up',priority='Routine',source_type='',source_id='',due_at='',episode_id='',reason='',data=None,created_by='System'):
 if owner_role not in ROLES:raise ValueError('Unknown task owner role')
 if priority not in VALUE_SETS['task_priority']:priority='Routine'
 tid='TASK-'+uuid.uuid4().hex[:10].upper();t=now();ep=episode_id or ((current_episode(c,pid) or {}).get('id') if pid else '')
 c.execute('INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(tid,pid,ep,task_type,title,'Open',priority,owner_role,actor(owner_role)['id'],source_type,source_id,due_at,'','','','',0,reason,jdump(data or {}),t,actor(created_by)['id'] if created_by in ROLES else str(created_by),t,actor(created_by)['id'] if created_by in ROLES else str(created_by)))
 if pid:grant_patient_access(c,pid,owner_role,'task',tid,created_by)
 audit(c,pid or '',created_by if created_by in ROLES else 'System','TASK_CREATE','task',tid,title)
 return tid

def tasks_for_role(c,role,pid=''):
 q='SELECT * FROM tasks WHERE 1=1';args=[]
 if pid:q+=' AND patient_id=?';args.append(pid)
 if role!='Hospital Management / Admin':q+=' AND owner_role=?';args.append(role)
 q+=' ORDER BY CASE priority WHEN \'Critical\' THEN 0 WHEN \'High\' THEN 1 ELSE 2 END, due_at, created_at'
 return [task_row(r) for r in c.execute(q,args)]

# PC8.0 connected-multidisciplinary task/handoff engine. Built on the existing
# create_task/tasks_for_role/patient_access primitives above -- additive only.
def ensure_task(c,pid,owner_role,title,task_type='Follow-up',priority='Routine',source_type='',source_id='',due_at='',episode_id='',reason='',data=None,created_by='System'):
 r=c.execute("SELECT * FROM tasks WHERE patient_id=? AND owner_role=? AND task_type=? AND source_type=? AND source_id=? AND status IN ('Open','Acknowledged') ORDER BY created_at DESC LIMIT 1",(pid,owner_role,task_type,source_type or '',source_id or '')).fetchone()
 if r:return r['id']
 return create_task(c,pid,owner_role,title,task_type,priority,source_type,source_id,due_at,episode_id,reason,data,created_by)

def complete_open_tasks(c,pid,owner_role=None,task_type=None,source_type=None,source_id=None,completed_by='System'):
 q="SELECT id FROM tasks WHERE patient_id=? AND status IN ('Open','Acknowledged')";args=[pid]
 if owner_role:q+=' AND owner_role=?';args.append(owner_role)
 if task_type:q+=' AND task_type=?';args.append(task_type)
 if source_type:q+=' AND source_type=?';args.append(source_type)
 if source_id:q+=' AND source_id=?';args.append(source_id)
 ids=[r['id'] for r in c.execute(q,args)]
 if ids:
  t=now();aid=actor(completed_by)['id'] if completed_by in ROLES else str(completed_by)
  for tid in ids:
   c.execute("UPDATE tasks SET status='Completed',completed_at=?,completed_by=?,updated_at=?,updated_by=? WHERE id=?",(t,aid,t,aid,tid));audit(c,pid,completed_by if completed_by in ROLES else 'System','TASK_AUTO_COMPLETE','task',tid,'Completed by workflow transition')
 return ids

def cancel_open_tasks(c,pid,owner_role=None,task_type=None,source_type=None,source_id=None,cancelled_by='System',reason='Source record superseded'):
 q="SELECT id FROM tasks WHERE patient_id=? AND status IN ('Open','Acknowledged')";args=[pid]
 if owner_role:q+=' AND owner_role=?';args.append(owner_role)
 if task_type:q+=' AND task_type=?';args.append(task_type)
 if source_type:q+=' AND source_type=?';args.append(source_type)
 if source_id:q+=' AND source_id=?';args.append(source_id)
 ids=[r['id'] for r in c.execute(q,args)]
 if ids:
  t=now();aid=actor(cancelled_by)['id'] if cancelled_by in ROLES else str(cancelled_by)
  for tid in ids:
   c.execute("UPDATE tasks SET status='Cancelled',reason=?,updated_at=?,updated_by=? WHERE id=?",(reason,t,aid,tid));audit(c,pid,cancelled_by if cancelled_by in ROLES else 'System','TASK_AUTO_CANCEL','task',tid,reason)
 return ids

def handoff(c,pid,owner_role,title,task_type,source_type,source_id,created_by,priority='Routine',reason='',data=None,due_at='',episode_id=''):
 tid=ensure_task(c,pid,owner_role,title,task_type,priority,source_type,source_id,due_at,episode_id,reason,data,created_by);grant_patient_access(c,pid,owner_role,'task',tid,created_by);return tid

def task_context(c,t,viewer_role=''):
 x=task_row(t) if not isinstance(t,dict) else t;pat=patient(c,x.get('patient_id')) if x.get('patient_id') else None;ep=get_rec(c,x.get('episode_id')) if x.get('episode_id') else current_episode(c,x.get('patient_id')) if x.get('patient_id') else None;raw=get_rec(c,x.get('source_id')) if x.get('source_id') else None
 signed_by='';signed_at=''
 if raw:
  d=raw.get('data',{});nested=(d.get('plan') if raw.get('entity_type')=='surgery' else d.get('prescription') if raw.get('entity_type')=='radiation' else {}) or {};sb=d.get('signed_by') or d.get('approved_by') or d.get('completed_by') or d.get('released_by') or nested.get('signed_by');signed_by=sb.get('name') if isinstance(sb,dict) else sb or '';signed_at=d.get('signed_at') or d.get('approved_at') or d.get('completed_at') or d.get('dispensed_at') or nested.get('signed_at') or ''
 # Task worklists must never become a side-channel around role projections. The same
 # minimum-necessary projection used by patient bootstrap is used here as well.
 src=project_record(raw,viewer_role) if raw and viewer_role and role_can_read(viewer_role,raw.get('entity_type')) else (raw if raw and not viewer_role else None)
 return {**x,'patient':project_patient(pat,viewer_role) if pat and viewer_role else pat,'episode':ep,'source_record':src,'source_record_type':raw.get('entity_type') if raw else x.get('source_type'),'source_record_id':raw.get('id') if raw else x.get('source_id'),'source_record_version':raw.get('version') if raw else None,'source_record_status':raw.get('status') if raw else '','source_record_updated_at':raw.get('updated_at') if raw else '','source_visible_to_role':bool(src),'signed_by':signed_by,'signed_at':signed_at,'provenance':{'created_by':raw.get('created_by') if raw else '','updated_by':raw.get('updated_by') if raw else '','source_type':x.get('source_type'),'source_id':x.get('source_id')}}

def record_snapshot(c,rid,version=None):
 r=get_rec(c,rid)
 if not r:return None
 if version in [None,'','current']:return r
 try:v=int(version)
 except:return None
 z=c.execute('SELECT * FROM record_versions WHERE record_id=? AND version=?',(rid,v)).fetchone()
 if not z:return None
 d=dict(z);data=jload(d.get('data_json'),{});return {'id':rid,'patient_id':d['patient_id'],'entity_type':d['entity_type'],'status':d['status'],'version':d['version'],'data':data,'created_at':r['created_at'],'updated_at':d['at'],'created_by':r['created_by'],'updated_by':d['actor_id']}

def latest_snapshot(c,pid,typ,version=None):
 r=latest(c,pid,typ)
 return record_snapshot(c,r['id'],version) if r else None

def order_is_superseded(c,order):
 if not order:return True
 if order.get('status') in ['Superseded','Cancelled','Entered in error']:return True
 # Explicit lineage wins even if an older status was not updated because of a partial failure.
 for newer in many(c,order['patient_id'],'treatment_order'):
  if newer['id']==order['id']:continue
  if newer.get('data',{}).get('supersedes_order_id')==order['id'] and newer.get('status') not in ['Cancelled','Entered in error']:
   return True
 return False

def order_current_or_error(c,order):
 if not order:return {'error':'Treatment order not found'},404
 if order_is_superseded(c,order):return {'error':'Superseded/stale Treatment Order cannot be acted on','order_id':order.get('id'),'order_status':order.get('status')},409
 return None

def rt_current_versions(rad):
 d=(rad or {}).get('data',{});rx=d.get('prescription',{});pl=d.get('planning',{})
 return int(rx.get('prescription_version') or 1),int(pl.get('plan_version') or 1)

def has_unresolved_inpatient_orders(c,pid,admission_id=''):
 out=[]
 terminal={'Completed','Cancelled','Rejected','Discontinued'}
 for o in many(c,pid,'treatment_order'):
  if o['data'].get('administration_setting')!='Inpatient':continue
  if admission_id and o['data'].get('admission_id') not in ['',None,admission_id]:continue
  if o['status'] not in terminal:out.append({'id':o['id'],'status':o['status'],'order_no':o['data'].get('order_no')})
 return out

def is_non_tnm_case(d):
 sys=str(d.get('staging_system') or d.get('classification_system') or '').upper().strip()
 cancer=str(d.get('cancer_type') or '').upper()
 hist=str(d.get('histology') or '').upper()
 systems=['WHO','WHO/ICC','ICC','ELN','ANN ARBOR','LUGANO','ISS','R-ISS','IPSS','IPSS-R','IPSS-M','FIGO','NONE / NOT APPLICABLE','NOT APPLICABLE','CNS WHO']
 keywords=['LEUKEMIA','LYMPHOMA','MYELOMA','MYELODYSPLASTIC','MYELOPROLIFERATIVE','GLIOBLASTOMA','MENINGIOMA','CNS TUMOR','BRAIN TUMOR','AML','ALL','CML','CLL']
 text=cancer+' '+hist
 # Use token/phrase boundaries. Substring matching is unsafe: e.g. ALL in LOCALLY or SMALL must not classify a solid tumour as ALL.
 keyword_match=any(re.search(r'(?<![A-Z0-9])'+re.escape(k)+r'(?![A-Z0-9])',text) for k in keywords)
 return bool(d.get('non_tnm')) or sys in systems or keyword_match

def validate_lab_plausibility(values,units):
 errors=[]
 for k,(lo,hi,canonical_unit) in LAB_PLAUSIBLE_RANGES.items():
  if values.get(k) in ['',None]:continue
  try:raw=float(values.get(k))
  except:errors.append({'field':k,'value':values.get(k),'error':'not numeric'});continue
  unit=(units or {}).get(k)
  v=normalize_lab(raw,unit,k)
  # Additional canonical conversions for analytes supported in alternate units.
  u=str(unit or '').lower().replace('μ','u').replace('µ','u').replace('×','x').replace('²','2').replace(' ','')
  if k=='creatinine' and u=='umol/l':v=raw/88.4
  elif k=='magnesium' and u=='mmol/l':v=raw*2.4305
  elif k=='calcium' and u=='mmol/l':v=raw*4.008
  if v is None:continue
  if v<lo or v>hi:errors.append({'field':k,'value':raw,'unit':unit,'normalized_value':round(v,6),'canonical_unit':canonical_unit,'plausible_range':[lo,hi]})
 return errors

def critical_lab_flags(values,units):
 flags=[]
 for k,rule in LAB_CRITICAL_ROUTING_RULES.items():
  if values.get(k) in ['',None]:continue
  try:raw=float(values.get(k))
  except:continue
  unit=(units or {}).get(k);v=normalize_lab(raw,unit,k)
  if v is None:v=raw
  if ('lt' in rule and v<rule['lt']) or ('gt' in rule and v>rule['gt']):flags.append({'field':k,'value':raw,'unit':unit,'normalized_value':v,'rule':rule})
 return flags

def safe_float(v):
 try:return float(v)
 except:return None

def project_patient(p,role):
 if not p:return None
 fs=PAT_FIELDS.get(role)
 if not fs:return p
 return {k:p.get(k) for k in fs if k in p}

def project_record(e,role):
 # Minimum-necessary operational consent projection for Front Desk. Clinical consent narrative/signers remain hidden.
 if role=='Front Desk' and e['entity_type']=='consent':
  items=[]
  for x in e['data'].get('items',[]):
   items.append({k:x.get(k) for k in ['id','type','status','valid_until','version'] if k in x})
  return {**e,'data':{'items':items,'completion_status':'Complete' if items and all(x.get('status') in ['Signed','Accepted'] for x in items) else 'Pending'}}
 if role in ['Biller','Finance / Billing'] and e['entity_type'] in ['lab_order','radiology_order']:
  d=e['data']; keep=['order_no','tests','study','date','billing','payment_receipt','sample_status','procedure_status','schedule','status']; e={**e,'data':{k:d.get(k) for k in keep if k in d}}
 if role=='Front Desk' and e['entity_type']=='documents': e={**e,'data':{'count':e['data'].get('count',0)}}
 # Minimum-necessary projection: full Psycho-Oncology counselling narrative is restricted to
 # the owning discipline; other care-team roles see only the coded risk/summary fields needed
 # to coordinate care, matching the same minimum-necessary pattern used for consent above.
 if e['entity_type']=='psychosocial' and role not in ['Psycho-Oncology','Hospital Management / Admin']:
  keep=['assessment_date','distress_score','risk_level','care_team_summary','status','signed_by','signed_at','supersedes','amendment_reason','superseded_by_record_id']
  e={**e,'data':{k:e['data'].get(k) for k in keep if k in e['data']}}
 return e

def role_can_read(role,typ): return typ in READ.get(role,set()) or role=='Hospital Management / Admin' and typ in READ['Hospital Management / Admin']
def role_can_write(role,typ): return role in WRITE.get(typ,set())

def normalize_lab(value,unit,kind):
 try:v=float(value)
 except:return None
 u=(unit or '').strip().lower().replace('μ','u').replace('µ','u').replace('×','x').replace('²','2').replace(' ','')
 if kind in ['anc','platelets','wbc']:
  if u in ['cells/ul','cells/microliter','/ul'] or 'cells' in u:return v/1000.0
  if u in ['10^9/l','x10^9/l','10e9/l']:return v
  return None
 if kind=='bilirubin':
  if u=='mg/dl':return v
  if u in ['umol/l','micromol/l']:return round(v/17.104,4)
  return None
 return v

def validate_lab_units(values,units,required_fields=None):
 units=units or {}; required_fields=required_fields or [k for k in LAB_NUMERIC_FIELDS if values.get(k) not in ['',None]]
 missing=[];invalid=[]
 for k in required_fields:
  if values.get(k) in ['',None]:continue
  unit=str(units.get(k) or '').strip()
  if not unit:missing.append(k);continue
  if unit not in LAB_UNIT_OPTIONS.get(k,[]):invalid.append({'field':k,'unit':unit,'allowed':LAB_UNIT_OPTIONS.get(k,[])})
 return missing,invalid

def latest_final_lab(c,pid):
 rows=many(c,pid,'lab')
 finals=[x for x in rows if x.get('status')=='Final']
 return finals[-1] if finals else None

def readiness_eval(data,protocol=None,as_of_date=None):
 protocol=protocol or PROTOCOL
 try:eval_date=date.fromisoformat(str(as_of_date or data.get('evaluation_as_of_date') or date.today())[:10])
 except:eval_date=date.today()
 hp=protocol['hold_parameters']; blockers=[]; alerts=[]; normalized={}
 units=data.get('lab_units') or {}
 unit_missing=[k for k in READINESS_REQUIRED_UNIT_FIELDS if data.get(k) not in ['',None] and not units.get(k)]
 if unit_missing:blockers.append('Required laboratory unit metadata is missing for: '+', '.join(unit_missing))
 anc=normalize_lab(data.get('anc'),units.get('anc'),'anc'); plt=normalize_lab(data.get('platelets'),units.get('platelets'),'platelets'); bili=normalize_lab(data.get('bilirubin'),units.get('bilirubin'),'bilirubin')
 normalized.update({'anc_10e9_L':anc,'platelets_10e9_L':plt,'bilirubin_mg_dL':bili,'source_units':{k:units.get(k) for k in READINESS_REQUIRED_UNIT_FIELDS}})
 try:egfr=float(data.get('egfr') or 0)
 except:egfr=0
 try:lvef=float(data.get('lvef') or 0)
 except:lvef=0
 ld=data.get('lab_date');age=None;freshness='Missing'
 if not ld:blockers.append('Required laboratory date is missing')
 else:
  try:
   age=(eval_date-date.fromisoformat(str(ld)[:10])).days
   if age<0:blockers.append('Laboratory result date is after the readiness evaluation date');freshness='Invalid'
   else:
    freshness='Current' if age<=hp['lab_max_age_days'] else 'Stale'
    if freshness=='Stale':blockers.append(f'Required labs are stale ({age} days old at evaluation; max {hp["lab_max_age_days"]})')
  except: blockers.append('Laboratory date is invalid');freshness='Invalid'
 def rr(rid,cat,field,current,unit,op,threshold,ok,source='lab'):
  return {'id':rid,'category':cat,'field':field,'current':current,'unit':unit,'operator':op,'threshold':threshold,'status':'PASS' if ok else 'HOLD','outcome':'PASS' if ok else 'HOLD','source_record_id':data.get('lab_source_id','') if source=='lab' else data.get('toxicity_source_id',''),'source_finalized_at':data.get('lab_source_finalized_at','') if source=='lab' else '', 'result_date':ld if source=='lab' else '', 'freshness_days':age if source=='lab' else None,'freshness_status':freshness if source=='lab' else 'Not applicable'}
 ok_anc=anc is not None and anc>=hp['ANC_min']; ok_plt=plt is not None and plt>=hp['platelets_min']; ok_egfr=egfr>=hp['eGFR_min']; ok_bili=bili is not None and bili<=hp['bilirubin_max']; ok_lvef=lvef>=hp['LVEF_min']
 if not ok_anc:blockers.append(f"ANC does not meet protocol criteria ({anc if anc is not None else 'missing/invalid unit'} vs min {hp['ANC_min']} ×10^9/L)")
 if not ok_plt:blockers.append(f"Platelets do not meet protocol criteria ({plt if plt is not None else 'missing/invalid unit'} vs min {hp['platelets_min']} ×10^9/L)")
 if not ok_egfr:blockers.append(f"eGFR does not meet protocol criteria ({egfr} vs min {hp['eGFR_min']})")
 if not ok_bili:blockers.append(f"Bilirubin exceeds protocol demo threshold ({bili if bili is not None else 'missing/invalid unit'} vs max {hp['bilirubin_max']} mg/dL)")
 if not ok_lvef:blockers.append(f"LVEF does not meet protocol criteria ({lvef} vs min {hp['LVEF_min']}%)")
 if str(data.get('pregnancy','')).lower() in ['positive','pregnant']:blockers.append('Pregnancy status requires clinician review before proceeding')
 elif data.get('pregnancy') not in ['Negative','N/A','Not applicable']: alerts.append('Pregnancy status requires clinical review')
 if str(data.get('infection','')).lower() in ['yes','active']:blockers.append('Active infection requires clinician review')
 rule_results=[
  rr('RR-ANC','Hematology','ANC',anc,'×10^9/L','>=',hp.get('ANC_min'),ok_anc),
  rr('RR-PLT','Hematology','Platelets',plt,'×10^9/L','>=',hp.get('platelets_min'),ok_plt),
  rr('RR-EGFR','Renal','eGFR',egfr,'mL/min/1.73m²','>=',hp.get('eGFR_min'),ok_egfr),
  rr('RR-BILI','Hepatic','Bilirubin',bili,'mg/dL','<=',hp.get('bilirubin_max'),ok_bili),
  rr('RR-LVEF','Cardiac','LVEF',lvef,'%','>=',hp.get('LVEF_min'),ok_lvef),
  {'id':'RR-AGE','category':'Freshness','field':'Laboratory freshness','current':age,'unit':'days','operator':'<=','threshold':hp.get('lab_max_age_days'),'status':'PASS' if freshness=='Current' else 'HOLD','outcome':'PASS' if freshness=='Current' else 'HOLD','source_record_id':data.get('lab_source_id',''),'source_finalized_at':data.get('lab_source_finalized_at',''),'result_date':ld,'freshness_days':age,'freshness_status':freshness},
 ]
 active_tox=data.get('active_toxicity_ids') or []
 rule_results.append({'id':'RR-TOX','category':'Toxicity','field':'Active toxicity review','current':data.get('toxicity_summary','') or 'No active toxicity recorded','unit':'CTCAE / clinical assessment','operator':'clinical review','threshold':'CCA regimen-specific toxicity rule','status':'REVIEW' if active_tox else 'PASS','outcome':'REVIEW' if active_tox else 'PASS','source_record_id':data.get('toxicity_source_id',''),'source_finalized_at':'','result_date':'','freshness_days':None,'freshness_status':'Not applicable'})
 monitoring=[]
 for req in protocol.get('monitoring_requirements',[]):
  cat=req.get('category');status='Required'
  if cat in ['Hematology','Renal','Hepatic']:
   status='Completed' if freshness=='Current' else ('Overdue' if freshness=='Stale' else 'Missing')
  elif cat=='Toxicity':status='Abnormal' if active_tox else 'Completed'
  monitoring.append({**req,'status':status,'source_record_id':data.get('lab_source_id','') if cat!='Toxicity' else data.get('toxicity_source_id',''),'evaluated_at':now()})
 return {'protocol_id':protocol['id'],'protocol_version':protocol['version'],'thresholds_source':'Institution Content Master / server-governed regimen version','lab_source_id':data.get('lab_source_id',''),'lab_source_finalized_at':data.get('lab_source_finalized_at',''),'normalized':normalized,'blockers':blockers,'alerts':alerts,'can_proceed':not blockers,'rule_results':rule_results,'monitoring_requirements':monitoring,'dose_modification_rules':protocol.get('dose_modification_rules',[]),'evaluation_as_of_date':eval_date.isoformat(),'lab_age_days_at_evaluation':age,'evaluated_at':now()}

def calc_dose(item,weight,bsa,cycle=1,renal=None):
 res=calculate_dose(item,weight,bsa,cycle,renal or {})
 return res.get('calculated_dose') if res.get('ok') else None

def cumulative_administered_by_code(c,pid):
 totals={}
 for inf in many(c,pid,'infusion'):
  oid=inf.get('data',{}).get('order_id');order=get_rec(c,oid) if oid else None
  if not order:continue
  by_item={x.get('item_id'):x for x in order.get('data',{}).get('items',[])}
  for mar in inf.get('data',{}).get('mar',[]):
   item=by_item.get(mar.get('item_id')) or {}
   code=mar.get('code') or item.get('code')
   val=safe_float(mar.get('actual_dose'))
   if code and val is not None and mar.get('completion_status') not in ['Held','Not Administered','Cancelled']:
    totals[code]=round(totals.get(code,0.0)+val,4)
 return totals

def verify_audit(c):
 prev='GENESIS'; errors=[]; n=0
 for r in c.execute('SELECT * FROM audit ORDER BY id'):
  n+=1; raw='|'.join([prev,r['patient_id'] or '',r['actor_id'],r['actor_role'],r['action'],r['entity_type'] or '',r['entity_id'] or '',r['detail'] or '',r['at']]); h=hashlib.sha256(raw.encode()).hexdigest()
  if r['prev_hash']!=prev or r['hash']!=h: errors.append(r['id'])
  prev=r['hash']
 return {'ok':not errors,'events':n,'errors':errors,'note':'Prototype hash chain. Production requires protected/WORM audit storage.'}

# =============================================================================
# PC4.0 — executable PRD catalogue / lifecycle engine
# =============================================================================
PC4_CATALOG_PATH=ROOT/'clinical_content'/'pc4_screen_catalog.json'
_PC4_CATALOG_CACHE={'mtime':None,'data':None}
def pc4_catalog():
 try:
  mtime=PC4_CATALOG_PATH.stat().st_mtime
  if _PC4_CATALOG_CACHE['data'] is None or _PC4_CATALOG_CACHE['mtime']!=mtime:
   _PC4_CATALOG_CACHE['data']=json.loads(PC4_CATALOG_PATH.read_text(encoding='utf-8'));_PC4_CATALOG_CACHE['mtime']=mtime
  return _PC4_CATALOG_CACHE['data']
 except Exception:return {'screens':[],'screen_count':0,'modules':{}}
def pc4_screen(sid):
 for x in pc4_catalog().get('screens',[]):
  if x.get('id')==sid:return x
 return None
def pc4_role_allowed(screen,role):
 return bool(screen and role in (screen.get('roles') or []))
def pc4_role_can_author(screen,role):
 return bool(screen and role in (screen.get('author_roles') or []))
def pc4_flat_fields(screen):
 out=list(screen.get('fields') or [])
 for t in screen.get('tables') or []:
  for c in t.get('columns') or []:
   out.append(c)
 return out
def pc4_num(v):
 try:return float(v)
 except:return None
def pc4_missing(v):return v is None or v=='' or v==[]
def pc4_value_by_label(screen,values,needle):
 n=needle.lower()
 for f in screen.get('fields') or []:
  if n in str(f.get('label','')).lower():return values.get(f.get('id'))
 return None
def pc4_derive(screen,values):
 d={}
 # Anthropometrics: detect discrete PRD labels, never infer from arbitrary prose fields.
 w=pc4_value_by_label(screen,values,'weight');h=pc4_value_by_label(screen,values,'height')
 wn=pc4_num(w);hn=pc4_num(h)
 if wn and hn and 15<=hn<=260 and 1<=wn<=500:
  d['bmi_kg_m2']=round(wn/((hn/100.0)**2),2)
  d['bsa_m2']=round(math.sqrt((hn*wn)/3600.0),3)
  d['bsa_formula']='Mosteller: sqrt(height_cm × weight_kg / 3600)'
 # RT dose/fraction arithmetic.
 total=pc4_value_by_label(screen,values,'total dose');fr=pc4_value_by_label(screen,values,'number of fractions')
 tn=pc4_num(total);fn=pc4_num(fr)
 if tn is not None and fn and fn>0:d['dose_per_fraction']=round(tn/fn,4)
 # Common arithmetic pairs.
 ordv=pc4_value_by_label(screen,values,'final ordered dose');act=pc4_value_by_label(screen,values,'actual administered dose')
 on=pc4_num(ordv);an=pc4_num(act)
 if on not in [None,0] and an is not None:d['administered_vs_ordered_variance_percent']=round((an-on)*100.0/on,2)
 prep=pc4_value_by_label(screen,values,'pharmacy prepared dose');pn=pc4_num(prep)
 if on not in [None,0] and pn is not None:d['prepared_vs_ordered_variance_percent']=round((pn-on)*100.0/on,2)
 vol=pc4_value_by_label(screen,values,'volume');dose=pc4_value_by_label(screen,values,'dose')
 vn=pc4_num(vol);dn=pc4_num(dose)
 if vn not in [None,0] and dn is not None:d['concentration_derived']=round(dn/vn,5)
 return d
def pc4_context(c,pid,role):
 if not pid:return {'patient':{},'episode':{},'source_summary':{}}
 pat=patient(c,pid) or {}; ep=current_episode(c,pid)
 # Clinical source context is intentionally a concise, provenance-bearing snapshot.
 src={}
 for typ in ['intake','diagnosis','treatment_plan','treatment_order','readiness','pharmacy','infusion','toxicity','radiation','surgery','pathology','radiology','response','admission','discharge']:
  r=latest(c,pid,typ)
  if r:src[typ]={'record_id':r['id'],'status':r['status'],'version':r['version'],'updated_at':r['updated_at']}
 return {'patient':project_patient(pat,role),'episode':{'record_id':ep['id'],'status':ep['status'],'version':ep['version'],'data':ep['data']} if ep else {},'source_summary':src,'captured_at':now()}
def pc4_validate(screen,values,for_sign=False):
 errors=[]; warnings=[]
 values=values or {}
 for f in screen.get('fields') or []:
  fid=f.get('id');v=values.get(fid);lab=f.get('label') or fid;typ=f.get('type')
  if f.get('readonly'):continue
  if for_sign and f.get('required') and pc4_missing(v):errors.append(lab+' is required')
  if pc4_missing(v):continue
  if typ=='number' and pc4_num(v) is None:errors.append(lab+' must be numeric')
  if typ=='select' and f.get('options') and str(v) not in [str(x) for x in f.get('options')]:errors.append(lab+' must use an allowed value')
  if typ=='multiselect' and f.get('options'):
   if not isinstance(v,list):errors.append(lab+' must contain a list of allowed values')
   elif any(str(x) not in [str(o) for o in f.get('options')] for x in v):errors.append(lab+' contains a value outside the configured set')
 for t in screen.get('tables') or []:
  key='table__'+t.get('id','table'); rows=values.get(key,[])
  if rows in [None,'']:rows=[]
  if not isinstance(rows,list):errors.append((t.get('label') or 'Table')+' must contain structured rows');continue
  for ri,row in enumerate(rows,1):
   if not isinstance(row,dict):errors.append(f"{t.get('label','Table')} row {ri} is invalid");continue
   for col in t.get('columns') or []:
    cv=row.get(col.get('id')); lab=col.get('label') or col.get('id')
    if for_sign and col.get('required') and pc4_missing(cv):errors.append(f"{t.get('label','Table')} row {ri}: {lab} is required")
    if pc4_missing(cv) or col.get('readonly'):continue
    if col.get('type')=='number' and pc4_num(cv) is None:errors.append(f"{t.get('label','Table')} row {ri}: {lab} must be numeric")
    if col.get('type')=='select' and col.get('options') and str(cv) not in [str(x) for x in col.get('options')]:errors.append(f"{t.get('label','Table')} row {ri}: {lab} must use an allowed value")
 # Safety guards for high-consequence authorising records.
 sid=screen.get('id','')
 if for_sign and sid=='SCR-RO-003':
  # Multiple phases can live in repeaters; if directly-entered total/fraction values exist they must be positive.
  for f in screen.get('fields') or []:
   lab=str(f.get('label','')).lower();v=values.get(f.get('id'))
   if ('total dose' in lab or 'number of fractions' in lab) and not pc4_missing(v):
    n=pc4_num(v)
    if n is None or n<=0:errors.append(f.get('label')+' must be positive')
 if for_sign and sid=='SCR-PAT-005':
  fd=pc4_value_by_label(screen,values,'final diagnosis')
  if pc4_missing(fd):errors.append('Final diagnosis is required for final pathology sign-out')
 if for_sign and sid=='SCR-RSP-007':
  cr=pc4_value_by_label(screen,values,'clinician-confirmed response')
  if pc4_missing(cr):errors.append('Clinician-confirmed response is required')
 # Generic signed-record governance warning when CCA-config masters are involved.
 if screen.get('module_code')=='C.26' and for_sign:
  warnings.append('Activation of clinical thresholds/content requires CCA institutional approval; signing this software record does not substitute for clinical governance.')
 return errors,warnings

def pc4_records(c,pid,role,screen_id=''):
 q="SELECT * FROM records WHERE entity_type='pc4_prd'";args=[]
 if pid:q+=' AND patient_id=?';args.append(pid)
 q+=' ORDER BY created_at DESC'
 out=[]
 for r in c.execute(q,args):
  z=dict(r);z['data']=jload(z.pop('data_json'),{})
  if screen_id and z['data'].get('screen_id')!=screen_id:continue
  sc=pc4_screen(z['data'].get('screen_id'))
  if sc and pc4_role_allowed(sc,role):out.append(z)
 return out

PC4_ACTION_TARGETS=[
 (r'order .*investigation|order investigations?|order pre-op workup','SCR-INV-001'),
 (r'submit to mdt|flag for mdt|re-list for mdt|refer back to mdt','SCR-MDT-001'),
 (r'create treatment plan|convert to plan','SCR-PLN-001'),
 (r'create treatment order|new cycle|continue to dosing','SCR-ORD-001'),
 (r'clearance|readiness','SCR-RDY-001'),
 (r'query pharmacy|request remake','SCR-PHA-003'),
 (r'record reaction','SCR-MAR-008'),
 (r'extravasation','SCR-MAR-009'),
 (r'create prescription|amend prescription','SCR-RO-003'),
 (r'planning|re-plan','SCR-RO-006'),
 (r'create surgical plan','SCR-SO-003'),
 (r'review pathology|pathology review','SCR-SO-014'),
 (r'adjuvant handoff','SCR-SO-018'),
 (r'response assessment','SCR-RSP-001'),
 (r'treatment summary|complete course','SCR-CMP-003'),
 (r'survivorship|surveillance plan','SCR-SURV-003'),
]
def pc4_action_target(action):
 a=str(action or '').lower()
 for pat,sid in PC4_ACTION_TARGETS:
  if re.search(pat,a,re.I):return sid
 return ''
def pc4_handoff_owner(screen):
 # First listed role is the accountable author/owner unless it is a view-only administrative actor.
 roles=screen.get('roles') or []
 return roles[0] if roles else ''

class H(BaseHTTPRequestHandler):
 server_version='CCA-V12.2-PC1.9/1.0'
 def handle_one_request(self):
  try:return super().handle_one_request()
  except Exception as exc:
   cid='ERR-'+uuid.uuid4().hex[:10].upper();print(f'[{cid}] Unhandled request error: {exc}',file=sys.stderr);traceback.print_exc()
   try:return self.sendj({'error':'Unexpected server error','correlation_id':cid},500)
   except Exception:return None
 def log_message(self,fmt,*args): pass
 def sendj(self,obj,status=200):
  b=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b)
 def body(self):
  n=int(self.headers.get('Content-Length','0') or 0);raw=self.rfile.read(n) if n else b'{}'
  try:return json.loads(raw.decode())
  except:return {}
 def auth(self,c):
  h=self.headers.get('Authorization','');tok=h[7:] if h.startswith('Bearer ') else ''
  if not tok:return None
  r=c.execute('SELECT * FROM sessions WHERE token=?',(tok,)).fetchone()
  if not r:return None
  try:
   if datetime.fromisoformat(r['expires_at'])<datetime.now().astimezone():return None
  except:return None
  u=c.execute('SELECT * FROM user_accounts WHERE id=? AND active=1',(r['user_id'],)).fetchone()
  if u:
   u=dict(u);REQUEST_CTX.actor={'id':u['id'],'username':u['username'],'name':u['display_name'],'role':u['role'],'professional_id':u['professional_id']}
  else:REQUEST_CTX.actor=USERS.get(r['role'],{'id':r['user_id'],'name':r['role'],'role':r['role']})
  return dict(r)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=='/api/health':return self.sendj({'ok':True,'product':'CCA Cancer Care HIS + Oncology EMR V12.2 Structural Conformance — PC4.0 PRD Screens + PC8.0 Connected Multidisciplinary','version':'12.2','build':'12.2-PC1.9-PC8.0','date':'2026-09-08','synthetic_test_content':True})
  if p.path.startswith('/static/') or p.path=='/':
   rel='index.html' if p.path=='/' else p.path[len('/static/'):];f=STATIC/rel
   if not f.exists():self.send_error(404);return
   mime=mimetypes.guess_type(f.name)[0] or 'application/octet-stream';b=f.read_bytes();self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b);return
  if p.path=='/api/login/users':
   c=db();rows=[{'username':r['username'],'display_name':r['display_name'],'role':r['role'],'professional_id':r['professional_id']} for r in c.execute('SELECT * FROM user_accounts WHERE active=1 ORDER BY role,display_name')];c.close();return self.sendj({'users':rows,'shared_role_login_enabled':ALLOW_SHARED_ROLE_LOGIN})
  c=db(); s=self.auth(c)
  if not s:c.close();return self.sendj({'error':'Authentication required'},401)
  role=s['role']
  if p.path=='/api/pc4/screens':
   cat=pc4_catalog();visible=[x for x in cat.get('screens',[]) if pc4_role_allowed(x,role)];c.close();return self.sendj({'build':cat.get('build'),'screen_count':cat.get('screen_count'),'visible_count':len(visible),'form_count':cat.get('form_count'),'worklist_count':cat.get('worklist_count'),'field_requirement_count':cat.get('field_requirement_count'),'modules':cat.get('modules'),'screens':visible,'source_boundary':cat.get('source_boundary')})
  if p.path=='/api/pc4/records':
   q=parse_qs(p.query);pid=q.get('patient',[''])[0];sid=q.get('screen',[''])[0]
   sc=pc4_screen(sid) if sid else None
   if sc and not pc4_role_allowed(sc,role):c.close();return self.sendj({'error':'Role is not authorized for this PRD screen'},403)
   if pid and not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   rows=pc4_records(c,pid,role,sid);c.close();return self.sendj({'records':rows})
  if p.path=='/api/pc4/context':
   q=parse_qs(p.query);pid=q.get('patient',[''])[0];sid=q.get('screen',[''])[0];sc=pc4_screen(sid)
   if not sc:c.close();return self.sendj({'error':'PRD screen not found'},404)
   if not pc4_role_allowed(sc,role):c.close();return self.sendj({'error':'Role is not authorized for this PRD screen'},403)
   if sc.get('module_code')!='C.26':
    if not pid or not patient(c,pid):c.close();return self.sendj({'error':'Patient required'},409)
    if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   out=pc4_context(c,pid,role);c.close();return self.sendj(out)
  if p.path=='/api/cca-validation/feedback':
   q=parse_qs(p.query);sid=(q.get('screen') or [''])[0];target=(q.get('target_id') or [''])[0];scope=(q.get('scope') or ['role'])[0]
   sql='SELECT * FROM cca_validation_feedback WHERE 1=1';args=[]
   if sid:sql+=' AND screen_id=?';args.append(sid)
   if target:sql+=' AND target_id=?';args.append(target)
   if role!='Hospital Management / Admin' or scope!='all':sql+=' AND reviewer_role=?';args.append(role)
   sql+=' ORDER BY created_at DESC'
   rows=[dict(r) for r in c.execute(sql,args)]
   c.close();return self.sendj({'feedback':rows,'count':len(rows)})
  if p.path=='/api/cca-validation/signoff':
   q=parse_qs(p.query);specialty=(q.get('specialty') or [role])[0]
   if specialty!=role and role!='Hospital Management / Admin':c.close();return self.sendj({'error':'A reviewer may view only their own specialty sign-off'},403)
   rows=[dict(r) for r in c.execute('SELECT * FROM cca_validation_signoff WHERE specialty_role=? ORDER BY created_at DESC',(specialty,))]
   c.close();return self.sendj({'signoffs':rows,'latest':rows[0] if rows else None})
  if p.path=='/api/cca-validation/summary':
   role_where='';args=[]
   if role!='Hospital Management / Admin':role_where=' WHERE reviewer_role=?';args=[role]
   rows=[dict(r) for r in c.execute('SELECT * FROM cca_validation_feedback'+role_where+' ORDER BY created_at DESC',args)]
   counts={}
   for r in rows:
    k=r.get('verdict') or 'Unspecified';counts[k]=counts.get(k,0)+1
   sev={}
   for r in rows:
    k=r.get('severity') or 'None';sev[k]=sev.get(k,0)+1
   c.close();return self.sendj({'count':len(rows),'verdicts':counts,'severity':sev,'feedback':rows[:200]})
  if p.path=='/api/meta':
   med_master=[{'id':x['id'],'label':x.get('display_name') or x.get('drug'),'drug':x.get('drug'),'code':x.get('code'),'code_system':x.get('code_system'),'allowed_routes':x.get('allowed_routes',[]),'formulations':x.get('formulations',[]),'clinical_content_status':'Synthetic QA / CCA formulary master'} for x in formulary_rows(c,True)]
   c.close();return self.sendj({'roles':ROLES,'value_sets':VALUE_SETS,'locations':LOCATION_MASTER,'lab_unit_options':LAB_UNIT_OPTIONS,'allergen_master':ALLERGEN_MASTER,'medication_master':med_master,'fall_risk_scales':FALL_RISK_SCALES,'diagnostic_catalog':list(DIAGNOSTIC_CATALOG.values()),'lab_abnormal_flags':LAB_ABNORMAL_FLAGS,'lab_reference_range_source':'INTEGRATED / server-owned Synthetic QA assay master','actor':actor(role),'product':'CCA V12.2-PC1.9 Structural Conformance Phase 7','synthetic_test_content_note':'Synthetic institutional content is for product testing/demonstration only; not patient care.'})
  if p.path=='/api/content':
   q=parse_qs(p.query);cat=q.get('category',[''])[0];needle=str(q.get('q',[''])[0]).strip().lower();status=str(q.get('status',[''])[0]).strip();rows=content_rows(c,cat)
   if needle: rows=[x for x in rows if needle in ' '.join([str(x.get(k,'')) for k in ['id','name','disease','setting','intent','line_of_therapy','version','status']]).lower()]
   if status: rows=[x for x in rows if str(x.get('status','')).lower()==status.lower()]
   src=[dict(x) for x in c.execute('SELECT * FROM content_sources ORDER BY name')];c.close();return self.sendj({'templates':rows,'sources':src,'categories':sorted(set(x['category'] for x in rows)),'query':needle,'status_filter':status})
  if p.path=='/api/formulary':
   if role not in ['Medical Oncology','Oncology Pharmacy','Hospital Management / Admin']:c.close();return self.sendj({'error':'Medical Oncology, Oncology Pharmacy or Admin required'},403)
   rows=formulary_rows(c,False);c.close();return self.sendj({'items':rows,'active_count':sum(1 for x in rows if x.get('status')=='Active'),'note':'Institution-level formulary master. Patient records reference it; they do not own it.'})
  if p.path=='/api/role-surface':
   wanted=parse_qs(p.query).get('role',[role])[0]
   if wanted!=role and role!='Hospital Management / Admin':c.close();return self.sendj({'error':'Admin required to inspect another role surface'},403)
   out=ROLE_SURFACES.get(wanted,{'input':[],'view':[],'output':[]});reviews=[dict(x) for x in c.execute('SELECT * FROM role_surface_reviews WHERE role_surface=? ORDER BY at DESC',(wanted,))];accepted=any(x.get('verdict')=='Accepted' for x in reviews);status='Specialist accepted' if accepted else 'Specialist review required';c.close();return self.sendj({'role':wanted,'surface':out,'status':status,'reviews':reviews})
  if p.path=='/api/content/template':
   tid=parse_qs(p.query).get('id',[''])[0];x=content_one(c,tid);c.close();return self.sendj(x if x else {'error':'Template not found'},200 if x else 404)
  if p.path=='/api/report/render':
   q=parse_qs(p.query);tid=q.get('template',[''])[0];pid=q.get('patient',[''])[0];rv=q.get('record_version',[''])[0]
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   out,code,err=render_report(c,pid,tid,role,rv);c.commit();c.close();return self.sendj(out if out is not None else err,code)
  if p.path=='/api/demo-showcase':
   cases=[]
   for spec in DEMO_SHOWCASE_CASES:
    pid=spec['patient_id']
    if not patient(c,pid) or not can_access_patient(c,role,pid):continue
    cf=core_flow_snapshot(c,pid);cases.append({**spec,'patient':project_patient(patient(c,pid),role),'current_treatment':cf.get('current_treatment',{}),'next_step':cf.get('next_step',{}),'drug_chart':cf.get('drug_chart',{}) if pid=='PAT-DEMO-CHEMO' else {},'journey':cf.get('journey',{})})
   c.close();return self.sendj({'synthetic_showcase':True,'disclaimer':'All showcase patients, treatments, thresholds, results, dates, doses and outcomes are synthetic and exist only to demonstrate information presentation and workflow. They are not CCA clinical policy or patient-care guidance.','cases':cases})
  if p.path=='/api/core-flow':
   if role=='External Consultant':c.close();return self.sendj({'error':'External consultant uses case-scoped access only'},403)
   pid=parse_qs(p.query).get('patient',['PAT-0001'])[0]
   if not patient(c,pid):c.close();return self.sendj({'error':'Patient not found'},404)
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   out=core_flow_snapshot(c,pid);c.close();return self.sendj(out)
  if p.path=='/api/pc7/terminology':
   c.close();return self.sendj({'terminology':ONCOLOGY_TERMINOLOGY,'ctcae_version':CTCAE_VERSION,'ctcae_terms':CTCAE_TERMS,'ctcae_attribution':CTCAE_ATTRIBUTION,'recist_version':RECIST_VERSION,'bsa_policy':BSA_POLICY})
  if p.path=='/api/finance/schemes':
   if role!='Finance / Billing':c.close();return self.sendj({'error':'Finance role required'},403)
   rows=[]
   for r in c.execute("SELECT * FROM finance_schemes WHERE status='Active' ORDER BY name"):
    z=dict(r);z['required_fields']=jload(z.pop('required_fields_json'),[]);z['package_model']=jload(z.pop('package_model_json'),{});rows.append(z)
   c.close();return self.sendj({'schemes':rows,'disclaimer':'Indicative workflow only. Definitive eligibility and package approval require current payer/official verification.'})
  if p.path=='/api/integrations':
   if role!='Hospital Management / Admin':c.close();return self.sendj({'error':'Admin required'},403)
   rows=[dict(r) for r in c.execute('SELECT * FROM integration_adapters ORDER BY id')];c.close();return self.sendj({'adapters':rows})
  if p.path=='/api/document-facts':
   q=parse_qs(p.query);pid=(q.get('patient') or [''])[0]
   if not pid:c.close();return self.sendj({'error':'patient query parameter is required'},400)
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   rows=[dict(r) for r in c.execute('SELECT * FROM document_facts WHERE patient_id=? ORDER BY created_at',(pid,))];c.close();return self.sendj({'facts':rows})
  if p.path=='/api/patients':
   if role=='External Consultant':c.close();return self.sendj({'error':'External consultant uses case-scoped access only'},403)
   rows=[project_patient(dict(x),role) for x in c.execute('SELECT * FROM patients ORDER BY name') if can_access_patient(c,role,x['id'])];c.close();return self.sendj({'patients':rows})
  if p.path=='/api/bootstrap':
   if role=='External Consultant':c.close();return self.sendj({'error':'External consultant uses case-scoped MDT access only'},403)
   pid=parse_qs(p.query).get('patient',['PAT-0001'])[0];pat=patient(c,pid)
   if not pat:c.close();return self.sendj({'error':'Patient not found'},404)
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   ents={}
   for typ in READ.get(role,set()):
    arr=many(c,pid,typ)
    if arr:ents[typ]=[project_record(x,role) for x in arr]
   docs=[]
   if 'documents' in READ.get(role,set()):
    docs=[dict(r) for r in c.execute('SELECT id,title,filename,mime,category,document_type,source_institution,document_date,uploaded_by,uploaded_at FROM documents WHERE patient_id=? ORDER BY uploaded_at DESC',(pid,))]
   aud=[]
   if role in ['Medical Oncology','Surgical Oncology','Radiation Oncology','Hospital Management / Admin','MDT Coordinator']:
    aud=[dict(r) for r in c.execute('SELECT id,actor_role,action,entity_type,entity_id,detail,at FROM audit WHERE patient_id=? ORDER BY id DESC LIMIT 150',(pid,))]
   c.close();return self.sendj({'patient':project_patient(pat,role),'entities':ents,'documents':docs,'audit':aud,'current_actor':actor(role),'value_sets':VALUE_SETS})
  if p.path.startswith('/api/document-file/'):
   did=p.path.split('/')[-1];r=c.execute('SELECT * FROM documents WHERE id=?',(did,)).fetchone()
   if not r:c.close();self.send_error(404);return
   if 'documents' not in READ.get(role,set()) or not can_access_patient(c,role,r['patient_id']):c.close();return self.sendj({'error':'Not authorized'},403)
   b=r['content']
   if b is None:c.close();self.send_error(404);return
   audit(c,r['patient_id'],role,'VIEW_DOCUMENT','document',did,r['title']);c.commit();c.close();self.send_response(200);self.send_header('Content-Type',r['mime']);self.send_header('Content-Disposition','attachment; filename="'+str(r['filename'] or r['id']).replace('"','')+'"');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'none'; sandbox");self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b);return
  if p.path=='/api/record-versions':
   rid=parse_qs(p.query).get('record',[''])[0];rec=get_rec(c,rid)
   if not rec:c.close();return self.sendj({'error':'Record not found'},404)
   if not role_can_read(role,rec['entity_type']) or not can_access_patient(c,role,rec['patient_id']):c.close();return self.sendj({'error':'Not authorized'},403)
   rows=[]
   for r in c.execute('SELECT * FROM record_versions WHERE record_id=? ORDER BY version',(rid,)):
    z=dict(r);z['data']=jload(z.pop('data_json'),{});rows.append(z)
   audit(c,rec['patient_id'],role,'VIEW_VERSION_HISTORY',rec['entity_type'],rid,'Version history viewed');c.commit();c.close();return self.sendj({'record_id':rid,'versions':rows})
  if p.path=='/api/tasks':
   q=parse_qs(p.query);pid=q.get('patient',[''])[0]
   if pid and not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   rows=[task_context(c,r,role) for r in tasks_for_role(c,role,pid)];c.close();return self.sendj({'tasks':rows,'owner_role':role})
  if p.path=='/api/task-source':
   tid=parse_qs(p.query).get('task',[''])[0];r=c.execute('SELECT * FROM tasks WHERE id=?',(tid,)).fetchone()
   if not r:c.close();return self.sendj({'error':'Task not found'},404)
   if role!='Hospital Management / Admin' and r['owner_role']!=role:c.close();return self.sendj({'error':'Task is not assigned to this role'},403)
   ctx=task_context(c,r,role);src=ctx.get('source_record')
   if not ctx.get('source_visible_to_role') and ctx.get('source_record_id'):ctx['consumable']=False;ctx['blocking_reason']='Owning role does not have minimum-necessary read permission for the task source; workflow configuration must be corrected before action.'
   elif src and src.get('status') in ['Superseded','Cancelled','Entered in Error']:ctx['consumable']=False;ctx['blocking_reason']='Source record is '+src.get('status')
   else:ctx['consumable']=True;ctx['blocking_reason']=''
   audit(c,r['patient_id'],role,'TASK_SOURCE_OPEN','task',tid,ctx.get('source_record_id',''));c.commit();c.close();return self.sendj(ctx)
  if p.path=='/api/ai-search':
   q=parse_qs(p.query);pid=q.get('patient',[''])[0];question=str(q.get('q',[''])[0]).strip()
   if not pid or not question:c.close();return self.sendj({'error':'patient and q are required'},409)
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   readable=READ.get(role,set());tokens=[x for x in re.findall(r'[a-z0-9]+',question.lower()) if len(x)>2];hits=[]
   for typ in readable:
    for r in many(c,pid,typ):
     blob=jdump(r.get('data',{})).lower();score=sum(1 for x in tokens if x in blob or x in typ.lower())
     if score:hits.append((score,r))
   hits.sort(key=lambda z:(z[0],z[1].get('updated_at','')),reverse=True);sources=[]
   for score,r in hits[:5]:sources.append({'record_id':r['id'],'entity_type':r['entity_type'],'status':r['status'],'version':r['version'],'updated_at':r['updated_at'],'excerpt':jdump(r['data'])[:700]})
   audit(c,pid,role,'AI_RECORD_SEARCH','patient_record','',question[:120]);c.commit();c.close()
   if not sources:return self.sendj({'answer':'I cannot determine this from the records available to your role.','sources':[],'grounded':True})
   return self.sendj({'answer':'Matching authorized patient-record evidence was found. Review the cited source records; this prototype search does not invent a clinical conclusion.','sources':sources,'grounded':True})
  if p.path=='/api/audit/verify':
   if role!='Hospital Management / Admin':c.close();return self.sendj({'error':'Admin required'},403)
   out=verify_audit(c);c.close();return self.sendj(out)
  if p.path=='/api/mdt/external-view':
   # authenticated External Consultant session plus separate case token
   if role!='External Consultant':c.close();return self.sendj({'error':'External Consultant role required'},403)
   tok=parse_qs(p.query).get('access',[''])[0];r=c.execute('SELECT * FROM external_tokens WHERE token=?',(tok,)).fetchone()
   if not r:c.close();return self.sendj({'error':'Invalid case token'},403)
   try:
    if datetime.fromisoformat(r['expires_at'])<datetime.now().astimezone():c.close();return self.sendj({'error':'Case token expired'},403)
   except:c.close();return self.sendj({'error':'Invalid expiry'},403)
   pid=r['patient_id'];dx=latest(c,pid,'diagnosis');m=latest(c,pid,'mdt');pa=latest(c,pid,'pathology');ra=latest(c,pid,'radiology')
   out={'case_code':'ANON-'+hashlib.sha256(pid.encode()).hexdigest()[:8].upper(),'scope':'De-identified MDT case only','expires_at':r['expires_at'],'diagnosis':{k:dx['data'].get(k) for k in ['cancer_type','primary_site','histology','stage_t','stage_n','stage_m','stage_group','ecog','biomarkers']} if dx else {},'mdt':{k:m['data'].get(k) for k in ['clinical_question','clinical_summary','intent','recommendation','alternatives','rationale','final_consensus']} if m else {},'pathology_summary':pa['data'].get('histology') if pa else '', 'imaging_summary':ra['data'].get('impression') if ra else ''}
   audit(c,pid,role,'EXTERNAL_MDT_VIEW','mdt',m['id'] if m else '',r['consultant_name']);c.commit();c.close();return self.sendj(out)
  c.close();self.send_error(404)

 def do_POST(self):
  p=urlparse(self.path);data=self.body();c=db()
  if p.path=='/api/login':
   # Selection-only sign-in: choosing a named validation user or a demo role is the entire
   # login action, no credential/PIN check. DEMO_USER_CREDENTIALS.txt remains a reference
   # roster of who each username maps to, it is no longer required to sign in.
   username=str(data.get('username') or '').strip()
   if username:
    u=c.execute('SELECT * FROM user_accounts WHERE username=? AND active=1',(username,)).fetchone()
    if not u:c.close();return self.sendj({'error':'Unknown validation user'},401)
    u=dict(u);act={'id':u['id'],'username':u['username'],'name':u['display_name'],'role':u['role'],'professional_id':u['professional_id']};REQUEST_CTX.actor=act;tok=secrets.token_urlsafe(32);exp=(datetime.now().astimezone()+timedelta(hours=SESSION_HOURS)).isoformat();c.execute('INSERT OR REPLACE INTO sessions VALUES(?,?,?,?)',(tok,u['id'],u['role'],exp));c.commit();c.close();return self.sendj({'token':tok,'actor':act,'expires_at':exp})
   role=data.get('role')
   if role not in ROLES:c.close();return self.sendj({'error':'Invalid demo role'},401)
   if not ALLOW_SHARED_ROLE_LOGIN:c.close();return self.sendj({'error':'Quick role demo login is disabled'},401)
   tok=secrets.token_urlsafe(32);exp=(datetime.now().astimezone()+timedelta(hours=SESSION_HOURS)).isoformat();c.execute('INSERT OR REPLACE INTO sessions VALUES(?,?,?,?)',(tok,actor(role)['id'],role,exp));c.commit();c.close();return self.sendj({'token':tok,'actor':actor(role),'expires_at':exp,'legacy_shared_role_login':True})
  if p.path=='/api/logout':
   tok=self.headers.get('Authorization','').removeprefix('Bearer ').strip()
   if tok:c.execute('DELETE FROM sessions WHERE token=?',(tok,));c.commit()
   c.close();return self.sendj({'ok':True,'session_revoked':True})
  s=self.auth(c)
  if not s:c.close();return self.sendj({'error':'Authentication required'},401)
  role=s['role']
  if p.path=='/api/pc4/action':
   sid=str(data.get('screen_id') or '');sc=pc4_screen(sid);act=str(data.get('action') or '').strip();rid=str(data.get('record_id') or '')
   if not sc:c.close();return self.sendj({'error':'PRD screen not found'},404)
   if not pc4_role_allowed(sc,role):c.close();return self.sendj({'error':'Role is not authorized for this PRD screen'},403)
   if act not in (sc.get('actions') or []):c.close();return self.sendj({'error':'Action is not defined on this PRD screen'},409)
   pid='' if sc.get('module_code')=='C.26' else str(data.get('patient_id') or '')
   if pid and (not patient(c,pid) or not can_access_patient(c,role,pid)):c.close();return self.sendj({'error':'Patient not found or access not assigned'},403)
   target=pc4_action_target(act);tasks=[]
   if target and pid:
    ts=pc4_screen(target)
    if ts:
     owner=pc4_handoff_owner(ts)
     if owner in ROLES and owner!=role:
      try:tasks.append(create_task(c,pid,owner,act,'PRD Handoff','High',sid,rid,'',((current_episode(c,pid) or {}).get('id') or ''),str(data.get('note') or ''),{'target_screen':target,'source_screen':sid,'action':act},role))
      except Exception:pass
   audit(c,pid,role,'PC4_PRD_ACTION',sid,rid,jdump({'action':act,'target_screen':target,'note':str(data.get('note') or '')[:500]}));c.commit();c.close();return self.sendj({'ok':True,'target_screen':target,'handoff_tasks':tasks})
  if p.path=='/api/pc4/record':
   sid=str(data.get('screen_id') or '');sc=pc4_screen(sid);op=str(data.get('op') or 'create').lower()
   if not sc:c.close();return self.sendj({'error':'PRD screen not found'},404)
   if sc.get('kind')!='form':c.close();return self.sendj({'error':'This PRD screen is a worklist/view, not a signable form'},409)
   if not pc4_role_can_author(sc,role):c.close();return self.sendj({'error':'Role may view this PRD screen but is not authorized to create/edit/sign its record'},403)
   pid='' if sc.get('module_code')=='C.26' else str(data.get('patient_id') or '')
   if sc.get('module_code')!='C.26':
    if not patient(c,pid):c.close();return self.sendj({'error':'Patient not found'},404)
    if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   vals=data.get('values') or {};rid=str(data.get('record_id') or '')
   if not isinstance(vals,dict):c.close();return self.sendj({'error':'values must be an object'},409)
   if op=='create':
    errs,warns=pc4_validate(sc,vals,False)
    if errs:c.close();return self.sendj({'error':'Validation failed','errors':errs,'warnings':warns},409)
    payload={'screen_id':sid,'screen_name':sc.get('name'),'module':sc.get('module'),'values':vals,'derived_values':pc4_derive(sc,vals),'source_context':pc4_context(c,pid,role),'lifecycle':'Draft','created_for_episode':((current_episode(c,pid) or {}).get('id') if pid else ''),'source_status':sc.get('source_status')}
    rid=new_record(c,pid,'pc4_prd',payload,'Draft',role);c.commit();out=get_rec(c,rid);c.close();return self.sendj({'ok':True,'record':out,'warnings':warns},201)
   rec=get_rec(c,rid)
   if not rec or rec.get('entity_type')!='pc4_prd' or rec.get('data',{}).get('screen_id')!=sid:c.close();return self.sendj({'error':'PC4 record not found'},404)
   if rec.get('patient_id')!=pid:c.close();return self.sendj({'error':'Patient/record mismatch'},409)
   expected=data.get('expected_version')
   if expected not in [None,''] and int(expected)!=int(rec.get('version',0)):c.close();return self.sendj({'error':'Version conflict — record changed since it was opened','current_version':rec.get('version')},409)
   if op=='update':
    if rec.get('status')!='Draft':c.close();return self.sendj({'error':'Only Draft records may be edited; create an amendment for a signed record'},409)
    errs,warns=pc4_validate(sc,vals,False)
    if errs:c.close();return self.sendj({'error':'Validation failed','errors':errs,'warnings':warns},409)
    out=update_rec(c,rid,{'values':vals,'derived_values':pc4_derive(sc,vals),'last_source_context':pc4_context(c,pid,role)},'Draft',role,'PC4_DRAFT_UPDATE','Draft structured fields updated');c.commit();c.close();return self.sendj({'ok':True,'record':out,'warnings':warns})
   if op=='sign':
    if rec.get('status')!='Draft':c.close();return self.sendj({'error':'Only a Draft may be signed'},409)
    current=vals if vals else rec.get('data',{}).get('values',{})
    errs,warns=pc4_validate(sc,current,True)
    if errs:c.close();return self.sendj({'error':'Cannot sign: validation failed','errors':errs,'warnings':warns},409)
    attest=str(data.get('attestation') or 'I affirm this record is complete and accurate for its intended clinical/operational use.').strip()
    frozen=pc4_context(c,pid,role)
    out=update_rec(c,rid,{'values':current,'derived_values':pc4_derive(sc,current),'signed_snapshot':{'values':current,'derived_values':pc4_derive(sc,current),'source_context':frozen},'lifecycle':'Signed','signed_by':actor(role),'signed_at':now(),'attestation':attest},'Signed',role,'PC4_SIGN','Explicit sign/finalize with frozen-value snapshot');
    # Downstream task on explicit signing when the action map has a natural target.
    c.commit();c.close();return self.sendj({'ok':True,'record':out,'warnings':warns})
   if op=='amend':
    if rec.get('status') not in ['Signed','Amended']:c.close();return self.sendj({'error':'Only a signed/current record can be amended'},409)
    reason=str(data.get('reason') or '').strip()
    if not reason:c.close();return self.sendj({'error':'Amendment reason is required'},409)
    newvals=vals or rec.get('data',{}).get('values',{})
    newdata={**rec.get('data',{}),'values':newvals,'derived_values':pc4_derive(sc,newvals),'lifecycle':'Draft Amendment','supersedes_record_id':rid,'amendment_reason':reason,'signed_by':None,'signed_at':None,'attestation':''}
    nrid=new_record(c,pid,'pc4_prd',newdata,'Draft',role)
    update_rec(c,rid,{'superseded_by_record_id':nrid,'superseded_reason':reason},'Superseded',role,'PC4_SUPERSEDE','Superseded by amendment '+nrid)
    c.commit();out=get_rec(c,nrid);c.close();return self.sendj({'ok':True,'record':out,'superseded_record_id':rid},201)
   c.close();return self.sendj({'error':'Unsupported PC4 record operation'},409)
  if p.path=='/api/cca-validation/feedback':
   sid=str(data.get('screen_id') or '').strip();sc=pc4_screen(sid)
   if not sc:c.close();return self.sendj({'error':'PRD screen not found'},404)
   if not pc4_role_allowed(sc,role) and role!='Hospital Management / Admin':c.close();return self.sendj({'error':'Reviewer role is not assigned to this PRD screen'},403)
   verdict=str(data.get('verdict') or '').strip();allowed=['Correct — Freeze','Change Required','Missing','Should Be Conditional','Should Be Integration','Not Applicable','Needs Discussion']
   if verdict not in allowed:c.close();return self.sendj({'error':'Validation verdict required','allowed':allowed},409)
   sev=str(data.get('severity') or 'None');sevs=['None','S1 — Safety / workflow blocker','S2 — Major','S3 — Moderate','S4 — Minor']
   if sev not in sevs:c.close();return self.sendj({'error':'Invalid severity','allowed':sevs},409)
   suggestion=str(data.get('suggestion') or '').strip();expected=str(data.get('expected') or '').strip();actual=str(data.get('actual') or '').strip()
   if verdict not in ['Correct — Freeze','Not Applicable'] and not (suggestion or expected):c.close();return self.sendj({'error':'A change/gap verdict requires expected behavior or suggested correction'},409)
   rid='CVF-'+uuid.uuid4().hex[:10].upper();stamp=now();pid=str(data.get('patient_id') or '')
   target_type=str(data.get('target_type') or 'Screen');target_id=str(data.get('target_id') or sid);target_label=str(data.get('target_label') or sc.get('name') or sid);dimension=str(data.get('dimension') or 'Overall screen / workflow')
   freeze=1 if verdict=='Correct — Freeze' or bool(data.get('freeze_correct')) else 0
   c.execute('INSERT INTO cca_validation_feedback VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(rid,'V12.2-PC4.0',pid,role,actor(role)['id'],sid,sc.get('module',''),target_type,target_id,target_label,dimension,verdict,sev,expected,actual,suggestion,freeze,'Open',stamp,stamp))
   audit(c,pid,role,'CCA_VALIDATION_FEEDBACK','cca_validation',rid,f'{sid} • {target_type} • {target_label} • {verdict} • {sev}')
   c.commit();c.close();return self.sendj({'ok':True,'id':rid,'verdict':verdict,'severity':sev},201)
  if p.path=='/api/cca-validation/signoff':
   specialty=str(data.get('specialty_role') or role)
   if specialty!=role and role!='Hospital Management / Admin':c.close();return self.sendj({'error':'A reviewer may sign off only their own specialty; Admin may record an externally supplied sign-off'},403)
   decision=str(data.get('decision') or '').strip();allowed=['Accepted for CCA configuration / integration phase','Accepted with required changes','Not accepted — workflow or information model requires redesign']
   if decision not in allowed:c.close();return self.sendj({'error':'Specialty validation decision required','allowed':allowed},409)
   rid='CVS-'+uuid.uuid4().hex[:10].upper();stamp=now();vals=(rid,'V12.2-PC4.0',specialty,role,actor(role)['id'],decision,str(data.get('what_to_freeze') or ''),str(data.get('required_changes') or ''),str(data.get('content_needed') or ''),str(data.get('integration_needed') or ''),stamp,stamp)
   c.execute('INSERT INTO cca_validation_signoff VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',vals);audit(c,'',role,'CCA_VALIDATION_SIGNOFF','cca_validation_signoff',rid,specialty+' • '+decision);c.commit();c.close();return self.sendj({'ok':True,'id':rid,'decision':decision},201)
  if p.path=='/api/duplicate-check':
   if role not in ['Front Desk','Patient Attender','PRE / Patient Relations Executive','Health Information Management']:c.close();return self.sendj({'error':'Front Desk/Patient Attender/PRE/HIM required'},403)
   matches=duplicate_candidates(c,data.get('name'),data.get('dob'),data.get('phone'),data.get('abha'),data.get('id_number'),data.get('mrn'));c.close();return self.sendj({'matches':matches,'high_risk_count':sum(1 for x in matches if x['risk']=='High'),'message':'Resolve High-risk duplicate candidates before creating a new patient.'})
  if p.path=='/api/patient':
   if role not in ['Front Desk','Patient Attender']:c.close();return self.sendj({'error':'Front Desk/Patient Attender required'},403)
   name=str(data.get('name','')).strip();dob=str(data.get('dob','')).strip();phone=str(data.get('phone','')).strip();abha=normalize_abha(data.get('abha'));idn=str(data.get('id_number','')).strip()
   if not all([name,dob,phone,idn]):c.close();return self.sendj({'error':'Name, DOB, phone and ID number are mandatory'},409)
   ok_dob,msg=valid_dob(dob)
   if not ok_dob:c.close();return self.sendj({'error':msg},409)
   if abha and not valid_abha(abha):c.close();return self.sendj({'error':'ABHA must contain exactly 14 digits when supplied'},409)
   matches=[]
   for r in c.execute('SELECT * FROM patients'):
    score=0;reasons=[]
    if abha and r['abha']==abha:score+=100;reasons.append('ABHA match')
    if r['name'].lower()==name.lower() and r['dob']==dob:score+=90;reasons.append('Name + DOB match')
    if r['phone']==phone:score+=50;reasons.append('Phone match')
    if score>=50:matches.append({'patient_id':r['id'],'mrn':r['mrn'],'name':r['name'],'score':score,'reasons':reasons})
   if matches and not str(data.get('duplicate_override_reason','')).strip():c.close();return self.sendj({'error':'Potential duplicate patient','matches':matches},409)
   pid='PAT-'+uuid.uuid4().hex[:8].upper();mrn='CCA-'+datetime.now().strftime('%Y')+'-'+uuid.uuid4().hex[:5].upper();t=now();c.execute('INSERT INTO patients VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(pid,mrn,name,dob,data.get('sex',''),phone,abha,idn,data.get('initial_specialty','Front Desk'),'Active','',t,t))
   new_record(c,pid,'registration',{'arrival_type':data.get('arrival_type','Walk-in'),'assigned_specialty':data.get('initial_specialty','Medical Oncology'),'clinician_assignment':data.get('clinician_assignment',''),'route_rule':data.get('route_rule','Manual routing'),'referral_doctor_name':'','referral_facility':'','referral_network_level3':'','referral_reason':'','address':'','general_consent':'Pending','photo_status':'Pending'},'Draft',role)
   new_record(c,pid,'referral',{'referral_no':'REF-'+uuid.uuid4().hex[:7].upper(),'source_type':data.get('arrival_type','Walk-in'),'referring_doctor':data.get('referring_doctor',''),'referring_facility':data.get('referring_facility',''),'reason':data.get('referral_reason',''),'priority':data.get('referral_priority','Routine'),'assigned_department':data.get('initial_specialty','Medical Oncology'),'assigned_clinician':data.get('clinician_assignment',''),'status':'Created','history':[{'at':t,'from':'','to':'Created','by':actor(role),'reason':'Patient registration'}]},'Created',role)
   new_record(c,pid,'consent',{'items':[]},'Active',role);new_record(c,pid,'appointments',{'items':[]},'Active',role);new_record(c,pid,'queue',{'current_location':'Front Desk','current_status':'In Service','priority':'Routine','token':'FD-'+uuid.uuid4().hex[:4].upper(),'history':[{'at':t,'from':'Arrival','to':'Front Desk','status':'Arrived','actor':actor(role)['name']}]},'Active',role)
   new_record(c,pid,'journey',{'current_location':'Front Desk','current_care_stage':'Registration','events':[{'id':'JNY-'+uuid.uuid4().hex[:8].upper(),'at':t,'department':'Registration','care_stage':'Registration','clinician':actor(role)['name'],'actor_role':role,'status':'Current','source_type':'registration','source_id':'','note':'Patient arrived'}]},'Active',role);epid=new_record(c,pid,'cancer_episode',{'episode_no':'EP-'+uuid.uuid4().hex[:6].upper(),'kind':'Primary cancer','label':'Oncology episode under evaluation','started_at':t,'ended_at':'','closure_reason':'','primary_diagnosis_id':'','status':'Active'},'Active',role);new_record(c,pid,'admission',{'admissions':[]},'Active',role);new_record(c,pid,'inpatient_care',{'daily_notes':[],'nursing_observations':[],'intake_output':[],'pain_assessments':[],'toxicity_events':[],'specialty_reviews':[],'inpatient_medication_orders':[]},'Active',role);new_record(c,pid,'discharge',{'summaries':[]},'Active',role);new_record(c,pid,'continuous_therapy',{'courses':[]},'Active',role);new_record(c,pid,'tumor_marker',{'measurements':[]},'Active',role)
   new_record(c,pid,'intake',{},'Draft',role);new_record(c,pid,'med_recon',{'items':[],'allergies':[],'allergy_status':'Unable to verify','reconciliation_events':[]},'Draft',role);new_record(c,pid,'dynamic_forms',{'definitions':latest(c,'PAT-0001','dynamic_forms')['data']['definitions'],'responses':{}},'Active',role);new_record(c,pid,'consultation',{},'Draft',role);new_record(c,pid,'diagnosis',{'biomarkers':[]},'Draft',role);new_record(c,pid,'care_plan',{'goals':[],'milestones':[],'dependencies':[],'status':'Draft'},'Draft',role);new_record(c,pid,'finance',{'payment_events':[]},'Active',role);new_record(c,pid,'conversion',{'tracking':[]},'Active',role)
   # Empty but real workspaces allow a newly registered patient to traverse the same downstream workflow.
   new_record(c,pid,'pathology',{},'Draft',role);new_record(c,pid,'mdt',{'case_no':'MDT-'+uuid.uuid4().hex[:6].upper(),'attendees':[]},'Draft',role);new_record(c,pid,'mdt_collab',{'comments':[],'attendance':[],'external_consultants':[]},'Active',role);new_record(c,pid,'mdt_followup',{'action_items':[]},'Active',role);new_record(c,pid,'treatment_plan',{'plan_no':'TP-'+uuid.uuid4().hex[:6].upper(),'version':1,'sequence':[],'phases':[]},'Draft',role);new_record(c,pid,'protocol_library',{'protocols':[PROTOCOL]},'Active',role);new_record(c,pid,'formulary',FORMULARY,'Active',role);new_record(c,pid,'readiness',{},'Draft',role);new_record(c,pid,'toxicity',{'events':[]},'Active',role);new_record(c,pid,'modification',{'items':[]},'Active',role);new_record(c,pid,'response',{'baseline':{'target_lesions':[]},'assessments':[]},'Active',role);new_record(c,pid,'radiation',{'prescription':{'status':'Draft'},'planning':{'simulation_status':'Pending','contouring_status':'Pending','planning_status':'Pending','physics_qa':'Pending','physics_qa_plan_version':None,'physics_qa_prescription_version':None,'physician_final_approval':'Pending','physician_approval_plan_version':None,'physician_approval_prescription_version':None,'dicom_refs':{}},'fractions':[],'interruptions':[]},'Draft',role);new_record(c,pid,'surgery',{'plan':{'status':'Recommended'},'preop':{'anesthesia_clearance':'Pending','labs':'Pending','consent':'Pending','ready':False},'outcome':{},'histopathology_link':''},'Recommended',role);new_record(c,pid,'treatment_history',{'episodes':[]},'Active',role);new_record(c,pid,'visit_summary',{},'Draft',role)
   initial=str(data.get('initial_specialty') or 'Medical Oncology');initial_roles={'Medical Oncology':['Medical Oncology'],'Surgical Oncology':['Surgical Oncology'],'Radiation Oncology':['Radiation Oncology']}.get(initial,['Medical Oncology'])
   for rr in ['Nurse Navigator','Intake Nurse','PRE / Patient Relations Executive','Biller','Finance / Billing','Patient Liaison',role]+initial_roles:grant_patient_access(c,pid,rr,'registration',pid,role)
   audit(c,pid,role,'PATIENT_CREATED','patient',pid,'New registration');c.commit();c.close();return self.sendj({'ok':True,'id':pid,'mrn':mrn,'matches':matches})
  if p.path=='/api/document-fact':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology','Pathology','Radiologist','Nurse Navigator']:c.close();return self.sendj({'error':'Clinical reviewer role required'},403)
   pid=str(data.get('patient_id') or '');docid=str(data.get('document_id') or '');doc=c.execute('SELECT * FROM documents WHERE id=? AND patient_id=?',(docid,pid)).fetchone()
   if not doc:c.close();return self.sendj({'error':'Patient-linked source document required'},404)
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   if not str(data.get('fact_name') or '').strip() or not str(data.get('fact_value') or '').strip():c.close();return self.sendj({'error':'fact_name and fact_value required'},409)
   rid='DF-'+uuid.uuid4().hex[:10].upper();stamp=now();method=str(data.get('extraction_method') or 'Manual clinician abstraction')
   c.execute('INSERT INTO document_facts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(rid,pid,docid,str(data.get('fact_name')),str(data.get('fact_value')),str(data.get('code_system') or ''),str(data.get('code') or ''),str(data.get('page_ref') or ''),str(data.get('section_ref') or ''),str(data.get('source_snippet') or ''),method,float(data.get('confidence') or 1.0),'Validated',actor(role)['id'],stamp,stamp));audit(c,pid,role,'DOCUMENT_FACT_VALIDATE','document_fact',rid,f'{docid} • {data.get("fact_name")}');c.commit();c.close();return self.sendj({'ok':True,'id':rid,'status':'Validated'},201)
  if p.path=='/api/document':
   if role not in ['Front Desk','Patient Attender','PRE / Patient Relations Executive','Patient Liaison','Nurse Navigator','Medical Oncology','Radiology Coordinator','Radiology Technician','Radiologist','Laboratory / Phlebotomy','Pathology','Surgical Oncology','Radiation Oncology']:c.close();return self.sendj({'error':'Not authorized to upload documents'},403)
   pid=data.get('patient_id');pat=patient(c,pid)
   if not pat:c.close();return self.sendj({'error':'Patient not found'},404)
   if not can_access_patient(c,role,pid):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   raw=str(data.get('content_base64',''));raw=raw.split(',',1)[-1]
   try:b=base64.b64decode(raw,validate=False)
   except:c.close();return self.sendj({'error':'Invalid file content'},400)
   if len(b)>8*1024*1024:c.close();return self.sendj({'error':'File too large for demo (8MB max)'},413)
   sniff=b[:2048].lstrip().lower()
   if any(x in sniff for x in [b'<html',b'<script',b'<svg',b'javascript:',b'<!doctype html']):c.close();return self.sendj({'error':'Active document content is not accepted even when the declared MIME type is different'},415)
   did='DOC-'+uuid.uuid4().hex[:10].upper();mime=str(data.get('mime') or 'application/octet-stream').lower().split(';')[0].strip()
   if mime in ACTIVE_CONTENT_MIME or mime not in SAFE_UPLOAD_MIME:c.close();return self.sendj({'error':'Active or unsupported document content type is not accepted','mime':mime,'allowed':sorted(SAFE_UPLOAD_MIME)},415)
   title=data.get('title') or data.get('filename') or did
   c.execute('INSERT INTO documents VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(did,pid,title,data.get('filename','upload'),mime,data.get('category','Other'),data.get('document_type','Other'),data.get('source_institution',''),data.get('document_date',''),b,actor(role)['id'],now()))
   if data.get('category')=='Patient Photo':c.execute('UPDATE patients SET photo_document_id=?,updated_at=? WHERE id=?',(did,now(),pid));reg=latest(c,pid,'registration');update_rec(c,reg['id'],{'photo_status':'Uploaded','photo_document_id':did},role=role,action='PHOTO_LINK') if reg else None
   audit(c,pid,role,'DOCUMENT_UPLOAD','document',did,title);c.commit();c.close();return self.sendj({'ok':True,'id':did})
  if p.path=='/api/task-action':
   tid=data.get('task_id');op=data.get('operation');r=c.execute('SELECT * FROM tasks WHERE id=?',(tid,)).fetchone()
   if not r:c.close();return self.sendj({'error':'Task not found'},404)
   t=task_row(r)
   if role!='Hospital Management / Admin' and t['owner_role']!=role:c.close();return self.sendj({'error':'Task belongs to another role'},403)
   if not can_access_patient(c,role,t['patient_id']):c.close();return self.sendj({'error':'Patient access not assigned to this role'},403)
   stamp=now();fields=[];args=[]
   if op=='acknowledge':fields=['status=?','acknowledged_at=?','acknowledged_by=?'];args=['Acknowledged',stamp,actor(role)['id']]
   elif op=='complete':fields=['status=?','completed_at=?','completed_by=?'];args=['Completed',stamp,actor(role)['id']]
   elif op=='cancel':fields=['status=?','reason=?'];args=['Cancelled',str(data.get('reason') or 'Cancelled by owner')]
   elif op=='escalate':fields=['priority=?','escalation_level=escalation_level+1','reason=?'];args=['Critical',str(data.get('reason') or 'Escalated')]
   elif op=='reassign':
    nr=data.get('owner_role')
    if nr not in ROLES:c.close();return self.sendj({'error':'Valid owner_role required'},409)
    fields=['owner_role=?','owner_user_id=?'];args=[nr,actor(nr)['id']];grant_patient_access(c,t['patient_id'],nr,'task',tid,role)
   else:c.close();return self.sendj({'error':'Invalid task operation'},409)
   fields+=['updated_at=?','updated_by=?'];args += [stamp,actor(role)['id'],tid];c.execute('UPDATE tasks SET '+','.join(fields)+' WHERE id=?',args);audit(c,t['patient_id'],role,'TASK_'+op.upper(),'task',tid,str(data.get('reason') or ''));c.commit();out=task_row(c.execute('SELECT * FROM tasks WHERE id=?',(tid,)).fetchone());c.close();return self.sendj({'ok':True,'task':out})
  if p.path=='/api/action':
   out,status=self.action(c,role,data);c.commit();c.close();return self.sendj(out,status)
  c.close();self.send_error(404)

 def action(self,c,role,req):
  a=req.get('action');pid=req.get('patient_id');eid=req.get('entity_id');d=req.get('data') or {};e=get_rec(c,eid) if eid else None
  def need(r): return role in r
  def must(typ):
   nonlocal e
   if e and e['entity_type']==typ:return e
   e=latest(c,pid,typ);return e
  if not patient(c,pid):return {'error':'Patient not found'},404
  if not can_access_patient(c,role,pid):return {'error':'Patient access not assigned to this role'},403
  if e and e.get('patient_id')!=pid:return {'error':'entity_id does not belong to the selected patient'},409
  if a in OPTIMISTIC_LOCK_ACTIONS:
   optimistic_type={'save_intake':'intake','med_recon':'med_recon','save_dynamic_form':'dynamic_forms','save_consultation':'consultation','save_diagnosis':'diagnosis','save_appointment':'appointments','queue_patient':'queue','save_care_plan':'care_plan','save_treatment_plan':'treatment_plan','save_radiology':'radiology','save_pathology':'pathology','mdt_comment':'mdt_collab','mdt_attendance':'mdt_collab','mdt_recommend':'mdt'}.get(a,'')
   # Authorization must be evaluated before record-version/concurrency details so a
   # forbidden role cannot learn whether a record exists or what its current version is.
   if optimistic_type and role not in WRITE.get(optimistic_type,set()):return {'error':'Role is not authorized for this action'},403
   target=e or (latest(c,pid,optimistic_type) if pid and optimistic_type else None)
   if target:
    if req.get('expected_version') in [None,'']:return {'error':'expected_version is required for conflict-safe updates','current_version':target['version']},428
    try:expected=int(req.get('expected_version'))
    except:return {'error':'expected_version must be an integer','current_version':target['version']},409
    if expected!=int(target['version']):return {'error':'Record changed since it was loaded','expected_version':expected,'current_version':target['version'],'record_id':target['id']},409
  if a=='create_cancer_episode':
   if role not in WRITE['cancer_episode']:return {'error':'Oncology clinician required'},403
   kind=d.get('kind') or 'New primary cancer';label=str(d.get('label') or '').strip()
   if not label:return {'error':'Cancer episode label required'},409
   rid=new_record(c,pid,'cancer_episode',{'episode_no':'EP-'+uuid.uuid4().hex[:6].upper(),'kind':kind,'label':label,'started_at':d.get('started_at') or now(),'ended_at':'','closure_reason':'','primary_diagnosis_id':'','status':'Active','created_by':actor(role)},'Active',role)
   journey_add(c,pid,role,'New Cancer Episode','Active',role,'cancer_episode',rid,label,True);return {'ok':True,'id':rid},200
  if a=='close_cancer_episode':
   if role not in WRITE['cancer_episode']:return {'error':'Oncology clinician required'},403
   target=get_rec(c,d.get('episode_id') or eid) if (d.get('episode_id') or eid) else current_episode(c,pid);reason=str(d.get('reason') or '').strip()
   if not target or target.get('entity_type')!='cancer_episode':return {'error':'Cancer episode not found'},404
   if not reason:return {'error':'Episode closure reason required'},409
   if target['status'] not in ['Active','Open']:return {'error':'Only an active cancer episode can be closed'},409
   update_rec(c,target['id'],{'ended_at':d.get('ended_at') or str(date.today()),'closure_reason':reason,'status':'Closed'},'Closed',role,'EPISODE_CLOSE',reason);close_future_work(c,pid,role,reason);journey_add(c,pid,'Episode Closure','Cancer Episode Closed','Closed',role,'cancer_episode',target['id'],reason,True);return {'ok':True,'episode_id':target['id'],'status':'Closed'},200
  if a=='reopen_cancer_episode':
   if role not in WRITE['cancer_episode']:return {'error':'Oncology clinician required'},403
   target=get_rec(c,d.get('episode_id') or eid);reason=str(d.get('reason') or '').strip()
   if not target or target.get('entity_type')!='cancer_episode':return {'error':'Cancer episode not found'},404
   if not reason:return {'error':'Reopen reason required'},409
   if current_episode(c,pid):return {'error':'Another active cancer episode already exists'},409
   rid=new_record(c,pid,'cancer_episode',{**target['data'],'episode_no':'EP-'+uuid.uuid4().hex[:6].upper(),'started_at':d.get('started_at') or str(date.today()),'ended_at':'','closure_reason':'','status':'Active','reopens':target['id'],'reopen_reason':reason,'reopened_by':actor(role),'reopened_at':now()},'Active',role);journey_add(c,pid,role,'Cancer Episode Reopened','Active',role,'cancer_episode',rid,reason,True);return {'ok':True,'episode_id':rid,'reopens':target['id']},200
  if a=='admit_patient':
   if role not in WRITE['admission']:return {'error':'Oncology/Day Care clinician required to initiate admission'},403
   e=must('admission');atype=d.get('admission_type');reason_code=d.get('reason_code') or d.get('reason')
   if atype not in VALUE_SETS['admission_type']:return {'error':'Governed admission type required','allowed':VALUE_SETS['admission_type']},409
   if reason_code not in VALUE_SETS['admission_reason']:return {'error':'Governed admission reason required','allowed':VALUE_SETS['admission_reason']},409
   active=[x for x in e['data'].get('admissions',[]) if x.get('status')=='Active']
   if active:return {'error':'Patient already has an active admission','admission_id':active[-1]['id']},409
   ep=get_rec(c,d.get('episode_id')) if d.get('episode_id') else (current_episode(c,pid) or ensure_episode(c,pid,role))
   if not ep or ep.get('entity_type')!='cancer_episode':return {'error':'Valid cancer episode required for admission'},409
   x={'id':'ADM-'+uuid.uuid4().hex[:8].upper(),'episode_id':ep['id'],'admission_type':atype,'reason_code':reason_code,'reason_note':d.get('reason_note',''),'admitting_specialty':d.get('admitting_specialty') or role,'attending_clinician':d.get('attending_clinician') or actor(role)['name'],'admitted_at':d.get('admitted_at') or now(),'ward':d.get('ward','Unassigned'),'bed':d.get('bed','Unassigned'),'source_context':d.get('source_context','OPD / Day Care'),'status':'Active','created_by':actor(role)}
   rows=list(e['data'].get('admissions',[]));rows.append(x);update_rec(c,e['id'],{'admissions':rows},'Active',role,'IPD_ADMISSION',reason_code);grant_patient_access(c,pid,'Inpatient Oncology Nurse','admission',e['id'],role);grant_patient_access(c,pid,'Inpatient Oncology Clinician','admission',e['id'],role);handoff(c,pid,'Inpatient Oncology Nurse','Complete nursing admission and bed assignment','IPD nursing admission','admission',e['id'],role,'High',reason_code,{'admission':x});handoff(c,pid,'Inpatient Oncology Clinician','Complete inpatient admission history & physical','IPD admission assessment','admission',e['id'],role,'High',reason_code,{'admission':x});journey_add(c,pid,'Inpatient Care','Admitted', 'Active',role,'admission',x['id'],reason_code,True);return {'ok':True,'admission':x,'next_roles':['Inpatient Oncology Nurse','Inpatient Oncology Clinician']},200
  if a=='assign_inpatient_bed':
   if role not in ['Nurse Navigator','Medical Oncology','Surgical Oncology','Radiation Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Surgical Nurse']:return {'error':'Clinical inpatient role required'},403
   e=must('admission');rows=list(e['data'].get('admissions',[]));x=next((x for x in rows if x.get('id')==d.get('admission_id') and x.get('status')=='Active'),None)
   if not x:return {'error':'Active admission not found'},404
   if not d.get('ward') or not d.get('bed'):return {'error':'Ward and bed are required'},409
   x.update({'ward':d['ward'],'bed':d['bed'],'assigned_at':now(),'assigned_by':actor(role)});update_rec(c,e['id'],{'admissions':rows},'Active',role,'IPD_BED_ASSIGN',d['ward']+' / '+d['bed']);journey_add(c,pid,'Inpatient Care',f"{d['ward']} / {d['bed']}",'Active',role,'admission',x['id'],'Bed assigned',True);return {'ok':True,'admission':x},200
  if a=='record_inpatient_observation':
   if role not in WRITE['inpatient_care']:return {'error':'Inpatient clinical role required'},403
   e=must('inpatient_care');adm=latest(c,pid,'admission');active=next((x for x in reversed(adm['data'].get('admissions',[])) if x.get('status')=='Active'),None) if adm else None
   if not active:return {'error':'Active admission required'},409
   typ=d.get('type') or 'Nursing observation';x={'id':'IPDOBS-'+uuid.uuid4().hex[:7].upper(),'admission_id':active['id'],'episode_id':active['episode_id'],'type':typ,'at':d.get('at') or now(),'vitals':d.get('vitals',{}),'pain_score':d.get('pain_score'),'intake_ml':d.get('intake_ml'),'output_ml':d.get('output_ml'),'note':d.get('note',''),'recorded_by':actor(role)}
   key='daily_notes' if typ=='Daily note' else 'nursing_observations';rows=list(e['data'].get(key,[]));rows.append(x);update_rec(c,e['id'],{key:rows},'Active',role,'IPD_OBSERVATION',typ);return {'ok':True,'record':x},200
  if a=='record_inpatient_toxicity':
   if role not in WRITE['inpatient_care']:return {'error':'Inpatient clinical role required'},403
   ipd=must('inpatient_care');tox=latest(c,pid,'toxicity');term=d.get('term');grade=str(d.get('grade') or '')
   if not term or grade not in VALUE_SETS['ctcae_grade']:return {'error':'CTCAE term and grade 1-5 required'},409
   x={'id':'IPDTOX-'+uuid.uuid4().hex[:7].upper(),'term':term,'grade':grade,'onset_date':d.get('onset_date') or str(date.today()),'attribution':d.get('attribution','Possibly related'),'outcome':d.get('outcome','Ongoing'),'intervention':d.get('intervention',''),'recorded_by':actor(role),'recorded_at':now(),'care_setting':'IPD'}
   rows=list(ipd['data'].get('toxicity_events',[]));rows.append(x);update_rec(c,ipd['id'],{'toxicity_events':rows},'Active',role,'IPD_TOXICITY',term)
   if tox:
    tx=list(tox['data'].get('events',[]));tx.append({**x,'id':'TOX-'+uuid.uuid4().hex[:7].upper()});update_rec(c,tox['id'],{'events':tx},'Active',role,'TOXICITY_RECORD','IPD '+term)
   return {'ok':True,'toxicity':x},200
  if a=='inpatient_specialty_review':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology','Inpatient Oncology Clinician']:return {'error':'Oncology specialist required'},403
   e=must('inpatient_care');adm=latest(c,pid,'admission');active=next((x for x in reversed(adm['data'].get('admissions',[])) if x.get('status')=='Active'),None) if adm else None
   if not active:return {'error':'Active admission required'},409
   if not str(d.get('assessment') or '').strip():return {'error':'Specialty assessment required'},409
   xs=list(e['data'].get('specialty_reviews',[]));x={'id':'IPDREV-'+uuid.uuid4().hex[:7].upper(),'admission_id':active['id'],'specialty':role,'assessment':d['assessment'],'plan':d.get('plan',''),'at':now(),'reviewed_by':actor(role)};xs.append(x);update_rec(c,e['id'],{'specialty_reviews':xs},'Active',role,'IPD_SPECIALTY_REVIEW',role);return {'ok':True,'review':x},200
  if a=='discharge_patient':
   if role not in WRITE['discharge']:return {'error':'Oncology/inpatient clinical role required'},403
   adm=latest(c,pid,'admission');disc=must('discharge');rows=list(adm['data'].get('admissions',[])) if adm else [];x=next((x for x in rows if x.get('id')==d.get('admission_id') and x.get('status')=='Active'),None)
   if not x:return {'error':'Active admission required'},409
   unresolved=has_unresolved_inpatient_orders(c,pid,x['id'])
   if unresolved:return {'error':'Discharge blocked while inpatient systemic treatment orders remain unresolved','unresolved_orders':unresolved},409
   for k in ['discharge_diagnosis','hospital_course','medications','follow_up','next_care_stage']:
    if d.get(k) in ['',None,[]]:return {'error':f'{k} required'},409
   x.update({'status':'Discharged','discharged_at':d.get('discharged_at') or now(),'discharged_by':actor(role),'discharge_reason':d.get('discharge_reason','Clinical discharge')});update_rec(c,adm['id'],{'admissions':rows},'Active',role,'IPD_DISCHARGE',x['id'])
   sm={'id':'DS-'+uuid.uuid4().hex[:8].upper(),'admission_id':x['id'],'episode_id':x['episode_id'],'discharge_diagnosis':d['discharge_diagnosis'],'hospital_course':d['hospital_course'],'medications':d['medications'],'follow_up':d['follow_up'],'treatment_delay_reason':d.get('treatment_delay_reason',''),'next_cycle':d.get('next_cycle',''),'next_care_stage':d['next_care_stage'],'created_at':now(),'signed_by':actor(role)};ss=list(disc['data'].get('summaries',[]));ss.append(sm);update_rec(c,disc['id'],{'summaries':ss},'Active',role,'DISCHARGE_SUMMARY',x['id'])
   if d.get('next_cycle'):
    ap=latest(c,pid,'appointments')
    if ap:
     aps=list(ap['data'].get('items',[]));aps.append({'id':'APT-'+uuid.uuid4().hex[:7].upper(),'date':d['next_cycle'],'department':'Medical Oncology','clinician':'Treating Oncology Team','location':'OPD / Day Care','purpose':'Post-IPD treatment review / next cycle','status':'Scheduled','source_discharge_id':sm['id'],'created_at':now(),'created_by':actor(role)});update_rec(c,ap['id'],{'items':aps},'Active',role,'DISCHARGE_FOLLOWUP_SCHEDULE',d['next_cycle'])
   journey_add(c,pid,d['next_care_stage'],'Post-discharge continuity','Active',role,'discharge',sm['id'],'Discharged from '+x.get('ward','IPD'),True);return {'ok':True,'summary':sm},200
  if a=='create_continuous_therapy':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   e=must('continuous_therapy');therapy=str(d.get('therapy') or '').strip();mode=d.get('mode') or ('Hormonal therapy' if 'hormon' in therapy.lower() else 'Other continuous systemic therapy')
   if not therapy or not d.get('start_date'):return {'error':'Therapy and start date required'},409
   if mode not in VALUE_SETS['continuous_mode']:return {'error':'Governed continuous-therapy mode required','allowed':VALUE_SETS['continuous_mode']},409
   ep=get_rec(c,d.get('episode_id')) if d.get('episode_id') else (current_episode(c,pid) or ensure_episode(c,pid,role));
   if not ep or ep.get('entity_type')!='cancer_episode':return {'error':'Valid cancer episode required'},409
   x={'id':'CONT-'+uuid.uuid4().hex[:8].upper(),'episode_id':ep['id'],'therapy':therapy,'mode':mode,'drug':d.get('drug',''),'dose':d.get('dose',''),'dose_unit':d.get('dose_unit',''),'frequency':d.get('frequency',''),'route':d.get('route','PO' if mode=='Oral systemic therapy' else ''),'schedule':d.get('schedule','Continuous / protocol-defined'),'food_instructions':d.get('food_instructions',''),'start_date':d['start_date'],'end_date':d.get('end_date'),'dispense_quantity':d.get('dispense_quantity',''),'refill_interval_days':d.get('refill_interval_days'),'monitoring_plan':d.get('monitoring_plan',''),'required_labs':d.get('required_labs',[]),'patient_education':d.get('patient_education',''),'missed_dose_instructions':d.get('missed_dose_instructions',''),'adherence_plan':d.get('adherence_plan',''),'next_review':d.get('next_review',''),'intent':d.get('intent',''),'status':'Active','status_reason':'','state_history':[{'status':'Active','at':now(),'by':actor(role),'reason':'Therapy authorized'}],'authorized_by':actor(role),'authorized_at':now(),'administration_setting':'Outpatient / self-administered','day_care_required':False,'compounding_required':False};rows=list(e['data'].get('courses',[]));rows.append(x);update_rec(c,e['id'],{'courses':rows},'Active',role,'CONTINUOUS_THERAPY_CREATE',therapy);journey_add(c,pid,'Medical Oncology','Continuous Systemic Therapy','Active',role,'continuous_therapy',x['id'],therapy,True);return {'ok':True,'course':x},200
  if a=='create_oral_therapy':
   d={**d,'therapy':d.get('therapy') or d.get('drug'),'mode':'Oral systemic therapy','route':'PO'};a='create_continuous_therapy'
   # fall through to the shared branch by executing its logic inline
   e=must('continuous_therapy');therapy=str(d.get('therapy') or '').strip()
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   if not therapy or not d.get('start_date'):d['start_date']=str(date.today())
   ep=get_rec(c,d.get('episode_id')) if d.get('episode_id') else (current_episode(c,pid) or ensure_episode(c,pid,role));
   if not ep or ep.get('entity_type')!='cancer_episode':return {'error':'Valid cancer episode required'},409
   x={'id':'CONT-'+uuid.uuid4().hex[:8].upper(),'episode_id':ep['id'],'therapy':therapy,'mode':'Oral systemic therapy','drug':d.get('drug',therapy),'dose':d.get('dose',''),'dose_unit':d.get('dose_unit',''),'frequency':d.get('frequency',''),'route':'PO','schedule':d.get('schedule','Protocol-defined oral schedule'),'food_instructions':d.get('food_instructions',''),'start_date':d['start_date'],'end_date':d.get('end_date'),'dispense_quantity':d.get('dispense_quantity',''),'refill_interval_days':d.get('refill_interval_days'),'monitoring_plan':d.get('monitoring_plan',''),'required_labs':d.get('required_labs',[]),'patient_education':d.get('patient_education',''),'missed_dose_instructions':d.get('missed_dose_instructions',''),'adherence_plan':d.get('adherence_plan',''),'next_review':d.get('next_review',''),'intent':d.get('intent',''),'status':'Active','status_reason':'','state_history':[{'status':'Active','at':now(),'by':actor(role),'reason':'Oral therapy authorized'}],'authorized_by':actor(role),'authorized_at':now(),'administration_setting':'Outpatient / self-administered','day_care_required':False,'compounding_required':False};rows=list(e['data'].get('courses',[]));rows.append(x);update_rec(c,e['id'],{'courses':rows},'Active',role,'ORAL_THERAPY_CREATE',therapy);journey_add(c,pid,'Medical Oncology','Oral Systemic Therapy','Active',role,'continuous_therapy',x['id'],therapy,True);return {'ok':True,'course':x},200
  if a=='update_continuous_therapy':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   e=must('continuous_therapy');rows=list(e['data'].get('courses',[]));cid=str(d.get('course_id') or '');course=next((x for x in rows if x.get('id')==cid),None)
   if not course:return {'error':'Continuous/oral therapy course not found'},404
   old_status=course.get('status','Active');new_status=d.get('status') or old_status
   allowed={'Active':{'Active','Held','Dose Modified','Completed','Discontinued'},'Held':{'Held','Restarted','Dose Modified','Discontinued'},'Restarted':{'Restarted','Held','Dose Modified','Completed','Discontinued'},'Dose Modified':{'Dose Modified','Held','Restarted','Completed','Discontinued'},'Completed':{'Completed'},'Discontinued':{'Discontinued'}}
   if new_status not in allowed.get(old_status,{old_status}):return {'error':'Illegal continuous-therapy state transition','from':old_status,'to':new_status,'allowed':sorted(allowed.get(old_status,{old_status}))},409
   reason=str(d.get('reason') or '').strip()
   if new_status!=old_status and new_status in ['Held','Restarted','Dose Modified','Discontinued'] and not reason:return {'error':'Reason is required for this therapy state change'},409
   for k in ['dose','dose_unit','frequency','schedule','food_instructions','dispense_quantity','refill_interval_days','monitoring_plan','required_labs','patient_education','missed_dose_instructions','adherence_plan','adherence_status','toxicity_review','next_review']:
    if k in d:course[k]=d[k]
   course['status']=new_status;course['status_reason']=reason or course.get('status_reason','');hist=list(course.get('state_history',[]));hist.append({'status':new_status,'at':now(),'by':actor(role),'reason':reason});course['state_history']=hist;course['updated_at']=now();course['updated_by']=actor(role)
   update_rec(c,e['id'],{'courses':rows},'Active',role,'CONTINUOUS_THERAPY_UPDATE',f'{cid}: {old_status} -> {new_status}');journey_add(c,pid,'Medical Oncology','Continuous Systemic Therapy',new_status,role,'continuous_therapy',cid,reason,True);return {'ok':True,'course':course},200
  if a=='record_tumor_marker':
   if role not in WRITE['tumor_marker']:return {'error':'Medical Oncology/Laboratory role required'},403
   e=must('tumor_marker');vals={k:v for k,v in d.items() if k not in ['date','context','episode_id']};
   if not vals:return {'error':'At least one tumor marker result is required'},409
   ep=d.get('episode_id') or ((current_episode(c,pid) or {}).get('id'));x={'id':'MARK-'+uuid.uuid4().hex[:8].upper(),'episode_id':ep,'date':d.get('date') or str(date.today()),'context':d.get('context','Response monitoring'),'values':vals,'recorded_by':actor(role),'recorded_at':now()};rows=list(e['data'].get('measurements',[]));rows.append(x);update_rec(c,e['id'],{'measurements':rows},'Active',role,'TUMOR_MARKER',x['date']);return {'ok':True,'measurement':x},200
  if a=='discontinue_treatment':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Oncology clinician required'},403
   reason=str(d.get('reason') or '').strip()
   if not reason:return {'error':'Discontinuation reason required'},409
   plan=e if e and e['entity_type']=='treatment_plan' else latest(c,pid,'treatment_plan')
   if plan:update_rec(c,plan['id'],{'discontinuation_reason':reason,'discontinued_at':now(),'discontinued_by':actor(role)},'Discontinued',role,'PLAN_DISCONTINUE',reason)
   close_future_work(c,pid,role,reason);journey_add(c,pid,role,'Treatment Discontinued','Discontinued',role,'treatment_plan',plan['id'] if plan else '',reason,True);return {'ok':True},200
  if a=='record_death':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Oncology clinician required'},403
   reason=str(d.get('reason') or 'Death during active care');dt=d.get('date') or str(date.today());c.execute('UPDATE patients SET status=?,updated_at=? WHERE id=?',('Deceased',now(),pid));close_future_work(c,pid,role,reason)
   ep=current_episode(c,pid)
   if ep:update_rec(c,ep['id'],{'ended_at':dt,'closure_reason':reason,'status':'Closed'},'Closed',role,'EPISODE_CLOSE',reason)
   adm=latest(c,pid,'admission')
   if adm:
    rows=list(adm['data'].get('admissions',[]))
    for x in rows:
     if x.get('status')=='Active':x.update({'status':'Deceased','discharged_at':now(),'discharge_reason':reason})
    update_rec(c,adm['id'],{'admissions':rows},'Active',role,'IPD_DEATH_CLOSE',reason)
   journey_add(c,pid,'Episode Closure','Death during treatment','Closed',role,'cancer_episode',ep['id'] if ep else '',reason,True);return {'ok':True,'patient_status':'Deceased'},200
  if a=='evaluate_conditional_phase':
   if role not in ['Surgical Oncology','Medical Oncology','Radiation Oncology']:return {'error':'Oncology clinician required'},403
   condition=str(d.get('condition') or '').lower();activate=d.get('activate') or 'Radiation';path=latest(c,pid,'pathology');margin=str((path['data'].get('margin_status') if path else '') or '').lower();matched=('positive margin' in condition and 'positive' in margin) or bool(d.get('condition_met'))
   plan=latest(c,pid,'treatment_plan')
   if not plan:return {'error':'Treatment plan required'},409
   if not matched:return {'ok':True,'condition_met':False,'action':'No phase activated'},200
   phases=list(plan['data'].get('phases',[]));found=False
   for x in phases:
    if str(x.get('modality','')).lower().startswith(str(activate).lower()):x.update({'status':'Draft — specialist review required','activation_reason':d.get('condition'),'activated_at':now(),'activated_by':actor(role)});found=True
   if not found:phases.append({'modality':activate,'status':'Draft — specialist review required','responsible':activate+' Oncology' if activate in ['Radiation','Surgical'] else 'Medical Oncology','activation_reason':d.get('condition'),'activated_at':now(),'activated_by':actor(role)})
   rid=new_record(c,pid,'treatment_plan',{**plan['data'],'phases':phases,'supersedes':plan['id'],'amendment_reason':'Conditional phase activated: '+str(d.get('condition')),'version':int(plan['data'].get('version',1))+1},'Draft',role);journey_add(c,pid,role,'Conditional Treatment Phase Added','Draft',role,'treatment_plan',rid,d.get('condition',''),True);return {'ok':True,'condition_met':True,'plan_id':rid,'status':'Draft'},200
  if a=='save_registration':
   if not need(['Front Desk','Patient Attender']):return {'error':'Not authorized'},403
   e=must('registration'); required=['name','dob','phone','id_number','assigned_specialty']; miss=[x for x in required if not str(d.get(x,'')).strip()]
   if miss:return {'error':'Mandatory registration fields missing','missing':miss},409
   ok_dob,msg=valid_dob(d['dob'])
   if not ok_dob:return {'error':msg},409
   c.execute('UPDATE patients SET name=?,dob=?,sex=?,phone=?,abha=?,id_number=?,current_department=?,updated_at=? WHERE id=?',(d['name'],d['dob'],d.get('sex',''),d['phone'],d.get('abha',''),d['id_number'],d.get('assigned_specialty','Front Desk'),now(),pid));patch={k:v for k,v in d.items() if k not in ['name','dob','sex','phone','abha','id_number','general_consent','photo_status']};update_rec(c,e['id'],patch,'Completed' if d.get('complete') else e['status'],role,'REGISTRATION_SAVE');return {'ok':True},200
  if a=='consent_action':
   if not need(['Front Desk','Patient Attender','Patient Liaison']):return {'error':'Not authorized'},403
   e=must('consent');items=list(e['data'].get('items',[]));op=d.get('operation')
   if op=='sign':
    for k in ['type','version','scope','signed_by','valid_from']:
     if not str(d.get(k,'')).strip():return {'error':f'{k} required'},409
    x={'id':'CONS-'+uuid.uuid4().hex[:8].upper(),'type':d['type'],'version':d['version'],'scope':d['scope'],'status':'Signed','signed_by':d['signed_by'],'signed_at':now(),'valid_from':d['valid_from'],'valid_until':d.get('valid_until',''),'document_id':d.get('document_id','')};items.append(x)
   elif op=='withdraw':
    x=next((x for x in items if x['id']==d.get('id')),None)
    if not x:return {'error':'Consent not found'},404
    if not str(d.get('reason','')).strip():return {'error':'Withdrawal reason required'},409
    x['status']='Withdrawn';x['withdrawn_at']=now();x['withdrawn_by']=actor(role);x['withdraw_reason']=d['reason']
   else:return {'error':'Invalid consent operation'},409
   update_rec(c,e['id'],{'items':items},'Active',role,'CONSENT_ACTION',op);reg=latest(c,pid,'registration');active=any(x.get('type')=='General Consent' and x.get('status')=='Signed' for x in items);update_rec(c,reg['id'],{'general_consent':'Signed' if active else 'Pending'},role=role,action='CONSENT_SYNC');return {'ok':True,'items':items},200
  if a=='save_appointment':
   if not need(['Front Desk','Patient Attender','PRE / Patient Relations Executive','Radiology Coordinator','Finance / Billing']):return {'error':'Not authorized'},403
   e=must('appointments');items=list(e['data'].get('items',[]));op=d.get('operation')
   if op=='create':
    for k in ['date','department','location']:
     if not d.get(k):return {'error':f'{k} required'},409
    if not future_or_today(d['date']):return {'error':'New appointments cannot be scheduled in the past'},409
    if d['location'] not in LOCATION_MASTER and d['location'] not in ['OPD','OPD / Day Care']:return {'error':'Appointment location must use a governed location','allowed':LOCATION_MASTER},409
    items.append({'id':'APT-'+uuid.uuid4().hex[:7].upper(),'date':d['date'],'department':d['department'],'clinician':d.get('clinician',''),'location':d['location'],'purpose':d.get('purpose',''),'status':'Scheduled','created_by':actor(role),'created_at':now()})
   else:
    x=next((x for x in items if x['id']==d.get('id')),None)
    if not x:return {'error':'Appointment not found'},404
    if op=='reschedule':
     nd=d.get('date',x['date'])
     if not future_or_today(nd):return {'error':'Rescheduled appointment cannot be in the past'},409
     x.update({'date':nd,'status':'Rescheduled','reason':d.get('reason',''),'updated_at':now()})
    elif op=='cancel':x.update({'status':'Cancelled','reason':d.get('reason',''),'updated_at':now()})
    elif op=='no_show':
     x.update({'status':'No-show','reason':d.get('reason','Patient did not attend'),'updated_at':now(),'recorded_by':actor(role)});create_task(c,pid,'Patient Liaison','Follow up after missed appointment','No-show follow-up','High','appointments',x['id'],str(date.today()+timedelta(days=1)),reason=x['reason'],created_by=role)
    elif op=='complete':x.update({'status':'Completed','updated_at':now(),'completed_by':actor(role)})
    else:return {'error':'Invalid appointment operation'},409
   update_rec(c,e['id'],{'items':items},'Active',role,'APPOINTMENT',op);return {'ok':True,'items':items},200
  if a=='queue_patient':
   if role not in WRITE['queue']:return {'error':'Not authorized'},403
   e=must('queue');to=d.get('to')
   if not to:return {'error':'Destination required'},409
   if to not in LOCATION_MASTER:return {'error':'Destination must be selected from the governed location master','allowed':LOCATION_MASTER},409
   targets=LOCATION_ROLE_MAP.get(to,[]);targets=[targets] if isinstance(targets,str) else targets
   for rr in targets:grant_patient_access(c,pid,rr,'queue',e['id'],role)
   hist=list(e['data'].get('history',[]));hist.append({'at':now(),'from':e['data'].get('current_location',''),'to':to,'status':d.get('status','Queued'),'actor':actor(role)['name'],'role':role});update_rec(c,e['id'],{'current_location':to,'current_status':d.get('status','Queued'),'priority':d.get('priority',e['data'].get('priority','Routine')),'history':hist},'Active',role,'QUEUE_TRANSFER',to);journey_add(c,pid,to,d.get('care_stage') or to,d.get('status','Queued'),role,'queue',e['id'],d.get('reason',''));return {'ok':True,'to':to},200
  if a=='save_intake':
   if role not in ['Nurse Navigator','Intake Nurse']:return {'error':'Nurse Navigator or Intake Nurse required'},403
   e=must('intake')
   # PC1.3: every measured intake element carries an explicit source unit/instrument.
   required=['sbp','dbp','hr','rr','temp','spo2','weight','height','ecog','kps'];miss=[x for x in required if d.get(x) in ['',None]]
   units=d.get('units') or {};unit_required=['bp','hr','rr','temp','spo2','weight','height'];umiss=[x for x in unit_required if not str(units.get(x,'')).strip()]
   if miss or umiss:return {'error':'Mandatory intake fields/explicit units missing','missing':miss,'missing_units':umiss},409
   if str(d.get('ecog')) not in VALUE_SETS['ecog']:return {'error':'ECOG must be 0–4','allowed':VALUE_SETS['ecog']},409
   if str(d.get('kps')) not in VALUE_SETS['kps']:return {'error':'Karnofsky score must use the governed 0–100 scale in 10-point increments','allowed':VALUE_SETS['kps']},409
   allowed_units={'bp':['mmHg'],'hr':['/min'],'rr':['/min'],'temp':['°C','°F','Cel','[degF]'],'spo2':['%'],'weight':['kg','lb'],'height':['cm','in']}
   for k,allowed in allowed_units.items():
    if units.get(k) not in allowed:return {'error':f'Unsupported unit for {k}','field':k,'unit':units.get(k),'allowed':allowed},409
   def nv(k):
    v=safe_float(d.get(k));
    if v is None:raise ValueError(k)
    return v
   try:sbp,dbp,hr,rr,temp,spo2,weight,height=[nv(k) for k in ['sbp','dbp','hr','rr','temp','spo2','weight','height']]
   except ValueError as ex:return {'error':f'{ex.args[0]} must be numeric'},409
   # Normalise source units; retain the source measurement + unit for auditability.
   temp_c=(temp-32)*5/9 if units['temp'] in ['°F','[degF]'] else temp
   weight_kg=weight*0.45359237 if units['weight']=='lb' else weight
   height_cm=height*2.54 if units['height']=='in' else height
   if not (50<=sbp<=260 and 30<=dbp<=180 and sbp>dbp):return {'error':'Blood pressure is outside the configured product-test plausibility range'},409
   limits={'hr':(20,250,hr),'rr':(4,80,rr),'temp_c':(25,45,temp_c),'spo2':(50,100,spo2),'weight_kg':(1,350,weight_kg),'height_cm':(30,250,height_cm)}
   for k,(lo,hi,v) in limits.items():
    if v<lo or v>hi:return {'error':f'{k} is outside the configured plausibility range','field':k,'range':[lo,hi],'value':v},409
   pain_instrument=d.get('pain_instrument') or ''
   if d.get('pain_score') not in ['',None]:
    if pain_instrument not in ['Numeric Rating Scale 0–10','Visual Analogue Scale 0–10','Faces scale']:return {'error':'Pain score requires an explicit approved pain instrument'},409
    pv=safe_float(d.get('pain_score'))
    if pv is None or pv<0 or pv>10:return {'error':'Pain score must be 0–10 for the configured demo instruments'},409
   fall_scale=str(d.get('fall_risk_scale') or '').strip();fall_score=safe_float(d.get('fall_risk_score'))
   if fall_scale not in FALL_RISK_SCALES:return {'error':'Fall-risk score requires an explicit governed scale','allowed':list(FALL_RISK_SCALES)},409
   fcfg=FALL_RISK_SCALES[fall_scale]
   if fall_score is None or fall_score<fcfg['min'] or fall_score>fcfg['max']:return {'error':'Fall-risk score is outside the configured scale range','scale':fall_scale,'range':[fcfg['min'],fcfg['max']]},409
   fall_level=next((b['level'] for b in fcfg['bands'] if fall_score<=b['max']),fcfg['bands'][-1]['level'])
   bmi=round(weight_kg/((height_cm/100)**2),2);bv=bsa_values(height_cm,weight_kg);bsa=bv['ordering'];measured_at=now()
   patch={**d};
   for k in ['sbp','dbp','temp','weight','height']:patch.pop(k,None)
   patch.pop('fall_risk_level',None)
   patch.update({'bp':f'{int(round(sbp))}/{int(round(dbp))}','hr':hr,'rr':rr,'temp_c':round(temp_c,3),'spo2':spo2,'weight_kg':round(weight_kg,4),'height_cm':round(height_cm,3),'bmi':bmi,'bsa_raw_m2':bv['raw'],'bsa_m2':bsa,'bsa_display_m2':bv['display'],'bsa_formula':'Mosteller: '+bv['formula_text'],'bsa_rounding_policy':BSA_POLICY,'measurement_units':{'bp':'mmHg','hr':'/min','rr':'/min','temp_c':'°C','spo2':'%','weight_kg':'kg','height_cm':'cm'},'source_measurements':{'sbp':{'value':sbp,'unit':units['bp']},'dbp':{'value':dbp,'unit':units['bp']},'hr':{'value':hr,'unit':units['hr']},'rr':{'value':rr,'unit':units['rr']},'temp':{'value':temp,'unit':units['temp']},'spo2':{'value':spo2,'unit':units['spo2']},'weight':{'value':weight,'unit':units['weight']},'height':{'value':height,'unit':units['height']}},'measured_at':measured_at,'assessor':actor(role),'fall_risk_scale':fall_scale,'fall_risk_score':fall_score,'fall_risk_level':fall_level,'fall_risk_scale_status':fcfg['clinical_content_status']})
   update_rec(c,e['id'],patch,'Completed' if d.get('complete') else 'Draft',role,'INTAKE_SAVE');journey_add(c,pid,'Nurse Intake','Intake Completed','Completed',role,'intake',e['id']) if d.get('complete') else None;return {'ok':True,'bmi':bmi,'bsa_raw_m2':bv['raw'],'bsa_m2':bsa,'bsa_rounding_policy':BSA_POLICY,'bsa_formula':patch['bsa_formula'],'canonical_units':patch['measurement_units'],'source_measurements':patch['source_measurements']},200
  if a=='med_recon':
   if not need(['Nurse Navigator','Intake Nurse','Medical Oncology']):return {'error':'Not authorized'},403
   e=must('med_recon');op=d.get('operation');data=e['data'];items=list(data.get('items',[]));als=list(data.get('allergies',[]));events=list(data.get('reconciliation_events',[]));allergy_status=data.get('allergy_status') or ('Allergy present' if als else 'Unable to verify')
   if op=='add_medication':
    fid=str(d.get('formulary_id') or '').strip();fi=formulary_one(c,fid) if fid else None
    if not fi or fi.get('status')!='Active':return {'error':'Current medication must be selected from the Active institution formulary','requires':'formulary_id'},409
    route=str(d.get('route') or '').strip();src=d.get('source');freq=d.get('frequency');mstatus=d.get('status');dose_unit=d.get('dose_unit');dose_value=safe_float(d.get('dose_value'))
    if route not in fi.get('allowed_routes',[]):return {'error':'Medication route must be one of the governed routes for the selected formulary item','allowed':fi.get('allowed_routes',[])},409
    if src not in VALUE_SETS['allergy_source']:return {'error':'Medication source must use the governed provenance value set','allowed':VALUE_SETS['allergy_source']},409
    if freq not in VALUE_SETS['medication_frequency']:return {'error':'Medication frequency must use the governed value set','allowed':VALUE_SETS['medication_frequency']},409
    if mstatus not in VALUE_SETS['medication_status']:return {'error':'Medication status must use the governed value set','allowed':VALUE_SETS['medication_status']},409
    if dose_value is None or dose_value<0 or dose_unit not in VALUE_SETS['medication_dose_unit']:return {'error':'Medication dose requires a numeric value and governed explicit dose unit','allowed_units':VALUE_SETS['medication_dose_unit']},409
    schedule_detail=str(d.get('schedule_detail') or '').strip()
    if freq=='Other prescribed schedule' and not schedule_detail:return {'error':'Other prescribed schedule requires structured schedule detail'},409
    items.append({'id':'MED-'+uuid.uuid4().hex[:6].upper(),'formulary_id':fi['id'],'name':fi.get('display_name') or fi.get('drug'),'drug':fi.get('drug'),'code':fi.get('code'),'code_system':fi.get('code_system'),'dose_value':dose_value,'dose_unit':dose_unit,'dose':f'{dose_value:g} {dose_unit}','route':route,'frequency':freq,'schedule_detail':schedule_detail,'status':mstatus,'source':src,'clinical_content_status':'Institution formulary reference — current demo content may be Synthetic QA','entered_by':actor(role),'entered_at':now()})
   elif op=='set_allergy_status':
    allergy_status=d.get('allergy_status')
    if allergy_status not in VALUE_SETS['allergy_status']:return {'error':'Allergy status must use the governed value set','allowed':VALUE_SETS['allergy_status']},409
    if allergy_status=='No known allergy' and any(str(x.get('status','Active')).lower()=='active' for x in als):return {'error':'Cannot record No known allergy while active allergy records exist'},409
   elif op=='add_allergy':
    code=str(d.get('code') or '').strip();master=ALLERGEN_BY_CODE.get(code)
    if not master:return {'error':'Allergen must be selected from the governed allergen master','allowed':ALLERGEN_MASTER},409
    reaction=d.get('reaction');src=d.get('source');sev=d.get('severity') or 'Unknown'
    if reaction not in VALUE_SETS['allergy_reaction']:return {'error':'Allergy reaction must use the governed value set','allowed':VALUE_SETS['allergy_reaction']},409
    if sev not in VALUE_SETS['allergy_severity']:return {'error':'Allergy severity must use the governed value set','allowed':VALUE_SETS['allergy_severity']},409
    if src not in VALUE_SETS['allergy_source']:return {'error':'Allergy source must use the governed provenance value set','allowed':VALUE_SETS['allergy_source']},409
    detail=str(d.get('reaction_detail') or '').strip()
    if reaction=='Other' and not detail:return {'error':'Other allergy reaction requires detail'},409
    als.append({'id':'ALG-'+uuid.uuid4().hex[:6].upper(),'substance':master['label'],'code':master['code'],'code_system':master['code_system'],'reaction':reaction,'reaction_detail':detail,'severity':sev,'onset_date':d.get('onset_date',''),'status':d.get('status') or 'Active','source':src,'entered_by':actor(role),'entered_at':now(),'clinical_content_status':'Synthetic QA allergen/reaction masters — CCA configuration required'})
    allergy_status='Allergy present'
   elif op=='reconcile':
    rs=d.get('reconciliation_status');src=d.get('source')
    if rs not in VALUE_SETS['med_reconciliation_status']:return {'error':'Medication reconciliation status must be explicitly attested','allowed':VALUE_SETS['med_reconciliation_status']},409
    if src not in VALUE_SETS['allergy_source']:return {'error':'Medication reconciliation source must use the governed provenance value set','allowed':VALUE_SETS['allergy_source']},409
    reason=str(d.get('reason') or d.get('note') or '').strip()
    if rs in ['Incomplete','Unable to verify'] and not reason:return {'error':'Incomplete/unverified medication reconciliation requires reason'},409
    if allergy_status not in VALUE_SETS['allergy_status']:return {'error':'Explicit allergy status required before medication reconciliation','allowed':VALUE_SETS['allergy_status']},409
    events.append({'at':now(),'reconciled_by':actor(role),'medication_count':len(items),'allergy_count':len(als),'allergy_status':allergy_status,'reconciliation_status':rs,'source':src,'reason':reason,'attestation':'Medication and allergy reconciliation reviewed to the stated status.'})
   else:return {'error':'Invalid operation'},409
   update_rec(c,e['id'],{'items':items,'allergies':als,'allergy_status':allergy_status,'reconciliation_events':events},'Active',role,'MED_RECON',op);return {'ok':True,'allergy_status':allergy_status,'reconciliation_status':events[-1].get('reconciliation_status') if events else None},200
  if a=='save_dynamic_form':
   e=must('dynamic_forms');op=d.get('operation');data=e['data'];defs=list(data.get('definitions',[]));res=dict(data.get('responses',{}))
   if op=='definition':
    if role!='Hospital Management / Admin':return {'error':'Admin required'},403
    q=d.get('definition') or {}; 
    if not q.get('id') or not q.get('name'):return {'error':'Form id/name required'},409
    defs=[x for x in defs if x.get('id')!=q['id']]+[q]
   elif op=='response':
    if role not in ['Nurse Navigator','Medical Oncology']:return {'error':'Clinical role required'},403
    fid=d.get('form_id');fd=next((x for x in defs if x.get('id')==fid),None)
    if not fd:return {'error':'Form not found'},404
    vals=d.get('values') or {};visible=[]
    for f in fd.get('fields',[]):
     sh=f.get('show_if');vis=not sh or vals.get(sh.get('field'))==sh.get('equals')
     if vis:visible.append(f)
    miss=[f['id'] for f in visible if f.get('required') and vals.get(f['id']) in ['',None,False]]
    if miss:return {'error':'Required dynamic-form fields missing','missing':miss},409
    res[fid]={'values':vals,'form_version':fd.get('version',1),'submitted_at':now(),'submitted_by':actor(role)}
   else:return {'error':'Invalid operation'},409
   update_rec(c,e['id'],{'definitions':defs,'responses':res},'Active',role,'DYNAMIC_FORM',op);return {'ok':True},200
  if a=='save_consultation':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   e=must('consultation');sign=bool(d.get('sign'));req=['encounter_type','date','chief_complaint','hpi','ros','assessment','plan'];miss=[x for x in req if not str(d.get(x,'')).strip()]
   pe=d.get('physical_exam_structured') or {};miss+=['physical_exam.'+x for x in ['general','cardiovascular','respiratory','abdomen','neurologic','tumor_site'] if not str(pe.get(x,'')).strip()]
   if sign and miss:return {'error':'Encounter incomplete','missing':miss},409
   if e['status']=='Signed':return {'error':'Signed encounter is immutable; create an addendum/new encounter'},409
   patch={**d};patch.pop('sign',None)
   if sign:patch.update({'signed_by':actor(role),'signed_at':now()})
   update_rec(c,e['id'],patch,'Signed' if sign else 'Draft',role,'CONSULTATION_SIGN' if sign else 'CONSULTATION_SAVE');return {'ok':True,'status':'Signed' if sign else 'Draft'},200
  if a=='save_diagnosis':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Oncology clinician required'},403
   e=must('diagnosis');verify=bool(d.get('verify'));non_tnm=is_non_tnm_case(d);base_req=['icd10','icd10_version','cancer_type','primary_site','histology','staging_system','staging_version','staging_date','staging_basis','treatment_intent'];req=base_req + (['classification_value'] if non_tnm else ['icdo_topography','icdo_morphology','icdo_version','stage_t','stage_n','stage_m','stage_group']);miss=[x for x in req if not str(d.get(x,'')).strip()];ep=current_episode(c,pid) or ensure_episode(c,pid,role);d={**d,'episode_id':d.get('episode_id') or ep['id'],'non_tnm':non_tnm,'classification_system':d.get('classification_system') or (d.get('staging_system') if non_tnm else '')}
   sd=parse_iso_date(d.get('staging_date'))
   if d.get('staging_date') and (not sd or sd>date.today()):return {'error':'Staging/classification date cannot be in the future'},409
   if verify and miss:return {'error':'Diagnosis/staging incomplete','missing':miss,'non_tnm':non_tnm},409
   if e['status']=='Verified':
    rid=new_record(c,pid,'diagnosis',{**e['data'],**{k:v for k,v in d.items() if k!='verify'},'supersedes':e['id'],'verification_reason':d.get('reason','Updated clinical staging')},'Verified' if verify else 'Draft',role);return {'ok':True,'id':rid,'status':'Verified' if verify else 'Draft'},200
   update_rec(c,e['id'],{k:v for k,v in d.items() if k!='verify'},'Verified' if verify else 'Draft',role,'DIAGNOSIS_VERIFY' if verify else 'DIAGNOSIS_SAVE');return {'ok':True,'status':'Verified' if verify else 'Draft'},200
  if a=='create_diagnostic_order':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   typ=d.get('type');name=str(d.get('name') or '').strip();catalog_id=str(d.get('catalog_id') or '').strip();ind=str(d.get('indication') or '').strip();priority=d.get('priority','Routine');reason=str(d.get('decision_reason') or d.get('reason') or '').strip();requested=d.get('date',str(date.today()))
   cat=DIAGNOSTIC_CATALOG.get(catalog_id) if catalog_id else next((x for x in DIAGNOSTIC_CATALOG.values() if x['type']==typ and x['name']==name and x.get('active')),None)
   if not cat:return {'error':'Investigation must be selected from the governed diagnostic catalogue','catalog':list(DIAGNOSTIC_CATALOG.values())},409
   typ=cat['type'];name=cat['name']
   if not ind:return {'error':'Clinical indication required'},409
   if priority not in ['Routine','Urgent','Stat']:return {'error':'Governed investigation priority required','allowed':['Routine','Urgent','Stat']},409
   if not reason:return {'error':'Investigation decision reason required'},409
   if not parse_iso_date(requested):return {'error':'Valid requested date required'},409
   base={'catalog_id':catalog_id or next(k for k,v in DIAGNOSTIC_CATALOG.items() if v is cat),'catalog_code':cat['code'],'catalog_code_system':cat['code_system'],'indication':ind,'priority':priority,'requested_date':requested,'decision_reason':reason,'ordered_by':actor(role),'ordered_at':now(),'billing':'Payment Pending','payment_receipt':''}
   if typ=='Laboratory':
    rid=new_record(c,pid,'lab_order',{**base,'order_no':'LAB-'+uuid.uuid4().hex[:6].upper(),'tests':[name],'date':requested,'sample_status':'Not Collected'},'Ordered',role);[grant_patient_access(c,pid,rr,'diagnostic_order',rid,role) for rr in ['Laboratory / Phlebotomy','Biller','Finance / Billing','PRE / Patient Relations Executive']]
   else:
    rid=new_record(c,pid,'radiology_order',{**base,'order_no':'RAD-'+uuid.uuid4().hex[:6].upper(),'study':name,'date':requested,'schedule':'','procedure_status':'Not Started','consent_required':True},'Ordered',role);[grant_patient_access(c,pid,rr,'diagnostic_order',rid,role) for rr in ['Radiology Coordinator','Radiology Technician','Radiologist','Biller','Finance / Billing','PRE / Patient Relations Executive']]
   return {'ok':True,'id':rid,'catalog_id':base['catalog_id']},200
  if a=='record_payment':
   if role not in ['Biller','Finance / Billing']:return {'error':'Billing role required'},403
   if not e or e['entity_type'] not in ['lab_order','radiology_order']:return {'error':'Diagnostic order required'},404
   st=d.get('payment_status');receipt=str(d.get('receipt_no','')).strip();
   if st not in ['Paid','Waived']:return {'error':'Paid or Waived required'},409
   if st=='Paid' and not receipt:return {'error':'Receipt number required'},409
   amount=safe_float(d.get('amount',0))
   if amount is None or amount<0:return {'error':'Payment amount must be a non-negative number'},409
   if st=='Paid':
    for typ in ['lab_order','radiology_order']:
     for z in many(c,pid,typ):
      if z['id']!=e['id'] and z['data'].get('payment_receipt')==receipt:return {'error':'Receipt number is already linked to another order','receipt_no':receipt,'order_id':z['id']},409
    if e['data'].get('billing')=='Paid' and e['data'].get('payment_receipt')==receipt:
     if float(e['data'].get('payment_amount') or 0)==amount:return {'ok':True,'idempotent':True,'message':'Duplicate payment replay suppressed'},200
     return {'error':'Receipt replay conflicts with the previously recorded amount','previous_amount':e['data'].get('payment_amount'),'submitted_amount':amount},409
   update_rec(c,e['id'],{'billing':st,'payment_receipt':receipt,'payment_amount':amount,'payment_reason':d.get('reason',''),'payment_at':now(),'payment_by':actor(role)},role=role,action='PAYMENT');return {'ok':True,'idempotent':False},200
  if a=='collect_sample':
   if role!='Laboratory / Phlebotomy':return {'error':'Lab role required'},403
   if not e or e['entity_type']!='lab_order':return {'error':'Lab order required'},404
   if e['data'].get('billing') not in ['Paid','Waived']:return {'error':'Payment/waiver required before collection'},409
   sid=d.get('sample_id') or 'SMP-'+uuid.uuid4().hex[:7].upper();update_rec(c,e['id'],{'sample_status':'Collected','sample_id':sid,'collected_at':d.get('collected_at') or now(),'collected_by':actor(role)},'Sample Collected',role,'SAMPLE_COLLECT');labid=new_record(c,pid,'lab',{'source_order_id':e['id'],'sample_id':sid,'date':str(date.today())},'Draft',role);return {'ok':True,'lab_entity_id':labid,'sample_id':sid},200
  if a=='reject_sample':
   if role!='Laboratory / Phlebotomy':return {'error':'Lab role required'},403
   if not e or e['entity_type']!='lab_order':return {'error':'Lab order required'},404
   reason=str(d.get('reason') or '').strip()
   if not reason:return {'error':'Sample rejection reason required'},409
   if e['data'].get('sample_status')!='Collected':return {'error':'Only a collected sample can be rejected'},409
   update_rec(c,e['id'],{'sample_status':'Rejected','sample_rejection_reason':reason,'sample_rejected_at':now(),'sample_rejected_by':actor(role)},'Sample Rejected',role,'SAMPLE_REJECT',reason);tid=create_task(c,pid,'Laboratory / Phlebotomy','Recollect rejected laboratory specimen','Specimen recollection','High','lab_order',e['id'],str(date.today()+timedelta(days=1)),reason=reason,created_by=role);return {'ok':True,'task_id':tid},200
  if a=='recollect_sample':
   if role!='Laboratory / Phlebotomy':return {'error':'Lab role required'},403
   if not e or e['entity_type']!='lab_order':return {'error':'Lab order required'},404
   if e['data'].get('sample_status')!='Rejected':return {'error':'Rejected sample state required before recollection'},409
   sid=d.get('sample_id') or 'SMP-'+uuid.uuid4().hex[:7].upper();update_rec(c,e['id'],{'sample_status':'Collected','sample_id':sid,'recollected_at':now(),'recollected_by':actor(role),'previous_rejected_sample_id':e['data'].get('sample_id')},'Sample Collected',role,'SAMPLE_RECOLLECT');labid=new_record(c,pid,'lab',{'source_order_id':e['id'],'sample_id':sid,'date':str(date.today()),'recollection':True},'Draft',role);return {'ok':True,'lab_entity_id':labid,'sample_id':sid},200
  if a=='save_lab':
   if role!='Laboratory / Phlebotomy':return {'error':'Lab role required'},403
   if not e or e['entity_type']!='lab':return {'error':'Lab record required'},404
   fin=bool(d.get('finalize')); amendment_reason=str(d.get('amendment_reason') or '').strip()
   patch={k:v for k,v in d.items() if k not in ['finalize','amendment_reason']}
   abnormal=patch.get('abnormal_flags') or {}
   if abnormal:
    bad={k:v for k,v in abnormal.items() if v not in LAB_ABNORMAL_FLAGS}
    if bad:return {'error':'Laboratory abnormal flag must use the governed value set','invalid':bad,'allowed':LAB_ABNORMAL_FLAGS},409
   # Reference ranges are INTEGRATED/read-only from the assay/LIS master; client-supplied ranges are never authoritative.
   patch.pop('reference_ranges',None)
   if fin:
    patch['reference_ranges']={k:dict(v) for k,v in LAB_REFERENCE_RANGE_MASTER.items() if ({**e['data'],**patch}).get(k) not in ['',None]}
    patch['reference_range_source_mode']='INTEGRATED / server-owned assay master'
    patch['reporting_clinician']=actor(role);patch['reporting_source']='Laboratory / LIS boundary';patch['result_status']='Final'
   # A final clinical result is immutable. Any correction starts a new linked record and requires a reason.
   amending=e['status']=='Final'
   if amending and not amendment_reason:
    return {'error':'A finalized laboratory result cannot be overwritten. Start an amendment with a documented reason.','requires_amendment_reason':True,'supersedes':e['id']},409
   # Units are first-class laboratory data. On every final submission they must be supplied explicitly
   # in the same request as the values; never inherit an old unit when a numeric result changes.
   submitted_units=patch.get('units') if isinstance(patch.get('units'),dict) else {}
   merged={**e['data'],**patch}
   units=submitted_units if fin else (submitted_units or (e['data'].get('units') or {}))
   if fin: merged['units']=units
   missing_units,invalid_units=validate_lab_units(merged,units)
   plausibility_errors=validate_lab_plausibility(merged,units)
   if plausibility_errors:return {'error':'One or more laboratory values are outside the configured product-test plausibility range','plausibility_errors':plausibility_errors},409
   if fin:
    req=['date','hb','wbc','anc','platelets','creatinine','egfr','bilirubin','ast','alt'];miss=[x for x in req if merged.get(x) in ['',None]]
    if miss:return {'error':'Core panel incomplete','missing':miss},409
    if missing_units:return {'error':'Unit selection is mandatory for every entered laboratory value','missing_units':missing_units},409
    if invalid_units:return {'error':'One or more laboratory units are outside the governed value set','invalid_units':invalid_units},409
    patch.update({'units':units,'finalized_at':now(),'finalized_by':actor(role)})
    obsdata={**merged,**patch};obsdata['source_order_id']=obsdata.get('source_order_id') or e['data'].get('source_order_id');patch['observations']=lab_observations(obsdata)
   elif invalid_units:return {'error':'One or more laboratory units are outside the governed value set','invalid_units':invalid_units},409
   if amending:
    newdata={**e['data'],**patch,'supersedes':e['id'],'amendment_reason':amendment_reason,'amended_at':now(),'amended_by':actor(role)}
    rid=new_record(c,pid,'lab',newdata,'Final' if fin else 'Draft',role)
    audit(c,pid,role,'LAB_AMENDMENT_CREATED','lab',rid,f'Supersedes {e["id"]}: {amendment_reason}')
    task_ids=[]
    if fin:
     flags=critical_lab_flags(newdata,units)
     if flags:task_ids=[create_task(c,pid,'Medical Oncology','Review critical amended laboratory result','Critical result','Critical','lab',rid,now(),reason='; '.join([f"{x['field']}={x['value']} {x.get('unit') or ''}" for x in flags]),data={'critical_flags':flags},created_by=role)]
    return {'ok':True,'id':rid,'status':'Final' if fin else 'Draft','units':units,'supersedes':e['id'],'amendment_reason':amendment_reason,'critical_tasks':task_ids},200
   update_rec(c,e['id'],patch,'Final' if fin else 'Draft',role,'LAB_FINAL' if fin else 'LAB_SAVE')
   task_ids=[]
   if fin:
    flags=critical_lab_flags({**merged,**patch},units)
    if flags:
     existing=c.execute("SELECT id FROM tasks WHERE source_type='lab' AND source_id=? AND task_type='Critical result' AND status IN ('Open','Acknowledged')",(e['id'],)).fetchone()
     if existing:task_ids=[existing['id']]
     else:task_ids=[create_task(c,pid,'Medical Oncology','Review critical laboratory result','Critical result','Critical','lab',e['id'],now(),reason='; '.join([f"{x['field']}={x['value']} {x.get('unit') or ''}" for x in flags]),data={'critical_flags':flags},created_by=role)]
   return {'ok':True,'id':e['id'],'status':'Final' if fin else 'Draft','units':units,'critical_tasks':task_ids},200
  if a=='schedule_radiology':
   if role not in ['Radiology Coordinator','PRE / Patient Relations Executive']:return {'error':'Coordinator/PRE required'},403
   if not e or e['entity_type']!='radiology_order':return {'error':'Radiology order required'},404
   if e['data'].get('billing') not in ['Paid','Waived']:return {'error':'Payment/waiver required before scheduling'},409
   if not d.get('schedule'):return {'error':'Schedule required'},409
   update_rec(c,e['id'],{'schedule':d['schedule'],'scheduled_by':actor(role),'scheduled_at':now()},'Scheduled',role,'RAD_SCHEDULE');return {'ok':True},200
  if a=='perform_radiology':
   if role!='Radiology Technician':return {'error':'Radiology Technician required'},403
   if not e or e['entity_type']!='radiology_order':return {'error':'Radiology order required'},404
   if e['data'].get('billing') not in ['Paid','Waived'] or not e['data'].get('schedule'):return {'error':'Paid/waived and scheduled order required'},409
   cons=latest(c,pid,'consent');valid=any(x.get('status')=='Signed' for x in (cons['data'].get('items',[]) if cons else []))
   if e['data'].get('consent_required') and not valid:return {'error':'Current signed consent required'},409
   update_rec(c,e['id'],{'procedure_status':'Performed','performed_at':d.get('performed_at') or now(),'performed_by':actor(role)},'Performed',role,'RAD_PERFORM');rid=new_record(c,pid,'radiology',{'source_order_id':e['id'],'study':e['data'].get('study'),'date':str(date.today()),'findings':'','impression':'','esigned':False},'Draft',role);return {'ok':True,'radiology_entity_id':rid},200
  if a=='save_radiology':
   if role!='Radiologist':return {'error':'Radiologist required'},403
   if not e or e['entity_type']!='radiology':return {'error':'Radiology record required'},404
   fin=bool(d.get('finalize'));amendment_reason=str(d.get('amendment_reason') or '').strip();patch={k:v for k,v in d.items() if k not in ['finalize','amendment_reason']}
   if fin:
    miss=[x for x in ['study','date','findings','impression'] if not str(patch.get(x,e['data'].get(x,''))).strip()]
    if miss:return {'error':'Report incomplete','missing':miss},409
    patch.update({'esigned':True,'signed_by':actor(role),'signed_at':now()})
   if e['status']=='Final':
    if not amendment_reason:return {'error':'A finalized radiology report is immutable. Create a linked amendment with a documented reason.','requires_amendment_reason':True,'supersedes':e['id']},409
    nd={**e['data'],**patch,'supersedes':e['id'],'amendment_reason':amendment_reason,'amended_by':actor(role),'amended_at':now()};rid=new_record(c,pid,'radiology',nd,'Final' if fin else 'Draft',role);audit(c,pid,role,'RADIOLOGY_AMENDMENT_CREATED','radiology',rid,f'Supersedes {e["id"]}: {amendment_reason}');return {'ok':True,'id':rid,'status':'Final' if fin else 'Draft','supersedes':e['id']},200
   update_rec(c,e['id'],patch,'Final' if fin else 'Draft',role,'RAD_FINAL' if fin else 'RAD_SAVE');return {'ok':True,'id':e['id'],'status':'Final' if fin else 'Draft'},200
  if a=='submit_mdt_case':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:
    return {'error':'Oncology clinician required to submit MDT case'},403
   m=latest(c,pid,'mdt');co=latest(c,pid,'mdt_collab')
   if not m or not co:return {'error':'MDT workspace not found'},404
   question=str(d.get('clinical_question') or '').strip();summary=str(d.get('clinical_summary') or '').strip()
   if not question or not summary:return {'error':'Clinical question and summary are required for MDT submission'},409
   patch={'clinical_question':question,'clinical_summary':summary,'submitted_by':actor(role),'submitted_at':now(),'meeting_mode':d.get('meeting_mode','Internal'),'meeting_at':d.get('meeting_at',''),'submission_status':'Submitted'}
   update_rec(c,m['id'],patch,'Submitted',role,'MDT_CASE_SUBMIT',question)
   grant_patient_access(c,pid,'MDT Coordinator','mdt_case',m['id'],role);grant_patient_access(c,pid,'MDT Chair','mdt_case',m['id'],role)
   journey_add(c,pid,'MDT / Tumour Board','MDT Submitted','Pending',role,'mdt',m['id'],question,False)
   return {'ok':True,'mdt_id':m['id'],'status':'Submitted'},200
  if a=='mdt_comment':
   if role not in ['MDT Coordinator','MDT Chair','Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'MDT participant required'},403
   e=must('mdt_collab');comments=list(e['data'].get('comments',[]));
   if not d.get('comment'):return {'error':'Comment required'},409
   m=latest(c,pid,'mdt');finalized=bool(m and m['status']=='MDT Recommended')
   if finalized and (d.get('mode')!='addendum' or not str(d.get('addendum_reason') or '').strip()):return {'error':'MDT is finalized. Late comments require explicit addendum mode and addendum_reason; the original recommendation remains unchanged.'},409
   x={'id':'CMT-'+uuid.uuid4().hex[:6].upper(),'comment':d['comment'],'author':actor(role),'at':now(),'entry_type':'Finalized MDT Addendum' if finalized else 'Discussion Comment','addendum_reason':d.get('addendum_reason',''),'mdt_recommendation_id':m['id'] if m else ''};comments.append(x);update_rec(c,e['id'],{'comments':comments},role=role,action='MDT_ADDENDUM' if finalized else 'MDT_COMMENT',detail=d.get('addendum_reason',''));return {'ok':True,'comment':x},200
  if a=='mdt_attendance':
   if role!='MDT Coordinator':return {'error':'MDT Coordinator required'},403
   e=must('mdt_collab');name=str(d.get('name') or '').strip();disc=d.get('discipline');status=d.get('status','Present')
   if not name or disc not in MDT_DISCIPLINES:return {'error':'Attendee name and governed MDT discipline required','allowed_disciplines':MDT_DISCIPLINES},409
   att=list(e['data'].get('attendance',[]))
   if any(x.get('name')==name and x.get('discipline')==disc for x in att):return {'error':'Duplicate MDT attendee/discipline entry'},409
   att.append({'name':name,'discipline':disc,'status':status,'at':now(),'recorded_by':actor(role)})
   present={x.get('discipline') for x in att if x.get('status')=='Present'};quorum='Met' if {'Medical Oncology','Radiation Oncology','Surgical Oncology'}.issubset(present) else 'Not met'
   update_rec(c,e['id'],{'attendance':att,'quorum_status':quorum,'quorum_rule':'Synthetic QA quorum: MO + RO + SO present; CCA configuration required'},role=role,action='MDT_ATTENDANCE');return {'ok':True,'quorum_status':quorum},200
  if a=='mdt_recommend':
   if role!='MDT Coordinator':return {'error':'MDT Coordinator required to submit recommendation for Chair review'},403
   e=must('mdt');co=latest(c,pid,'mdt_collab');req=['meeting_at','clinical_question','clinical_summary','intent','recommendation','rationale','final_consensus','specialty_responsible'];miss=[x for x in req if not str(d.get(x,e['data'].get(x,''))).strip()]
   if miss:return {'error':'MDT recommendation incomplete','missing':miss},409
   if co and co['data'].get('quorum_status')!='Met':return {'error':'Configured MDT quorum must be met before Chair review','quorum_status':co['data'].get('quorum_status','Not met')},409
   if d.get('final_consensus') not in MDT_CONSENSUS:return {'error':'Governed MDT consensus required','allowed':MDT_CONSENSUS},409
   patch={**d,'recommendation_submitted_by':actor(role),'recommendation_submitted_at':now(),'chair_decision':'Pending','chair_signed_by':None,'chair_signed_at':'','chair_reason':'','signed_by':None,'signed_at':''}
   update_rec(c,e['id'],patch,'Pending Chair Approval',role,'MDT_RECOMMEND_SUBMIT');grant_patient_access(c,pid,'MDT Chair','mdt_chair_review',e['id'],role);handoff(c,pid,'MDT Chair','Review and sign submitted MDT recommendation','MDT case preparation','mdt',e['id'],role,'High',d.get('clinical_question',''),{'mdt_id':e['id']});return {'ok':True,'status':'Pending Chair Approval'},200
  if a=='mdt_chair_sign':
   if role!='MDT Chair':return {'error':'MDT Chair required'},403
   e=must('mdt');decision=d.get('decision');reason=str(d.get('reason') or '').strip();co=latest(c,pid,'mdt_collab')
   if e['status']!='Pending Chair Approval':return {'error':'Submitted MDT recommendation awaiting Chair review required'},409
   if not co or co['data'].get('quorum_status')!='Met':return {'error':'Derived MDT quorum must be Met before Chair sign-off'},409
   if decision not in ['Approve','Return for revision'] or not reason:return {'error':'Chair decision and reason required','allowed':['Approve','Return for revision']},409
   if decision=='Return for revision':
    update_rec(c,e['id'],{'chair_decision':'Returned for revision','chair_reason':reason,'chair_signed_by':actor(role),'chair_signed_at':now(),'signed_by':None,'signed_at':''},'Returned for Revision',role,'MDT_CHAIR_RETURN',reason);complete_open_tasks(c,pid,'MDT Chair','MDT case preparation',source_type='mdt',source_id=e['id'],completed_by=role);handoff(c,pid,'MDT Coordinator','Correct returned MDT recommendation','MDT case preparation','mdt',e['id'],role,'High',reason,{'return_reason':reason});return {'ok':True,'status':'Returned for Revision'},200
   patch={'chair_decision':'Approved','chair_reason':reason,'chair_signed_by':actor(role),'chair_signed_at':now(),'signed_by':actor(role),'signed_at':now()};update_rec(c,e['id'],patch,'MDT Recommended',role,'MDT_CHAIR_APPROVE',reason);complete_open_tasks(c,pid,'MDT Chair','MDT case preparation',source_type='mdt',source_id=e['id'],completed_by=role);resp=str(e['data'].get('specialty_responsible') or '')
   for rr in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:
    if rr in resp or resp in ['Combined-Modality','Multimodality','All Oncology']:grant_patient_access(c,pid,rr,'mdt',e['id'],role)
   journey_add(c,pid,'MDT / Tumour Board','Chair-approved MDT Recommendation','MDT Recommended',role,'mdt',e['id'],e['data'].get('recommendation',''),True);return {'ok':True,'status':'MDT Recommended','signed_by':actor(role)},200
  if a=='invite_external_mdt':
   if role!='MDT Coordinator':return {'error':'MDT Coordinator required'},403
   exp=d.get('expires_at');
   if not d.get('name') or not exp:return {'error':'Name and expiry required'},409
   tok=secrets.token_urlsafe(20);c.execute('INSERT INTO external_tokens VALUES(?,?,?,?,?,?,?)',(tok,pid,d['name'],d.get('discipline',''),exp,actor(role)['id'],now()));e=must('mdt_collab');xs=list(e['data'].get('external_consultants',[]));xs.append({'name':d['name'],'discipline':d.get('discipline',''),'expires_at':exp,'status':'Invited','case_scope':'De-identified MDT case only'});update_rec(c,e['id'],{'external_consultants':xs},role=role,action='MDT_EXTERNAL_INVITE');return {'ok':True,'access_token':tok},200
  if a=='save_care_plan':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator','Patient Liaison']:return {'error':'Care-team role required'},403
   e=must('care_plan');goals=d.get('goals',e['data'].get('goals',[]));milestones=d.get('milestones',e['data'].get('milestones',[]));deps=d.get('dependencies',e['data'].get('dependencies',[]));old_status=str(e['data'].get('status') or e['status'] or 'Draft');new_status=str(d.get('status') or old_status)
   if new_status not in VALUE_SETS['care_plan_status']:return {'error':'Care Plan status must use the governed state machine','allowed':VALUE_SETS['care_plan_status']},409
   if new_status not in CARE_PLAN_TRANSITIONS.get(old_status,{old_status}):return {'error':'Illegal Care Plan state transition','from':old_status,'to':new_status,'allowed':sorted(CARE_PLAN_TRANSITIONS.get(old_status,[]))},409
   if new_status in ['Blocked','On Hold','Cancelled','Superseded'] and not str(d.get('status_reason') or '').strip():return {'error':'status_reason is required for this Care Plan transition'},409
   update_rec(c,e['id'],{'goals':goals,'milestones':milestones,'dependencies':deps,'status':new_status,'status_reason':d.get('status_reason',''),'status_changed_at':now(),'status_changed_by':actor(role)},new_status,role,'CARE_PLAN_SAVE',f'{old_status} -> {new_status}');return {'ok':True,'status':new_status},200
  if a=='create_pathology_order':
   if role not in ['Medical Oncology','Surgical Oncology']:
    return {'error':'Medical or Surgical Oncology required to request pathology'},403
   path=latest(c,pid,'pathology')
   if not path:return {'error':'Pathology workspace not found'},404
   specimen=str(d.get('specimen') or '').strip();site=str(d.get('site') or '').strip();indication=str(d.get('indication') or '').strip()
   if not specimen or not site or not indication:return {'error':'Specimen, site and clinical indication are required'},409
   order_id='PATHORD-'+uuid.uuid4().hex[:8].upper()
   patch={'order_id':order_id,'ordered_specimen':specimen,'ordered_site':site,'clinical_indication':indication,'ordered_by':actor(role),'ordered_at':now(),'collection_status':'Pending','result_status':'Pending'}
   update_rec(c,path['id'],patch,'Ordered',role,'PATHOLOGY_ORDER',indication)
   grant_patient_access(c,pid,'Pathology','pathology_order',order_id,role)
   journey_add(c,pid,'Pathology','Pathology Ordered','Pending',role,'pathology',path['id'],indication,False)
   return {'ok':True,'pathology_record_id':path['id'],'order_id':order_id},200
  if a=='save_pathology':
   if role!='Pathology':return {'error':'Pathology role required'},403
   e=must('pathology');fin=bool(d.get('finalize'));amendment_reason=str(d.get('amendment_reason') or '').strip();patch={k:v for k,v in d.items() if k not in ['finalize','amendment_reason']}
   if fin:
    req=['date','site','specimen','histology'];miss=[x for x in req if not str(patch.get(x,e['data'].get(x,''))).strip()]
    if miss:return {'error':'Pathology report incomplete','missing':miss},409
    nex=patch.get('nodes_examined',e['data'].get('nodes_examined'));npos=patch.get('nodes_positive',e['data'].get('nodes_positive'))
    if nex not in ['',None] and npos not in ['',None]:
     try:
      if float(npos)>float(nex):return {'error':'Incoherent node counts: nodes_positive cannot exceed nodes_examined','nodes_examined':nex,'nodes_positive':npos},409
     except (TypeError,ValueError):pass
    patch.update({'signed_by':actor(role),'signed_at':now()})
   if e['status']=='Final':
    if not amendment_reason:return {'error':'A finalized pathology report is immutable. Create a linked amendment with a documented reason.','requires_amendment_reason':True,'supersedes':e['id']},409
    nd={**e['data'],**patch,'supersedes':e['id'],'amendment_reason':amendment_reason,'amended_by':actor(role),'amended_at':now()};rid=new_record(c,pid,'pathology',nd,'Final' if fin else 'Draft',role);update_rec(c,e['id'],{'superseded_by_record_id':rid},'Superseded',role,'PATHOLOGY_SUPERSEDE',amendment_reason);audit(c,pid,role,'PATHOLOGY_AMENDMENT_CREATED','pathology',rid,f'Supersedes {e["id"]}: {amendment_reason}');return {'ok':True,'id':rid,'status':'Final' if fin else 'Draft','supersedes':e['id']},200
   update_rec(c,e['id'],patch,'Final' if fin else 'Draft',role,'PATHOLOGY_FINAL' if fin else 'PATHOLOGY_SAVE');return {'ok':True,'id':e['id'],'status':'Final' if fin else 'Draft'},200

  if a=='create_plan_from_mdt':
   if role not in ['MDT Coordinator','Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'MDT/Oncology role required'},403
   mdt=e if e and e['entity_type']=='mdt' else latest(c,pid,'mdt')
   if not mdt or mdt['status']!='MDT Recommended' or (mdt['data'].get('chair_decision') not in [None,'','Approved']):return {'error':'A Chair-approved finalized MDT recommendation is required before creating a specialty plan'},409
   specialty=d.get('specialty');allowed=['Medical Oncology','Radiation Oncology','Surgical Oncology','Combined-Modality']
   if specialty not in allowed:return {'error':'Valid specialty plan type required'},409
   dx=latest(c,pid,'diagnosis');dd=dx['data'] if dx else {};rec=mdt['data'].get('recommendation','')
   phases=[]
   if specialty in ['Medical Oncology','Combined-Modality']:
    phases.append({'modality':'Systemic Therapy','regimen':'Select governed regimen','regimen_template_id':'','start_target':'','duration':'','status':'Draft','responsible':'Medical Oncology'})
   if specialty in ['Surgical Oncology','Combined-Modality']:
    phases.append({'modality':'Surgery','procedure':'Select governed surgical procedure template','start_target':'','duration':'Operative episode','status':'Draft','responsible':'Surgical Oncology'})
   if specialty in ['Radiation Oncology','Combined-Modality']:
    phases.append({'modality':'Radiation','regimen':'Create RT prescription','start_target':'','duration':'Fractions per prescription','status':'Draft','responsible':'Radiation Oncology'})
   seq=[p['modality'] for p in phases]
   ep=get_rec(c,d.get('episode_id')) if d.get('episode_id') else (current_episode(c,pid) or ensure_episode(c,pid,role))
   if not ep or ep.get('entity_type')!='cancer_episode':return {'error':'Valid cancer episode required for Treatment Plan'},409
   plan={'plan_no':'TP-'+uuid.uuid4().hex[:6].upper(),'version':1,'episode_id':ep['id'],'source_mdt_id':mdt['id'],'source_mdt_signed_at':mdt['data'].get('signed_at',''),'source_mdt_recommendation':rec,'created_from_mdt_at':now(),'created_by':actor(role),'plan_type':specialty,'diagnosis':dd.get('cancer_type',''),'stage':dd.get('stage_group',''),'histology':dd.get('histology',''),'biomarkers':dd.get('biomarkers',[]),'intent':mdt['data'].get('intent') or dd.get('treatment_intent',''),'line_of_therapy':'','disease_status':dd.get('disease_status',''),'responsible_specialty':specialty,'sequence':seq,'phases':phases,'mdt_proposed_by':mdt['data'].get('proposed_by',''),'mdt_participants':mdt['data'].get('attendees',[]),'mdt_final_consensus':mdt['data'].get('final_consensus',''),'mdt_outstanding_investigations':mdt['data'].get('outstanding_investigations',[])}
   rid=new_record(c,pid,'treatment_plan',plan,'Draft',role)
   for rr in sorted(set(p.get('responsible') for p in phases if p.get('responsible') in ['Medical Oncology','Surgical Oncology','Radiation Oncology'])):
    grant_patient_access(c,pid,rr,'treatment_plan',rid,role)
   return {'ok':True,'id':rid,'status':'Draft','note':'MDT created a draft plan only; no treatment order was generated.'},200
  if a=='save_treatment_plan':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Oncology clinician required'},403
   e=must('treatment_plan');sign=bool(d.get('sign'));patch={k:v for k,v in d.items() if k!='sign'}
   if sign:
    no_mdt_reason=str(patch.get('mdt_not_required_reason',e['data'].get('mdt_not_required_reason','')) or '').strip()
    external_origin=bool(patch.get('external_origin',e['data'].get('external_origin')))
    req=['diagnosis','stage','intent','line_of_therapy','sequence','phases'] + ([] if (external_origin or no_mdt_reason) else ['source_mdt_id']);miss=[x for x in req if patch.get(x,e['data'].get(x)) in ['',None,[]]]
    if miss:return {'error':'Treatment Plan incomplete','missing':miss},409
    patch.update({'signed_by':actor(role),'signed_at':now(),'version':int(e['data'].get('version',1))+1})
   if e['status'] in ['Clinician Approved','Active'] and sign:
    merged={**e['data'],**patch,'supersedes':e['id']}
    rid=new_record(c,pid,'treatment_plan',merged,'Clinician Approved',role)
    phases_for_access=merged.get('phases',[]) or []
    for rr in sorted(set(p.get('responsible') for p in phases_for_access if p.get('responsible') in ['Medical Oncology','Surgical Oncology','Radiation Oncology'])):
     grant_patient_access(c,pid,rr,'treatment_plan',rid,role)
    cancelled=[p for p in phases_for_access if p.get('status')=='Cancelled']
    if cancelled:
     reason=patch.get('amendment_reason') or '; '.join(str(p.get('cancellation_reason') or '') for p in cancelled if p.get('cancellation_reason')) or 'Treatment phase cancelled'
     journey_add(c,pid,role,'Treatment Phase Cancelled','Cancelled',role,'treatment_plan',rid,reason,True)
    else:
     journey_add(c,pid,role,'Treatment Plan Amendment','Clinician Approved',role,'treatment_plan',rid,patch.get('amendment_reason',''),True)
    return {'ok':True,'id':rid,'status':'Clinician Approved'},200
   update_rec(c,e['id'],patch,'Clinician Approved' if sign else 'Draft',role,'PLAN_SIGN' if sign else 'PLAN_SAVE',patch.get('amendment_reason','Treatment Plan updated'))
   if sign:
    phases_for_access=patch.get('phases',e['data'].get('phases',[])) or []
    for rr in sorted(set(p.get('responsible') for p in phases_for_access if p.get('responsible') in ['Medical Oncology','Surgical Oncology','Radiation Oncology'])):
     grant_patient_access(c,pid,rr,'treatment_plan',e['id'],role)
    journey_add(c,pid,role,'Treatment Plan','Clinician Approved',role,'treatment_plan',e['id'],patch.get('amendment_reason',''),True)
   return {'ok':True,'status':'Clinician Approved' if sign else 'Draft'},200
  if a=='amend_treatment_phase':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Oncology clinician required'},403
   plan=e if e and e['entity_type']=='treatment_plan' else latest(c,pid,'treatment_plan')
   if not plan:return {'error':'Treatment Plan required'},404
   reason=str(d.get('reason') or '').strip(); phase_index=d.get('phase_index')
   if not reason:return {'error':'Amendment reason required'},409
   try:phase_index=int(phase_index)
   except:return {'error':'Valid phase_index required'},409
   phases=[dict(x) for x in plan['data'].get('phases',[])]
   if phase_index<0 or phase_index>=len(phases):return {'error':'Treatment phase not found'},404
   old_phase=dict(phases[phase_index]);new_phase={**old_phase,**(d.get('changes') or {})}
   if d.get('operation')=='cancel':new_phase.update({'status':'Cancelled','cancellation_reason':reason,'cancelled_by':actor(role),'cancelled_at':now()})
   elif d.get('operation')=='activate':new_phase.update({'status':'Planned','activation_reason':reason,'activated_by':actor(role),'activated_at':now()})
   else:new_phase.update({'amendment_reason':reason,'amended_by':actor(role),'amended_at':now()})
   phases[phase_index]=new_phase
   patch={**plan['data'],'phases':phases,'version':int(plan['data'].get('version',1))+1,'supersedes':plan['id'],'amendment_reason':reason,'amendment_actor':actor(role),'amendment_at':now()}
   rid=new_record(c,pid,'treatment_plan',patch,'Clinician Approved' if plan['status'] in ['Clinician Approved','Active'] else plan['status'],role)
   journey_add(c,pid,role,'Treatment Plan Amendment',patch.get('phases',[{}])[phase_index].get('status','Amended'),role,'treatment_plan',rid,reason,True)
   return {'ok':True,'id':rid,'supersedes':plan['id'],'previous_phase':old_phase,'new_phase':new_phase},200
  if a in ['preview_readiness','save_readiness']:
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   template=regimen_from_template(c,d.get('template_id') or d.get('content_template_id') or 'REG-CCA-TCHP-DEMO')
   if not template or not template.get('orderable') or template.get('status')!='Active':return {'error':'Select an Active, CCA-approved orderable regimen template for readiness'},409
   lab=latest_final_lab(c,pid)
   if not lab:return {'error':'A finalized laboratory result is required before treatment readiness can be evaluated'},409
   ld=lab['data']; units=ld.get('units') or {};missing_units,invalid_units=validate_lab_units(ld,units,READINESS_REQUIRED_UNIT_FIELDS)
   if missing_units:return {'error':'Finalized laboratory result is missing required unit metadata','missing_units':missing_units,'lab_source_id':lab['id']},409
   if invalid_units:return {'error':'Finalized laboratory result contains unsupported unit metadata','invalid_units':invalid_units,'lab_source_id':lab['id']},409
   intake=latest(c,pid,'intake'); idata=intake['data'] if intake else {}
   tox=latest(c,pid,'toxicity'); active_tox=[]
   if tox:
    active_tox=[x for x in tox['data'].get('events',[]) if str(x.get('outcome','')).lower() not in ['resolved','recovered']]
   tox_summary=d.get('toxicity_summary') or '; '.join([f"{x.get('term') or x.get('toxicity_type')} G{x.get('grade')} ({x.get('outcome','Ongoing')})" for x in active_tox])
   # Never trust readiness-screen lab numbers or units. Resolve them from the finalized Lab record.
   resolved={**d,'lab_date':ld.get('date'),'anc':ld.get('anc'),'platelets':ld.get('platelets'),'egfr':ld.get('egfr'),'bilirubin':ld.get('bilirubin'),'lvef':ld.get('lvef'),'pregnancy':ld.get('pregnancy'),'lab_units':units,'lab_source_id':lab['id'],'lab_source_finalized_at':ld.get('finalized_at'),'weight_kg':idata.get('weight_kg'),'bsa_m2':idata.get('bsa_m2'),'toxicity_summary':tox_summary,'toxicity_source_id':tox['id'] if tox else '','active_toxicity_ids':[x.get('id') for x in active_tox]}
   protocol=template['data'];ev=readiness_eval(resolved,protocol);d2={**resolved,'protocol_id':protocol['id'],'protocol_version':protocol['version'],'content_template_id':template['id'],'content_template_version':template['version'],'protocol_evaluation':ev}
   if a=='preview_readiness':return ev,200
   e=must('readiness');sign=bool(d.get('sign'))
   if sign and d.get('decision') in ['Proceed as Planned','Proceed with Modification'] and ev['blockers']:return {'error':'Cannot sign proceeding decision while protocol blockers exist','blockers':ev['blockers']},409
   if sign and not d.get('decision'):return {'error':'Readiness decision required'},409
   decision_reason=str(d.get('decision_reason') or d.get('reason') or '').strip()
   if sign and not decision_reason:return {'error':'Every signed treatment-readiness decision requires an explicit clinician reason'},409
   if sign:d2.update({'decision':d.get('decision'),'decision_reason':decision_reason,'signed_by':actor(role),'signed_at':now(),'readiness_attestation':'I reviewed the regimen-specific criteria, source results, freshness, toxicity and proposed outcomes and make the stated treatment-readiness decision.'})
   update_rec(c,e['id'],d2,'Signed' if sign else 'Draft',role,'READINESS_SIGN' if sign else 'READINESS_SAVE')
   if sign:
    decision=d.get('decision','')
    cp=latest(c,pid,'care_plan')
    if decision in ['Hold','Delay']:
     reason=d.get('decision_reason') or d.get('clinical_rationale') or '; '.join(ev.get('blockers',[])) or 'Treatment held/delayed'
     reevaluate=d.get('reevaluation_date','')
     if cp:update_rec(c,cp['id'],{'current_exception':{'type':decision,'reason':reason,'reevaluation_date':reevaluate,'at':now(),'by':actor(role)}},'Active',role,'CARE_PLAN_EXCEPTION',reason)
     ap=latest(c,pid,'appointments')
     if ap:
      rows=[]
      for x in ap['data'].get('items',[]):
       y=dict(x)
       if y.get('status') in ['Scheduled','Rescheduled','Pending'] and ('treat' in str(y.get('purpose','')).lower() or 'day care' in str(y.get('department','')).lower()):y.update({'status':decision,'reason':reason,'reevaluation_date':reevaluate,'updated_at':now(),'updated_by':actor(role)})
       rows.append(y)
      update_rec(c,ap['id'],{'items':rows},'Active',role,'TREATMENT_SCHEDULE_EXCEPTION',reason)
     journey_add(c,pid,'Medical Oncology','Treatment '+decision,decision,role,'readiness',e['id'],reason,True)
    elif decision in ['Proceed as Planned','Proceed with Modification'] and cp and cp['data'].get('current_exception'):
     update_rec(c,cp['id'],{'current_exception':None},'Active',role,'CARE_PLAN_EXCEPTION_CLEAR',decision)
   return {'ok':True,'status':'Signed' if sign else 'Draft','evaluation':ev},200
  if a=='review_role_surface':
   target=d.get('role_surface') or role
   if target!=role and role!='Hospital Management / Admin':return {'error':'A role may review only its own working surface; Admin may record an externally supplied review.'},403
   if target not in ROLE_SURFACES:return {'error':'Unknown role surface'},404
   verdict=d.get('verdict');allowed=['Accepted','Minor Gap','Major Gap','Critical Gap']
   if verdict not in allowed:return {'error':'Review verdict required','allowed':allowed},409
   note=str(d.get('note') or '').strip()
   if verdict!='Accepted' and not note:return {'error':'Gap review requires a note'},409
   rid='RSR-'+uuid.uuid4().hex[:10].upper();c.execute('INSERT INTO role_surface_reviews VALUES(?,?,?,?,?,?,?)',(rid,target,role,actor(role)['id'],verdict,note,now()));audit(c,'',role,'ROLE_SURFACE_REVIEW','role_surface',target,verdict+(' • '+note if note else ''));return {'ok':True,'id':rid,'verdict':verdict},200
  if a=='content_regimen_safety_rules':
   if role not in ['Medical Oncology','Oncology Pharmacy']:return {'error':'Medical Oncology or Oncology Pharmacy required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x or x['category']!='Regimen':return {'error':'Regimen template required'},404
   if x.get('source_id')!='SRC-CCA-DEMO':return {'error':'Imported source references are immutable. Clone to a CCA Working Copy before adding local safety rules or reviews.'},409
   rules=d.get('hold_parameters') or {};required=['ANC_min','platelets_min','eGFR_min','bilirubin_max','lab_max_age_days'];miss=[k for k in required if rules.get(k) in ['',None]]
   if miss:return {'error':'Minimum readiness-rule fields missing','missing':miss},409
   cd=dict(x['data']);cd['hold_parameters']={**cd.get('hold_parameters',{}),**rules};gov=dict(cd.get('governance',{}));gov['safety_rules_updated_by']=actor(role);gov['safety_rules_updated_at']=now();cd['governance']=gov;y=content_update(c,x['id'],{'data':cd},role);return {'ok':True,'template':y},200
  if a=='content_clinical_review':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x or x['category']!='Regimen':return {'error':'Regimen template required'},404
   if x.get('source_id')!='SRC-CCA-DEMO':return {'error':'Imported source references are immutable. Clone to a CCA Working Copy before adding local safety rules or reviews.'},409
   cd=dict(x['data']);gov=dict(cd.get('governance',{}));gov['clinical_review']={'status':d.get('status','Approved'),'by':actor(role),'at':now(),'note':d.get('note','')};cd['governance']=gov;y=content_update(c,x['id'],{'data':cd,'clinical_owner':actor(role)['name'],'governance_status':'Clinical Review Complete / Pharmacy Review Pending' if gov['clinical_review']['status']=='Approved' else 'Clinical Review Requires Changes'},role);return {'ok':True,'template':y},200
  if a=='content_pharmacy_review':
   if role!='Oncology Pharmacy':return {'error':'Oncology Pharmacy required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x or x['category']!='Regimen':return {'error':'Regimen template required'},404
   if x.get('source_id')!='SRC-CCA-DEMO':return {'error':'Imported source references are immutable. Clone to a CCA Working Copy before adding local safety rules or reviews.'},409
   cd=dict(x['data']);gov=dict(cd.get('governance',{}));gov['pharmacy_review']={'status':d.get('status','Approved'),'by':actor(role),'at':now(),'note':d.get('note','')};cd['governance']=gov;clinical=(gov.get('clinical_review') or {}).get('status')=='Approved';gs='Clinical + Pharmacy Review Complete / Admin Activation Pending' if clinical and gov['pharmacy_review']['status']=='Approved' else 'Pharmacy Review Complete / Clinical Review Pending';y=content_update(c,x['id'],{'data':cd,'pharmacy_owner':actor(role)['name'],'governance_status':gs},role);return {'ok':True,'template':y},200
  if a=='content_specialty_review':
   x=content_one(c,d.get('template_id') or eid)
   if not x:return {'error':'Template not found'},404
   status=d.get('status','Approved')
   if status not in ['Approved','Requires Changes']:return {'error':'Approved or Requires Changes required'},409
   cd=dict(x['data']);gov=dict(cd.get('governance',{}));key='';label=''
   if x['category']=='Radiation Template':
    if role=='Radiation Oncology':key='radiation_oncology_review';label='Radiation Oncology'
    elif role=='Radiation Physicist':key='physics_review';label='Radiation Physics'
    else:return {'error':'Radiation Oncology or Radiation Physicist required'},403
   elif x['category']=='Surgical Template':
    if role!='Surgical Oncology':return {'error':'Surgical Oncology required'},403
    key='surgical_oncology_review';label='Surgical Oncology'
   else:return {'error':'Specialty review action is only for Radiation or Surgical templates'},409
   gov[key]={'status':status,'by':actor(role),'at':now(),'note':d.get('note','')};cd['governance']=gov
   if x['category']=='Radiation Template':
    ro=(gov.get('radiation_oncology_review') or {}).get('status')=='Approved';ph=(gov.get('physics_review') or {}).get('status')=='Approved';gs='Radiation Oncology + Physics Review Complete / Admin Activation Pending' if ro and ph else label+' review recorded / additional review pending'
   else:gs='Surgical Oncology Review Complete / Admin Activation Pending' if status=='Approved' else 'Surgical Oncology Review Requires Changes'
   y=content_update(c,x['id'],{'data':cd,'governance_status':gs},role);return {'ok':True,'template':y},200
  if a=='content_regimen_item_edit':
   if role!='Medical Oncology':return {'error':'Medical Oncology required to edit clinical regimen items'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x or x['category']!='Regimen':return {'error':'Regimen template required'},404
   if x.get('source_id')!='SRC-CCA-DEMO':return {'error':'Imported source references are immutable. Clone to a CCA Working Copy first.'},409
   if x.get('status')=='Active' or x.get('orderable'):return {'error':'Active/orderable templates are immutable. Clone a new version before editing.'},409
   op=d.get('operation','update');cd=dict(x['data']);items=[dict(z) for z in cd.get('items',[])];seq=d.get('sequence')
   if op=='remove':
    try:seq=int(seq)
    except:return {'error':'Sequence required'},409
    if not any(int(z.get('sequence',-1))==seq for z in items):return {'error':'Regimen item not found'},404
    items=[z for z in items if int(z.get('sequence',-1))!=seq]
   else:
    item=dict(d.get('item') or {});required=['sequence','group','drug','code','dose_basis','protocol_dose','protocol_unit','route'];missing=[k for k in required if item.get(k) in ['',None]]
    if missing:return {'error':'Structured regimen item incomplete','missing':missing},409
    try:item['sequence']=int(item['sequence']);item['protocol_dose']=float(item['protocol_dose'])
    except:return {'error':'Sequence and protocol dose must be numeric'},409
    if item['dose_basis'] not in VALUE_SETS['dose_basis']:return {'error':'Dose basis must use governed value set'},409
    if item['route'] not in VALUE_SETS['route']:return {'error':'Route must use governed value set'},409
    allowed_groups=['Premedication','Hydration','Antineoplastic','Targeted Therapy','Immunotherapy','Hormonal Therapy','Supportive','Rescue','Emergency / Hypersensitivity','Other']
    if item['group'] not in allowed_groups:return {'error':'Medication group must use governed value set','allowed':allowed_groups},409
    if item.get('relative_start_days') is None:item['relative_start_days']=[1]
    if not isinstance(item.get('relative_start_days'),list):return {'error':'relative_start_days must be a list'},409
    found=False
    for n,z in enumerate(items):
     if int(z.get('sequence',-1))==item['sequence']:items[n]={**z,**item};found=True;break
    if not found:items.append(item)
   items=sorted(items,key=lambda z:int(z.get('sequence',9999)))
   # Editing clinical content invalidates prior approvals/reviews.
   cd['items']=items;gov=dict(cd.get('governance',{}));gov.pop('clinical_review',None);gov.pop('pharmacy_review',None);gov['clinical_content_last_edited_by']=actor(role);gov['clinical_content_last_edited_at']=now();cd['governance']=gov
   y=content_update(c,x['id'],{'data':cd,'status':'Draft','governance_status':'Clinical + Pharmacy Re-review Required','orderable':False,'clinical_owner':actor(role)['name'],'pharmacy_owner':'Pending'},role);return {'ok':True,'template':y},200
  if a=='content_regimen_pharmacy_detail':
   if role!='Oncology Pharmacy':return {'error':'Oncology Pharmacy required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x or x['category']!='Regimen':return {'error':'Regimen template required'},404
   if x.get('source_id')!='SRC-CCA-DEMO':return {'error':'Imported source references are immutable. Clone to a CCA Working Copy first.'},409
   if x.get('status')=='Active' or x.get('orderable'):return {'error':'Active/orderable templates are immutable. Clone a new version before editing.'},409
   try:seq=int(d.get('sequence'))
   except:return {'error':'Sequence required'},409
   cd=dict(x['data']);items=[dict(z) for z in cd.get('items',[])];target=next((z for z in items if int(z.get('sequence',-1))==seq),None)
   if not target:return {'error':'Regimen item not found'},404
   for k in ['diluent','volume_ml','duration_min','timing','preparation_notes','special_instructions']:
    if k in d:target[k]=d[k]
   gov=dict(cd.get('governance',{}));gov.pop('pharmacy_review',None);gov['pharmacy_detail_last_edited_by']=actor(role);gov['pharmacy_detail_last_edited_at']=now();cd['governance']=gov;cd['items']=items
   y=content_update(c,x['id'],{'data':cd,'status':'Draft','governance_status':'Pharmacy Re-review Required','orderable':False,'pharmacy_owner':actor(role)['name']},role);return {'ok':True,'template':y},200
  if a=='formulary_save':
   if role not in ['Oncology Pharmacy','Hospital Management / Admin']:return {'error':'Oncology Pharmacy or Admin required'},403
   fid=d.get('formulary_id') or eid or ('FORM-'+uuid.uuid4().hex[:8].upper());existing=formulary_one(c,fid)
   if existing and existing.get('status') in ['Active','Retired']:return {'error':'Active/retired formulary versions are immutable. Clone a new Draft version before editing.'},409
   required=['drug','display_name','code_system','code','version'];missing=[k for k in required if not str(d.get(k) or '').strip()]
   if missing:return {'error':'Formulary item incomplete','missing':missing},409
   routes=d.get('allowed_routes') or [];diluents=d.get('allowed_diluents') or [];forms=d.get('formulations') or []
   if not routes:return {'error':'At least one allowed route is required'},409
   if any(x not in VALUE_SETS['route'] for x in routes):return {'error':'Formulary route must use governed route value set'},409
   if not forms:return {'error':'At least one formulation/strength is required'},409
   for f in forms:
    if not f.get('label') or f.get('strength_mg') in ['',None]:return {'error':'Each formulation requires label and strength_mg'},409
   t=now();review={}
   if existing:
    c.execute('UPDATE content_formulary SET drug=?,display_name=?,code_system=?,code=?,version=?,status=?,source_id=?,source_ref=?,routes_json=?,diluents_json=?,formulations_json=?,rounding_policy=?,notes=?,pharmacy_review_json=?,updated_at=?,approved_by=?,approved_at=?,retired_at=? WHERE id=?',(d['drug'],d['display_name'],d['code_system'],d['code'],d['version'],'Draft','SRC-CCA-DEMO',d.get('source_ref','CCA institution formulary'),jdump(routes),jdump(diluents),jdump(forms),d.get('rounding_policy','No rounding'),d.get('notes',''),jdump(review),t,'','','',fid))
   else:
    c.execute('INSERT INTO content_formulary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(fid,d['drug'],d['display_name'],d['code_system'],d['code'],d['version'],'Draft','SRC-CCA-DEMO',d.get('source_ref','CCA institution formulary'),jdump(routes),jdump(diluents),jdump(forms),d.get('rounding_policy','No rounding'),d.get('notes',''),jdump(review),t,t,'','',''))
   audit(c,'',role,'FORMULARY_SAVE','content_formulary',fid,d['drug']+' v'+d['version']);return {'ok':True,'item':formulary_one(c,fid)},200
  if a=='formulary_clone':
   if role not in ['Oncology Pharmacy','Hospital Management / Admin']:return {'error':'Oncology Pharmacy or Admin required'},403
   src=formulary_one(c,d.get('formulary_id') or eid)
   if not src:return {'error':'Formulary item not found'},404
   fid='FORM-'+uuid.uuid4().hex[:8].upper();t=now();ver=str(d.get('version') or 'next-draft');c.execute('INSERT INTO content_formulary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(fid,src['drug'],src['display_name'],src['code_system'],src['code'],ver,'Draft','SRC-CCA-DEMO','New CCA version cloned from '+src['id'],jdump(src['allowed_routes']),jdump(src['allowed_diluents']),jdump(src['formulations']),src.get('rounding_policy','No rounding'),src.get('notes',''),jdump({}),t,t,'','',''));audit(c,'',role,'FORMULARY_CLONE','content_formulary',fid,src['id']);return {'ok':True,'item':formulary_one(c,fid)},200
  if a=='formulary_review':
   if role!='Oncology Pharmacy':return {'error':'Oncology Pharmacy required'},403
   x=formulary_one(c,d.get('formulary_id') or eid)
   if not x:return {'error':'Formulary item not found'},404
   if x.get('status')!='Draft':return {'error':'Only Draft formulary versions can be reviewed'},409
   status=d.get('status','Approved')
   if status not in ['Approved','Requires Changes']:return {'error':'Approved or Requires Changes required'},409
   review={'status':status,'by':actor(role),'at':now(),'note':d.get('note','')};c.execute('UPDATE content_formulary SET pharmacy_review_json=?,updated_at=? WHERE id=?',(jdump(review),now(),x['id']));audit(c,'',role,'FORMULARY_PHARMACY_REVIEW','content_formulary',x['id'],status);return {'ok':True,'item':formulary_one(c,x['id'])},200
  if a=='formulary_approve':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   x=formulary_one(c,d.get('formulary_id') or eid)
   if not x:return {'error':'Formulary item not found'},404
   if (x.get('pharmacy_review') or {}).get('status')!='Approved':return {'error':'Oncology Pharmacy approval required before formulary activation'},409
   # only one Active version per exact local code; older versions are retired, never deleted
   t=now();c.execute("UPDATE content_formulary SET status='Retired',retired_at=?,updated_at=? WHERE code=? AND status='Active' AND id<>?",(t,t,x['code'],x['id']));c.execute("UPDATE content_formulary SET status='Active',approved_by=?,approved_at=?,updated_at=? WHERE id=?",(actor(role)['name'],t,t,x['id']));audit(c,'',role,'FORMULARY_ACTIVATE','content_formulary',x['id'],x['drug']+' v'+x['version']);return {'ok':True,'item':formulary_one(c,x['id'])},200
  if a=='formulary_retire':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   x=formulary_one(c,d.get('formulary_id') or eid)
   if not x:return {'error':'Formulary item not found'},404
   t=now();c.execute("UPDATE content_formulary SET status='Retired',retired_at=?,updated_at=? WHERE id=?",(t,t,x['id']));audit(c,'',role,'FORMULARY_RETIRE','content_formulary',x['id'],d.get('reason',''));return {'ok':True,'item':formulary_one(c,x['id'])},200
  if a=='content_approve':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x:return {'error':'Template not found'},404
   if x.get('source_id')!='SRC-CCA-DEMO':return {'error':'Imported/reference templates cannot be activated directly. Clone to a CCA Working Copy first.'},409
   if x['category']=='Regimen':
    cd=x['data'];missing=[]
    for k in ['name','version','cycle_length_days','planned_cycles','items','hold_parameters']:
     if cd.get(k) in [None,'',[],{}]:missing.append(k)
    if missing:return {'error':'Regimen cannot become orderable until clinical content is complete','missing':missing},409
    fmap=active_formulary_map(c);unmapped=[i.get('drug') for i in cd.get('items',[]) if i.get('drug') not in fmap and i.get('code') not in fmap]
    if unmapped:return {'error':'Regimen cannot become orderable until every medication has an Active institution formulary mapping','unmapped_drugs':unmapped},409
    if not x.get('clinical_owner') or x.get('clinical_owner')=='Pending' or not x.get('pharmacy_owner') or x.get('pharmacy_owner')=='Pending':return {'error':'Named Medical Oncology and Pharmacy owners required before regimen activation'},409
    gov=cd.get('governance',{});reviews=[]
    if (gov.get('clinical_review') or {}).get('status')!='Approved':reviews.append('Medical Oncology clinical review')
    if (gov.get('pharmacy_review') or {}).get('status')!='Approved':reviews.append('Oncology Pharmacy review')
    if reviews:return {'error':'Required independent content reviews are incomplete','missing':reviews},409
   if x['category']=='Radiation Template':
    gov=x['data'].get('governance',{});missing=[]
    if (gov.get('radiation_oncology_review') or {}).get('status')!='Approved':missing.append('Radiation Oncology review')
    if (gov.get('physics_review') or {}).get('status')!='Approved':missing.append('Radiation Physics review')
    if missing:return {'error':'Radiation template review is incomplete','missing':missing},409
   if x['category']=='Surgical Template':
    gov=x['data'].get('governance',{})
    if (gov.get('surgical_oncology_review') or {}).get('status')!='Approved':return {'error':'Surgical Oncology review is incomplete','missing':['Surgical Oncology review']},409
   y=content_update(c,x['id'],{'status':'Active','governance_status':'CCA Approved','orderable':True if x['category']=='Regimen' else x['orderable'],'approved_by':actor(role)['name'],'approved_at':now()},role);return {'ok':True,'template':y},200
  if a=='content_retire':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x:return {'error':'Template not found'},404
   y=content_update(c,x['id'],{'status':'Retired','governance_status':'Retired','orderable':False,'retired_at':now()},role);return {'ok':True,'template':y},200
  if a=='content_clone':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   src=content_one(c,d.get('template_id') or eid)
   if not src:return {'error':'Template not found'},404
   nid='TPL-'+uuid.uuid4().hex[:8].upper();t=now();name=str(d.get('name') or (src['name']+' — CCA Working Copy'));ver=str(d.get('version') or '1.0-draft');copy_data={**src['data'],'origin_source_id':src.get('source_id'),'origin_source_ref':src.get('source_ref'),'origin_template_id':src.get('id'),'origin_template_version':src.get('version'),'governance':{}};c.execute('INSERT INTO content_templates VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(nid,src['category'],name,src['subtype'],src['disease'],src['setting'],src['intent'],src['line_of_therapy'],ver,'Draft','Clinical + Pharmacy Review Required',0,'SRC-CCA-DEMO','Cloned from '+src['id'],'','',d.get('clinical_owner','Pending'),d.get('pharmacy_owner','Pending'),jdump(copy_data),t,t,'','',''));audit(c,'',role,'CONTENT_TEMPLATE_CLONE','content_template',nid,src['id']);return {'ok':True,'template':content_one(c,nid)},200
  if a=='content_update':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   x=content_one(c,d.get('template_id') or eid)
   if not x:return {'error':'Template not found'},404
   if x.get('source_id') not in ['SRC-CCA-DEMO','SRC-CCA-QA']:return {'error':'Imported source references are immutable. Clone before local editing.'},409
   if x.get('status') in ['Active','Retired'] or x.get('orderable'):return {'error':'Active/orderable/retired clinical content is immutable. Clone a new Draft version before editing.','template_id':x['id'],'status':x.get('status'),'orderable':x.get('orderable')},409
   allowed={k:d[k] for k in ['name','disease','setting','intent','line_of_therapy','version','clinical_owner','pharmacy_owner','review_due'] if k in d};y=content_update(c,x['id'],allowed,role);return {'ok':True,'template':y},200
  if a=='create_order':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   ready=latest(c,pid,'readiness');template=regimen_from_template(c,d.get('template_id') or 'REG-CCA-TCHP-DEMO');
   if not template or not template.get('orderable') or template.get('status')!='Active':return {'error':'Select an Active, CCA-approved orderable regimen template'},409
   protocol=template['data'];ev=(ready['data'].get('protocol_evaluation') if ready and ready['data'].get('protocol_id')==protocol.get('id') else None) or readiness_eval(ready['data'] if ready else {},protocol)
   if not ready or ready['status']!='Signed' or ready['data'].get('decision') not in ['Proceed as Planned','Proceed with Modification'] or ev['blockers']:return {'error':'Signed treatment readiness without blockers is required','blockers':ev['blockers'] if ev else []},409
   intake=latest(c,pid,'intake')
   if not intake or not intake['data'].get('source_measurements') or not intake['data'].get('measurement_units'):
    return {'error':'Treatment Order requires a current Intake measurement set with explicit source units. Re-measure/re-save Intake before dose calculation.'},409
   w=float(intake['data'].get('weight_kg') or 0);bsa=float(intake['data'].get('bsa_m2') or 0);bsa_calc=float(intake['data'].get('bsa_raw_m2') or bsa);pat=patient(c,pid);med=latest(c,pid,'med_recon');coded_allergies=med['data'].get('allergies',[]) if med else [];allergy=[f"{x.get('substance')} — {x.get('reaction')}" for x in coded_allergies]
   recon_events=list((med or {}).get('data',{}).get('reconciliation_events',[]));latest_recon=recon_events[-1] if recon_events else {}
   if latest_recon.get('reconciliation_status')!='Complete':return {'error':'A current Complete medication/allergy reconciliation attestation is required before authorising systemic treatment','reconciliation_status':latest_recon.get('reconciliation_status') or 'Missing'},409
   decision_reasons=d.get('dose_decision_reasons') or {};admin_reason=str(d.get('administration_decision_reason') or '').strip();schedule_reason=str(d.get('schedule_decision_reason') or '').strip();decision_at=now();decision_actor=actor(role)
   if not admin_reason:return {'error':'Signed Treatment Order requires an explicit clinician reason for accepting/setting route, diluent, volume, rate and duration parameters'},409
   if not schedule_reason:return {'error':'Signed Treatment Order requires an explicit clinician reason for the administration date/time decision'},409
   fmap=active_formulary_map(c);cum_before=cumulative_administered_by_code(c,pid);admin_params=d.get('administration_parameters') or {};order_cycle=int(d.get('cycle',1))
   items=[]
   for q in protocol['items']:
    fi=fmap.get(q.get('drug')) or fmap.get(q.get('code'))
    if not fi:return {'error':f"No Active institution formulary mapping for {q['drug']}"},409
    item_renal=(d.get('renal_dosing') or {}).get(q['code']) if q['dose_basis']=='AUC' else None
    calc=calc_dose(q,w,bsa_calc,order_cycle,item_renal);ordered=d.get('doses',{}).get(q['code'],calc)
    if q['dose_basis']=='AUC' and ordered in [None,'']: return {'error':f"Clinician must enter patient-specific ordered dose for {q['drug']} AUC item; demo does not calculate AUC automatically"},409
    try:ordered=float(ordered)
    except:return {'error':f"Invalid ordered dose for {q['drug']}"},409
    if ordered<0:return {'error':f"Ordered dose cannot be negative for {q['drug']}"},409
    hardmax=safe_float(q.get('max_dose_mg'))
    if hardmax is not None and ordered>hardmax:return {'error':f"Ordered dose {ordered} mg exceeds configured hard maximum {hardmax} mg for {q['drug']}"},409
    if item_renal:
     rmethod=str(item_renal.get('method') or '').strip();rvalue=safe_float(item_renal.get('value_ml_min'));rsource=str(item_renal.get('source_id') or '').strip();rat=str(item_renal.get('measured_at') or '').strip()
     if not rmethod or rmethod not in ALLOWED_RENAL_METHODS:return {'error':f"AUC dosing for {q['drug']} requires an explicitly governed renal dosing method when renal dosing provenance is supplied",'allowed_renal_methods':ALLOWED_RENAL_METHODS},409
     if rvalue is None or rvalue<=0:return {'error':f"AUC dosing for {q['drug']} requires a positive renal dosing value in mL/min"},409
     if not rsource or not rat:return {'error':f"AUC dosing for {q['drug']} requires a documented renal value source and timestamp"},409
    variance=0 if calc in [None,0] else round((ordered-calc)/calc*100,1);variance_reason=(d.get('variance_reasons') or {}).get(q['code'],'')
    if abs(variance)>20 and not variance_reason:return {'error':f"Dose variance >20% requires variance reason for {q['drug']}"},409
    decision_reason=str(decision_reasons.get(q['code']) or decision_reasons.get('*') or '').strip()
    if not decision_reason:return {'error':f"Final ordered dose for {q['drug']} is a clinician decision and requires an explicit decision reason before signature",'field':q['code'],'requires':'dose_decision_reasons'},409
    ap=admin_params.get(q['code']) or {};route=ap.get('route',q.get('route'));diluent=ap.get('diluent',q.get('diluent',''));volume=ap.get('volume_ml',q.get('volume_ml'));duration=ap.get('duration_min',q.get('duration_min'));rate=ap.get('rate_ml_hr')
    if route not in fi.get('allowed_routes',[]):return {'error':f"Route is not allowed by the active formulary for {q['drug']}",'route':route,'allowed':fi.get('allowed_routes',[])},409
    if diluent and diluent not in fi.get('allowed_diluents',[]):return {'error':f"Diluent is not allowed by the active formulary for {q['drug']}",'diluent':diluent,'allowed':fi.get('allowed_diluents',[])},409
    if route=='IV':
     volume=safe_float(volume);duration=safe_float(duration);rate=safe_float(rate) if rate not in [None,''] else (round(volume/(duration/60),2) if volume and duration else None)
     if volume is None or volume<=0 or duration is None or duration<=0 or rate is None or rate<=0:return {'error':f"IV order requires positive diluent volume, infusion duration and rate for {q['drug']}"},409
     expected_rate=volume/(duration/60)
     if abs(rate-expected_rate)>max(0.5,expected_rate*0.02):return {'error':f"Infusion rate must reconcile with ordered volume and duration for {q['drug']}",'expected_rate_ml_hr':round(expected_rate,2),'submitted_rate_ml_hr':rate},409
    else:
     volume=volume if volume not in ['',None] else None;duration=duration if duration not in ['',None] else None;rate=rate if rate not in ['',None] else None
    rounding=(d.get('rounding') or {}).get(q['code'],fi.get('rounding_policy') or 'No rounding')
    if rounding!=(fi.get('rounding_policy') or 'No rounding'):return {'error':f"Dose rounding selection must use the active formulary policy for {q['drug']}",'allowed':[fi.get('rounding_policy') or 'No rounding']},409
    out_unit='mg' if q['dose_basis'] in ['mg/kg','mg/m²','AUC'] else q.get('protocol_unit','mg')
    block='Pre-treatment' if q.get('group')=='Premedication' else ('Anti-cancer treatment' if q.get('group') in ['Antineoplastic','Targeted Therapy'] else 'Post-treatment / supportive')
    before=float(cum_before.get(q['code'],0) or 0);limit=q.get('cumulative_dose_limit')
    items.append({**q,'treatment_block':block,'item_id':'OI-'+uuid.uuid4().hex[:7].upper(),'calculated_dose':calc,'calculated_unit':out_unit,'ordered_dose':ordered,'ordered_unit':out_unit,'final_approved_dose':ordered,'renal_dosing':item_renal,'dose_decision_reason':decision_reason,'dose_decided_by':decision_actor,'dose_decided_at':decision_at,'variance_pct':variance,'variance_reason':variance_reason,'rounding':rounding,'route':route,'diluent':diluent,'volume_ml':volume,'duration_min':duration,'rate_ml_hr':rate or 0,'administration_parameter_decision_reason':admin_reason,'administration_parameters_decided_by':decision_actor,'administration_parameters_decided_at':decision_at,'administration_at':d.get('administration_at',now()),'schedule_decision_reason':schedule_reason,'schedule_decided_by':decision_actor,'schedule_decided_at':decision_at,'cumulative_dose_before':before,'cumulative_dose_limit':limit,'cumulative_dose_after_if_fully_administered':round(before+ordered,4)})
   ep=get_rec(c,d.get('episode_id')) if d.get('episode_id') else (current_episode(c,pid) or ensure_episode(c,pid,role));
   if not ep or ep.get('entity_type')!='cancer_episode' or ep.get('patient_id')!=pid:return {'error':'Valid patient cancer episode required for Treatment Order'},409
   # Executable systemic orders must always be instantiated from a clinician-authorized
   # Treatment Plan for the same patient/cancer episode. MDT recommendation or a Draft
   # plan is strategy context only and must never become an executable order directly.
   plan=get_rec(c,d.get('plan_id')) if d.get('plan_id') else latest(c,pid,'treatment_plan')
   if not plan or plan.get('entity_type')!='treatment_plan' or plan.get('patient_id')!=pid:
    return {'error':'Clinician-approved Treatment Plan is required before creating a Treatment Order'},409
   if plan.get('status') not in ['Clinician Approved','Active']:
    return {'error':'Treatment Order cannot be created from an unsigned or inactive Treatment Plan','plan_id':plan.get('id'),'plan_status':plan.get('status')},409
   plan_episode=plan.get('data',{}).get('episode_id')
   if plan_episode and plan_episode!=ep['id']:
    return {'error':'Treatment Plan belongs to a different cancer episode','plan_id':plan['id'],'plan_episode_id':plan_episode,'order_episode_id':ep['id']},409
   systemic_phases=[x for x in plan.get('data',{}).get('phases',[]) if x.get('modality')=='Systemic Therapy']
   if systemic_phases and not any(str(x.get('status','')).lower() not in ['cancelled','superseded','completed'] for x in systemic_phases):
    return {'error':'The clinician-approved Treatment Plan has no active systemic-therapy phase'},409
   cycle=int(d.get('cycle',1));day=int(d.get('day',1));supersedes_id=str(d.get('supersedes_order_id') or '').strip();supersession_reason=str(d.get('supersession_reason') or '').strip()
   same_cycle=[x for x in many(c,pid,'treatment_order') if x.get('data',{}).get('plan_id')==plan['id'] and int(x.get('data',{}).get('cycle') or 0)==cycle and int(x.get('data',{}).get('day') or 0)==day and not order_is_superseded(c,x) and x.get('status') not in ['Completed','Rejected','Cancelled']]
   if same_cycle and not supersedes_id:return {'error':'An active Treatment Order already exists for this plan/cycle/day. Explicit supersession is required to replace it.','active_order_ids':[x['id'] for x in same_cycle],'requires':['supersedes_order_id','supersession_reason']},409
   old_order=None
   if supersedes_id:
    old_order=get_rec(c,supersedes_id)
    if not old_order or old_order.get('entity_type')!='treatment_order' or old_order.get('patient_id')!=pid:return {'error':'Valid superseded Treatment Order required'},409
    if order_is_superseded(c,old_order) or old_order.get('status') in ['Completed','Rejected','Cancelled']:return {'error':'Only a current uncompleted Treatment Order can be superseded','order_id':supersedes_id,'status':old_order.get('status')},409
    if old_order.get('data',{}).get('plan_id')!=plan['id'] or int(old_order.get('data',{}).get('cycle') or 0)!=cycle or int(old_order.get('data',{}).get('day') or 0)!=day:return {'error':'Superseding order must replace the same Treatment Plan/cycle/day'},409
    old_inf=next((x for x in many(c,pid,'infusion') if x.get('data',{}).get('order_id')==supersedes_id),None)
    if old_inf and (old_inf.get('data',{}).get('mar') or old_inf.get('status') in ['In Progress','Completed']):return {'error':'A Treatment Order with administration already started cannot be superseded; use a governed clinical modification/variance workflow'},409
    if not supersession_reason:return {'error':'Treatment Order supersession requires a documented reason'},409
   latest_mod=latest(c,pid,'modification');mod_id='';
   if ready['data'].get('decision')=='Proceed with Modification' and latest_mod and latest_mod['data'].get('items'):mod_id=latest_mod['data']['items'][-1].get('id','')
   setting=d.get('administration_setting','Day Care')
   if setting not in ['Day Care','Inpatient']:return {'error':'Administration setting must be Day Care or Inpatient'},409
   if setting=='Inpatient':
    adm=latest(c,pid,'admission');active=next((x for x in reversed(adm['data'].get('admissions',[])) if x.get('status')=='Active'),None) if adm else None
    if not active:return {'error':'Active inpatient admission is required before creating an inpatient systemic treatment order'},409
   admission_id=active['id'] if setting=='Inpatient' else ''
   order={'order_no':'ORD-'+uuid.uuid4().hex[:6].upper(),'episode_id':ep['id'],'admission_id':admission_id,'modification_id':d.get('modification_id') or mod_id,'administration_setting':setting,'plan_id':plan['id'],'protocol_id':protocol['id'],'protocol_version':protocol['version'],'regimen':protocol['name'],'content_template_id':template['id'],'content_template_version':template['version'],'content_source_id':template['source_id'],'diagnosis':d.get('diagnosis') or ((latest(c,pid,'diagnosis') or {}).get('data',{}).get('cancer_type','')),'intent':d.get('intent') or template.get('intent') or ((latest(c,pid,'treatment_plan') or {}).get('data',{}).get('intent','')),'line_of_therapy':d.get('line_of_therapy') or template.get('line_of_therapy') or ((latest(c,pid,'treatment_plan') or {}).get('data',{}).get('line_of_therapy','')),'cycle':cycle,'day':day,'planned_cycles':protocol['planned_cycles'],'supersedes_order_id':supersedes_id,'supersession_reason':supersession_reason,'start_date':d.get('start_date',str(date.today())),'patient_snapshot':{'name':pat['name'],'dob':pat['dob'],'mrn':pat['mrn'],'weight_kg':w,'height_cm':intake['data'].get('height_cm'),'bsa_raw_m2':intake['data'].get('bsa_raw_m2'),'bsa_m2':bsa,'bsa_formula':intake['data'].get('bsa_formula'),'bsa_rounding_policy':intake['data'].get('bsa_rounding_policy') or BSA_POLICY,'measurement_units':intake['data'].get('measurement_units',{}),'source_measurements':intake['data'].get('source_measurements',{}),'measured_at':intake['data'].get('measured_at'),'assessor':intake['data'].get('assessor'),'allergies':allergy,'coded_allergies':coded_allergies,'readiness_id':ready['id']},'cumulative_dose_ledger_before_order':cum_before,'items':items,'signed_by':actor(role),'signed_at':now(),'authorization_statement':'I reviewed patient history, labs, allergies, regimen, calculations and treatment criteria and authorize this patient-specific order instantiated from the selected governed regimen version.','locked':True}
   oid=new_record(c,pid,'treatment_order',order,'Verification Pending',role);phid=new_record(c,pid,'pharmacy',{'order_id':oid,'verification_checks':{},'items':[dict(x) for x in items],'query_history':[]},'Verification Pending',role);infid=new_record(c,pid,'infusion',{'order_id':oid,'care_setting':order['administration_setting'],'checklist':{},'mar':[]},'Awaiting Pharmacy',role)
   if old_order:
    update_rec(c,old_order['id'],{'superseded_by_order_id':oid,'superseded_at':now(),'superseded_by':actor(role),'supersession_reason':supersession_reason},'Superseded',role,'ORDER_SUPERSEDED',supersession_reason)
    old_ph=next((x for x in many(c,pid,'pharmacy') if x.get('data',{}).get('order_id')==old_order['id']),None);old_inf=next((x for x in many(c,pid,'infusion') if x.get('data',{}).get('order_id')==old_order['id']),None)
    if old_ph:update_rec(c,old_ph['id'],{'superseded_by_order_id':oid,'supersession_reason':supersession_reason},'Superseded',role,'PHARMACY_ORDER_SUPERSEDED',supersession_reason)
    if old_inf:update_rec(c,old_inf['id'],{'superseded_by_order_id':oid,'supersession_reason':supersession_reason},'Superseded',role,'INFUSION_ORDER_SUPERSEDED',supersession_reason)
   grant_patient_access(c,pid,'Oncology Pharmacy','treatment_order',oid,role);grant_patient_access(c,pid,'Inpatient Oncology Nurse' if setting=='Inpatient' else 'Day Care / Infusion Nurse','treatment_order',oid,role);journey_add(c,pid,'Medical Oncology','Treatment Ordered','Verification Pending',role,'treatment_order',oid,order['regimen'],True);return {'ok':True,'order_id':oid,'pharmacy_id':phid,'infusion_id':infid,'supersedes_order_id':supersedes_id},200
  if a=='pharmacy_decision':
   if role!='Oncology Pharmacy':return {'error':'Oncology Pharmacy required'},403
   if not e or e['entity_type']!='pharmacy':return {'error':'Pharmacy record required'},404
   ordr=get_rec(c,e['data'].get('order_id'));stale=order_current_or_error(c,ordr)
   if stale:return stale
   decision=d.get('decision');checks=d.get('verification_checks') or {};reqchecks=['patient_identity','allergy','regimen_version','cycle_day','dose_basis','calculated_dose','ordered_dose','dose_variance','renal_adjustment','hepatic_adjustment','cumulative_dose','interaction','duplication','route','diluent','final_concentration','stock','expiry'];miss=[x for x in reqchecks if checks.get(x) is not True]
   if decision=='Verified' and miss:return {'error':'Independent verification checklist incomplete','missing':miss},409
   if decision in ['Query','Reject'] and (not d.get('query_reason') or not d.get('message')):return {'error':'Structured reason and message required'},409
   independent=None
   if decision=='Verified':
    tpl=regimen_from_template(c,(ordr or {}).get('data',{}).get('content_template_id') or 'REG-CCA-TCHP-DEMO')
    if not ordr or not tpl:return {'error':'Source treatment order/regimen is unavailable for independent pharmacy recalculation'},409
    independent=order_safety_recalculation(c,pid,ordr,tpl['data'])
    if not independent['ok']:return {'error':'Independent pharmacy dose recalculation failed','safety_errors':independent['errors'],'independent_verification':independent},409
   ready=get_rec(c,ordr.get('data',{}).get('readiness_id') or ordr.get('data',{}).get('patient_snapshot',{}).get('readiness_id','')) if ordr else None
   verification_snapshot={'order_id':ordr['id'] if ordr else '', 'order_version':ordr.get('version') if ordr else None,'protocol_id':ordr.get('data',{}).get('protocol_id') if ordr else '', 'protocol_version':ordr.get('data',{}).get('protocol_version') if ordr else '', 'cycle':ordr.get('data',{}).get('cycle') if ordr else None,'day':ordr.get('data',{}).get('day') if ordr else None,'readiness_id':ready.get('id') if ready else '', 'readiness_signed_at':ready.get('data',{}).get('signed_at') if ready else '', 'readiness_decision':ready.get('data',{}).get('decision') if ready else '', 'cumulative_dose_ledger':ordr.get('data',{}).get('cumulative_dose_ledger_before_order',{}) if ordr else {}, 'patient_snapshot':ordr.get('data',{}).get('patient_snapshot',{}) if ordr else {}}
   patch={'verification_checks':checks,'verification_snapshot':verification_snapshot,'independent_recalculation':independent,'decision':decision,'verified_actor':actor(role),'verified_at':now(),'verification_attestation':'I independently verified the current signed order, readiness evidence, dosing, organ-function context, cumulative exposure, route/diluent and preparation prerequisites.'}
   if decision in ['Query','Reject']:
    hist=list(e['data'].get('query_history',[]));hist.append({'at':now(),'by':actor(role),'decision':decision,'reason':d['query_reason'],'message':d['message'],'resolved':False});patch['query_history']=hist;st='Queried' if decision=='Query' else 'Rejected'
   elif decision=='Verified':st='Preparation Pending'
   else:return {'error':'Invalid decision'},409
   update_rec(c,e['id'],patch,st,role,'PHARMACY_DECISION',decision);ordr=get_rec(c,e['data'].get('order_id'));update_rec(c,ordr['id'],{},'Verification Pending' if st=='Queried' else ('Verified' if st=='Preparation Pending' else 'Rejected'),role,'ORDER_PHARMACY_STATE') if ordr else None;journey_add(c,pid,'Oncology Pharmacy','Pharmacy Verification',st,role,'pharmacy',e['id'],decision,True);return {'ok':True,'status':st},200
  if a=='oncologist_query_response':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   order=e if e and e['entity_type']=='treatment_order' else None
   if not order:return {'error':'Treatment order required'},404
   ph=next((x for x in many(c,pid,'pharmacy') if x['data'].get('order_id')==order['id']),None)
   if not ph or ph['status']!='Queried':return {'error':'No active pharmacy query'},409
   hist=list(ph['data'].get('query_history',[]));
   for q in reversed(hist):
    if not q.get('resolved'):q.update({'resolved':True,'resolved_at':now(),'resolved_by':actor(role),'response_action':d.get('response_action'),'response_note':d.get('response_note')});break
   update_rec(c,ph['id'],{'query_history':hist},'Verification Pending',role,'PHARMACY_QUERY_RESPONSE');return {'ok':True},200
  if a=='pharmacy_prepare':
   if role!='Oncology Pharmacy':return {'error':'Oncology Pharmacy required'},403
   if not e or e['entity_type']!='pharmacy' or e['status']!='Preparation Pending':return {'error':'Verified pharmacy record required'},409
   stale=order_current_or_error(c,get_rec(c,e['data'].get('order_id')))
   if stale:return stale
   fmap=active_formulary_map(c);items=d.get('items') or []
   if len(items)!=len(e['data'].get('items',[])):return {'error':'All ordered items must be represented in preparation'},409
   prepared_at=now(); prepared_dt=datetime.fromisoformat(prepared_at)
   prepared_items=[]
   for i0 in items:
    i=dict(i0);fi=fmap.get(i.get('drug')) or fmap.get(i.get('code'));form=i.get('formulation');strength=i.get('formulation_strength_mg');rule=PHARMACY_PREP_RULES.get(i.get('code'))
    if not fi:return {'error':f"No governed formulary item for {i.get('drug')}"},409
    if not any(f['label']==form and float(f.get('strength_mg',0))==float(strength or 0) for f in fi.get('formulations',[])):return {'error':f"Select governed formulation/strength for {i.get('drug')}"},409
    if i.get('route') not in fi.get('allowed_routes',[]):return {'error':f"Route not allowed for {i.get('drug')}"},409
    if i.get('diluent') and i.get('diluent') not in fi.get('allowed_diluents',[]):return {'error':f"Diluent not allowed for {i.get('drug')}"},409
    if not i.get('batch') or not i.get('expiry'):return {'error':f"Batch and expiry required for {i.get('drug')}"},409
    av=safe_float(i.get('actual_volume_ml')); avu=i.get('actual_volume_unit')
    # Preparation volume is conditionally required for IV/compounded liquid items.
    # Non-IV solid/self-administered items do not invent a preparation volume.
    if i.get('route')=='IV':
     if av is None or av<=0 or avu!='mL':return {'error':f"Actual measured preparation volume with explicit mL unit required for {i.get('drug')}"},409
    else:
     if av is None: av=0.0
     if av<0:return {'error':f"Preparation volume cannot be negative for {i.get('drug')}"},409
     if av>0 and avu!='mL':return {'error':f"Any measured preparation volume requires explicit mL unit for {i.get('drug')}"},409
    if not rule:return {'error':f"CCA-approved Pharmacy preparation rule is not configured for {i.get('drug')}",'clinical_content_status':'NEEDS CCA PHARMACY DECISION'},409
    try:
     if date.fromisoformat(str(i.get('expiry'))[:10])<=date.today():return {'error':f"Expired/invalid batch cannot be prepared for {i.get('drug')}"},409
    except:return {'error':f"Valid expiry date required for {i.get('drug')}"},409
    # BUD/use-before is system-derived from the governed stability duration; client values are ignored.
    bud=(prepared_dt+timedelta(hours=float(rule['stability_hours']))).isoformat()
    ordered=safe_float(i.get('ordered_dose')); final_conc=round(ordered/av,6) if ordered is not None and av>0 and i.get('route')=='IV' else None
    waste=safe_float(i.get('wastage_amount')) or 0.0;wunit=str(i.get('wastage_unit') or '').strip();wreason=i.get('wastage_reason')
    if waste<0:return {'error':f"Wastage cannot be negative for {i.get('drug')}"},409
    if waste>0 and (not wunit or wreason not in VALUE_SETS['pharmacy_wastage_reason']):return {'error':f"Wastage requires explicit unit and governed reason for {i.get('drug')}",'allowed_reasons':VALUE_SETS['pharmacy_wastage_reason']},409
    i.update({'prepared_by':actor(role),'prepared_at':prepared_at,'compatibility_status':rule['compatibility_status'],'stability_reference':rule['stability_reference'],'stability_hours':rule['stability_hours'],'beyond_use_at':bud,'storage_condition':rule['storage_condition'],'light_protection':rule['light_protection'],'filter_requirement':rule['filter_requirement'],'container_requirement':rule['container_requirement'],'final_concentration':final_conc,'final_concentration_unit':'mg/mL' if final_conc is not None else 'Not applicable','pharmacy_content_status':'Synthetic QA — CCA Pharmacy must replace/approve preparation rules','wastage_amount':waste,'wastage_unit':wunit,'wastage_reason':wreason or ''})
    prepared_items.append(i)
   update_rec(c,e['id'],{'items':prepared_items,'preparation_note':d.get('preparation_note',''),'prepared_at':prepared_at,'prepared_by':actor(role)},'Dispensing Pending',role,'PHARMACY_PREPARE');return {'ok':True,'status':'Dispensing Pending','prepared_at':prepared_at},200
  if a=='pharmacy_release':
   if role!='Oncology Pharmacy':return {'error':'Oncology Pharmacy required'},403
   if not e or e['entity_type']!='pharmacy' or e['status']!='Dispensing Pending':return {'error':'Prepared record required'},409
   stale=order_current_or_error(c,get_rec(c,e['data'].get('order_id')))
   if stale:return stale
   # Preserve the server-governed preparation record. The client may submit only
   # final-check attestations keyed by item_id; it cannot overwrite BUD, stability,
   # compatibility, concentration, batch, expiry or prepared-by provenance.
   prepared_items=[dict(x) for x in e['data'].get('items',[])]
   submitted={x.get('item_id'):x for x in (d.get('items') or []) if isinstance(x,dict) and x.get('item_id')}
   items=[];checked_at=now()
   for base in prepared_items:
    i=dict(base); att=submitted.get(i.get('item_id'),{})
    second=att.get('second_check_by'); label_ok=att.get('label_verified') is True
    if not second or not label_ok:return {'error':f"Independent final check required for {i.get('drug')}"},409
    prepared_name=(i.get('prepared_by') or {}).get('name') if isinstance(i.get('prepared_by'),dict) else i.get('prepared_by')
    if second==prepared_name:return {'error':'Preparer cannot be the independent second checker'},409
    i.update({'second_check_by':second,'label_verified':True,'second_check_role':'Oncology Pharmacy','second_checked_at':checked_at,'second_check_attestation':'Independent final product/label check completed.'})
    items.append(i)
   dest=d.get('dispensed_to');
   if not dest:return {'error':'Dispense destination required'},409
   ordr=get_rec(c,e['data'].get('order_id'))
   setting=(ordr['data'].get('administration_setting','Day Care') if ordr else 'Day Care')
   if setting=='Inpatient' and 'inpatient' not in str(dest).lower() and 'ward' not in str(dest).lower():return {'error':'Inpatient treatment must be released to an inpatient destination'},409
   update_rec(c,e['id'],{'items':items,'dispensed_to':dest,'manifest_no':d.get('manifest_no',''),'dispensed_at':now(),'released_by':actor(role)},'Dispensed',role,'PHARMACY_RELEASE');inf=next((x for x in many(c,pid,'infusion') if x['data'].get('order_id')==e['data'].get('order_id')),None);update_rec(c,inf['id'],{},'Ready for Verification',role,'INFUSION_READY') if inf else None;return {'ok':True,'status':'Dispensed'},200
  if a=='start_infusion':
   if not e or e['entity_type']!='infusion':return {'error':'Infusion record required'},404
   care_setting=e['data'].get('care_setting','Day Care');allowed_role='Inpatient Oncology Nurse' if care_setting=='Inpatient' else 'Day Care / Infusion Nurse'
   if role!=allowed_role:return {'error':f'{allowed_role} required for {care_setting} administration'},403
   order=get_rec(c,e['data'].get('order_id'));stale=order_current_or_error(c,order)
   if stale:return stale
   ph=next((x for x in many(c,pid,'pharmacy') if x['data'].get('order_id')==order['id']),None) if order else None
   if not order or order['status']!='Verified' or not order['data'].get('signed_at') or not ph or ph['status']!='Dispensed':return {'error':'Signed, pharmacy-verified order and pharmacy release required'},409
   # Clinical prerequisites are verified from server records, not accepted as client checkboxes alone.
   consent=latest(c,pid,'consent');valid_treatment_consent=any(x.get('status')=='Signed' and x.get('type')=='Treatment Consent' for x in (consent['data'].get('items',[]) if consent else []))
   if not valid_treatment_consent:return {'error':'Current signed Treatment Consent is required'},409
   ready=get_rec(c,order['data'].get('readiness_id') or order['data'].get('patient_snapshot',{}).get('readiness_id',''))
   ord_template=regimen_from_template(c,order['data'].get('content_template_id') or 'REG-CCA-TCHP-DEMO');rev=(ready['data'].get('protocol_evaluation') if ready else None) or readiness_eval(ready['data'] if ready else {},ord_template['data'] if ord_template else PROTOCOL)
   if not ready or ready['status']!='Signed' or ready['data'].get('decision') not in ['Proceed as Planned','Proceed with Modification'] or rev.get('blockers'):return {'error':'Current signed treatment readiness without blockers is required','blockers':rev.get('blockers',[])},409
   ident=d.get('identity_confirmation') or {};pat=patient(c,pid);matches=sum([str(ident.get('name','')).strip().lower()==str(pat['name']).strip().lower(),str(ident.get('mrn','')).strip()==str(pat['mrn']).strip(),str(ident.get('dob','')).strip()==str(pat['dob']).strip()])
   if matches<2:return {'error':'Two matching patient identifiers are required before administration'},409
   checks=d.get('checklist') or {};need=['identity','order','consent','allergy','vitals','labs','access','pharmacy'];miss=[x for x in need if checks.get(x) is not True]
   if miss:return {'error':'Pre-administration checklist incomplete','missing':miss},409
   access=d.get('access') or {};
   if not isinstance(access,dict) or access.get('type') not in VALUE_SETS['access_type'] or access.get('site') not in VALUE_SETS['access_site']:return {'error':'Administration requires governed access type and site','allowed_types':VALUE_SETS['access_type'],'allowed_sites':VALUE_SETS['access_site']},409
   pv=d.get('pre_vitals') or {};pvu=pv.get('units') or {}
   if pv and any(not pvu.get(k) for k in ['bp','hr','rr','temp','spo2']):return {'error':'Pre-administration measured vitals require explicit units'},409
   update_rec(c,e['id'],{'checklist':checks,'identity_confirmation':ident,'pre_vitals':pv,'access':access,'bedside_verification':d.get('bedside_verification',{}),'started_at':now(),'started_by':actor(role)},'In Progress',role,'INFUSION_START');setting=e['data'].get('care_setting','Day Care');journey_add(c,pid,'Inpatient Care' if setting=='Inpatient' else 'Day Care / Infusion','Systemic Therapy Administration','In Progress',role,'infusion',e['id'],setting,True);return {'ok':True},200
  if a=='administer_item':
   if not e or e['entity_type']!='infusion' or e['status']!='In Progress':return {'error':'Active infusion required'},409
   care_setting=e['data'].get('care_setting','Day Care');allowed_role='Inpatient Oncology Nurse' if care_setting=='Inpatient' else 'Day Care / Infusion Nurse'
   if role!=allowed_role:return {'error':f'{allowed_role} required for {care_setting} administration'},403
   order=get_rec(c,e['data'].get('order_id'));stale=order_current_or_error(c,order)
   if stale:return stale
   items=sorted(order['data'].get('items',[]),key=lambda x:x['sequence']);mar=list(e['data'].get('mar',[]));r=d.get('record') or {};item=next((x for x in items if x['item_id']==r.get('item_id')),None)
   if not item:return {'error':'Order item not found'},404
   if any(x.get('item_id')==item['item_id'] for x in mar):return {'error':'Duplicate administration detected'},409
   expected=items[len(mar)] if len(mar)<len(items) else None
   if not expected or expected['item_id']!=item['item_id']:return {'error':'Medication sequence violation'},409
   if float(r.get('actual_dose',-1))<0:return {'error':'Actual administered dose required'},409
   actual_unit=str(r.get('actual_dose_unit') or '').strip(); ordered_unit=str(item.get('ordered_unit') or '').strip()
   if not actual_unit:return {'error':'Actual administered dose requires an explicit unit selection'},409
   if actual_unit!=ordered_unit:return {'error':'Actual administered dose unit must match the signed order unit in this prototype','actual_unit':actual_unit,'ordered_unit':ordered_unit},409
   actual=float(r.get('actual_dose'));ordered=float(item.get('ordered_dose',0));completion=r.get('completion_status','Administered')
   if completion not in VALUE_SETS['completion_status']:return {'error':'Administration completion status must use the governed value set','allowed':VALUE_SETS['completion_status']},409
   variance_type=r.get('variance_type') or ('Dose variance' if abs(actual-ordered)>1e-9 else 'None');variance_reason_code=r.get('variance_reason_code')
   if variance_type not in VALUE_SETS['mar_variance_type']:return {'error':'Administration variance type must use the governed value set','allowed':VALUE_SETS['mar_variance_type']},409
   needs_variance=abs(actual-ordered)>1e-9 or completion in ['Partially Administered','Held','Stopped','Not Administered','Cancelled'] or variance_type!='None'
   if needs_variance and variance_reason_code not in VALUE_SETS['mar_variance_reason']:return {'error':'Administration variance requires a governed reason code','allowed':VALUE_SETS['mar_variance_reason']},409
   if item.get('route')=='IV' or float(item.get('rate_ml_hr') or 0)>0:
    ar=safe_float(r.get('actual_rate')); aru=str(r.get('actual_rate_unit') or '').strip()
    if ar is None or ar<0 or aru!='mL/h':return {'error':'IV administration requires actual rate with explicit mL/h unit'},409
   if needs_variance and not str(r.get('reason') or r.get('variance_note') or '').strip():return {'error':'Administration variance/incomplete status requires narrative documentation in addition to the governed reason code'},409
   if item.get('group') in ['Antineoplastic','Targeted Therapy']:
    cv=r.get('chairside_verification') or {};cks=cv.get('checks') or {};need=['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings'];miss=[x for x in need if cks.get(x) is not True]
    if not cv.get('verified_by') or miss:return {'error':'Independent chairside verification incomplete','missing':miss},409
    if cv.get('verified_by')==actor(role).get('name'):return {'error':'Chairside verifier must be a separately named verifier in this prototype'},409
    cv.update({'verified_role':'Day Care / Infusion Nurse','verified_at':now(),'attestation':'Independent chairside check completed against the current signed order and prepared product.'});r['chairside_verification']=cv
   r.update({'drug':item['drug'],'code':item.get('code'),'sequence':item['sequence'],'ordered_dose':item['ordered_dose'],'ordered_unit':item['ordered_unit'],'actual_dose_unit':actual_unit,'unit':actual_unit,'route':item['route'],'variance_type':variance_type,'variance_reason_code':variance_reason_code or '','administered_by':actor(role),'recorded_at':now()});mar.append(r);update_rec(c,e['id'],{'mar':mar},'In Progress',role,'MAR_ITEM',item['drug']);return {'ok':True,'count':len(mar)},200
  if a=='escalate_to_ipd':
   if role!='Day Care / Infusion Nurse':return {'error':'Day Care / Infusion Nurse required'},403
   inf=e if e and e['entity_type']=='infusion' else latest(c,pid,'infusion')
   if not inf or inf['status'] not in ['In Progress','Held','Stopped']:return {'error':'Active/held infusion required for escalation'},409
   reason_code=d.get('reason_code') or 'Adverse drug reaction'
   if reason_code not in VALUE_SETS['admission_reason']:return {'error':'Governed admission reason required','allowed':VALUE_SETS['admission_reason']},409
   adm=latest(c,pid,'admission');active=[x for x in adm['data'].get('admissions',[]) if x.get('status')=='Active'] if adm else []
   if active:return {'error':'Patient already has an active admission','admission_id':active[-1]['id']},409
   ep=current_episode(c,pid) or ensure_episode(c,pid,role)
   x={'id':'ADM-'+uuid.uuid4().hex[:8].upper(),'episode_id':ep['id'],'admission_type':'Emergency','reason_code':reason_code,'reason_note':d.get('reason_note','Infusion reaction requiring inpatient escalation'),'admitting_specialty':'Medical Oncology','attending_clinician':d.get('attending_clinician','On-call Medical Oncology'),'admitted_at':d.get('admitted_at') or now(),'ward':d.get('ward','Emergency / Unassigned'),'bed':d.get('bed','Unassigned'),'source_context':'Day Care infusion '+inf['id'],'status':'Active','created_by':actor(role)}
   rows=list(adm['data'].get('admissions',[]));rows.append(x);update_rec(c,adm['id'],{'admissions':rows},'Active',role,'DAYCARE_TO_IPD',reason_code);grant_patient_access(c,pid,'Inpatient Oncology Nurse','admission',x['id'],role)
   update_rec(c,inf['id'],{'escalated_to_admission_id':x['id'],'escalation_reason':reason_code,'escalated_at':now(),'escalated_by':actor(role)},'Held' if inf['status']=='In Progress' else inf['status'],role,'INFUSION_ESCALATE_IPD',reason_code)
   journey_add(c,pid,'Inpatient Care','Emergency admission from Day Care','Active',role,'admission',x['id'],reason_code,True);return {'ok':True,'admission':x},200
  if a=='complete_infusion':
   if not e or e['entity_type']!='infusion' or e['status']!='In Progress':return {'error':'Active infusion required'},409
   care_setting=e['data'].get('care_setting','Day Care');allowed_role='Inpatient Oncology Nurse' if care_setting=='Inpatient' else 'Day Care / Infusion Nurse'
   if role!=allowed_role:return {'error':f'{allowed_role} required for {care_setting} administration'},403
   order=get_rec(c,e['data'].get('order_id'));stale=order_current_or_error(c,order)
   if stale:return stale
   mar=e['data'].get('mar',[])
   if len(mar)!=len(order['data'].get('items',[])):return {'error':'Every ordered item needs final MAR status before cycle completion'},409
   if not d.get('post_vitals') or not d.get('tolerance') or not d.get('discharge_instructions'):return {'error':'Post-treatment vitals, tolerance and discharge instructions required'},409
   pv=d.get('post_vitals') or {};units=pv.get('units') or {};
   if any(units.get(k) in [None,''] for k in ['bp','hr','rr','temp','spo2']):return {'error':'Post-treatment measured vitals require explicit units for BP, HR, RR, temperature and SpO2'},409
   completed_at=now();cum_after=cumulative_administered_by_code(c,pid)
   update_rec(c,e['id'],{'post_vitals':pv,'tolerance':d['tolerance'],'discharge_instructions':d['discharge_instructions'],'next_cycle':d.get('next_cycle',''),'completed_at':completed_at,'completed_by':actor(role),'cumulative_dose_ledger_after':cum_after},'Completed',role,'INFUSION_COMPLETE');update_rec(c,order['id'],{'administration_completed_at':completed_at,'administration_record_id':e['id'],'cumulative_dose_ledger_after_administration':cum_after},'Completed',role,'ORDER_EXECUTION_COMPLETE');hist=latest(c,pid,'treatment_history');eps=list(hist['data'].get('episodes',[]));eps.append({'type':'Systemic Therapy Administration','order_id':order['id'],'regimen':order['data']['regimen'],'cycle':order['data']['cycle'],'day':order['data']['day'],'date':completed_at,'status':'Completed','actual_items':mar,'cumulative_dose_ledger_after':cum_after});update_rec(c,hist['id'],{'episodes':eps},'Active',role,'HISTORY_APPEND');journey_add(c,pid,'Inpatient Care' if care_setting=='Inpatient' else 'Day Care / Infusion','Cycle Completed','Completed',role,'infusion',e['id'],d.get('next_cycle',''),True)
   # PC8.0 connected-workflow task handoff: close this administration's task and open
   # Medical Oncology's next-cycle decision task (consumed by post_cycle_review).
   complete_open_tasks(c,pid,role,'Treatment administration',source_type='treatment_order',source_id=order['id'],completed_by=role);handoff(c,pid,'Medical Oncology','Post-cycle decision after treatment administration','Next-cycle decision','infusion',e['id'],role,'High',d.get('tolerance',''),{'infusion_id':e['id'],'order_id':order['id'],'cumulative_dose_ledger_after':cum_after})
   return {'ok':True,'order_status':'Completed','cumulative_dose_ledger_after':cum_after},200
  if a=='record_toxicity':
   if role not in ['Medical Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Nurse Navigator']:return {'error':'Clinical role required'},403
   e=must('toxicity');d={**d}
   # UI-friendly aliases are normalized into the canonical toxicity fields.
   if not d.get('term') and d.get('toxicity_type'):d['term']=d['toxicity_type']
   if not d.get('attribution') and d.get('relationship'):d['attribution']=d['relationship']
   req=['term','grade','onset_date','attribution','outcome'];miss=[x for x in req if not d.get(x)]
   if miss:return {'error':'Toxicity fields missing','missing':miss},409
   if str(d['grade']) not in VALUE_SETS['ctcae_grade']:return {'error':'CTCAE grade must be 1–5'},409
   serious=d.get('seriousness') or {};sae=bool(d.get('sae')) or any(bool(serious.get(k)) for k in ['death','life_threatening','hospitalization','disability','congenital_anomaly','other_medically_important'])
   last_completed=next((o for o in reversed(many(c,pid,'treatment_order')) if o['status']=='Completed'),None);cycle=d.get('cycle') or ((last_completed or {}).get('data',{}).get('cycle'))
   xs=list(e['data'].get('events',[]));x={'id':'TOX-'+uuid.uuid4().hex[:7].upper(),**d,'toxicity_type':d.get('term'),'relationship':d.get('attribution'),'ctcae_version':CTCAE_VERSION,'seriousness':serious,'sae':sae,'suspected_agents':d.get('suspected_agents',[]),'cycle':cycle,'recorded_by':actor(role),'recorded_at':now()};xs.append(x);update_rec(c,e['id'],{'ctcae_version':CTCAE_VERSION,'events':xs},'Active',role,'TOXICITY_RECORD');journey_add(c,pid,'Medical Oncology','Toxicity Review','Active',role,'toxicity',e['id'],f"{x.get('term')} Grade {x.get('grade')}",True);return {'ok':True,'id':x['id'],'cycle':cycle,'sae':sae},200
  if a=='create_modification':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   e=must('modification');req=['original_order_id','reason','modification_type','clinical_justification'];miss=[x for x in req if not d.get(x)]
   if miss:return {'error':'Modification incomplete','missing':miss},409
   xs=list(e['data'].get('items',[]));x={'id':'MOD-'+uuid.uuid4().hex[:7].upper(),**d,'approved_by':actor(role),'approved_at':now()};xs.append(x);update_rec(c,e['id'],{'items':xs},'Active',role,'MODIFICATION_CREATE');return {'ok':True,'id':x['id']},200
  if a=='save_response':
   if role not in ['Medical Oncology','Radiologist']:return {'error':'Medical Oncology/Radiologist required'},403
   e=must('response');ass=list(e['data'].get('assessments',[]));les=d.get('target_lesions') or [];new_les=bool(d.get('new_lesions'))
   if not d.get('date') or not les:return {'error':'Scan date and target lesion measurements required'},409
   if len(les)>5:return {'error':'RECIST 1.1 permits at most 5 target lesions in total'},409
   organ_counts={}
   for x in les:
    org=str(x.get('organ') or '').strip() or 'Unspecified';organ_counts[org]=organ_counts.get(org,0)+1
    if organ_counts[org]>2:return {'error':f'RECIST 1.1 permits at most 2 target lesions per organ ({org})'},409
    if str(x.get('lesion_type') or 'Non-nodal')=='Lymph node' and x.get('baseline_selected') is True:
     sz=safe_float(x.get('size') if x.get('size') not in [None,''] else x.get('size_mm'))
     szmm=sz*10 if str(x.get('unit'))=='cm' and sz is not None else sz
     if szmm is None or szmm<15:return {'error':'A target lymph node must have short axis ≥15 mm at baseline'},409
   norm=[]
   for x in les:
    y=dict(x);unit=y.get('unit');raw=y.get('size') if y.get('size') not in [None,''] else y.get('size_mm')
    if unit in [None,''] and y.get('size_mm') not in [None,'']:unit='mm'  # compatibility: size_mm is an explicitly canonical field
    if unit not in ['mm','cm']:return {'error':'Every target lesion requires explicit mm or cm unit'},409
    try:v=float(raw)
    except:return {'error':'Target lesion measurement must be numeric'},409
    if v<0:return {'error':'Target lesion measurement cannot be negative'},409
    y['source_value']=v;y['source_unit']=unit;y['size_mm']=round(v*10 if unit=='cm' else v,4);norm.append(y)
   baseline=sum(float(x['size_mm']) for x in e['data'].get('baseline',{}).get('target_lesions',[]));curr=round(sum(float(x['size_mm']) for x in norm),4);nadir=min([baseline]+[float(x.get('sum_mm',baseline)) for x in ass if x.get('sum_mm') is not None]) if baseline else curr
   pct=round(((curr-baseline)/baseline)*100,3) if baseline else None
   if new_les:cat='Progressive disease'
   elif baseline and curr<=baseline*0.70:cat='Partial response'
   elif nadir and curr>=nadir*1.20 and curr-nadir>=5:cat='Progressive disease'
   else:cat='Stable disease'
   epid=d.get('episode_id') or ((current_episode(c,pid) or {}).get('id'));aid='RESP-'+uuid.uuid4().hex[:6].upper()
   x={'id':aid,'episode_id':epid,'criteria_set':d.get('criteria_set','RECIST 1.1'),'criteria_version':d.get('criteria_version','1.1'),'date':d['date'],'source_imaging_id':d.get('source_imaging_id',''),'target_lesions':norm,'sum_mm':curr,'baseline_sum_mm':baseline,'nadir_sum_mm':nadir,'percent_change_from_baseline':pct,'non_target':d.get('non_target',''),'new_lesions':new_les,'proposed_response_category':cat,'response_category':'','confirmation_status':'Pending clinician confirmation','biomarkers':d.get('biomarkers',[]),'notes':d.get('notes',''),'measured_by':actor(role),'measured_at':now()};ass.append(x);update_rec(c,e['id'],{'assessments':ass},'Active',role,'RESPONSE_MEASUREMENT');handoff(c,pid,'Medical Oncology','Confirm proposed RECIST response category','Response confirmation','response',e['id'],role,'High','Radiologist proposed '+cat,{'assessment_id':aid,'proposed_category':cat});return {'ok':True,'proposed_category':cat,'assessment':x},200
  if a=='confirm_response':
   if role!='Medical Oncology':return {'error':'Medical Oncology required to confirm response'},403
   e=must('response');ass=list(e['data'].get('assessments',[]));aid=d.get('assessment_id');x=next((z for z in ass if z.get('id')==aid),None)
   if not x:return {'error':'Response assessment not found'},404
   if x.get('confirmation_status')=='Confirmed':return {'error':'Confirmed response is immutable; create a new assessment for changed evidence'},409
   cat=d.get('response_category');reason=str(d.get('reason') or '').strip()
   if cat not in RESPONSE_CATEGORIES or not reason:return {'error':'Governed response category and clinician reason required','allowed':RESPONSE_CATEGORIES},409
   x.update({'response_category':cat,'confirmation_status':'Confirmed','confirmation_reason':reason,'confirmed_by':actor(role),'confirmed_at':now()});update_rec(c,e['id'],{'assessments':ass},'Active',role,'RESPONSE_CONFIRM',reason);complete_open_tasks(c,pid,role,'Response confirmation',source_type='response',source_id=e['id'],completed_by=role);return {'ok':True,'assessment':x},200
  if a=='rt_save_prescription':
   if role!='Radiation Oncology':return {'error':'Radiation Oncology required'},403
   e=must('radiation');p={**e['data'].get('prescription',{}),**d};sign=bool(d.get('sign'));p.pop('sign',None)
   req=['site','laterality','intent','modality','technique','energy','treatment_phase','total_dose_gy','dose_per_fraction_gy','fractions','frequency','planned_start','target_volumes','organs_at_risk','oar_constraints','simulation_requirement','image_guidance'];miss=[x for x in req if p.get(x) in ['',None,[]]]
   if sign and miss:return {'error':'RT prescription incomplete','missing':miss},409
   try:
    total=float(p.get('total_dose_gy'));per=float(p.get('dose_per_fraction_gy'));n=int(p.get('fractions'));expected=round(per*n,4)
    if sign and abs(total-expected)>0.01:return {'error':'RT prescription arithmetic does not reconcile','total_dose_gy':total,'dose_per_fraction_gy':per,'fractions':n,'expected_total_gy':expected},409
   except Exception:
    if sign:return {'error':'Valid RT dose/fraction arithmetic required'},409
   old_rx=dict(e['data'].get('prescription',{}));old_ver=int(old_rx.get('prescription_version') or 1);old_signed=old_rx.get('status')=='RT Oncologist Approved'
   material_keys=['site','laterality','intent','modality','technique','total_dose_gy','dose_per_fraction_gy','fractions','frequency','planned_start','target_volumes','organs_at_risk','oar_constraints','image_guidance']
   changed=any(p.get(k)!=old_rx.get(k) for k in material_keys)
   if old_signed and changed:
    hist=list(e['data'].get('prescription_history',[]));hist.append(old_rx);p['prescription_version']=old_ver+1
   else:
    hist=list(e['data'].get('prescription_history',[]));p['prescription_version']=old_ver
   if sign:p.update({'status':'RT Oncologist Approved','signed_by':actor(role),'signed_at':now()});st='RT Oncologist Approved'
   else:st='Draft';p['status']='Draft'
   planning=dict(e['data'].get('planning',{}))
   if old_signed and changed:
    phist=list(e['data'].get('planning_history',[]));
    if planning:phist.append(planning)
    planning={'plan_version':int(planning.get('plan_version') or 1)+1,'prescription_version':p['prescription_version'],'simulation_status':planning.get('simulation_status','Pending'),'contouring_status':'Pending','planning_status':'Pending','physics_qa':'Pending','physics_qa_plan_version':None,'physician_final_approval':'Pending','physician_approval_plan_version':None,'dicom_refs':planning.get('dicom_refs',{})}
   else:phist=list(e['data'].get('planning_history',[]));planning.setdefault('plan_version',1);planning['prescription_version']=p['prescription_version']
   epid=d.get('episode_id') or e['data'].get('episode_id') or ((current_episode(c,pid) or ensure_episode(c,pid,role))['id']);data={**e['data'],'episode_id':epid,'prescription':p,'prescription_history':hist,'planning':planning,'planning_history':phist};update_rec(c,e['id'],data,st,role,'RT_PRESCRIPTION')
   if sign:
    grant_patient_access(c,pid,'Radiation Physicist','rt_prescription',e['id'],role);grant_patient_access(c,pid,'Radiation Technologist','rt_prescription',e['id'],role);journey_add(c,pid,'Radiation Oncology','RT Prescription',st,role,'radiation',e['id'],p.get('site',''),True)
   return {'ok':True,'status':st},200
  if a=='rt_planning_status':
   if role not in ['Radiation Oncology','Radiation Physicist']:return {'error':'Radiation Oncology or Radiation Physicist required'},403
   e=must('radiation');plan={**e['data'].get('planning',{})};rx=e['data'].get('prescription',{});rxv=int(rx.get('prescription_version') or 1);planv=int(plan.get('plan_version') or 1)
   supplied=d.get('plan_version')
   if supplied in [None,'']:return {'error':'Current RT plan_version is required for version-safe approval/update','current_plan_version':planv},409
   try:supplied=int(supplied)
   except:return {'error':'plan_version must be an integer','current_plan_version':planv},409
   if supplied!=planv:return {'error':'RT plan version changed since it was loaded','expected_plan_version':supplied,'current_plan_version':planv},409
   if role=='Radiation Physicist':
    if 'physician_final_approval' in d:return {'error':'Radiation Physicist cannot grant physician final approval'},403
    if plan.get('simulation_status')!='Completed' or plan.get('contouring_status')!='Completed' or plan.get('planning_status')!='Planning Complete':return {'error':'Simulation, contouring and plan preparation must be complete before Physics QA','planning':{'simulation_status':plan.get('simulation_status'),'contouring_status':plan.get('contouring_status'),'planning_status':plan.get('planning_status')}},409
    qa=d.get('physics_qa')
    if qa not in ['Approved','Rejected / Replan Required']:return {'error':'Physics QA decision required'},409
    if not d.get('physics_qa_note'):return {'error':'Physics QA note required'},409
    plan.update({'physics_qa':qa,'physics_qa_note':d.get('physics_qa_note'),'physics_qa_by':actor(role),'physics_qa_at':now(),'physics_qa_plan_version':planv,'physics_qa_prescription_version':rxv})
    st='Planning' if qa!='Approved' else e['status']
   else:
    # Material planning change after QA/approval creates an explicit new plan version and invalidates approvals.
    material={k:v for k,v in d.items() if k in ['simulation_status','contouring_status','planning_status','dicom_refs','plan_note']}
    changing=any(material.get(k)!=plan.get(k) for k in material)
    if changing and (plan.get('physics_qa')=='Approved' or plan.get('physician_final_approval')=='Approved'):
     hist=list(e['data'].get('planning_history',[]));hist.append(plan);plan={**plan,**material,'plan_version':planv+1,'prescription_version':rxv,'physics_qa':'Pending','physics_qa_plan_version':None,'physics_qa_by':None,'physics_qa_at':None,'physician_final_approval':'Pending','physician_approval_plan_version':None,'physician_approval_by':None,'physician_approval_at':None};update_rec(c,e['id'],{'planning':plan,'planning_history':hist},'Planning',role,'RT_PLAN_NEW_VERSION','Material plan revision invalidated prior approvals');return {'ok':True,'status':'Planning','plan_version':planv+1,'approvals_reset':True},200
    plan.update(material)
    if d.get('physician_final_approval')=='Approved':
     if plan.get('physics_qa')!='Approved' or int(plan.get('physics_qa_plan_version') or 0)!=planv or int(plan.get('physics_qa_prescription_version') or 0)!=rxv:return {'error':'Current plan version requires current Physics QA before Radiation Oncologist final approval','current_plan_version':planv,'prescription_version':rxv},409
     plan.update({'physician_final_approval':'Approved','physician_approval_by':actor(role),'physician_approval_at':now(),'physician_approval_plan_version':planv,'physician_approval_prescription_version':rxv})
    elif 'physician_final_approval' in d:plan['physician_final_approval']=d.get('physician_final_approval')
    st=d.get('status') or e['status']
    if st=='Ready for Treatment':
     valid_physics=plan.get('physics_qa')=='Approved' and int(plan.get('physics_qa_plan_version') or 0)==planv and int(plan.get('physics_qa_prescription_version') or 0)==rxv
     valid_ro=plan.get('physician_final_approval')=='Approved' and int(plan.get('physician_approval_plan_version') or 0)==planv and int(plan.get('physician_approval_prescription_version') or 0)==rxv
     if not (valid_physics and valid_ro):return {'error':'Current RT plan/prescription version requires both current Physics QA and Radiation Oncologist final approval before Treatment Ready','plan_version':planv,'prescription_version':rxv},409
   update_rec(c,e['id'],{'planning':plan},st,role,'RT_PLANNING');return {'ok':True,'status':st,'plan_version':int(plan.get('plan_version') or 1),'prescription_version':rxv},200
  if a=='rt_deliver_fraction':
   if role!='Radiation Technologist':return {'error':'Radiation Technologist required'},403
   e=must('radiation');rx=e['data'].get('prescription',{});plan=e['data'].get('planning',{});rxv=int(rx.get('prescription_version') or 1);planv=int(plan.get('plan_version') or 1)
   valid_physics=plan.get('physics_qa')=='Approved' and int(plan.get('physics_qa_plan_version') or 0)==planv and int(plan.get('physics_qa_prescription_version') or 0)==rxv
   valid_ro=plan.get('physician_final_approval')=='Approved' and int(plan.get('physician_approval_plan_version') or 0)==planv and int(plan.get('physician_approval_prescription_version') or 0)==rxv
   if rx.get('status')!='RT Oncologist Approved' or not valid_physics or not valid_ro:return {'error':'Current approved prescription plus Physics QA and RO final approval for the current RT plan/prescription version are required','plan_version':planv,'prescription_version':rxv},409
   fr=list(e['data'].get('fractions',[]));num=int(d.get('fraction_number') or len(fr)+1)
   if any(int(x.get('fraction_number',0))==num and x.get('status')=='Delivered' for x in fr):return {'error':'Duplicate fraction delivery'},409
   if num<1 or num>int(rx.get('fractions',0)):return {'error':'Fraction number outside prescription'},409
   status=d.get('status','Delivered');dose=float(d.get('delivered_dose_gy') or rx.get('dose_per_fraction_gy',0)) if status=='Delivered' else 0
   saf=rt_fraction_safety(rx,fr,dose,status)
   if not saf['ok']:return {'error':'RT fraction dose safety check failed','details':saf['errors'],'prescribed_fraction_dose_gy':saf.get('prescribed_fraction_dose_gy'),'projected_cumulative_dose_gy':saf.get('projected_cumulative_dose_gy'),'prescribed_total_dose_gy':saf.get('prescribed_total_dose_gy')},409
   x={'fraction_number':num,'status':status,'date_time':d.get('date_time') or now(),'planned_date_time':d.get('planned_date_time',''),'rescheduled_to':d.get('rescheduled_to',''),'delivered_dose_gy':dose,'dose_safety_snapshot':saf,'prescription_version':rxv,'plan_version':planv,'delivered_by':actor(role),'verified_by':d.get('verified_by') or actor(role)['name'],'image_guidance_performed':bool(d.get('image_guidance_performed')),'setup_variation':d.get('setup_variation',''),'toxicity':d.get('toxicity',''),'reason':d.get('reason','')};fr.append(x);delivered=sum(1 for z in fr if z['status']=='Delivered');st='In Progress' if delivered<int(rx['fractions']) else 'Completed';update_rec(c,e['id'],{'fractions':fr},st,role,'RT_FRACTION',f"{num} • Rx v{rxv} • Plan v{planv}");journey_add(c,pid,'Radiation Treatment',f"Fraction {num} {x['status']}",st,role,'radiation',e['id'],x.get('reason',''),True);return {'ok':True,'status':st,'delivered_count':delivered,'plan_version':planv,'prescription_version':rxv,'cumulative_delivered_dose_gy':saf.get('projected_cumulative_dose_gy')},200
  if a=='surgery_sign_plan':
   if role!='Surgical Oncology':return {'error':'Surgical Oncology required'},403
   e=must('surgery');plan={**e['data'].get('plan',{}),**d};req=['procedure','indication','intent','site','laterality','extent','approach','nodal_procedure','reconstruction','planned_date','priority','preop_requirements','required_imaging_pathology','anesthesia','anesthesia_clearance','blood_requirement'];miss=[x for x in req if plan.get(x) in ['',None,[]]]
   if miss:return {'error':'Surgical plan incomplete','missing':miss},409
   plan.update({'status':'Planned','signed_by':actor(role),'signed_at':now()});epid=d.get('episode_id') or e['data'].get('episode_id') or ((current_episode(c,pid) or ensure_episode(c,pid,role))['id']);update_rec(c,e['id'],{'episode_id':epid,'plan':plan},'Planned',role,'SURGERY_PLAN_SIGN');grant_patient_access(c,pid,'Surgical Nurse','surgery_plan',e['id'],role);handoff(c,pid,'Patient Liaison','Obtain signed surgical consent for '+plan.get('procedure',''),'Surgical consent','surgery',e['id'],role,'High','Signed surgical plan available for consent',{'procedure':plan.get('procedure')});handoff(c,pid,'Anaesthetist','Complete pre-operative anaesthesia assessment','Support service referral','surgery',e['id'],role,'High','Signed surgical plan available for anaesthesia clearance',{'procedure':plan.get('procedure')});handoff(c,pid,'Blood Bank / Transfusion','Confirm blood product availability for surgery','Support service referral','surgery',e['id'],role,'Routine','Signed surgical plan requires blood availability confirmation',{'blood_requirement':plan.get('blood_requirement')});return {'ok':True,'episode_id':epid},200
  if a=='surgery_preop':
   if role not in ['Surgical Oncology','Surgical Nurse']:return {'error':'Surgical team required'},403
   e=must('surgery');pre={**e['data'].get('preop',{}),**d};pre['ready']=all(pre.get(k)=='Complete' for k in ['anesthesia_clearance','labs','consent']);update_rec(c,e['id'],{'preop':pre},'Pre-op Ready' if pre['ready'] else 'Planned',role,'SURGERY_PREOP');return {'ok':True,'ready':pre['ready']},200
  if a=='surgery_performed':
   if role!='Surgical Oncology':return {'error':'Surgical Oncology required'},403
   e=must('surgery');
   if not e['data'].get('preop',{}).get('ready'):return {'error':'Pre-op readiness required'},409
   req=['actual_procedure','operation_date_time','preop_diagnosis','postop_diagnosis','laterality','findings','specimens','estimated_blood_loss_ml','operative_time_min','surgeons','postop_plan'];miss=[x for x in req if d.get(x) in ['',None,[]]]
   if miss:return {'error':'Operative record incomplete','missing':miss},409
   out={**d,'signed_by':actor(role),'signed_at':now()};update_rec(c,e['id'],{'outcome':out},'Performed',role,'SURGERY_PERFORMED');grant_patient_access(c,pid,'Pathology','surgical_specimen',e['id'],role);grant_patient_access(c,pid,'Pathology Technologist','surgical_specimen',e['id'],role);handoff(c,pid,'Pathology Technologist','Accession and process surgical specimen(s)','Pathology accession','surgery',e['id'],role,'High','Signed operative note with specimen(s) submitted for accession',{'specimens':d.get('specimens',[])});handoff(c,pid,'Stoma / Wound Nurse','Complete post-operative wound assessment','Support service referral','surgery',e['id'],role,'Routine','Post-operative wound/stoma assessment required',{'stoma_created':d.get('stoma_created')});journey_add(c,pid,'Surgery','Procedure Performed','Performed',role,'surgery',e['id'],d.get('actual_procedure',''),True);hist=latest(c,pid,'treatment_history');eps=list(hist['data'].get('episodes',[]));eps.append({'type':'Surgery','episode_id':e['data'].get('episode_id') or ((current_episode(c,pid) or {}).get('id')),'date':d['operation_date_time'],'status':'Performed','procedure':d['actual_procedure'],'laterality':d['laterality']});update_rec(c,hist['id'],{'episodes':eps},role=role,action='HISTORY_APPEND');return {'ok':True},200
  if a=='surgery_pathology_link':
   if role!='Surgical Oncology':return {'error':'Surgical Oncology required to link final pathology and create pathological stage'},403
   e=must('surgery');link=d.get('pathology_record_id');path=get_rec(c,link) if link else None
   if not path or path['entity_type']!='pathology' or path['status']!='Final':return {'error':'Final pathology record required'},409
   req=['postop_stage','margin_status','nodes_examined','nodes_positive'];miss=[x for x in req if d.get(x) in ['',None]]
   if miss:return {'error':'Post-operative pathology handoff incomplete','missing':miss},409
   node_status=f"{int(d['nodes_positive'])}/{int(d['nodes_examined'])} positive"
   update_rec(c,e['id'],{'histopathology_link':link,'postop_stage':d['postop_stage'],'margin_status':d['margin_status'],'nodes_examined':int(d['nodes_examined']),'nodes_positive':int(d['nodes_positive']),'node_status':node_status,'adjuvant_review_required':True,'pathology_linked_at':now(),'pathology_linked_by':actor(role)},'Histopathology Available',role,'SURGERY_PATH_LINK')
   prev=latest(c,pid,'diagnosis');base=dict(prev['data']) if prev else {};base.update({'episode_id':e['data'].get('episode_id') or base.get('episode_id') or ((current_episode(c,pid) or {}).get('id')),'stage_t':d.get('path_t',base.get('stage_t','')),'stage_n':d.get('path_n',base.get('stage_n','')),'stage_m':d.get('path_m',base.get('stage_m','')),'stage_group':d['postop_stage'],'staging_basis':'Pathological','staging_date':d.get('staging_date') or str(date.today()),'previous_stage_record_id':prev['id'] if prev else '','source_surgery_id':e['id'],'source_pathology_id':link,'margin_status':d['margin_status'],'nodes_examined':int(d['nodes_examined']),'nodes_positive':int(d['nodes_positive']),'staged_by':actor(role),'staged_at':now()})
   dxid=new_record(c,pid,'diagnosis',base,'Verified',role)
   adjuvant={'status':'Ready for adjuvant review','derived':True,'source_operating_record_id':e['id'],'source_pathology_id':link,'source_pathological_stage_id':dxid,'derived_at':now(),'formula':'Signed operative record + final pathology + pathological stage available'}
   update_rec(c,e['id'],{'adjuvant_review':adjuvant},'Histopathology Available',role,'ADJUVANT_REVIEW_READY')
   task_ids=[]
   for rr,title in [('MDT Coordinator','Post-operative adjuvant MDT review'),('Medical Oncology','Post-operative adjuvant systemic-therapy review')]:
    grant_patient_access(c,pid,rr,'adjuvant_review',e['id'],role);task_ids.append(create_task(c,pid,rr,title,'Adjuvant review','High','surgery',e['id'],str(date.today()+timedelta(days=3)),reason='Final operative pathology and pathological stage are available',data={'adjuvant_review':adjuvant},created_by=role))
   for rr in ['MDT Chair','Radiation Oncology']:grant_patient_access(c,pid,rr,'adjuvant_review',e['id'],role)
   hist=latest(c,pid,'treatment_history')
   if hist:
    eps=list(hist['data'].get('episodes',[]));eps.append({'type':'Post-operative pathology / restaging','episode_id':base.get('episode_id'),'date':base['staging_date'],'status':'Verified','stage':d['postop_stage'],'source_surgery_id':e['id'],'source_pathology_id':link,'diagnosis_record_id':dxid});update_rec(c,hist['id'],{'episodes':eps},role=role,action='HISTORY_APPEND')
   return {'ok':True,'pathological_stage_record_id':dxid,'adjuvant_review':adjuvant,'task_ids':task_ids,'note':'New pathological staging record created; prior clinical stage preserved.'},200
  if a=='complete_adjuvant_review':
   if role not in ['Medical Oncology','MDT Chair']:return {'error':'Medical Oncology or MDT Chair required'},403
   e=must('surgery');adj=dict(e['data'].get('adjuvant_review') or {})
   if adj.get('status')!='Ready for adjuvant review':return {'error':'Ready for adjuvant review state required'},409
   reason=str(d.get('reason') or '').strip();source=str(d.get('source_record_id') or '').strip()
   if not reason or not source:return {'error':'Completion reason and source_record_id required'},409
   adj.update({'status':'Adjuvant review complete','completed_by':actor(role),'completed_at':now(),'completion_reason':reason,'completion_source_record_id':source});update_rec(c,e['id'],{'adjuvant_review':adj},e['status'],role,'ADJUVANT_REVIEW_COMPLETE',reason);return {'ok':True,'adjuvant_review':adj},200
  if a=='finance_estimate':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');order=latest(c,pid,'treatment_order');
   if not order:return {'error':'No treatment order'},409
   est=tariff_estimate(c,order);est.update({'source_order_id':order['id'],'generated_at':now(),'clinical_dose_read_only':True});update_rec(c,e['id'],{'mo_drug_estimate':est,'estimate_status':'Calculated','estimate_no':'EST-'+uuid.uuid4().hex[:6].upper(),'valid_until':str(date.today()+timedelta(days=15))},'Active',role,'FIN_ESTIMATE');return {'ok':True,'total':est['total'],'lines':est['lines'],'basis':est['basis']},200
  if a=='finance_scheme_assessment':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');sid=str(d.get('scheme_id') or '');row=c.execute("SELECT * FROM finance_schemes WHERE id=? AND status='Active'",(sid,)).fetchone()
   if not row:return {'error':'Active payer scheme required'},409
   row=dict(row);required=jload(row['required_fields_json'],[]);evidence=d.get('evidence') or {};missing=[x for x in required if not str(evidence.get(x) or '').strip()];result='Information incomplete' if missing else 'Potentially eligible — external verification required'
   arow={'id':'SCHEME-'+uuid.uuid4().hex[:8].upper(),'scheme_id':sid,'scheme_name':row['name'],'assessed_at':now(),'assessed_by':actor(role),'evidence':evidence,'result':result,'missing':missing,'verification_mode':row['verification_mode'],'package_model':jload(row['package_model_json'],{}),'definitive_eligibility':False,'source_ref':row['source_ref']};xs=list(e['data'].get('scheme_assessments',[]));xs.append(arow);update_rec(c,e['id'],{'scheme_assessments':xs,'payer_category':row['name']},'Active',role,'FIN_SCHEME_ASSESS');return {'ok':True,'assessment':arow},200
  if a=='finance_counselling':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');track=list(e['data'].get('tracking',[]));track.append({'at':now(),'status':d.get('financial_status'),'note':d.get('note',''),'by':actor(role)});update_rec(c,e['id'],{'counselling_status':d.get('counselling_status','Completed'),'payer_category':d.get('payer_category',''),'financial_status':d.get('financial_status',''),'counselled_by':actor(role),'counselled_at':now(),'tracking':track},'Active',role,'FIN_COUNSELLING');return {'ok':True},200
  if a=='fundraising_letter':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');pat=patient(c,pid);dx=latest(c,pid,'diagnosis');est=e['data'].get('mo_drug_estimate',{});cons=active_disclosure_consent(c,pid);redacted=bool(d.get('redacted',True))
   if not redacted and not cons:return {'error':'Active External Financial Assistance Disclosure Consent is required before an identifiable external letter can be created'},409
   case_code='CCA-SUPPORT-'+hashlib.sha256(pid.encode()).hexdigest()[:8].upper();ident=f"{pat['name']} ({pat['mrn']})" if not redacted else case_code;diag=dx['data'].get('cancer_type','oncology care') if not redacted else 'oncology care'
   if redacted and str(d.get('text') or '').strip():return {'error':'Custom external-letter text is not permitted in redacted mode because it could reintroduce patient identifiers; use the server-generated redacted template or obtain disclosure consent'},409
   text=d.get('text') or f"To whom it may concern,\n\n{ident} is receiving {diag}. The current synthetic demo estimate is INR {est.get('total',0)}. This letter is a draft for financial-assistance workflow demonstration and is not a clinical or financial commitment.\n\nCCA Demo Finance Team";letter={'status':'Draft — Approval Required','recipient':d.get('recipient',''),'purpose':d.get('purpose','Treatment support'),'text':text,'redacted':redacted,'consent_id':cons.get('id') if cons else '','generated_by':actor(role),'generated_at':now(),'approved_by':None,'approved_at':'','released_at':''};update_rec(c,e['id'],{'fundraising_letter':letter},'Active',role,'FUNDRAISING_LETTER');handoff(c,pid,'Finance / Billing','Independent approval required for fundraising letter','External disclosure approval','conversion',e['id'],role,'High','Draft fundraising letter awaiting independent Finance approval',{'letter':letter});return {'ok':True,'letter':letter,'next_role':'Finance / Billing'},200
  if a=='fundraising_approve':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');letter=e['data'].get('fundraising_letter') or {};cons=active_disclosure_consent(c,pid)
   if not cons:return {'error':'Active disclosure consent required before external release approval'},409
   if not str(letter.get('status','')).startswith('Draft'):return {'error':'A draft fundraising letter is required'},409
   if (letter.get('generated_by') or {}).get('id')==actor(role)['id']:return {'error':'Independent second-person approval required; generator cannot approve their own external disclosure'},409
   letter={**letter,'status':'Approved for Release','approved_by':actor(role),'approved_at':now(),'consent_id':cons['id']};update_rec(c,e['id'],{'fundraising_letter':letter},'Active',role,'FUNDRAISING_APPROVE');complete_open_tasks(c,pid,'Finance / Billing','External disclosure approval',source_type='conversion',source_id=e['id'],completed_by=role);handoff(c,pid,'Finance / Billing','Release approved fundraising letter','External disclosure release','conversion',e['id'],role,'High','Fundraising letter approved for release',{'letter':letter});return {'ok':True,'letter':letter,'next_role':'Finance / Billing'},200
  if a=='fundraising_release':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');letter=e['data'].get('fundraising_letter') or {}
   if letter.get('status')!='Approved for Release':return {'error':'Independent approval is required before release'},409
   if not active_disclosure_consent(c,pid):return {'error':'Disclosure consent is no longer active'},409
   letter={**letter,'status':'Released','released_by':actor(role),'released_at':now()};update_rec(c,e['id'],{'fundraising_letter':letter},'Active',role,'FUNDRAISING_RELEASE');complete_open_tasks(c,pid,'Finance / Billing','External disclosure release',source_type='conversion',source_id=e['id'],completed_by=role);return {'ok':True,'letter':letter},200
  if a=='integration_status_update':
   if role!='Hospital Management / Admin':return {'error':'Admin required'},403
   iid=str(d.get('adapter_id') or '');status=str(d.get('status') or '');allowed=['Not configured','Configured — not connected','Connected','Degraded','Error','Disabled']
   if status not in allowed:return {'error':'Governed integration status required','allowed':allowed},409
   row=c.execute('SELECT * FROM integration_adapters WHERE id=?',(iid,)).fetchone()
   if not row:return {'error':'Integration adapter not found'},404
   c.execute('UPDATE integration_adapters SET status=?,last_checked_at=?,notes=? WHERE id=?',(status,now(),str(d.get('notes') or row['notes']),iid));audit(c,'',role,'INTEGRATION_STATUS','integration_adapter',iid,status);return {'ok':True,'status':status},200
  if a=='abha_set_verification':
   if role not in ['Front Desk','Patient Attender','Health Information Management']:return {'error':'Front Desk / HIM role required'},403
   pat=patient(c,pid);abha=normalize_abha(d.get('abha') or pat.get('abha'))
   if not valid_abha(abha) or not abha:return {'error':'A valid 14-digit ABHA is required before verification can be recorded'},409
   status=d.get('verification_status');allowed=['Unverified','Verified — Document','Verified — External ABDM adapter']
   if status not in allowed:return {'error':'Governed ABHA verification status required','allowed':allowed},409
   source=str(d.get('source_reference') or '').strip()
   if status!='Unverified' and not source:return {'error':'Verification source/reference is required'},409
   if status=='Verified — External ABDM adapter':
    ad=c.execute("SELECT * FROM integration_adapters WHERE id='ABDM'").fetchone()
    if not ad or ad['status']!='Connected':return {'error':'ABDM adapter is not connected; external verification cannot be asserted'},409
   reg=latest(c,pid,'registration');info={'abha':abha,'verification_status':status,'source_reference':source,'verified_by':actor(role),'verified_at':now() if status!='Unverified' else ''};update_rec(c,reg['id'],{'abha_verification':info},role=role,action='ABHA_VERIFICATION');c.execute('UPDATE patients SET abha=?,updated_at=? WHERE id=?',(abha,now(),pid));return {'ok':True,'verification':info},200
  if a=='abdm_consent_record':
   if role not in ['Patient Liaison','Health Information Management','Front Desk','Patient Attender']:return {'error':'Consent-authorized role required'},403
   e=must('consent');items=list(e['data'].get('items',[]));purpose=str(d.get('purpose') or '').strip();status=str(d.get('status') or 'Granted')
   if not purpose:return {'error':'ABDM consent purpose is required'},409
   if status not in ['Granted','Denied','Revoked','Expired']:return {'error':'Invalid ABDM consent status'},409
   x={'id':'ABDMCONS-'+uuid.uuid4().hex[:8].upper(),'type':'ABDM Health Information Exchange Consent','purpose':purpose,'status':status,'hip':d.get('hip',''),'hiu':d.get('hiu',''),'date_from':d.get('date_from',''),'date_to':d.get('date_to',''),'granted_at':now() if status=='Granted' else '','recorded_by':actor(role),'source_reference':d.get('source_reference',''),'adapter_status':'Interface boundary — live ABDM exchange requires connected adapter'};items.append(x);update_rec(c,e['id'],{'items':items},'Active',role,'ABDM_CONSENT');return {'ok':True,'consent':x},200
  if a=='save_referral':
   if role not in WRITE['referral']:return {'error':'Role not authorized for referral lifecycle'},403
   e=must('referral')
   if not e:
    rid=new_record(c,pid,'referral',{'referral_no':'REF-'+uuid.uuid4().hex[:7].upper(),'history':[]},'Created',role);e=get_rec(c,rid)
   cur=str(e.get('status') or e['data'].get('status') or 'Created');new=str(d.get('status') or cur)
   if new!=cur and new not in REFERRAL_TRANSITIONS.get(cur,set()):return {'error':'Illegal referral state transition','from':cur,'to':new,'allowed':sorted(REFERRAL_TRANSITIONS.get(cur,set()))},409
   priority=d.get('priority',e['data'].get('priority','Routine'))
   if priority not in VALUE_SETS['referral_priority']:return {'error':'Governed referral priority required','allowed':VALUE_SETS['referral_priority']},409
   dept=d.get('assigned_department',e['data'].get('assigned_department',''))
   clinician=d.get('assigned_clinician',e['data'].get('assigned_clinician',''))
   if new in ['Assigned','Accepted','Scheduled','Seen','Closed'] and not dept:return {'error':'Assigned department is required for referral progression'},409
   if new in ['Assigned','Accepted','Scheduled','Seen','Closed'] and not clinician:return {'error':'Assigned clinician/service is required for referral progression'},409
   hist=list(e['data'].get('history',[]))
   if new!=cur:hist.append({'at':now(),'from':cur,'to':new,'by':actor(role),'reason':d.get('transition_reason','')})
   patch={**{k:v for k,v in d.items() if k not in ['transition_reason']},'priority':priority,'assigned_department':dept,'assigned_clinician':clinician,'status':new,'history':hist,'updated_by':actor(role),'updated_at':now()}
   update_rec(c,e['id'],patch,new,role,'REFERRAL_UPDATE',f'{cur} -> {new}')
   if new in ['Assigned','Accepted']:
    owner=referral_owner_role(dept);grant_patient_access(c,pid,owner,'referral',e['id'],role)
    create_task(c,pid,owner,'Referral: '+str(d.get('reason') or e['data'].get('reason') or 'Oncology referral'),'Referral lifecycle','Critical' if priority=='Emergency' else ('High' if priority=='Urgent' else 'Routine'),'referral',e['id'],'',((current_episode(c,pid) or {}).get('id','')),new,{'referral_id':e['id'],'status':new},role)
   journey_add(c,pid,dept or 'Front Desk','Referral '+new,new,role,'referral',e['id'],d.get('reason',e['data'].get('reason','')),True)
   return {'ok':True,'id':e['id'],'status':new},200
  if a=='inpatient_med_order':
   if role!='Inpatient Oncology Clinician':return {'error':'Inpatient Oncology Clinician required for inpatient medication orders'},403
   e=must('inpatient_care');adm=latest(c,pid,'admission');active=next((x for x in reversed((adm or {}).get('data',{}).get('admissions',[])) if x.get('status')=='Active'),None)
   if not active:return {'error':'Active admission required'},409
   req=['medication','dose','unit','route','frequency','indication'];miss=[k for k in req if d.get(k) in ['',None]]
   if miss:return {'error':'Inpatient medication order incomplete','missing':miss},409
   try:dose=float(d['dose'])
   except:return {'error':'Medication dose must be numeric'},409
   if dose<=0:return {'error':'Medication dose must be greater than zero'},409
   orders=list(e['data'].get('medication_orders',[]));x={'id':'IPDORD-'+uuid.uuid4().hex[:7].upper(),'order_no':'IPD-RX-'+uuid.uuid4().hex[:6].upper(),'admission_id':active['id'],'episode_id':active.get('episode_id',''),'medication':d['medication'],'dose':dose,'unit':d['unit'],'route':d['route'],'frequency':d['frequency'],'indication':d['indication'],'start_at':d.get('start_at') or now(),'stop_at':d.get('stop_at',''),'status':'Active','ordered_by':actor(role),'ordered_at':now()};orders.append(x);update_rec(c,e['id'],{'medication_orders':orders},'Active',role,'IPD_MED_ORDER',x['order_no']);handoff(c,pid,'Inpatient Oncology Nurse','Administer/execute inpatient medication order','IPD medication administration','inpatient_care',e['id'],role,'High','Signed inpatient medication order',{'medication_order':x});return {'ok':True,'order':x,'next_role':'Inpatient Oncology Nurse'},200
  if a=='inpatient_mar':
   if role!='Inpatient Oncology Nurse':return {'error':'Inpatient Oncology Nurse required for inpatient MAR'},403
   e=must('inpatient_care');orders=e['data'].get('medication_orders',[]);oid=d.get('order_id');o=next((x for x in orders if x.get('id')==oid),None)
   if not o or o.get('status')!='Active':return {'error':'Active inpatient medication order required'},409
   clinical=parse_dt(d.get('administration_datetime'))
   if not clinical:return {'error':'Valid clinical administration datetime required'},409
   try:actual=float(d.get('actual_dose'))
   except:return {'error':'Actual administered dose required'},409
   if abs(actual-float(o['dose']))>1e-9 and not str(d.get('variance_reason') or '').strip():return {'error':'Dose variance requires documentation'},409
   mar=list(e['data'].get('mar',[]));x={'id':'IPDMAR-'+uuid.uuid4().hex[:7].upper(),'order_id':oid,'admission_id':o['admission_id'],'medication':o['medication'],'ordered_dose':o['dose'],'unit':o['unit'],'route':o['route'],'actual_dose':actual,'administration_datetime':clinical.isoformat(),'system_entry_time':now(),'variance_reason':d.get('variance_reason',''),'response':d.get('response',''),'administered_by':actor(role)};mar.append(x)
   if d.get('complete_order'):o['status']='Completed';o['completed_at']=now();o['completed_by']=actor(role)
   update_rec(c,e['id'],{'mar':mar,'medication_orders':orders},'Active',role,'IPD_MAR',o['medication']);complete_open_tasks(c,pid,role,'IPD medication administration',source_type='inpatient_care',source_id=e['id'],completed_by=role);return {'ok':True,'mar':x,'order_status':o['status']},200
  if a=='post_cycle_review':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   inf=e if e and e.get('entity_type')=='infusion' else get_rec(c,d.get('infusion_id')) if d.get('infusion_id') else latest(c,pid,'infusion')
   if not inf or inf.get('status')!='Completed':return {'error':'Completed systemic administration source required for post-cycle review'},409
   order=get_rec(c,inf.get('data',{}).get('order_id'));decision=str(d.get('decision') or '').strip();allowed=['Proceed','Hold','Delay','Modify','Stop']
   if decision not in allowed:return {'error':'Governed post-cycle decision required','allowed':allowed},409
   reason=str(d.get('clinical_reason') or '').strip()
   if not reason:return {'error':'Post-cycle clinical reason required'},409
   tox=latest(c,pid,'toxicity');events=list((tox or {}).get('data',{}).get('events',[]));selected=d.get('toxicity_event_ids') or [x.get('id') for x in events if str(x.get('outcome','')).lower() not in ['resolved','recovered']]
   mod=latest(c,pid,'modification')
   if not mod:return {'error':'Modification/post-cycle record unavailable'},404
   reviews=list(mod.get('data',{}).get('post_cycle_reviews',[]));x={'id':'PCR-'+uuid.uuid4().hex[:7].upper(),'infusion_id':inf['id'],'infusion_version':inf['version'],'order_id':(order or {}).get('id',''),'order_version':(order or {}).get('version'),'cycle':(order or {}).get('data',{}).get('cycle'),'day':(order or {}).get('data',{}).get('day'),'actual_administered_snapshot':inf.get('data',{}).get('actual_administered_snapshot') or inf.get('data',{}).get('mar',[]),'toxicity_source_id':(tox or {}).get('id',''),'toxicity_event_ids':selected,'decision':decision,'clinical_reason':reason,'next_cycle':d.get('next_cycle'),'reevaluation_date':d.get('reevaluation_date',''),'reviewed_by':actor(role),'reviewed_at':now()};reviews.append(x);update_rec(c,mod['id'],{'post_cycle_reviews':reviews},'Active',role,'POST_CYCLE_REVIEW',decision);complete_open_tasks(c,pid,role,'Next-cycle decision',source_type='infusion',source_id=inf['id'],completed_by=role)
   if decision=='Modify':handoff(c,pid,'Medical Oncology','Create treatment modification from post-cycle review','Treatment modification','infusion',inf['id'],role,'High',reason,{'post_cycle_review':x})
   elif decision=='Proceed':handoff(c,pid,'Medical Oncology','Perform next-cycle treatment readiness','Treatment readiness','infusion',inf['id'],role,'High',reason,{'post_cycle_review':x})
   elif decision in ['Hold','Delay']:handoff(c,pid,'Medical Oncology','Re-evaluate next-cycle readiness','Readiness re-evaluation','infusion',inf['id'],role,'High',reason,{'post_cycle_review':x},d.get('reevaluation_date',''))
   journey_add(c,pid,'Medical Oncology','Post-cycle Review',decision,role,'infusion',inf['id'],reason,True);return {'ok':True,'review':x,'next_action':'Treatment modification' if decision=='Modify' else ('Treatment readiness' if decision=='Proceed' else ('Readiness re-evaluation' if decision in ['Hold','Delay'] else 'None'))},200
  if a=='save_response_baseline':
   if role not in ['Radiologist','Medical Oncology']:return {'error':'Radiologist / Medical Oncology required'},403
   e=must('response');study=get_rec(c,d.get('source_study_id')) if d.get('source_study_id') else None
   if not study or study.get('entity_type')!='radiology' or study.get('status')!='Final':return {'error':'Final radiology source study required for RECIST baseline','blocking_role':'Radiologist'},409
   lesions=d.get('target_lesions') or []
   if not d.get('date') or not lesions:return {'error':'Baseline date and target lesions required'},409
   clean=[]
   for x in lesions:clean.append({**x,'baseline_selected':True})
   res=recist_evaluate(clean,clean,[],False,d.get('non_target',''))
   if not res.get('ok'):return {'error':res.get('error')},409
   existing=e.get('data',{}).get('baseline') or {};reason=str(d.get('amendment_reason') or '').strip()
   if existing and not reason:return {'error':'RECIST baseline is frozen once established; amendment_reason required to replace it'},409
   hist=list(e.get('data',{}).get('baseline_history',[]))
   if existing:hist.append(existing)
   b={'date':d['date'],'framework':'RECIST 1.1','criteria_version':'1.1','source_study_id':study['id'],'source_study_version':study['version'],'target_lesions':clean,'sum_mm':res['sum_mm'],'non_target':d.get('non_target',''),'recorded_by':actor(role),'recorded_at':now(),'amendment_reason':reason};update_rec(c,e['id'],{'baseline':b,'baseline_history':hist},'Active',role,'RECIST_BASELINE',reason);return {'ok':True,'baseline':b},200
  if a=='surgery_theatre_readiness':
   if role!='Surgical Nurse':return {'error':'Surgical Nurse required'},403
   e=must('surgery');pre=e['data'].get('preop',{})
   if not pre.get('ready'):return {'error':'Completed pre-operative readiness required'},409
   checks=d.get('checklist') or {};req=['identity','site_laterality','procedure','consent','anaesthesia','equipment','blood_if_required','counts_baseline'];miss=[x for x in req if checks.get(x) is not True]
   if miss:return {'error':'Theatre readiness checklist incomplete','missing':miss},409
   if not d.get('theatre') or not d.get('scheduled_start'):return {'error':'Theatre and scheduled start required'},409
   tr={'status':'Signed','checklist':checks,'theatre':d['theatre'],'scheduled_start':d['scheduled_start'],'team_brief':d.get('team_brief',''),'signed_by':actor(role),'signed_at':now()};update_rec(c,e['id'],{'theatre_readiness':tr},e['status'],role,'SURGERY_THEATRE_READY');complete_open_tasks(c,pid,role,'Theatre readiness',source_type='surgery',source_id=e['id'],completed_by=role);handoff(c,pid,'Surgical Oncology','Proceed to surgery / operative record','Surgery execution','surgery',e['id'],role,'High','Theatre readiness signed',{'theatre_readiness':tr});journey_add(c,pid,'Operating Theatre','Theatre Ready','Theatre Ready',role,'surgery',e['id'],d['theatre'],True);return {'ok':True,'status':'Theatre Ready','next_role':'Surgical Oncology'},200
  if a=='surgery_adjuvant_decision':
   if role not in ['Surgical Oncology','Medical Oncology','Radiation Oncology']:return {'error':'Treating oncology role required'},403
   e=must('surgery')
   if not e['data'].get('histopathology_link'):return {'error':'Final post-operative Pathology review required'},409
   decision=str(d.get('decision') or '');allowed=['Adjuvant Systemic Therapy','Adjuvant Radiation','Combined Adjuvant Therapy','MDT Re-discussion','Surveillance / No Adjuvant Treatment'];reason=str(d.get('rationale') or '').strip()
   if decision not in allowed or not reason:return {'error':'Structured adjuvant decision and rationale required','allowed':allowed},409
   owners={'Adjuvant Systemic Therapy':['Medical Oncology'],'Adjuvant Radiation':['Radiation Oncology'],'Combined Adjuvant Therapy':['Medical Oncology','Radiation Oncology'],'MDT Re-discussion':['MDT Coordinator'],'Surveillance / No Adjuvant Treatment':['Nurse Navigator']}[decision];ad={'decision':decision,'rationale':reason,'responsible_roles':owners,'decided_by':actor(role),'decided_at':now(),'source_pathology_id':e['data'].get('histopathology_link'),'postop_stage':e['data'].get('postop_stage')};update_rec(c,e['id'],{'adjuvant_decision':ad,'adjuvant_review_required':False},e['status'],role,'SURGERY_ADJUVANT_DECISION',decision)
   for rr in owners:handoff(c,pid,rr,decision,'Adjuvant decision','surgery',e['id'],role,'High',reason,ad)
   return {'ok':True,'decision':ad,'next_roles':owners},200
  if a=='rt_record_otv':
   if role!='Radiation Oncology':return {'error':'Radiation Oncology required'},403
   e=e if e and e.get('entity_type')=='radiation' else latest(c,pid,'radiation');delivered=[x for x in (e or {}).get('data',{}).get('fractions',[]) if x.get('status')=='Delivered']
   if not e or not delivered:return {'error':'At least one delivered fraction is required before OTV'},409
   req=['assessment','toxicity_summary','plan'];miss=[x for x in req if not str(d.get(x) or '').strip()]
   if miss:return {'error':'On-treatment review incomplete','missing':miss},409
   rows=list(e['data'].get('otv',[]));x={'id':'OTV-'+uuid.uuid4().hex[:7].upper(),'after_fraction':d.get('after_fraction') or delivered[-1].get('fraction_number'),'assessment':d['assessment'],'toxicity_summary':d['toxicity_summary'],'plan':d['plan'],'weight_kg':d.get('weight_kg'),'performance_status':d.get('performance_status'),'signed_by':actor(role),'signed_at':now()};rows.append(x);update_rec(c,e['id'],{'otv':rows},e['status'],role,'RT_OTV_SIGN');complete_open_tasks(c,pid,role,'RT OTV',source_type='radiation',source_id=e['id'],completed_by=role);return {'ok':True,'otv':x},200
  if a=='rt_record_interruption':
   if role not in ['Radiation Oncology','Radiation Technologist']:return {'error':'Radiation Oncology / Radiation Technologist required'},403
   e=e if e and e.get('entity_type')=='radiation' else latest(c,pid,'radiation');reason=str(d.get('reason') or '').strip()
   if not e or not reason:return {'error':'Active RT course and interruption reason required'},409
   rows=list(e['data'].get('interruptions',[]));x={'id':'RTINT-'+uuid.uuid4().hex[:7].upper(),'start_at':d.get('start_at') or now(),'end_at':d.get('end_at',''),'reason':reason,'category':d.get('category','Clinical/Operational'),'recorded_by':actor(role),'recorded_at':now(),'compensation_plan':d.get('compensation_plan','')};rows.append(x);update_rec(c,e['id'],{'interruptions':rows},e['status'],role,'RT_INTERRUPTION',reason);handoff(c,pid,'Radiation Oncology','Review RT interruption and decide continuation/modification','RT interruption review','radiation',e['id'],role,'High',reason,{'interruption':x});journey_add(c,pid,'Radiation Treatment','RT Interrupted',e['status'],role,'radiation',e['id'],reason,True);return {'ok':True,'interruption':x,'next_role':'Radiation Oncology'},200
  if a=='request_treatment_history_confirmation':
   if role not in ['Medical Oncology','Nurse Navigator']:return {'error':'Medical Oncology / Nurse Navigator required to request historical treatment confirmation'},403
   target=str(d.get('target_role') or '');typ=str(d.get('type') or '');reason=str(d.get('reason') or '').strip();owners={'Surgery':'Surgical Oncology','Radiation Therapy':'Radiation Oncology','Systemic Therapy':'Medical Oncology'}
   if typ not in owners:return {'error':'Historical treatment type must identify the owning specialty','allowed':list(owners)},409
   if target!=owners[typ]:return {'error':'Historical treatment confirmation must be routed to the owning specialty','expected_role':owners[typ]},409
   if not reason:return {'error':'Reason/provenance for historical treatment confirmation is required'},409
   dx=latest_usable(c,pid,'diagnosis',['Verified']);src=dx or current_episode(c,pid)
   if not src:return {'error':'Verified diagnosis / active Cancer Episode required before historical treatment reconciliation'},409
   tid=handoff(c,pid,target,'Confirm historical '+typ,'Historical treatment confirmation',src['entity_type'],src['id'],role,'Routine',reason,{'treatment_type':typ,'requested_by':actor(role),'provenance_reason':reason,'episode_id':(current_episode(c,pid) or {}).get('id','')})
   return {'ok':True,'task_id':tid,'next_role':target},200
  if a=='record_treatment_history_event':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Treating oncology clinician required'},403
   hist=e if e and e.get('entity_type')=='treatment_history' else latest(c,pid,'treatment_history')
   if not hist:
    rid=new_record(c,pid,'treatment_history',{'episodes':[]},'Active',role);hist=get_rec(c,rid)
   ep=current_episode(c,pid) or ensure_episode(c,pid,role)
   typ=str(d.get('type') or '').strip();dt=str(d.get('date') or '').strip();status=str(d.get('status') or '').strip();desc=str(d.get('description') or '').strip()
   allowed_types=['Systemic Therapy','Radiation Therapy','Surgery','Other Cancer-Directed Treatment']
   if typ not in allowed_types:return {'error':'Governed completed-treatment type required','allowed':allowed_types},409
   owner_by_type={'Systemic Therapy':'Medical Oncology','Radiation Therapy':'Radiation Oncology','Surgery':'Surgical Oncology'};expected_owner=owner_by_type.get(typ)
   if expected_owner and role!=expected_owner:return {'error':expected_owner+' owns '+typ+' treatment-history confirmation'},403
   if not dt or not desc:return {'error':'Treatment date and description required'},409
   if status!='Completed':return {'error':'Treatment-completion review can only be initiated from a completed treatment-history event'},409
   rows=list(hist['data'].get('episodes',[]));x={'id':'HIST-'+uuid.uuid4().hex[:8].upper(),'type':typ,'episode_id':ep['id'],'date':dt,'status':'Completed','description':desc,'source_record_id':d.get('source_record_id',''),'source_document_id':d.get('source_document_id',''),'entered_reason':d.get('entered_reason','Historical/externally completed treatment entered by treating clinician'),'recorded_by':actor(role),'recorded_at':now()};rows.append(x);update_rec(c,hist['id'],{'episodes':rows},'Active',role,'TREATMENT_HISTORY_EVENT','Completed treatment history');complete_open_tasks(c,pid,role,'Historical treatment confirmation',completed_by=role)
   tid=''
   if bool(d.get('trigger_completion_review')):
    tc=latest(c,pid,'treatment_completion')
    if not tc or tc['status'] in ['Signed','Superseded']:
     rid=new_record(c,pid,'treatment_completion',{'episode_id':ep['id'],'source_treatment_history_id':hist['id'],'source_history_event_id':x['id']},'Draft',role);tc=get_rec(c,rid)
    else:update_rec(c,tc['id'],{'episode_id':ep['id'],'source_treatment_history_id':hist['id'],'source_history_event_id':x['id']},'Draft',role,'TREATMENT_COMPLETION_INIT')
    tid=handoff(c,pid,role,'Complete End-of-Treatment Review / Cancer Treatment Summary','Treatment completion review','treatment_history',hist['id'],role,'High','Completed cancer-directed treatment documented; formal end-of-treatment review required',{'history_event':x,'treatment_completion_id':tc['id'],'episode_id':ep['id']})
    journey_add(c,pid,'Treatment Completion','Treatment Completion Review Due','Open',role,'treatment_history',hist['id'],desc,False)
   return {'ok':True,'history_event':x,'treatment_history_id':hist['id'],'task_id':tid,'next_role':role if tid else ''},200
  if a=='save_treatment_completion':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Treating oncology clinician required'},403
   cur=e if e and e.get('entity_type')=='treatment_completion' else latest(c,pid,'treatment_completion')
   if not cur:rid=new_record(c,pid,'treatment_completion',{},'Draft',role);cur=get_rec(c,rid)
   amend_reason=str(d.get('amendment_reason') or '').strip()
   if cur['status']=='Signed':
    if not amend_reason:return {'error':'Signed End-of-Treatment Review is immutable; amendment_reason is required to create a superseding version','supersedes':cur['id']},409
    old=cur;rid=new_record(c,pid,'treatment_completion',{**old['data'],'supersedes':old['id'],'amendment_reason':amend_reason,'amendment_started_by':actor(role),'amendment_started_at':now()},'Draft',role);cur=get_rec(c,rid);update_rec(c,old['id'],{'superseded_by_record_id':rid,'superseded_reason':amend_reason},'Superseded',role,'TREATMENT_COMPLETION_SUPERSEDE',amend_reason);cancel_open_tasks(c,pid,task_type='Survivorship planning',source_type='treatment_completion',source_id=old['id'],cancelled_by=role,reason='Source Treatment Summary superseded: '+amend_reason)
   sign=bool(d.get('sign'));req=['treatment_completed','completion_date','diagnosis_at_completion','treatment_received','current_disease_status','late_effect_risks','follow_up_recommendations'];miss=[k for k in req if d.get(k,cur['data'].get(k)) in ['',None,[]]]
   if sign and miss:return {'error':'End-of-Treatment Review incomplete','missing':miss},409
   ep=current_episode(c,pid) or ensure_episode(c,pid,role);hist=latest(c,pid,'treatment_history');completed=[x for x in (hist or {}).get('data',{}).get('episodes',[]) if x.get('episode_id')==ep['id'] and x.get('status')=='Completed' and x.get('type') in ['Systemic Therapy','Radiation Therapy','Surgery','Other Cancer-Directed Treatment']]
   if sign and not completed:return {'error':'At least one completed cancer-directed treatment-history event is required before signing End-of-Treatment Review','blocking_role':role},409
   vals={**cur['data'],**{k:v for k,v in d.items() if k not in ['sign','amendment_reason']}};vals['episode_id']=ep['id'];vals['source_treatment_history_id']=(hist or {}).get('id','');vals['source_completed_treatment_event_ids']=[x.get('id') for x in completed]
   if sign:vals.update({'signed_by':actor(role),'signed_at':now(),'treatment_summary':{'diagnosis':vals['diagnosis_at_completion'],'treatment_received':vals['treatment_received'],'completion_date':vals['completion_date'],'disease_status':vals['current_disease_status'],'late_effect_risks':vals['late_effect_risks'],'follow_up_recommendations':vals['follow_up_recommendations']},'signed_snapshot':{'episode_id':ep['id'],'completed_treatment_event_ids':[x.get('id') for x in completed],'diagnosis_at_completion':vals['diagnosis_at_completion'],'treatment_received':vals['treatment_received'],'completion_date':vals['completion_date'],'current_disease_status':vals['current_disease_status'],'late_effect_risks':vals['late_effect_risks'],'follow_up_recommendations':vals['follow_up_recommendations']}})
   update_rec(c,cur['id'],vals,'Signed' if sign else 'Draft',role,'TREATMENT_COMPLETION_SIGN' if sign else 'TREATMENT_COMPLETION_SAVE')
   if sign:
    complete_open_tasks(c,pid,role,'Treatment completion review',source_type='treatment_history',source_id=(hist or {}).get('id'),completed_by=role);handoff(c,pid,'Nurse Navigator','Create survivorship / surveillance plan','Survivorship planning','treatment_completion',cur['id'],role,'High','Signed Cancer Treatment Summary available',{'treatment_summary_id':cur['id'],'episode_id':ep['id'],'summary':vals['treatment_summary'],'source_completed_treatment_event_ids':vals['source_completed_treatment_event_ids']});journey_add(c,pid,'Treatment Completion','End-of-Treatment Review Signed','Survivorship Planning',role,'treatment_completion',cur['id'],'',True)
   return {'ok':True,'id':cur['id'],'status':'Signed' if sign else 'Draft','supersedes':cur['data'].get('supersedes',''),'next_role':'Nurse Navigator' if sign else ''},200
  if a=='save_survivorship_plan':
   if role!='Nurse Navigator':return {'error':'Nurse Navigator required'},403
   src=get_rec(c,d.get('treatment_completion_id')) if d.get('treatment_completion_id') else latest_usable(c,pid,'treatment_completion',['Signed'])
   if not src or src.get('status')!='Signed':return {'error':'Signed End-of-Treatment Review / Cancer Treatment Summary required'},409
   cur=e if e and e.get('entity_type')=='survivorship' else latest(c,pid,'survivorship')
   if not cur:rid=new_record(c,pid,'survivorship',{},'Draft',role);cur=get_rec(c,rid)
   amend_reason=str(d.get('amendment_reason') or '').strip()
   if cur['status']=='Signed':
    if not amend_reason:return {'error':'Signed Survivorship Plan is immutable; amendment_reason is required to create a superseding version','supersedes':cur['id']},409
    old=cur;rid=new_record(c,pid,'survivorship',{**old['data'],'supersedes':old['id'],'amendment_reason':amend_reason,'amendment_started_by':actor(role),'amendment_started_at':now()},'Draft',role);cur=get_rec(c,rid);update_rec(c,old['id'],{'superseded_by_record_id':rid,'superseded_reason':amend_reason},'Superseded',role,'SURVIVORSHIP_SUPERSEDE',amend_reason);cancel_open_tasks(c,pid,task_type='Surveillance encounter',source_type='survivorship',source_id=old['id'],cancelled_by=role,reason='Source Survivorship Plan superseded: '+amend_reason)
   sign=bool(d.get('sign'));req=['surveillance_schedule','late_effect_monitoring','health_promotion','red_flags','contact_plan'];vals={**cur['data'],**{k:v for k,v in d.items() if k not in ['sign','amendment_reason']}};miss=[k for k in req if vals.get(k) in ['',None,[]]]
   if sign and miss:return {'error':'Survivorship plan incomplete','missing':miss},409
   vals.update({'episode_id':src['data'].get('episode_id'),'source_treatment_completion_id':src['id'],'source_treatment_completion_version':src['version']})
   if sign:vals.update({'signed_by':actor(role),'signed_at':now(),'signed_snapshot':{k:vals.get(k) for k in req+['episode_id','source_treatment_completion_id','source_treatment_completion_version','next_surveillance_at']}})
   update_rec(c,cur['id'],vals,'Signed' if sign else 'Draft',role,'SURVIVORSHIP_SIGN' if sign else 'SURVIVORSHIP_SAVE');complete_open_tasks(c,pid,role,'Survivorship planning',source_type='treatment_completion',source_id=src['id'],completed_by=role)
   if sign:handoff(c,pid,'Nurse Navigator','Perform scheduled surveillance encounter','Surveillance encounter','survivorship',cur['id'],role,'Routine','Signed surveillance plan active',{'survivorship_plan_id':cur['id'],'episode_id':vals['episode_id'],'source_treatment_completion_id':src['id']},d.get('next_surveillance_at',''));journey_add(c,pid,'Survivorship','Surveillance Plan Signed','Surveillance',role,'survivorship',cur['id'],'',True)
   return {'ok':True,'id':cur['id'],'status':'Signed' if sign else 'Draft','supersedes':cur['data'].get('supersedes','')},200
  if a=='record_surveillance':
   if role not in ['Nurse Navigator','Medical Oncology','Radiation Oncology','Surgical Oncology']:return {'error':'Surveillance care-team role required'},403
   surv=e if e and e.get('entity_type')=='surveillance' else latest(c,pid,'surveillance')
   if not surv:rid=new_record(c,pid,'surveillance',{'encounters':[],'disease_status_events':[]},'Active',role);surv=get_rec(c,rid)
   plan=latest_usable(c,pid,'survivorship',['Signed'])
   if not plan:return {'error':'Signed Survivorship/Surveillance Plan required'},409
   req=['date','assessment','disease_status'];miss=[k for k in req if not d.get(k)]
   if miss:return {'error':'Surveillance encounter incomplete','missing':miss},409
   ep=current_episode(c,pid)
   if not ep or ep['id']!=plan['data'].get('episode_id'):return {'error':'Active Cancer Episode does not match Survivorship Plan provenance'},409
   rows=list(surv['data'].get('encounters',[]));x={'id':'SURV-'+uuid.uuid4().hex[:7].upper(),'episode_id':ep['id'],'date':d['date'],'assessment':d['assessment'],'disease_status':d['disease_status'],'symptoms':d.get('symptoms',[]),'investigations':d.get('investigations',[]),'recorded_by':actor(role),'recorded_at':now()};rows.append(x);update_rec(c,surv['id'],{'encounters':rows},'Active',role,'SURVEILLANCE_ENCOUNTER',d['disease_status']);complete_open_tasks(c,pid,role,'Surveillance encounter',source_type='survivorship',source_id=plan['id'],completed_by=role)
   suspected=str(d['disease_status']).lower() in ['suspected recurrence','suspected progression','possible recurrence','possible progression'] or bool(d.get('suspected_progression'))
   if suspected:handoff(c,pid,'Medical Oncology','Confirm suspected recurrence/progression','Progression confirmation','surveillance',surv['id'],role,'High','Surveillance raised suspected recurrence/progression',{'surveillance_encounter':x,'episode_id':ep['id']})
   return {'ok':True,'encounter':x,'next_role':'Medical Oncology' if suspected else ''},200
  if a=='confirm_progression':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   surv=e if e and e.get('entity_type')=='surveillance' else latest(c,pid,'surveillance');ep=current_episode(c,pid)
   if not surv or not ep:return {'error':'Active surveillance record and Cancer Episode required'},409
   status=d.get('disease_status');allowed=['Confirmed Recurrence','Confirmed Progression','No Recurrence / Stable'];reason=str(d.get('evidence_summary') or '').strip()
   if status not in allowed or not reason:return {'error':'Structured disease-status confirmation and evidence summary required','allowed':allowed},409
   events=list(surv['data'].get('disease_status_events',[]));x={'id':'DSE-'+uuid.uuid4().hex[:7].upper(),'episode_id':ep['id'],'disease_status':status,'evidence_summary':reason,'evidence_source_ids':d.get('evidence_source_ids',[]),'confirmed_by':actor(role),'confirmed_at':now()};events.append(x);update_rec(c,surv['id'],{'disease_status_events':events},'Active',role,'DISEASE_STATUS_CONFIRM',status);complete_open_tasks(c,pid,role,'Progression confirmation',source_type='surveillance',source_id=surv['id'],completed_by=role)
   if status in ['Confirmed Recurrence','Confirmed Progression']:
    hist=latest(c,pid,'treatment_history');lines=[z for z in (hist or {}).get('data',{}).get('episodes',[]) if z.get('type')=='Line of Therapy'];line_no=len(lines)+1;evt={'type':'Line of Therapy','episode_id':ep['id'],'line_number':line_no,'disease_status':status,'started_at':now(),'source_status_event_id':x['id'],'status':'Planning'}
    if hist:rows=list(hist['data'].get('episodes',[]));rows.append(evt);update_rec(c,hist['id'],{'episodes':rows},'Active',role,'NEW_LINE_OF_THERAPY',status)
    m=latest(c,pid,'mdt');
    if not m or m['status'] in ['MDT Recommended','Superseded','Cancelled']:rid=new_record(c,pid,'mdt',{'case_no':'MDT-'+uuid.uuid4().hex[:6].upper(),'attendees':[]},'Draft',role);m=get_rec(c,rid)
    update_rec(c,m['id'],{'clinical_question':'Review '+status+' and define next line of therapy','clinical_summary':reason,'intent':m['data'].get('intent') or 'Curative','recommendation':m['data'].get('recommendation') or 'Pending MDT discussion','rationale':m['data'].get('rationale') or reason,'final_consensus':m['data'].get('final_consensus') or 'Deferred pending information','specialty_responsible':m['data'].get('specialty_responsible') or 'Medical Oncology','episode_id':ep['id'],'source_status_event_id':x['id']},'Draft',role,'MDT_CASE_SUBMIT',status);handoff(c,pid,'MDT Coordinator','Prepare recurrence/progression MDT','MDT case preparation','mdt',m['id'],role,'High',status,{'disease_status_event':x,'line_number':line_no,'episode_id':ep['id']});journey_add(c,pid,'MDT / Tumour Board',status+' — New Line Planning','Draft',role,'mdt',m['id'],reason,True);return {'ok':True,'status_event':x,'episode_id_before':ep['id'],'episode_id_after':current_episode(c,pid)['id'],'line_number':line_no,'mdt_id':m['id'],'next_role':'MDT Coordinator'},200
   return {'ok':True,'status_event':x,'episode_id':ep['id']},200
  if a=='refer_support_service':
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator','Inpatient Oncology Clinician','Inpatient Oncology Nurse','Day Care / Infusion Nurse','Intake Nurse']:return {'error':'Care-team role required to create support referral'},403
   target=d.get('target_role');allowed=['Nurse Navigator','Dietitian / Nutrition','Psycho-Oncology','Palliative Care','Clinical Trials / Research','Stoma / Wound Nurse','Anaesthetist','Blood Bank / Transfusion','Health Information Management']
   if target not in allowed:return {'error':'Governed support-service target required','allowed':allowed},409
   reason=str(d.get('reason') or '').strip()
   if not reason:return {'error':'Referral reason required'},409
   tid=handoff(c,pid,target,d.get('title') or ('Support referral: '+target),'Support service referral',d.get('source_type') or 'care_plan',d.get('source_id') or ((latest(c,pid,'care_plan') or {}).get('id','')),role,d.get('priority','Routine'),reason,{'referrer_role':role,'reason':reason,'context':d.get('context',{})},d.get('due_at',''));journey_add(c,pid,target,'Support Service Referral','Open',role,'task',tid,reason,False);return {'ok':True,'task_id':tid,'next_role':target},200
  if a=='save_support_record':
   owner_map={'navigation':'Nurse Navigator','anaesthesia':'Anaesthetist','blood_bank':'Blood Bank / Transfusion','stoma_wound':'Stoma / Wound Nurse','nutrition':'Dietitian / Nutrition','psychosocial':'Psycho-Oncology','palliative':'Palliative Care','clinical_trial':'Clinical Trials / Research','him':'Health Information Management','pathology_processing':'Pathology Technologist','rt_planning':'Radiation Dosimetrist / Planner'};typ=str(d.get('record_type') or '');owner=owner_map.get(typ)
   if not owner:return {'error':'Unsupported supporting-service record type','allowed':sorted(owner_map)},409
   if role!=owner:return {'error':owner+' required for '+typ},403
   sign=bool(d.get('sign'));reason=str(d.get('amendment_reason') or '').strip();cur=e if e and e.get('entity_type')==typ else latest(c,pid,typ)
   ev=req.get('expected_version')
   if cur and ev not in [None,'']:
    try:evi=int(ev)
    except:return {'error':'expected_version must be an integer','current_version':cur['version']},409
    if evi!=int(cur['version']):return {'error':'Record changed since it was loaded','expected_version':evi,'current_version':cur['version'],'record_id':cur['id']},409
   if cur and cur['status']=='Signed':
    if not reason:return {'error':'Signed '+typ+' record is immutable; amendment_reason required','supersedes':cur['id']},409
    old_id=cur['id'];rid=new_record(c,pid,typ,{**cur['data'],'supersedes':old_id,'amendment_reason':reason},'Draft',role);update_rec(c,old_id,{'superseded_by_record_id':rid},'Superseded',role,'SUPPORT_SUPERSEDE',reason);cancel_open_tasks(c,pid,source_type=typ,source_id=old_id,cancelled_by=role,reason='Source support record superseded by '+rid);cur=get_rec(c,rid)
   if not cur:rid=new_record(c,pid,typ,{},'Draft',role);cur=get_rec(c,rid)
   reqmap={'navigation':['contact_type','barriers','plan','next_step'],'anaesthesia':['assessment_date','asa_class','airway_assessment','anesthesia_plan','fitness_decision'],'blood_bank':['assessment_date','blood_group','antibody_screen','crossmatch_status','availability_status'],'stoma_wound':['assessment_date','wound_status','drain_status','stoma_status','plan'],'nutrition':['assessment_date','weight_kg','intake_assessment','nutrition_diagnosis','intervention_plan','monitoring_plan'],'psychosocial':['assessment_date','distress_score','risk_level','intervention_plan','care_team_summary'],'palliative':['assessment_date','symptom_summary','goals_of_care_status','plan'],'clinical_trial':['trial_id','protocol_version','screening_status','consent_status'],'him':['operation_type','reason','status'],'pathology_processing':['accession_id','specimen_received_at','grossing_status','blocks_slides_status','ready_for_pathologist'],'rt_planning':['plan_id','planning_system','plan_status']}
   vals={**cur['data'],**{k:v for k,v in d.items() if k not in ['record_type','sign','amendment_reason']}}
   if sign:
    miss=[x for x in reqmap.get(typ,[]) if vals.get(x) in ['',None,[]]]
    if miss:return {'error':typ+' record incomplete','missing':miss},409
    if typ=='psychosocial':
     try:ds=float(vals.get('distress_score'))
     except:return {'error':'Distress score must be numeric'},409
     if ds<0 or ds>10:return {'error':'Distress score must be 0–10'},409
    if typ=='nutrition':
     try:float(vals.get('weight_kg'))
     except:return {'error':'Nutrition weight must be numeric'},409
     vals['weight_unit']='kg'
    vals.update({'signed_by':actor(role),'signed_at':now(),'signed_snapshot':{k:vals.get(k) for k in reqmap.get(typ,[])}})
   update_rec(c,cur['id'],vals,'Signed' if sign else 'Draft',role,'SUPPORT_SIGN' if sign else 'SUPPORT_SAVE',typ)
   if sign:
    refrow=c.execute("SELECT * FROM tasks WHERE patient_id=? AND owner_role=? AND task_type='Support service referral' AND status IN ('Open','Acknowledged') ORDER BY created_at DESC LIMIT 1",(pid,role)).fetchone();reft=task_row(refrow) if refrow else None;referrer=((reft or {}).get('data') or {}).get('referrer_role') or 'Medical Oncology';referrer=referrer if referrer in ROLES else 'Medical Oncology'
    if reft:complete_open_tasks(c,pid,role,'Support service referral',source_type=reft.get('source_type'),source_id=reft.get('source_id'),completed_by=role)
    if typ=='anaesthesia':handoff(c,pid,'Surgical Nurse','Update surgical pre-op readiness after anaesthesia assessment','Surgical pre-op','anaesthesia',cur['id'],role,'High',vals.get('fitness_decision',''),{'anaesthesia_record_id':cur['id'],'fitness_decision':vals.get('fitness_decision')})
    elif typ=='blood_bank':handoff(c,pid,'Surgical Nurse','Update theatre readiness with Blood Bank status','Surgical pre-op','blood_bank',cur['id'],role,'High',vals.get('availability_status',''),{'blood_bank_record_id':cur['id'],'availability_status':vals.get('availability_status')})
    elif typ=='pathology_processing':
     path=get_rec(c,vals.get('pathology_record_id')) if vals.get('pathology_record_id') else latest(c,pid,'pathology')
     if path:update_rec(c,path['id'],{'accession_id':vals.get('accession_id'),'specimen_received_at':vals.get('specimen_received_at'),'grossing_status':vals.get('grossing_status'),'blocks_slides_status':vals.get('blocks_slides_status'),'processing_record_id':cur['id']},'Processing Complete' if vals.get('ready_for_pathologist') else path['status'],role,'PATH_PROCESSING_SYNC')
     if vals.get('ready_for_pathologist') and path:handoff(c,pid,'Pathology','Interpret and sign pathology report','Pathology reporting','pathology',path['id'],role,'High','Specimen processing complete',{'processing_record_id':cur['id'],'accession_id':vals.get('accession_id')})
    elif typ=='nutrition':handoff(c,pid,referrer,'Review Dietitian recommendation','Support result review','nutrition',cur['id'],role,'Routine','Signed nutrition assessment available',{'nutrition_record_id':cur['id'],'care_team_summary':vals.get('intervention_plan')})
    elif typ=='psychosocial':handoff(c,pid,referrer,'Review Psycho-Oncology care-team summary','Support result review','psychosocial',cur['id'],role,'High' if vals.get('risk_level') in ['High','Critical'] else 'Routine','Minimum-necessary Psycho-Oncology summary available',{'psychosocial_record_id':cur['id'],'care_team_summary':vals.get('care_team_summary'),'risk_level':vals.get('risk_level')})
    elif typ=='palliative':handoff(c,pid,referrer,'Review Palliative Care recommendations','Support result review','palliative',cur['id'],role,'High','Signed palliative assessment available',{'palliative_record_id':cur['id'],'plan':vals.get('plan')})
    elif typ=='clinical_trial':handoff(c,pid,referrer,'Review Clinical Trials screening status','Clinical trial review','clinical_trial',cur['id'],role,'High','Trials coordinator update',{'trial_id':vals.get('trial_id'),'screening_status':vals.get('screening_status'),'consent_status':vals.get('consent_status')})
    elif typ=='stoma_wound':handoff(c,pid,referrer if referrer in ['Surgical Oncology','Inpatient Oncology Clinician','Medical Oncology'] else 'Surgical Oncology','Review wound/stoma assessment','Support result review','stoma_wound',cur['id'],role,'High' if vals.get('risk_flag') in ['High','Urgent'] else 'Routine','Signed wound/stoma record available',{'record_id':cur['id'],'plan':vals.get('plan')})
    elif typ=='navigation':handoff(c,pid,referrer,'Review Nurse Navigation coordination result','Support result review','navigation',cur['id'],role,'Routine','Signed navigation/care-coordination record available',{'record_id':cur['id'],'next_step':vals.get('next_step'),'barriers':vals.get('barriers',[])})
    elif typ=='him':handoff(c,pid,referrer,'Review HIM request outcome','Support result review','him',cur['id'],role,'Routine','Signed HIM correction/reconciliation outcome available',{'record_id':cur['id'],'operation_type':vals.get('operation_type'),'status':vals.get('status'),'reason':vals.get('reason')})
    elif typ=='rt_planning':handoff(c,pid,referrer if referrer in ['Radiation Oncology','Radiation Physicist','Radiation Technologist'] else 'Radiation Oncology','Review RT planning status','Support result review','rt_planning',cur['id'],role,'Routine','Signed RT planning update available',{'record_id':cur['id'],'plan_status':vals.get('plan_status')})
   return {'ok':True,'id':cur['id'],'status':'Signed' if sign else 'Draft'},200
  return {'error':'Unknown action'},404

if __name__=='__main__':
 if DEPLOYMENT_MODE=='production' and ALLOW_SHARED_ROLE_LOGIN:raise SystemExit('Refusing production startup with shared-role login enabled. Set CCA_ALLOW_SHARED_ROLE_LOGIN=0.')
 init_db();print(f'CCA Cancer Care V12.2 Final Defect Remediation (PC8.0 connected-multidisciplinary) running at http://{HOST}:{PORT}');ThreadingHTTPServer((HOST,PORT),H).serve_forever()
