# V12.2-PC1.2 — Mature Oncology UX & Workflow Summary

## Purpose

Frontend-first remediation to make the oncology product usable as a clinician-facing workflow rather than a technical prototype. The validated V12.2 state/safety backend remains the source of truth.

## Major UX changes

- Patient-centric oncology workflow stepper: Patient → Assessment → Investigations → MDT → Treatment Plan → Treatment Order → Readiness → Delivery → Response.
- Clean investigation ordering for Laboratory and Imaging with clinical indication and downstream status visibility.
- One multidisciplinary Treatment Plan supporting Medical Oncology, Radiation Oncology and Surgical Oncology in any clinically required combination (1, 2 or 3 modalities), with named participating clinicians.
- Medical Oncology order header with cancer/site, intent/line, regimen/version, cycle/day, start date, treating oncologist, weight, height and BSA.
- Readable treatment execution sequence: pre-treatment/premedication/hydration → anti-cancer treatment → post-treatment/supportive/rescue.
- Regimen-specific readiness domains grouped into Hematology, Renal, Hepatic, Cardiac, Toxicity, Required Investigations and Drug/Regimen-specific criteria.
- Structured dose variance/modification display inside the treatment order.
- Oncology Pharmacy workflow redesigned around Verification → Query → Verified → Prepared → Dispensed, with visible compatibility/stability placeholders for institutional configuration.
- Day Care treatment-day workspace redesigned around pre-check → ordered sequence → MAR → reaction management → completion.
- Rich infusion reaction event writes to the longitudinal toxicity record.
- Oral/continuous therapy workflow expanded to dose, schedule, food instructions, dispensing, monitoring, missed-dose education and adherence.
- Radiation Oncology redesigned into planned prescription, planning/physics/RO approvals and delivered fractions.
- Surgical Oncology redesigned into immutable intended Surgical Plan vs separate Operative Record, followed by histopathology/pathological stage/adjuvant planning.
- Synthetic clinical values remain visible only in Product Test Mode and are masked in Clinician Review Mode.
- NEXUS remains frontend-only and is not presented as an active NCCN engine.
- Raw JSON is not used by the new clinician-facing PC1.2 surfaces.

## Evidence-informed design basis

The UX structure was benchmarked against publicly available oncology workflow and safety sources, including:

- 2024 ASCO-ONS Antineoplastic Therapy Administration Safety Standards: ordering, preparing, dispensing, administration, monitoring, adherence, toxicity and complications.
- Elekta MOSAIQ medical oncology: consistent drug ordering, dose/diluent calculation, cumulative dose management and concise treatment summaries.
- eviQ safe anti-cancer administration: pretreatment tests reviewed, documented clearance, current consent, pharmacy verification, premedications/fluids and administration in protocol order.
- ASTRO minimum radiation oncology data elements: diagnosis, site, modality, technique, dose/fraction, planned/delivered fractions, planned/delivered total dose and treatment dates.
- AAPM TG-275 / MPPG 11.a: physics plan and chart review before treatment and during/end of treatment.
- American College of Surgeons Commission on Cancer: structured/synoptic operative documentation with universal plus cancer-specific elements.

These sources inform data presentation and workflow architecture only. CCA-approved clinical content remains a separate institutional configuration/sign-off gate.

## Validation

Existing executable gates remain unchanged and pass when run against the local server:

- Defect remediation: 38 PASS / 0 FAIL
- V12 process + IPD: 48 PASS / 0 FAIL
- Regression: 94 PASS / 0 FAIL
- Synthetic scenario pack: 41 / 41 CASE PASS; preflight 0; audit errors 0
- PC1 pre-clinician acceptance: 15 PASS / 0 FAIL
- PC1.1 clinician UX acceptance: 9 PASS / 0 FAIL
- PC1.2 mature oncology UX acceptance: 19 PASS / 0 FAIL
- JavaScript syntax: app.js PASS, pc1.js PASS, pc1_2.js PASS

## Remaining gate

Full interactive browser UAT remains mandatory before external clinician distribution. Headless Chromium could not be reliably completed in the managed environment. Run the package locally in Chrome/Safari and verify all role navigation, forms, state transitions, modals, scrolling, responsive behavior and print/export presentation.
