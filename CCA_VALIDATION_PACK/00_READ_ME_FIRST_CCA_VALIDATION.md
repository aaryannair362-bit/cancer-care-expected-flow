# CCA Cancer Care AI OS — Clinician & Stakeholder Validation Release

**Product build:** V12.2-PC4.0 — Full PRD Conformance  
**Purpose of this release:** CCA clinician and stakeholder validation of **workflow, information standards, role ownership, documentation structure, safety/state behavior and usability** before institutional configuration and production integration.

## What CCA is being asked to validate

This is not a request to approve the synthetic demo doses/regimens as CCA clinical policy. Reviewers should validate whether the **software captures the right information, from the right person, at the right stage, in the right format, with the right downstream handoff**.

For every screen/flow, please answer:

1. Is this the correct step in the real CCA workflow?
2. Is the correct role responsible for entering, verifying, signing or only viewing the information?
3. Are all clinically important fields present?
4. Are mandatory / optional / conditional fields correct?
5. Are dropdowns, units and value choices appropriate?
6. Are calculated values shown correctly and are their source values visible?
7. Is information presented in a clinically usable format rather than as unnecessary narrative?
8. Are planned, ordered, prepared, delivered and actual values clearly separated?
9. Are the status changes, queues and handoffs correct?
10. Are the blocking safety checks and override requirements appropriate?
11. Is the generated/signable clinical note sufficient for real clinical documentation?
12. After signing, should this information remain immutable and require an amendment? If not, state the correct behavior.

## What not to approve as institutional clinical content in this review

The build intentionally contains synthetic/demo clinical content so workflows can be exercised. Do **not** treat those values as CCA-approved patient-care content.

The following require CCA institutional population / specialist sign-off before patient use:

- Regimen Master values and treatment protocols
- Formulary details
- Treatment-readiness thresholds
- Dose modification / hold / restart rules
- Dose-rounding policy
- Pharmacy compatibility / stability / BUD content
- RT templates, dose/fractionation sets, OAR constraints and technique-specific rules
- Surgery procedure templates
- Pathology disease-specific synoptic datasets
- Consent wording and patient education content
- Institution-specific scheduling and escalation policies

## Not part of this validation release

- NEXUS/NCCN backend clinical reasoning — frontend shell only
- OPD voice transcription accuracy
- OCR accuracy
- Regulatory / certification assessment
- Live LIS, RIS/PACS, Pathology LIS, TPS/OIS/R&V, Pharmacy ERP, Billing, IAM/SSO or ABDM integrations
- Production security, HA/DR and infrastructure validation

## How to run

### macOS / Linux

```bash
python3 reset_demo.py
python3 server.py
```

Open: `http://127.0.0.1:8765`  
Demo PIN: `2026`

On macOS, `Start_CCA_Prototype.command` may also be used.

### Windows

Use `Start_CCA_Prototype_Windows.bat` included in this build. Python 3 must be installed.

## In-product validation mode

This distribution includes a **CCA Validation Center** in the sidebar and a **Validate this screen / Validate field / Validate table column** control on the PRD workflow surfaces. Reviewers can record structured findings directly in the product while they test.

For consolidated/offline review, use `CCA_Clinician_Stakeholder_Validation_Workbook.xlsx`, which contains the 246-screen and 4,669-field validation matrices.

## How reviewers should work

- Select the reviewer’s real role at login.
- Use the seeded **synthetic patient only**.
- Follow the role-specific test path in `02_ROLE_BASED_VALIDATION_GUIDE.md`.
- Follow the integrated patient journey in `01_GOLDEN_FLOW_VALIDATION.md`.
- Record findings in `CCA_Clinician_Stakeholder_Validation_Workbook.xlsx`.
- For every problem, record **Role → Screen → Field / Action → Expected → Actual → Severity → Suggested correction**.

## Issue severity

- **S1 — Safety / workflow blocker:** could allow wrong patient/treatment/route/dose/site/status, bypass a clinical gate, or prevent safe care.
- **S2 — Major:** clinically important information missing/wrong, incorrect ownership/handoff, unusable documentation or major workflow mismatch.
- **S3 — Moderate:** information/control present but needs correction, better default/value set, clearer status/presentation or fewer steps.
- **S4 — Minor:** wording, alignment, naming, cosmetic or convenience improvement.

## Final validation decision

Each specialty should return one of:

- **Accepted for CCA configuration / integration phase**
- **Accepted with required changes**
- **Not accepted — workflow or information model requires redesign**

This review validates the **product model and operational flow**, not institutional clinical policy contained in synthetic test values.
