# Track B — Structural Conformance Phase 2

Register basis: `CCA_Clinical_Data_Ownership_Input_Register_v1.1`.

## Evidence-backed Phase-2 focus

| Area | Register concern | Product behaviour now tested |
|---|---|---|
| Fall risk | MEASURED score requires explicit selected scale; risk level must not be client-entered | Missing scale blocks; governed Synthetic QA scale accepted; level derived server-side |
| Allergy | governed status/allergen/reaction/severity/source | Free allergen/reaction blocked; coded values accepted; status maintained |
| Medication reconciliation | explicit attested Complete/Incomplete/Unable to verify | Missing status blocks; incomplete without reason blocks; Complete stores actor/time/attestation |
| Final ordered dose | DECIDED = reason + signature | Order signing blocked without dose-decision reason; each drug stores reason/actor/time |
| Signed-order replacement | no silent mutation | duplicate active order blocked; explicit supersession creates lineage; old order cannot be acted on |
| RT plan/approval | version-specific Physics + RO approval; no stale delivery | stale plan actions blocked; replan increments version and resets approvals; fractions store plan/Rx versions |

## Phase-2 acceptance
`v12_2_pc1_4_structural_conformance_phase2_acceptance.py`

Fresh result: **38 PASS / 0 FAIL**.

## Evidence policy
A row in `TRACK_B_CONFORMANCE` is marked `CONFORMS` only when the six requested checks are sufficiently evidenced. Where only a subset has executable proof, individual columns are marked PASS but verdict remains `NOT TESTED` until the remaining checks are executed.
