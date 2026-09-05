# V12.2-PC1.2 Remaining Gates

## Before external clinician UAT

1. Run the package locally in Chrome and Safari.
2. Smoke-test Medical Oncology: Patient Overview → Assessment → Investigations → MDT → Treatment Plan → Treatment Order → Readiness → Delivery → Response.
3. Create a plan with exactly 1 modality, 2 modalities and 3 modalities; verify the correct specialties appear in the shared plan.
4. Place at least one laboratory and one imaging order and verify the downstream status trail remains understandable.
5. Verify treatment-order tables do not expose raw JSON and remain readable at common laptop widths.
6. Verify Clinician Review Mode masks synthetic doses/fractionation while preserving workflow structure.
7. Verify Pharmacy, Day Care, RT and Surgical Oncology layouts in the roles that use them.
8. Check all modals for clipping/scrolling and all primary buttons for valid state transitions.

## Still requiring CCA clinical/institutional configuration

- Actual systemic regimens, doses, cycle schedules, dose caps, rounding rules, readiness thresholds, premedication/hydration/supportive medication and monitoring schedules.
- Pharmacy formulary, compatibility, stability/BUD, concentration, storage, light protection, filters, containers and wastage rules.
- RT prescriptions, fractionation, target/OAR constraints, simulation/IGRT/physics QA practices and interruption policies.
- Disease-specific surgical procedure/subtemplate fields and local operative documentation requirements.
- Facility/department/location/user/schedule/queue/service/catalogue masters.

## Later engineering gates

- Production IAM/SSO/session hardening.
- Protected/immutable audit infrastructure and operational monitoring.
- Production database/migrations/backups/concurrency hardening.
- HMIS, LIS, RIS/PACS, pharmacy/inventory and available MOSAIQ/RT interfaces.
- Load/performance testing at five-hospital scale.
- Final production-quality reports/exports and document storage hardening.
- NEXUS-NCCN backend connection (frontend only in PC1.2).
