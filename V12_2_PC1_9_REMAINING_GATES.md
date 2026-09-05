# V12.2-PC1.9 — Remaining Gates

## 1. Full interactive browser UAT
Run the packaged build in unrestricted Chrome and Safari and execute the major workflows end to end: role switching, queues, patient summary, diagnostic ordering/results, MDT Chair review, multidisciplinary Treatment Plan, systemic order/readiness/Pharmacy/MAR, RT, surgery/adjuvant review, oral/continuous therapy, IPD, reports, long tables/modals, invalid inputs, printing/export, network/console errors, and Clinician Review ↔ Product Test mode.

## 2. CCA clinical-content configuration
PC1.9 still contains synthetic QA content. CCA specialists must configure/approve actual regimen doses and schedules, readiness thresholds, dose modifications, monitoring, formulary products, compatibility/stability/BUD rules, RT prescriptions/constraints, surgical subtemplates, fall-risk instrument, consent templates/languages/validity, ward/bed/location masters and tariffs.

## 3. Open register / architecture decisions
- `ORD-028`: decide whether Medical Oncology needs an **Ordered/target concentration** distinct from Pharmacy's authoritative actual prepared concentration (`PHM-016`).
- `SUR-039`: confirm the genuine consumer list for the derived adjuvant-review state. Product currently follows minimum-necessary visibility rather than exposing the decision to Pathology/IPD without a workflow reason.
- Front Desk consent projection: CCA Governance should confirm that completion/status/validity only is the correct operational scope.
- Configure who may be designated MDT Chair and how actual staff map to Intake Nurse vs Nurse Navigator.

## 4. Live external-system integration
Production sources/interfaces remain separate gates: HMIS, LIS, RIS/PACS, Pharmacy/inventory, MOSAIQ/OIS/TPS, SSO/IAM, facility/clinician masters. The prototype's read-only assay/reference-range master is a structural stand-in, not a claim of live LIS integration.

## 5. Production hardening
Protected production audit storage/WORM or equivalent controls, production IAM and patient-assignment scoping, hosted persistence, backup/restore, disaster recovery, monitoring, concurrency/load, security review, migration, operational support and training remain separate gates.

## 6. NEXUS / Guideline Pathway / Staging
Per project decision, this release keeps the NEXUS/Guideline/Staging experience as frontend structure only. No NCCN/NEXUS clinical-reasoning correctness is claimed here.

## Claim boundary
PC1.9 has **zero observed failures across the fresh executable suites listed in its validation results**. This does not mean zero undiscovered defects and does not establish production, clinical, regulatory, accreditation or live-integration readiness.
