# V12.2-PC1 validation note

PC1 adds a dedicated structural acceptance suite: `v12_2_pc1_preclinician_acceptance.py`. The release must also preserve all V12.2 defect/process/regression/scenario gates. Full browser interaction remains an external UAT gate because Chromium localhost access is administrator-blocked in this environment.

---

# CCA Oncology OS V12.2 — Final Defect-Remediation Runtime Validation

**Build:** `CCA_Cancer_Care_Functional_Product_v12_2_Final_Defect_Remediation`  
**Validation date:** 4 September 2026  
**Method:** fresh isolated HTTP/API execution against reset SQLite product-test runtimes. Tests exercise real writes, persistence, server-side authorization, role-scoped reads, safety/state gates, downstream reconciliation, OPD/IPD continuity, clinical-content governance, versioning and audit integrity.

## Release verdict for the executed product-test scope

**All requested executable V12.2 acceptance suites completed with zero observed failures in the tested scope.**

This statement is narrower than claiming the product has no possible defects. Full browser interaction, production IAM/WORM infrastructure, live external integrations and specialist approval of real patient-care clinical content are not demonstrated by these runs.

## Results

| Validation stream | Result | Canonical evidence |
|---|---:|---|
| Targeted defect remediation | **38 PASS / 0 FAIL** | `validation_evidence/V12_2_DEFECT_REMEDIATION_38_PASS.log` |
| V12 process + IPD acceptance | **48 PASS / 0 FAIL** | `validation_evidence/V12_2_PROCESS_48_PASS.log` |
| Legacy/full regression | **94 PASS / 0 FAIL** | `validation_evidence/V12_2_REGRESSION_94_PASS.log` |
| Supplied scenario pack | **41 CASE PASS / 0 CASE FAIL** | `validation_evidence/V12_2_SCENARIOS_41_OF_41_PASS.log` |
| Scenario preflight | **0 failures** | `validation_evidence/V12_2_SCENARIOS_41_RESULTS.json` |
| Scenario audit-chain check | **HTTP 200 / 0 audit errors** | `validation_evidence/V12_2_SCENARIOS_41_RESULTS.json` |

The 38, 48, 94 and 41 counts overlap and must not be summed as unique requirements.

## Targeted defect-remediation coverage

The 38-check suite is the current superset of the previous defect reproduction set plus later findings. It demonstrates, among other items:

- final radiology and pathology records reject silent mutation and require linked amendments;
- active/orderable clinical-content masters reject direct mutation;
- stale/invalid workflow writes are rejected where covered;
- queue destinations are restricted to the governed location master;
- appointments cannot be created in the past;
- medication route, allergy severity and Care Plan states use governed value sets;
- finance idempotency is enforced for the tested payment path;
- rejected specimens create a recollection loop;
- critical lab results create/route tasks and can be acknowledged;
- report history can retrieve both current and historical versions;
- death propagates discontinuation/cancellation to active treatment/future work;
- Treatment Order cannot be created from an unsigned/inactive Treatment Plan;
- discharge is blocked while inpatient systemic orders remain unresolved;
- patient queue assignment grants only the intended receiving access path;
- laboratory plausibility and unit handling reject impossible ANC values.

### New lab plausibility defect — closed

Fresh results:

| Input | Runtime result |
|---|---|
| `ANC 999999 ×10^9/L` | **409 rejected** — outside configured product-test plausibility range |
| `ANC 350 ×10^9/L` | **409 rejected** |
| `ANC 3.5 ×10^9/L` | **200 Final result accepted** |
| `ANC 800 cells/µL` | **200 accepted**, unit retained at source and normalized to canonical readiness value |

The configured plausibility envelope is intentionally broad and serves as a transcription/data-quality guard. It does not replace disease/regimen-specific readiness criteria.

## Process + IPD coverage

The 48-check process run demonstrates:

- department-level Patient Journey updates;
- Pharmacy visibility of patient-specific dose variables required for verification;
- exact order → verification → preparation → release → MAR reconciliation;
- Day Care vs Inpatient administration-setting separation;
- inpatient order rejection without active admission;
- admission → inpatient systemic treatment → ward MAR → toxicity/observation → discharge → OPD follow-up;
- discharge blocking until inpatient systemic treatment is resolved;
- readmission linked to the existing cancer episode;
- inpatient toxicity feeding subsequent Treatment Readiness;
- continuous/open-ended therapy without forced Day Care/compounding;
- phase cancellation/amendment by superseding Treatment Plan version;
- multiple cancer-episode isolation;
- RT Delivered/Missed/Rescheduled behavior with cumulative dose derived only from Delivered fractions;
- audit-chain integrity after process execution.

## Regression coverage

The 94-check regression run demonstrates the retained core behavior including:

- role-surface and server-side read/write restrictions exercised by the suite;
- fresh-patient workflow scaffolding;
- duplicate detection;
- nurse vitals/BSA path;
- governed Treatment Plan → Treatment Order separation;
- systemic-order safety/completeness;
- Pharmacy verification/preparation/dispense;
- Day Care MAR execution;
- MDT recommendation separation from executable ordering;
- Radiation Oncology approval/Physics QA/fraction state gates;
- Surgical Oncology pre-op/performed/pathological-stage append behavior;
- finance separation from clinical authorization;
- audit and record-version history.

## 41-scenario institutional-content run

The supplied process pack contains **41 distinct case IDs**. V12.2 executes all 41 using synthetic institutional content specifically created to test software flow without falsely treating external/reference clinical material as approved patient-care content.

Result:

**41 CASE PASS / 0 CASE FAIL; PREFLIGHT_FAIL 0; AUDIT_HTTP 200; AUDIT_ERRORS 0**

The cases exercise systemic-only, surgery-only, RT-only, multimodality sequences, OPD/IPD, toxicity, hold, emergency admission, discharge, continuous therapy, pharmacy query loops, RT interruption, external-plan paths, multiple cancer episodes, recurrence, treatment refusal and death/closure behavior.

## Synthetic content boundary

The QA content master contains 53 synthetic templates: 21 orderable systemic regimens, 16 RT templates, 14 surgery templates and 2 continuous-therapy templates, plus 5 synthetic formulary items. The existing synthetic TCHP demo regimen remains separately present, giving a reset runtime 22 active/orderable demo/test systemic regimens.

This content is intentionally labelled **synthetic product testing/demo only**. It is not a specialist-approved clinical library and must not be used to infer medical correctness or patient-care suitability.

Historical OpenMRS-derived regimen imports remain non-orderable references.

## Browser/UI status

Backend/API execution and persistence were run live. `python -m py_compile` and `node --check static/app.js` pass. A full headless-Chromium localhost interaction run could not complete in this managed container, so full browser UX interaction remains **not independently verified in this environment** and is not counted as a pass.

## Remaining non-product-test release boundaries

These do not invalidate the executable product-test results above, but remain separate gates before production patient use:

- production authentication/IAM rather than demo PIN identity;
- protected/WORM audit storage;
- live HMIS/MOSAIQ/ARIA/LIS/PACS/RIS/TPS/pharmacy-ERP integrations;
- institution specialist approval of real clinical regimens, RT templates, surgery templates, formulary and value sets;
- regulatory/licensing/conformance work;
- NCCN/NEXUS clinical correctness;
- OPD voice transcription and OCR accuracy.
