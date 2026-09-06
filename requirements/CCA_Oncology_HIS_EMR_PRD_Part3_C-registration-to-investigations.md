# CCA CANCER CARE — ONCOLOGY HIS + EMR
# MASTER FUNCTIONAL & CLINICAL PRODUCT REQUIREMENT INVENTORY
## Document 3 of N — PART C (Screen-by-Screen), Section 1
### C.1 Registration · C.2 Intake · C.3 Nurse Navigation · C.4 Medical Oncology Consultation · C.5 Diagnosis & Staging · C.6 Investigations

---

## C.0 — SCREEN SPECIFICATION CONVENTIONS

### C.0.1 The screen template
Every screen in Parts C.1–C.26 is specified against the same 20 dimensions. Where a dimension is genuinely not applicable, it is stated as "n/a" with a reason rather than omitted.

`SCREEN ID · NAME · ROLE(S) · NAVIGATION · PURPOSE · HEADER · SECTIONS · FIELDS · TABLES · DROPDOWNS · CALCULATED · ACTIONS · CHIPS · ALERTS · CONDITIONAL LOGIC · READ-ONLY · SIGN/APPROVE · AMENDMENT/VERSION · COMPARISON VIEW · POST-SIGNATURE · DOWNSTREAM · EMPTY / LOADING / ERROR / BLOCKED / SUPERSEDED STATES · PRINT/EXPORT`

### C.0.2 Universal state behaviour `[PRODUCT]`
Stated once; applies to every screen without restatement.

| State | Required behaviour |
|---|---|
| **Loading** | Skeleton placeholders matching the final layout — never a blank page or a spinner over an empty canvas. Patient header loads first and independently of body content. Clinically critical elements (allergy banner, alerts) must render before any input control becomes interactive — **GEN-STA-001 [PRODUCT]**: a user must never be able to enter data on a patient whose allergy banner has not yet loaded. Partial-load indicators per card where a data source is slow. Timeout at a configured interval `[CCA CONFIG]` converts to error state. |
| **Empty** | Explains what would appear, why it is empty (no data vs no permission vs not yet applicable), and the action that would populate it. Never "No records found" alone. Distinguishes "no data recorded" from "recorded as none" — clinically distinct (see NKDA, `INT-NUR-300`). |
| **Error** | States what failed, whether the user's unsaved data is retained (it must be), whether the failure is retryable, a retry action, an error reference for support, and — where the failure affects a clinical decision — an explicit statement that data may be incomplete. Never a raw exception. **GEN-STA-002 [PRODUCT]**: a data-retrieval failure on a safety-relevant panel (allergies, labs used for readiness, active orders) must block dependent actions rather than silently render as empty. |
| **Blocked** | Explains the blocking rule in clinical language, names the blocking item and its source record, names the role who can unblock, and offers the escalation action. Blocked ≠ disabled-with-no-explanation. |
| **Superseded** | Persistent `SUPERSEDED` chip, muted styling, banner naming the superseding record with a link, read-only, all actions removed except View/Print/Compare. Never hidden. |
| **Draft** | Persistent `DRAFT — NOT SIGNED` banner, watermark on any print output, excluded from all downstream consumption and from all worklists that imply completion. |
| **Offline/degraded** | Read-only cached view per `GEN-DTM-001`; write actions disabled with explanation. |

### C.0.3 Universal print/export behaviour `[PRODUCT]`
Every print/export carries the header defined in `GEN-EXP-001` plus: document status (Draft/Signed/Amended/Superseded), version number, generation timestamp, generating user, and — for any document containing calculated values — the calculation inputs and their source dates.

---

# C.1 — REGISTRATION SCREENS

## C.1.1 · `SCR-REG-001` — Front Desk Home / Appointment Worklist

| Dimension | Specification |
|---|---|
| **Role(s)** | Front Desk / Registration. Read-only variant for Operations Manager. |
| **Navigation** | Landing screen on login for the Front Desk role. Also from global nav → Front Desk. |
| **Purpose** | Single operational surface for the day: who is expected, who has arrived, who is waiting, what is blocking each patient's progress. |
| **Header** | No patient header (list screen). Facility/location selector, date selector (default today), user + role, counts strip: Expected / Arrived / Waiting / With clinician / Completed / No-show / Cancelled. |
| **Sections** | Tab bar: `Today's Appointments` · `Live Queue` · `Registration Pending` · `Scheduling`. Filter rail (collapsible, left). Result table (centre). Detail preview drawer (right, on row hover/select). |
| **Fields (filter rail)** | Date / date range (date picker); Department (multiselect); Clinician (multiselect, dependent on Department); Visit type (multiselect); Appointment status (multiselect); Payer (multiselect); Financial clearance (multiselect); Location (multiselect); Waiting-time threshold (numeric, minutes); toggles: Arrived-not-seen only, No-shows only, Walk-ins only, Has pending action. Free-text search (name / UHID / phone / national ID / appointment no.). |
| **Table columns** | Per B.1.B View 1 — Appointment time · Patient name · UHID · Age `[DERIVED]` · Sex · Contact (masked per `[CCA CONFIG]`) · Visit type · Department · Clinician · Appointment status · Check-in time · Waiting time `[DERIVED]` · Current location · Payer · Financial clearance · Pending action · Alerts · Referring dept/clinician · Prior visit date · Row actions. |
| **Dropdowns** | Department (`[CCA CONFIG]` facility master); Clinician (derived from Department + roster); Visit type (**product-defined backbone**: New / Follow-up / Treatment / Procedure / Investigation-only / Teleconsultation / MDT-related / Report-review; `[CCA CONFIG]` extensions); Appointment status (**product-defined, state-machine controlled — not freely selectable**); Payer (`[CCA CONFIG]`); Financial clearance (product-defined); Location (`[CCA CONFIG]`). |
| **Calculated** | Age (Part E `CALC-001`); Waiting time = now − check-in time (`CALC-002`); counts strip aggregates; no-show derivation = appointment time + configured grace `[CCA CONFIG]` elapsed with no check-in (`CALC-003`) — **system proposes `No-show`; Front Desk confirms**. |
| **Actions** | Row: Check in · Reschedule · Cancel · Print appointment slip · Send reminder · Collect payment · Route to Financial Counsellor · Print wristband/label · Open encounter. Screen: New registration · New walk-in appointment · Export list · Refresh · Save view · Print day list. |
| **Chips** | Appointment status (colour per `GEN-WLQ-003`); Visit type (neutral); Financial clearance (green cleared / amber pending / red rejected / grey not required); Pending action (amber, stacked with count); Waiting time (green→amber→red at configured thresholds `[CCA CONFIG]`). |
| **Alerts/banners** | Operational only: interpreter required, mobility assistance, isolation precaution, confidential record, "allergy recorded — see clinical staff" (`REG-FD-040`). Screen-level banner if the roster is unpublished for the selected date, or if a clinician is marked absent with patients still booked. |
| **Conditional logic** | Clinician filter disabled until Department chosen. Check-in disabled if: appointment cancelled, patient already checked in to another open encounter today (offers "view open encounter"), or financial clearance is `Rejected` and policy blocks check-in `[CCA CONFIG]`. Send-reminder disabled if no consented contact method. |
| **Read-only** | All clinical columns; Age; Waiting time; Appointment status (changed only via actions, never typed). |
| **Sign/approve** | None — no clinical signature on this screen. |
| **Amendment/version** | n/a (live list). Underlying appointment changes are versioned on the appointment object. |
| **Comparison view** | n/a. |
| **Post-signature** | n/a. |
| **Downstream** | Check-in → opens Encounter, places patient in **Intake queue** (`SCR-INT-001`) and in the destination clinician's clinic worklist. Reschedule/cancel → notification to patient + Navigator if pathway milestone affected. Route to Financial Counsellor → `SCR-FIN-001` queue entry. |
| **Empty state** | "No appointments for [date] in [department]." Offers: change date, clear filters, book appointment, view walk-ins. |
| **Print/export** | Day list (columns as displayed, respecting privacy config), queue board output. |

---

## C.1.2 · `SCR-REG-002` — New Patient Registration

| Dimension | Specification |
|---|---|
| **Role(s)** | Front Desk. HIM (correction rights). |
| **Navigation** | `SCR-REG-001` → New registration; or global "+ Register patient"; or from a failed search ("no match — register new"). |
| **Purpose** | Create a unique, verified patient identity and issue a UHID. |
| **Header** | None until UHID issued; then a provisional administrative header appears. |
| **Sections** | 1 Identity · 2 Demographics · 3 Contact · 4 Next of Kin / Emergency · 5 Identification documents · 6 Payer · 7 Referral source · 8 Consents · 9 Preferences & needs · 10 Duplicate check result. |
| **Fields** | **Identity:** Title (dropdown); Given name (text, R); Middle name (text, O); Family name (text, R); Preferred name (text, O); Name in local script (text, O `[CCA CONFIG]`); Date of birth (date, R — with "estimated DOB" checkbox and age-entry fallback, which sets DOB precision flag); Age at registration `[DERIVED]`, read-only; Sex (dropdown, R — **product-defined**: Male / Female / Other / Unknown, `[CCA CONFIG]` extensions); Gender identity (dropdown, O `[CCA CONFIG]`); Marital status (dropdown, O); Photograph (capture/upload, O `[CCA CONFIG]`). **Demographics:** Nationality; Religion `[CCA CONFIG]`; Occupation; Education level; Ethnicity `[CCA CONFIG]` — all dropdowns, optionality `[CCA CONFIG]`. **Contact:** Mobile (text, R, format-validated); Alternate phone; Email; Preferred contact method (dropdown); Consent to contact by SMS/email/call (checkboxes, each timestamped); Address line 1/2, area, city, district, state, postcode, country (R per `[CCA CONFIG]`). **NOK:** Name (R); Relationship (dropdown, R); Phone (R); Address; Is legal representative (checkbox); Authorised to receive clinical information (checkbox + scope `[CCA CONFIG]`). **ID documents:** Document type (dropdown `[CCA CONFIG]`); Number; Issuing authority; Expiry; Verified (checkbox) + verification method + verified by/at; Scan attachment. **Payer:** per `SCR-FIN-001` embedded panel. **Referral:** Source (dropdown — product-defined: Self / GP / Specialist / Hospital transfer / Screening programme / Internal department / Emergency / Other); Referring facility; Referring clinician; Referral date; Referral reason (text); Referral document upload; Suspected cancer flag (checkbox → routes to Navigator). **Consents:** Registration/treat consent (`[CCA CONFIG]` wording, versioned) — status, version, obtained by, date/time, method (in person/electronic/telephone with witness), signature capture, witness where required; Data privacy consent; Consent to photography `[CCA CONFIG]`. **Preferences:** Preferred language (dropdown); Interpreter required (checkbox + language); Mobility assistance (dropdown); Communication needs (multiselect); Cultural/religious requirements (text). |
| **Tables** | ID documents (type, number, expiry, verified, attachment, actions); Payer list (payer, policy, validity, priority, verified); Duplicate candidates (see below). |
| **Dropdowns** | All above. Sources: product-defined where marked; `[CCA CONFIG]` masters otherwise; national ID document types `[CCA CONFIG]`. |
| **Calculated** | Age `[DERIVED]` from DOB (`CALC-001`); Duplicate match score `[DERIVED]` (`CALC-004`) — algorithm product-defined, threshold `[CCA CONFIG]`. |
| **Actions** | Check for duplicates (auto-fires on name+DOB+phone entry, and again on save) · Save draft · Register & issue UHID · Register & book appointment · Register & check in · Print wristband · Print registration slip · Cancel. |
| **Chips** | Duplicate risk (green none / amber possible n / red probable n); Verification status per document; Consent status. |
| **Alerts** | **Hard stop:** save blocked while a `probable` duplicate is unresolved — user must select "same patient — use existing" or "different patient — confirm with reason" (`REG-FD-050`: Front Desk may create, never merge). **Warning:** missing mandatory identity document per `[CCA CONFIG]`; DOB estimated; contact number format unverified; patient age implies paediatric pathway `[CCA CONFIG]`. |
| **Conditional logic** | Estimated-DOB checkbox → enables age-in-years entry and sets precision flag on the record, displayed forever alongside age. Interpreter checkbox → language required. NOK "authorised to receive information" → scope selector required. Suspected-cancer flag → Navigator referral panel appears. Sex/age → conditional visibility of pregnancy-relevant downstream screening (not asked here). |
| **Read-only** | UHID (system-issued); Age; Duplicate score; audit fields. |
| **Sign/approve** | Consent artifacts are signed (patient signature + staff attestation). Registration itself is attributed, not signed. |
| **Amendment/version** | Demographic changes create a new version of the demographic record with prior values retained and viewable (`SCR-REG-004`). UHID is never editable. |
| **Comparison view** | Duplicate resolution shows candidate record vs entered data field-by-field with match/mismatch marking. |
| **Post-signature** | Consent artifacts become immutable, version-stamped, and appear in the patient's document list and in every consent-status chip across the product. |
| **Downstream** | UHID issued → patient searchable; Suspected-cancer flag → **Navigator queue** (`SCR-NAV-001`); Payer entered → **Financial Counsellor queue** if verification required; Registration → optional immediate appointment booking (`SCR-REG-005`). |
| **Empty/Loading/Error** | Standard. Error on UHID issuance must not lose entered data and must not issue a partial identity — **REG-FD-070 [PRODUCT]**: UHID issuance is atomic. |
| **Blocked** | Unresolved probable duplicate; missing mandatory field; consent version not configured (`[CCA CONFIG]` gap) — the last must produce an explicit configuration error naming the missing master, not a silent failure. |
| **Print/export** | Registration slip; wristband/label (name, UHID, DOB, sex, barcode, allergy indicator); consent copy for patient. |

---

## C.1.3 · `SCR-REG-003` — Duplicate Resolution

**Role:** Front Desk (identify + request), HIM (execute merge — `HIM-010`).
**Navigation:** From `SCR-REG-002` duplicate alert; from HIM data-quality worklist; from search results showing possible duplicates.
**Purpose:** Prevent two records for one patient and prevent merging two different patients.
**Header:** Side-by-side administrative headers of both candidate records.
**Sections:** Match summary · Field-by-field comparison · Clinical activity summary per record · Decision · Merge execution (HIM only).
**Table — field comparison:** Field · Record A value · Record B value · Match (exact/fuzzy/mismatch) · Weight in score.
**Table — clinical activity per record:** Encounter count, first/last activity date, documents count, orders count, results count, cancer episodes count, active treatment y/n. **REG-FD-080 [PRODUCT]** — a merge candidate with an active treatment order, an active RT course or an in-progress admission requires clinical sign-off in addition to HIM authorisation.
**Calculated:** Match score `[DERIVED]`; activity counts `[DERIVED]`.
**Actions:** Front Desk — Mark as same patient (raise merge request) · Mark as different (with reason) · Escalate. HIM — Execute merge (dual authorisation) · Reject request · Unmerge (reversible, audited).
**Chips:** Match confidence; Active-treatment warning; Merge status (Requested / Under review / Approved / Executed / Rejected / Reversed).
**Alerts:** Hard stop on merging records with conflicting sex or DOB beyond tolerance without explicit override + reason; hard stop on merge by a single user (dual authorisation required).
**Downstream:** Merge → all clinical records re-pointed, surviving UHID recorded, retired UHID retained as an alias and searchable, notification to all clinicians with open orders on either record.
**Print/export:** Merge audit record.

---

## C.1.4 · `SCR-REG-004` — Patient Administrative Profile

**Role:** Front Desk (edit contact/payer/preferences), HIM (edit identity), all roles (view subset).
**Navigation:** From any worklist row → patient → Administrative profile tab; from search.
**Purpose:** Maintain the non-clinical patient record and view its history.
**Sections:** Identity (HIM-editable only) · Contact · Address history · NOK · Documents · Payers · Preferences · Consents · Encounter history · Alias/merge history · Change log.
**Tables:** Encounter history (date, type, department, clinician, outcome, documents); Consent register (type, version, status, obtained by, date, expiry, withdrawal date/reason); Change log (field, old value, new value, changed by, role, date/time, reason).
**Conditional logic:** Identity fields render read-only for Front Desk with an explanatory tooltip and a "request correction" action routing to HIM.
**Amendment/version:** Every change versioned; prior values always viewable; consent withdrawal is a new consent-status event, never a deletion — **REG-FD-090 [PRODUCT]**.
**Downstream:** Contact change → re-issues pending reminders; consent withdrawal → suppresses the corresponding communication channel and alerts Navigator.

---

## C.1.5 · `SCR-REG-005` — Scheduling Calendar & Booking

| Dimension | Specification |
|---|---|
| **Role(s)** | Front Desk; Radiology Coordinator (imaging slots); Day Care charge nurse (chair slots); RT scheduling (linac slots); Surgical scheduling (theatre). Cross-visibility read-only. |
| **Navigation** | `SCR-REG-001` → Scheduling tab; from Check-out; from a clinician's "book follow-up" action; from a signed treatment order's "book next cycle". |
| **Purpose** | Allocate finite resources (clinician time, chairs, machines, theatres, rooms) against clinical requirements and protocol intervals. |
| **Header** | Resource selector; date range; view mode (day/week/resource/patient). Patient header appears when booking for a specific patient. |
| **Sections** | Resource calendar grid · Slot detail panel · Patient requirement panel · Conflict panel. |
| **Fields (booking)** | Patient (search/select, R); Appointment type (dropdown, R); Department (R); Resource (clinician/chair/machine/room, R); Date (R); Start time (R); Duration (numeric minutes, defaulted from appointment type `[CCA CONFIG]`, editable with reason); Priority (dropdown); Reason for visit (text/coded); Linked order (select — e.g. the imaging order or treatment order this appointment fulfils); Preparation set (dropdown `[CCA CONFIG]`, auto-applied by appointment type); Interpreter required (auto from profile); Transport required; Isolation precautions (auto); Accompanying person; Notes to the receiving department; Notification method(s). |
| **Tables** | Slot grid (resource × time); Waitlist (patient, requested type, requested by, urgency, requested-by date, days waiting `[DERIVED]`); Conflicts. |
| **Dropdowns** | Appointment type (`[CCA CONFIG]` with product-defined categories); Priority (product-defined: Routine / Urgent / Emergency / Protocol-driven); Preparation set `[CCA CONFIG]`; Cancellation reason (product-defined + `[CCA CONFIG]`). |
| **Calculated** | Expected duration `[DERIVED]` — for Day Care, from the regimen's summed administration time + premedication + observation (`CALC-020`); Next-cycle due date `[DERIVED]` from last administration + cycle length (`CALC-021`); Slot utilisation %; Days waiting. |
| **Actions** | Book · Book series (for a full course: n cycles at cycle-length intervals, or n fractions on consecutive treatment days) · Reschedule · Cancel · Add to waitlist · Overbook (permission-gated, reason required) · Block resource · Print schedule · Notify patient. |
| **Chips** | Slot status (Available / Held / Booked / Blocked / Overbooked); Booking status; Protocol-interval compliance (green within window / amber outside window / red outside window with no reason). |
| **Alerts** | **Warning:** booking a treatment appointment outside the protocol interval window `[CCA CONFIG]`; booking before required readiness labs would be available; booking an RT fraction on a non-treatment day; booking surgery inside the configured post-neoadjuvant interval `[CCA CONFIG]`. **Hard stop:** double-booking a resource without overbook permission; booking a Day Care chair for a regimen whose duration exceeds remaining unit hours `[CCA CONFIG]`. |
| **Conditional logic** | Series booking enabled only when a signed treatment plan or RT prescription exists. Preparation set auto-applies and can only be removed with reason. Linked-order field mandatory for investigation and treatment appointments — **REG-FD-100 [PRODUCT]**: treatment and investigation appointments must be traceable to the clinical order that justifies them. |
| **Read-only** | Resource availability derived from roster/machine masters; expected duration (recalculated, overridable with reason). |
| **Downstream** | Booking → patient's appointment list, receiving department's worklist, patient notification, Navigator pathway milestone update, Financial Counsellor if authorisation needed. Cancellation → Navigator alert if a pathway milestone is at risk. |
| **Print/export** | Patient appointment schedule (full course); resource day sheet; waitlist report. |

---

## C.1.6 · `SCR-REG-006` — Check-in

**Role:** Front Desk. **Navigation:** `SCR-REG-001` row action, or barcode scan of appointment slip.
**Purpose:** Open the encounter and release the patient into the clinical queue.
**Header:** Administrative header + today's appointment summary.
**Sections:** Identity verification · Appointment confirmation · Administrative checklist · Queue placement.
**Fields:** Identity verified by (auto), method (dropdown — product-defined: Photo ID / Wristband barcode / Verbal two-identifier / Biometric `[CCA CONFIG]`); Attending in person / telehealth (radio); Arrival time (datetime, defaults now, editable); Accompanying person name/relationship; Contact details confirmed (checkbox, forces review if last confirmed > `[CCA CONFIG]` interval); Payer confirmed (checkbox); Consent current (auto-checked; if expired/absent, prompts capture); Documents outstanding (checklist); Payment collected (amount, method, receipt); Destination queue (dropdown: Intake / Direct to clinician / Day Care / Radiology / Phlebotomy); Location assigned.
**Calculated:** Encounter number issued; queue position.
**Chips:** Consent status; Payment status; Document completeness.
**Alerts:** Warning if consent expired, contact stale, documents missing. Hard stop if the appointment is cancelled or belongs to a different date without override.
**Downstream:** Encounter opened → **Intake worklist** (`SCR-INT-001`) and clinician clinic worklist; live queue board updated; waiting-time clock starts.
**Print/export:** Queue token; label sheet.

---

## C.1.7 · `SCR-REG-007` — Live Queue Board
**Role:** Front Desk (control), all clinical areas (view), public display (restricted variant).
**Purpose:** Real-time visibility and flow control.
**Sections:** Per-department lanes; clinician status strip; public-display configuration.
**Table columns:** Token/position, patient (identifiable or tokenised per `[CCA CONFIG]`), visit type, waiting time `[DERIVED]`, location, status, assigned room.
**Actions:** Call next · Call specific · Recall · Mark absent · Reorder (permission-gated, reason captured) · Send to another queue · Update location.
**Alerts:** Waiting time exceeding threshold `[CCA CONFIG]`; patient called twice without response; clinician idle with patients waiting.
**REG-FD-110 [PRODUCT]** — the public display variant must be configurable to show tokens/initials only and must never display department names that disclose diagnosis (e.g. it must be possible to display "Clinic 3" rather than "Oncology").

---

## C.1.8 · `SCR-REG-008` — Document Capture
**Role:** Front Desk, HIM, any clinical role (clinical documents).
**Fields:** Document type (dropdown `[CCA CONFIG]` — product-defined categories: Identity / Insurance / Referral / External report — imaging / External report — pathology / External report — discharge / Consent / Correspondence / Other); Document date; Source facility; Author; Description; Cancer episode linkage (required for clinical documents — **GEN-EPI-002**); Confidentiality level; Attachment (scan/upload, multi-page).
**Actions:** Capture · Upload · Classify · Link to episode · Route for clinical review · Mark superseded.
**Downstream:** External pathology/imaging documents → route to the treating clinician's Results Inbox with an "external document — requires review and reconciliation" flag; if designated as a response-assessment baseline, routes to Radiology (`RAD-040`).

---

## C.1.9 · `SCR-REG-009` — Check-out & Next Appointment
**Role:** Front Desk.
**Purpose:** Close the encounter, ensure the next step is booked, and hand the patient their instructions.
**Sections:** Encounter closure · Outstanding actions from the visit · Next appointments · Instructions issued · Payment.
**Fields:** Departure time; Outcome (dropdown: Seen and discharged / Seen — follow-up booked / Seen — admitted / Left without being seen / Deferred); Orders raised during visit (read-only list with booking status per order); Next appointments (auto-proposed from clinician's plan, editable); Instructions issued (checklist with versions); Payment/balance.
**Alerts:** Warning if an order placed during the visit has no appointment booked; warning if a follow-up interval specified by the clinician has not been honoured — **REG-FD-120 [PRODUCT]**: the clinician's requested review interval is a structured field, and check-out must compare the booked date against it.
**Downstream:** Closes encounter; unbooked orders → Navigator loop-closure queue; instruction issuance recorded to the patient education log.

---

# C.2 — INTAKE SCREENS

## C.2.1 · `SCR-INT-001` — Intake Worklist
**Role:** Intake Nurse; Day Care nurse (treatment-day subset); charge nurse.
**Navigation:** Landing screen for the Intake Nurse role.
**Purpose:** Show which arrived patients need which intake dataset, and in what order.
**Header:** Location selector, date, counts strip (Awaiting intake / In progress / Complete / Escalated / Deferred).
**Table columns:** Per B.2.B, including the **Required intake set** chip stack `[DERIVED]` (`CALC-030` — derived from visit type + treatment modality + treatment-day status + protocol prerequisites `[CCA CONFIG]`).
**Actions:** Start intake · Record vitals only · Record weight only · Escalate · Defer with reason · Print label · Open previous intake.
**Conditional logic:** "Record weight only" available only where a weight is the sole outstanding item. Treatment-day rows are visually distinct and sorted ahead of routine rows when the Day Care unit is in context.
**Alerts:** Weight overdue for a patient scheduled for dosing today; vitals abnormal from a prior same-day reading; escalation unacknowledged beyond threshold `[CCA CONFIG]`.
**Empty state:** distinguishes "no patients have arrived yet" from "all intakes complete" — different messages, different actions.

---

## C.2.2 · `SCR-INT-002` — Intake Assessment (master screen)

| Dimension | Specification |
|---|---|
| **Role(s)** | Intake Nurse; Day Care nurse; Inpatient nurse (variant). |
| **Navigation** | `SCR-INT-001` → Start intake. |
| **Purpose** | Capture the complete, attributable clinical baseline for this visit. |
| **Header** | Full Intake Nurse header per B.2.C — identifiers, alert banners with substance-level allergy, episode, treatment status (regimen + cycle/day or fraction n/m or POD n), last weight/height/BSA with dates and staleness, last vitals, key labs, active toxicities, isolation, fall risk. |
| **Sections (accordion, progress-tracked)** | 1 Anthropometrics · 2 Vital signs · 3 Allergies · 4 Medications · 5 Performance status · 6 Symptom & toxicity screen · 7 Infection/isolation screen · 8 Pregnancy/lactation screen · 9 Fall risk · 10 Nutrition · 11 Distress · 12 Pain · 13 Vascular access · 14 Nurse narrative · 15 Escalation · 16 Sign. |
| **Fields** | Every field per B.2.D `INT-NUR-100` through `INT-NUR-395`, with the exact input types, units, validations, method qualifiers and delta checks specified there. |
| **Tables** | Previous values panel per measurement (last 5 values: value, unit, date/time, method, recorder) with expand-to-trend; Medication reconciliation table (drug, strength, dose, route, frequency, indication, source, status, action taken: continued/held/stopped/changed/unknown); Allergy table; Symptom screen table (symptom, present, severity, onset, change since last visit, action). |
| **Dropdowns** | Height method; weight method; weight condition qualifier; BP site/position; cuff size; temperature site; oxygen delivery device; PS instrument + score; symptom severity; allergy substance (coded, `[CCA CONFIG]` catalogue) / reaction type (product-defined) / manifestation (`[CCA CONFIG]`) / severity (`[CCA CONFIG]`) / certainty (product-defined); medication source and reconciliation action (product-defined); isolation type (`[CCA CONFIG]`); pregnancy applicability reason (product-defined); vascular access type/site/patency (product-defined + `[CCA CONFIG]`); escalation recipient role; defer reason. |
| **Calculated** | BMI (`CALC-010`); BSA (`CALC-011`) with named formula; MAP (`CALC-012`) where configured; weight delta absolute and % since last and since order weight (`CALC-013`); fall-risk total and band (`CALC-014`); nutrition score and band (`CALC-015`); distress score (`CALC-016`); EWS where configured (`CALC-017`); age (`CALC-001`). Each displays inputs, source timestamps and formula on expand. |
| **Actions** | Save section · Save all (draft) · Carry forward previous height (explicit, records method) · Add allergy · Reconcile medication · Escalate · Defer · Print intake summary · **Sign intake**. |
| **Chips** | Per-section completion (Not started / In progress / Complete / Not applicable — reason); Required-vs-optional per field; Staleness on carried-forward values; Delta-check triggered; Out-of-range; Critical value. |
| **Alerts** | **Hard stop on sign:** required field for this visit type missing; weight absent on a treatment day; NKDA not affirmatively asserted and no allergies listed. **Override-with-reason:** value outside plausibility bounds; weight delta beyond threshold on a treatment day (`INT-NUR-111`) — must acknowledge that the active order is being flagged for dose review. **Warning:** BP recorded on a limb flagged for lymphoedema (`INT-NUR-204`); temperature at/above configured febrile threshold with a neutropenia risk flag; carried-forward height older than configured validity. |
| **Conditional logic** | Pregnancy section renders only per sex/age configuration and can be marked not-applicable with a structured reason. Oxygen sub-fields render only when "on oxygen". Glucose renders when diabetes flag or steroid-containing regimen. Vascular access section renders for patients with a device or scheduled for infusion. Symptom screen item set varies by current treatment modality `[CCA CONFIG]`. Fall/nutrition/distress instruments render per configured triggers. |
| **Read-only** | All derived values; header data; previous values; the required-set derivation (with an explanation tooltip naming the rule). |
| **Sign/approve** | Single nurse signature with re-authentication (`GEN-SIG-002`). Countersignature configurable `[CCA CONFIG]`. |
| **Amendment/version** | Post-signature correction by addendum or amendment with reason; original values remain visible; **any downstream consumer that used a changed value is notified** — specifically, if a weight used by an unsigned order changes, the order recalculates; if it was used by a signed order, the order displays both values (`INT-NUR-132`). |
| **Comparison view** | Every measurement shows current vs previous inline; expand shows the full series with treatment-event overlay. |
| **Post-signature** | Values become consumable by readiness, dosing, RT OTV, nutrition and reporting. Intake Note is generated and appears in the document list. |
| **Downstream** | Signed intake → patient status advances in the clinician's clinic worklist ("Intake complete"); escalations → named clinician's task inbox with acknowledgement tracking; abnormal screens → automatic referral proposals (dietitian, psycho-oncology, falls team) requiring nurse or clinician confirmation, never auto-referral — **INT-NUR-400 [PRODUCT]**. |
| **Blocked state** | Blocked if no open encounter, if the patient has no active episode and the visit type requires one, or if a device integration returns a value that fails validation (must fall back to manual entry, never accept an implausible device value silently — **INT-NUR-401 [PRODUCT]**). |
| **Print/export** | Intake / Nursing Assessment Note (full sections per Part F). |

---

## C.2.3 · `SCR-INT-003` — Vitals Quick-Entry
**Role:** Intake, Day Care, Inpatient, RT nursing.
**Navigation:** Row action from any worklist; from the observation flowsheet; from an active infusion record ("record vitals now").
**Purpose:** Rapid, repeated capture of a vitals set without opening the full intake screen.
**Fields:** The `INT-NUR-200` series only, plus context field: reason for observation (dropdown — product-defined: Routine / Pre-administration / During administration — scheduled / During administration — unscheduled / Post-administration / Reaction assessment / Escalation / Pre-discharge).
**Calculated:** EWS where configured; deltas from previous set.
**Downstream:** When entered during an active infusion, the vitals set is **linked to that administration record** so the infusion note renders observations in sequence with the drug timeline — **MAR-030 [PRODUCT]**.
**Chips:** Scheduled/unscheduled; overdue observation.
**Alerts:** Critical value → escalation prompt with named recipient; reaction-suggestive pattern during infusion `[CCA CONFIG]` → prompts the reaction screen.

---

## C.2.4 · `SCR-INT-004` — Allergy & Adverse Reaction Management
**Role:** All clinical roles (add/edit per permission); pharmacist (verify).
**Navigation:** From the allergy banner (click), intake, pharmacy verification, order entry, admission.
**Purpose:** Maintain the safety-critical allergy list, including oncology-specific infusion reaction history.
**Sections:** Active allergies · Inactive/refuted · Prior infusion reactions · NKDA assertion · History.
**Fields per allergy:** Substance (coded, R); Substance class (auto-derived where the catalogue supports it — enables class-level checking); Reaction type (product-defined: Allergy / Intolerance / Adverse reaction / Unknown); Manifestations (multiselect `[CCA CONFIG]`); Severity (`[CCA CONFIG]`); Onset date; Certainty (product-defined: Confirmed / Suspected / Refuted / Unknown); Informant; Comments; Status; Recorded by/at; Last verified by/at.
**Fields per infusion reaction (oncology-specific):** Agent; Regimen; Cycle and day; Infusion number; Time from start to reaction (`[DERIVED]` where start time known); Signs/symptoms (multiselect); Grade (`[CCA CONFIG]` terminology); Interventions (multiselect: infusion stopped, rate reduced, antihistamine, steroid, adrenaline, oxygen, fluids, other); Outcome; Rechallenge performed (y/n); Rechallenge outcome; Premedication used at rechallenge; Desensitisation performed; Future precautions (free text + structured flags).
**Actions:** Add · Edit · Mark inactive/refuted (reason required) · Assert NKDA · Verify · View history.
**Alerts:** Asserting NKDA when allergies exist → hard stop. Editing an allergy that is referenced by an active order → warning naming the order.
**Downstream:** Immediate propagation to the banner, to order-entry checking, to pharmacy verification, to MAR administration checks, to radiology contrast screening.
**INT-NUR-410 [PRODUCT]** — Removal of an allergy is never a deletion; it is a status change to Refuted/Entered-in-error with reason and attribution, and the entry remains viewable.

---

## C.2.5 · `SCR-INT-005` — Medication Reconciliation
**Role:** Intake nurse (capture), clinician (confirm), pharmacist (verify).
**Sections:** Current list · New/changed at this visit · Reconciliation decisions · Sources consulted.
**Table columns:** Drug · Strength · Form · Dose · Unit · Route · Frequency · Schedule · Indication · Prescriber · Source (product-defined: Prescribed here / External prescription / Patient-reported / Carer-reported / Discharge summary / Pharmacy record) · Class flags (anticancer / supportive / anticoagulant / antiplatelet / herbal / OTC / QT-relevant `[CCA CONFIG]`) · Start date · Stop date · Status · Reconciliation action (Continue / Hold / Stop / Change dose / Substitute / Unknown — product-defined) · Reason · Decided by · Decided at.
**Calculated:** Count of unreconciled items; days since last reconciliation.
**Alerts:** Anticoagulant present + surgery scheduled → warning routed to the surgical team; herbal/OTC present + active systemic therapy → interaction review prompt to pharmacy; unreconciled items at the point of order signing → warning.
**Sign:** Nurse attests capture; clinician attests reconciliation. Both retained separately — **INT-NUR-420 [PRODUCT]**: nurse capture is not clinician reconciliation and the two must never be conflated.

---

## C.2.6 · `SCR-INT-006` — Screening Instruments
**Role:** Intake, inpatient, RT nursing.
**Purpose:** Administer configured instruments with item-level capture.
**Structure:** One generic instrument engine `[PRODUCT]` rendering any configured instrument `[CCA CONFIG]`: instrument name, version, items (each with type, options, scores), scoring rule, bands, interpretation text, triggered actions, review interval.
**Fields per administration:** Instrument + version; item-level responses (stored discretely, never only as a total); total score `[DERIVED]`; band `[DERIVED]`; assessed by; role; date/time; not-assessable reason; triggered interventions (checklist with completion).
**INT-NUR-430 [PRODUCT]** — item-level responses must be stored; storing only the total makes re-scoring, audit and instrument version migration impossible.
**Downstream:** Band crossing a configured threshold → referral proposal, care-plan intervention, and (for fall risk) nursing intervention checklist on the ward.

---

## C.2.7 · `SCR-INT-007` — Vascular Access Assessment
**Role:** Intake, Day Care, Inpatient nursing.
**Fields:** Device present (y/n); Device type (dropdown — product-defined: Peripheral cannula / Midline / PICC / Tunnelled central catheter / Implanted port / Dialysis catheter / Other); Site (dropdown: anatomical); Laterality; Insertion date; Days in situ `[DERIVED]`; Inserted by/where; Gauge/size; Lumens; Patency (Flushes and aspirates / Flushes only / Neither / Not assessed); Blood return present; Site assessment (multiselect: normal, erythema, swelling, tenderness, discharge, leakage, bruising, thrombosis signs); Phlebitis/infiltration score where configured `[CCA CONFIG]`; Dressing status and date; Securement; Last flushed; Complication; Action taken; Suitable for vesicant administration (**explicit clinician/nurse determination**, product-defined value set) — **MAR-040 [PRODUCT]**.
**Alerts:** Warning if a vesicant is ordered and access is not documented as suitable; warning if peripheral access is the only route for a regimen flagged as requiring central access `[CCA CONFIG]`.
**Downstream:** Day Care administration screen; inpatient device care record; escalation for device replacement.

---

## C.2.8 · `SCR-INT-008` — Intake Escalation
**Fields:** Finding (structured + narrative); Category (dropdown); Severity; Escalated to (named user + role); Method (in person / phone / secure message / emergency call); Time raised; Time acknowledged `[DERIVED]` response interval; Response/instruction received; Action taken; Outcome; Patient disposition (Continue to clinic / Send to Day Care hold / Send to Emergency / Admit / Defer visit); Closed by/at.
**Downstream:** Named clinician's task inbox with escalating reminders; appears on the clinic worklist as a chip; unacknowledged escalations escalate further per `[CCA CONFIG]`.

---

# C.3 — NURSE NAVIGATION SCREENS

## C.3.1 · `SCR-NAV-001` — Navigator Panel / Pathway Board
**Role:** Nurse Navigator; clinical manager (read-only).
**Navigation:** Landing screen for the Navigator role.
**Purpose:** Surface every navigated patient's position against expected milestones and the specific item blocking progress.
**Header:** Panel selector (my panel / team / all), disease-site filter, counts strip (On track / At risk / Breached / Paused / New this week).
**Table columns:** Per B.3.B View 1, with **Pathway status** `[DERIVED]` (`CALC-040`), **Days in current milestone** `[DERIVED]` (`CALC-041`), **Blocking item** (text naming the specific outstanding artifact and its owner).
**Actions:** Log contact · Add barrier · Chase investigation · Submit to MDT · Book appointment · Refer · Escalate · Send patient information · Pause pathway (reason) · Discharge from navigation.
**Chips:** Pathway status; MDT status; readiness; consent; financial clearance; barrier count.
**Alerts:** Breach imminent (configured lead time `[CCA CONFIG]`); critical result unacknowledged; MDT recommendation with overdue action; patient with no future appointment and an active episode — **NAV-020 [PRODUCT]**: "active episode with no next event booked" is a first-class alert condition, because it is the commonest silent failure.
**Empty state:** distinguishes an empty panel from a filtered-to-nothing view.
**Downstream:** Each action creates the corresponding record and, where relevant, a task on another role's inbox.

## C.3.2 · `SCR-NAV-002` — Patient Pathway Detail
**Purpose:** One patient's full pathway with milestone-by-milestone evidence.
**Sections:** Milestone timeline (visual) · Milestone table · Outstanding items · Barriers · Contacts · Education · Referrals · Appointments across all departments.
**Milestone table columns:** Milestone name (`[CCA CONFIG]` per pathway template) · Target interval · Due date `[DERIVED]` · Actual date · Status · Evidence record (link) · Days variance `[DERIVED]` · Pause periods (with reason) · Owner.
**NAV-030 [PRODUCT]** — pause periods are excluded from breach calculation and the exclusion must be visible and reason-stamped, so that clinically justified delays are not reported as service failures.
**Print/export:** Pathway status report; patient journey summary.

## C.3.3 · `SCR-NAV-003` — Barrier Register
Fields per `NAV-110`. Table columns: Barrier type · Description · Identified date/by · Severity · Actions · Referrals made · Status · Resolution date · Outcome · Days open `[DERIVED]`.
**Downstream:** Financial barriers → Financial Counsellor queue; comprehension barriers → education task; transport → social work referral `[CCA CONFIG]`.

## C.3.4 · `SCR-NAV-004` — Contact Log
Fields per `NAV-120`. Signed, immutable per `GEN-SIG-001`. Rendered chronologically with the clinical timeline so a clinician can see that a patient was contacted between visits.

## C.3.5 · `SCR-NAV-005` — Education Delivery
Fields per `NAV-130`. Table: Topic · Material + version · Language · Format · Delivered to · Delivered by · Date · Comprehension confirmed · Method of confirmation · Reinforcement due.
**NAV-040 [PRODUCT]** — where a material version is superseded, previously delivered records retain the version actually given; the register flags patients who received a superseded version of a safety-critical material so they can be re-educated.

## C.3.6 · `SCR-NAV-006` — Referral Tracking
Fields per `NAV-140`. Columns: Referral · To (internal/external) · Reason · Urgency · Sent · Acknowledged `[DERIVED]` interval · Appointment date · Outcome received · Loop closed by/at · Days open.
**Alerts:** Referral unacknowledged beyond threshold; appointment not booked; outcome not received.

## C.3.7 · `SCR-NAV-007` — Outstanding Results / Loop Closure
Columns: Patient · Investigation · Ordered by · Ordered date · Expected date · Status · Result date · Acknowledged by/at · Days unacknowledged `[DERIVED]` · Critical flag · Action taken.
**NAV-010** enforced here: every result has an acknowledgement owner and an audit trail.

---

# C.4 — MEDICAL ONCOLOGY CONSULTATION SCREENS

## C.4.1 · `SCR-MO-001` — Medical Oncology Clinic Worklist
**Role:** Medical Oncologist; fellow/registrar (scoped); clinic nurse (read-only).
**Navigation:** Landing screen.
**Purpose:** Per B.4.B View 1, with the readiness chip computed before opening (`MO-CON-010`).
**Tabs:** Today's Clinic · Treatment-Day Clearance · Results Inbox · Orders & Signatures Pending · My Patients · Inpatients.
**Table columns:** per B.4.B.
**Actions:** Open consultation · Open treatment order · Grant clearance · Review results · Submit to MDT · Refer · Write note · Print clinic list.
**Alerts:** Unsigned notes older than threshold `[CCA CONFIG]`; unacknowledged critical results; pharmacy queries awaiting response; orders expiring.
**Downstream:** Opening a patient with visit type "New" launches `SCR-MO-002`; "Follow-up" launches `SCR-MO-003`; "Treatment-day" launches `SCR-MO-004` (clearance).

---

## C.4.2 · `SCR-MO-002` — New Medical Oncology Consultation

| Dimension | Specification |
|---|---|
| **Role(s)** | Medical Oncologist; trainee (draft + countersignature). |
| **Navigation** | Clinic worklist → patient (visit type New); or from Navigator; or from MDT action. |
| **Purpose** | Establish the clinical picture, the diagnosis or diagnostic pathway, the stage or staging plan, and the initial management plan. |
| **Header** | Full MO header per B.4.C — persistent strip plus expandable panel. |
| **Sections (left nav, progress-tracked)** | 1 Referral & source · 2 Presenting complaints · 3 History of present illness / cancer chronology · 4 Previous cancer treatment · 5 Past medical & surgical history · 6 Medications · 7 Allergies · 8 Family history · 9 Social history · 10 Reproductive/pregnancy history · 11 Prior toxicities & infusion reactions · 12 Systems review · 13 Performance status · 14 Examination · 15 Investigations reviewed · 16 Assessment & provisional diagnosis · 17 Staging (link to `SCR-DX-002`) · 18 Plan · 19 Discussion & counselling · 20 Orders raised · 21 Sign. |
| **Fields — selected detail** | **Referral:** source (dropdown), referrer, referral date, referral reason, documents reviewed (checklist with links). **Presenting complaints:** repeating group — complaint (coded + free text), duration (numeric + unit dropdown: days/weeks/months/years), severity, progression (dropdown: improving/static/worsening/fluctuating), associated features (multiselect). **Cancer chronology:** repeating timeline entries — event type (dropdown — product-defined: Symptom onset / Investigation / Diagnosis / Surgery / Systemic therapy / Radiotherapy / Recurrence / Progression / Remission / Other), date (with precision flag: exact/month/year/estimated), description, facility, documents. **Previous treatment:** per modality — systemic (regimen, drugs, start/end dates, cycles received, best response, toxicities, reason for stopping); RT (site, dose, fractions, dates, technique, facility); surgery (procedure, date, findings, margins, complications). **Comorbidities:** coded problem list with onset, status, severity, oncology-relevance flag. **Family history:** repeating — relative, relationship, condition (coded), age at diagnosis, alive/deceased, genetic testing done; plus a `[DERIVED]` hereditary-risk flag against configured criteria `[CCA CONFIG]` proposing a genetics referral. **Social:** tobacco (status, type, quantity, duration, pack-years `[DERIVED]` `CALC-050`, quit date), alcohol (status, quantity, units/week `[DERIVED]`), betel/areca or other regional exposures `[CCA CONFIG]`, occupational exposures, living situation, dependants, caregiver, employment, functional independence. **Reproductive:** menarche, parity, LMP, menopausal status, contraception, fertility-preservation discussion (y/n, date, outcome, referral) — **MO-CON-030 [PRODUCT]**: fertility preservation discussion must be a discrete, dated, auditable field for patients within a configured age band `[CCA CONFIG]`, not buried in narrative. **Prior toxicities:** linked to the longitudinal toxicity record. **Performance status:** instrument, score, assessed by (clinician — distinct from nurse-assessed), date. **Examination:** general (with vitals auto-imported read-only), systemic examination by system (structured normal/abnormal with descriptors), site-specific tumour examination (measurable lesion sizes with method and units, node stations, laterality), performance observations. **Assessment:** provisional/working diagnosis (coded), differential (repeating), diagnostic certainty (product-defined: Confirmed histologically / Confirmed cytologically / Radiological — pending tissue / Clinical — pending confirmation), basis of diagnosis. **Plan:** investigations to order (launches `SCR-INV-001`), referrals, MDT submission required (y/n + question), treatment intent (provisional), next review interval (structured numeric + unit — consumed by check-out per `REG-FD-120`), admission required. **Discussion:** topics covered (multiselect `[CCA CONFIG]`), who was present, interpreter used, patient understanding, information materials issued, prognosis discussed (y/n — content free text), decisions deferred. |
| **Tables** | Complaints; chronology; previous treatments (one per modality); comorbidities; medications; allergies; family history; investigations reviewed (test, date, source, key result, link); orders raised this visit. |
| **Dropdowns** | See above; all coded clinical fields are standard-terminology backed where a standard exists, `[CCA CONFIG]` for local value sets, product-defined for workflow enums. |
| **Calculated** | Age; BMI/BSA (imported read-only with source dates); pack-years; alcohol units; hereditary-risk flag; interval since last treatment; PS trend. |
| **Actions** | Save draft · Insert template `[CCA CONFIG]` · Import previous note (explicitly marked as copied content with source and date — **MO-CON-040 [PRODUCT]**: copied-forward content must be visually attributed, never silently inherited) · Order investigations · Refer · Submit to MDT · Create treatment plan · Print · **Sign**. |
| **Chips** | Section completion; diagnosis certainty; staging status (Not staged / Clinical stage recorded / Pathological stage recorded / Restaged); MDT status; draft/signed. |
| **Alerts** | **Hard stop on sign:** no diagnosis or diagnostic-plan recorded; no performance status; no allergy status. **Warning:** no episode selected/created; family history meets hereditary-referral criteria but no referral raised; fertility discussion not recorded for a patient in the configured age band; treatment intent absent when a treatment plan is being created. |
| **Conditional logic** | Reproductive section by sex/age; fertility-preservation prompt by age band and intent; hereditary flag by family-history pattern; site-specific examination template by primary site `[CCA CONFIG]`; MDT-submission section mandatory where the disease-site pathway rule requires discussion `[CCA CONFIG]`. |
| **Read-only** | Vitals, anthropometrics, labs, imaging results, prior notes, derived values — all imported with source and date, none editable here. |
| **Sign/approve** | Clinician signature with re-authentication. Trainee draft → countersignature routing to the responsible consultant, whose signature is what makes the note consumable — **MO-CON-050 [PRODUCT]**. |
| **Amendment/version** | Addendum or amendment with reason; prior version viewable side by side; consumers notified where the diagnosis, stage or plan changed. |
| **Comparison view** | "Previous note" panel docked alongside, showing the last note of the same type, section-aligned. |
| **Post-signature** | Note immutable; diagnosis/stage/PS/intent written to the episode; orders released; MDT submission created; referrals dispatched; next-review interval published to check-out and Navigator. |
| **Downstream queues** | Radiology/Lab/Pathology order queues; MDT Coordinator submissions inbox; Navigator pathway update; Financial Counsellor if a costed plan is implied; Pharmacy if an oral therapy is prescribed. |
| **Blocked state** | Cannot sign without an active cancer episode where the note asserts a cancer diagnosis; cannot sign if a required `[CCA CONFIG]` mandatory template section is empty. |
| **Print/export** | Initial Medical Oncology Consultation Note (full sections per Part F); referral letter derived from it. |

---

## C.4.3 · `SCR-MO-003` — Follow-up Oncology Consultation
**Differences from `SCR-MO-002`:** Sections are interval-focused — 1 Interval history since last visit (auto-populated event list: cycles administered, fractions delivered, admissions, results, toxicities, contacts — read-only, with the clinician's narrative on top) · 2 Symptoms and toxicity review (linked to the longitudinal toxicity record, pre-populated with active toxicities requiring re-grading) · 3 Treatment tolerance · 4 Adherence (for oral therapy) · 5 Examination · 6 Results review · 7 Response assessment (link to `SCR-RSP-001`) · 8 Assessment · 9 Plan (continue / modify / hold / delay / discontinue / change line) · 10 Orders · 11 Discussion · 12 Sign.
**MO-CON-060 [PRODUCT]** — the interval-history panel is generated from the record, not typed. It must list every treatment event, admission, result and toxicity since the last note of this type, so that nothing that happened between visits is invisible at the visit.
**Alerts:** Active toxicity not re-graded at this visit; response assessment proposed by radiology and not yet confirmed; treatment plan reaching its planned cycle count without a documented next decision.
**Downstream:** Plan decisions route to treatment order modification, hold, delay or discontinuation screens (Document 4).

---

## C.4.4 · `SCR-MO-004` — Results Inbox & Result Review
**Role:** All ordering clinicians.
**Purpose:** Guarantee that every result is seen, interpreted and acted on by a named clinician.
**Sections:** Inbox list · Result detail · Trend/compare · Action.
**Table columns:** Patient · UHID · Result type · Test/study · Ordered by · Ordered for (indication) · Collected/acquired · Resulted · Abnormal flag · Critical flag · Status (Unread / Read / Acknowledged / Action taken / Delegated) · Days unacknowledged `[DERIVED]` · Linked episode.
**Result detail fields:** full result with reference ranges, units, method, performing lab/radiologist, comparison to previous (value, delta, % change `[DERIVED]`), and for imaging the structured report with lesion table and viewer link.
**Actions:** Acknowledge · Acknowledge with comment · Order follow-up · Notify patient (with method and content recorded) · Notify navigator · Flag for MDT · Delegate acknowledgement (records both users) · Mark as reviewed-not-mine (returns to correct clinician with reason).
**Alerts:** Critical results pinned, cannot be bulk-acknowledged — **MO-INV-010 [PRODUCT]**: critical results require individual acknowledgement with the clinician having opened the detail view. Corrected results re-enter the inbox as unacknowledged even if the original was acknowledged (`LAB-050`).
**Downstream:** Acknowledgement closes the Navigator loop-closure entry; "flag for MDT" creates an MDT submission draft; follow-up orders enter the ordering queues.

---

# C.5 — DIAGNOSIS & STAGING SCREENS

## C.5.1 · `SCR-DX-001` — Cancer Episode
**Role:** MO / RO / SO (create and edit), all clinical (view).
**Navigation:** From consultation → "Create/edit episode"; from the header episode selector.
**Purpose:** Define the malignancy that all other records attach to.
**Fields:** Episode ID (auto); Episode label (auto-generated from site + laterality + date, editable); Date of first diagnosis (date + precision flag); Diagnosing facility (internal/external); Basis of diagnosis (dropdown — product-defined: Histology of primary / Histology of metastasis / Cytology / Radiology only / Clinical only / Laboratory/tumour marker / Death certificate); Primary site (coded topography, R); Sub-site; Laterality (product-defined); Morphology/histology (coded, R); Behaviour; Grade (system + value); Multiple primaries relationship (dropdown: independent primary / synchronous / metachronous); Related episode link; Trial enrolment; Episode status (per A.1.2 state machine); Responsible specialty; Primary treating clinician; Date of episode closure and reason.
**Calculated:** Time from symptom onset to diagnosis `[DERIVED]`; time from referral to diagnosis `[DERIVED]` (both feed pathway metrics).
**Actions:** Create episode · Edit · Change status (with reason) · Link/unlink related episode · Close episode · Merge episodes (permission-gated, requires reason and clinical authority — **MO-DX-020 [PRODUCT]**).
**Alerts:** Hard stop on creating a second episode with the same site and laterality within a configured window without explicitly declaring the relationship (`GEN-FLW-001`).
**Downstream:** Every record written thereafter carries this episode; registry export dataset; Treatment Summary.

## C.5.2 · `SCR-DX-002` — Staging
**Role:** MO / RO / SO (clinical stage), Pathologist (pathological stage — via `SCR-PAT-*`), all (view).
**Purpose:** Record stage as a versioned, dated, attributed clinical assertion using a named system.
**Sections:** Staging system selection · Clinical stage (cTNM) · Pathological stage (pTNM, read-only here — sourced from pathology) · Restaging events · Stage history.
**Fields:** Staging system (dropdown `[CCA CONFIG]` — name + edition/version, R); Staging basis (dropdown: clinical examination / imaging / endoscopy / surgical exploration / pathology); T (dropdown, value set driven by system + site); N; M; Prefix/suffix modifiers (multiselect: y, r, a, m, c/p — product-defined); Site-specific factors required by the system (dynamic fields `[CCA CONFIG]` — e.g. grade, biomarker status, risk group where the system incorporates them); Stage group `[DERIVED]` (`CALC-060` — derived from T/N/M plus required factors against the system's stage table `[CCA CONFIG]`); Stage group override (permitted with mandatory reason — **MO-DX-030 [PRODUCT]**: the derived group is authoritative unless a clinician explicitly overrides with a recorded rationale); Date staged; Staged by; Evidence (linked investigations, multiselect, required — **MO-DX-031 [PRODUCT]**: a stage assertion must cite the records supporting it); Comments.
**Tables:** Stage history (system, basis, cTNM/pTNM, stage group, date, stager, evidence, current/superseded).
**Chips:** `CLINICAL STAGE` vs `PATHOLOGICAL STAGE` — permanently distinct, never merged into "stage" (`GEN-CMP-001`); Current vs Superseded; Restaged.
**Alerts:** Warning if M is asserted without supporting imaging/pathology evidence; warning if pathological stage exists and differs from clinical stage without a recorded restaging event; hard stop on entering a T/N/M combination invalid for the selected system.
**Comparison view:** cTNM and pTNM side by side with the derivation of each stage group displayed.
**Post-signature:** Stage frozen into any note or MDT record that displayed it; a later restaging never rewrites history.
**Downstream:** MDT case pack, treatment planning, registry export, Treatment Summary, eligibility rules.

## C.5.3 · `SCR-DX-003` — Biomarker Panel
**Role:** MO (interpret), Pathologist (source), all (view).
**Purpose:** Present every biomarker with method, cutoff and therapeutic implication, from all sources, in one comparable table.
**Table columns:** Marker · Method · Specimen/accession · Specimen date · Specimen site (primary vs metastasis — clinically important) · Result value · Unit · Scoring system · Score · Interpretation (Positive / Negative / Equivocal / Not evaluable) · Cutoff applied `[CCA CONFIG]` · Laboratory · Internal/external · Reported date · Therapeutic implication flag · Status (Current / Superseded / Repeat pending) · Actions.
**Fields:** Manual entry supported for external results with source document attachment and a "not internally verified" flag — **MO-DX-040 [PRODUCT]**.
**Alerts:** Conflicting results for the same marker from different specimens → flagged, both retained, clinician records which is being acted upon and why; required biomarker for the selected regimen absent → blocks order signing per `[CCA CONFIG]` rule.
**Germline handling:** separate section with distinct access permission and consent linkage (`MO-DX-010`, `PAT-192`).
**Downstream:** Regimen eligibility checking, MDT pack, treatment plan, Treatment Summary.

## C.5.4 · `SCR-DX-004` — Disease Status & Line of Therapy
**Purpose:** Maintain the two longitudinal clinical assertions that drive most reporting and most treatment decisions.
**Disease status fields:** Status (dropdown — product-defined: No evidence of disease / Complete response / Partial response / Stable disease / Progressive disease / Recurrent — local / Recurrent — regional / Recurrent — distant / Newly diagnosed / Not assessed); Date; Basis (dropdown: imaging / pathology / clinical examination / biochemical / composite); Evidence links (R); Sites of disease (multiselect anatomical, with dates); Assessed by; Comments.
**Line of therapy fields:** Line number `[DERIVED]` with clinician confirmation (`CALC-061` — derived from the count of distinct systemic treatment courses for this episode, with configurable rules `[CCA CONFIG]` on what constitutes a new line); Line label (1L, 2L, maintenance, adjuvant, neoadjuvant, consolidation — product-defined); Intent; Start date; End date; Reason for ending (dropdown: completed as planned / progression / toxicity / patient choice / comorbidity / death / lost to follow-up / other); Best response achieved; Regimens within the line.
**MO-DX-050 [PRODUCT]** — line-of-therapy derivation must be transparent: the screen shows which treatment courses were counted and which were excluded, and the rule applied.
**Downstream:** Eligibility rules, MDT, reporting, Treatment Summary.

---

# C.6 — INVESTIGATION SCREENS

## C.6.1 · `SCR-INV-001` — Investigation Ordering

| Dimension | Specification |
|---|---|
| **Role(s)** | MO, RO, SO, Inpatient clinician; nurse (protocol-driven orders per `[CCA CONFIG]` with clinician co-signature). |
| **Navigation** | From any consultation "Plan" section; from the patient header "+ Order"; from a treatment plan's required-monitoring list; from a readiness screen's failed-criterion "order this test". |
| **Purpose** | Create clinically justified, correctly prioritised, adequately contextualised orders that the performing department can act on without telephoning back. |
| **Header** | Full clinical header for the ordering role. |
| **Sections** | Catalogue search / Order sets · Selected orders · Clinical context · Scheduling · Review & sign. |
| **Fields per order** | Test/study (coded from Laboratory / Radiology / Pathology catalogue `[CCA CONFIG]`, R); Quantity/frequency (single / repeating with interval and count / standing with review date); Priority (dropdown — product-defined: Routine / Urgent / STAT / Pre-treatment — required by [date] / MDT deadline [date]); Requested date/time; Required-by date (drives coordinator prioritisation, R for treatment-gating tests); Clinical indication (coded + narrative, **mandatory, minimum length enforced, "routine" alone rejected** — **MO-INV-020 [PRODUCT]**); Specific question (text, R for imaging); Purpose (dropdown: Diagnostic / Staging / Restaging / Response assessment / Surveillance / Monitoring — treatment safety / Complication / Procedure planning / RT planning); Relevant clinical details (auto-assembled from record: diagnosis, stage, treatment, prior studies — clinician can supplement, cannot delete the auto content); Body region / specimen site / laterality (conditional, R for imaging and pathology); Contrast requested (conditional); Isolation/precautions (auto); Interpreter/mobility (auto); Fasting required (auto from catalogue); Linked appointment; Copy results to (multiselect of clinicians); Order set applied (name + version `[CCA CONFIG]`). |
| **Tables** | Catalogue results (test, code, specimen/modality, TAT, prerequisites, cost where displayed `[CCA CONFIG]`, add); Selected orders (test, priority, required-by, indication, scheduling status, remove); Recent duplicates panel — **MO-INV-030 [PRODUCT]**: on selecting a test, the screen shows any same/similar test ordered within a configured window with its date, status and result, to prevent duplicate ordering. |
| **Dropdowns** | Catalogue (`[CCA CONFIG]`); priority, purpose (product-defined); laterality (product-defined); contrast (product-defined); order sets (`[CCA CONFIG]`, versioned). |
| **Calculated** | Prerequisite status `[DERIVED]` (e.g. creatinine present and within validity for a contrast study — `CALC-070`); expected result date from catalogue TAT `[DERIVED]`; conflict with scheduled treatment date `[DERIVED]`. |
| **Actions** | Search catalogue · Apply order set · Add · Remove · Set priority · Attach clinical documents · Save draft · **Sign and release** · Sign and schedule · Cancel order (with reason, permitted only before result). |
| **Chips** | Prerequisite met/not met; duplicate warning; priority; scheduling status. |
| **Alerts** | **Hard stop:** ordering a contrast study without a valid renal result where the rule requires one `[CCA CONFIG]`; ordering a test contraindicated by a recorded allergy; missing mandatory indication. **Warning:** duplicate within window; test scheduled after the treatment date it is meant to gate — **MO-INV-040 [PRODUCT]**: the system must detect that a readiness-gating investigation is booked after the treatment it gates. |
| **Conditional logic** | Contrast fields appear per modality; laterality mandatory for paired organs; specimen fields for pathology; fasting/preparation auto-attached from catalogue; MDT-deadline priority requires a linked MDT date. |
| **Read-only** | Auto-assembled clinical details (supplementable, not deletable); catalogue attributes; prerequisite derivation. |
| **Sign/approve** | Clinician signature releases the order. Nurse-initiated protocol orders require clinician co-signature before the performing department acts — **MO-INV-050 [PRODUCT]**. |
| **Amendment/version** | An released order may be cancelled (with reason) or amended before collection/acquisition; after that, a new order is required. Amendments are versioned and the performing department is notified. |
| **Post-signature** | Order becomes visible to the performing department; requisition/label generated; appointment booking prompted; Navigator loop-closure entry created. |
| **Downstream queues** | Laboratory collection list; Radiology Coordinator unscheduled-orders queue (`SCR-RADC-001`); Pathology requisition; Financial Counsellor if authorisation required. |
| **Blocked state** | No active episode where the order requires one; catalogue master unavailable; patient has no valid identifiers for the performing system `[INTEGRATION]`. |
| **Print/export** | Requisition form; specimen labels; patient preparation instruction sheet. |

## C.6.2 · `SCR-INV-002` — Order Sets & Panels
**Role:** Clinician (use), Clinical Content Administrator (maintain).
**Purpose:** Apply a versioned, clinically approved bundle of investigations (e.g. pre-treatment baseline panel, cycle-day monitoring panel, surveillance panel).
**Fields:** Order set name; version; effective date; disease site; treatment context; included tests with default priority and frequency; mandatory vs optional members; approver.
**MO-INV-060 [PRODUCT]** — when an order set is applied, the version applied is stamped on the resulting orders, and each order remains individually editable and individually cancellable. Order sets never create orders that cannot be inspected line by line.

## C.6.3 · `SCR-INV-003` — Result Trend & Compare
**Purpose:** Show a result in its longitudinal and treatment context.
**Sections:** Tabular series · Graph · Treatment overlay · Reference bands.
**Table columns:** Date/time · Value · Unit · Reference range · Flag · Delta from previous `[DERIVED]` · % change `[DERIVED]` · Method · Lab · Comments.
**Overlay:** treatment events (cycle days, RT fractions, surgery, transfusions, growth factor administration, steroid courses) plotted against the series — **MO-INV-070 [PRODUCT]**: a count result cannot be interpreted without knowing whether growth factor was given, so the overlay is a requirement, not a nicety.
**Actions:** Change date range · Select comparators · Export · Add to MDT pack · Print.
**Blocked/Error:** where unit normalisation across labs is not possible, the screen must display source units per point and refuse to plot a single series with mixed non-convertible units — **GEN-UNI-001 [PRODUCT]**.

---

## END OF DOCUMENT 3

**Continues in Document 4 — PART C, Section 2:** MDT screens · Treatment Plan · Systemic Treatment Order (regimen selection, dosing, supportive care, review and signature) · Treatment Readiness · Pharmacy (verification, preparation, double check, dispensing).
