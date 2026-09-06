# PRD / Conformance Source Index for CCA Validation

This distribution asks clinicians to validate the product against the complete requirements chain rather than only the visible screen title. The following files are the canonical reference set packaged with the product.

| Source | File | Validation purpose |
|---|---|---|
| Part A + B roles 1–6 | `requirements/CCA_Oncology_HIS_EMR_PRD_Part1_A-B.md` | End-to-end workflow, platform rules, roles 1–6 |
| Part B roles 7–21 | `requirements/CCA_Oncology_HIS_EMR_PRD_Part2_B-roles-7-21.md` | Remaining role-by-role responsibilities, queues, input/view/output |
| Part C C.1–C.6 | `requirements/CCA_Oncology_HIS_EMR_PRD_Part3_C-registration-to-investigations.md` | Registration, Intake, Navigation, Medical Oncology, Diagnosis/Staging, Investigations |
| Part C C.7–C.11 | `requirements/CCA_Oncology_HIS_EMR_PRD_Part4_C-MDT-to-Pharmacy.md` | MDT, Treatment Plan, Systemic Order, Readiness, Oncology Pharmacy |
| Part C C.12–C.14 | `requirements/CCA_Oncology_HIS_EMR_PRD_Part5_C-DayCare-Toxicity-Oral.md` | Day Care/MAR, Toxicity, Oral/Continuous therapy |
| Part C C.15–C.17 | `requirements/Pasted markdown(20260905-181629).md` | Radiation Oncology, Physics, RTT |
| Part C C.18 | `requirements/Pasted markdown(20260905-185907).md` | Surgical Oncology |
| Part C C.19–C.26 target-state completion | `requirements/PC4_0_TARGET_STATE_COMPLETION_C19_C26.md` | Pathology, Radiology, Inpatient, Response, Completion, Survivorship, Finance, Administration |
| Master field dictionary | `PC4_0_MASTER_FIELD_DICTIONARY.md` | Canonical field/input inventory |
| Calculation catalogue | `PC4_0_CALCULATION_CATALOGUE.json` | Derived calculations and source/input relationships |
| Clinical note catalogue | `PC4_0_CLINICAL_NOTE_CATALOGUE.md` | Structured signable note/document families |
| Value-set catalogue | `PC4_0_VALUE_SET_CATALOGUE.md` | Dropdown/controlled values |
| Unit catalogue | `PC4_0_UNIT_CATALOGUE.md` | Canonical units and normalization |
| Handoff matrix | `PC4_0_HANDOFF_MATRIX.md` | Role-to-role downstream information flow |
| CCA-configurable masters | `PC4_0_CCA_CONFIGURABLE_MASTERS.md` | Institutional clinical content ownership/configuration |

## Validation precedence

1. The supplied detailed Part-C PRD is the primary source where it exists.
2. Part A/B defines cross-cutting lifecycle, role ownership and information-flow requirements.
3. Canonical dictionaries/catalogues normalize fields, calculations, units, notes, value sets and handoffs.
4. `[CCA CONFIG]` values must be supplied/approved by CCA; reviewers validate the structure and consumption point, not the synthetic value.
5. `[INTEGRATION]` items should be validated as integration requirements, not reclassified as manual-entry fields.