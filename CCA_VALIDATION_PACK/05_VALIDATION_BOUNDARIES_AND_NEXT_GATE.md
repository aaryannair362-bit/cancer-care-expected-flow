# Validation Boundary and Next Gate

## This release can be used to validate

- end-to-end oncology workflow fit;
- role-specific information requirements;
- forms, tables, dropdowns and display structure;
- treatment planning/order/execution separation;
- pharmacy/day-care/RT/surgery/inpatient process behavior;
- documentation templates;
- statuses/queues/handoffs;
- signing/amendment/audit concepts;
- CCA clinical-master structure.

## This release is not authorised for patient care

All demo clinical data is synthetic. Specialist clinical-content approval, integration testing and production controls are separate gates.

## After clinician validation, the implementation sequence should be

1. Resolve S1/S2 workflow/information findings.
2. Freeze approved screen/field/state model.
3. Obtain CCA-owned institutional clinical masters/content.
4. Configure and clinically sign off those masters.
5. Connect real enterprise integrations.
6. Execute multidisciplinary UAT with realistic CCA cases.
7. Complete performance/security/backup/DR/production IAM work.
8. Complete regulatory/licensing work separately where applicable.
9. Production pilot under a controlled rollout plan.

## Acceptance target for this review

A specialty is considered validated only when the clinician can complete their work and the receiving role can continue the patient journey **without reconstructing missing clinical information outside the system**.
