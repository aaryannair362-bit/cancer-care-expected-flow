#!/usr/bin/env python3
import os, json, sqlite3, uuid, hashlib, hmac, secrets, base64, mimetypes, re, math
from datetime import datetime, timedelta, date
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def _load_dotenv():
 p=ROOT/'.env'
 if not p.exists():return
 for line in p.read_text().splitlines():
  line=line.strip()
  if not line or line.startswith('#') or '=' not in line:continue
  k,v=line.split('=',1);os.environ.setdefault(k.strip(),v.strip().strip('"').strip("'"))
_load_dotenv()

STATIC=ROOT/'static'; DB=ROOT/'cca_v12.sqlite3'
PORT=int(os.environ.get('PORT') or 8765)
SESSION_HOURS=12

ROLES=['Front Desk','Patient Attender','PRE / Patient Relations Executive','Nurse Navigator','Intake Nurse','Medical Oncology','Surgical Oncology','Radiation Oncology','Radiology Coordinator','Radiology Technician','Radiologist','Laboratory / Phlebotomy','Pathology','MDT Coordinator','MDT Chair','External Consultant','Oncology Pharmacy','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Radiation Technologist','Radiation Physicist','Surgical Nurse','Biller','Finance / Billing','Patient Liaison','Hospital Management / Admin']
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

WRITE={
'registration':{'Front Desk','Patient Attender'},'consent':{'Front Desk','Patient Attender','Patient Liaison'},'appointments':{'Front Desk','Patient Attender','PRE / Patient Relations Executive','Radiology Coordinator','Finance / Billing'},'queue':{'Front Desk','PRE / Patient Relations Executive','Nurse Navigator','Radiology Coordinator','Laboratory / Phlebotomy','Finance / Billing','Oncology Pharmacy','Day Care / Infusion Nurse','MDT Coordinator'},
'intake':{'Nurse Navigator','Intake Nurse'},'med_recon':{'Nurse Navigator','Intake Nurse','Medical Oncology'},'dynamic_forms':{'Hospital Management / Admin','Nurse Navigator'},'consultation':{'Medical Oncology'},'diagnosis':{'Medical Oncology','Surgical Oncology','Radiation Oncology'},
'lab_order':{'Medical Oncology'},'radiology_order':{'Medical Oncology'},'lab':{'Laboratory / Phlebotomy'},'radiology':{'Radiologist','Radiology Technician'},'pathology':{'Pathology'},'mdt':{'MDT Coordinator','MDT Chair','Medical Oncology','Surgical Oncology','Radiation Oncology'},'mdt_collab':{'MDT Coordinator','MDT Chair','Medical Oncology','Surgical Oncology','Radiation Oncology'},'mdt_followup':{'MDT Coordinator','MDT Chair'},
'journey':{'Front Desk','Patient Attender','PRE / Patient Relations Executive','Nurse Navigator','Intake Nurse','Medical Oncology','Surgical Oncology','Radiation Oncology','MDT Coordinator','Oncology Pharmacy','Day Care / Infusion Nurse'},'cancer_episode':{'Medical Oncology','Surgical Oncology','Radiation Oncology'},'admission':{'Medical Oncology','Surgical Oncology','Radiation Oncology','Day Care / Infusion Nurse'},'inpatient_care':{'Nurse Navigator','Medical Oncology','Surgical Oncology','Radiation Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Surgical Nurse'},'discharge':{'Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator'},'continuous_therapy':{'Medical Oncology'},'tumor_marker':{'Medical Oncology','Laboratory / Phlebotomy'},'care_plan':{'Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator','Patient Liaison'},'treatment_plan':{'Medical Oncology','Surgical Oncology','Radiation Oncology'},'readiness':{'Medical Oncology'},'treatment_order':{'Medical Oncology'},'pharmacy':{'Oncology Pharmacy'},'infusion':{'Day Care / Infusion Nurse'},'toxicity':{'Medical Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Nurse Navigator'},'modification':{'Medical Oncology'},'response':{'Medical Oncology','Radiologist'},'radiation':{'Radiation Oncology','Radiation Technologist','Radiation Physicist'},'surgery':{'Surgical Oncology','Surgical Nurse'},'finance':{'Finance / Billing','Biller'},'conversion':{'Finance / Billing'},'visit_summary':{'Medical Oncology'},'protocol_library':{'Hospital Management / Admin'},'formulary':{'Hospital Management / Admin'},'standards':{'Hospital Management / Admin'},'cca_requirements':{'Hospital Management / Admin'}}

VALUE_SETS={'ecog':['0','1','2','3','4'],'kps':[str(x) for x in range(0,101,10)],'intent':['Curative','Palliative','Neoadjuvant','Adjuvant','Definitive','Maintenance','Diagnostic','Other'],'route':['IV','PO','IM','SQ','Intrathecal','CIV','Other'],'allergy_severity':['Mild','Moderate','Severe','Life-threatening','Unknown'],'allergy_status':['No known allergy','Allergy present','Unable to verify'],'allergy_source':['Patient','Caregiver','Prior record','External clinician','Observed at CCA','Integrated record'],'allergy_reaction':['Rash','Urticaria','Pruritus','Angioedema','Anaphylaxis','Bronchospasm','Nausea / vomiting','Other','Unknown'],'med_reconciliation_status':['Complete','Incomplete','Unable to verify'],'care_plan_status':['Draft','Proposed','Active','Blocked','On Hold','Completed','Superseded','Cancelled'],'appointment_status':['Scheduled','Rescheduled','No-show','Cancelled','Completed'],'dose_basis':['Fixed','mg/kg','mg/m²','AUC','Other'],'decision':['Proceed as Planned','Proceed with Modification','Hold','Delay','Omit','Substitute','Stop'],'toxicity':['Nausea','Vomiting','Diarrhea','Mucositis','Neutropenia','Thrombocytopenia','Anemia','Fatigue','Neuropathy','Alopecia','Cardiotoxicity','Nephrotoxicity','Hepatotoxicity','Other'],'ctcae_grade':['1','2','3','4','5'],'laterality':['Left','Right','Bilateral','Midline','Not applicable'],'treatment_line':['Neoadjuvant','Adjuvant','1st line','2nd line','3rd line','Subsequent line','Maintenance','Consolidation','Salvage','Other'],'pharmacy_decision':['Verified','Query','Reject'],'completion_status':['Administered','Partially Administered','Held','Stopped'],'rt_frequency':['Daily','5x/week','3x/week','Weekly','Other'],'surgery_priority':['Routine','Urgent','Emergency'],'admission_type':['Planned','Emergency','Unplanned'],'admission_reason':['Treatment / procedure','Treatment toxicity','Infection / febrile neutropenia','Adverse drug reaction','Post-operative care','Brachytherapy procedure','Seizure / neurologic event','Nutrition / dehydration','Other'],'admission_status':['Active','Transferred','Discharged','Deceased'],'care_setting':['OPD','Day Care','IPD'],'continuous_mode':['Oral systemic therapy','Hormonal therapy','Other continuous systemic therapy'],'task_status':['Open','Acknowledged','Completed','Cancelled'],'task_priority':['Routine','High','Critical'],'medication_status':['Continue','Hold','Stopped'],'medication_frequency':['Once daily','Twice daily','Three times daily','Every other day','Weekly','As needed','Other prescribed schedule'],'medication_dose_unit':['mg','mcg','g','mL','tablet','capsule','unit'],'access_type':['Peripheral IV','PICC','Central venous catheter','Port','Oral / no vascular access','Other'],'access_site':['Left upper limb','Right upper limb','Left lower limb','Right lower limb','Chest central access','Not applicable','Other'],'mar_variance_type':['None','Dose variance','Rate variance','Route variance','Timing variance','Sequence variance','Other'],'mar_variance_reason':['Clinician instruction','Infusion reaction','Access issue','Patient condition','Operational delay','Product issue','Other'],'pharmacy_wastage_reason':['Partial vial','Dose rounding','Preparation error','Spill / breakage','Cancelled treatment','Expired / BUD exceeded','Return not reusable','Other']}

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
'items':[
 {'sequence':1,'group':'Premedication','drug':'Dexamethasone','code':'DEMO-DEX','dose_basis':'Fixed','protocol_dose':8,'protocol_unit':'mg','route':'PO','timing':'30–60 min before systemic therapy'},
 {'sequence':2,'group':'Targeted Therapy','drug':'Pertuzumab','code':'DEMO-PER','dose_basis':'Fixed','protocol_dose':840,'protocol_unit':'mg','route':'IV','diluent':'NS','volume_ml':250,'duration_min':60},
 {'sequence':3,'group':'Targeted Therapy','drug':'Trastuzumab','code':'DEMO-TRA','dose_basis':'mg/kg','protocol_dose':8,'protocol_unit':'mg/kg','route':'IV','diluent':'NS','volume_ml':250,'duration_min':90},
 {'sequence':4,'group':'Antineoplastic','drug':'Docetaxel','code':'DEMO-DOC','dose_basis':'mg/m²','protocol_dose':75,'protocol_unit':'mg/m²','route':'IV','diluent':'NS','volume_ml':250,'duration_min':60},
 {'sequence':5,'group':'Antineoplastic','drug':'Carboplatin','code':'DEMO-CARBO','dose_basis':'AUC','protocol_dose':6,'protocol_unit':'AUC','route':'IV','diluent':'D5W','volume_ml':250,'duration_min':60},
 {'sequence':6,'group':'Supportive','drug':'Pegfilgrastim','code':'DEMO-PEG','dose_basis':'Fixed','protocol_dose':6,'protocol_unit':'mg','route':'SQ','timing':'Per institutional policy'}]}
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


def now(): return datetime.now().astimezone().isoformat(timespec='seconds')
def jdump(x): return json.dumps(x,separators=(',',':'),ensure_ascii=False)
def jload(s,d=None):
    try:return json.loads(s)
    except:return {} if d is None else d

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
 CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY,patient_id TEXT,title TEXT,filename TEXT,mime TEXT,category TEXT,document_type TEXT,source_institution TEXT,document_date TEXT,content BLOB,uploaded_by TEXT,uploaded_at TEXT);
 CREATE TABLE IF NOT EXISTS external_tokens(token TEXT PRIMARY KEY,patient_id TEXT,consultant_name TEXT,discipline TEXT,expires_at TEXT,created_by TEXT,created_at TEXT);
 CREATE TABLE IF NOT EXISTS content_sources(id TEXT PRIMARY KEY,name TEXT,source_url TEXT,license_status TEXT,license_name TEXT,commercial_use TEXT,status TEXT,notes TEXT,created_at TEXT,updated_at TEXT);
 CREATE TABLE IF NOT EXISTS content_templates(id TEXT PRIMARY KEY,category TEXT,name TEXT,subtype TEXT,disease TEXT,setting TEXT,intent TEXT,line_of_therapy TEXT,version TEXT,status TEXT,governance_status TEXT,orderable INTEGER,source_id TEXT,source_ref TEXT,effective_date TEXT,review_due TEXT,clinical_owner TEXT,pharmacy_owner TEXT,data_json TEXT,created_at TEXT,updated_at TEXT,approved_by TEXT,approved_at TEXT,retired_at TEXT);
 CREATE TABLE IF NOT EXISTS content_formulary(id TEXT PRIMARY KEY,drug TEXT,display_name TEXT,code_system TEXT,code TEXT,version TEXT,status TEXT,source_id TEXT,source_ref TEXT,routes_json TEXT,diluents_json TEXT,formulations_json TEXT,rounding_policy TEXT,notes TEXT,pharmacy_review_json TEXT,created_at TEXT,updated_at TEXT,approved_by TEXT,approved_at TEXT,retired_at TEXT);
 CREATE TABLE IF NOT EXISTS role_surface_reviews(id TEXT PRIMARY KEY,role_surface TEXT,reviewer_role TEXT,reviewer_actor_id TEXT,verdict TEXT,note TEXT,at TEXT);
 CREATE TABLE IF NOT EXISTS patient_access(patient_id TEXT,role TEXT,scope_type TEXT,source_id TEXT,active INTEGER,granted_at TEXT,granted_by TEXT,PRIMARY KEY(patient_id,role,scope_type,source_id));
 CREATE INDEX IF NOT EXISTS idx_patient_access_role ON patient_access(role,patient_id,active);
 CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY,patient_id TEXT,episode_id TEXT,task_type TEXT,title TEXT,status TEXT,priority TEXT,owner_role TEXT,owner_user_id TEXT,source_type TEXT,source_id TEXT,due_at TEXT,acknowledged_at TEXT,acknowledged_by TEXT,completed_at TEXT,completed_by TEXT,escalation_level INTEGER,reason TEXT,data_json TEXT,created_at TEXT,created_by TEXT,updated_at TEXT,updated_by TEXT);
 CREATE INDEX IF NOT EXISTS idx_tasks_patient_owner ON tasks(patient_id,owner_role,status,due_at);
 '''); c.commit(); seed_content_master(c); c.commit(); c.close(); seed()

def actor(role): return USERS.get(role,{'id':'USR-UNKNOWN','name':role,'role':role})
def audit(c,pid,role,action,etype='',eid='',detail=''):
 last=c.execute('SELECT hash FROM audit ORDER BY id DESC LIMIT 1').fetchone(); prev=last['hash'] if last else 'GENESIS'; at=now(); raw='|'.join([prev,pid or '',actor(role)['id'],role,action,etype or '',eid or '',detail or '',at]); h=hashlib.sha256(raw.encode()).hexdigest(); c.execute('INSERT INTO audit(patient_id,actor_id,actor_role,action,entity_type,entity_id,detail,at,prev_hash,hash) VALUES(?,?,?,?,?,?,?,?,?,?)',(pid,actor(role)['id'],role,action,etype,eid,detail,at,prev,h))

def new_record(c,pid,typ,data,status='Draft',role='System',rid=None):
 rid=rid or f'{typ.upper()}-{uuid.uuid4().hex[:10].upper()}'; t=now(); c.execute('INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?)',(rid,pid,typ,status,1,jdump(data),t,t,actor(role)['id'],actor(role)['id'])); c.execute('INSERT INTO record_versions(record_id,patient_id,entity_type,version,status,data_json,actor_id,actor_role,reason,at) VALUES(?,?,?,?,?,?,?,?,?,?)',(rid,pid,typ,1,status,jdump(data),actor(role)['id'],role,'Created',t)); audit(c,pid,role,'CREATE',typ,rid,status); return rid

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
 try: payload=json.loads(path.read_text())
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
  try:qa=json.loads(qa_path.read_text())
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

def seed():
 c=db()
 if c.execute('SELECT COUNT(*) n FROM patients').fetchone()['n']:
  c.close();return
 p={'id':'PAT-0001','mrn':'CCA-DEMO-0001','name':'Maya Iyer','dob':'1980-02-11','sex':'Female','phone':'+91 90000 01001','abha':'91-1111-2222-3333','id_number':'AADHAAR-DEMO-1001','current_department':'Medical Oncology','status':'Active','photo_document_id':''}
 t=now(); c.execute('INSERT INTO patients VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(p['id'],p['mrn'],p['name'],p['dob'],p['sex'],p['phone'],p['abha'],p['id_number'],p['current_department'],p['status'],p['photo_document_id'],t,t))
 pid=p['id']
 new_record(c,pid,'registration',{'arrival_type':'Clinician specified','assigned_specialty':'Medical Oncology','clinician_assignment':'Medical Oncology Clinic','route_rule':'Clinician assignment','referral_doctor_name':'Dr External Referrer','referral_facility':'Outside Hospital','referral_network_level3':'External referral source','referral_reason':'Breast cancer opinion','address':'Hyderabad','general_consent':'Signed','photo_status':'Pending'},'Completed','System','REG-0001')
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

def readiness_eval(data,protocol=None):
 protocol=protocol or PROTOCOL
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
   age=(date.today()-date.fromisoformat(str(ld)[:10])).days;freshness='Current' if age<=hp['lab_max_age_days'] else 'Stale'
   if freshness=='Stale':blockers.append(f'Required labs are stale ({age} days old; max {hp["lab_max_age_days"]})')
  except: blockers.append('Laboratory date is invalid');freshness='Invalid'
 def rr(rid,cat,field,current,unit,op,threshold,ok,source='lab'):
  return {'id':rid,'category':cat,'field':field,'current':current,'unit':unit,'operator':op,'threshold':threshold,'status':'PASS' if ok else 'HOLD','outcome':'PASS' if ok else 'HOLD','source_record_id':data.get('lab_source_id','') if source=='lab' else data.get('toxicity_source_id',''),'source_finalized_at':data.get('lab_source_finalized_at','') if source=='lab' else '', 'result_date':ld if source=='lab' else '', 'freshness_days':age if source=='lab' else None,'freshness_status':freshness if source=='lab' else 'Not applicable'}
 ok_anc=anc is not None and anc>=hp['ANC_min']; ok_plt=plt is not None and plt>=hp['platelets_min']; ok_egfr=egfr>=hp['eGFR_min']; ok_bili=bili is not None and bili<=hp['bilirubin_max']; ok_lvef=lvef>=hp['LVEF_min']
 if not ok_anc:blockers.append(f"ANC does not meet protocol criteria ({anc if anc is not None else 'missing/invalid unit'} vs min {hp['ANC_min']} ×10^9/L)")
 if not ok_plt:blockers.append(f"Platelets do not meet protocol criteria ({plt if plt is not None else 'missing/invalid unit'} vs min {hp['platelets_min']} ×10^9/L)")
 if not ok_egfr:blockers.append(f"eGFR does not meet protocol criteria ({egfr} vs min {hp['eGFR_min']})")
 if not ok_bili:blockers.append(f"Bilirubin exceeds protocol demo threshold ({bili if bili is not None else 'missing/invalid unit'} vs max {hp['bilirubin_max']} mg/dL)")
 if not ok_lvef:blockers.append(f"LVEF does not meet protocol criteria ({lvef} vs min {hp['LVEF_min']}%)")
 if data.get('pregnancy') not in ['Negative','N/A','Not applicable']: alerts.append('Pregnancy status requires clinical review')
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
 return {'protocol_id':protocol['id'],'protocol_version':protocol['version'],'thresholds_source':'Institution Content Master / server-governed regimen version','lab_source_id':data.get('lab_source_id',''),'lab_source_finalized_at':data.get('lab_source_finalized_at',''),'normalized':normalized,'blockers':blockers,'alerts':alerts,'can_proceed':not blockers,'rule_results':rule_results,'monitoring_requirements':monitoring,'dose_modification_rules':protocol.get('dose_modification_rules',[]),'evaluated_at':now()}

def calc_dose(item,weight,bsa):
 if item['dose_basis']=='Fixed':return float(item['protocol_dose'])
 if item['dose_basis']=='mg/kg':return round(float(item['protocol_dose'])*float(weight),2)
 if item['dose_basis']=='mg/m²':return round(float(item['protocol_dose'])*float(bsa),2)
 if item['dose_basis']=='AUC':return None
 return None

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

class H(BaseHTTPRequestHandler):
 server_version='CCA-V12.2-PC1.9/1.0'
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
  return dict(r)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=='/api/health':return self.sendj({'ok':True,'product':'CCA Cancer Care HIS + Oncology EMR V12.2 Structural Conformance','version':'12.2','build':'12.2-PC1.9','date':'2026-09-05','synthetic_test_content':True})
  if p.path.startswith('/static/') or p.path=='/':
   rel='index.html' if p.path=='/' else p.path[len('/static/'):];f=STATIC/rel
   if not f.exists():self.send_error(404);return
   mime=mimetypes.guess_type(f.name)[0] or 'application/octet-stream';b=f.read_bytes();self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b);return
  c=db(); s=self.auth(c)
  if not s:c.close();return self.sendj({'error':'Authentication required'},401)
  role=s['role']
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
   rows=tasks_for_role(c,role,pid);c.close();return self.sendj({'tasks':rows,'owner_role':role})
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
   role=data.get('role')
   if role not in ROLES:c.close();return self.sendj({'error':'Invalid demo role'},401)
   tok=secrets.token_urlsafe(32);exp=(datetime.now().astimezone()+timedelta(hours=SESSION_HOURS)).isoformat();c.execute('INSERT OR REPLACE INTO sessions VALUES(?,?,?,?)',(tok,actor(role)['id'],role,exp));c.commit();c.close();return self.sendj({'token':tok,'actor':actor(role),'expires_at':exp})
  if p.path=='/api/logout':
   tok=self.headers.get('Authorization','').removeprefix('Bearer ').strip()
   if tok:c.execute('DELETE FROM sessions WHERE token=?',(tok,));c.commit()
   c.close();return self.sendj({'ok':True,'session_revoked':True})
  s=self.auth(c)
  if not s:c.close();return self.sendj({'error':'Authentication required'},401)
  role=s['role']
  if p.path=='/api/patient':
   if role not in ['Front Desk','Patient Attender']:c.close();return self.sendj({'error':'Front Desk/Patient Attender required'},403)
   name=str(data.get('name','')).strip();dob=str(data.get('dob','')).strip();phone=str(data.get('phone','')).strip();abha=str(data.get('abha','')).strip();idn=str(data.get('id_number','')).strip()
   if not all([name,dob,phone,idn]):c.close();return self.sendj({'error':'Name, DOB, phone and ID number are mandatory'},409)
   ok_dob,msg=valid_dob(dob)
   if not ok_dob:c.close();return self.sendj({'error':msg},409)
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
   new_record(c,pid,'consent',{'items':[]},'Active',role);new_record(c,pid,'appointments',{'items':[]},'Active',role);new_record(c,pid,'queue',{'current_location':'Front Desk','current_status':'In Service','priority':'Routine','token':'FD-'+uuid.uuid4().hex[:4].upper(),'history':[{'at':t,'from':'Arrival','to':'Front Desk','status':'Arrived','actor':actor(role)['name']}]},'Active',role)
   new_record(c,pid,'journey',{'current_location':'Front Desk','current_care_stage':'Registration','events':[{'id':'JNY-'+uuid.uuid4().hex[:8].upper(),'at':t,'department':'Registration','care_stage':'Registration','clinician':actor(role)['name'],'actor_role':role,'status':'Current','source_type':'registration','source_id':'','note':'Patient arrived'}]},'Active',role);epid=new_record(c,pid,'cancer_episode',{'episode_no':'EP-'+uuid.uuid4().hex[:6].upper(),'kind':'Primary cancer','label':'Oncology episode under evaluation','started_at':t,'ended_at':'','closure_reason':'','primary_diagnosis_id':'','status':'Active'},'Active',role);new_record(c,pid,'admission',{'admissions':[]},'Active',role);new_record(c,pid,'inpatient_care',{'daily_notes':[],'nursing_observations':[],'intake_output':[],'pain_assessments':[],'toxicity_events':[],'specialty_reviews':[],'inpatient_medication_orders':[]},'Active',role);new_record(c,pid,'discharge',{'summaries':[]},'Active',role);new_record(c,pid,'continuous_therapy',{'courses':[]},'Active',role);new_record(c,pid,'tumor_marker',{'measurements':[]},'Active',role)
   new_record(c,pid,'intake',{},'Draft',role);new_record(c,pid,'med_recon',{'items':[],'allergies':[],'allergy_status':'Unable to verify','reconciliation_events':[]},'Draft',role);new_record(c,pid,'dynamic_forms',{'definitions':latest(c,'PAT-0001','dynamic_forms')['data']['definitions'],'responses':{}},'Active',role);new_record(c,pid,'consultation',{},'Draft',role);new_record(c,pid,'diagnosis',{'biomarkers':[]},'Draft',role);new_record(c,pid,'care_plan',{'goals':[],'milestones':[],'dependencies':[],'status':'Draft'},'Draft',role);new_record(c,pid,'finance',{'payment_events':[]},'Active',role);new_record(c,pid,'conversion',{'tracking':[]},'Active',role)
   # Empty but real workspaces allow a newly registered patient to traverse the same downstream workflow.
   new_record(c,pid,'pathology',{},'Draft',role);new_record(c,pid,'mdt',{'case_no':'MDT-'+uuid.uuid4().hex[:6].upper(),'attendees':[]},'Draft',role);new_record(c,pid,'mdt_collab',{'comments':[],'attendance':[],'external_consultants':[]},'Active',role);new_record(c,pid,'mdt_followup',{'action_items':[]},'Active',role);new_record(c,pid,'treatment_plan',{'plan_no':'TP-'+uuid.uuid4().hex[:6].upper(),'version':1,'sequence':[],'phases':[]},'Draft',role);new_record(c,pid,'protocol_library',{'protocols':[PROTOCOL]},'Active',role);new_record(c,pid,'formulary',FORMULARY,'Active',role);new_record(c,pid,'readiness',{},'Draft',role);new_record(c,pid,'toxicity',{'events':[]},'Active',role);new_record(c,pid,'modification',{'items':[]},'Active',role);new_record(c,pid,'response',{'baseline':{'target_lesions':[]},'assessments':[]},'Active',role);new_record(c,pid,'radiation',{'prescription':{'status':'Draft'},'planning':{'simulation_status':'Pending','contouring_status':'Pending','planning_status':'Pending','physics_qa':'Pending','physics_qa_plan_version':None,'physics_qa_prescription_version':None,'physician_final_approval':'Pending','physician_approval_plan_version':None,'physician_approval_prescription_version':None,'dicom_refs':{}},'fractions':[],'interruptions':[]},'Draft',role);new_record(c,pid,'surgery',{'plan':{'status':'Recommended'},'preop':{'anesthesia_clearance':'Pending','labs':'Pending','consent':'Pending','ready':False},'outcome':{},'histopathology_link':''},'Recommended',role);new_record(c,pid,'treatment_history',{'episodes':[]},'Active',role);new_record(c,pid,'visit_summary',{},'Draft',role)
   initial=str(data.get('initial_specialty') or 'Medical Oncology');initial_roles={'Medical Oncology':['Medical Oncology'],'Surgical Oncology':['Surgical Oncology'],'Radiation Oncology':['Radiation Oncology']}.get(initial,['Medical Oncology'])
   for rr in ['Nurse Navigator','Intake Nurse','PRE / Patient Relations Executive','Biller','Finance / Billing','Patient Liaison',role]+initial_roles:grant_patient_access(c,pid,rr,'registration',pid,role)
   audit(c,pid,role,'PATIENT_CREATED','patient',pid,'New registration');c.commit();c.close();return self.sendj({'ok':True,'id':pid,'mrn':mrn,'matches':matches})
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
   rows=list(e['data'].get('admissions',[]));rows.append(x);update_rec(c,e['id'],{'admissions':rows},'Active',role,'IPD_ADMISSION',reason_code);grant_patient_access(c,pid,'Inpatient Oncology Nurse','admission',x['id'],role);journey_add(c,pid,'Inpatient Care','Admitted', 'Active',role,'admission',x['id'],reason_code,True);return {'ok':True,'admission':x},200
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
   if role not in ['Medical Oncology','Surgical Oncology','Radiation Oncology']:return {'error':'Oncology specialist required'},403
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
   bmi=round(weight_kg/((height_cm/100)**2),2);bsa=round(math.sqrt(height_cm*weight_kg/3600),2);measured_at=now()
   patch={**d};
   for k in ['sbp','dbp','temp','weight','height']:patch.pop(k,None)
   patch.pop('fall_risk_level',None)
   patch.update({'bp':f'{int(round(sbp))}/{int(round(dbp))}','hr':hr,'rr':rr,'temp_c':round(temp_c,3),'spo2':spo2,'weight_kg':round(weight_kg,4),'height_cm':round(height_cm,3),'bmi':bmi,'bsa_m2':bsa,'bsa_formula':'Mosteller: sqrt(height_cm × weight_kg / 3600)','measurement_units':{'bp':'mmHg','hr':'/min','rr':'/min','temp_c':'°C','spo2':'%','weight_kg':'kg','height_cm':'cm'},'source_measurements':{'sbp':{'value':sbp,'unit':units['bp']},'dbp':{'value':dbp,'unit':units['bp']},'hr':{'value':hr,'unit':units['hr']},'rr':{'value':rr,'unit':units['rr']},'temp':{'value':temp,'unit':units['temp']},'spo2':{'value':spo2,'unit':units['spo2']},'weight':{'value':weight,'unit':units['weight']},'height':{'value':height,'unit':units['height']}},'measured_at':measured_at,'assessor':actor(role),'fall_risk_scale':fall_scale,'fall_risk_score':fall_score,'fall_risk_level':fall_level,'fall_risk_scale_status':fcfg['clinical_content_status']})
   update_rec(c,e['id'],patch,'Completed' if d.get('complete') else 'Draft',role,'INTAKE_SAVE');journey_add(c,pid,'Nurse Intake','Intake Completed','Completed',role,'intake',e['id']) if d.get('complete') else None;return {'ok':True,'bmi':bmi,'bsa_m2':bsa,'bsa_formula':patch['bsa_formula'],'canonical_units':patch['measurement_units'],'source_measurements':patch['source_measurements']},200
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
   update_rec(c,e['id'],patch,'Pending Chair Approval',role,'MDT_RECOMMEND_SUBMIT');grant_patient_access(c,pid,'MDT Chair','mdt_chair_review',e['id'],role);return {'ok':True,'status':'Pending Chair Approval'},200
  if a=='mdt_chair_sign':
   if role!='MDT Chair':return {'error':'MDT Chair required'},403
   e=must('mdt');decision=d.get('decision');reason=str(d.get('reason') or '').strip();co=latest(c,pid,'mdt_collab')
   if e['status']!='Pending Chair Approval':return {'error':'Submitted MDT recommendation awaiting Chair review required'},409
   if not co or co['data'].get('quorum_status')!='Met':return {'error':'Derived MDT quorum must be Met before Chair sign-off'},409
   if decision not in ['Approve','Return for revision'] or not reason:return {'error':'Chair decision and reason required','allowed':['Approve','Return for revision']},409
   if decision=='Return for revision':
    update_rec(c,e['id'],{'chair_decision':'Returned for revision','chair_reason':reason,'chair_signed_by':actor(role),'chair_signed_at':now(),'signed_by':None,'signed_at':''},'Returned for Revision',role,'MDT_CHAIR_RETURN',reason);return {'ok':True,'status':'Returned for Revision'},200
   patch={'chair_decision':'Approved','chair_reason':reason,'chair_signed_by':actor(role),'chair_signed_at':now(),'signed_by':actor(role),'signed_at':now()};update_rec(c,e['id'],patch,'MDT Recommended',role,'MDT_CHAIR_APPROVE',reason);resp=str(e['data'].get('specialty_responsible') or '')
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
    patch.update({'signed_by':actor(role),'signed_at':now()})
   if e['status']=='Final':
    if not amendment_reason:return {'error':'A finalized pathology report is immutable. Create a linked amendment with a documented reason.','requires_amendment_reason':True,'supersedes':e['id']},409
    nd={**e['data'],**patch,'supersedes':e['id'],'amendment_reason':amendment_reason,'amended_by':actor(role),'amended_at':now()};rid=new_record(c,pid,'pathology',nd,'Final' if fin else 'Draft',role);audit(c,pid,role,'PATHOLOGY_AMENDMENT_CREATED','pathology',rid,f'Supersedes {e["id"]}: {amendment_reason}');return {'ok':True,'id':rid,'status':'Final' if fin else 'Draft','supersedes':e['id']},200
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
   w=float(intake['data'].get('weight_kg') or 0);bsa=float(intake['data'].get('bsa_m2') or 0);pat=patient(c,pid);med=latest(c,pid,'med_recon');allergy=[f"{x.get('substance')} — {x.get('reaction')}" for x in med['data'].get('allergies',[])] if med else []
   recon_events=list((med or {}).get('data',{}).get('reconciliation_events',[]));latest_recon=recon_events[-1] if recon_events else {}
   if latest_recon.get('reconciliation_status')!='Complete':return {'error':'A current Complete medication/allergy reconciliation attestation is required before authorising systemic treatment','reconciliation_status':latest_recon.get('reconciliation_status') or 'Missing'},409
   decision_reasons=d.get('dose_decision_reasons') or {};admin_reason=str(d.get('administration_decision_reason') or '').strip();schedule_reason=str(d.get('schedule_decision_reason') or '').strip();decision_at=now();decision_actor=actor(role)
   if not admin_reason:return {'error':'Signed Treatment Order requires an explicit clinician reason for accepting/setting route, diluent, volume, rate and duration parameters'},409
   if not schedule_reason:return {'error':'Signed Treatment Order requires an explicit clinician reason for the administration date/time decision'},409
   fmap=active_formulary_map(c);cum_before=cumulative_administered_by_code(c,pid);admin_params=d.get('administration_parameters') or {}
   items=[]
   for q in protocol['items']:
    fi=fmap.get(q.get('drug')) or fmap.get(q.get('code'))
    if not fi:return {'error':f"No Active institution formulary mapping for {q['drug']}"},409
    calc=calc_dose(q,w,bsa);ordered=d.get('doses',{}).get(q['code'],calc)
    if q['dose_basis']=='AUC' and ordered in [None,'']: return {'error':f"Clinician must enter patient-specific ordered dose for {q['drug']} AUC item; demo does not calculate AUC automatically"},409
    try:ordered=float(ordered)
    except:return {'error':f"Invalid ordered dose for {q['drug']}"},409
    if ordered<0:return {'error':f"Ordered dose cannot be negative for {q['drug']}"},409
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
    items.append({**q,'treatment_block':block,'item_id':'OI-'+uuid.uuid4().hex[:7].upper(),'calculated_dose':calc,'calculated_unit':out_unit,'ordered_dose':ordered,'ordered_unit':out_unit,'final_approved_dose':ordered,'dose_decision_reason':decision_reason,'dose_decided_by':decision_actor,'dose_decided_at':decision_at,'variance_pct':variance,'variance_reason':variance_reason,'rounding':rounding,'route':route,'diluent':diluent,'volume_ml':volume,'duration_min':duration,'rate_ml_hr':rate or 0,'administration_parameter_decision_reason':admin_reason,'administration_parameters_decided_by':decision_actor,'administration_parameters_decided_at':decision_at,'administration_at':d.get('administration_at',now()),'schedule_decision_reason':schedule_reason,'schedule_decided_by':decision_actor,'schedule_decided_at':decision_at,'cumulative_dose_before':before,'cumulative_dose_limit':limit,'cumulative_dose_after_if_fully_administered':round(before+ordered,4)})
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
   order={'order_no':'ORD-'+uuid.uuid4().hex[:6].upper(),'episode_id':ep['id'],'admission_id':admission_id,'modification_id':d.get('modification_id') or mod_id,'administration_setting':setting,'plan_id':plan['id'],'protocol_id':protocol['id'],'protocol_version':protocol['version'],'regimen':protocol['name'],'content_template_id':template['id'],'content_template_version':template['version'],'content_source_id':template['source_id'],'diagnosis':d.get('diagnosis') or ((latest(c,pid,'diagnosis') or {}).get('data',{}).get('cancer_type','')),'intent':d.get('intent') or template.get('intent') or ((latest(c,pid,'treatment_plan') or {}).get('data',{}).get('intent','')),'line_of_therapy':d.get('line_of_therapy') or template.get('line_of_therapy') or ((latest(c,pid,'treatment_plan') or {}).get('data',{}).get('line_of_therapy','')),'cycle':cycle,'day':day,'planned_cycles':protocol['planned_cycles'],'supersedes_order_id':supersedes_id,'supersession_reason':supersession_reason,'start_date':d.get('start_date',str(date.today())),'patient_snapshot':{'name':pat['name'],'dob':pat['dob'],'mrn':pat['mrn'],'weight_kg':w,'height_cm':intake['data'].get('height_cm'),'bsa_m2':bsa,'bsa_formula':intake['data'].get('bsa_formula'),'measurement_units':intake['data'].get('measurement_units',{}),'source_measurements':intake['data'].get('source_measurements',{}),'measured_at':intake['data'].get('measured_at'),'assessor':intake['data'].get('assessor'),'allergies':allergy,'readiness_id':ready['id']},'cumulative_dose_ledger_before_order':cum_before,'items':items,'signed_by':actor(role),'signed_at':now(),'authorization_statement':'I reviewed patient history, labs, allergies, regimen, calculations and treatment criteria and authorize this patient-specific order instantiated from the selected governed regimen version.','locked':True}
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
   ready=get_rec(c,ordr.get('data',{}).get('readiness_id') or ordr.get('data',{}).get('patient_snapshot',{}).get('readiness_id','')) if ordr else None
   verification_snapshot={'order_id':ordr['id'] if ordr else '', 'order_version':ordr.get('version') if ordr else None,'protocol_id':ordr.get('data',{}).get('protocol_id') if ordr else '', 'protocol_version':ordr.get('data',{}).get('protocol_version') if ordr else '', 'cycle':ordr.get('data',{}).get('cycle') if ordr else None,'day':ordr.get('data',{}).get('day') if ordr else None,'readiness_id':ready.get('id') if ready else '', 'readiness_signed_at':ready.get('data',{}).get('signed_at') if ready else '', 'readiness_decision':ready.get('data',{}).get('decision') if ready else '', 'cumulative_dose_ledger':ordr.get('data',{}).get('cumulative_dose_ledger_before_order',{}) if ordr else {}, 'patient_snapshot':ordr.get('data',{}).get('patient_snapshot',{}) if ordr else {}}
   patch={'verification_checks':checks,'verification_snapshot':verification_snapshot,'decision':decision,'verified_actor':actor(role),'verified_at':now(),'verification_attestation':'I independently verified the current signed order, readiness evidence, dosing, organ-function context, cumulative exposure, route/diluent and preparation prerequisites.'}
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
   update_rec(c,e['id'],{'post_vitals':pv,'tolerance':d['tolerance'],'discharge_instructions':d['discharge_instructions'],'next_cycle':d.get('next_cycle',''),'completed_at':completed_at,'completed_by':actor(role),'cumulative_dose_ledger_after':cum_after},'Completed',role,'INFUSION_COMPLETE');update_rec(c,order['id'],{'administration_completed_at':completed_at,'administration_record_id':e['id'],'cumulative_dose_ledger_after_administration':cum_after},'Completed',role,'ORDER_EXECUTION_COMPLETE');hist=latest(c,pid,'treatment_history');eps=list(hist['data'].get('episodes',[]));eps.append({'type':'Systemic Therapy Administration','order_id':order['id'],'regimen':order['data']['regimen'],'cycle':order['data']['cycle'],'day':order['data']['day'],'date':completed_at,'status':'Completed','actual_items':mar,'cumulative_dose_ledger_after':cum_after});update_rec(c,hist['id'],{'episodes':eps},'Active',role,'HISTORY_APPEND');journey_add(c,pid,'Inpatient Care' if care_setting=='Inpatient' else 'Day Care / Infusion','Cycle Completed','Completed',role,'infusion',e['id'],d.get('next_cycle',''),True);return {'ok':True,'order_status':'Completed','cumulative_dose_ledger_after':cum_after},200
  if a=='record_toxicity':
   if role not in ['Medical Oncology','Day Care / Infusion Nurse','Inpatient Oncology Nurse','Nurse Navigator']:return {'error':'Clinical role required'},403
   e=must('toxicity');d={**d}
   # UI-friendly aliases are normalized into the canonical toxicity fields.
   if not d.get('term') and d.get('toxicity_type'):d['term']=d['toxicity_type']
   if not d.get('attribution') and d.get('relationship'):d['attribution']=d['relationship']
   req=['term','grade','onset_date','attribution','outcome'];miss=[x for x in req if not d.get(x)]
   if miss:return {'error':'Toxicity fields missing','missing':miss},409
   if str(d['grade']) not in VALUE_SETS['ctcae_grade']:return {'error':'CTCAE grade must be 1–5'},409
   xs=list(e['data'].get('events',[]));x={'id':'TOX-'+uuid.uuid4().hex[:7].upper(),**d,'toxicity_type':d.get('term'),'relationship':d.get('attribution'),'recorded_by':actor(role),'recorded_at':now()};xs.append(x);update_rec(c,e['id'],{'events':xs},'Active',role,'TOXICITY_RECORD');return {'ok':True,'id':x['id']},200
  if a=='create_modification':
   if role!='Medical Oncology':return {'error':'Medical Oncology required'},403
   e=must('modification');req=['original_order_id','reason','modification_type','clinical_justification'];miss=[x for x in req if not d.get(x)]
   if miss:return {'error':'Modification incomplete','missing':miss},409
   xs=list(e['data'].get('items',[]));x={'id':'MOD-'+uuid.uuid4().hex[:7].upper(),**d,'approved_by':actor(role),'approved_at':now()};xs.append(x);update_rec(c,e['id'],{'items':xs},'Active',role,'MODIFICATION_CREATE');return {'ok':True,'id':x['id']},200
  if a=='save_response':
   if role not in ['Medical Oncology','Radiologist']:return {'error':'Medical Oncology/Radiologist required'},403
   e=must('response');ass=list(e['data'].get('assessments',[]));les=d.get('target_lesions') or [];new_les=bool(d.get('new_lesions'))
   if not d.get('date') or not les:return {'error':'Scan date and target lesion measurements required'},409
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
   x={'id':aid,'episode_id':epid,'criteria_set':d.get('criteria_set','RECIST 1.1'),'criteria_version':d.get('criteria_version','1.1'),'date':d['date'],'source_imaging_id':d.get('source_imaging_id',''),'target_lesions':norm,'sum_mm':curr,'baseline_sum_mm':baseline,'nadir_sum_mm':nadir,'percent_change_from_baseline':pct,'non_target':d.get('non_target',''),'new_lesions':new_les,'proposed_response_category':cat,'response_category':'','confirmation_status':'Pending clinician confirmation','biomarkers':d.get('biomarkers',[]),'notes':d.get('notes',''),'measured_by':actor(role),'measured_at':now()};ass.append(x);update_rec(c,e['id'],{'assessments':ass},'Active',role,'RESPONSE_MEASUREMENT');return {'ok':True,'proposed_category':cat,'assessment':x},200
  if a=='confirm_response':
   if role!='Medical Oncology':return {'error':'Medical Oncology required to confirm response'},403
   e=must('response');ass=list(e['data'].get('assessments',[]));aid=d.get('assessment_id');x=next((z for z in ass if z.get('id')==aid),None)
   if not x:return {'error':'Response assessment not found'},404
   if x.get('confirmation_status')=='Confirmed':return {'error':'Confirmed response is immutable; create a new assessment for changed evidence'},409
   cat=d.get('response_category');reason=str(d.get('reason') or '').strip()
   if cat not in RESPONSE_CATEGORIES or not reason:return {'error':'Governed response category and clinician reason required','allowed':RESPONSE_CATEGORIES},409
   x.update({'response_category':cat,'confirmation_status':'Confirmed','confirmation_reason':reason,'confirmed_by':actor(role),'confirmed_at':now()});update_rec(c,e['id'],{'assessments':ass},'Active',role,'RESPONSE_CONFIRM',reason);return {'ok':True,'assessment':x},200
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
   x={'fraction_number':num,'status':d.get('status','Delivered'),'date_time':d.get('date_time') or now(),'planned_date_time':d.get('planned_date_time',''),'rescheduled_to':d.get('rescheduled_to',''),'delivered_dose_gy':float(d.get('delivered_dose_gy') or rx.get('dose_per_fraction_gy',0)) if d.get('status','Delivered')=='Delivered' else 0,'prescription_version':rxv,'plan_version':planv,'delivered_by':actor(role),'verified_by':d.get('verified_by') or actor(role)['name'],'image_guidance_performed':bool(d.get('image_guidance_performed')),'setup_variation':d.get('setup_variation',''),'toxicity':d.get('toxicity',''),'reason':d.get('reason','')};fr.append(x);delivered=sum(1 for z in fr if z['status']=='Delivered');st='In Progress' if delivered<int(rx['fractions']) else 'Completed';update_rec(c,e['id'],{'fractions':fr},st,role,'RT_FRACTION',f"{num} • Rx v{rxv} • Plan v{planv}");journey_add(c,pid,'Radiation Treatment',f"Fraction {num} {x['status']}",st,role,'radiation',e['id'],x.get('reason',''),True);return {'ok':True,'status':st,'delivered_count':delivered,'plan_version':planv,'prescription_version':rxv},200
  if a=='surgery_sign_plan':
   if role!='Surgical Oncology':return {'error':'Surgical Oncology required'},403
   e=must('surgery');plan={**e['data'].get('plan',{}),**d};req=['procedure','indication','intent','site','laterality','extent','approach','nodal_procedure','reconstruction','planned_date','priority','preop_requirements','required_imaging_pathology','anesthesia','anesthesia_clearance','blood_requirement'];miss=[x for x in req if plan.get(x) in ['',None,[]]]
   if miss:return {'error':'Surgical plan incomplete','missing':miss},409
   plan.update({'status':'Planned','signed_by':actor(role),'signed_at':now()});epid=d.get('episode_id') or e['data'].get('episode_id') or ((current_episode(c,pid) or ensure_episode(c,pid,role))['id']);update_rec(c,e['id'],{'episode_id':epid,'plan':plan},'Planned',role,'SURGERY_PLAN_SIGN');grant_patient_access(c,pid,'Surgical Nurse','surgery_plan',e['id'],role);return {'ok':True,'episode_id':epid},200
  if a=='surgery_preop':
   if role not in ['Surgical Oncology','Surgical Nurse']:return {'error':'Surgical team required'},403
   e=must('surgery');pre={**e['data'].get('preop',{}),**d};pre['ready']=all(pre.get(k)=='Complete' for k in ['anesthesia_clearance','labs','consent']);update_rec(c,e['id'],{'preop':pre},'Pre-op Ready' if pre['ready'] else 'Planned',role,'SURGERY_PREOP');return {'ok':True,'ready':pre['ready']},200
  if a=='surgery_performed':
   if role!='Surgical Oncology':return {'error':'Surgical Oncology required'},403
   e=must('surgery');
   if not e['data'].get('preop',{}).get('ready'):return {'error':'Pre-op readiness required'},409
   req=['actual_procedure','operation_date_time','preop_diagnosis','postop_diagnosis','laterality','findings','specimens','estimated_blood_loss_ml','operative_time_min','surgeons','postop_plan'];miss=[x for x in req if d.get(x) in ['',None,[]]]
   if miss:return {'error':'Operative record incomplete','missing':miss},409
   out={**d,'signed_by':actor(role),'signed_at':now()};update_rec(c,e['id'],{'outcome':out},'Performed',role,'SURGERY_PERFORMED');grant_patient_access(c,pid,'Pathology','surgical_specimen',e['id'],role);journey_add(c,pid,'Surgery','Procedure Performed','Performed',role,'surgery',e['id'],d.get('actual_procedure',''),True);hist=latest(c,pid,'treatment_history');eps=list(hist['data'].get('episodes',[]));eps.append({'type':'Surgery','episode_id':e['data'].get('episode_id') or ((current_episode(c,pid) or {}).get('id')),'date':d['operation_date_time'],'status':'Performed','procedure':d['actual_procedure'],'laterality':d['laterality']});update_rec(c,hist['id'],{'episodes':eps},role=role,action='HISTORY_APPEND');return {'ok':True},200
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
   costs={'Dexamethasone':50,'Pertuzumab':85000,'Trastuzumab':35000,'Docetaxel':6000,'Carboplatin':4500,'Pegfilgrastim':9000};lines=[];total=0
   for i in order['data']['items']:
    amt=costs.get(i['drug'],0);lines.append({'drug':i['drug'],'charge_basis':'Synthetic fixed demo cost line; clinical dose intentionally not exposed to Finance','demo_unit_estimate_inr':amt,'amount_inr':amt});total+=amt
   est={'source_order_id':order['id'],'currency':'INR','lines':lines,'total':total,'basis':'Synthetic demo cost master — not hospital tariff'};update_rec(c,e['id'],{'mo_drug_estimate':est,'estimate_status':'Calculated','estimate_no':'EST-'+uuid.uuid4().hex[:6].upper(),'valid_until':str(date.today()+timedelta(days=15))},'Active',role,'FIN_ESTIMATE');return {'ok':True,'total':total,'lines':lines},200
  if a=='finance_counselling':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');track=list(e['data'].get('tracking',[]));track.append({'at':now(),'status':d.get('financial_status'),'note':d.get('note',''),'by':actor(role)});update_rec(c,e['id'],{'counselling_status':d.get('counselling_status','Completed'),'payer_category':d.get('payer_category',''),'financial_status':d.get('financial_status',''),'counselled_by':actor(role),'counselled_at':now(),'tracking':track},'Active',role,'FIN_COUNSELLING');return {'ok':True},200
  if a=='fundraising_letter':
   if role!='Finance / Billing':return {'error':'Finance role required'},403
   e=must('conversion');pat=patient(c,pid);dx=latest(c,pid,'diagnosis');est=e['data'].get('mo_drug_estimate',{});text=d.get('text') or f"To whom it may concern,\n\n{pat['name']} ({pat['mrn']}) is receiving oncology care for {dx['data'].get('cancer_type','cancer')}. The current synthetic demo estimate is INR {est.get('total',0)}. This letter is for demonstration only and is not a clinical or financial commitment.\n\nCCA Demo Finance Team";letter={'status':'Draft','recipient':d.get('recipient',''),'purpose':d.get('purpose','Treatment support'),'text':text,'generated_by':actor(role),'generated_at':now()};update_rec(c,e['id'],{'fundraising_letter':letter},'Active',role,'FUNDRAISING_LETTER');return {'ok':True,'letter':letter},200
  return {'error':'Unknown action'},404

if __name__=='__main__':
 init_db();print(f'CCA Cancer Care V12.2 Final Defect Remediation running at http://127.0.0.1:{PORT}');ThreadingHTTPServer(('127.0.0.1',PORT),H).serve_forever()
