# V12 Role Working Surfaces — INPUT / VIEW / OUTPUT

**Roles:** 24  
**Specified fields:** 337  

Every field contract comes from the runtime `ROLE_SURFACES` definition. `Pending terminology mapping` or `Pending specialist value-set review` is retained explicitly rather than replaced with invented clinical content.

| Role | INPUT | VIEW | OUTPUT |
|---|---:|---:|---:|
| Medical Oncology | 29 | 14 | 6 |
| Radiation Oncology | 22 | 7 | 4 |
| Surgical Oncology | 17 | 6 | 4 |
| Oncology Pharmacy | 16 | 10 | 4 |
| Day Care / Infusion Nurse | 20 | 6 | 4 |
| Nurse Navigator | 9 | 4 | 3 |
| Front Desk | 6 | 2 | 3 |
| Patient Attender | 3 | 2 | 2 |
| Biller | 4 | 1 | 1 |
| PRE / Patient Relations Executive | 2 | 2 | 2 |
| Laboratory / Phlebotomy | 5 | 3 | 3 |
| Radiology Coordinator | 4 | 4 | 2 |
| Radiology Technician | 3 | 2 | 1 |
| Radiologist | 3 | 2 | 1 |
| Pathology | 5 | 1 | 2 |
| MDT Coordinator | 7 | 3 | 3 |
| Radiation Physicist | 3 | 4 | 1 |
| Radiation Technologist | 6 | 2 | 1 |
| Surgical Nurse | 3 | 2 | 1 |
| Finance / Billing | 4 | 1 | 3 |
| Patient Liaison | 3 | 2 | 1 |
| Hospital Management / Admin | 2 | 3 | 3 |
| External Consultant | 1 | 1 | 1 |
| Inpatient Oncology Nurse | 8 | 8 | 4 |

## Medical Oncology

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Regimen / protocol | search-select | Yes | Approved Regimen Master | Institution regimen ID | Clinical Content Master |
| Protocol version | read-only from selection | Yes | Selected version | Versioned master | Clinical Content Master |
| Treatment intent | select | Yes | intent | SNOMED CT/local mapping | Treatment Plan |
| Line of therapy | select | Yes | treatment_line | Structured oncology line | Treatment Plan |
| Cycle number | integer | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Day number | integer | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Planned cycles | integer | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Start date | date | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Generic drug | coded select | Yes | Regimen ordered item | RxNorm/SNOMED/local formulary | Regimen Master |
| Sequence number | integer/read-only | Yes | Regimen sequence | Not applicable | Regimen Master |
| Dose basis | select | Yes | dose_basis | UCUM dose expression | Regimen Master |
| Protocol dose | number/read-only | Yes | Template value | UCUM | Regimen Master |
| Patient-calculated dose | number/read-only | Yes | Calculated | UCUM | Order engine |
| Final ordered dose | number | Yes | Clinician-entered/confirmed | UCUM | Role workflow / local master |
| Dose rounding | select | No | Institution rounding rule | Local pharmacy policy | Role workflow / local master |
| Dose reduction % | number | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Dose modification reason | select | No | Toxicity|Organ function|Tolerance|Clinical judgment|Other | SNOMED CT/local | Role workflow / local master |
| Route | select | Yes | route | SNOMED CT | Role workflow / local master |
| Diluent | select | No | Formulary allowed diluents | Local formulary | Role workflow / local master |
| Diluent volume | number + mL | No | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Final concentration | calculated/read-only | No | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Infusion rate | number | No | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Infusion duration | duration | No | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Administration date/time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Special instructions | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Premedications / hydration / antiemetics / growth factors / rescue / emergency standby | template sections | No | Approved regimen items | Drug terminology | Regimen Master |
| Admission decision | select | No | admission_type | Pending terminology mapping | Role workflow / local master |
| Admission reason | select | No | admission_reason | Pending terminology mapping | Role workflow / local master |
| Continuous/oral therapy plan | structured | No | continuous_mode | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Allergies with reaction/severity | Medication reconciliation |  |
| Current reconciled medications | Medication reconciliation |  |
| Height/weight/BSA + formula + measurement date | Nurse Intake |  |
| Renal function + result date | Final Lab |  |
| Hepatic function + result date | Final Lab |  |
| Pregnancy status where applicable | Final Lab |  |
| Performance status | Nurse Intake / Diagnosis |  |
| Cumulative dose tracking | Treatment History / prior administrations |  |
| CBC/ANC/platelets and regimen criteria | Readiness engine |  |
| Protocol vs calculated vs ordered vs administered dose | Canonical order/admin chain |  |
| MDT recommendation and originating meeting | MDT |  |
| Treatment Plan phase / intent / line | Treatment Plan |  |
| Cancer episode selector / longitudinal episode history | Cancer Episode |  |
| Active admission and inpatient observations | IPD Record |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Radiation Oncology

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Diagnosis | read-only link | Yes | Not applicable / field-format constrained | ICD/SNOMED | Cancer record |
| Treatment site | coded select | Yes | Institution RT site master | SNOMED CT | Role workflow / local master |
| Laterality | select | Yes | laterality | SNOMED CT | Role workflow / local master |
| Intent | select | Yes | intent | Pending terminology mapping | Role workflow / local master |
| Modality | select | Yes | External Beam|Brachytherapy|Stereotactic|Particle|Other | Pending terminology mapping | Role workflow / local master |
| Technique | select | Yes | 3D Conformal|IMRT|VMAT|Proton|Brachytherapy|Stereotactic|Other | Pending terminology mapping | Role workflow / local master |
| Energy / radioisotope | select/text from machine master | Yes | TPS/OIS machine/energy master | Pending terminology mapping | Role workflow / local master |
| Treatment phase | integer | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Total prescribed dose | number Gy | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Dose per fraction | number Gy | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Number of fractions | integer | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Frequency | select | Yes | rt_frequency | Pending terminology mapping | Role workflow / local master |
| Planned start date | date | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Concurrent systemic treatment | linked order/select | No | Active Medical Oncology orders | Pending terminology mapping | Role workflow / local master |
| Target volumes | structured list | Yes | RT structure reference | DICOM-RT / SNOMED | Role workflow / local master |
| Organs at risk | multi-select | Yes | Institution OAR master | Pending terminology mapping | Role workflow / local master |
| OAR constraints | structured constraint list | Yes | Institution RT constraint master | Pending terminology mapping | Role workflow / local master |
| Simulation requirement | select | Yes | Yes|No | Pending terminology mapping | Role workflow / local master |
| Immobilisation | select | No | Institution immobilisation master | Pending terminology mapping | Role workflow / local master |
| Image guidance | select | No | Institution IGRT master | Pending terminology mapping | Role workflow / local master |
| Bolus | select | No | None|Custom|Other | Pending terminology mapping | Role workflow / local master |
| Special instructions | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Cancer diagnosis/stage | Cancer record |  |
| MDT recommendation | MDT |  |
| Concurrent systemic order | Medical Oncology |  |
| Prior radiation exposure / overlapping course | Treatment History / OIS integration |  |
| Relevant imaging | Radiology/PACS references |  |
| TPS/OIS plan references | DICOM-RT integration boundary |  |
| Active signed systemic order / cycle-day | Medical Oncology |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Surgical Oncology

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Procedure | coded select | Yes | Surgical procedure master | SNOMED CT/ICD-PCS/local | Role workflow / local master |
| Indication | select | Yes | Diagnostic|Definitive treatment|Palliative|Debulking|Re-section for recurrence|Other | Pending terminology mapping | Role workflow / local master |
| Intent | select | Yes | Curative|Palliative|Diagnostic|Other | Pending terminology mapping | Role workflow / local master |
| Anatomical site | coded select | Yes | Anatomical site master | SNOMED CT | Role workflow / local master |
| Laterality | select | Yes | laterality | Pending terminology mapping | Role workflow / local master |
| Proposed extent | select | Yes | Procedure-specific extent master | Pending terminology mapping | Role workflow / local master |
| Approach | select | Yes | Open|Laparoscopic|Robotic|Hybrid|Other | Pending terminology mapping | Role workflow / local master |
| Nodal procedure | select | No | Procedure-specific nodal master | Pending terminology mapping | Role workflow / local master |
| Reconstruction | select | No | Procedure-specific reconstruction master | Pending terminology mapping | Role workflow / local master |
| Planned date | date | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Priority | select | Yes | surgery_priority | Pending terminology mapping | Role workflow / local master |
| Pre-operative requirements | checklist | Yes | Procedure template checklist | Not applicable | Role workflow / local master |
| Required imaging/pathology | multi-select | Yes | Order/result references | Pending terminology mapping | Role workflow / local master |
| Anaesthesia type | select | Yes | General|Regional|Local|Monitored sedation|Other | Pending terminology mapping | Role workflow / local master |
| Anaesthesia clearance | select | Yes | Pending|Complete|Not cleared | Pending terminology mapping | Role workflow / local master |
| Blood product requirement | select | No | Local transfusion/pre-op master | Pending terminology mapping | Role workflow / local master |
| Special instructions | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Diagnosis/stage | Cancer record |  |
| MDT recommendation | MDT |  |
| Response after neoadjuvant therapy | Response Assessment |  |
| Pre-op clearances | Surgical Nurse / Anaesthesia interface |  |
| Imaging/pathology | Radiology/Pathology |  |
| Active signed systemic order / cycle-day | Medical Oncology |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Oncology Pharmacy

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Verification checklist | boolean checklist | Yes | Allergy|Interaction|Dose method|Calculated dose|Dose|Organ function|Diluent|Volume|Stock|Expiry | Not applicable | Role workflow / local master |
| Verification decision | select | Yes | pharmacy_decision | Pending terminology mapping | Role workflow / local master |
| Query/reject reason | select | No | Dose clarification|Allergy|Interaction|Formulation|Stock|Expiry|Other | Pending terminology mapping | Role workflow / local master |
| Message to oncologist | text | No | Required for Query/Reject | Not applicable | Role workflow / local master |
| Formulation / strength | governed select | Yes | Formulary Master | Pending terminology mapping | Role workflow / local master |
| Batch / lot | text | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Expiry | date | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Actual measured volume | number | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Wastage | number + reason | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Preparation start / finish | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Prepared by | authenticated actor | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Independent checker | authenticated actor | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Barcode / label match | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Dispense destination | select | Yes | Day Care / Other approved destination | Pending terminology mapping | Role workflow / local master |
| Dispense time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Manifest | identifier | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Patient + 2 identifiers | Registration |  |
| Allergies | Medication reconciliation |  |
| Signed regimen/cycle/day/order sequence | Treatment Order |  |
| Protocol vs calculated vs ordered dose | Treatment Order / Regimen Master |  |
| Route/diluent/volume/concentration/rate/duration | Treatment Order |  |
| Prescriber + authorization timestamp | Treatment Order |  |
| Renal/hepatic function | Readiness/Lab |  |
| Current medication list | Medication reconciliation |  |
| Height / weight / BSA + formula + measurement date | Nurse Intake |  |
| Intake assessor / provenance | Nurse Intake |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Day Care / Infusion Nurse

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Two patient identifiers | verification | Yes | Name+MRN/DOB | Not applicable | Role workflow / local master |
| Order vs prepared medication check | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Consent current | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Allergies verified with patient | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Pre-treatment vitals | structured vitals | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Required labs in range/current | boolean + evidence | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Venous access type/site/patency | structured select/text | Yes | Central line|PICC|Port|Peripheral IV|Other | Pending terminology mapping | Role workflow / local master |
| Pharmacy-prepared medication/label match | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Actual administered dose | number | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Route / access site | read-only route + selected access | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Actual rate | number | No | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Start / end time | time | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Reaction | select | Yes | None|Flushing|Rash|Hypotension|Tachycardia|Chest pain|Dyspnea|Allergic|Other | Pending terminology mapping | Role workflow / local master |
| Intervention | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Completion status | select | Yes | completion_status | Pending terminology mapping | Role workflow / local master |
| Reason if incomplete | select/text | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Post-treatment vitals | structured vitals | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Tolerance | select | Yes | Good|Mild symptoms|Significant reaction | Pending terminology mapping | Role workflow / local master |
| Discharge instructions | template/text | Yes | Pending specialist value-set review | Not applicable | Role workflow / local master |
| Next cycle date | date | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Signed locked Treatment Order | Medical Oncology |  |
| Pharmacy verification/release | Oncology Pharmacy |  |
| Allergies | Medication reconciliation |  |
| Consent status | Consent |  |
| Readiness labs + hold criteria | Readiness |  |
| Administration sequence | Treatment Order |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Nurse Navigator

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Vitals | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Height/weight | number | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| ECOG/Karnofsky | select | Yes | ecog/kps | Pending terminology mapping | Role workflow / local master |
| Pain assessment | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Fall risk | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Medication reconciliation | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Allergies/adverse reactions | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Oncology history | dynamic structured form | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Old document upload | file + metadata | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Registration/queue | Front Desk |  |
| Prior documents | Document store |  |
| Current care plan | Care Plan |  |
| Active admission / ward / bed | Inpatient record |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## Front Desk

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Name/DOB/contact/ID | structured registration | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| ABHA association | identifier | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Clinician/specialty routing | select | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Referral hierarchy | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Appointment | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Queue destination | select | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Administrative identity | Patient master |  |
| Appointment/queue state | Scheduling/Queue |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## Patient Attender

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Registration form demographics | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Consent artefact | file/signature | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Patient photograph | file | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Registration status | Patient master |  |
| Consent status | Consent register |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |

## Biller

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Payment status | select | Yes | Paid|Waived | Pending terminology mapping | Role workflow / local master |
| Amount | number | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Receipt number | identifier | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Waiver reason | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Billable service order only | Lab/Radiology order |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## PRE / Patient Relations Executive

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Patient movement/escort status | select | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Radiology appointment scheduling | datetime/location | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Queue destination | Queue |  |
| Payment-cleared diagnostic order | Billing/Order |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |

## Laboratory / Phlebotomy

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Sample/accession ID | identifier | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Collection time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Laboratory result value | number | Yes | Test-specific result entry | LOINC observation mapping | Role workflow / local master |
| Laboratory result unit | mandatory coded select | Yes | Governed test-specific unit set; no implicit/default unit | UCUM mapping | Role workflow / local master |
| Final-result amendment reason | text | No | Required when correcting a finalized result | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Paid/waived lab order | Medical Oncology/Billing |  |
| Two patient identifiers | Registration |  |
| Prior finalized result + units when creating an amendment | Longitudinal Lab Record |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## Radiology Coordinator

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Scheduled date/time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Location / modality room | select | Yes | Radiology location master | Pending terminology mapping | Role workflow / local master |
| Scheduling note | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Relevant document checklist | checklist | No | Pending specialist value-set review | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Physician radiology order and indication | Medical Oncology |  |
| Payment/waiver status | Biller / Finance |  |
| Patient identifiers | Registration |  |
| Relevant prior imaging/documents | EMR documents |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |

## Radiology Technician

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Procedure performed time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Consent verified | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Technical note | text | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Paid/waived scheduled imaging order | Medical Oncology/Billing/PRE |  |
| Relevant documents | Document store |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Radiologist

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Findings | structured/text report | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Impression | text | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| eSignature | authenticated sign | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Imaging order/indication | Medical Oncology |  |
| Prior imaging | Radiology record |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Pathology

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Specimen/site | coded | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Histology/grade | coded | Yes | Pending specialist value-set review | ICD-O/SNOMED | Role workflow / local master |
| Biomarkers | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Margin/node data | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Pathology sign-off | authenticated sign | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Procedure/specimen context | Surgery/Order |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |

## MDT Coordinator

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Meeting date/time/mode | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Case list | patient/case references | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Attendance | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Discussion/comments | attributed entries | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Formal recommendation | structured/text | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Consensus | select/text | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Outstanding investigations | task list | No | Pending specialist value-set review | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Diagnosis/stage/performance status | Cancer record |  |
| Pathology/biomarkers | Pathology |  |
| Imaging/labs | Diagnostics |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## Radiation Physicist

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Physics QA decision | select | Yes | Approved|Rejected / Replan Required | Pending terminology mapping | Role workflow / local master |
| Physics QA note | textarea | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| QA completion time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Signed RT prescription | Radiation Oncology |  |
| Simulation / contouring / plan references | RT workflow / TPS-OIS references |  |
| OAR constraints and planned dose | RT prescription / plan references |  |
| Prior overlapping radiation | Treatment History / OIS reference |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Radiation Technologist

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Fraction number/status | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Delivery date/time | datetime | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Delivered dose | number Gy | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Image guidance performed | boolean | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Setup variation | structured/text | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Toxicity noted | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Approved RT prescription | Radiation Oncology |  |
| Physics QA/physician approval | RT planning record |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Surgical Nurse

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Pre-op checklist | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Consent/labs/anesthesia clearance | status | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Scheduling/OR readiness note | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Signed Surgical Plan | Surgical Oncology |  |
| Patient identity/allergy/consent | EMR |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Finance / Billing

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Financial counselling status | select | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Payer/funding category | select | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Estimate adjustment | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Funding letter recipient/purpose | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Signed treatment plan/order cost basis only | Treatment/Cost master |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## Patient Liaison

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Consent/education status | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Care-plan task update | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Appointment coordination | structured | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Care plan tasks | Care Plan |  |
| Upcoming appointments | Scheduling |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Hospital Management / Admin

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Content-template governance | approve/retire/version | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Form/workflow/report master configuration | structured master data | No | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Operational queues/volumes | De-identified/limited operational data |  |
| Clinical content governance status | Content Master |  |
| Audit integrity | Audit ledger |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## External Consultant

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Case-scoped token | token | Yes | Not applicable / field-format constrained | Not applicable | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| De-identified MDT case only | MDT external projection |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |

## Inpatient Oncology Nurse

### INPUT

| Field | Type | Mandatory | Value set | Code system | Source |
|---|---|:---:|---|---|---|
| Ward/bed confirmation | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Inpatient vitals / nursing observations | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |
| Pain score | number | No | Not applicable / field-format constrained | Not applicable | Role workflow / local master |
| Intake/output | number mL | No | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| Inpatient toxicity | CTCAE structured | No | toxicity | CTCAE | Role workflow / local master |
| Two patient identifiers | verification | Yes | Pending specialist value-set review | Not applicable | Role workflow / local master |
| MAR actual administered dose | number | Yes | Not applicable / field-format constrained | UCUM | Role workflow / local master |
| MAR start/end/rate/access | structured | Yes | Pending specialist value-set review | Pending terminology mapping | Role workflow / local master |

### VIEW

| Field / information | Source | Code system / note |
|---|---|---|
| Diagnosis / cancer episode | Cancer record |  |
| Active admission / ward / bed | Admission |  |
| Allergies / reconciled medications | Medication reconciliation |  |
| Nurse Intake weight/BSA | Nurse Intake |  |
| Signed inpatient treatment order | Medical Oncology |  |
| Pharmacy verification/release | Oncology Pharmacy |  |
| Treatment readiness/labs | Readiness |  |
| Prior toxicity | Toxicity |  |

### OUTPUT

| Record / output | Downstream | Code system / note |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

---

# PC1.4 Structural Conformance Delta

This delta supplements the baseline role contract above.

## Medical Oncology
- Final ordered dose is a **DECIDED** item. Every drug requires an explicit final-dose decision reason before order signature; the decision stores actor and timestamp.
- A replacement order must explicitly identify the order it supersedes and give a supersession reason. The old order cannot be acted on downstream.
- Systemic order authorisation requires the latest medication reconciliation attestation to be `Complete`.

## Nurse intake / Nurse Navigator surface
- Intake measurements require explicit source units for BP, HR, RR, temperature, SpO2, weight and height.
- BMI/BSA are server-derived and not client-editable.
- Fall-risk score requires an explicit governed scale; the risk level is derived server-side.
- Medication reconciliation carries explicit allergy status and reconciliation status, provenance, attesting actor and timestamp.
- **Role mapping remains NEEDS CCA DECISION:** Intake Nurse may be a separate role or mapped to Nurse Navigator.

## Oncology Pharmacy
- Stale/superseded orders are rejected by Pharmacy actions.
- Pharmacy receives the current signed order lineage plus readiness/laboratory/toxicity/treatment context introduced in PC1.3.

## Day Care / Infusion Nurse
- Stale/superseded orders are rejected by Day Care actions.
- MAR retains explicit administered-dose unit and IV rate unit requirements from PC1.3.

## Radiation Oncology / Physics / Technologist
- RT prescription and plan versions are explicit.
- Physics QA and RO final approval are tied to the exact current prescription + plan version.
- Material replanning resets approvals and requires current-version reapproval.
- Fraction delivery is blocked when approvals are stale and each delivered fraction stores the prescription/plan version used.
