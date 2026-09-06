# CCA CANCER CARE — ONCOLOGY HIS + EMR
# MASTER FUNCTIONAL & CLINICAL PRODUCT REQUIREMENT INVENTORY
## Document 5 of N — PART C (Screen-by-Screen), Section 3
### C.12 Day Care / Infusion & MAR · C.13 Toxicity / Adverse Events · C.14 Oral / Continuous Anticancer Therapy

*Conventions and universal state behaviour per C.0 (Document 3) apply throughout.*

---

# C.12 — DAY CARE / INFUSION & MEDICATION ADMINISTRATION SCREENS

## C.12.0 — Module design principles `[PRODUCT]`

**MAR-001** — The Day Care module is a **sequential gated workflow**, not a set of independently reachable forms. Administration cannot be started until arrival, identity, consent, clearance, readiness, product receipt, product verification and vascular access gates are each individually satisfied or explicitly overridden with a recorded reason and an authorised role. The screen must show the gate sequence and which gate is currently blocking.

**MAR-002** — The **ordered dose and the administered dose are never the same field**. Value #5 (actual administered) is entered by the nurse and defaults to the prepared dose *only as a pre-fill that the nurse must affirmatively confirm*; it is never silently equal.

**MAR-003** — Nothing in this module may be back-entered without the system recording both the clinical time and the entry time separately (`GEN-DTM-002`). Infusion start and stop times are to the minute.

**MAR-004** — Every screen in this module must remain usable on a mobile/tablet form factor at the chairside, and must tolerate intermittent connectivity by queuing writes locally with visible sync state. A write that has not synced must be visually distinct from one that has.

---

## C.12.1 · `SCR-MAR-001` — Day Care Treatment Queue

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care / Infusion Nurse; charge nurse (assignment); MO (view); Pharmacist (view). |
| **Navigation** | Landing screen for the Day Care nurse role. |
| **Purpose** | Show every patient scheduled today, their gate status, and what is blocking each. |
| **Header** | Unit selector; date; shift; counts strip (Scheduled / Arrived / In assessment / Ready / In treatment / In observation / Discharged / Deferred / Cancelled); chair occupancy `[DERIVED]`; unit capacity remaining `[DERIVED]`. |
| **Sections/tabs** | Today's Queue · Live Infusions (`SCR-MAR-013`) · Post-treatment Observation · Reactions & Incidents · Tomorrow / Upcoming · Unassigned. |
| **Table columns (exact)** | 1 Scheduled time · 2 Chair/bay · 3 Patient name · 4 UHID · 5 Age · 6 Sex · 7 Photograph thumbnail · 8 Regimen (short name) · 9 Cycle/Day · 10 Order version · 11 Expected duration `[DERIVED]` · 12 Expected finish time `[DERIVED]` · 13 Arrival status chip · 14 **Gate status strip** — eight micro-chips in fixed order: Identity · Consent · Clearance · Readiness · Product · Verification · Access · Premed (each green/amber/red/grey) — **MAR-005 [PRODUCT]** · 15 Pharmacy status chip · 16 Allergy/prior-reaction icon · 17 Vitals status · 18 Today's weight (value + delta vs order weight) · 19 Active toxicity max grade · 20 Assigned nurse · 21 Alerts icon stack · 22 Waiting time `[DERIVED]` · 23 Row actions. |
| **Filters** | Unit, chair, nurse, regimen, arrival status, gate blocked (which gate), pharmacy status, cleared/not cleared, has prior reaction, first cycle, delayed. |
| **Dropdowns** | Unit `[CCA CONFIG]`; nurse (roster); arrival status (product-defined, state-machine controlled); defer reason; cancel reason. |
| **Calculated** | Expected duration (`CALC-020`); expected finish; chair occupancy and turnover; waiting time; weight delta vs order weight (`CALC-013`); gate status derivation (`CALC-140`). |
| **Actions (row)** | Record arrival · Start assessment · Assign chair · Assign nurse · Open administration · Record vitals · Defer (reason) · Cancel (reason) · Escalate to clinician · Print chair label. **Actions (screen):** Assign chairs · Print unit day list · Refresh · Handover report. |
| **Chips** | Arrival status; per-gate chips; pharmacy status (Not sent / Verified / In preparation / Prepared / Released / Received / Returned); clearance (`Cleared by [name] at [time]` per `MAR-010`); readiness; consent; access suitability; first cycle; delayed cycle; prior reaction (persistent red). |
| **Alerts** | **Unit-level banner:** product released but not received within configured interval; a prepared product approaching BUD expiry with the patient not yet started (**MAR-006 [PRODUCT]** — BUD countdown must be visible on the queue, not only in pharmacy); order superseded after preparation; clearance expired; a patient in a chair with no assigned nurse; overdue observation on an active infusion. |
| **Conditional logic** | "Open administration" disabled until all gates green or overridden; hovering the disabled action names the blocking gate and the role who can resolve it (`GEN-STA` blocked-state contract). |
| **Empty state** | Distinguishes "no patients scheduled today", "all patients discharged", and "filtered to nothing". |
| **Downstream** | Arrival → assessment queue and waiting-time clock; assessment complete → ready state; administration start → live infusion board and MO/pharmacy visibility. |
| **Print/export** | Unit day list; chair allocation sheet; handover report. |

---

## C.12.2 · `SCR-MAR-002` — Arrival & Patient Identity Verification

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care nurse. |
| **Navigation** | Queue row → Record arrival; or wristband barcode scan at the unit desk. |
| **Purpose** | Establish that the person present is the person the order was written for — the first and most consequential gate. |
| **Header** | Patient photograph (large), name, UHID, DOB, age, sex; regimen, cycle/day; allergy banner. |
| **Sections** | 1 Arrival · 2 Identity verification · 3 Escort/accompaniment · 4 Immediate concerns. |
| **Fields** | **Arrival:** Arrival date/time (datetime, defaults now, editable with reason if changed); Arrived from (dropdown: Home / Ward / Clinic / Another facility / Emergency); Mode of arrival (Ambulant / Wheelchair / Stretcher / Assisted); Accompanied by (name, relationship); Interpreter present (auto-flagged requirement + Y/N + service/name). **Identity verification:** Verification method (multiselect, **minimum two independent identifiers required — product-defined, `MAR-007 [PRODUCT]`**): Full name stated by patient · Date of birth stated by patient · UHID on wristband scanned · Photograph matched · Photo ID document · Address stated · Carer confirmation (only where the patient cannot self-identify, with reason). Each selected method records: value confirmed (Y/N), and for scanning, the scanned value and the match result `[DERIVED]`. Patient able to self-identify (Y/N + reason if no). Verified by (auto); Verified at (auto). Wristband applied/present (Y/N; if applied now, printed by, at). **Immediate concerns:** Any new symptoms since last contact (Y/N + text → prompts toxicity screen); Feels well enough to proceed (Y/N + text); Fasting/preparation instructions followed where applicable. |
| **Tables** | Identity verification log (method, value, result, timestamp) — retained on the administration record. |
| **Dropdowns** | Arrived from, mode of arrival, verification method (product-defined); interpreter service `[CCA CONFIG]`. |
| **Calculated** | Barcode match result; time since last cycle `[DERIVED]`; waiting time start. |
| **Actions** | Scan wristband · Print wristband · Confirm identity · Report identity discrepancy · Record arrival · Defer. |
| **Chips** | Identity gate (green verified / red discrepancy / amber single-identifier only). |
| **Alerts** | **Hard stop:** scanned UHID does not match the open order's patient — the screen must halt the workflow, display both identities, and require a supervisor-level resolution action; the event is logged as a near-miss (`MAR-008 [PRODUCT]`). **Hard stop:** fewer than two identifiers verified. **Warning:** patient reports feeling unwell; interpreter required but not present. |
| **Conditional logic** | Carer-confirmation method available only when "able to self-identify = No". Wristband print action appears when no wristband present. |
| **Read-only** | Patient photograph and demographics; order patient identity. |
| **Sign/approve** | Nurse attestation of identity verification (attributed act, timestamped; forms part of the signed infusion note). |
| **Downstream** | Identity gate → green; arrival time published to the queue; waiting-time clock starts; next gate (`SCR-MAR-003`) unlocked. |
| **Print/export** | Wristband/label. |

---

## C.12.3 · `SCR-MAR-003` — Pre-Administration Assessment (Consent · Clearance · Readiness · Vitals · Weight)

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care nurse. |
| **Navigation** | From arrival → Start assessment. |
| **Purpose** | Confirm the authorisation chain and capture the day's clinical baseline that dosing and monitoring depend on. |
| **Header** | Full Day Care nurse header (B.13.C) with allergy/prior-reaction banner at highest priority. |
| **Sections** | 1 Order verification · 2 Consent · 3 Clinician clearance · 4 Readiness · 5 Anthropometrics · 6 Vitals · 7 Symptom & toxicity screen · 8 Pregnancy check where applicable · 9 Infection screen · 10 Fall risk · 11 Assessment conclusion. |
| **Fields — Order verification** | Order number and version (read-only); Order status (read-only — must be `SIGNED`/`RELEASED`, not draft, not superseded, not expired); Regimen, cycle, day (read-only, **nurse confirms each with an explicit checkbox** — `MAR-009 [PRODUCT]`: cycle and day confirmation is an affirmative act, because administering the wrong cycle day is a recognised error mode); Planned administration date matches today (auto-check); Order expiry not passed (auto-check); Any order changes since last cycle (auto-generated diff summary, read-only). |
| **Fields — Consent** | Consent type required (auto per `[CCA CONFIG]`); Consent status (auto: Obtained / Expired / Absent / Withdrawn); Consent version and date (read-only); Patient re-affirms willingness to proceed today (Y/N — **a separate, per-visit act distinct from the formal consent document**, `MAR-011 [PRODUCT]`); Reason if declined. |
| **Fields — Clearance** | Clearance status (auto: Cleared / Cleared with conditions / Not cleared / Expired); Clearing clinician name and timestamp (read-only); **Conditions attached to clearance** (read-only, rendered as a checkable list per `RDY-070` — each condition must be individually marked met/not met by the nurse before proceeding, with the supporting value recorded); Request clearance action (where absent — routes to MO clearance queue with urgency). |
| **Fields — Readiness** | Readiness snapshot (read-only table from `SCR-RDY-001`: criterion, result, date, outcome, override); Readiness evaluated at (timestamp); Re-evaluate action; Any criterion now expired `[DERIVED]` flag. |
| **Fields — Anthropometrics** | Weight today (numeric, kg, R where the regimen or `[CCA CONFIG]` requires; method and condition qualifiers per `INT-NUR-110`); Weight delta vs order weight `[DERIVED]` (absolute and %); **Dose review required flag** `[DERIVED]` when delta exceeds tolerance (`INT-NUR-111`) — routes to MO, blocks administration until resolved or overridden; Height (display, carry-forward action). |
| **Fields — Vitals** | Full `INT-NUR-200` set with reason for observation = "Pre-administration"; baseline for the day (this set is the comparator for all intra-infusion observations — **MAR-012 [PRODUCT]**). |
| **Fields — Symptom & toxicity screen** | Regimen-specific symptom checklist `[CCA CONFIG]`; each active toxicity presented for re-grading; new symptoms captured; each entry writes to the longitudinal toxicity record (`SCR-TOX-002`). |
| **Fields — Pregnancy check** | Where applicable per sex/age/`[CCA CONFIG]`: applicability, LMP, test required this cycle (Y/N per protocol), test result, test date/time. |
| **Fields — Infection screen** | Fever in preceding period, symptoms of infection, current antimicrobials, isolation requirement, recent contacts `[CCA CONFIG]`. |
| **Fields — Conclusion** | Nurse assessment summary (narrative); Fit to proceed (Y/N); If no — reason and action (escalate / defer / cancel); Escalation record. |
| **Tables** | Readiness criteria; clearance conditions; active toxicities for re-grading; vitals comparison (today vs last cycle). |
| **Calculated** | Weight delta; readiness expiry; BSA recomputed with today's weight (**displayed alongside the order BSA, not replacing it** — `MAR-013 [PRODUCT]`); time since clearance. |
| **Actions** | Confirm order · Confirm cycle/day · Record vitals · Record weight · Re-evaluate readiness · Request clearance · Mark condition met · Escalate · Defer · Complete assessment. |
| **Chips** | Per-gate; consent; clearance (with conditions count); readiness; weight delta; fit to proceed. |
| **Alerts** | **Hard stop:** order not signed, superseded, expired, or belonging to a different date; consent absent where required; clearance absent or expired; a non-overridable readiness criterion failed (`RDY-040`); patient declines. **Override with reason (authorised role):** readiness failure already overridden by the clinician (displayed, nurse acknowledges); clearance condition not met. **Warning:** weight delta beyond tolerance; vitals outside configured limits; new grade ≥ configured threshold toxicity `[CCA CONFIG]`; pregnancy test not performed where protocol requires. |
| **Conditional logic** | Pregnancy, infection and fall sections render per configuration. Clearance-condition checklist renders only when conditions exist. Re-grading list is generated from active toxicities. |
| **Read-only** | Order content; clearance; readiness derivation; consent record. |
| **Sign/approve** | Nurse signs the pre-administration assessment; this signature is a precondition for opening the administration record. |
| **Downstream** | Gates flip green; patient state → `READY`; administration screen unlocked; escalations routed; toxicity entries written; deferral cancels the chair booking and notifies MO, pharmacy (product disposition) and Navigator. |
| **Blocked** | If the prepared product has not been received, the assessment can complete but administration remains blocked at the product gate. |
| **Print/export** | Pre-administration assessment section of the Infusion Nursing Note. |

---

## C.12.4 · `SCR-MAR-004` — Product Receipt & Barcode Verification

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care nurse; second nurse (independent check). |
| **Navigation** | From queue → Receive product; from administration screen → Verify product; triggered by scanning a product barcode anywhere in the unit. |
| **Purpose** | Confirm that the physical product in hand is the right product, for the right patient, in date, undamaged, and matches the signed order. |
| **Header** | Patient identity strip with photograph; order/regimen/cycle/day. |
| **Sections** | 1 Receipt · 2 Product list · 3 Per-product verification · 4 Independent double check · 5 Discrepancies. |
| **Fields — Receipt** | Received from (Pharmacy / Ward / External); Received by (auto); Received at (datetime); Transport condition (dropdown: Ambient / Cold chain maintained / Cold chain breached / Light-protected / Unknown); Number of items expected `[DERIVED]` vs received (numeric); Condition on receipt (dropdown: Intact / Leaking / Damaged packaging / Precipitate visible / Discoloured / Label damaged / Other + text). |
| **Table — per product (exact columns)** | 1 Sequence · 2 Treatment block · 3 Drug name · 4 Label barcode scanned (scan field + `[DERIVED]` match result) · 5 Patient identifiers on label match patient (checkbox) · 6 Order number/version on label matches active order `[DERIVED]` · 7 Drug matches order row (checkbox) · 8 **Prepared dose on label** (read-only, value #4) · 9 Final ordered dose (read-only, value #3) · 10 Prepared-vs-ordered deviation `[DERIVED]` with tolerance status (`CALC-135`) · 11 Volume · 12 Diluent · 13 Concentration · 14 Route on label matches order (checkbox) · 15 **BUD (date/time)** · 16 BUD remaining `[DERIVED]` at receipt and projected at planned start · 17 Storage condition maintained (checkbox) · 18 Light protection present where required (checkbox) · 19 Filter/set supplied where required (checkbox) · 20 Container intact (checkbox) · 21 Visual inspection (dropdown: Clear / Particulate / Precipitate / Discoloured / Not applicable) · 22 Verification outcome (Accepted / Query / Rejected) · 23 Verified by · 24 Second checker · 25 Timestamps. |
| **Fields — Independent double check** | Second nurse identity (must differ from first — `GEN-AUD-004`); itemised checklist mirroring the columns above; discrepancies found; resolution; both signatures. **MAR-014 [PRODUCT]** — the double check is required for every hazardous/anticancer product; which products require it is `[CCA CONFIG]` but the *capability and enforcement* is product. |
| **Calculated** | Barcode match; prepared-vs-ordered deviation; BUD remaining; projected BUD at planned start and at projected end of infusion (**a product whose BUD expires mid-infusion must be flagged before starting** — `MAR-015 [PRODUCT]`). |
| **Actions** | Scan product · Accept · Query pharmacy · Reject and return · Request remake · Record discrepancy · Complete verification. |
| **Chips** | Per product: Not received / Received / Verified / Query / Rejected / Returned / Expired. BUD countdown chip (green/amber/red). |
| **Alerts** | **Hard stop:** barcode does not match the patient or the active order; BUD already expired; container damaged or particulate present; prepared dose deviation beyond tolerance without pharmacist review (`PHA-060`); product belongs to a superseded order version (`ORD-120`). **Warning:** BUD will expire before projected infusion end; cold chain breached; single-nurse verification where double check is configured. |
| **Read-only** | Order content; label content; pharmacy preparation record. |
| **Sign/approve** | Two nurse signatures where double check applies. |
| **Downstream** | Product gate green; product state → `RECEIVED`/`VERIFIED`; pharmacy notified of receipt (`PHA-080`); rejection creates a pharmacy remake task and a discrepancy record; the verification record is embedded in the Infusion Nursing Note. |
| **Print/export** | Product verification record. |

---

## C.12.5 · `SCR-MAR-005` — Vascular Access

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care nurse; vascular access nurse. |
| **Navigation** | From assessment; from administration screen access gate. |
| **Purpose** | Establish and document access adequate for what is being given — including explicit suitability for vesicants. |
| **Sections** | 1 Existing device · 2 New device insertion · 3 Patency & site assessment · 4 Suitability determination · 5 Care performed. |
| **Fields — Existing device** | Full `SCR-INT-007` field set (type, site, laterality, insertion date, days in situ `[DERIVED]`, gauge, lumens, dressing status/date, securement, last flushed). |
| **Fields — New insertion** | Device type (dropdown); Site (anatomical dropdown); Laterality — **with automatic contraindication check against recorded lymphoedema, axillary dissection, AV fistula, ipsilateral surgery** `[CCA CONFIG]` (`MAR-016 [PRODUCT]`); Gauge; Attempts (numeric); Inserted by; Insertion date/time; Local anaesthetic used; Ultrasound guided (Y/N); Insertion successful (Y/N); Complication at insertion; Dressing applied; Device lot where captured. |
| **Fields — Patency & site** | Flushes freely (Y/N); Blood return present (Y/N); Resistance felt (Y/N); Site appearance (multiselect: normal, erythema, swelling, tenderness, induration, discharge, leakage, bruising, cording); Phlebitis/infiltration score where configured `[CCA CONFIG]` (item scores + `[DERIVED]` total + band); Pain at site (score); Patient sensation on flush. |
| **Fields — Suitability** | **Suitable for this order's requirements** (dropdown — product-defined: Suitable for all ordered drugs / Suitable — non-vesicant only / Not suitable — requires central access / Not suitable — requires re-siting / Not assessed); Basis for determination; Determined by; Determined at; Vesicant drugs in this order `[DERIVED]` (auto-listed from formulary flags); Central access required by protocol `[DERIVED]`. |
| **Calculated** | Days in situ; suitability requirement derivation; contraindicated-limb check. |
| **Actions** | Assess existing · Insert new device · Re-site · Escalate for central access · Flush and confirm patency · Record care · Complete access gate. |
| **Chips** | Access gate; device type; days in situ (amber/red at configured limits `[CCA CONFIG]`); suitability. |
| **Alerts** | **Hard stop:** a vesicant is ordered and access is not documented suitable (`MAR-040`); insertion attempted on a contraindicated limb without override. **Warning:** device in situ beyond configured dwell limit; no blood return on a central device (prompts occlusion pathway `[CCA CONFIG]`); multiple failed attempts (prompts escalation). |
| **Downstream** | Access gate green; device record written to the longitudinal device register; escalation tasks; the access details are carried onto every administration row. |
| **Print/export** | Access assessment record. |

---

## C.12.6 · `SCR-MAR-006` — Administration Record (the MAR)

*The central screen of the module. Exceptional depth.*

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care / Infusion nurse (primary); second nurse (independent checks); MO and Pharmacist (view live). |
| **Navigation** | Queue → Open administration (enabled only when all gates satisfied per `MAR-001`). |
| **Purpose** | Execute and record the administration of each ordered item in sequence, capturing what was *actually* given. |
| **Header** | Fixed chairside header: patient photograph, name, UHID, age/sex; **allergy and prior-reaction banner (highest priority, non-dismissible)**; regimen, cycle/day; order number + version; assigned nurse; chair; elapsed session time `[DERIVED]`; next observation due `[DERIVED]`; emergency/rescue medication availability chip. |
| **Sections** | 1 Session start · 2 Sequence timeline · 3 Premedication block · 4 Hydration (pre) · 5 Anticancer block · 6 Hydration (post) · 7 Supportive block · 8 Observations · 9 Events (interruptions, reactions, extravasation) · 10 Session end. |
| **Sequence timeline** | Horizontal timeline showing every ordered item in sequence with planned start offset, planned duration, actual start, actual elapsed and status colouring. Items out of sequence are visually flagged. Displays projected session end `[DERIVED]` updating live. **MAR-017 [PRODUCT]** — administering out of the ordered sequence requires an explicit action with a recorded reason; the sequence is a clinical instruction, not a display convenience. |
| **Table — administration rows: exact columns** | 1 Sequence · 2 Treatment block · 3 Drug · 4 Formulation · 5 **STANDARD DOSE** (read-only) · 6 **CALCULATED DOSE** (read-only) · 7 **FINAL ORDERED DOSE** (read-only) · 8 **PHARMACY PREPARED DOSE** (read-only, from `SCR-PHA-005`) · 9 **ACTUAL ADMINISTERED DOSE** (editable, R — pre-filled from prepared dose but requiring affirmative confirmation per `MAR-002`) · 10 Dose unit · 11 Administered-vs-ordered variance `[DERIVED]` (% and absolute, `CALC-150`) · 12 Variance reason (dropdown, R when variance ≠ 0) · 13 Route (read-only from order; change requires prescriber authorisation) · 14 Access device used (dropdown from the patient's device list, R) · 15 Diluent/volume (read-only) · 16 **Ordered rate** (read-only) · 17 **Actual rate** (numeric + unit, R) · 18 Rate changes during infusion (expandable sub-table) · 19 Volume infused `[DERIVED]` · 20 **Start date/time** (datetime, R, to the minute) · 21 **End date/time** (datetime, R) · 22 Actual duration `[DERIVED]` (`CALC-151`) · 23 Duration variance vs ordered `[DERIVED]` · 24 Administration status (dropdown — product-defined: Not started / In progress / Paused / Completed in full / Completed — partial / Stopped — not resumed / Omitted / Cancelled) · 25 Partial administration detail (fraction of dose given `[DERIVED]`, volume remaining, reason) · 26 Administered by (auto) · 27 Independent checker (second nurse, where required) · 28 Product barcode scanned at administration (`[DERIVED]` match) · 29 Patient identity re-verified at administration (checkbox + method) · 30 Row notes · 31 Row actions. |
| **Per-row sub-tables** | **Rate changes:** time, previous rate, new rate, reason (dropdown: protocol step-up / reaction / patient tolerance / clinical instruction / device factor / other), instructed by, recorded by. **Pauses:** pause time, restart time, duration `[DERIVED]`, reason, volume infused at pause, action taken. |
| **Fields — Session start** | Session start time; nurse; chair; emergency medications available and in date (checklist, R — **MAR-018 [PRODUCT]**: availability of the protocol-required rescue medications is verified before the first anticancer drug, not assumed); spill kit available; extravasation kit available; resuscitation equipment checked `[CCA CONFIG]`; patient positioned and comfortable; call bell in reach; patient briefed on what to report. |
| **Fields — Observations** | Observation schedule `[DERIVED]` from the regimen's monitoring requirements `[CCA CONFIG]` (e.g. baseline, 15 min after start of drug X, every 30 min, at completion). Each observation: due time, actual time, vitals set (full `INT-NUR-200`), patient symptoms (checklist + free text), infusion site check, action taken, recorded by. Overdue observations flagged red on the header and the live board. |
| **Fields — Session end** | All rows in a terminal state (validated); total volume administered `[DERIVED]`; total session duration `[DERIVED]`; post-treatment vitals (link to `SCR-MAR-010`); patient condition; access device (flushed / removed / retained — with details); disposal of cytotoxic waste per policy `[CCA CONFIG]` (checkbox); session end time; nurse signature. |
| **Calculated** | Actual duration; duration variance; volume infused; fraction of dose administered on partial; administered-vs-ordered variance; cumulative administered dose update (`CALC-102`, using value #5); session totals; next observation due; projected end time. |
| **Actions (row)** | Scan product · Verify identity · Start · Pause · Change rate · Restart · Complete · Complete as partial · Stop · Omit (reason) · Record reaction · Record extravasation · Add note · Re-order sequence (with reason). **Actions (screen):** Record observation · Escalate to clinician · Call pharmacy · Print MAR · End session. |
| **Chips** | Per row: Not started / In progress / Paused / Complete / Partial / Stopped / Omitted; variance; sequence deviation; barcode verified. Session: gates, observation overdue, reaction active, BUD countdown per hanging product. |
| **Alerts** | **Hard stop:** starting a row whose product is not verified; starting a row when the order is superseded or expired; starting out of sequence without the explicit reason action; administering a vesicant through access not documented suitable; BUD expired; barcode mismatch at administration; starting before the pre-administration assessment is signed. **Override with reason:** dose variance beyond tolerance; route change; rate exceeding the ordered rate or the drug's configured maximum. **Warning:** observation overdue; infusion running longer than ordered duration by more than tolerance `[CCA CONFIG]` (suggests pump or access problem); infusion completing faster than ordered duration (suggests free-flow) — **MAR-019 [PRODUCT]**: both directions of duration deviation must alert, not only slow running. |
| **Conditional logic** | Independent checker required per drug flag `[CCA CONFIG]`. Observation schedule varies per drug and per first-exposure status (first dose of a monoclonal, for example, carries a different schedule `[CCA CONFIG]`). Partial-administration fields appear on selecting that status. Rate-change sub-table appears once any change is recorded. |
| **Read-only** | Dose values #1–#4; ordered route, rate, diluent, volume; order content; product label content. |
| **Sign/approve** | Per-row administration is an attributed, timestamped act. The **session** is signed by the administering nurse at end; where a second nurse participated, both are recorded. Signature freezes all values into the Infusion Nursing Note. |
| **Amendment/version** | Post-signature correction only by addendum with reason; original values retained and displayed. **MAR-020 [PRODUCT]** — an administered dose can never be edited to match the ordered dose retrospectively; corrections are additive and visible. |
| **Current vs previous** | Previous cycle's administration record accessible side by side (doses, rates, durations, reactions, variances), so that a change in tolerance is visible at the chairside. |
| **Post-signature** | Cumulative doses updated; Treatment Summary source data written; billing charge capture triggered `[CCA CONFIG]`; next-cycle due date computed; MO's post-cycle review task created; toxicity entries written; pharmacy notified of any returns/wastage. |
| **Downstream queues** | Post-treatment observation (`SCR-MAR-010`); MO post-cycle review; pharmacy wastage/returns; scheduling for next cycle; Navigator. |
| **Blocked/error** | Loss of connectivity queues writes locally with visible unsynced state (`MAR-004`); the screen must never lose a recorded start or stop time. If a write fails, the nurse is told explicitly which row is unsaved. |
| **Print/export** | MAR sheet; Infusion Nursing Note (`SCR-MAR-012`). |

---

## C.12.7 · `SCR-MAR-007` — Interruption, Partial Administration & Variance

**Role:** Day Care nurse; MO (authorising where required).
**Navigation:** Row action from the MAR; or automatically prompted when a row is stopped before completion.
**Purpose:** Record precisely why an administration did not proceed as ordered, and what was actually delivered.
**Sections:** Event · Delivered amount · Clinical response · Decision · Authorisation.
**Fields:** Event type (dropdown — product-defined: Paused — clinical / Paused — patient request / Paused — access problem / Paused — equipment / Stopped — reaction / Stopped — clinical decision / Stopped — patient request / Stopped — equipment failure / Not started — product unavailable / Not started — patient declined / Omitted — clinical decision); Event time; Volume infused at event (numeric, mL, R); **Dose delivered at event** `[DERIVED]` (`CALC-152` — from volume infused × concentration, with the calculation shown, R to confirm); Fraction of ordered dose delivered `[DERIVED]` (%); Reason (dropdown + narrative, R); Clinical observations at event; Interventions performed; Clinician notified (name, method, time, response); Decision (dropdown: Resume at same rate / Resume at reduced rate / Resume after intervention / Do not resume — complete as partial / Do not resume — omit remainder / Substitute route / Reschedule remainder); Remainder disposition (Discard / Return to pharmacy / Retain for later administration — with BUD check `[DERIVED]`); Authorisation required (Y/N per `[CCA CONFIG]`) and authorising clinician.
**Calculated:** Dose delivered from volume; fraction delivered; remaining dose; effect on cumulative dose; effect on dose intensity `[DERIVED]`.
**Alerts:** Hard stop on retaining a remainder whose BUD would expire before the intended later administration; warning that partial administration affects the cycle's dose intensity and should be reviewed by the prescriber.
**Downstream:** Writes value #5 as the partial amount (never the ordered amount); creates an MO review task; updates cumulative dose using the actual delivered amount; pharmacy notified for disposition; toxicity record if the cause was clinical.
**Print/export:** Interruption record appended to the Infusion Nursing Note.

---

## C.12.8 · `SCR-MAR-008` — Infusion Reaction Management

| Dimension | Specification |
|---|---|
| **Role(s)** | Day Care nurse (primary); MO (assessment and orders); resuscitation team. |
| **Navigation** | MAR row action "Record reaction"; header emergency action (always accessible from any Day Care screen — **MAR-021 [PRODUCT]**: reaction recording must be reachable in one action from anywhere in the module); prompted automatically by observation values crossing configured thresholds `[CCA CONFIG]`. |
| **Purpose** | Capture a time-critical clinical event contemporaneously, without the documentation impeding the care. |
| **Design constraint** | **MAR-022 [PRODUCT]** — the screen opens in a minimal "capture now, complete later" mode: a single timestamp button, a symptom multiselect and an "infusion stopped" toggle are the only required immediate entries. Everything else is completable after the event, with the clinical times preserved. |
| **Sections** | 1 Immediate capture · 2 Timeline · 3 Clinical detail · 4 Interventions · 5 Outcome · 6 Rechallenge decision · 7 Reporting. |
| **Fields — Immediate** | Reaction onset time (button-captured, editable); Suspected agent (dropdown of currently/recently running drugs, pre-selected to the running drug); Infusion stopped (toggle + time); Symptoms (multiselect `[CCA CONFIG]`: flushing, rash, urticaria, pruritus, angioedema, dyspnoea, wheeze, stridor, cough, chest tightness, back pain, abdominal pain, nausea/vomiting, rigors, fever, hypotension, hypertension, tachycardia, bradycardia, desaturation, dizziness, syncope, altered consciousness, injection-site pain, other); Severity impression (initial). |
| **Fields — Timeline** | Repeating time-stamped entries: time, observation/vitals, symptom change, intervention given, responder present. Vitals sets link to the observation record. Time from infusion start to onset `[DERIVED]` (`CALC-153`); volume/dose infused at onset `[DERIVED]`. |
| **Fields — Clinical detail** | Prior exposure to this agent (auto: cycle count); prior reactions to this agent (auto from `SCR-INT-004`); premedication given this cycle (auto, with times); infusion rate at onset; concurrent medications; reaction grade (`[CCA CONFIG]` terminology, R); reaction type (dropdown — product-defined: Infusion-related reaction / Hypersensitivity — immediate / Hypersensitivity — delayed / Anaphylaxis / Cytokine release / Extravasation-related / Other / Undetermined); attribution to agent (dropdown: Definite / Probable / Possible / Unlikely / Unrelated). |
| **Fields — Interventions** | Repeating: intervention (multiselect: infusion stopped, infusion rate reduced, IV fluids, oxygen — with flow and device, antihistamine, corticosteroid, adrenaline — with dose/route/site, bronchodilator, antipyretic, vasopressor, positioning, cardiac monitoring, ECG, resuscitation called, transfer to higher care), drug interventions with drug/dose/route/time/administered by, response to intervention, time. |
| **Fields — Outcome** | Outcome (dropdown — product-defined: Resolved completely / Resolved with sequelae / Ongoing at discharge / Transferred to inpatient / Transferred to emergency / Death); Resolution time `[DERIVED]` duration; Observation period extended (Y/N + duration); Discharged / admitted; Follow-up arranged. |
| **Fields — Rechallenge decision** | Rechallenge attempted today (Y/N); If yes: restart time, restart rate, premedication given, outcome; Future rechallenge (dropdown: Permitted with premedication / Permitted with slower rate / Permitted after desensitisation / Not permitted / Clinician to decide); Decided by; Future precautions (structured + narrative) — **written back to the allergy/reaction record (`SCR-INT-004`) so it appears on every future order and administration** — `MAR-023 [PRODUCT]`. |
| **Fields — Reporting** | Adverse drug reaction report required `[CCA CONFIG]` (Y/N); report reference; serious criteria met (checkboxes); reported to (pharmacovigilance / sponsor for trial patients / institutional incident system); reported by/at. |
| **Calculated** | Time to onset; dose/volume at onset; duration of reaction; cumulative reaction count for this agent for this patient. |
| **Actions** | Capture onset · Stop infusion · Add timeline entry · Record intervention · Call clinician · Call emergency team · Record outcome · Complete record · Link to toxicity record · Generate ADR report. |
| **Chips** | Reaction active (red, persistent across the module until closed); grade; attribution; reporting status. |
| **Alerts** | Hard stop on closing the record without an outcome; warning if adrenaline was administered and no emergency escalation is recorded; warning if rechallenge is attempted without documented clinician authorisation. |
| **Sign/approve** | Nurse signs the nursing record; the clinician signs the clinical assessment and rechallenge decision — two distinct signatures. |
| **Downstream** | Allergy/reaction record updated; toxicity record entry created; MO notified immediately; pharmacy notified (premedication implications for future cycles); order flagged for review; incident/ADR reporting queue; the reaction appears permanently in the patient header banner. |
| **Print/export** | Infusion Reaction Record; ADR report. |

---

## C.12.9 · `SCR-MAR-009` — Extravasation Management

**Role:** Day Care nurse; MO; vascular access/tissue viability.
**Navigation:** MAR row action; access assessment; one-action emergency access.
**Purpose:** Manage and document a time-critical tissue injury event with agent-specific management.
**Fields:** Detection time; Detected by; How detected (dropdown: patient symptom / nurse observation / alarm / routine site check); Drug involved; Drug classification `[DERIVED]` from formulary (vesicant / irritant / neutral); Volume estimated to have extravasated (numeric, mL); Dose estimated extravasated `[DERIVED]`; Access device involved (from device register); Site and laterality; Site appearance (multiselect: swelling, erythema, blanching, blistering, induration, discolouration, coolness, warmth); Measurement of affected area (length × width, mm); Pain score; Sensory/motor changes; Photograph (capture, dated, consented `[CCA CONFIG]`); **Immediate actions** (checklist: infusion stopped, cannula aspirated, cannula retained/removed with time, limb elevated, thermal application — warm/cold per agent-specific protocol `[CCA CONFIG]`, marking of affected area); Antidote required `[DERIVED]` from the agent's protocol `[CCA CONFIG]` — antidote name, dose, route, time given, administered by; Clinician notified (name, time, response); Specialist referral (plastic surgery / tissue viability / vascular); Follow-up plan (review intervals, who, where); Follow-up assessments (repeating: date, appearance, measurement, photograph, pain, function, action); Outcome (dropdown: Resolved without sequelae / Resolved with skin change / Ulceration / Necrosis / Surgical intervention required / Ongoing); Incident report reference.
**Calculated:** Time from detection to antidote; affected area; follow-up due dates.
**Alerts:** Hard stop on closing without recording whether the agent was a vesicant and whether the agent-specific protocol was followed; warning if an antidote required by protocol is not recorded as given within the protocol's time window `[CCA CONFIG]`.
**MAR-024 [PRODUCT]** — extravasation follow-up creates scheduled review tasks; the event does not close at the end of the session.
**Downstream:** Toxicity record; incident register; device register; future orders flagged for central access consideration; Navigator follow-up.
**Print/export:** Extravasation Record; patient instruction sheet.

---

## C.12.10 · `SCR-MAR-010` — Post-Treatment Observation

**Role:** Day Care nurse.
**Purpose:** Observe for the protocol-required period and confirm the patient is safe to leave.
**Fields:** Observation period required `[DERIVED]` from regimen and first-exposure status `[CCA CONFIG]`; Observation start time (= last infusion end); Required end time `[DERIVED]`; Observations (repeating vitals sets with reason "Post-administration"); Symptoms; Access device disposition (flushed and retained / removed — with time, site condition after removal, dressing, bleeding); Oral intake tolerated; Mobility; Pain; Nausea; **Discharge criteria checklist** `[CCA CONFIG]` — each item with met/not met and the supporting value (vitals within limits, no active reaction, tolerating fluids, ambulant to baseline, no uncontrolled symptoms, escort present where required, transport arranged); Discharge criteria met `[DERIVED]`; Extended observation (Y/N + reason + duration).
**Chips:** Observation period remaining (countdown); criteria met.
**Alerts:** Hard stop on discharge before the required observation period without clinician authorisation; warning on any unmet discharge criterion.
**Downstream:** Discharge screen unlocked.

---

## C.12.11 · `SCR-MAR-011` — Discharge from Day Care

**Role:** Day Care nurse.
**Sections:** Condition at discharge · Education · Instructions · Medications · Next appointments · Contacts · Sign.
**Fields:** Condition at discharge (dropdown: Stable — unchanged from baseline / Stable — minor symptoms / Symptomatic — managed / Deteriorated — admitted / Deteriorated — referred to emergency); Final vitals (link); Symptoms at discharge; Mode of departure; Escorted by; Transport; **Education delivered** (checklist with material versions per `NAV-130`: expected side effects and their timing, self-care measures, oral supportive medication instructions, hydration, infection precautions, handling of body fluids `[CCA CONFIG]`, activity, diet, contraception, when to take temperature); **Red-flag instructions** (structured, R — the specific symptoms and thresholds requiring urgent contact, from the regimen's patient-information master `[CCA CONFIG — CLINICAL SIGN-OFF]`) — **MAR-025 [PRODUCT]**: red-flag instructions are a structured, versioned, mandatory artifact, not narrative advice; **24-hour contact number** (from `[CCA CONFIG]`, printed); Take-home medications dispensed (list with counselling confirmation); Comprehension confirmed (method: teach-back / verbal / written acknowledgement); Carer present for education; Next treatment date (auto-proposed `[DERIVED]`, booked Y/N); Next review appointment; Investigations before next cycle (list with dates booked); Nurse signature.
**Alerts:** Hard stop on discharge without red-flag instruction issuance and comprehension recording; warning if the next cycle is unbooked or if pre-cycle investigations are unbooked (`REG-FD-120` analogue).
**Downstream:** Encounter closed; next-cycle booking task; pre-cycle investigation orders; Navigator; MO post-cycle review; patient education log; Infusion Nursing Note finalised.
**Print/export:** Patient discharge instruction sheet (lay language, versioned, with red flags and contact number); appointment schedule.

---

## C.12.12 · `SCR-MAR-012` — Infusion Nursing Note (assembled & signed)

**Purpose:** One signed document assembling the entire treatment-day record. Assembled from the structured data captured above — **not re-typed** (`MAR-026 [PRODUCT]`).
**Required sections (fixed order):**
1. **Header** — patient identifiers, episode, diagnosis, regimen, cycle/day, order number and version, unit, chair, date, nurse(s).
2. **Arrival & identity verification** — arrival time, mode, identity methods used and results.
3. **Authorisation chain** — consent (type, version, date), clinician clearance (name, time, conditions and whether met), readiness snapshot as at clearance.
4. **Pre-administration assessment** — weight (with delta and dose-review outcome), height, BSA (order vs today), baseline vitals, symptom/toxicity screen with grades, pregnancy/infection screens where applicable, fit-to-proceed conclusion.
5. **Vascular access** — device, site, insertion/assessment, patency, suitability determination.
6. **Product receipt & verification** — per product: barcode match, prepared dose vs ordered dose, BUD, condition, verification signatures.
7. **Administration record** — the full five-value table per drug, with actual rate, start/end times, duration and variance, access used, checkers, and sequence adherence.
8. **Observations** — all vitals sets in time order, interleaved with the drug timeline.
9. **Events** — interruptions, rate changes, partial administrations, reactions, extravasations, with times and interventions.
10. **Post-treatment observation** — observations, discharge criteria.
11. **Discharge** — condition, education delivered with versions, red-flag instructions issued, comprehension, take-home medications, next appointments.
12. **Cumulative position** — cumulative doses after this cycle for tracked agents, cycles completed of planned.
13. **Signatures** — administering nurse, second checker(s), any clinician entries, times.
**Amendment:** addendum only; original immutable.
**Print/export:** Full note; abbreviated chairside summary; copy to referring/inpatient team on request.

---

## C.12.13 · `SCR-MAR-013` — Live Infusion Board

**Role:** All unit staff; charge nurse.
**Purpose:** Unit-wide situational awareness.
**Columns:** Chair · Patient · Regimen · Current drug (sequence n of m) · Start time · Elapsed `[DERIVED]` · Ordered duration · Projected end `[DERIVED]` · Rate · Volume remaining `[DERIVED]` · Next observation due `[DERIVED]` (with overdue flag) · Reaction status · Interruption status · Nurse · BUD countdown for hanging products.
**Alerts:** Overdue observation; infusion running beyond tolerance; unattended chair (no nurse assigned); reaction active anywhere in the unit; BUD expiry imminent (`MAR-020` visual prominence requirement).
**Print/export:** Shift handover board.

---

# C.13 — TOXICITY / ADVERSE EVENT SCREENS

## C.13.1 · `SCR-TOX-001` — Toxicity Register & Timeline

| Dimension | Specification |
|---|---|
| **Role(s)** | All clinical roles (view); MO/RO/SO/inpatient clinician (grade and attribute); nursing (report and observe). |
| **Navigation** | Patient header → Toxicity tab; from any consultation's toxicity section; from Day Care; from OTV; from inpatient review. |
| **Purpose** | Show toxicity **over time**, per event, with grade trajectory — not as a list of isolated entries (`TOX-001` requirement from the brief). |
| **Header** | Full clinical header + toxicity strip: count of active toxicities, highest active grade, treatment currently held for toxicity (Y/N). |
| **Sections** | 1 Timeline view · 2 Active toxicities · 3 Resolved toxicities · 4 Grade trajectory chart · 5 Treatment impact log. |
| **Timeline view** | Horizontal swim-lane chart: one lane per toxicity term, plotted against time, with grade encoded by height/colour, overlaid with treatment events (cycle administrations, RT fractions, surgery, dose reductions, holds, growth factor, transfusions, admissions). **TOX-010 [PRODUCT]** — this overlay is mandatory; a toxicity grade is not interpretable without knowing what treatment preceded it. |
| **Table — active toxicities (exact columns)** | 1 Toxicity term (coded `[CCA CONFIG]` terminology) · 2 Category/system · 3 Onset date · 4 Days since onset `[DERIVED]` · 5 Grade at onset · 6 **Current grade** · 7 Peak grade `[DERIVED]` · 8 Grade trend `[DERIVED]` (improving / stable / worsening, from the last two gradings) · 9 Last graded date · 10 Last graded by · 11 Days since last grading `[DERIVED]` (overdue flag `[CCA CONFIG]`) · 12 Attribution · 13 Suspected agent(s) · 14 Treatment cycle/fraction at onset · 15 Current status (Active / Improving / Resolved / Resolved with sequelae / Chronic / Unknown) · 16 Interventions in place · 17 Treatment impact (none / dose reduced / delayed / held / discontinued) · 18 Linked records · 19 Actions. |
| **Table — treatment impact log** | Date · Toxicity · Grade · Decision (reduce/delay/hold/discontinue) · Magnitude (e.g. −25%) · Decided by · Linked order version · Outcome. |
| **Calculated** | Days since onset; peak grade; trend; days since last grading; duration of each grade level; cumulative days at grade ≥ threshold `[DERIVED]`; count of toxicity-driven dose modifications. |
| **Actions** | Add toxicity · Re-grade · Resolve · Reopen · Attribute · Link to intervention · Link to dose modification · Print toxicity summary · Filter by agent/cycle/system. |
| **Chips** | Grade (colour-banded by grade, `[CCA CONFIG]` scale); trend arrow; overdue grading; treatment-limiting; serious/reportable. |
| **Alerts** | Active toxicity not re-graded at a treatment encounter (blocks clearance per `SCR-RDY-002`); grade ≥ configured threshold without a documented management action; a toxicity that triggered a dose modification not re-graded before the next cycle. |
| **Print/export** | Toxicity summary for MDT, Treatment Summary and Survivorship plan. |

## C.13.2 · `SCR-TOX-002` — Toxicity Entry & Grading
**Fields:** Toxicity term (coded, searchable, R — terminology and version `[CCA CONFIG]`); Category/system (auto); Onset date (date + precision); Onset context (dropdown: after cycle n day n / during infusion / during RT fraction n / post-operative day n / between cycles / unrelated to treatment); Grade (dropdown, value set derived from the term's grading definitions `[CCA CONFIG]` — **each grade's definition text displayed inline so the grader is not grading from memory**, `TOX-020 [PRODUCT]`); Grading basis (clinical / laboratory / patient-reported / imaging); Supporting value (e.g. the lab result, auto-linked where laboratory-graded); Attribution (dropdown: Definite / Probable / Possible / Unlikely / Unrelated / Not assessable); Suspected agent(s) (multiselect from current and recent treatments, auto-populated); Alternative explanations considered; Serious criteria (checkboxes: death, life-threatening, hospitalisation/prolongation, disability, congenital anomaly, medically significant); Expected/unexpected per protocol `[CCA CONFIG]`; Examination findings; Investigations ordered; Interventions (medication with dose/route/duration, procedure, supportive care, referral, admission); Treatment decision (none / dose reduction with % / delay with days / hold / discontinue — links to `SCR-ORD-005`/`SCR-ORD-006`); Patient advised (Y/N, instructions); Follow-up plan (review date, by whom, parameters to monitor); Resolution date; Resolution status; Sequelae; Grader identity and timestamp.
**Conditional logic:** Serious criteria trigger the reportable-AE workflow (`SCR-TOX-004`) and, for trial patients, the sponsor SAE pathway (`TRL-030`). Laboratory-graded terms auto-populate grade from the linked result with clinician confirmation.
**Alerts:** Hard stop on grading without attribution; warning if grade ≥ threshold with no intervention and no treatment decision; warning if the term is one for which the protocol mandates a specific action `[CCA CONFIG]`.
**Downstream:** Register and timeline; readiness criteria; clearance; dose modification; MDT pack; Treatment Summary; Survivorship late-effects section; ADR/SAE reporting.

## C.13.3 · `SCR-TOX-003` — Toxicity Review Note
**Purpose:** A clinician-signed longitudinal review, not a per-event entry.
**Sections:** 1 Period reviewed · 2 Treatment received in period · 3 Toxicities by term with grade trajectory · 4 Interventions and response · 5 Impact on treatment delivered (cycles delayed, dose intensity `[DERIVED]`) · 6 Current status per toxicity · 7 Management plan · 8 Monitoring plan · 9 Patient instructions · 10 Next review · 11 Signature.
**Calculated:** Relative dose intensity for the period `[DERIVED]` (`CALC-117`); days of treatment delay attributable to toxicity; number of unscheduled contacts/admissions.
**Print/export:** Toxicity Assessment / Follow-up Note.

## C.13.4 · `SCR-TOX-004` — Serious / Reportable Adverse Event
**Fields:** Event; seriousness criteria; onset; description narrative; relevant history; concomitant medications; suspect product(s) with lot where known; dechallenge/rechallenge; outcome; reporter; report type (initial/follow-up); regulatory reference `[CCA CONFIG]`; sponsor reference for trials; submission date; acknowledgements; internal incident linkage.
**Alerts:** Reporting deadline countdown `[DERIVED]` per configured timeframe `[CCA CONFIG]`.
**Downstream:** Pharmacovigilance queue; trials coordinator; clinical governance register.

---

# C.14 — ORAL / CONTINUOUS ANTICANCER THERAPY SCREENS

## C.14.1 · `SCR-ORL-001` — Oral Therapy Prescription

| Dimension | Specification |
|---|---|
| **Role(s)** | Medical Oncologist (prescribe/sign); Pharmacist (verify/dispense); nurse (counsel). |
| **Navigation** | Treatment plan → oral component; consultation → prescribe; refill review → re-prescribe. |
| **Purpose** | Prescribe a self-administered anticancer therapy with the same rigour as an infusion order, recognising that the administration happens unobserved. |
| **Header** | Full MO header + oral therapy strip: drug, current dose, start date, days on therapy `[DERIVED]`, cycle position where cyclical, next review due, last dispensed. |
| **Sections** | 1 Regimen/drug selection · 2 Dosing · 3 Schedule · 4 Administration instructions · 5 Dispensing · 6 Monitoring · 7 Interactions · 8 Patient instructions · 9 Sign. |
| **Fields — Drug & dosing** | Regimen/protocol (from Regimen Master where the oral agent is part of a named regimen, else standalone); Drug (Formulary, R); Formulation and strength (dropdown — **the available tablet/capsule strengths must be shown, because the prescribed dose must be achievable from real strengths**, `ORL-010 [PRODUCT]`); Dose basis (fixed / mg/m² / mg/kg); Standard dose (from master); Calculated dose `[DERIVED]`; Dose modification % and reason; **Final prescribed dose** (numeric, R); Dose unit; **Achievable from available strengths** `[DERIVED]` (Y/N — with the tablet combination shown, `CALC-160`); Dose per administration; Number of units per administration `[DERIVED]`. |
| **Fields — Schedule** | Frequency (dropdown — product-defined: once daily / twice daily / three times daily / four times daily / alternate days / weekly / specified days); Timing (dropdown + specific times); Schedule pattern (dropdown: Continuous / Cyclical — n days on, m days off / Intermittent — specified days / Loading then maintenance); Cycle length (days, conditional); Days on/off (conditional, R for cyclical); Cycle number; Start date (R); Planned duration or number of cycles; Planned end date `[DERIVED]`; First-dose date and time. |
| **Fields — Administration instructions** | Food instruction (dropdown — product-defined: With food / Without food — 1h before or 2h after / With or without food / Specific instruction); Fluid; Swallow whole / may crush (from formulary); Handling precautions (hazardous drug handling for the patient and household `[CCA CONFIG]`); Storage; **Missed-dose instruction** (structured, from the drug's patient-information master `[CCA CONFIG — CLINICAL SIGN-OFF]`, R — `ORL-020 [PRODUCT]`: this must be a structured, drug-specific, versioned instruction, never blank and never generic); Vomited-dose instruction; What to do if a dose is late. |
| **Fields — Dispensing** | Quantity to dispense (numeric, R — with `[DERIVED]` days-supply calculation `CALC-161`); Days supply `[DERIVED]`; Refills authorised (numeric); Refill interval; **Dispense-to-next-review constraint** `[DERIVED]` — the system must not authorise a supply extending beyond the next monitoring review without an explicit override (`ORL-030 [PRODUCT]`); Dispensing location; Patient collection or delivery. |
| **Fields — Monitoring** | Required baseline investigations (auto from master, with status); Ongoing monitoring schedule (repeating: test, frequency, next due `[DERIVED]`); Clinical review interval; Specific monitoring for this drug (e.g. blood pressure, ECG, ophthalmic, dermatological, thyroid — `[CCA CONFIG]` per drug); Toxicity thresholds for dose modification `[CCA CONFIG]` displayed for reference. |
| **Fields — Interactions** | Interaction check results (drug–drug including OTC and herbal, drug–food including specific foods `[CCA CONFIG]`, drug–disease); Disposition per alert; Medications to avoid (listed for the patient sheet). |
| **Tables** | Dose history (date, dose, reason for change, prescriber); dispensing history (date, quantity, days supply, dispensed by, collected by); monitoring schedule with due/overdue status; interaction alerts. |
| **Calculated** | Calculated dose; achievable-dose combination; days supply; planned end date; next monitoring due; cumulative exposure where tracked; adherence-expected pill count `[DERIVED]` for reconciliation at review (`CALC-162`). |
| **Actions** | Select drug · Calculate dose · Check strengths · Check interactions · Set schedule · Set monitoring · Preview patient instructions · Save draft · **Sign and send to pharmacy** · Print prescription. |
| **Chips** | Prescription status (Draft / Signed / Dispensed / Active / On hold / Discontinued / Completed); monitoring due/overdue; supply remaining `[DERIVED]`; dose modified. |
| **Alerts** | **Hard stop:** dose not achievable from available strengths without an explicit "prescriber accepts splitting/rounding" action; missed-dose instruction absent; baseline monitoring not done where required; supply authorised beyond the next review without override. **Warning:** interaction present; monitoring overdue; drug requires patient education not yet delivered. |
| **Sign/approve** | Prescriber signature; values frozen (`GEN-SIG-003`). |
| **Amendment/version** | Dose changes create a new prescription version with reason and effective date; prior versions retained; the patient's instruction sheet is regenerated and re-issued, with the re-issue recorded (`ORL-040 [PRODUCT]`). |
| **Downstream** | Pharmacy dispensing queue; counselling task; monitoring orders; Navigator; adherence review schedule; Treatment Summary. |
| **Print/export** | Prescription; patient instruction sheet (`PTP-140`); dosing calendar for the patient. |

## C.14.2 · `SCR-ORL-002` — Oral Therapy Counselling
**Role:** Pharmacist or nurse.
**Checklist fields (each individually recorded, `[CCA CONFIG]` content, product-defined structure):** drug name and purpose; dose and how many units per dose; timing; food instruction; what to do if a dose is missed; what to do if vomited; storage; handling precautions for the patient and household; expected side effects and their management; **red-flag symptoms and thresholds requiring urgent contact**; monitoring appointments and why they matter; interactions and what to avoid (including OTC and herbal); contraception and pregnancy; refill process; who to contact and 24-hour number; adherence importance and strategies (pill box, alarms, diary).
**Per item:** covered (Y/N), material issued (version), patient/carer understanding (dropdown: Full / Partial — reinforcement planned / Not understood — re-counsel), teach-back performed.
**Fields:** Counselled by, date/time, duration, language, interpreter, carer present, adherence aids provided, patient diary issued.
**Downstream:** Education log; adherence review schedule; dispensing gate — **ORL-050 [PRODUCT]**: first dispensing is blocked until counselling is recorded.
**Print/export:** Oral Therapy Counselling Note; patient information pack.

## C.14.3 · `SCR-ORL-003` — Dispensing & Refill
**Role:** Pharmacist.
**Fields:** Prescription (link, with version); Quantity dispensed; Batch/lot and expiry; Days supply `[DERIVED]`; Dispensed by; Checked by; Date; Collected by (patient/carer name and relationship); Counselling status (read-only gate); Monitoring status (read-only gate — **ORL-060 [PRODUCT]**: refill is blocked where required monitoring is overdue, with a clinician override path); Adherence review status; Returned/unused quantity from previous supply (numeric — the basis for pill-count adherence); Expected remaining `[DERIVED]` vs actual returned `[DERIVED]` discrepancy (`CALC-162`); Next refill due `[DERIVED]`.
**Alerts:** Refill early (suggests over-use or loss) or late (suggests non-adherence) beyond tolerance `[CCA CONFIG]`; monitoring overdue; prescription expired; dose changed since last dispense (requires re-counselling).
**Downstream:** Adherence record; supply tracking; clinician alert on adherence discrepancy.

## C.14.4 · `SCR-ORL-004` — Adherence & Toxicity Review
**Role:** MO, pharmacist or nurse per `[CCA CONFIG]`.
**Sections:** Adherence · Toxicity · Monitoring results · Dose decision · Next supply · Sign.
**Fields — Adherence:** Method of assessment (multiselect: patient report, pill count, diary, refill history, electronic monitoring); Doses prescribed in period `[DERIVED]`; Doses reported taken; Doses missed (numeric + reasons multiselect: forgot, side effects, cost, supply, felt unwell, felt well, confusion about instructions, other); **Adherence percentage** `[DERIVED]` (`CALC-163` — with the method stated, since methods disagree); Pill count discrepancy; Barriers identified; Interventions.
**Fields — Toxicity:** structured review linked to `SCR-TOX-002`; drug-specific toxicity checklist `[CCA CONFIG]`.
**Fields — Monitoring:** results due and received, with values and dates; overdue items.
**Fields — Dose decision:** Continue unchanged / Reduce (with %, new dose, reason) / Interrupt (with duration and restart criteria — structured per `ORD-140`) / Restart after interruption (with date and dose) / Discontinue (with reason and date); Next review date; Next supply authorised.
**Alerts:** Adherence below configured threshold `[CCA CONFIG]`; toxicity grade requiring protocol-defined action; monitoring overdue.
**Downstream:** New prescription version where dose changed; dispensing authorisation; toxicity record; Navigator; Treatment Summary.
**Print/export:** Oral Therapy Review / Refill Note; Adherence Review record.

## C.14.5 · `SCR-ORL-005` — Oral Therapy Hold / Restart / Discontinue
Mirrors `SCR-ORD-006` in structure, with oral-specific fields: interruption start date, last dose taken date, restart criteria (structured), restart date, restart dose (same/reduced), remaining supply disposition, patient instruction issued on holding, patient contacted and understanding confirmed.
**ORL-070 [PRODUCT]** — because the patient administers the drug, a hold decision is not effective until the patient has been contacted and the contact recorded. The hold record must carry the patient-notification fields and must remain flagged `HOLD NOT COMMUNICATED` until they are completed.

---

## END OF DOCUMENT 5

**Continues in Document 6 — PART C, Section 4:** C.15 Radiation Oncology (consultation → prescription → simulation → contouring → planning → approval) · C.16 Radiation Physics (QA and release) · C.17 Radiation Technologist (setup, imaging, delivery, OTV support, completion).
