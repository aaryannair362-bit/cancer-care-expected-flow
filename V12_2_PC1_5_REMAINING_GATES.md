# V12.2-PC1.5 — Remaining Gates

## CCA decisions / configuration

- `Intake Nurse` vs `Nurse Navigator`: one role or two distinct permissioned roles.
- CCA-approved fall-risk scale and cut-offs.
- CCA institutional formulary terminology, codes, routes and formulations.
- CCA regimen-specific readiness thresholds, freshness windows, monitoring and dose-modification rules.
- CCA Pharmacy compatibility, stability, BUD, storage, light-protection, filter and container content.
- `ORD-028` ordered/target concentration vs `PHM-016` actual prepared concentration.
- Front Desk visibility of consent/document-completion status.

## Track-B development still remaining

Continue row-level conformance, with no assumption that untested rows pass:

1. remaining Treatment Order rows not yet fully evidenced;
2. remaining Readiness/Monitoring rows and dose-modification rows;
3. remaining Pharmacy/MAR visibility and amendment checks;
4. Radiation Oncology remaining prescription/delivery rows beyond the version/approval controls already tested;
5. Surgery — universal plan, disease subtemplate, operative record, pathology/adjuvant handoff;
6. MDT and multidisciplinary Treatment Plan;
7. Investigations and Diagnosis/Staging/Pathology;
8. Response Assessment;
9. Oral/continuous therapy;
10. Inpatient, Financial and cross-cutting lifecycle/audit elements.

## Browser / UX gate

Full interactive Chrome/Safari UAT remains mandatory. Static/syntax checks do not prove interaction quality, modal behaviour, scrolling, responsive layout, role navigation or every button/state.

## Deployment / production gates

- real IAM/SSO/user lifecycle;
- protected/immutable production audit storage;
- database hardening, backup/restore and concurrency/load testing;
- HMIS/MOSAIQ/LIS/RIS-PACS/Pharmacy/RT integration testing against CCA's actual licensed interfaces;
- production observability and error/retry handling;
- institutional clinical-content sign-off.
