# V12.2-PC1.4 — Remaining Gates

## P0 before external clinician/nurse/UX UAT

1. **Local browser smoke/UAT**
   - Chrome and Safari.
   - All main role navigation, modals, dropdowns, required fields, error states and responsive/table behaviour.
   - Verify Clinician Review Mode hides Synthetic QA values where intended.
   - Verify no raw JSON appears in clinician surfaces.

2. **Resolve Intake Nurse vs Nurse Navigator role model — NEEDS CCA DECISION**
   - Decide whether Intake Nurse is a separate role or a duty/surface of Nurse Navigator.
   - Then align RBAC, reviewer extract routing and UI naming.

3. **Current medication master / selection control**
   - Medication reconciliation now has governed provenance/status, but the full CCA medication/formulary-backed current-medication search/control still requires a dedicated Track-B pass.

## P1 Track-B structural conformance still to execute

Continue the 467-row conformance matrix. Recommended order:

1. Remaining Treatment Order rows — dose basis, route, diluent/volume, rate/duration, sequence, cumulative dose, supportive-order sections.
2. Treatment Readiness — every criterion source/freshness/outcome and overall decision visibility/audit.
3. Pharmacy — item-by-item verification fields, compatibility/stability content status, BUD derivation, wastage, independent checker and dispense lineage.
4. MAR — access/site, per-drug sequence, completion/variance, post-treatment observations and correction/amendment behaviour.
5. Intake — pain, ECOG/KPS, history, medication master, nutrition and remaining role-entry checks.
6. RT — prescription field controls, OAR/target structure, interruption semantics and full consumer visibility.
7. Surgery — plan vs operative artefact, disease-specific subtemplates, specimen/pathology/stage/adjuvant links.
8. MDT, Investigation, Diagnosis/Staging, IPD, Response, Consent/Documents, Finance, Cross-cutting.

## Track A — CCA clinical configuration decisions
These are intentionally not invented by engineering:
- actual regimen library, dose/schedule/caps/rounding,
- readiness thresholds and freshness windows,
- dose-modification rules,
- fall-risk scale/cut-offs,
- allergen/clinical terminology masters,
- monitoring requirements,
- formulary, compatibility/stability/BUD/preparation rules,
- RT prescriptions, OAR constraints, simulation/IGRT and Physics policies,
- disease/procedure-specific surgical template content,
- consents/documents and local approval policies.

## Later pilot / production engineering
- production IAM/SSO/session controls,
- protected/immutable production audit storage,
- production DB, migration/backup/restore/concurrency hardening,
- HMIS, LIS, RIS/PACS, Pharmacy/Inventory and MOSAIQ/OIS/TPS interfaces as licensed/available,
- load/performance/observability and operational recovery,
- deployment security and live integration validation.

## NEXUS
Frontend shell only in this release. Backend clinical-decision connection is intentionally deferred.
