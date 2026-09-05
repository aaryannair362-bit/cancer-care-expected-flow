# V12.2-PC1.5 — Track B Structural Conformance Phase 3

This phase is driven by `CCA_Clinical_Data_Ownership_Input_Register_v1.1`. It does not invent CCA clinical thresholds or institution-specific content.

## Scope completed

### Governed current medication
- current medication must come from the active formulary master;
- route must be allowed by the selected formulary item;
- dose requires numeric value + explicit governed dose unit;
- frequency, status, source, code/code-system, actor and timestamp are retained;
- medication-reconciliation attestation remains explicit.

### Treatment readiness
- criterion provenance is retained (`source_record_id`, dates/finalisation context);
- freshness is explicit and evaluated;
- per-condition outcome uses controlled states;
- monitoring requirements use `Required / Completed / Overdue / Abnormal / Missing`;
- signed overall readiness requires a clinician decision reason and attestation.

### Systemic treatment order
- treatment rows retain an explicit, unique sequence;
- rows are separated into `Pre-treatment`, `Anti-cancer treatment`, and `Post-treatment / supportive`;
- route and diluent are governed;
- rate/volume/duration consistency is server-validated;
- non-governed rounding is rejected;
- final-dose, administration-parameter and schedule decisions retain clinician rationale;
- cumulative-dose-before-order is derived from verified administration history.

### Pharmacy
- verification snapshot pins order/version, regimen/version, cycle/day, signed readiness and cumulative-dose context;
- preparation ignores client attempts to override server-governed compatibility/stability/BUD/storage/filter/container content;
- actual final concentration is calculated in Pharmacy from preparation data;
- wastage requires a reason;
- preparer and independent final checker cannot be the same named person;
- release requires a destination;
- server-derived preparation fields survive release unchanged.

### Day Care / MAR
- vascular access is structured;
- actual administered dose and unit are explicit;
- IV actual rate and rate unit are explicit;
- antineoplastic/targeted treatment requires chairside verification;
- the independent verifier must be separately named;
- administration variance requires a governed reason code;
- post-treatment observations require units;
- cumulative exposure is based on **actual administered dose**, including partial administration.

## Register evidence discipline

The Phase-3 workbook records evidence on 101 register rows. It does **not** mark untested rows as compliant. At publication time the Track-B matrix contains:

- 20 rows: `CONFORMS`
- 1 row: `MISSING`
- 22 rows: `NOT TESTED` verdict with partial evidence
- remaining rows: not yet assigned a final verdict

The single explicit `MISSING` item is `ORD-028 Final concentration`, which is an architecture/register decision rather than a blind coding defect. PC1.5 treats `PHM-016` as authoritative **actual prepared concentration** because actual preparation volume is known in Pharmacy. CCA must decide whether `ORD-028` should instead mean **ordered/target concentration** where the prescriber is required to specify one.

## Not claimed by this phase

- complete 467-row conformance;
- CCA-approved regimen thresholds, Pharmacy stability/compatibility content, formulary or nursing scales;
- browser usability acceptance;
- institutional clinical validation;
- production integrations or production IAM/infrastructure.
