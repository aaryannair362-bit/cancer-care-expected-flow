# CCA CANCER CARE — ONCOLOGY HIS + EMR
# MASTER FUNCTIONAL & CLINICAL PRODUCT REQUIREMENT INVENTORY
## Document 1 of N — PART A (End-to-End Workflow) and PART B (Roles 1–6)

**Document status:** Target-state build specification
**Audience:** Product management, UX, frontend, backend, QA, clinical stakeholders (medical oncology, radiation oncology, surgical oncology, pharmacy, nursing, pathology, radiology, physics, administration)
**Nature of document:** This is a *requirement inventory*, not an audit. It states what the finished product must contain, irrespective of what currently exists in the build.

---

## 0. HOW TO READ THIS DOCUMENT

### 0.1 Requirement classification tags

Every requirement in this document carries one of the following classifications. These tags are load-bearing — engineering and CCA clinical governance divide their work along this line.

| Tag | Meaning | Owner |
|---|---|---|
| **[PRODUCT]** | Software structure, behaviour, state machine, screen, field, calculation engine, permission, workflow. Must be built. Not negotiable by site. | Vendor / engineering |
| **[CCA CONFIG]** | Institutional clinical content that populates a product structure. The *structure* is [PRODUCT]; the *content* is supplied by CCA. | CCA clinical governance |
| **[CCA CONFIG — CLINICAL SIGN-OFF]** | As above, but requires named clinical authority approval and versioning before go-live (thresholds, doses, consent wording, protocol rules). | CCA clinical governance + named approver |
| **[DERIVED]** | System-calculated. Never hand-entered. Formula fully specified in Part E. | Vendor / engineering |
| **[INTEGRATION]** | Depends on an external system (LIS, RIS/PACS, TPS, R&V, billing, national ID, SMS/email gateway). | Vendor + CCA IT |

**Rule applied throughout:** where a clinical threshold, dose, regimen, consent text or institutional policy is required, this document defines the *field, data type, unit, versioning, consumption point and behaviour* and marks the value itself `[CCA CONFIG]`. No clinical thresholds, regimen doses or consent wording are invented in this document.

### 0.2 Requirement ID scheme

Format: `MODULE-SUBMODULE-NNN`

| Prefix | Module |
|---|---|
| `GEN` | Cross-cutting / platform |
| `REG-FD` | Registration / Front Desk |
| `INT-NUR` | Intake Nurse |
| `NAV` | Nurse Navigator |
| `MO-CON` / `MO-DX` / `MO-INV` / `MO-PLN` / `MO-ORD` / `MO-RDY` / `MO-MOD` / `MO-RVW` | Medical Oncology sub-domains |
| `RO` / `RO-RX` / `RO-SIM` / `RO-PLN` / `RO-OTV` | Radiation Oncology |
| `PHY` | Radiation Physics |
| `RTT` | Radiation Technologist |
| `SO` | Surgical Oncology |
| `PAT` | Pathology |
| `RAD` | Radiology |
| `RADC` | Radiology Coordinator |
| `MDT` | Multidisciplinary Team |
| `PHA` | Oncology Pharmacy |
| `MAR` | Day Care / Infusion / Medication Administration |
| `TOX` | Toxicity / Adverse Events |
| `ORL` | Oral / Continuous Anticancer Therapy |
| `IPD` | Inpatient Oncology |
| `RSP` | Response Assessment |
| `TXS` | Treatment Completion / Treatment Summary |
| `SURV` | Surveillance / Survivorship |
| `FIN` | Financial Counselling / Billing |
| `ADM` | Administration |
| `PTP` | Patient-facing |
| `CFG` | Configurable masters |

Requirement rows are consolidated in **PART U — Final Master Requirement Checklist** (later document in this set).

### 0.3 Document map

| Part | Contents | Document |
|---|---|---|
| **PART A** | End-to-end oncology workflow, state machines, cross-cutting platform rules | **This document** |
| **PART B** | Role-by-role requirements (purpose, worklist, patient header) — 21 roles | **This document (roles 1–6)** + following documents |
| PART C | Screen-by-screen requirements | Document 3+ |
| PART D | Field / input dictionary | Document 4+ |
| PART E | Calculation catalogue | Document 5 |
| PART F | Clinical note / document catalogue + Document Requirement Matrix | Document 6 |
| PART G | Dropdown / value-set catalogue | Document 7 |
| PART H | Unit catalogue | Document 7 |
| PART I | Treatment Order specification | Document 8 |
| PART J | Pharmacy specification | Document 8 |
| PART K | Day Care / MAR specification | Document 9 |
| PART L | Radiation specification | Document 10 |
| PART M | Surgical specification | Document 11 |
| PART N | Pathology specification | Document 12 |
| PART O | Radiology specification | Document 12 |
| PART P | MDT specification | Document 13 |
| PART Q | Inpatient specification | Document 13 |
| PART R | Response / Treatment Completion / Survivorship | Document 14 |
| PART S | Handoff matrix | Document 15 |
| PART T | CCA-configurable clinical-content masters | Document 15 |
| PART U | Final master requirement checklist (every requirement, ID'd) | Document 16 |

---

# PART A — END-TO-END ONCOLOGY WORKFLOW

## A.1 The clinical spine

The product must support a single longitudinal record organised around the **Cancer Episode** — not around visits, not around encounters, not around departments. Every clinical artifact in the system (note, order, result, image, plan, administration record, toxicity entry) attaches to exactly one Cancer Episode, and a patient may have more than one concurrently (e.g. a treated breast primary under surveillance plus a new colorectal primary under active treatment).

**GEN-EPI-001 [PRODUCT]** — Cancer Episode is a first-class object with its own identifier, independent of patient identifier and independent of visit identifier.

**GEN-EPI-002 [PRODUCT]** — Every clinical record must be attributable to one Cancer Episode. Records that legitimately span episodes (allergies, comorbidities, social history, baseline demographics) are held at patient level and displayed within every episode.

**GEN-EPI-003 [PRODUCT]** — Where a patient has more than one active Cancer Episode, every screen must display an unambiguous episode selector, and every write action must record which episode it was written against. No screen may allow a clinician to write to an ambiguous episode.

### A.1.1 End-to-end flow (department/event level)

```
REGISTRATION
   → INTAKE (vitals, anthropometrics, allergies, PS screen, triage)
      → CONSULTATION (Medical / Radiation / Surgical Oncology)
         → DIAGNOSIS ESTABLISHMENT (histology + biomarkers + imaging)
            → INVESTIGATIONS (Pathology, Radiology, Laboratory, Cardiac, Nuclear medicine)
               → STAGING (clinical stage; later pathological stage)
                  → MDT / TUMOUR BOARD
                     → TREATMENT PLAN (intent, modality sequence, line)
                        ├── SYSTEMIC THERAPY
                        │     → Treatment Order → Readiness → Pharmacy
                        │       → Day Care Administration → Toxicity → Post-cycle Review
                        ├── ORAL / CONTINUOUS THERAPY
                        │     → Counselling → Dispense → Adherence/Refill Review → Toxicity
                        ├── RADIATION ONCOLOGY
                        │     → RT Prescription → Simulation → Contouring → Planning
                        │       → Physics QA → RO Approval → Fraction Delivery
                        │       → Weekly OTV → RT Completion
                        └── SURGICAL ONCOLOGY
                              → Surgical Plan → Pre-op Assessment → Consent → Scheduling
                                → Surgery → Post-op → Histopathology → Pathological Stage
                                  → Adjuvant Handoff
                           ↓
                     INPATIENT ONCOLOGY (may be entered from any branch)
                           ↓
                  RESPONSE ASSESSMENT
                           ↓
             TREATMENT COMPLETION → CANCER TREATMENT SUMMARY
                           ↓
        SURVEILLANCE / FOLLOW-UP / SURVIVORSHIP CARE PLAN
                           ↓
            (recurrence/progression → re-enters at Consultation or MDT
             as a NEW LINE within the same Cancer Episode)
```

**GEN-FLW-001 [PRODUCT]** — Progression/recurrence must not create a new Cancer Episode by default. It creates a new **Line of Therapy** and a new **Disease Status** event within the same episode. A new Cancer Episode is created only for a new primary malignancy, and the system must require explicit clinician selection between "new line / progression of existing episode" and "new primary — new episode".

### A.1.2 Cancer Episode state machine

| State | Entered when | Exited when | Who can transition |
|---|---|---|---|
| `SUSPECTED` | Registration/consultation with suspicion, no tissue diagnosis | Histological or cytological confirmation, or exclusion | MO / SO / RO |
| `DIAGNOSED — STAGING IN PROGRESS` | Tissue diagnosis confirmed | Clinical stage recorded | MO / SO / RO |
| `STAGED — PLANNING` | Clinical stage recorded | Treatment Plan signed | MO / SO / RO / MDT |
| `ON TREATMENT` | First treatment activity signed (first cycle order released, first fraction delivered, surgery performed, oral therapy started) | Treatment completion, discontinuation or death | Treating clinician |
| `TREATMENT INTERRUPTED` | Hold / delay exceeding a configured interval `[CCA CONFIG]` | Treatment resumed or discontinued | Treating clinician |
| `TREATMENT COMPLETED` | End-of-treatment review signed | Recurrence or progression | Treating clinician |
| `SURVEILLANCE` | Survivorship/Surveillance Care Plan signed | Recurrence, progression, transfer of care, death | MO / SO / RO / Navigator |
| `PROGRESSED / RECURRED` | Clinician-confirmed response = Progressive Disease, or recurrence documented | New line commenced | Treating clinician |
| `TRANSFERRED / REFERRED OUT` | Care handed to external provider | Return of care | MO / Administrator |
| `DECEASED` | Death recorded | — | Clinician / Administrator |
| `LOST TO FOLLOW-UP` | Configured number of missed scheduled reviews `[CCA CONFIG]` | Patient re-presents | System-proposed, clinician/navigator confirmed |

**GEN-FLW-002 [PRODUCT]** — Episode state is `[DERIVED]` from underlying clinical events wherever derivation is unambiguous, but must be **clinician-confirmable and clinician-overridable with a recorded reason**. The system proposes; a human confirms. Never auto-advance a state that carries clinical meaning (e.g. never auto-set `PROGRESSED`).

**GEN-FLW-003 [PRODUCT]** — Every state transition records: previous state, new state, transitioning user, role, date/time, reason (from value set + free text), and the source record that triggered it. Immutable audit.

---

## A.2 Cross-cutting platform requirements

These apply to *every* screen, field and document in the product. They are stated once here and assumed thereafter.

### A.2.1 Identity, authorship and time

**GEN-AUD-001 [PRODUCT]** — Every stored value carries: `entered_by` (user ID + display name + role at time of entry), `entered_at` (date + time, to the minute minimum; to the second for medication administration and RT delivery), `source` (measured / reported by patient / imported from device / imported from external system / transcribed / derived), and `entry_device/location` where available.

**GEN-AUD-002 [PRODUCT]** — Every edit to a stored value retains the prior value. Nothing is destructively overwritten. Edits record: prior value, new value, editor, role, timestamp, reason for change (mandatory where the value has been consumed by a signed record).

**GEN-AUD-003 [PRODUCT]** — All timestamps stored in UTC with timezone offset; displayed in facility local time. Clinical time-of-day fields (infusion start/stop, operation start/end, fraction delivery) must be to-the-minute and must never be silently defaulted to "now" without the user seeing and being able to change the value.

**GEN-AUD-004 [PRODUCT]** — Verified/second-check actions (pharmacy double check, nursing double check, blood product check, RT plan approval) record two distinct user identities. The system must prevent the same user satisfying both roles.

### A.2.2 Signature and immutability

**GEN-SIG-001 [PRODUCT]** — Signature model: `DRAFT` → `SIGNED` → (`AMENDED` | `ADDENDUM` | `RETRACTED-IN-ERROR`).

- **DRAFT** — editable by author, visible to author and (configurably `[CCA CONFIG]`) to the care team marked clearly as draft. Never consumed by downstream workflows.
- **SIGNED** — immutable. Content frozen. Timestamped. Attributed. Consumable downstream.
- **AMENDED** — a new version supersedes the previous; **both remain retrievable and viewable**; the amendment records reason, amender, timestamp; consumers of the original are notified.
- **ADDENDUM** — appended content; original body unchanged; separately timestamped and signed.
- **RETRACTED-IN-ERROR** — content suppressed from clinical view but retained in audit; requires reason and (configurable) countersignature `[CCA CONFIG]`.

**GEN-SIG-002 [PRODUCT]** — Signing requires re-authentication or an equivalent explicit affirmation step `[CCA CONFIG — which method]`. A signature must never be applied as a side effect of navigation or saving.

**GEN-SIG-003 [PRODUCT]** — **Frozen-value rule.** Any calculated or referenced value that appears on a signed document is stored *by value* on that document, not by reference. If the source value later changes, the signed document continues to display the value as at signature, together with the source timestamp. Where the current value differs, the system must be able to show both, labelled `AS SIGNED` and `CURRENT`. This rule governs BSA on treatment orders, creatinine clearance on carboplatin dosing, weight on dose calculations, stage on MDT notes, and every analogous case.

**GEN-SIG-004 [PRODUCT]** — Co-signature and countersignature are distinct and both supported: co-signature (two authors of equal standing), countersignature (supervisory review of a trainee/junior entry). Which documents require which is `[CCA CONFIG — CLINICAL SIGN-OFF]`.

### A.2.3 Data provenance and display of superseded information

**GEN-DSP-001 [PRODUCT]** — Wherever a "current" value is displayed, the display must include: value, unit, date/time of the source measurement (not the date of display), and an affordance to view the prior series.

**GEN-DSP-002 [PRODUCT]** — Superseded records (previous treatment order versions, previous RT plan versions, previous stage entries, previous response assessments) must be visually distinguished by persistent treatment — struck-through/greyed with a `SUPERSEDED` chip — and must never be removed from view. The current record must carry a `CURRENT` chip.

**GEN-DSP-003 [PRODUCT]** — Data staleness. Every clinically time-sensitive value (labs used for readiness, weight used for dosing, pregnancy status, cardiac function) displays an age indicator relative to the configured freshness window `[CCA CONFIG]`, with three visual states: within window, approaching expiry, expired.

### A.2.4 Alerts, banners and clinical decision support

**GEN-ALT-001 [PRODUCT]** — Alert severity tiers with distinct visual treatment and distinct interaction requirements:

| Tier | Example | Behaviour |
|---|---|---|
| `CRITICAL — HARD STOP` | Known allergy to ordered drug; wrong-patient mismatch at administration; unsigned order presented for administration | Blocks the action. Cannot be overridden by the acting role. Escalation path defined. |
| `CRITICAL — OVERRIDE WITH REASON` | Readiness criterion failed; cumulative anthracycline dose above configured ceiling; dose variance beyond configured tolerance | Blocks until an authorised role records a structured reason + free text + signature |
| `WARNING` | Lab value outside reference range; stale weight; missing consent | Non-blocking, persistent, acknowledged with one click, acknowledgement audited |
| `INFORMATION` | New result available; MDT scheduled; regimen has a newer version | Non-blocking, dismissible |

**GEN-ALT-002 [PRODUCT]** — Every alert records: alert ID, trigger rule, tier, patient, episode, context (screen/order), presented-to user, presented-at, action taken (acknowledged / overridden / blocked), override reason, override signature.

**GEN-ALT-003 [PRODUCT]** — Alert rules themselves are `[CCA CONFIG — CLINICAL SIGN-OFF]`: which conditions fire, at what tier, for which roles. The rule *engine*, the tiers, the audit and the override workflow are `[PRODUCT]`.

**GEN-ALT-004 [PRODUCT]** — Patient-level banner set, displayed on every screen where the patient is in context, in fixed order: (1) Allergy/adverse reaction, (2) Active isolation/infection precaution, (3) Pregnancy/lactation status where relevant, (4) Active clinical trial enrolment, (5) Do-not-resuscitate / advance directive status `[CCA CONFIG — whether captured]`, (6) Active treatment hold, (7) Critical unacknowledged result, (8) VIP/confidential record flag.

### A.2.5 Permissions

**GEN-PRM-001 [PRODUCT]** — Role-based access control with four orthogonal dimensions per object: **view / create / edit / sign**. Editing another user's signed content is never permitted; amendment by a different authorised user is permitted where configured and is always attributed.

**GEN-PRM-002 [PRODUCT]** — "Read but not write" must be a genuinely supported state. Many roles in this specification need broad clinical visibility with narrow write scope (e.g. Radiation Technologist sees the prescription, cannot alter it).

**GEN-PRM-003 [PRODUCT]** — Break-glass access with mandatory reason, immediate audit entry, and notification to the privacy officer `[CCA CONFIG — notification recipients]`.

**GEN-PRM-004 [PRODUCT]** — Delegation/proxy entry (scribe, junior entering on behalf of consultant) must record both identities: `entered_by` and `on_behalf_of`, and must require the responsible clinician's signature before the record is consumable.

### A.2.6 Search, worklists and queues (generic behaviour)

**GEN-WLQ-001 [PRODUCT]** — Every role worklist supports: column selection, column ordering, saved views (per user), default view (per role, set by administrator `[CCA CONFIG]`), multi-column sort, quick text search (name / UHID / phone / national ID / accession / order number), advanced filter panel, result count, pagination or infinite scroll with stable ordering, refresh indicator with last-refreshed timestamp, and auto-refresh interval `[CCA CONFIG]`.

**GEN-WLQ-002 [PRODUCT]** — Every worklist row supports: click-through to a defined destination screen (defined per role in Part B), a hover/long-press preview card, and a row-level quick-action menu (actions defined per role).

**GEN-WLQ-003 [PRODUCT]** — Status is expressed as a **chip** with three encodings simultaneously: colour, text label, and icon/shape. Never colour alone (accessibility). Colour semantics must be consistent product-wide:

| Colour | Semantic | Never used for |
|---|---|---|
| Red | Blocked / failed / critical / overdue | "Complete" |
| Amber | Needs review / pending / approaching threshold | Errors |
| Green | Ready / passed / complete | Warnings |
| Blue | Informational / scheduled / in progress | Failure |
| Grey | Not applicable / not started / superseded | Active states |
| Purple | On hold / suspended by clinician decision | — |

**GEN-WLQ-004 [PRODUCT]** — Worklists must be derivable from state, not from manual list maintenance. A patient appears in Pharmacy's queue *because* an order is in state `RELEASED-TO-PHARMACY`, not because someone added them.

### A.2.7 Print, export and interoperability

**GEN-EXP-001 [PRODUCT]** — Every signed clinical document is renderable as a print/PDF artifact containing: facility header `[CCA CONFIG]`, patient identifiers, episode identifier, document type, version, author + role + registration number `[CCA CONFIG]`, signature date/time, page numbering `page n of m`, document ID and (configurable) verification QR/barcode.

**GEN-EXP-002 [INTEGRATION]** — Interfaces required at minimum: Laboratory Information System (results in, orders out), Radiology/RIS + PACS (orders out, reports in, image link out), Pathology LIS, Radiotherapy TPS and Record-and-Verify system (prescription/plan/delivery), pharmacy inventory, billing/tariff, patient communication gateway, national/health ID verification `[CCA CONFIG — which]`, cancer registry export `[CCA CONFIG — which registry, which dataset]`.

**GEN-EXP-003 [PRODUCT]** — All coded clinical concepts must be stored with both the local display term and the standard code where a standard applies (morphology/topography coding, diagnosis coding, drug coding, LOINC-style lab coding, adverse-event terminology). Which standards and which versions are `[CCA CONFIG — CLINICAL SIGN-OFF]`; the *dual storage capability* is `[PRODUCT]`.

### A.2.8 Downtime and data integrity

**GEN-DTM-001 [PRODUCT]** — Read-only downtime view: last-known patient summary, active orders, active RT prescription, allergy list, exportable/printable, refreshed at a configured cadence.

**GEN-DTM-002 [PRODUCT]** — Back-entry of downtime data must be flagged as retrospective, with both the *actual clinical time* and the *entry time* recorded and displayed.

**GEN-DTM-003 [PRODUCT]** — No clinical action requiring a signature may be recorded without an identified user, under any circumstance including downtime.

---

## A.3 The five-value dose principle (stated here, specified in Parts I–K)

Because it governs the visual design of three modules, it is stated at platform level:

**GEN-DOS-001 [PRODUCT]** — For every systemic anticancer medication, the product maintains and displays **five distinct values**, which must never be collapsed, inferred from one another, or shown in a way that permits confusion:

| # | Value | Owner | Frozen when |
|---|---|---|---|
| 1 | **STANDARD DOSE** (protocol dose per regimen master) | Regimen Master `[CCA CONFIG]` | At order creation (version-stamped) |
| 2 | **CALCULATED DOSE** (standard dose × dosing parameter) | System `[DERIVED]` | At order creation |
| 3 | **FINAL ORDERED DOSE** (after clinician modification and rounding) | Ordering oncologist | At order signature |
| 4 | **PHARMACY PREPARED DOSE** (actual dose compounded, from actual vials) | Pharmacist | At preparation verification |
| 5 | **ACTUAL ADMINISTERED DOSE** (dose actually given, accounting for interruption/wastage) | Administering nurse | At administration completion |

**GEN-DOS-002 [PRODUCT]** — Each of the five carries its own unit, its own timestamp, its own responsible user, and its own variance-from-previous-value with a structured reason where variance exceeds a configured tolerance `[CCA CONFIG]`.

**GEN-DOS-003 [PRODUCT]** — Cumulative dose tracking uses value #5 (actual administered), not #3. Protocol adherence reporting compares #3 against #1. Preparation accuracy compares #4 against #3.

---

## A.4 Comparable "two-value" pairs requiring the same discipline

**GEN-CMP-001 [PRODUCT]** — The following pairs must be structurally distinct objects with side-by-side comparison views, never merged into a single mutable field:

| A | B | Comparison view required in |
|---|---|---|
| Clinical stage (cTNM) | Pathological stage (pTNM) | Patient header, MDT note, Treatment Summary |
| Planned procedure | Actual procedure performed | Operative note, Treatment Summary, Pathology requisition |
| RT prescribed dose/fractions | RT delivered dose/fractions | OTV, RT Completion Summary, Treatment Summary |
| Planned cycle date | Actual administration date | Cycle timeline, Treatment Summary |
| Baseline lesion measurement | Current lesion measurement | Response Assessment |
| Radiologist-proposed response | Clinician-confirmed response | Response Assessment, MDT |
| Current treatment order | Superseded treatment order | Order screen, Pharmacy screen |
| Current RT plan version | Previous RT plan version | Physics QA, RO approval |
| Current result | Prior result series | Every results view |
| Regimen master version at order | Current regimen master version | Order screen (info-tier alert) |
| Prescribed oral dose | Dispensed quantity / patient-reported taken | Oral therapy review |

---

## A.5 Cross-cutting longitudinal objects

Four objects are longitudinal and must be accessible/updatable from many roles rather than owned by one screen:

**GEN-LNG-001 Allergy & Adverse Reaction List [PRODUCT]** — patient-level; entries carry substance (coded + free text), reaction type (allergy / intolerance / adverse reaction / not-known), manifestation (multiselect `[CCA CONFIG]`), severity (`[CCA CONFIG]` value set), onset date, certainty, informant (patient/family/record), recorded by, recorded date, status (active / inactive / entered-in-error), and — critically for oncology — **prior infusion reaction detail** (agent, cycle, reaction grade, management, rechallenge outcome, desensitisation performed). "No known allergies" must be an affirmative, timestamped, attributed assertion, not an empty list.

**GEN-LNG-002 Medication List [PRODUCT]** — patient-level, with sub-classification: anticancer systemic, anticancer oral, supportive care, comorbidity medication, anticoagulant/antiplatelet (separately flagged for surgical and procedural workflows), herbal/complementary, over-the-counter. Each entry: drug, strength, form, dose, unit, route, frequency, schedule, start date, planned stop date, actual stop date, indication, prescriber, source (prescribed here / external / patient-reported), reconciliation status, last reconciled by/at.

**GEN-LNG-003 Problem/Comorbidity List [PRODUCT]** — coded + free text, onset, status (active/resolved), severity where applicable, and a flag for problems that affect oncology treatment decisions (renal impairment, hepatic impairment, cardiac disease, diabetes, prior malignancy, immunosuppression, hepatitis/HIV status where captured `[CCA CONFIG]`).

**GEN-LNG-004 Toxicity Record [PRODUCT]** — longitudinal per episode, specified in full in Part 11/PART F. Must render as a *timeline*, not a list of unrelated events.

---

# PART B — ROLE-BY-ROLE REQUIREMENTS

Roles covered across this document set:

1. Front Desk / Registration — *this document*
2. Intake Nurse — *this document*
3. Nurse Navigator — *this document*
4. Medical Oncologist — *this document*
5. Radiation Oncologist — *this document*
6. Surgical Oncologist — *this document*
7. Radiologist · 8. Radiology Coordinator · 9. Pathologist · 10. MDT Coordinator · 11. MDT Chair · 12. Oncology Pharmacist · 13. Day Care / Infusion Nurse · 14. Radiation Physicist · 15. Radiation Technologist · 16. Inpatient Oncology Clinician · 17. Inpatient Nurse · 18. Financial Counsellor / Billing · 19. Hospital / Clinical Administrator · 20. Patient-facing · 21. Additional roles (Laboratory Technologist, Palliative Care Clinician, Dietitian, Psycho-oncology, Clinical Trials Coordinator, Medical Records/HIM, Stoma/Wound Nurse, Anaesthetist, Blood Bank) — *following document*

---

## B.1 — FRONT DESK / REGISTRATION

### B.1.A Role purpose

**Why this role uses the system.** The Front Desk creates and maintains the patient identity record, establishes the visit/encounter, associates the visit to the correct department, clinician, cancer episode and payer, and controls the physical flow of patients into clinical areas. Every downstream clinical record inherits the identity and encounter context created here; an identity error at this point propagates into pathology accessions, pharmacy labels, treatment orders and radiation delivery.

**Clinical/operational responsibility owned.**
- Uniqueness and correctness of patient identity (no duplicate UHID; no merged-in-error records).
- Correct visit type, department, clinician and appointment slot.
- Correct payer/sponsorship and eligibility capture at the point of entry.
- Consent to treat / registration consent and data-privacy consent capture `[CCA CONFIG — wording]`.
- Queue management and communication of waiting status.
- Document collection (identity proof, referral letter, external reports, insurance authorisation).

**Entry point into the patient journey.** First contact — walk-in, referral, appointment, transfer-in, or emergency presentation.

**Where responsibility ends.** When the patient is checked in and placed in the Intake or clinician queue, and when the encounter's administrative data is complete. Front Desk does not enter clinical assessment data and must not be able to.

**Receives work from.** External referrers, call centre/appointment booking, Nurse Navigator (scheduling requests), Medical/Radiation/Surgical Oncology (follow-up scheduling), Day Care (next-cycle scheduling), Radiology Coordinator (imaging appointment coordination), Financial Counsellor (authorisation cleared → may proceed).

**Sends work to.** Intake Nurse (check-in complete), clinician queues, Financial Counsellor (payer verification / estimate required), Medical Records (document scanning), Radiology Coordinator, Nurse Navigator (new cancer suspicion requiring navigation).

### B.1.B Role home / worklist / queue

Front Desk requires **four worklist views** as tabs within one screen.

#### View 1 — Today's Appointments

**Columns (default set; all columns configurable per GEN-WLQ-001):**

| Column | Type | Notes |
|---|---|---|
| Appointment time | time | Sortable; default sort ascending |
| Patient name | text | Click-through target |
| UHID / MRN | text | Barcode-scannable search |
| Age | `[DERIVED]` | From DOB, at today's date; format per Part E |
| Sex | coded | |
| Contact number | text | Masked per privacy config `[CCA CONFIG]` |
| Visit type | chip | New / Follow-up / Treatment (Day Care) / Procedure / Investigation-only / Teleconsultation / MDT-related / Review-report-only |
| Department | coded | Medical Oncology / Radiation Oncology / Surgical Oncology / Day Care / Radiology / Pathology collection / Palliative / Other |
| Clinician | text | |
| Appointment status | chip | Booked / Confirmed / Arrived / In Intake / With Clinician / Completed / No-show / Cancelled / Rescheduled |
| Check-in time | time | |
| Waiting time | `[DERIVED]` | Now − check-in time; escalating colour at configured thresholds `[CCA CONFIG]` |
| Current location | coded | Waiting area / Intake room / Consultation room n / Day Care bay n / Radiology / Billing |
| Payer / sponsorship | chip | Self-pay / Insurance / Corporate / Scheme / Trust-funded `[CCA CONFIG]` |
| Financial clearance | chip | Not required / Pending / Cleared / Rejected / Estimate given |
| Pending action | chip stack | Documents pending / Payment pending / Consent pending / Authorisation pending |
| Alerts | icon stack | Allergy, isolation precaution, VIP/confidential, interpreter required, mobility/wheelchair required |
| Referring department / clinician | text | |
| Prior visit date | date | |
| Quick actions | menu | Check in · Reschedule · Cancel · Print appointment slip · Send reminder · Collect payment · Route to Financial Counsellor · Print wristband/label |

**Front Desk must NOT see on this worklist:** diagnosis text, stage, biomarker status, treatment regimen, or any narrative clinical content. Cancer-related information visible to Front Desk is limited to what is operationally necessary: department, clinician, visit type and appointment purpose category (`[CCA CONFIG]` — whether even the purpose category is displayed).

**REG-FD-010 [PRODUCT]** — Front Desk worklist must be constructible without exposing diagnosis. Diagnosis-carrying columns must be role-gated, not merely hidden by default.

**Filters:** date/date-range, department, clinician, visit type, appointment status, payer, financial clearance status, location, "arrived but not yet seen > n minutes", "no-show", "unscheduled walk-in".

**Search:** name (partial, phonetic-tolerant), UHID, phone, national ID, appointment number, date of birth. Search must span registered patients *and* today's appointments and clearly distinguish which it matched.

**Sorting:** appointment time (default), waiting time descending, clinician, status.

**Drill-down on click:** opens **Encounter Detail / Check-in screen** (not the clinical chart). From there, a role-permitted link to the patient's *administrative* profile.

#### View 2 — Waiting / Live Queue

Real-time board showing, per department and clinician: patients arrived, order in queue, waiting time, current location, and clinicians' current status (available / in consultation / on break / in procedure). Supports drag-to-reorder with reason capture `[CCA CONFIG — whether permitted]`, call-next action, and display-board output for the public waiting area (**patient-identifiable content on public boards must be configurable to token/initials only** `[CCA CONFIG]`) — **REG-FD-020 [PRODUCT]**.

#### View 3 — Registration Pending / Incomplete

Patients registered with incomplete mandatory data: missing identity proof, missing address, missing next-of-kin, missing consent, unverified payer, unresolved possible-duplicate flag.

#### View 4 — Scheduling / Booking

Multi-resource calendar: clinician slots, Day Care chairs/beds, procedure rooms, simulation slot, linac slot (view-only from RT scheduling), radiology slots (view-only from RIS `[INTEGRATION]`). Shows slot type, duration, capacity, over-booking rules `[CCA CONFIG]`, blocked/holiday periods.

**REG-FD-030 [PRODUCT]** — Day Care booking must not be a free calendar entry. It must be able to consume the expected next-cycle date derived from the signed treatment order (regimen cycle length + last administration date) and must display expected chair-time duration derived from the regimen's total infusion duration.

### B.1.C Patient header / snapshot for Front Desk

Deliberately minimal. Front Desk sees an **administrative header**, not the clinical patient header.

**Displayed:**
- Photograph (if captured) `[CCA CONFIG — whether captured]`
- Patient name (and preferred name)
- UHID/MRN — with barcode
- Age `[DERIVED]` and date of birth
- Sex; gender identity where captured `[CCA CONFIG]`
- Contact number(s), email
- Address (city/area level in header; full on detail)
- Next of kin / emergency contact name + relationship + number
- Preferred language / interpreter required
- Payer, policy/scheme number, validity, authorisation status
- Registration status and registration date
- Active alerts limited to operational ones: interpreter, mobility assistance, isolation precaution, confidential record
- Attending department(s) and primary treating clinician (name only)
- Outstanding balance / financial hold flag `[CCA CONFIG]`
- Open encounter indicator (patient already checked in elsewhere today)

**Explicitly not displayed to Front Desk:** diagnosis, primary site, histology, stage, biomarkers, performance status, treatment regimen, cycle/day, lab values, toxicity, prognosis, notes.

**REG-FD-040 [PRODUCT]** — Allergy information: Front Desk sees only a non-specific "Allergy recorded — see clinical staff" indicator unless CCA configures substance-level display for this role `[CCA CONFIG]`. The indicator must exist so that wristband/labels can be printed correctly.

### B.1.D Front Desk core functions (screen list, detailed in Part C)

| Function | Screen | Key outputs |
|---|---|---|
| New patient registration | Registration form | UHID issued, duplicate check performed, wristband/label printed |
| Duplicate detection & merge request | Possible-duplicate resolution | Merge request to Medical Records (Front Desk must **not** be able to execute a merge — **REG-FD-050 [PRODUCT]**) |
| Demographic update | Patient profile edit | Versioned, audited |
| Appointment booking / reschedule / cancel | Scheduling | Appointment record, patient notification |
| Check-in | Check-in | Encounter opened, patient enters Intake queue |
| Payer & eligibility capture | Payer panel | Financial clearance status; handoff to Financial Counsellor |
| Registration/privacy consent capture | Consent capture | Signed consent artifact `[CCA CONFIG — wording]` |
| Document upload/scan | Document capture | Typed, indexed to patient + episode |
| Referral capture | Referral panel | Referring facility, clinician, date, reason, documents; feeds Navigator queue |
| Queue management | Live queue | Call-next, reorder, location update |
| Check-out & next appointment | Check-out | Next appointment, instructions slip, follow-up loop closure |
| Death/transfer administrative recording | Administrative status | Requires clinical confirmation before episode state changes — **REG-FD-060 [PRODUCT]** |

---

## B.2 — INTAKE NURSE

### B.2.A Role purpose

**Why this role uses the system.** The Intake Nurse converts a checked-in patient into a clinically prepared patient. This role generates the objective measurement baseline that the *entire dosing chain depends on* — height, weight, and therefore BSA — and the safety baseline: allergies, current medications, performance status screen, symptom screen, infection screen and pregnancy screen where applicable.

**Clinical/operational responsibility owned.**
- Accurate anthropometrics and vital signs with correct method, unit, time and attribution.
- Allergy and adverse-reaction elicitation and reconciliation.
- Medication reconciliation (initial capture; clinician confirms).
- Performance status screening (recorded as *nurse-assessed*; the clinician's own assessment is a separate field — **INT-NUR-010 [PRODUCT]**).
- Symptom and toxicity screening for patients on active treatment.
- Pain screen, fall-risk screen, nutrition screen, distress screen `[CCA CONFIG — which instruments]`.
- Infection/isolation screen.
- Pregnancy/lactation status where applicable.
- Escalation of red-flag findings before the consultation.

**Entry point.** After Front Desk check-in, before clinician consultation; and on treatment days, before Day Care assessment where the model separates the two.

**Where responsibility ends.** When the intake record is signed and the patient is routed to the clinician queue with any escalations raised.

**Receives work from.** Front Desk (check-in), Day Care (pre-treatment measurement request), Nurse Navigator.

**Sends work to.** Medical/Radiation/Surgical Oncologist (patient ready), Nurse Navigator (unmet needs, social/financial concern, symptom escalation), Day Care (weight/vitals for the day's dosing), Financial Counsellor (where a need is identified), Inpatient/Emergency (where red-flag escalation triggers).

### B.2.B Role home / worklist / queue

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Queue position / arrival order | numeric | |
| Patient name | text | |
| UHID | text | |
| Age / Sex | `[DERIVED]` / coded | |
| Visit type | chip | New / Follow-up / Treatment day / Pre-procedure / Post-treatment review |
| Department & clinician | text | |
| Appointment time / check-in time / waiting time | time / time / `[DERIVED]` | |
| Intake status | chip | Not started / In progress / Complete / Escalated / Deferred |
| Required intake set | chip stack | `[DERIVED]` from visit type + treatment status. E.g. treatment-day visits require weight + vitals + toxicity screen; new consultations require full intake |
| Last weight (value + date) | numeric + date | With staleness indicator |
| Last height (value + date) | numeric + date | |
| Treatment context | chip | On systemic therapy (regimen short name, cycle n day n) / On RT (fraction n of m) / Post-op day n / Surveillance / Not on treatment |
| Alerts | icon stack | Allergy, isolation, fall risk, interpreter, pregnancy-relevant, prior infusion reaction |
| Escalation flag | chip | Raised / Acknowledged / Resolved |
| Quick actions | menu | Start intake · Record vitals only · Record weight only · Escalate · Defer with reason · Print label |

**Filters:** department, clinician, visit type, intake status, treatment context, escalation raised, "weight overdue for dosing", "vitals abnormal".

**Drill-down:** opens the **Intake Assessment screen** with the correct required-field set pre-selected by visit type.

**INT-NUR-020 [PRODUCT]** — The required intake field set is `[DERIVED]` from visit type, treatment modality, treatment day status and configured protocol prerequisites `[CCA CONFIG]`. The nurse must see *why* a field is required ("required: treatment day — dose recalculation") on hover.

### B.2.C Patient header / snapshot for Intake Nurse

**Displayed:**
- Identifiers: name, UHID, age `[DERIVED]`, sex, photograph
- Alert banners (full set per GEN-ALT-004) — Intake Nurse sees **substance-level allergy detail**
- Cancer episode selector; primary site and laterality; diagnosis short form
- Treatment status: modality, regimen short name, cycle/day, or RT fraction n of m, or post-op day n
- Last recorded weight, height, BSA — each with date/time and staleness indicator
- Last vitals set with date/time
- Latest key labs relevant to intake screening (Hb, WBC/ANC, platelets, creatinine) with date and out-of-range flags — **display only, no interpretation** `[CCA CONFIG — which panel]`
- Active allergies and prior infusion reactions
- Active toxicities with grade
- Current medications (count + expandable)
- Isolation/infection precautions
- Mobility/fall-risk status
- Next scheduled clinical event

**Not displayed:** full staging detail, biomarker panel, MDT deliberation content, prognosis narrative — available on drill-down where role permits, not in the header.

### B.2.D Intake Nurse — required data capture (field-level; full dictionary in Part D)

This section is included here in full field-level form because the brief specifies this exact example. All other role field sets follow the same template in Part D.

#### Anthropometrics

**HEIGHT — `INT-NUR-100`**

| Attribute | Specification |
|---|---|
| Field name | Height |
| Clinical meaning | Standing (or alternative) body height, used for BSA and BMI derivation, and therefore for systemic anticancer dosing |
| Input type | Measured (numeric) — with method qualifier |
| Method qualifier | Dropdown: Measured — standing / Measured — supine / Measured — segmental (knee height, arm span) / Patient-reported / Carried forward from previous record. `[CCA CONFIG — whether patient-reported permitted for dosing]` |
| Required / conditional / optional | **Required** for: new consultation; any visit at which a systemic therapy order will be created or a dose recalculated; RT simulation. Otherwise optional if a value exists within the configured validity window |
| Unit | Canonical: **cm** |
| Allowed source units | cm, m, inches, feet+inches — **normalised to cm on save; source unit and source value retained and displayable** |
| Default value | None. The system must not pre-fill a height. The previous value is *displayed adjacent* with its date, and an explicit "carry forward" action copies it, recording method = carried forward and retaining the original measurement date |
| Value set | n/a (numeric) |
| Free text | Not allowed in the value field. A separate comment field permits free text |
| Validation | Numeric, one decimal place. Plausibility bounds `[CCA CONFIG]` — e.g. adult/paediatric bounds by age band. Values outside bounds require confirmation with reason (warning tier). Values outside absolute bounds are rejected (hard stop) |
| Delta check | If new height differs from the most recent height by more than a configured percentage/absolute amount `[CCA CONFIG]`, warning tier alert requiring confirmation. Critical for adults where a large change indicates measurement error |
| Dependency | Feeds BSA and BMI. Changing height triggers recalculation of *unsigned* dependent values only (see GEN-SIG-003) |
| Source | Device-integrated stadiometer where available `[INTEGRATION]`, else manual |
| Entered by | Intake nurse (recorded automatically) |
| Verified by | Not routinely; a verification field exists for paediatric/high-risk dosing `[CCA CONFIG — when verification required]` |
| Date/time | Measurement date/time — **defaulted to now but explicitly editable**, with edit reason if backdated |
| Editable | Yes before signing of the intake record. After signing, corrigible only by amendment with reason; the original remains visible |
| After signature | Value frozen on any signed document that consumed it |
| Displayed later | Intake record, patient header, dosing panel of every treatment order, RT simulation record, growth chart for paediatric patients `[CCA CONFIG]`, trend view |
| Consumed by | BSA, BMI, systemic dose calculation, RT positioning/immobilisation notes, nutrition assessment |
| Display format | `172.0 cm` — value, one decimal, unit, and secondary line `measured 05-Sep-2026 09:14 · N. Rao (Intake Nurse)` |
| Previous value visible | **Yes** — the immediately previous value with its date is shown adjacent to the input at all times, plus a trend link |
| Auto-load most recent | The most recent value is *displayed* but not *auto-entered*. Auto-entry into a new measurement event is prohibited — **INT-NUR-101 [PRODUCT]** |

**WEIGHT — `INT-NUR-110`**

| Attribute | Specification |
|---|---|
| Field name | Weight |
| Clinical meaning | Body weight, used for BSA, BMI, mg/kg dosing, carboplatin/renal-function estimation, nutrition monitoring and fluid balance |
| Input type | Measured (numeric) with method qualifier |
| Method qualifier | Dropdown: Measured — standing scale / Measured — chair scale / Measured — bed scale / Measured — hoist / Patient-reported / Estimated / Carried forward. `[CCA CONFIG — which methods acceptable for dose calculation]` |
| Clothing/condition qualifier | Dropdown: Light clothing / Full clothing / With prosthesis / With cast / Post-dialysis / Pre-dialysis / Post-paracentesis `[CCA CONFIG]` — relevant because oncology dosing weight can be materially affected |
| Required | **Required** on every treatment day; every new consultation; every RT weekly OTV `[CCA CONFIG]`; every inpatient day where configured; before any dose recalculation |
| Unit | Canonical: **kg** |
| Allowed source units | kg, g (paediatric), lb — normalised to kg; source retained |
| Default value | None. Previous value displayed adjacent with date and delta |
| Validation | Numeric, one decimal (adult) / two decimals (paediatric/neonatal). Plausibility bounds by age band `[CCA CONFIG]` |
| Delta check | Change from previous weight exceeding configured absolute or percentage threshold `[CCA CONFIG]` raises a warning-tier alert. **On a treatment day, a weight change beyond the configured threshold must additionally flag the active treatment order for dose review — INT-NUR-111 [PRODUCT]** |
| Dependency | Feeds BSA, BMI, dosing weight selection, weight-change trend, nutrition screen |
| Dosing weight | A **separate derived/selected field** — see `INT-NUR-115` below. Actual weight and dosing weight are never the same field |
| Source | Device-integrated scale where available `[INTEGRATION]`, else manual |
| Entered by / Date-time / Editable / After signature | As for Height |
| Displayed later | Intake record, header, dosing panel, weight trend chart, nutrition assessment, RT OTV, inpatient flowsheet, Treatment Summary |
| Display format | `68.4 kg` with secondary line `measured 05-Sep-2026 09:15 · standing scale · light clothing · N. Rao` and delta chip `−2.1 kg vs 22-Aug-2026 (−3.0%)` |

**DOSING WEIGHT — `INT-NUR-115` [PRODUCT] + [CCA CONFIG — CLINICAL SIGN-OFF]**

| Attribute | Specification |
|---|---|
| Clinical meaning | The weight value actually used for dose calculation, which may differ from measured weight (e.g. where an institutional policy applies to obesity, amputation, massive ascites or oedema) |
| Input type | Selected + optionally clinician-entered |
| Options | Actual measured weight (default) / Adjusted weight / Ideal weight / Clinician-specified weight. Formulae for adjusted and ideal weight are `[CCA CONFIG — CLINICAL SIGN-OFF]`; the *capability to hold and apply named weight formulae* is `[PRODUCT]` |
| Required | Conditional — required whenever a weight-based or BSA-based dose is calculated |
| Who sets it | Ordering oncologist, not the intake nurse. The intake nurse supplies the measurement; the selection of dosing weight is a clinician decision — **INT-NUR-116 [PRODUCT]** |
| Displayed | On the order dosing panel, on the pharmacy verification screen, on the printed order, and in the Treatment Summary |
| Frozen | Yes — frozen on the signed order together with the underlying measurement and its date |

**BMI — `INT-NUR-120` [DERIVED]**

| Attribute | Specification |
|---|---|
| Input type | System calculated. Read-only. Never editable |
| Inputs | Weight (kg), Height (cm → m) |
| Formula | `BMI = weight_kg / (height_m)²` |
| Unit | kg/m² |
| Rounding / display precision | One decimal place; round-half-up |
| Input values visible | **Yes** — the formula and the two source values with their measurement dates must be viewable on hover/expand |
| Recalculation | Recalculates automatically when either source measurement changes, **for unsigned contexts only** |
| Timestamps retained | The BMI carries the timestamps of both source measurements, not the calculation time; calculation time also stored |
| Who can see | All clinical roles |
| Frozen | Frozen into any signed note that displays it |
| Consumed by | Nutrition screen, comorbidity assessment, dose-policy rules `[CCA CONFIG]`, reporting |
| Display format | `23.1 kg/m²` with expandable `= 68.4 kg ÷ (1.72 m)² · wt 05-Sep-2026, ht 12-Mar-2026` |

**BSA — `INT-NUR-130` [DERIVED]**

| Attribute | Specification |
|---|---|
| Input type | System calculated. Read-only result |
| Formula | **The formula in use must be explicitly named and displayed on screen and on every printed order.** The product must support multiple named BSA formulae and must allow CCA to designate a default and to permit/prohibit per-order override — `[CCA CONFIG — CLINICAL SIGN-OFF: which formula is default; whether override permitted; whether different formulae apply to paediatric vs adult]` |
| Formula library | `[PRODUCT]` — the system holds a library of named, versioned BSA formulae. CCA activates the ones it uses. Formula identity is stored on every calculation result |
| Inputs | Height (cm) and dosing weight (kg) — **the dosing weight, not necessarily the measured weight** |
| Unit | m² |
| Rounding / display precision | Two decimal places `[CCA CONFIG — whether 2 dp or other]`; rounding rule explicit and stored |
| BSA capping | The product must support an optional BSA cap (a maximum BSA used for dosing). Whether a cap applies, and its value, is `[CCA CONFIG — CLINICAL SIGN-OFF]`. Where a cap is applied, **both the uncapped and capped BSA must be displayed** with the cap policy named — `INT-NUR-131 [PRODUCT]` |
| Source timestamps | The BSA result carries the measurement date/time of both the height and the weight used |
| Recalculation | Automatic on source change in unsigned contexts. **Never silently recalculated on a signed order** |
| Editable | Not editable. A clinician who disagrees changes the *inputs* (dosing weight) or applies a documented dose override — never the BSA itself |
| Who can see | Ordering oncologist, pharmacist, day care nurse, inpatient clinician, physicist (where relevant), administrator reporting |
| Frozen | **The BSA used on a signed order must remain visible on that order forever, even after a newer weight is recorded.** Where the current BSA differs from the order BSA by more than a configured tolerance `[CCA CONFIG]`, the order screen must display an information/warning-tier indicator showing both values — `INT-NUR-132 [PRODUCT]` |
| Consumed by | Systemic therapy dose calculation, pharmacy verification, day care administration record, cumulative dose calculation, Treatment Summary |
| Display format | `1.81 m²` with expandable panel: `Mosteller · ht 172.0 cm (12-Mar-2026) · dosing wt 68.4 kg [actual] (05-Sep-2026) · calculated 05-Sep-2026 09:16` — formula name shown is illustrative of *display structure*; the active formula is `[CCA CONFIG]` |

#### Vital signs — decomposed (`INT-NUR-200` series)

Every vital is a distinct field with its own unit, method, time and validation. A "vitals set" is a container with one measurement date/time and one recorder, containing individually-attributed values.

| ID | Field | Type | Unit (canonical) | Accepted source units | Method qualifier | Validation / notes |
|---|---|---|---|---|---|---|
| `INT-NUR-201` | BP systolic | numeric | mmHg | mmHg, kPa | Manual / Automated / Arterial line | Integer; plausibility bounds `[CCA CONFIG]`; critical-value thresholds `[CCA CONFIG]` |
| `INT-NUR-202` | BP diastolic | numeric | mmHg | mmHg, kPa | as above | Must be < systolic (validation) |
| `INT-NUR-203` | BP site & position | dropdown | — | — | — | Left arm / Right arm / Left leg / Right leg / Other; Sitting / Standing / Supine. **Required where lymphoedema or ipsilateral axillary surgery is recorded — the system must warn if BP is recorded on a contraindicated limb** `[CCA CONFIG — rule]` — `INT-NUR-204 [PRODUCT]` |
| `INT-NUR-205` | Cuff size | dropdown | — | — | — | `[CCA CONFIG]` |
| `INT-NUR-206` | Mean arterial pressure | `[DERIVED]` | mmHg | — | — | Formula stated in Part E; displayed only where configured |
| `INT-NUR-210` | Pulse rate | numeric | beats/min | — | Manual palpation / Monitor / Pulse oximeter | Integer |
| `INT-NUR-211` | Pulse rhythm | dropdown | — | — | — | Regular / Irregular / Irregularly irregular |
| `INT-NUR-220` | Temperature | numeric | °C | °C, °F — normalised, source retained | Oral / Axillary / Tympanic / Temporal / Rectal / Core | One decimal. **Site must be captured — a febrile-neutropenia rule cannot be applied without it.** Threshold values `[CCA CONFIG — CLINICAL SIGN-OFF]` |
| `INT-NUR-230` | Respiratory rate | numeric | breaths/min | — | Counted / Monitor | Integer |
| `INT-NUR-240` | SpO₂ | numeric | % | — | Pulse oximeter | Integer; site optional |
| `INT-NUR-241` | Oxygen support | conditional group | — | — | — | On room air (default) / On oxygen. If on oxygen: delivery device (dropdown `[CCA CONFIG]`), flow rate (L/min), FiO₂ (%) |
| `INT-NUR-250` | Pain score | numeric/scale | score | — | Instrument named | Scale instrument is `[CCA CONFIG]` (numeric rating, faces, behavioural). Must capture: score, instrument used, site, character, radiation, aggravating/relieving factors, current analgesia, time of last analgesic dose |
| `INT-NUR-260` | Consciousness / alertness | dropdown | — | — | — | `[CCA CONFIG — which scale]` |
| `INT-NUR-270` | Capillary blood glucose | numeric | mg/dL or mmol/L `[CCA CONFIG — canonical]` | both, normalised | Point-of-care / Lab | Conditional on diabetes flag or steroid-containing regimen `[CCA CONFIG]` |
| `INT-NUR-280` | Measurement date/time | datetime | — | — | — | Defaults to now, explicitly editable, backdating requires reason |
| `INT-NUR-281` | Measured by | auto | — | — | — | Logged-in user + role |
| `INT-NUR-282` | Source | dropdown | — | — | — | Measured here / Device-integrated / Reported by patient / Transcribed from external record |
| `INT-NUR-283` | Vitals set comment | free text | — | — | — | Optional |

**INT-NUR-290 [PRODUCT]** — Every vitals field must display the previous value and a trend sparkline inline, and a full trend table/graph on expand, filterable by date range and overlaid with treatment events (cycle days, RT fractions, surgery date).

**INT-NUR-291 [PRODUCT]** — Out-of-range values are flagged against two separate reference sets: the general reference range and the **patient's own configured treatment-specific parameters** where a protocol defines them `[CCA CONFIG]`.

**INT-NUR-292 [PRODUCT]** — Critical vital values fire an alert to a configured recipient role and create an entry in an escalation log requiring acknowledgement. Thresholds and recipients `[CCA CONFIG — CLINICAL SIGN-OFF]`.

#### Other intake screens (field detail in Part D)

| ID | Screen/section | Contents summary |
|---|---|---|
| `INT-NUR-300` | Allergy & adverse reaction capture/reconciliation | Per GEN-LNG-001; affirmative NKDA assertion required |
| `INT-NUR-310` | Medication reconciliation (nurse-captured) | Per GEN-LNG-002; each entry marked as patient-reported until clinician-confirmed |
| `INT-NUR-320` | Performance status screen (nurse-assessed) | Instrument `[CCA CONFIG]` (ECOG/KPS/Lansky-Play). Stored as: instrument, score, assessed by, role, date/time. **Nurse-assessed and clinician-assessed scores are separate fields and both are retained** |
| `INT-NUR-330` | Symptom / toxicity screen | Structured symptom checklist `[CCA CONFIG]`, each with present/absent, severity, onset, change since last visit; feeds the longitudinal Toxicity Record |
| `INT-NUR-340` | Infection / isolation screen | Fever in last n hours, recent antibiotics, contacts, travel `[CCA CONFIG]`, current isolation requirement |
| `INT-NUR-350` | Pregnancy / lactation / contraception screen | Conditional on sex and age band `[CCA CONFIG]`; capture: applicable/not applicable with reason (post-menopausal, surgically sterile, etc.), last menstrual period, pregnancy test required?, test result, test date, contraception counselling given, lactation status. **Must be blockable as a readiness criterion** |
| `INT-NUR-360` | Fall-risk assessment | Instrument `[CCA CONFIG]`; individual item scores + `[DERIVED]` total + `[DERIVED]` risk band; interventions triggered |
| `INT-NUR-370` | Nutrition screen | Instrument `[CCA CONFIG]`; weight loss over defined interval `[DERIVED]`, appetite, intake, dysphagia, supplements; triggers dietitian referral |
| `INT-NUR-380` | Psychosocial / distress screen | Instrument `[CCA CONFIG]`; triggers psycho-oncology referral |
| `INT-NUR-390` | Vascular access assessment | Existing device type, insertion date, site, dressing status, patency, complication; feeds Day Care |
| `INT-NUR-395` | Intake escalation | Structured escalation: finding, severity, escalated to (role/person), method, time, response, outcome |

**Required document: INTAKE / NURSING ASSESSMENT NOTE** — full section specification in Part F.

---

## B.3 — NURSE NAVIGATOR

### B.3.A Role purpose

**Why this role uses the system.** The Nurse Navigator owns *continuity* — the thing that is otherwise owned by nobody. Oncology care fails between departments, not within them. The Navigator tracks each patient against expected milestones, chases outstanding investigations, ensures MDT submission happens, ensures the patient understands and can access the next step, resolves barriers (financial, transport, comprehension, caregiver), and closes loops on referrals and results.

**Clinical/operational responsibility owned.**
- Milestone tracking against configured target intervals `[CCA CONFIG]` (e.g. referral→first consult, diagnosis→MDT, MDT→treatment start).
- Outstanding-investigation follow-up and result loop closure.
- Barrier identification, documentation and resolution.
- Patient education delivery and comprehension confirmation.
- Coordination of multimodality sequencing appointments.
- Contact log and non-visit encounters (telephone, message).
- Escalation of patients falling behind pathway milestones.

**Entry point.** At the point of cancer suspicion or confirmed referral — typically immediately after registration or first consultation.

**Where responsibility ends.** Continues through the entire episode into survivorship; formally hands over at transfer of care or discharge from navigation `[CCA CONFIG — criteria]`.

**Receives work from.** Front Desk (new referral), all clinicians (navigation referral), Intake Nurse (identified need), MDT Coordinator (action items), Financial Counsellor.

**Sends work to.** All clinical and operational roles; is the principal generator of "chase" tasks.

### B.3.B Role home / worklist / queue

The Navigator worklist is **milestone-driven**, not appointment-driven. Four views:

#### View 1 — My Panel (all navigated patients)

| Column | Type |
|---|---|
| Patient name, UHID, age, sex | mixed |
| Primary site / diagnosis (short) | coded |
| Episode state | chip (per A.1.2) |
| Current pathway milestone | `[DERIVED]` chip |
| Days in current milestone | `[DERIVED]` numeric with threshold colouring `[CCA CONFIG]` |
| Next milestone due | date `[DERIVED]` |
| Pathway status | `[DERIVED]` chip: On track / At risk / Breached / Paused (clinical reason) / Paused (patient reason) |
| Outstanding investigations | count + expandable list with ordered date, expected date, status |
| MDT status | chip: Not required / To be submitted / Submitted / Scheduled / Discussed / Recommendation pending action / Actioned |
| Treatment readiness | chip (see Part I) |
| Consent status | chip: Not required / Pending / Obtained / Declined / Withdrawn |
| Financial clearance | chip |
| Open barriers | count + type icons |
| Last contact date / method / by | mixed |
| Next scheduled appointment (date, department) | mixed |
| Alerts | icon stack |
| Assigned navigator | text |
| Quick actions | Log contact · Add barrier · Chase investigation · Submit to MDT · Book appointment · Refer (dietitian/psych/palliative/financial) · Escalate · Send patient information |

#### View 2 — Breaches & At-Risk
Filtered to pathway breaches and at-risk patients, sorted by days overdue, with the specific blocking item named.

#### View 3 — Outstanding Results / Loop Closure
Every ordered investigation not yet resulted, and every resulted investigation not yet acknowledged by an ordering clinician. **NAV-010 [PRODUCT]** — result acknowledgement is a tracked, audited state with an owner; unacknowledged critical results escalate on a configured schedule `[CCA CONFIG]`.

#### View 4 — Task / Action Inbox
MDT action items assigned to navigation, clinician-delegated tasks, patient callbacks due, education due, follow-up calls after treatment day `[CCA CONFIG].

### B.3.C Patient header for Navigator

Broad clinical visibility, read-mostly. Displays: identifiers; episode; primary site, laterality, histology, stage (clinical and pathological, distinguished); treatment intent; current treatment modality and phase; regimen name, cycle/day or RT fraction n/m or post-op day n; performance status (latest, with assessor and date); allergies; active toxicities; treatment holds; MDT status and last recommendation summary; consent status; outstanding investigations; open barriers; next appointments across all departments; care team roster (named clinicians per specialty); preferred language and communication preferences; caregiver/contact details and consent to share information `[CCA CONFIG]`.

### B.3.D Navigator core functions

| ID | Function | Notes |
|---|---|---|
| `NAV-100` | Pathway/milestone definition and tracking | Pathway templates per disease site are `[CCA CONFIG]`; the *engine* — milestones, target intervals, dependencies, automatic status derivation, breach calculation, pause-with-reason — is `[PRODUCT]` |
| `NAV-110` | Barrier register | Barrier type (dropdown `[CCA CONFIG]`: financial, transport, comprehension/language, caregiver, employment, distance, comorbidity, psychological, treatment fear, other), description, identified date, identified by, severity, actions taken, referrals made, status, resolution date, outcome |
| `NAV-120` | Contact log | Non-visit encounter: date/time, direction (inbound/outbound), method (phone/SMS/email/portal/in-person/home visit), contacted party (patient/caregiver/external provider), purpose, content summary, outcome, follow-up required, next contact date. Signed and permanent |
| `NAV-130` | Education delivery record | Topic (from Education Master `[CCA CONFIG]`), material version issued, format, language, delivered to (patient/caregiver), delivered by, date, comprehension confirmed (yes/partial/no — method: teach-back/verbal/other), reinforcement required, notes |
| `NAV-140` | Referral generation & tracking | Internal and external; captures referral reason, urgency, target specialty/provider, documents attached, sent date, acknowledged date, appointment date, outcome received date, loop closed by/at |
| `NAV-150` | Multimodality sequencing view | Timeline showing planned and actual dates of surgery, systemic cycles, RT phases, with dependency conflicts flagged (e.g. RT scheduled before planned post-op interval `[CCA CONFIG]`) |
| `NAV-160` | Escalation | Structured escalation to named clinician with reason, urgency, response required by, response received, outcome |

**Required document: NAVIGATION / CARE COORDINATION NOTE** — sections in Part F.

---

## B.4 — MEDICAL ONCOLOGIST

This role is documented in exceptional detail per the brief. Its screens are enumerated here; field-level specification of each continues in Part C/D, and the ordering chain is fully specified in Part I.

### B.4.A Role purpose

**Why this role uses the system.** The Medical Oncologist establishes and maintains the oncological diagnosis, stage, biomarker profile and treatment intent; determines the line and sequence of systemic therapy; issues and signs treatment orders that authorise the preparation and administration of hazardous drugs; grants or withholds treatment-day clearance; modifies, delays, holds and discontinues therapy; assesses toxicity and response; and authors the clinical record on which pharmacy, nursing, radiation, surgery and MDT all depend.

**Clinical/operational responsibility owned.**
- Diagnosis and cancer episode definition.
- Clinical staging (and interpretation of pathological staging).
- Biomarker interpretation and treatment implication.
- Treatment intent (curative / adjuvant / neoadjuvant / palliative / maintenance / consolidation / definitive-with-RT `[CCA CONFIG]`).
- Line of therapy determination.
- Regimen selection, dose determination, dose modification.
- Signing of systemic therapy orders — the legal authorisation for cytotoxic/biologic administration.
- Treatment-day clearance decision.
- Toxicity attribution and management.
- Response assessment confirmation (the radiologist proposes; the oncologist confirms).
- End-of-treatment determination and Treatment Summary approval.
- Surveillance plan.

**Entry point.** First consultation, or MDT-directed referral, or transfer of care.

**Where responsibility ends.** At transfer of care, treatment discontinuation with handover, discharge to survivorship follow-up, or death.

**Receives work from.** Front Desk/Intake (patient ready), Nurse Navigator, Radiologist (results), Pathologist (results), Laboratory (results), MDT (recommendation), Pharmacy (order queries), Day Care (administration events, reactions, clearance requests), Surgical Oncology (adjuvant handoff), Radiation Oncology (concurrent therapy coordination), Inpatient team.

**Sends work to.** Radiology (imaging orders), Laboratory (lab orders), Pathology (biomarker requests), MDT Coordinator (case submission), Pharmacy (signed treatment orders), Day Care (administration authorisation), Radiation Oncology (referral), Surgical Oncology (referral), Nurse Navigator, Financial Counsellor, Inpatient (admission request), Palliative Care.

### B.4.B Role home / worklist / queue

Medical Oncology requires **six views**.

#### View 1 — Today's Clinic

| Column | Type | Notes |
|---|---|---|
| Appointment time | time | |
| Patient name / UHID / age / sex | mixed | |
| Visit type | chip | New consultation / Follow-up / Treatment-day review / Post-cycle review / Toxicity review / Response review / Report review / Teleconsultation |
| Diagnosis (short) + primary site + laterality | coded | |
| Stage | chip | Displays `c` or `p` prefix explicitly; both shown where both exist |
| Treatment intent | chip | |
| Line of therapy | chip | e.g. `1L`, `2L`, `Adjuvant`, `Maintenance` |
| Current regimen + cycle/day | text | e.g. `Regimen X · C3 D1` |
| Treatment phase | chip | Diagnostic workup / Staging / Awaiting MDT / Planning / On systemic / On RT / Post-op / On oral therapy / Response assessment / Surveillance / Best supportive care |
| Intake status | chip | Complete / Pending / Escalated |
| Readiness status | `[DERIVED]` chip | Ready / Not ready — n criteria failed / Pending results / Needs clinician review / Not applicable |
| Key results status | chip stack | Labs available (date) · Imaging available (date) · Pathology available (date) · Results pending |
| New/unacknowledged results | count badge | |
| Performance status | value + date + assessor | |
| Active toxicity | highest grade chip + count | |
| Alerts | icon stack | |
| Consent status | chip | |
| MDT status | chip | |
| Pending actions for me | chip stack | Order to sign · Result to acknowledge · Pharmacy query · Day Care clearance request · MDT action item · Note unsigned |
| Waiting time / location | `[DERIVED]` / coded | |
| Quick actions | menu | Open consultation · Open treatment order · Grant clearance · Review results · Submit to MDT · Refer · Write note |

**MO-CON-010 [PRODUCT]** — The readiness chip on the clinic worklist must be computed and displayed *before* the clinician opens the patient, so the clinician can see at a glance which patients cannot proceed.

#### View 2 — Treatment Day Clearance Queue
Patients scheduled for systemic therapy today (or within a configured horizon `[CCA CONFIG]`) requiring the oncologist's clearance. Columns emphasise: scheduled time, regimen, cycle/day, readiness criteria pass/fail breakdown (expandable inline without opening the chart), latest relevant labs with dates and staleness, weight change since last cycle, active toxicity grade, last cycle's issues, dose modification proposed, and one-click access to the Clearance action.

**MO-RDY-010 [PRODUCT]** — Clearance must be grantable from this queue *only after* the full readiness breakdown has been displayed. Bulk clearance of multiple patients without individual review is prohibited.

#### View 3 — Results Inbox
All results for the oncologist's patients: labs, imaging, pathology, external documents. Columns: patient, result type, test name, resulted date/time, abnormal flag, critical flag, ordered by, ordered for (indication), acknowledgement status, action taken. Supports acknowledge, acknowledge-with-comment, order follow-up action, notify navigator, and **flag for MDT**. Critical results are pinned and escalate if unacknowledged within a configured interval `[CCA CONFIG]`.

#### View 4 — Orders & Signatures Pending
Draft treatment orders, unsigned notes, orders returned by pharmacy with queries, orders requiring co-signature, expiring orders.

#### View 5 — My Patients (panel view)
Full panel with episode state, next event, last seen, treatment progress (cycles completed / planned), and surveillance due.

#### View 6 — Inpatient List
Where the oncologist has admitted patients — see B.16.

### B.4.C Patient header / snapshot for Medical Oncologist

This is the richest header in the product. It must be organised into a compact persistent strip plus an expandable panel.

**Persistent strip (always visible, all screens):**
- Patient name, UHID, age `[DERIVED]`, sex, photograph
- Episode selector (where >1)
- Diagnosis: primary site + laterality + histology (short) + grade
- Stage: displayed as **two distinct chips** — `cTNM / Clinical Stage` and `pTNM / Pathological Stage` — each with staging system name and version `[CCA CONFIG]`, date and stager
- Treatment intent chip
- Line of therapy chip
- Current treatment: regimen name (short) + cycle n of m + day n + planned next date
- Performance status: instrument + score + date + assessor
- Alert banner row (GEN-ALT-004)

**Expandable panel — organised in the following blocks:**

1. **Identifiers & demographics** — full name, UHID, alternate IDs, DOB, age, sex, gender identity `[CCA CONFIG]`, contact, address, next of kin, preferred language, payer.
2. **Cancer episode** — episode ID, date of first diagnosis, basis of diagnosis (histology/cytology/imaging/clinical `[CCA CONFIG]`), morphology code + term, topography code + term, laterality, grade, staging system + edition, cTNM (T, N, M, stage group, date, stager), pTNM (same), restaging events with dates, current disease status (with date and basis), sites of metastasis (multiselect, with dates).
3. **Biomarkers** — table: marker, method, specimen/accession, result value, result unit, interpretation (positive/negative/equivocal/not evaluable), reference/cutoff used, tested date, reported date, laboratory, therapeutic implication flag. Must handle: IHC, FISH/ISH, PCR, NGS panel results, MSI/MMR, TMB, germline results (with separate consent and access control `[CCA CONFIG]`) — **MO-DX-010 [PRODUCT]**: germline/hereditary results require distinct consent capture and distinct access permissions from somatic results.
4. **Performance status trend** — instrument, scores over time, with assessor and date.
5. **Allergies & prior reactions** — including prior infusion reaction detail (agent, cycle, grade, management, rechallenge outcome).
6. **Current medications** — segmented as per GEN-LNG-002, with anticoagulants and QT-relevant medications separately flagged `[CCA CONFIG]`.
7. **Comorbidities/problems** — with oncology-relevant flags.
8. **Treatment status summary** — modalities received (systemic/RT/surgery/oral), with per-modality micro-summary: for systemic, regimen + cycles completed/planned + last date + cumulative doses of tracked agents; for RT, site + prescribed dose/fractions + delivered dose/fractions + completion date; for surgery, procedure + date + margin status; for oral, drug + start date + current dose + adherence.
9. **Latest laboratory panel** — configurable panel `[CCA CONFIG]` with, at minimum: Hb, WBC, ANC `[DERIVED]` or reported, platelets, creatinine, calculated creatinine clearance `[DERIVED]`, eGFR `[DERIVED]`, bilirubin (total/direct), AST, ALT, ALP, albumin, sodium, potassium, calcium (with corrected calcium `[DERIVED]`), magnesium, LDH, tumour markers where relevant. Each with value, unit, reference range, abnormal/critical flag, resulted date/time, staleness indicator, and a trend sparkline.
10. **Cardiac/organ function** — LVEF or equivalent with date and method; pulmonary function where relevant; audiology where relevant `[CCA CONFIG — which regimens require which]`.
11. **Active toxicities** — term, grade, onset, trend arrow, attribution, current management.
12. **Treatment holds/delays** — active hold with reason, decided by, date, review date.
13. **MDT** — last discussion date, recommendation summary, action status, next MDT.
14. **Latest response assessment** — proposed vs confirmed, method/criteria used, date, target lesion sum, % change from baseline and from nadir.
15. **Consents** — type, status, date, version.
16. **Trial enrolment** — trial ID, arm (where unblinded), site PI, enrolment date `[CCA CONFIG]`.
17. **Care team** — named clinicians by specialty, navigator, pharmacist.
18. **Advance care planning / goals of care** `[CCA CONFIG — whether captured]`.

**MO-CON-020 [PRODUCT]** — Every header value displays its source date and is click-through to the source record. No header value may be displayed without a date.

### B.4.D Medical Oncology screens (enumerated; specified in Parts C, D, I)

| ID | Screen | Purpose |
|---|---|---|
| `MO-CON-100` | New Consultation | Full history, examination, provisional diagnosis, workup plan |
| `MO-CON-200` | Follow-up Consultation | Interval history, toxicity, examination, results review, plan continuation/change |
| `MO-DX-100` | Diagnosis & Cancer Episode | Episode creation, morphology/topography, basis of diagnosis, grade |
| `MO-DX-200` | Staging | cTNM entry, stage group `[DERIVED]`, staging system/version, restaging |
| `MO-DX-300` | Biomarker panel | Entry/import, interpretation, therapeutic implication |
| `MO-DX-400` | Disease status & Line of therapy | Status events over time; line definition |
| `MO-INV-100` | Investigation ordering | Lab, imaging, pathology/biomarker, cardiac, nuclear medicine; indication, urgency, clinical details for the performing department |
| `MO-INV-200` | Result review & acknowledgement | With comparison to prior, trend, acknowledgement audit |
| `MO-PLN-100` | Treatment Plan | Intent, modality sequence, planned regimen, planned cycles, planned RT/surgery referral, goals, prognostic discussion record |
| `MO-ORD-100` | Systemic Treatment Order — regimen selection | Part I |
| `MO-ORD-200` | Systemic Treatment Order — dosing & modification | Part I |
| `MO-ORD-300` | Systemic Treatment Order — supportive/premed/hydration | Part I |
| `MO-ORD-400` | Order review & signature | Part I |
| `MO-RDY-100` | Treatment readiness review | Part I §8 |
| `MO-RDY-200` | Treatment-day clearance | Clearance decision + note |
| `MO-MOD-100` | Dose modification | Structured reason, %, new dose, effective from cycle |
| `MO-MOD-200` | Hold / Delay | Reason, duration, review date, resumption criteria |
| `MO-MOD-300` | Discontinuation | Reason, date, final cumulative doses, next plan |
| `MO-RVW-100` | Post-cycle review | Tolerance, toxicity, labs, next cycle decision |
| `MO-RVW-200` | Toxicity review | Part 11 |
| `MO-RVW-300` | Response assessment confirmation | Part R |
| `MO-RVW-400` | End-of-treatment review | Triggers Treatment Summary |
| `MO-RVW-500` | Surveillance planning | Triggers Survivorship Care Plan |
| `MO-MDT-100` | MDT case submission | Part P |
| `MO-REF-100` | Referral (internal/external) | |
| `MO-ADM-100` | Admission request | Part Q |
| `MO-ORL-100` | Oral therapy prescription & review | Part 12 |

**Required documents (specified in Part F):** Initial Medical Oncology Consultation Note; Follow-up Oncology Note; Treatment-Day Review/Clearance Note; Post-Cycle Review Note; Toxicity Review Note; Treatment Modification/Hold Decision Note; End-of-Treatment Summary; Follow-up/Surveillance Note; Prognosis & Goals-of-Care Discussion Note `[CCA CONFIG — whether separate]`; Death Summary.

---

## B.5 — RADIATION ONCOLOGIST

### B.5.A Role purpose

**Why this role uses the system.** The Radiation Oncologist determines whether radiotherapy is indicated, defines the prescription (the legal authorisation for delivering ionising radiation), defines target volumes and organ-at-risk constraints, approves the treatment plan, authorises the start of treatment, monitors the patient weekly during delivery, manages acute toxicity, and signs the completion summary.

**Responsibility owned.** RT indication and intent; prescription (dose, fractionation, technique, target, energy, image-guidance regimen); target volume delineation; OAR constraint specification; plan approval; treatment authorisation; weekly on-treatment review; interruption and gap management; RT toxicity management; completion documentation; RT follow-up.

**Entry point.** Referral from MO/SO/MDT, or direct referral.

**Where responsibility ends.** RT completion and defined RT follow-up period, then handover to the coordinating specialty or surveillance.

**Receives work from.** MO, SO, MDT, Radiologist, Pathologist, Physicist (plan ready for approval, QA result), RTT (delivery events, positioning issues), Nursing (toxicity).

**Sends work to.** Simulation/CT-Sim, Dosimetry/Planning, Physics (plan QA), RTT (authorised plan for delivery), MO (concurrent systemic coordination), Nursing (supportive care), Navigator.

### B.5.B Worklist views

1. **RT Clinic Today** — new consults, follow-ups, on-treatment reviews.
2. **RT Pathway Board** — every RT patient with a `[DERIVED]` pathway state chip: `Consult done` → `Prescription signed` → `Simulation booked` → `Simulated` → `Contouring in progress` → `Contouring complete` → `Planning in progress` → `Plan ready for RO review` → `Plan approved by RO` → `Physics QA pending` → `Physics QA passed` → `Ready for treatment` → `On treatment (fraction n of m)` → `Treatment interrupted` → `Completed`. Each state with days-in-state and target interval `[CCA CONFIG]`.
3. **Plans Awaiting My Approval** — plan version, planner, dose objectives met/not met summary, OAR constraint table, comparison to previous version.
4. **On-Treatment Review (OTV) Due** — patients due weekly review, with fractions delivered, cumulative dose `[DERIVED]`, days since last OTV, current toxicity.
5. **Interruptions & Gaps** — patients with missed fractions, showing gap days and cumulative treatment time `[DERIVED]`.
6. **Results Inbox** — as for MO.

**Key worklist columns unique to RO:** treatment site(s), laterality, modality, technique, phase (n of m), prescribed dose/fractions, delivered dose/fractions `[DERIVED]`, fractions remaining `[DERIVED]`, machine/unit assigned, immobilisation device, image-guidance protocol, concurrent systemic therapy (yes/regimen), plan version, QA status.

### B.5.C Patient header for Radiation Oncologist

Shares the oncology core header (identifiers, diagnosis, stage cTNM/pTNM, biomarkers where relevant, performance status, allergies, comorbidities) plus RT-specific blocks:

- **Prior radiotherapy** — this is safety-critical. Must display: site(s), dates, total dose, dose/fraction, fractions, technique, treating centre (internal/external), overlap assessment with current target, cumulative dose to relevant OARs where computable `[INTEGRATION with TPS]`. **RO-010 [PRODUCT]** — the system must require an affirmative statement of prior RT (including "none") before a prescription can be signed.
- **Current prescription** — version, site, dose, fractions, dose/fraction, technique, phase.
- **Delivery progress** — fractions delivered/prescribed, cumulative delivered dose `[DERIVED]`, elapsed treatment days `[DERIVED]`, missed fractions with dates and reasons, projected completion date `[DERIVED]`.
- **Plan status** — current plan version, approval status, QA status, previous versions.
- **Concurrent systemic therapy** — regimen, cycle/day, last administration.
- **RT-specific toxicity** — site-specific acute toxicity grades over time (skin, mucositis, dysphagia, dermatitis, cystitis, proctitis etc. per site `[CCA CONFIG]`), weight trend, nutrition status, analgesia.
- **Devices/implants** — pacemaker/ICD (critical for RT), prosthesis, expander/implant `[CCA CONFIG]`.
- **Pregnancy status** where applicable.

Full RT specification, including every prescription parameter and every RT document, is in **PART L**.

---

## B.6 — SURGICAL ONCOLOGIST

### B.6.A Role purpose

**Why this role uses the system.** The Surgical Oncologist assesses operability and resectability, defines and documents the surgical plan, obtains procedure-specific informed consent, confirms fitness and site/laterality pre-operatively, performs and documents the operation, manages the post-operative course, interprets the resection pathology, establishes pathological stage, and hands off to adjuvant therapy.

**Responsibility owned.** Operability/resectability assessment; surgical plan; consent; pre-operative verification (including site and laterality); the operative record; specimen labelling and orientation instructions to pathology; post-operative management including wound, drain and stoma care; complication documentation; pathological staging; adjuvant handoff; surgical follow-up.

**Entry point.** Referral from MO/RO/MDT/external, or direct presentation.

**Where responsibility ends.** At surgical follow-up completion and adjuvant handoff, or at transfer to surveillance.

**Receives work from.** MO, RO, MDT, Radiologist, Pathologist (frozen section and final report), Anaesthetist (fitness), Inpatient team, Nursing.

**Sends work to.** Pathology (specimens), Anaesthesia (pre-op assessment), Theatre scheduling, Inpatient team, MO (adjuvant handoff), RO (adjuvant RT referral), MDT (post-operative discussion), Stoma/wound nursing, Navigator, Physiotherapy/Rehabilitation.

### B.6.B Worklist views

1. **Surgical Clinic Today** — new consults, pre-op reviews, post-op follow-ups, pathology-review visits.
2. **Surgical Pathway Board** — `[DERIVED]` state chips: `Consulted` → `Plan signed` → `Pre-op workup ordered` → `Workup complete` → `Anaesthesia cleared` → `Consent obtained` → `Scheduled` → `Pre-op H&P complete` → `Operated` → `Post-op day n` → `Pathology awaited` → `Pathology reviewed` → `pStage assigned` → `Adjuvant handoff done` → `Surgical follow-up`. With days-in-state and target intervals `[CCA CONFIG]`.
3. **Operating List** — date, theatre, order, patient, planned procedure, site + laterality, approach, estimated duration, anaesthesia type, blood requirement and availability status, implant/device requirement, frozen-section requirement, special equipment, consent status, fasting status, pre-op checklist status, `[DERIVED]` "ready for theatre" chip.
4. **Post-op Inpatients** — patient, post-op day `[DERIVED]`, procedure, ward/bed, vitals summary, drain outputs (per drain, 24-hour and cumulative `[DERIVED]`), wound status, stoma status, complication flags, mobilisation, nutrition, antibiotics day n, VTE prophylaxis status, planned discharge date, discharge readiness `[DERIVED]`.
5. **Pathology Awaiting Review** — specimens sent, accession, date sent, expected date, status (received/grossing/processing/reported/addendum), critical findings flag, margin status, node status, days outstanding.
6. **Adjuvant Handoff Pending** — operated patients whose pathology is reported but who have not yet been handed off to MO/RO/MDT, with days elapsed against configured target `[CCA CONFIG]`.

### B.6.C Patient header for Surgical Oncologist

Oncology core header plus:

- **Planned procedure vs Actual procedure** — displayed as a distinct pair (GEN-CMP-001), never one mutable field.
- **Site and laterality** — displayed with high visual prominence and mandatory reconfirmation at consent, pre-op H&P and operative note.
- **Neoadjuvant treatment received** — regimen, cycles, completion date, best response, interval since completion `[DERIVED]` (surgically critical).
- **Prior surgery** — procedures, dates, approach, findings, complications, adhesion risk.
- **Anaesthesia fitness** — ASA grade or equivalent `[CCA CONFIG]`, assessor, date, restrictions, airway concerns.
- **Anticoagulation/antiplatelet status** — drug, last dose, planned bridging, restart plan (safety-critical, must be surfaced not buried).
- **Blood group and antibody screen; blood availability** `[INTEGRATION]`.
- **Relevant imaging** — with direct viewer link and key measurements.
- **Frozen-section/intra-operative pathology plan.**
- **Implants/devices in situ.**
- **Post-op status where applicable** — POD n, drains (site, type, output), wound, stoma, complications (with grading system `[CCA CONFIG]`), current diet, mobilisation.
- **Pathology status** — accession, stage-relevant fields once reported (tumour size, grade, margins with distances, nodes examined/positive, LVI, PNI, treatment effect), pT/pN/pM, pathological stage.

Full surgical specification — every field of the Surgical Consultation Note, Surgical Plan, Pre-operative H&P, Operative Note, Immediate Post-op Note, Daily Progress Note, Wound/Drain/Stoma Note, Complication Note, Histopathology Review Note, Surgical Follow-up Note, Adjuvant Handoff Note and Surgical Discharge Note — is in **PART M**.

---

## END OF DOCUMENT 1

**Continues in Document 2:** PART B roles 7–21 (Radiologist, Radiology Coordinator, Pathologist, MDT Coordinator, MDT Chair, Oncology Pharmacist, Day Care/Infusion Nurse, Radiation Physicist, Radiation Technologist, Inpatient Oncology Clinician, Inpatient Nurse, Financial Counsellor/Billing, Hospital/Clinical Administrator, Patient-facing, and additional roles).
