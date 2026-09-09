"""CCA V12.2-PC7.0 clinical-safety helpers.

The platform supplies calculation/verification machinery. Institution-specific clinical
thresholds and policy values remain versioned CCA configuration. The bundled demo master
is synthetic QA content and must not be interpreted as CCA prescribing policy.
"""
from datetime import date,datetime
import math

BUILD='12.2-PC7.1-PC8.0'
BSA_POLICY={'formula':'Mosteller','raw_precision':4,'display_precision':2,'ordering_precision':2,'formula_text':'sqrt(height_cm × weight_kg / 3600)'}
ALLOWED_RENAL_METHODS=['Measured GFR','Validated nuclear medicine GFR','Cockcroft-Gault creatinine clearance','CCA-approved renal dosing value']
CTCAE_VERSION='5.0'
CTCAE_TERMS={
 'Nausea':{'soc':'Gastrointestinal disorders'},'Vomiting':{'soc':'Gastrointestinal disorders'},
 'Diarrhea':{'soc':'Gastrointestinal disorders'},'Mucositis oral':{'soc':'Gastrointestinal disorders'},
 'Fatigue':{'soc':'General disorders and administration site conditions'},
 'Neutrophil count decreased':{'soc':'Investigations'},'Platelet count decreased':{'soc':'Investigations'},
 'Anemia':{'soc':'Blood and lymphatic system disorders'},'Febrile neutropenia':{'soc':'Blood and lymphatic system disorders'},
 'Peripheral sensory neuropathy':{'soc':'Nervous system disorders'},'Rash maculo-papular':{'soc':'Skin and subcutaneous tissue disorders'},
}
CTCAE_ATTRIBUTION=['Unrelated','Unlikely','Possible','Probable','Definite']
RECIST_VERSION='RECIST 1.1'

TERMINOLOGY={
 'ICD-10':{'C50.4':'Malignant neoplasm of upper-outer quadrant of breast','C50.9':'Malignant neoplasm of breast, unspecified','C53.9':'Malignant neoplasm of cervix uteri, unspecified','C18.7':'Malignant neoplasm of sigmoid colon','C83.3':'Diffuse large B-cell lymphoma'},
 'ICD-O-3 Topography':{'C50.4':'Upper-outer quadrant of breast','C50.9':'Breast, NOS','C53.9':'Cervix uteri, NOS','C18.7':'Sigmoid colon'},
 'ICD-O-3 Morphology':{'8500/3':'Invasive carcinoma of no special type / ductal carcinoma, malignant','8070/3':'Squamous cell carcinoma, NOS, malignant','8140/3':'Adenocarcinoma, NOS, malignant','9680/3':'Diffuse large B-cell lymphoma'},
 'SNOMED CT':{'254837009':'Malignant neoplasm of breast'},
}
BREAST_STAGE_DEMO={('cT2','cN1','cM0'):'Stage IIB'}

DIRECT_ALLERGY_CLASS_MAP={
 # Only explicit, governed direct mappings belong here. Do not infer cross-reactivity.
}

def safe_float(v):
 try:return float(v)
 except:return None

def bsa_values(height_cm,weight_kg):
 h=safe_float(height_cm);w=safe_float(weight_kg)
 if not h or not w or h<=0 or w<=0:return {'raw':None,'display':None,'ordering':None,**BSA_POLICY}
 raw=math.sqrt(h*w/3600.0)
 return {'raw':round(raw,BSA_POLICY['raw_precision']),'display':round(raw,BSA_POLICY['display_precision']),'ordering':round(raw,BSA_POLICY['ordering_precision']),**BSA_POLICY}

def effective_protocol(item,cycle):
 c=max(1,int(cycle or 1));dose=item.get('protocol_dose');phase='standard'
 lm=item.get('loading_maintenance') or {}
 if lm:
  if c==1 and lm.get('loading_dose') is not None:dose=lm['loading_dose'];phase='loading'
  elif c>1 and lm.get('maintenance_dose') is not None:dose=lm['maintenance_dose'];phase='maintenance'
 elif item.get('loading_cycles') is not None or item.get('maintenance_protocol_dose') is not None:
  # PC8.0 flexible loading-phase shape: an explicit list of loading-phase cycle numbers plus
  # a separate maintenance dose, instead of a single cycle==1 cutover. Only engages when the
  # regimen item uses this shape at all; existing loading_maintenance-shaped content above
  # takes precedence and is untouched.
  loading_cycles={int(x) for x in (item.get('loading_cycles') or [])}
  if c in loading_cycles:dose=item.get('protocol_dose');phase='loading'
  elif item.get('maintenance_protocol_dose') is not None:dose=item.get('maintenance_protocol_dose');phase='maintenance'
 return dose,phase

def calculate_dose(item,weight_kg,bsa_m2,cycle=1,renal=None):
 renal=renal or {};basis=item.get('dose_basis');pdose,phase=effective_protocol(item,cycle);trace={'basis':basis,'protocol_dose':pdose,'protocol_unit':item.get('protocol_unit'),'cycle':int(cycle or 1),'cycle_phase':phase}
 if pdose is None:return {'ok':False,'error':'Protocol dose is not configured','calculated_dose':None,'trace':trace}
 try:pd=float(pdose)
 except:return {'ok':False,'error':'Protocol dose is invalid','calculated_dose':None,'trace':trace}
 if basis=='Fixed':calc=pd;trace['formula']='fixed dose'
 elif basis=='mg/kg':
  w=safe_float(weight_kg)
  if not w or w<=0:return {'ok':False,'error':'Valid dosing weight is required','calculated_dose':None,'trace':trace}
  calc=pd*w;trace.update({'weight_kg':w,'formula':f'{pd} mg/kg × {w} kg'})
 elif basis=='mg/m²':
  b=safe_float(bsa_m2)
  if not b or b<=0:return {'ok':False,'error':'Valid BSA is required','calculated_dose':None,'trace':trace}
  calc=pd*b;trace.update({'bsa_m2':b,'formula':f'{pd} mg/m² × {b} m²'})
 elif basis=='AUC':
  method=str(renal.get('method') or '').strip();rv=safe_float(renal.get('value_ml_min'));source=str(renal.get('source_id') or '').strip();at=str(renal.get('measured_at') or renal.get('source_time') or '').strip()
  cfg=item.get('renal_dosing') or {};allowed=cfg.get('allowed_methods') or ALLOWED_RENAL_METHODS
  if not method or method not in allowed:return {'ok':False,'error':'AUC dosing requires an explicitly governed renal dosing method','calculated_dose':None,'trace':{**trace,'allowed_renal_methods':allowed}}
  if rv is None or rv<=0:return {'ok':False,'error':'AUC dosing requires a positive renal dosing value in mL/min','calculated_dose':None,'trace':trace}
  if not source or not at:return {'ok':False,'error':'AUC dosing requires renal value source and timestamp','calculated_dose':None,'trace':trace}
  cap=cfg.get('gfr_cap_ml_min');eff=min(rv,float(cap)) if cap not in [None,''] else rv
  calc=pd*(eff+25.0);trace.update({'formula':'Calvert: target AUC × (renal dosing value + 25)','renal_method':method,'renal_value_ml_min':rv,'effective_renal_value_ml_min':eff,'renal_source_id':source,'renal_source_time':at,'gfr_cap_ml_min':cap})
 else:return {'ok':False,'error':'Unsupported dose basis','calculated_dose':None,'trace':trace}
 precision=int(item.get('calculation_precision',2));calc=round(calc,precision);trace['calculated_dose_mg']=calc
 return {'ok':True,'calculated_dose':calc,'trace':trace}

def safety_check(item,ordered,calc_result,variance_reason=''):
 errors=[];warnings=[]
 od=safe_float(ordered)
 if od is None or od<=0:errors.append('Final ordered dose must be a positive number')
 if not calc_result.get('ok'):errors.append('Patient-specific dose calculation is unresolved: '+str(calc_result.get('error') or 'unknown calculation error'))
 calc=safe_float(calc_result.get('calculated_dose'));variance=None
 if calc and od is not None:
  variance=round((od-calc)/calc*100.0,1)
  max_var=float(item.get('max_variance_pct',20))
  if abs(variance)>max_var:errors.append(f'Ordered dose variance {variance}% exceeds the configured {max_var}% safety limit')
  elif abs(variance)>0.01 and not str(variance_reason or '').strip():errors.append('Dose variance requires a documented clinical reason')
 hardmax=safe_float(item.get('max_dose_mg'))
 if hardmax is not None and od is not None and od>hardmax:errors.append(f'Ordered dose {od} mg exceeds configured hard maximum {hardmax} mg')
 return {'ok':not errors,'errors':errors,'warnings':warnings,'variance_pct':variance,'max_dose_mg':hardmax}

def allergy_conflicts(allergies,item):
 # Direct coded ingredient/class matches only, restricted to allergies not explicitly
 # resolved/inactive (PC8.0 status filter). A labeled lower-confidence substring match is
 # unioned in as an additional, distinctly-tagged hit category (PC8.0) -- it never replaces
 # or suppresses an exact governed-code/name match, and both require clinician review.
 codes=set(str(x).strip() for x in (item.get('allergen_codes') or [item.get('code')]) if x)
 names=set(str(x).strip().lower() for x in (item.get('allergen_names') or [item.get('drug')]) if x)
 drug_name=str(item.get('drug') or '').strip().lower()
 hits=[]
 for a in allergies or []:
  status=str(a.get('status') or '').strip().lower()
  if status in ['resolved','recovered','inactive','entered in error','no known allergy']:continue
  ac=str(a.get('code') or '').strip();an=str(a.get('substance') or a.get('generic_ingredient') or '').strip().lower()
  if (ac and ac in codes) or (an and an in names):
   hits.append({'allergy_id':a.get('id'),'substance':a.get('substance'),'code':ac,'reaction':a.get('reaction'),'severity':a.get('severity'),'match_type':'exact'})
  elif an and drug_name and (an in drug_name or drug_name in an):
   hits.append({'allergy_id':a.get('id'),'substance':a.get('substance'),'code':ac,'reaction':a.get('reaction'),'severity':a.get('severity'),'match_type':'partial — clinician review required'})
 return hits

def validate_terminology(d):
 errors=[]
 checks=[('icd10','ICD-10'),('icdo_topography','ICD-O-3 Topography'),('icdo_morphology','ICD-O-3 Morphology'),('snomed','SNOMED CT')]
 for field,system in checks:
  val=str(d.get(field) or '').strip()
  if not val:continue
  if val not in TERMINOLOGY[system]:
   if d.get('terminology_validation_status')!='Validated by CCA terminology service' or not d.get('terminology_service_reference'):
    errors.append(f'{field}={val} is not in the bundled oncology demo terminology set and lacks external terminology validation provenance')
 return errors

def derive_stage(d):
 if str(d.get('staging_system'))=='AJCC' and 'Breast' in str(d.get('staging_version')):
  return BREAST_STAGE_DEMO.get((str(d.get('stage_t')),str(d.get('stage_n')),str(d.get('stage_m'))))
 return None

def recist_evaluate(targets,baseline_targets,prior_assessments,new_lesions=False,non_target=''):
 if len(targets)>5:return {'ok':False,'error':'RECIST 1.1 permits at most 5 target lesions in total'}
 organs={}
 for x in targets:
  org=str(x.get('organ') or '').strip() or 'Unspecified';organs[org]=organs.get(org,0)+1
  if organs[org]>2:return {'ok':False,'error':f'RECIST 1.1 permits at most 2 target lesions per organ ({org})'}
  typ=str(x.get('lesion_type') or 'Non-nodal');size=safe_float(x.get('size_mm'))
  if size is None or size<0:return {'ok':False,'error':'Every target lesion requires a valid measurement in mm'}
  if typ=='Lymph node' and x.get('baseline_selected') is True and size<15:return {'ok':False,'error':'A target lymph node must have short axis ≥15 mm at baseline'}
 base=sum(safe_float(x.get('size_mm')) or 0 for x in baseline_targets or []);curr=sum(safe_float(x.get('size_mm')) or 0 for x in targets)
 prior=[safe_float(x.get('sum_mm')) for x in prior_assessments or []];prior=[x for x in prior if x is not None]
 nadir=min([base]+prior) if base else (min(prior) if prior else curr)
 if new_lesions:cat='PD'
 elif 'unequivocal progression' in str(non_target or '').lower():cat='PD'  # PC8.0: explicit non-target progression trigger
 else:
  all_cr=all((safe_float(x.get('size_mm')) or 0)==0 if str(x.get('lesion_type') or 'Non-nodal')!='Lymph node' else (safe_float(x.get('size_mm')) or 0)<10 for x in targets)
  if all_cr and str(non_target or '').lower() in ['', 'none','cr','complete response']:cat='CR'
  elif base and curr<=base*0.70:cat='PR'
  elif nadir and curr>=nadir*1.20 and curr-nadir>=5:cat='PD'
  else:cat='SD'
 return {'ok':True,'category':cat,'sum_mm':round(curr,2),'baseline_sum_mm':round(base,2),'nadir_sum_mm':round(nadir,2),'change_from_baseline_pct':round((curr-base)/base*100,1) if base else None,'change_from_nadir_pct':round((curr-nadir)/nadir*100,1) if nadir else None,'framework':RECIST_VERSION}

# RT delivery safety. Institution tolerance is configurable on the signed prescription;
# the bundled default is a tight technical QA tolerance for synthetic validation only.
def rt_fraction_safety(rx, prior_fractions, delivered_dose_gy, status='Delivered'):
    errors=[]
    try:
        prescribed=float(rx.get('dose_per_fraction_gy') or 0)
        total=float(rx.get('total_dose_gy') or 0)
        dose=float(delivered_dose_gy or 0)
    except Exception:
        return {'ok':False,'errors':['Valid numeric RT dose values are required']}
    tol=float(rx.get('delivery_tolerance_gy') or 0.01)
    cumulative=sum(float(x.get('delivered_dose_gy') or 0) for x in (prior_fractions or []) if x.get('status')=='Delivered')
    projected=cumulative+(dose if status=='Delivered' else 0)
    if status=='Delivered':
        if prescribed<=0 or total<=0:errors.append('Signed prescription must contain positive dose per fraction and total dose')
        if dose<=0:errors.append('Delivered fraction dose must be greater than zero')
        if abs(dose-prescribed)>tol:errors.append(f'Delivered fraction dose {dose} Gy differs from prescribed {prescribed} Gy beyond configured tolerance ±{tol} Gy; amend/re-approve the prescription before delivery')
        if projected>total+tol:errors.append(f'Projected cumulative delivered dose {round(projected,4)} Gy exceeds prescribed total {total} Gy')
    elif dose not in [0,0.0]:errors.append('Missed/rescheduled fractions cannot carry a delivered dose')
    return {'ok':not errors,'errors':errors,'prescribed_fraction_dose_gy':prescribed,'delivered_dose_gy':dose,'delivery_tolerance_gy':tol,'prior_cumulative_dose_gy':round(cumulative,4),'projected_cumulative_dose_gy':round(projected,4),'prescribed_total_dose_gy':total}
