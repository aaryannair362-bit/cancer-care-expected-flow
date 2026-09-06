# Role-Based CCA Validation Guide

The reviewer should log in with the closest matching role and validate **Input → View → Decision/Action → Output/Handoff**.

| Role | Main areas to validate | Core questions |
|---|---|---|
| Front Desk | Registration, identity, duplicate search, payer/referral, consent completion, appointment/check-in, routing | Is non-clinical data sufficient? Is clinical data hidden? Is routing simple and unambiguous? |
| Intake Nurse | Vitals, height/weight/BMI/BSA source data, allergies, medication reconciliation, PS, pregnancy, symptoms, screening, escalation | Are measurements/units/source/time correct? Are derived values not manually authoritative? Is escalation safe? |
| Nurse Navigator | Coordination queue, barriers, contact log, investigations, MDT/treatment milestones, follow-up | Does the Navigator see enough to coordinate without gaining inappropriate authoring rights? |
| Medical Oncologist | Patient summary, consultation, diagnosis/stage/biomarkers, investigations, MDT, plan, systemic order, readiness, toxicity, response, completion | Can the oncologist make and document the treatment decision safely with minimal duplication? |
| MDT Coordinator | Submission, completeness, agenda, case pack, actions | Can cases be prepared without clinically signing the recommendation? |
| MDT Chair | Live board, recommendation, rationale, dissent, action owners, final sign-off | Is Chair approval clearly authoritative and immutable after signing? |
| Oncology Pharmacist | Verification queue, recalculation, interactions, cumulative exposure, preparation, BUD/stability, double check, release | Are ordered vs prepared values clear? Can Pharmacy query but not edit the physician order? |
| Day Care / Infusion Nurse | Treatment-day queue, product receipt, identity verification, MAR, access, actual delivery, reactions, observation/discharge | Can the nurse document what actually happened rather than only “given/not given”? |
| Radiation Oncologist | Consultation, prescription, simulation review, contour/plan approval, OTV, interruptions, completion | Are prescription, plan and delivery separate and version-aware? |
| Radiation Physicist | Prescription-plan concordance, independent calculation, plan/transfer/deliverability/QA review, sign-off | Can Physics verify without modifying the RO prescription? |
| Radiation Technologist | Schedule, setup, IGRT, shifts, delivered fraction, missed/partial treatment | Is actual delivered data captured correctly and cumulative dose derived only from delivered treatment? |
| Surgical Oncologist | Consultation, plan, pre-op, operative note, pathology review, pStage, adjuvant handoff, follow-up/discharge | Are planned vs actual surgery, pathology linkage and post-op handoff clinically complete? |
| Anaesthetist | Pre-anaesthesia assessment/fitness, peri-operative considerations and handoff | Are anaesthetic facts owned by Anaesthesia and visible to Surgery appropriately? |
| Surgical / Stoma-Wound Nurse | Theatre/readiness support, wound, drain, stoma, education and longitudinal follow-up | Are devices/outputs/status longitudinal and not retyped into disconnected notes? |
| Pathologist | Accession, grossing, blocks/slides, synoptic report, margins/nodes, biomarkers/molecular, frozen, amendment, critical communication | Is pathology provenance, specimen lineage and final-report immutability correct? |
| Radiologist | Worklist, protocol, structured oncology reporting, lesion tracking, response proposal, addendum, critical communication | Are baseline/current/nadir and target/non-target/new lesions usable? Is proposed response separate from clinician confirmation? |
| Radiology Coordinator | Protocol/scheduling/prerequisites/result loop | Are orders closed-loop from request to completed study/report? |
| Laboratory / Phlebotomy | Order, collection, specimen acceptance/rejection, result, critical result, units/plausibility | Are units/source values preserved? Are impossible values blocked and recollection/critical-result workflows closed-loop? |
| Inpatient Oncology Clinician | Admission H&P, problem list, ward round, orders, consults, transfer, treatment continuity, discharge | Can inpatient care continue the same cancer episode/treatment context without duplicating the oncology record? |
| Inpatient Oncology Nurse | Nursing assessment, observations/EWS, MAR, fluid balance, lines/devices, escalation, discharge readiness | Are time-series measurements and escalation actions clear? |
| Dietitian / Nutrition | Assessment, intervention, monitoring | Does the role see the relevant cancer/treatment context without unrelated chart exposure? |
| Psycho-Oncology | Distress/psychosocial assessment, intervention, follow-up | Are sensitive notes appropriately scoped? |
| Palliative Care | Symptom/goals-of-care documentation and shared plan | Is palliative care integrated without incorrectly equating it with treatment abandonment? |
| Finance / Billing | Eligibility, estimate, pre-auth, approval scope, utilisation, charges, claims, denial/appeal | Can Finance consume clinical facts without changing treatment? Is minimum-necessary clinical visibility respected? |
| Hospital Admin | Users/roles/resources, masters, governance, audit/configuration | Can Admin administer software without becoming universal clinical author? Do clinical masters require clinical approval? |
| HIM | Record integrity, merge/unmerge, amendments, releases, data quality | Is the legal/clinical record preserved with versions, provenance and audit? |

## For each role, record at least

- 1 item that is correct and should be **frozen**;
- every missing field/control;
- every field that should be conditional rather than mandatory;
- every unnecessary field that slows the workflow;
- every incorrect role permission;
- every incorrect status or handoff;
- every note/report that would be inadequate in real clinical practice;
- every piece of information that should be pulled from another system rather than manually entered.
