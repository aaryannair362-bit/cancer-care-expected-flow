# Source and Scope — V12.2 Final Defect Remediation

## Product basis

V12.2 implements and hardens the CCA cancer-centre requirements supplied in this project: registration/routing, intake, Oncology OPD, diagnostics, MDT, treatment planning, systemic order execution, Pharmacy verification/preparation/dispensing, Day Care/MAR, toxicity/readiness/response, Radiation Oncology, Surgical Oncology, finance, role-based access, longitudinal history and audit/versioning.

The governing record hierarchy is:

> **MDT recommendation → specialist Treatment Plan → patient-specific authorised Order → Verification/Preparation/Dispensing → actual Administration/Delivery.**

These are different records and statuses. MDT never silently becomes an executable order.

## V12 laboratory safety boundary

Laboratory result values and units are first-class clinical data. Final numeric results require explicit units; finalized results are immutable and corrections create linked amendments. Treatment Readiness resolves the latest Final laboratory record server-side, normalizes its stored units and then evaluates the exact governed regimen version. Client-supplied readiness values/units are not accepted as the clinical source of truth.

## Open-source historical regimen input

Repository: `openmrs/openmrs-module-oncology`  
Branch used for provenance: `master`

V12 imports the 12 historical regimen YAMLs found in its `regimens/` directory:

- `5FULeucovorin.yaml`
- `AC.yaml`
- `CHOP.yaml`
- `CMF.yaml`
- `COP.yaml`
- `CarboTaxol.yaml`
- `CyclophosphamideSingleAgent.yaml`
- `Doxorubicin20.yaml`
- `Doxorubicin60.yaml`
- `Paclitaxel175.yaml`
- `Paclitaxel175ReChallenge.yaml`
- `Paclitaxel80.yaml`

The normalized entries preserve source path/blob provenance and useful order-set concepts such as cycle count/interval, relative treatment day, medication category, medication identity, dose/unit, route, timing and dilution/instruction fields where present.

They are **historical references, not current prescribing authority**. Every import is immutable, non-orderable and must first be cloned to a CCA working copy before any local clinical editing/review is possible.

## OpenMRS license boundary

The repository `LICENSE` is **Mozilla Public License 2.0** and includes the **OpenMRS Healthcare Disclaimer**. The local `clinical_content/OPENMRS_NOTICE.txt` records this boundary. MPL/source-notice/distribution obligations still need to be handled correctly in any commercial release, so legal review is recommended for the intended packaging.

The healthcare disclaimer separately reinforces the clinical rule already used in V12: source content is not a substitute for professional judgment or local verification.

## Other software references

- **OpenMRS Order Extension** — architecture/reference for cyclical orders and chemotherapy-order concepts.
- **OpenEMR** — architecture/reference for centrally managed EHR form/document/template infrastructure. V12 does not copy its UI.
- Commercial oncology systems are used as workflow/UX benchmarks, not as copied proprietary content.

## Clinical governance boundary

Source import proves only that the schema can ingest the historical artifact. To make a local CCA working-copy regimen orderable, the institution must complete/localize its clinical sequence, map every medication to an Active institution formulary version, add current server-owned readiness criteria, record independent Medical Oncology and Oncology Pharmacy review and explicitly activate the reviewed CCA version.

The active TCHP content and initial formulary supplied in the demo database are synthetic workflow-test data only.

## External boundaries

- NEXUS/NCCN content is intentionally excluded from V12 and can be connected later through a separately governed guideline layer.
- Voice/OCR are interface-ready but not treated as clinical source-of-truth without human confirmation.
- Live MOSAIQ, ABDM, PACS/RIS, LIS, TPS/OIS, pharmacy ERP/inventory and production IAM remain external integrations.

## Distributed data

The clean distributed database contains synthetic demonstration patient data, synthetic active demo treatment content and non-orderable historical reference imports. Acceptance-test-created local mappings/approvals are removed by `reset_demo.py` before packaging.


## V12.2 synthetic institutional product-test content

V12.2 adds an explicitly synthetic institutional content pack so software workflows can be exercised across the complete 41-case process pack without converting historical/reference material into patient-care authority. The pack contains 21 orderable systemic-regimen templates, 16 Radiation Oncology templates, 14 Surgical Oncology templates, 2 continuous-therapy templates and 5 synthetic formulary items. Together with the original synthetic TCHP demo regimen, a reset runtime exposes 22 active/orderable synthetic/demo systemic regimens for product testing.

This content is **product-test/demo only**. It is not a clinical recommendation, institution-approved regimen library or patient-care source. Historical/open-source imports remain non-orderable references unless separately governed.
