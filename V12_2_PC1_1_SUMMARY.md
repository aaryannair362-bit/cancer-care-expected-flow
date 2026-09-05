# V12.2-PC1.1 Clinician UX Remediation

## Purpose
Frontend-only remediation after PC1 browser review identified confusing navigation and raw JSON presentation. The V12.2 clinical workflow, safety, persistence, authorization and validation core were preserved.

## UX changes
- Raw JSON removed from clinician-facing template, protocol/formulary, pathology, generated report, readiness-result and external MDT views.
- Regimen, Radiation, Surgical and Continuous/Oral templates now render as labelled clinical cards, tables, lists and field chips.
- Role navigation is reduced to a primary **Clinical Workspace**; secondary tools are collapsed under **More tools**.
- Patient Summary prioritizes diagnosis/disease state, treatment plan/order, readiness, delivery and the next action.
- Regimen template view shows Treatment Sequence, Monitoring and Dose Modification as clinical tables.
- RT templates show Prescription Structure, Planning & Approval, Targets/OARs and Course Workflow.
- Surgery templates show Surgical Plan, Pre-op Requirements and separate Operative Record fields.
- Continuous/oral templates show Therapy Structure, Lifecycle and treatment-monitoring fields.
- Clinician Review Mode continues to mask synthetic clinical values.
- NEXUS remains frontend-only.

## Fresh executed validation
- 38 / 38 defect-remediation PASS
- 48 / 48 process + IPD PASS
- 94 / 94 regression PASS
- 41 / 41 scenario cases PASS; preflight 0; audit errors 0
- 15 / 15 PC1 pre-clinician checks PASS
- 9 / 9 PC1.1 UX-remediation checks PASS
- app.js syntax PASS
- pc1.js syntax PASS

## Remaining validation boundary
Full interactive browser UAT is still required on the actual deployment, particularly with a nurse, UX reviewer and oncologist. This release does not claim that visual usability is clinically accepted until that review occurs.
