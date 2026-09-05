# CCA Cancer Care AI OS — Final Product Build V12.2

This ZIP is the consolidated final **clinician-review / product-validation build** derived from V12.2-PC1.9 Structural Conformance Phase 7.

## Included scope

- Registration, intake, consultation, investigations and longitudinal patient summary
- Diagnosis, staging and pathology data structures
- MDT / Tumour Board workflow with distinct Coordinator and MDT Chair sign-off roles
- Multidisciplinary Treatment Plan across Medical Oncology, Radiation Oncology and Surgical Oncology
- Systemic Treatment Order with dose provenance, readiness, dose modification and signed-order versioning
- Oncology Pharmacy verification, preparation and dispense workflow
- Day Care / Infusion MAR, independent checks, reactions and toxicity workflow
- Oral / continuous therapy lifecycle
- Radiation Oncology planned-vs-delivered treatment workflow with version-bound approvals
- Surgical Plan separated from immutable/versioned Operative Record and post-operative pathology/adjuvant handoff
- Inpatient oncology, response assessment, finance and cross-cutting audit/version controls
- Clinical Data Ownership & Input Register v1.1 Track-B Phase 7
- Clinician Review Mode and Product Test Mode
- NEXUS / Guideline Pathway / Staging frontend shells only; no NCCN/NEXUS reasoning backend is claimed in this package

## Clinical-content boundary

Institution-specific clinical content remains configurable. Synthetic QA/demo regimens, thresholds, formularies, consent rules, RT prescriptions, surgical templates, pharmacy compatibility/stability values and other test content are **not CCA-approved patient-care guidance**.

## Validation boundary

The latest packaged descendant has executable evidence for the requested remediation/process/regression/scenario and structural-conformance suites recorded in the included release evidence. The product should still undergo full interactive Chrome/Safari clinician UAT before external sign-off.

Do not interpret this package as a claim of production, regulatory or clinical validation readiness.

## Run locally

```bash
python3 reset_demo.py
python3 server.py
```

Open `http://127.0.0.1:8765`

Demo PIN: `2026`
