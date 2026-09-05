# V12.2-PC1 — Remaining Gates Before CCA Clinician / Pilot Sign-off

## 1. Browser UAT — still required

Run the packaged build on an unrestricted workstation and execute the major flows in Chrome and Safari.

Required checks:
- login/logout and role switching;
- sidebar navigation and every PC1 page;
- Clinician Review Mode ↔ Product Test Mode;
- patient search, queue, summary and major-event journey;
- regimen library, readiness, treatment order and dose modification;
- pharmacy verify/query/prepare/dispense;
- Day Care MAR and infusion reaction;
- oral/continuous therapy create/hold/restart/dose-modify/complete;
- RT prescription/planning/Physics QA/fraction delivery;
- surgical plan/pre-op/operative record/pathology handoff;
- NEXUS frontend placeholder behavior;
- required fields, dropdowns, invalid values, modals, scroll/table usability;
- print/export presentation where applicable;
- console errors and failed network calls.

## 2. Medical Oncology clinical-content configuration — clinician decision required

CCA must approve/configure:
- actual regimens and indications;
- regimen versions and line/intent applicability;
- doses, dose caps and rounding policy;
- cycle/day schedules and planned cycles;
- regimen-specific ANC/platelet/renal/hepatic/cardiac rules;
- required lab freshness;
- premedications, hydration and supportive medications;
- dose-hold/delay/reduction/omit/discontinue rules;
- toxicity rules and monitoring schedules.

## 3. Oncology Pharmacy configuration — pharmacist decision required

CCA Pharmacy must approve/configure:
- local formulary and product mappings;
- allowed diluents/routes/concentrations;
- compatibility references;
- stability and beyond-use time;
- storage/light protection/filter/container requirements;
- compounding/independent-check rules;
- inventory/batch/expiry/wastage policy;
- pharmacy query/reject/escalation policy.

## 4. Radiation Oncology / Physics configuration — specialist decision required

CCA RO/Physics must approve/configure:
- disease-specific prescription templates;
- dose/fractionation and phase/boost structures;
- target/OAR data elements and constraints;
- simulation and immobilization options;
- image-guidance requirements;
- planning/Physics QA/approval sequence;
- interruption/rescheduling rules;
- TPS/OIS field mappings.

## 5. Surgical Oncology configuration — specialist decision required

CCA surgeons must approve/configure disease/procedure-specific subtemplates:
- procedure options and extent;
- laterality/site/approach choices;
- nodal procedures;
- reconstruction choices;
- pre-op requirements;
- synoptic operative-record fields;
- specimen/pathology linkage;
- post-op/adjuvant review triggers.

## 6. CCA institutional master-data setup

Still needed from CCA management/IT:
- facility and department structure;
- clinicians, schedules and locations;
- queue/routing rules including day-based routing;
- role/permission matrix confirmation;
- service/charge master;
- laboratory and radiology catalogues;
- consent/document/report templates;
- local status/approval/escalation rules.

## 7. Live integrations — later deployment gate

Not required for PC1 clinician review, but required before a connected production pilot as applicable:
- HMIS registration/MRN/billing/payment/services;
- MOSAIQ interfaces available to CCA;
- LIS lab orders/results;
- RIS/PACS imaging orders/results/images;
- Pharmacy/inventory;
- RT TPS/OIS/machine interfaces;
- identity/SSO and other hospital infrastructure.

Exact integration claims must be based on the interfaces licensed/enabled in CCA's installed systems.

## 8. NEXUS-NCCN engine — intentionally not in PC1

PC1 contains the frontend only:
- Patient Clinical Snapshot;
- Current Guideline Position;
- Applicable Options;
- Missing Information;
- Why NEXUS Reached This Position;
- Run/refresh/send-to-MDT/create-plan controls.

The actual extraction/pathway/NCCN decision engine and licensed content are a later integration and validation gate.

## 9. Production hardening / operational validation

Before production use, separately validate:
- protected production audit storage (prototype hash chain is not WORM storage);
- backup/restore and disaster recovery;
- deployment monitoring/logging;
- concurrency/load with target CCA usage;
- large longitudinal records and large patient queues;
- session/security configuration for production infrastructure;
- data migration/import if required;
- user training and pilot support process.

## Expected clinician-review outcome

Feedback should be classified as:

- **ACCEPT** — product structure/workflow is correct;
- **CONFIGURE** — software can represent the requirement but CCA needs different values/options/rules;
- **PRODUCT GAP** — the software cannot represent a required workflow/data element.

PC1 is designed to move as much feedback as possible from PRODUCT GAP into CONFIGURE.
