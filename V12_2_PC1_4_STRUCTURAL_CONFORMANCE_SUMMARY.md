# V12.2-PC1.4 — Structural Conformance Phase 2

**Purpose:** remediate evidence-backed structural defects identified by `CCA_Clinical_Data_Ownership_Input_Register_v1.1` without inventing CCA clinical content.

## Scope implemented

### 1. Final ordered dose is now a true DECIDED element
- Every systemic-treatment item requires an explicit final-dose decision reason before order signature.
- The item stores decision reason, deciding actor and timestamp.
- A protocol/calculated-dose variance still has its separate variance/modification reason.
- The signed order remains versioned/locked.

### 2. Explicit treatment-order supersession / stale-order protection
- A second active order for the same Treatment Plan + cycle + day is blocked by default.
- Replacement requires `supersedes_order_id` plus a mandatory supersession reason.
- The old Treatment Order, linked Pharmacy record and linked Infusion record become `Superseded`.
- Pharmacy and Day Care APIs reject action on a superseded/stale order.
- The replacement retains lineage to the previous order.

### 3. Allergy structure and medication-reconciliation attestation
- Explicit allergy status: `No known allergy | Allergy present | Unable to verify`.
- Allergen must come from the governed allergen master.
- Reaction, severity and provenance use governed sets; `Other` requires detail.
- Medication reconciliation requires explicit status: `Complete | Incomplete | Unable to verify`.
- Incomplete/unverified reconciliation requires a reason.
- Reconciliation stores actor, role, timestamp, source and attestation text.
- Systemic order authorisation requires the latest medication reconciliation attestation to be `Complete`.

> Current allergen master is a **Synthetic QA structural fixture**, not CCA clinical content. CCA must approve/configure the real allergen/terminology content.

### 4. Fall-risk structure
- A fall-risk score cannot be recorded without an explicit governed scale.
- The risk level is derived server-side from the selected scale and score; the client cannot dictate it.
- The current scale is explicitly marked **Synthetic QA** and exists only to test the product structure.

> CCA Nursing must decide the real scale, score range and cut-offs.

### 5. RT version-bound approval integrity
- RT prescription version and plan version are first-class version identifiers.
- Material prescription change creates a new prescription version and resets downstream planning approvals as applicable.
- Material plan revision after approval creates a new plan version and resets approval state.
- Physics QA requires the exact current plan version and cannot be completed before simulation/contouring/planning prerequisites.
- Radiation Oncologist final approval requires Physics QA for the exact current prescription + plan version.
- `Ready for Treatment` is derived only when current-version approvals are satisfied.
- Fraction delivery is blocked when approvals are stale/missing.
- Delivered fractions retain the prescription and plan version under which they were delivered.

### 6. Phase-1 structural controls preserved
Inherited PC1.3 controls remain active:
- explicit intake units and normalization,
- server-derived BSA,
- signed-order anthropometric snapshot/provenance,
- richer Pharmacy visibility and preparation structure,
- explicit MAR dose/rate units,
- role-surface visibility remediation.

## Fresh executed validation on PC1.4

| Suite | Result |
|---|---:|
| V12.2 defect remediation | **38 PASS / 0 FAIL** |
| V12 process + IPD | **48 PASS / 0 FAIL** |
| Legacy regression | **95 PASS / 0 FAIL** |
| Full 41-case scenario pack | **41 / 41 PASS** |
| Scenario preflight | **0 failures** |
| Scenario audit chain | **0 errors** |
| PC1 pre-clinician | **15 PASS / 0 FAIL** |
| PC1.1 UX | **9 PASS / 0 FAIL** |
| PC1.2 Mature Oncology UX | **19 PASS / 0 FAIL** |
| PC1.3 Track-B Phase 1 | **27 PASS / 0 FAIL** |
| **PC1.4 Track-B Phase 2** | **38 PASS / 0 FAIL** |
| Python compile checks | **PASS** |
| JS syntax: app + PC1 + PC1.2 + PC1.3 + PC1.4 | **PASS** |

The current legacy regression script executes 95 checks in this descendant build; all 95 passed.

## What this release does not claim
- It does **not** establish clinical correctness of synthetic regimens, thresholds, fall-risk cut-offs, allergens, Pharmacy compatibility/stability, RT constraints or other CCA-owned clinical content.
- It does **not** resolve the Intake Nurse vs Nurse Navigator role-model question.
- It does **not** complete browser UAT.
- It does **not** complete all 467 Track-B register rows.
- NEXUS-NCCN remains frontend-only.

## Track-B interpretation
This release closes/partially closes register conformance defects only where executable evidence exists. The accompanying updated register workbook records PASS only against checks actually demonstrated; untested checks remain unclaimed.
