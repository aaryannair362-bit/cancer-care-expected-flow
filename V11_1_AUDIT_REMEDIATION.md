# V11 Independent Audit → V11.1 Remediation Register

Date: 4 September 2026

| Audit item | V11.1 change | Live evidence | Status |
|---|---|---|---|
| C1: readiness UI hardcoded ANC/platelet unit | Removed hardcoded readiness units; laboratory value + unit is first-class input; readiness reads latest Final lab server-side | `800 cells/uL` → `0.8 ×10^9/L` → ANC blocker | **FIXED** |
| No unit selector | Added test-specific mandatory unit selectors in Laboratory result UI; blank on new result | Missing ANC unit → HTTP 409 | **FIXED** |
| Potential old-unit inheritance on result correction | Final lab immutable; amendment requires reason and explicit units on final submission | Amendment without explicit units → HTTP 409 | **FIXED** |
| Administration path not independently exercised | Ran Pharmacy → Day Care → six MAR item execution → completion | 6/6 MAR items; reconciliation passes | **TESTED** |
| RT fraction delivery not independently exercised | Ran prescription → Physics QA → physician approval → delivered + missed fraction | 2.67 Gy delivered fraction + missed fraction with reason persist | **TESTED** |
| Finance sees ordered dose | Removed raw treatment order from Finance read projection; estimate returns no dose field | Finance payload has no `treatment_order` / `ordered_dose` | **HARDENED** |
| RT protocol breadth | No unsafe fabricated protocol defaults added | Skeletons remain marked for Rad Onc/Physics review | **OPEN — CLINICAL CONTENT** |
| Regimen breadth / only one orderable | Governance retained; historical imports remain non-orderable | Content activation still requires local clinical + pharmacy review | **OPEN — CLINICAL REVIEW CAPACITY** |
| Synthetic terminology mappings | No false production-code claim added | Existing content remains labelled local/synthetic/pending mapping | **OPEN — INTEROPERABILITY MASTER DATA** |
| Production WORM audit | Prototype hash-chain warning retained | Audit verifies, with explicit production limitation | **OPEN — PRODUCTION INFRASTRUCTURE** |

## Design decision: laboratory source of truth

The most important change is not merely a dropdown. V11.1 moves the safety boundary to the correct place:

```text
Laboratory Result
  value + explicit unit + result date + finalizer + timestamp
         ↓
Latest Final Laboratory Record
         ↓
Server unit normalization
         ↓
Server-owned regimen-version criteria
         ↓
Treatment Readiness
         ↓
Signed Proceed / Modified / Hold / Delay / Stop decision
```

Medical Oncology can view the source values, units and timestamps but cannot redefine them on the readiness screen.

## Final laboratory corrections

```text
Final Lab v1
   ↓ correction requires reason
New Final Lab Amendment v2
  supersedes = v1
  actor/time/reason preserved
   ↓
Readiness uses latest Final amendment
```

The original Final result remains reconstructable for audit and medicolegal review.
