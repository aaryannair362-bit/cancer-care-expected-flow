# V12.2-PC1.1 Remaining Gates

## Before sharing for formal clinician UAT
1. Run locally in Chrome and Safari and confirm login, role navigation, patient switching, modals, forms, tables, scrolling and responsive layout.
2. Confirm no clinician-facing page exposes raw JSON or technical object dumps.
3. Confirm Clinician Review Mode is the default and synthetic dose/fraction values are masked.
4. Confirm role-specific primary navigation feels usable for Medical Oncology, Day Care/Infusion Nursing and Oncology Pharmacy.

## Reviewer UAT
- Nurse: intake, treatment-day checks, MAR, infusion reaction, toxicity handoff.
- Oncologist: summary, diagnosis/staging, MDT, plan, order, readiness, dose modification, response.
- UX reviewer: navigation, density, terminology, actions, tables, modal behavior and visual hierarchy across roles.

Classify feedback only as ACCEPT, CONFIGURE or PRODUCT GAP.

## Still deliberately outside PC1.1
- Real CCA clinical content sign-off and institutional masters.
- Live HMIS/LIS/RIS-PACS/MOSAIQ/pharmacy/RT integrations.
- NEXUS-NCCN backend.
- Production IAM, protected audit infrastructure, scale/performance hardening and deployment observability.
