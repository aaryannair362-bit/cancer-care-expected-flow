# In-Product CCA Validation Mode

The CCA validation distribution includes a **CCA Validation Center** in the product sidebar for every non-external reviewer role.

## What reviewers can record inside the product

On every role-authorised PRD screen, reviewers can validate:

- the complete screen / workflow;
- an individual field;
- a repeating-table column;
- how information is entered and displayed;
- role ownership and permissions;
- mandatory / conditional logic;
- units / calculations / dropdowns;
- safety gates / overrides;
- status / queue / handoff behavior;
- clinical note / report adequacy;
- planned-vs-actual presentation;
- whether information should come from an external integration instead of manual entry.

## Validation verdicts

- **Correct — Freeze**
- **Change Required**
- **Missing**
- **Should Be Conditional**
- **Should Be Integration**
- **Not Applicable**
- **Needs Discussion**

## Severity

- **S1 — Safety / workflow blocker**
- **S2 — Major**
- **S3 — Moderate**
- **S4 — Minor**
- **None** for items accepted as correct or non-issue observations.

## Specialty sign-off

The CCA Validation Center allows each reviewer role to record:

- Accepted for CCA configuration / integration phase
- Accepted with required changes
- Not accepted — workflow or information model requires redesign

The sign-off also captures what should be frozen, required changes, CCA-owned clinical content and integration requirements.

## Offline / consolidated tracker

Use `CCA_Clinician_Stakeholder_Validation_Workbook.xlsx` when multiple reviewers need one shared offline tracker. It contains:

- Role Validation
- Screen Validation — all **246** PRD screens
- Field Validation — all **4,669** atomic fields/table columns
- Issue Register
- Specialty Signoff
- CCA Content & Integration register
- Dashboard

The in-product and workbook verdict/severity language is intentionally identical so feedback can be consolidated without reinterpretation.
