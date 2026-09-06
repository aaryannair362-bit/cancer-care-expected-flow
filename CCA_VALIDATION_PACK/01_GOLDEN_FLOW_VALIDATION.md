# CCA Golden Flow — Multidisciplinary Validation Script

Use the same synthetic patient throughout wherever the workflow permits. Review both **what is entered** and **what the next role receives**.

## A. Core systemic-therapy flow

| Step | Reviewer | Validation action | What must be checked |
|---|---|---|---|
| 1 | Front Desk | Register/search/check-in patient | Identity, duplicate prevention, referral/payer/consent/appointment, queue destination |
| 2 | Intake Nurse | Complete intake/vitals/history | Height, weight, BMI/BSA, BP, pulse, temperature, RR, SpO2, allergies, medications, performance status, pregnancy where applicable, escalation |
| 3 | Medical Oncologist | Open patient summary and consultation | Cancer history, diagnosis, pathology/imaging review, stage, biomarkers, ECOG/PS, investigations, assessment and plan |
| 4 | Medical Oncologist / Diagnostics | Order investigations | Indication, priority, prerequisites, duplicate checks, required-by date, result status and acknowledgement |
| 5 | MDT Coordinator | Submit case / prepare meeting | Clinical question, completeness, required specialties, case pack, agenda |
| 6 | MDT Chair + Specialists | Conduct/sign MDT decision | Options considered, rationale, dissent, recommendation, action owners, due dates, Chair sign-off |
| 7 | Treating Oncologist | Create/approve Treatment Plan | Intent, multimodality sequence, milestones, plan version, clinician approval |
| 8 | Medical Oncologist | Create systemic Treatment Order | Regimen, cycle/day, weight/height/BSA snapshot, labs, drug sequence, STANDARD → CALCULATED → FINAL ORDERED, route, diluent, volume, rate, duration, premeds/hydration/supportive care, modifications |
| 9 | Medical Oncologist | Perform treatment readiness / clearance | Criterion-by-criterion source/result/date/freshness/threshold/pass-fail; override role/reason/signature |
| 10 | Oncology Pharmacist | Verify order | Protocol/version, allergies, interactions, renal/hepatic context, dose recalculation, cumulative exposure, query/reject/verify states |
| 11 | Oncology Pharmacy | Prepare/release product | Actual prepared dose, concentration, diluent, volume, lot/batch/expiry, BUD/stability, independent check, label, release |
| 12 | Day Care Nurse | Receive and administer | Patient/product verification, access, premeds, sequence, start/end, rate changes, ACTUAL ADMINISTERED dose, interruptions/partial doses, observations |
| 13 | Day Care Nurse / Clinician | Reaction/extravasation if simulated | Immediate capture, vitals, interventions, grade, outcome, rechallenge/future precautions, longitudinal visibility |
| 14 | Clinician | Toxicity and cycle review | CTCAE-style event, onset/current/peak grade, attribution, intervention, treatment impact, hold/delay/modification linkage |
| 15 | Treating Oncologist | Response assessment | Baseline/current/nadir evidence, radiologist-proposed vs clinician-confirmed response, disease status and next decision |
| 16 | Treating team | Treatment completion | Reconcile planned vs actual treatment; generate treatment summary from signed source records |
| 17 | Treating team / Navigator | Surveillance / survivorship | Follow-up schedule, responsible specialty, investigations, late effects, red flags, patient-facing care plan |

## B. Radiation Oncology parallel flow

**RO Consultation → RT Prescription → CT Simulation → Contouring → Treatment Planning → RO Approval → Physics QA → Authorisation to Treat → RTT Setup/IGRT → Actual Fraction Delivery → OTV → Interruption/Replan → Completion Summary → Follow-up**

Validate specifically:

- prescription version is distinct from treatment-plan version;
- physician-prescribed vs planner-proposed vs physics-verified vs machine-delivered information is distinguishable;
- approved plan changes invalidate downstream approval/QA where required;
- prescribed dose is never silently treated as delivered dose;
- missed/rescheduled/partial fractions do not falsely increase cumulative delivered dose;
- OTV and RT completion notes contain clinically usable structured data.

## C. Surgical Oncology parallel flow

**Surgical Consultation → Surgical Plan → Pre-op Workup → Consent → Scheduling → Day-of-Surgery H&P → Theatre Safety Gate → Detailed Operative Note → Immediate Post-op → Daily Progress → Wound/Drain/Stoma → Complication → Final Histopathology → pStage Review → Adjuvant Handoff → Follow-up/Discharge**

Validate specifically:

- planned procedure and actual procedure are distinct;
- site/laterality are reconfirmed at appropriate safety checkpoints;
- operative specimens retain identity/orientation and link to Pathology accession;
- final pathology does not overwrite clinical stage; cStage and pStage remain visible;
- margins/nodes/treatment effect/biomarkers are structured;
- adjuvant handoff contains recovery status, pathology, readiness, owner, target date and acknowledgement;
- surgical discharge is specialty-appropriate rather than a generic discharge form.

## D. Inpatient oncology flow

**Admission Request → Bed/Admission → Admission H&P → Problem List → Daily Oncology Round → Nursing Assessment/Observations → Escalation → Consults/Transfers → Oncology Treatment if required → Discharge Readiness → Discharge Summary / Death Workflow**

Validate specifically:

- inpatient systemic treatment uses the same signed order → readiness → pharmacy → MAR safety chain;
- oral anticancer drugs are not automatically continued without clinician review;
- deterioration alerts require acknowledgement/action;
- discharge is blocked where unresolved treatment/safety conditions remain;
- medication reconciliation, pending results and next oncology action have named owners.

## E. Information continuity test

At every handoff ask the receiving clinician:

> “Can I make my next clinical/operational decision from what the system shows me, without calling the previous department to reconstruct missing information?”

If the answer is no, record exactly what information is missing, where it should originate and where it should be displayed.
