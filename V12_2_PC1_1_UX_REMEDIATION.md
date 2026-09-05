# V12.2-PC1.1 Clinician UX Remediation

Frontend-only remediation of V12.2-PC1. The validated clinical workflow, safety, persistence and authorization logic are not intentionally changed.

## Changes
- Removed raw JSON presentation from template, protocol/formulary, pathology, report, readiness and external MDT views.
- Added human-readable category views for regimen, radiation, surgery and continuous/oral therapy templates.
- Simplified role navigation into a primary Clinical Workspace with secondary tools collapsed under More tools.
- Patient Summary now prioritizes current disease state, treatment status, readiness, delivery and next step.
- Synthetic values continue to be masked in Clinician Review Mode.
- NEXUS remains frontend-only.

## Remaining gate
Full browser UAT by Nurse, UX reviewer and Oncologist remains required.
