# Information Standards Validation Checklist

This checklist asks CCA clinicians to validate the **information model**, not just whether a screen exists.

## 1. Identity / encounter / episode
- Patient identifiers remain visible at clinical decision points.
- Cancer Episode is explicit and multiple primaries remain separated.
- Encounter/location/date/time/author are captured where clinically relevant.
- No department silently overwrites another specialty’s signed record.

## 2. Measurements and units
- Height and weight contain value, unit, measurement method/source and time.
- BMI/BSA are derived and source measurements remain visible.
- Lab result retains source value + source unit; canonical normalized value is separate.
- Dose, concentration, volume, rate and duration never share ambiguous units.
- RT planned dose and delivered dose are separate.

## 3. Diagnosis, staging and biomarkers
- Diagnosis/histology/site/laterality are structured.
- Stage system/edition/date are visible.
- cTNM and pTNM are distinct; pStage never erases cStage.
- Non-TNM disease classification is supported without forcing fake TNM values.
- Biomarker result includes specimen, method/assay where relevant, result, date and source.

## 4. Treatment Plan and systemic order
- Treatment Plan is distinct from Treatment Order.
- Plan includes intent, modality sequence, milestones and approval/version.
- Order identifies regimen/version, line, cycle/day, planned cycles and start date.
- Weight/height/BSA/renal/hepatic context used for the signed order are preserved as a snapshot.
- Every drug clearly shows **STANDARD → CALCULATED → FINAL ORDERED → PREPARED → ACTUAL ADMINISTERED**.
- Dose change requires percentage/value plus reason/clinical context.
- Premedication, hydration, treatment drug and supportive/post-treatment sequence is explicit.

## 5. Readiness / safety gate
- Each criterion shows source result, unit, timestamp/freshness, threshold source and pass/fail.
- Missing criteria do not silently become “ready”.
- Override requires authorised role, reason and signature where appropriate.
- Readiness rules are regimen/version-specific rather than a universal client-provided checklist.

## 6. Pharmacy
- Verification is independent of prescribing.
- Recalculation inputs are visible.
- Allergy/interactions/organ function/cumulative exposure are visible where needed.
- Product preparation captures actual prepared dose, diluent, volume, concentration, lot/batch, expiry/BUD and checker.
- Pharmacy query returns the workflow to the prescriber rather than editing the order.

## 7. Administration / MAR
- Identity/product verification is documented.
- Route/site/access/sequence are explicit.
- Start/end/pauses/rate changes are timestamped.
- Partial/omitted/interrupted treatment records the **actual delivered amount** and reason.
- Reaction/extravasation has a dedicated acute workflow and longitudinal follow-up.

## 8. Toxicity / oral therapy
- Toxicity has onset, current grade, peak grade, attribution, action and resolution status.
- Toxicity links to hold/delay/reduction decisions.
- Oral therapy includes achievable formulation/schedule, dispense quantity/days supply, monitoring, adherence and patient communication.
- A hold is not considered complete until the patient communication step is closed.

## 9. Radiation Oncology
- Consultation/prescription/simulation/contours/plan/approval/physics QA/delivery are distinct objects/states.
- Prescription and plan versions are traceable.
- Changes invalidate affected approval/QA steps.
- Fraction records capture actual delivered dose and interruption/missed/partial treatment.
- OTV and completion summary compare prescribed vs actual delivery.

## 10. Surgical Oncology
- Surgical Plan is distinct from Operative Record.
- Actual operation contains team, approach, findings, key steps, oncology findings, specimens, margins/frozen information, blood loss/transfusion, drains/devices, complications and post-op plan.
- Specimens link to Pathology accession.
- Wound/drain/stoma records are longitudinal.
- Final pathology → pStage → surgeon review → adjuvant handoff is explicit and closed-loop.

## 11. Pathology / Radiology
- Final reports are immutable; correction occurs by addendum/amendment.
- Pathology retains specimen → cassette/block → slide/test lineage where required.
- Oncology pathology provides structured margins/nodes/treatment effect/biomarkers/pTNM.
- Radiology has comparison study identity, persistent lesion IDs and serial measurements.
- Radiologist-proposed response remains separate from treating-clinician confirmation.
- Critical/unexpected results require direct acknowledgement/communication where configured.

## 12. Inpatient
- Active problems, daily plan, nursing observations, medications, devices and consults are longitudinal.
- Systemic anticancer therapy cannot bypass the oncology order/pharmacy/MAR chain because the patient is admitted.
- Transfer includes sending/receiving acknowledgement.
- Discharge reconciles medications, devices, pending results and next oncology action.

## 13. Response, completion and survivorship
- Baseline/current/nadir and source evidence are explicit.
- Proposed response ≠ clinician-confirmed response.
- Treatment summary is assembled from signed source records, not manually re-created.
- Planned vs actual systemic/RT/surgery exposure is visible.
- Surveillance tasks have due dates and responsible owners.

## 14. RBAC, signing and audit
- Users see the minimum information necessary for their role.
- View permission does not automatically grant create/edit/sign permission.
- Signed clinical records are immutable.
- Amendments retain original version and reason.
- Every clinically important state change has actor/date/time/reason/audit evidence.
- Clinical master activation requires clinical approval, not only IT/Admin approval.
