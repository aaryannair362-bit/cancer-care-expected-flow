# CCA Cancer Care AI OS V12.2-PC1 — Pre-Clinician Candidate

## Purpose

V12.2-PC1 is a clinician-facing structural refinement of the frozen V12.2 defect-remediation core. It is intended to reduce avoidable product-structure feedback during CCA clinician review while keeping clinical values that require institutional approval explicitly separate from software behavior.

This is **not** a claim of institutional clinical-content approval. Synthetic content remains product-test/demo content only.

## PC1 additions

1. Regimen-specific readiness-rule schema, grouped by hematology, renal, hepatic, cardiac and result-freshness domains.
2. First-class treatment sequence presentation: pre-treatment/premedication/hydration → anti-cancer treatment → post-treatment/supportive/rescue.
3. Structured dose-modification architecture with trigger, affected domain, allowed action and protocol-specific new-dose rule.
4. Monitoring/investigation requirements per regimen with phase/category/result-source/freshness semantics.
5. Radiation Oncology planned-versus-delivered course presentation.
6. RT approval chain with prescription approval, plan versioning, Physics QA and RO final approval.
7. Disease-specific configurable Surgical Oncology subtemplates layered over a universal surgical plan.
8. Explicit separation of Surgical Plan from Operative Record.
9. Rich infusion-reaction capture linked to MAR workflow.
10. Dedicated oral/continuous systemic therapy workflow with hold/restart/dose-modify/completed/discontinued lifecycle.
11. Pharmacy compatibility/stability/BUD/storage/light/filter/container structure.
12. Clinician Review Mode masks obviously synthetic clinical execution values; Product Test Mode retains synthetic QA values for testing.
13. NEXUS / Guideline Pathway / Staging frontend shells only. No NCCN reasoning engine is executed in PC1.
14. Richer clinician patient summary and major-event patient journey presentation.

## Safety/content boundary

- Existing V12.2 server-side safety gates, normalization, plausibility checks, authorization, audit and state-transition controls remain intact.
- PC1 does not convert synthetic regimen/RT/surgical values into clinical guidance.
- Values requiring CCA approval are labelled/configured as such in clinician-facing mode.
- NEXUS is presentation-only in this package; it must not be represented as generating real guideline recommendations.

## Validation target

PC1 must preserve the V12.2 executable baseline:

- 38 / 38 defect-remediation checks
- 48 / 48 process + IPD checks
- 94 / 94 regression checks
- 41 / 41 supplied synthetic scenarios
- 0 scenario preflight failures
- 0 scenario audit-chain errors

In addition, `v12_2_pc1_preclinician_acceptance.py` checks the new PC1 structural requirements.

## Browser limitation

Headless Chromium exists in the build environment, but access to `localhost` is blocked by administrator policy (`ERR_BLOCKED_BY_ADMINISTRATOR`). Therefore browser interaction cannot be independently executed here. JavaScript syntax and server/API/state/persistence paths are validated; browser UAT remains a separate release gate on an unrestricted workstation.
