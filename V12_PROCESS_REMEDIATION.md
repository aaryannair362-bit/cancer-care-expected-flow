# V12 — 35/41-Case Process Audit Remediation Register

**Input:** CCA Oncology OS process scenario execution report, 4 September 2026.  
**Note:** the supplied pack headline says 35 cases, but the tables contain **41 unique case IDs** (8 T + 6 B + 6 M + 4 S + 5 U + 12 E).

## Engineering findings and disposition

| Process-audit finding | V12 disposition | Evidence |
|---|---|---|
| Pharmacy cannot see nurse-entered weight/height/BSA | **Fixed** | Pharmacy read projection + role surface; live acceptance verifies BSA/formula visibility |
| Rad/Surg Onc cannot see active systemic order | **Fixed with minimum-necessary projection** | Both specialties receive active signed `treatment_order`; Pharmacy/MAR remain hidden |
| No Patient Journey entity | **Fixed** | Dedicated `journey` record with major care-stage transitions |
| No admission / ward / bed / IPD model | **Fixed at oncology workflow layer** | Admission, ward/bed, IPD observations, toxicity, specialty review, discharge, readmission |
| Inpatient chemotherapy impossible | **Fixed structurally** | Inpatient setting on treatment order; same Pharmacy chain; Inpatient Nurse MAR; Day Care blocked |
| Day Care cannot escalate to IPD | **Fixed structurally** | `escalate_to_ipd` links infusion context to emergency admission |
| IPD toxicity not feeding next cycle readiness | **Fixed** | longitudinal toxicity source is consumed by Treatment Readiness |
| Discharge → OPD continuity missing | **Fixed** | discharge summary plus linked post-discharge appointment |
| Continuous/non-cyclical therapy thin | **Expanded** | open-ended oral/hormonal/continuous courses; no cycle/end date required |
| Modality removal / plan amendment | **Expanded** | per-phase amendment/cancellation creates superseding Treatment Plan version |
| RT interruption/rescheduling | **Expanded** | Delivered/Missed/Rescheduled fractions; cumulative dose uses delivered only |
| Multiple cancer episodes risk merging | **Expanded** | explicit episode IDs on core treatment/course objects; second-episode test passes |
| Management patient projection too broad | **Hardened** | per-patient Management header reduced to MRN/current location/status |

## Content blocker deliberately not bypassed

The scenario report found only one orderable systemic regimen. V12 **does not auto-approve additional borrowed/reference regimens** just to make test cases execute.

A regimen becomes orderable only through the existing governance chain:

`Reference / draft → CCA working copy → formulary mapping → server safety rules → Medical Oncology review → Pharmacy review → Admin activation`

This remains the principal blocker to running disease-specific systemic cases such as lymphoma, AML, gastric, colorectal, cervix, head & neck and lung with clinically meaningful orders.

RT and surgical skeletons likewise remain non-prescriptive until Radiation Oncology/Physics or Surgical Oncology review.

## Scenario capability interpretation after V12

The process engine now has structural support for the important previously absent patterns:

- Day Care and Inpatient systemic administration
- concurrent-modality visibility
- RT interruption
- conditional/cancelled phases
- emergency Day Care → IPD escalation
- open-ended oral/hormonal therapy
- multiple cancer episodes
- treatment hold/delay propagation
- death/episode closure
- external-origin Treatment Plan without an internal MDT

That does **not** mean every case is clinically executable. Where a disease-specific approved regimen/protocol is absent, the correct V12 behavior remains `BLOCKED — governed clinical content unavailable`.

## Recommended next work order

1. **CCA clinical-content review sprint:** approve high-volume systemic regimens rather than weakening the activation gate.
2. **Radiation content pack:** top site-specific prescription/fractionation templates reviewed by Radiation Oncology + Physics.
3. **Surgical content pack:** site/procedure/pre-op defaults reviewed by Surgical Oncology.
4. **Run scenario pack again** after the content pack exists; preserve per-case handoff/visibility/reconciliation evidence.
5. Production integration/IAM/audit-storage hardening after clinical workflow/content validation.
