# CCA CANCER CARE — ONCOLOGY HIS + EMR
# MASTER FUNCTIONAL & CLINICAL PRODUCT REQUIREMENT INVENTORY
## Document 4 of N — PART C (Screen-by-Screen), Section 2
### C.7 MDT / Tumour Board · C.8 Treatment Plan · C.9 Systemic Treatment Order · C.10 Treatment Readiness / Cycle Clearance · C.11 Oncology Pharmacy

*Conventions and universal state behaviour per C.0 (Document 3) apply throughout and are not restated.*

---

# C.7 — MDT / TUMOUR BOARD SCREENS

## C.7.1 · `SCR-MDT-001` — MDT Case Submission

| Dimension | Specification |
|---|---|
| **Role(s)** | Any treating clinician (MO, RO, SO, Pathologist, Radiologist, Inpatient clinician); Nurse Navigator (submit on behalf of, with clinician attribution). |
| **Navigation** | Consultation note → "Submit to MDT"; patient header → "+ MDT"; Results Inbox → "Flag for MDT"; Navigator pathway board → "Submit to MDT"; pathway rule auto-proposal `[CCA CONFIG]` appearing in the clinician's task inbox. |
| **Purpose** | Place a case before the right meeting with a *specific answerable question* and a complete evidence base. |
| **Header** | Full clinical header for the submitting role, plus a submission strip: target meeting, meeting date, submission deadline `[DERIVED]`, completeness score. |
| **Sections** | 1 Meeting selection · 2 Question · 3 Clinical summary · 4 Evidence attachment · 5 Completeness check · 6 Logistics · 7 Submit. |
| **Fields — visible & editable** | **Meeting:** Tumour stream / meeting type (dropdown `[CCA CONFIG]`, R); Target meeting date (dropdown of scheduled meetings with remaining capacity, R); Urgency (dropdown — product-defined: Routine / Urgent — next available / Emergency — out-of-cycle discussion); Reason for urgency (conditional text, R when urgent/emergency); Case category (dropdown — product-defined: New diagnosis / Post-operative / Progression or recurrence / Complex management / Re-discussion / Second opinion / Trial screening / Toxicity management / End-of-treatment). **Question:** Specific question(s) (repeating group, R, minimum one; each with question text (R, minimum length enforced), question type (dropdown: Diagnosis confirmation / Staging / Treatment modality choice / Sequencing / Operability / Radiotherapy indication / Systemic therapy choice / Trial eligibility / Palliative approach / Pathology review / Imaging review / Other)) — **MDT-020 [PRODUCT]**: a submission without a specific question is rejected; "for discussion" is not an acceptable question. **Clinical summary:** Narrative (R, templated `[CCA CONFIG]`, seeded from the latest consultation note but editable, with the seeded portion visually attributed per `MO-CON-040`); Key clinical points (repeating short statements); Patient's own views/preferences recorded (text + date discussed); Comorbidities affecting treatment (auto-listed, supplementable); Performance status (auto, read-only, with date and assessor); Prognosis considerations (optional narrative). **Evidence:** auto-assembled checklist (see Tables) with per-item include/exclude and comment; Additional documents (upload/select). **Logistics:** Presenter (dropdown of participants, defaults to submitter); Radiology review required (checkbox → studies selector + radiologist assignment request); Pathology review required (checkbox → accession selector + slides/blocks availability + pathologist assignment request); Patient/family attending (checkbox `[CCA CONFIG]`); Estimated discussion time (numeric minutes, defaulted by case category); Conflict of interest declaration `[CCA CONFIG]`. |
| **Tables** | **Evidence checklist:** Item · Required for this meeting type (`[CCA CONFIG]`) · Present (Y/N) `[DERIVED]` · Source record · Date · Age in days `[DERIVED]` · Within validity window `[DERIVED]` · Include in pack · Comment. Rows minimally: histological diagnosis, morphology code, grade, primary site/laterality, cTNM + system, pTNM where applicable, biomarker panel (itemised — each configured marker as its own row), staging imaging (modality + date), current imaging, performance status, comorbidity list, current medications, prior treatment record, treatment response history, toxicity history, renal/hepatic function, cardiac function where required, consent status, trial screening status. **Prior MDT discussions:** Date · Meeting · Question · Recommendation summary · Action status · Link. |
| **Dropdowns** | Meeting type `[CCA CONFIG]`; urgency, case category, question type (product-defined); presenter (roster-derived); documents (record-derived). |
| **Calculated** | Completeness score and per-item status `[DERIVED]` (`CALC-080`) against the meeting's required dataset `[CCA CONFIG]`; submission deadline = meeting date − configured lead time `[DERIVED]`; days until meeting; evidence age per item. |
| **Actions** | Save draft · Auto-assemble evidence · Add document · Request radiology review · Request pathology review · Check completeness · **Submit** · Withdraw submission (before agenda lock) · Submit as incomplete (permission-gated, reason mandatory). |
| **Chips** | Completeness (green complete / amber n items outstanding / red mandatory item missing); Urgency; Case category; Submission status (Draft / Submitted / Accepted / Returned / Listed / Deferred / Discussed / Withdrawn). |
| **Alerts** | **Hard stop:** no question; no target meeting; mandatory evidence item missing and submitter lacks incomplete-submission permission. **Override with reason:** submitting with outstanding evidence (`MDT-010`) — the override reason and the outstanding items are carried onto the agenda and into the minutes. **Warning:** submission after the deadline for the selected meeting (offers next meeting); duplicate submission for the same episode within a configured window; imaging older than the configured validity window for the meeting type. |
| **Conditional logic** | Reason-for-urgency appears when urgency ≠ Routine. Pathology/radiology reviewer request panels appear on checkbox. pTNM evidence row appears only when a resection specimen exists. Trial screening row appears only when open trials match the disease site `[CCA CONFIG]`. |
| **Read-only** | All auto-assembled evidence values and their dates; completeness derivation (with rule tooltip); performance status; prior MDT history. |
| **Sign/approve** | Submission is attributed and locked, not signed as a clinical document. Where a Navigator submits, the responsible clinician's confirmation is required before the case is accepted onto an agenda — **MDT-021 [PRODUCT]**. |
| **Amendment/version** | Editable while `Draft` or `Submitted`; once `Listed` (agenda locked), changes create a version with the coordinator notified and the prior version retained. After discussion, the submission is immutable. |
| **Current vs superseded** | Re-discussions link to the prior discussion; the case pack shows the previous recommendation and its action status alongside the new question. |
| **Downstream** | Creates an entry in **`SCR-MDT-002` Submissions Inbox** (MDT Coordinator); creates review-request tasks for the named radiologist and pathologist; creates a Navigator pathway milestone; if evidence is missing, creates ordering prompts for the submitter. |
| **Empty/blocked** | Blocked if no active cancer episode; blocked if no future meeting exists for the selected stream (offers to request an out-of-cycle meeting). |
| **Print/export** | Submission summary; case pack preview. |

---

## C.7.2 · `SCR-MDT-002` — Submissions Inbox & Agenda Builder
**Role:** MDT Coordinator; Chair (view + reorder).
**Navigation:** Landing screen for the Coordinator role.
**Purpose:** Triage submissions and construct a timed, quorate, evidence-complete agenda.
**Sections:** Submissions inbox · Agenda canvas · Capacity panel · Participant panel · Deferrals.
**Tables:**
- *Submissions:* Submitted date · Submitter · Patient · UHID · Primary site · Case category · Urgency · Question (truncated, expandable) · Completeness chip · Outstanding items · Requested meeting · Days waiting `[DERIVED]` · Prior discussions · Actions (Accept to agenda / Return with reason / Defer / Reassign meeting).
- *Agenda canvas:* Order (drag) · Time slot `[DERIVED]` from cumulative allocations · Patient · Case category · Question · Presenter · Radiology reviewer · Pathology reviewer · Allocated minutes · Pack status (Assembled / Incomplete / Not started) · Actions.
- *Capacity:* total allocated minutes vs meeting duration `[DERIVED]`, over-run warning.
**Fields:** Meeting date/time; duration; venue + virtual link; meeting type; chair (dropdown); scribe; quorum rule displayed (read-only, from `[CCA CONFIG]`); agenda lock time `[DERIVED]`; distribution list.
**Actions:** Accept · Return with reason (dropdown: incomplete evidence / wrong meeting / question unclear / duplicate / not required — with free text) · Defer (reason + awaited item + expected date + auto re-list) · Reorder · Allocate time · Assemble packs · Lock agenda · Distribute agenda · Add ad-hoc case (permission-gated).
**Chips:** Completeness; pack status; agenda lock status; capacity (within/over).
**Alerts:** Agenda over-capacity; a case listed without an assigned radiology/pathology reviewer where review was requested; urgent case not listed within its target interval `[CCA CONFIG]`; quorum forecast not met based on RSVPs — **MDT-030 [PRODUCT]**: the coordinator must see a quorum *forecast* before the meeting, not discover non-quoracy during it.
**Downstream:** Agenda lock → case packs frozen, distribution to participants, calendar invitations, reviewer tasks, patient-facing notification where configured.
**Print/export:** Agenda; per-case pack (PDF); attendance sheet.

---

## C.7.3 · `SCR-MDT-003` — Case Pack (assembled view)
**Role:** All participants; Chair; presenter.
**Navigation:** From agenda; from the live meeting screen; from the patient record.
**Purpose:** Present all evidence for one case in a single reviewable artifact, generated from live data (`MDT-111`).
**Sections (fixed order):** 1 Patient identifiers & demographics · 2 Question(s) · 3 Cancer episode & diagnosis · 4 Pathology (synoptic summary + full report link) · 5 Biomarkers · 6 Imaging (reports, lesion table, viewer links) · 7 Staging (cTNM and pTNM, side by side) · 8 Performance status & comorbidities · 9 Current medications · 10 Prior treatment (systemic with cumulative doses, RT with delivered dose, surgery with pathology) · 11 Response history · 12 Toxicity history · 13 Outstanding investigations · 14 Trial options `[CCA CONFIG]` · 15 Patient preferences · 16 Prior MDT recommendations and action status · 17 Submitter's summary.
**Tables:** as per each section's canonical structure elsewhere in this document set.
**Chips:** Data freshness per section; "assembled at [timestamp]"; "frozen at agenda lock".
**MDT-112 [PRODUCT]** — the pack displays the timestamp at which it was assembled and flags any evidence item that has changed since assembly, so the meeting is never discussing a superseded fact without knowing it.
**Actions:** Present (full-screen) · Refresh from record (re-assembles, logs the refresh) · Add annotation (participant-attributed, not part of the record) · Export.
**Print/export:** Case pack PDF with page-numbered sections.

---

## C.7.4 · `SCR-MDT-004` — Live Meeting / Minute Capture

| Dimension | Specification |
|---|---|
| **Role(s)** | MDT Coordinator (scribe, primary write); Chair (adjudicate); participants (declare attendance, contribute dissent). |
| **Navigation** | Agenda → Start meeting. |
| **Purpose** | Capture attendance, quorum, discussion, options, recommendation, rationale, consensus, dissent and actions — in real time, in a structure that survives audit. |
| **Header** | Meeting strip: meeting type, date, chair, elapsed time, quorum chip, current case n of m, case timer. Patient header for the current case (full clinical). |
| **Sections/tabs** | Attendance · Case list (navigable) · Current case: [Pack | Discussion | Recommendation | Actions] · Meeting close. |
| **Fields — Attendance** | Per participant: Name (auto); Discipline (dropdown, product-defined backbone + `[CCA CONFIG]`); Role in meeting (Core / Extended / Observer / Presenter / Chair / Scribe); Attendance status (Present in person / Present remotely / Absent — apologies / Absent — no apologies / Delegated to [named person]); Arrival time; Departure time (for partial attendance — **MDT-040 [PRODUCT]**: a participant who leaves before a case is discussed must not be counted toward that case's quorum); Conflict of interest declared (checkbox + detail). Add ad-hoc attendee. |
| **Fields — Discussion (per case)** | Presenter (auto/editable); Discussion started/ended (auto timestamps); **Evidence reviewed** (checklist, each with reviewer attribution: Imaging reviewed — by [radiologist]; Pathology reviewed — by [pathologist]; Prior treatment reviewed; Toxicity reviewed; Comorbidities considered; Patient preferences considered; Trial options considered — each Y/N with comment; **MDT-041 [PRODUCT]**: imaging/pathology "reviewed" requires the named reviewing specialist to be recorded as present); Discussion narrative (rich text, scribe-entered, R); Key points (repeating). |
| **Fields — Options considered** | Repeating group: Option (text + optional coded modality); Proposed by; Arguments for; Arguments against; Evidence cited; Selected (radio — exactly one across the group, or "none — further information required"); Reason not selected (R for non-selected options) — **MDT-042 [PRODUCT]**: options considered and rejected must be recorded with reasons; a minute showing only the chosen option is not an MDT record. |
| **Fields — Recommendation** | Recommendation narrative (R); Structured recommendation: Responsible specialty (dropdown, R); Treatment intent (dropdown, R); Recommended modality sequence (ordered multiselect: Surgery / Systemic / Radiotherapy / Combined chemoradiation / Best supportive care / Observation / Further investigation / Trial); Recommended systemic regimen (link to Regimen Master, optional); Recommended RT (site, intent, optional); Recommended surgery (procedure, intent, optional); Further investigations required (linked orderables, repeating); Referrals required (repeating); Trial recommended (dropdown of open trials); Re-discussion required (checkbox + trigger + expected date); Patient discussion required (checkbox + who); Prognosis discussion flagged (checkbox); Rationale (R, narrative — **must be separate from the recommendation text**); Guideline/evidence reference `[CCA CONFIG]`. |
| **Fields — Consensus & dissent** | Consensus (radio — product-defined: Unanimous / Majority / No consensus — deferred / No consensus — chair decision); Dissent (repeating: dissenting participant (dropdown of present attendees), discipline, dissenting view (text, R), rationale (text), whether the dissenter wishes it recorded in distributed minutes (checkbox, default yes)) — dissent is enterable by the dissenter directly as well as by the scribe. |
| **Fields — Actions** | Repeating: Action description (R); Action type (dropdown — product-defined: Order investigation / Refer / Commence systemic therapy / Refer for RT / Schedule surgery / Obtain consent / Obtain further pathology / Re-list for MDT / Communicate to patient / Arrange appointment / Trial screening / Other); Owner (named user, R — **not a department**, `MDT-043 [PRODUCT]`); Owner role; Due date (R); Priority; Linked orderable/record; Notes. |
| **Tables** | Attendance table; case list with per-case status chip; options table; dissent table; actions table. |
| **Calculated** | Quorum met `[DERIVED]` (`CALC-081`) — rule, required disciplines, present disciplines, result, recomputed per case using presence at the time of that case; case elapsed time; meeting running time vs allocation; cases remaining. |
| **Actions** | Start meeting · Record attendance · Open case · Start/stop case timer · Save discussion · Add option · Add dissent · Add action · Mark case discussed · Defer case (reason + awaited item) · Next case · Close meeting · Route minutes to Chair. |
| **Chips** | Quorum (green met / red not met / amber met-with-caveat); Case status (Pending / In discussion / Discussed / Deferred / Not reached); Consensus; Dissent present; Actions assigned n. |
| **Alerts** | **Hard stop:** marking a case discussed with no recommendation and no deferral reason; assigning an action with no named owner or no due date. **Override with reason:** recording a recommendation while quorum is not met (`MDT-131`); recording "imaging reviewed" when no radiologist is present. **Warning:** case exceeding allocated time; meeting exceeding scheduled duration with cases unreached. |
| **Conditional logic** | Regimen/RT/surgery recommendation sub-panels appear per selected modality. Re-discussion date field appears on checkbox. Dissent section always available, never hidden. Deferral requires awaited item and expected availability. |
| **Read-only** | Case pack content; quorum derivation; attendance-derived eligibility to be recorded as a reviewer. |
| **Sign/approve** | The scribe saves; **the Chair signs** (`SCR-MDT-005`). Nothing here is consumable downstream until chair signature. |
| **Amendment/version** | Draft minutes editable until chair signature. Post-signature amendment per `MDT-250` with reason, prior version retained, consumers notified. |
| **Current vs previous** | For re-discussions, the previous recommendation and its action-completion status are pinned alongside the current discussion. |
| **Post-signature** | Minutes immutable; recommendation written to the episode as an `MDT RECOMMENDATION` object; actions dispatched; distribution executed. |
| **Downstream queues** | Action owners' task inboxes; Treatment Plan screen pre-populated with the recommendation (`SCR-PLN-001`); Navigator pathway milestone; submitting clinician notified; Radiology/Pathology/Surgery/RT queues per action type. |
| **Blocked/error** | Meeting cannot close while any listed case is neither discussed nor deferred. Loss of connectivity must preserve entered minute text locally and re-sync — **MDT-044 [PRODUCT]**. |
| **Print/export** | Draft minutes (watermarked); attendance sheet. |

---

## C.7.5 · `SCR-MDT-005` — Chair Review & Sign-off
**Role:** MDT Chair.
**Navigation:** Chair worklist → Minutes awaiting signature.
**Purpose:** Verify and authorise.
**Sections:** Meeting summary · Case-by-case review (rendered in the mandated order) · Quorum attestation · Dissent verification · Action review · Signature.
**Rendered order per case (fixed, `MDT-050 [PRODUCT]`):** QUESTION → EVIDENCE REVIEWED (with reviewer names) → DISCUSSION → OPTIONS CONSIDERED (with reasons rejected) → RECOMMENDATION → RATIONALE → CONSENSUS → DISSENT → ACTION OWNER(S) & DUE DATES → CHAIR SIGNATURE.
**Fields:** Quorum attestation (attest / record non-quorate override + reason); Per-case chair comment; Return-for-correction reason (dropdown per `MDT-240` + free text); Signature.
**Actions:** Approve case · Approve all · Return case for correction · Return meeting · Amend with chair attribution · **Sign**.
**Chips:** Per-case approval status; quorum; dissent present; days since meeting `[DERIVED]` against signing target `[CCA CONFIG]`.
**Alerts:** Warning if signing beyond the configured interval; hard stop if any case lacks a recommendation or deferral; hard stop if an action lacks an owner.
**Constraints:** Chair cannot silently edit discussion narrative (`MDT-201`); cannot remove dissent (`MDT-221`).
**Post-signature:** As above. **Print/export:** Signed MDT/Tumour Board Note (minutes) per Part P.

---

## C.7.6 · `SCR-MDT-006` — Action Tracker
**Role:** Coordinator, Chair, Navigator, action owners.
**Table columns:** Patient · UHID · Meeting date · Question · Recommendation (short) · Action · Type · Owner · Role · Due date · Status (Open / In progress / Completed / Overdue / Blocked / Cancelled — reason) · Days overdue `[DERIVED]` · Evidence of completion (linked record) · Escalation level · Last update.
**Actions:** Update status · Attach evidence · Reassign (with reason) · Escalate · Close · Cancel with reason · Re-list for MDT.
**Alerts:** Overdue at configured thresholds escalating to owner → owner's supervisor → Chair `[CCA CONFIG]`; action blocked by an unavailable prerequisite.
**MDT-060 [PRODUCT]** — an action can only be closed with either a linked record demonstrating completion or an explicit "completed without record" attestation with reason.
**Print/export:** Action status report by meeting, by owner, by patient.

---

# C.8 — TREATMENT PLAN SCREENS

## C.8.1 · `SCR-PLN-001` — Treatment Plan

| Dimension | Specification |
|---|---|
| **Role(s)** | MO / RO / SO (create and sign, per modality ownership); all clinical (view); Navigator, Pharmacy, Finance (view). |
| **Navigation** | Consultation → "Create treatment plan"; MDT recommendation → "Convert to plan"; patient header → Treatment Plan tab. |
| **Purpose** | Convert a diagnosis and an MDT recommendation into a signed, versioned, multimodality intention that all downstream ordering derives from. |
| **Header** | Full clinical header + plan strip: plan version, status, intent, responsible specialty, date signed, MDT linkage. |
| **Sections** | 1 Basis of plan · 2 Diagnosis & staging snapshot · 3 Treatment intent & goals · 4 Modality sequence · 5 Systemic component · 6 Radiotherapy component · 7 Surgical component · 8 Supportive & ancillary care · 9 Monitoring plan · 10 Expected duration & milestones · 11 Consent requirements · 12 Patient discussion · 13 Financial implications · 14 Sign. |
| **Fields** | **Basis:** Derived from MDT (checkbox + linked MDT record, auto-populating the recommendation read-only); Deviation from MDT recommendation (checkbox → mandatory reason, and **notification back to the MDT Coordinator and Chair** — `PLN-010 [PRODUCT]`); Basis if not MDT (dropdown: Not required per pathway / Urgent — MDT to follow / Patient declined MDT pathway / Second opinion / Emergency). **Diagnosis snapshot:** auto, read-only, frozen at signature (site, laterality, histology, grade, cTNM, pTNM, biomarkers, disease status, line of therapy). **Intent & goals:** Treatment intent (dropdown — product-defined: Curative / Neoadjuvant / Adjuvant / Definitive chemoradiation / Palliative — life-prolonging / Palliative — symptom control / Maintenance / Consolidation / Best supportive care, R); Goals of treatment (narrative + structured multiselect); Expected benefit discussed (text); Prognosis discussed (Y/N + date + narrative). **Modality sequence:** ordered repeating group — Sequence number; Modality (dropdown); Planned start (date or relative: "after cycle 3", "6–8 weeks post-op"); Planned duration; Dependency (dropdown: none / after completion of step n / concurrent with step n / conditional on response); Owning specialty; Status `[DERIVED]` (Planned / In progress / Completed / Cancelled / Modified). **Systemic component:** Regimen (link to Regimen Master with version, R if systemic in sequence); Intent; Line; Planned number of cycles; Cycle length; Planned start date; Dose modifications planned upfront (with reason, e.g. organ dysfunction); Route/access requirement (peripheral acceptable / central required); Required baseline investigations (auto from regimen master + additions); Required ongoing monitoring (auto + additions). **RT component:** Site(s); Intent; Modality; Planned total dose and fractions (indicative — the authoritative prescription lives in `SCR-RO-002`); Concurrent systemic therapy (Y/N + regimen); Planned start. **Surgical component:** Planned procedure; Site/laterality; Intent; Planned timing; Prerequisites. **Supportive:** Antiemetic strategy `[CCA CONFIG]`; Growth factor support (Y/N + criteria); Anti-infective prophylaxis; Bone-modifying therapy; Fertility preservation; Nutrition; Psychosocial; Palliative care referral; Dental assessment where indicated `[CCA CONFIG]`; Cardiac monitoring plan; Vaccination `[CCA CONFIG]`. **Monitoring:** Repeating — investigation, frequency, trigger, owner. **Duration & milestones:** Expected total duration `[DERIVED]`; Key milestone dates `[DERIVED]`; Planned response assessment points (after cycle n / at week n / post-RT + n weeks). **Consent:** Required consents (auto per modality and `[CCA CONFIG]`) with status per consent. **Patient discussion:** Attendees; Interpreter; Materials issued (with versions); Patient decision (dropdown: Agreed / Agreed with modifications / Declined / Deferred / Seeking second opinion); Patient-stated preferences. **Financial:** Estimate required (checkbox → routes to Finance); High-cost drug flag `[DERIVED]`. |
| **Tables** | Modality sequence; monitoring schedule; consent requirements (consent type, required by, status, obtained date, version, obtained by); required baseline investigations with status `[DERIVED]`; MDT linkage history. |
| **Dropdowns** | Intent, modality, dependency, patient decision (product-defined); regimen, consent types, supportive protocols, monitoring catalogue (`[CCA CONFIG]`). |
| **Calculated** | Expected duration; milestone dates; baseline investigation completeness `[DERIVED]`; high-cost flag; cycles × cycle length projection; planned end date. |
| **Actions** | Import MDT recommendation · Save draft · Add modality step · Reorder sequence · Attach consent requirement · Request financial estimate · Order baseline investigations (launches `SCR-INV-001` pre-filled) · Print patient plan summary · **Sign** · Create new version. |
| **Chips** | Plan status (Draft / Active / Superseded / Completed / Abandoned); per-step status; consent status; MDT-concordance (Concordant / Deviation — reason); baseline readiness. |
| **Alerts** | **Hard stop on sign:** no intent; no modality sequence; systemic component selected without a regimen; MDT required by pathway rule and neither present nor overridden. **Warning:** plan intent inconsistent with recorded stage (rule `[CCA CONFIG]`); deviation from MDT recommendation without reason; consent requirement unmet at planned start date; baseline investigation not ordered. |
| **Conditional logic** | Modality sub-sections render only when that modality is in the sequence. Fertility panel per age/intent. Cardiac monitoring auto-required when the selected regimen carries the flag `[CCA CONFIG]`. Deviation reason mandatory on the deviation checkbox. |
| **Read-only** | Diagnosis/staging snapshot; MDT recommendation; regimen master content; derived dates. |
| **Sign/approve** | Responsible clinician signature with re-authentication. Multimodality plans may require per-modality sign-off by the owning specialty `[CCA CONFIG]` — **PLN-020 [PRODUCT]**: the systemic component is signed by MO, the RT component acknowledged by RO, the surgical component by SO; the plan displays which components are signed and by whom. |
| **Amendment/version** | Any clinically meaningful change creates **Version n+1**; the prior version is retained, viewable and marked `SUPERSEDED`. The version in force at the time of any order is stamped on that order. Version change requires reason (dropdown: response / toxicity / progression / patient choice / comorbidity / MDT re-discussion / error correction / resource availability). |
| **Current vs previous** | Side-by-side version comparison with changed fields highlighted; a version timeline showing what changed, when and why. |
| **Post-signature** | Plan becomes the authority for ordering: the Treatment Order screen can only select regimens consistent with the active plan version, or requires an explicit off-plan reason — **PLN-030 [PRODUCT]**. |
| **Downstream queues** | Systemic component → MO ordering queue; RT component → RO referral queue (`SCR-RO-001`); Surgical component → SO scheduling queue; consents → consent capture tasks; baseline investigations → ordering; Finance → estimate queue; Navigator → pathway milestones; Pharmacy → advance notice of high-cost drug requirement. |
| **Empty/blocked** | Blocked without an active episode, without a recorded stage where the pathway requires one, or without a diagnosis basis. |
| **Print/export** | Treatment Plan (clinical); Patient Treatment Plan Summary (lay version, `PTP-*`); Financial estimate input. |

## C.8.2 · `SCR-PLN-002` — Plan Version Comparison
**Purpose:** Make plan evolution legible.
**Layout:** Two-column diff (any two versions), plus a vertical timeline of all versions.
**Columns:** Field · Version A value · Version B value · Changed · Change reason · Changed by · Changed at.
**Actions:** Select versions · Export comparison · Restore field values into a new version (never overwriting a signed version).

## C.8.3 · `SCR-PLN-003` — Consent Capture
**Role:** Clinician (obtain), nurse (witness where configured), patient (sign).
**Navigation:** From plan, order, surgery scheduling, RT prescription, trial enrolment, procedure.
**Purpose:** Capture procedure/treatment-specific informed consent as a versioned artifact tied to the thing consented to.
**Fields:** Consent type (dropdown `[CCA CONFIG]`); Template + version (auto, read-only, displayed); Procedure/treatment consented to (auto-linked to the specific plan/order/prescription — **PLN-040 [PRODUCT]**: consent is linked to a specific clinical object, never a free-floating "chemotherapy consent"); Risks discussed (checklist from template, each acknowledged); Benefits discussed; Alternatives discussed (including no treatment); Questions answered; Information material issued (version); Interpreter used (Y/N + name/service + language); Capacity assessed (Y/N + assessor + basis); Consent given by (Patient / Legal representative — with relationship and authority basis); Patient signature (capture); Clinician name/signature; Witness (conditional); Date/time; Validity period `[CCA CONFIG]`; Withdrawal (date, reason, recorded by).
**Chips:** Consent status (Not required / Pending / Obtained / Expired / Withdrawn / Declined); Template version currency (flag if a newer template version exists).
**Alerts:** Warning if consent template has been superseded since capture (`NAV-040` analogue); hard stop on treatment administration without valid consent where the rule requires it `[CCA CONFIG]`.
**Downstream:** Consent chip on every relevant screen; readiness criterion; Day Care pre-administration check; theatre checklist.
**Print/export:** Signed consent form (patient copy + record copy).

---

# C.9 — SYSTEMIC TREATMENT ORDER SCREENS
*Exceptional depth per instruction. The five-value dose model (`GEN-DOS-001`) is realised visually here.*

## C.9.1 · `SCR-ORD-001` — Regimen Selection

| Dimension | Specification |
|---|---|
| **Role(s)** | Medical Oncologist; trainee (draft only, no signature); Pharmacist (view). |
| **Navigation** | Treatment Plan → "Create treatment order"; clinic worklist → "New cycle"; previous cycle → "Order next cycle"; MDT action item. |
| **Purpose** | Select the correct regimen, version, cycle and day-set, and establish the patient dosing context before any dose is calculated. |
| **Header** | Full MO header, plus an order strip: intent, line, regimen (once selected), cycle n of m, planned date, order status. |
| **Sections** | 1 Plan context · 2 Regimen search & selection · 3 Regimen detail (read-only from master) · 4 Cycle context · 5 Patient dosing context · 6 Continue to dosing. |
| **Fields — Plan context** | Active treatment plan version (read-only, linked); On-plan / off-plan (radio) — off-plan requires reason (dropdown + text) per `PLN-030`; Treatment intent (auto from plan, overridable with reason); Line of therapy (auto `[DERIVED]`, confirmable). |
| **Fields — Regimen selection** | Search (text, searches name, drug components, disease, protocol code); Filter by disease site / intent / line / modality; Regimen (select from Regimen Master `[CCA CONFIG]`, R); Regimen version (auto — **latest active version**, with an information alert if a newer version exists than the one used in prior cycles of this course — `ORD-010 [PRODUCT]`); Protocol source/reference (read-only from master); Regimen status (Active / Inactive / Under review — inactive regimens are selectable only with permission and reason). |
| **Fields — Regimen detail (read-only from master, displayed in full before selection is confirmed)** | Regimen name; alternative names; protocol code; disease/indication; intent(s); line(s); cycle length (days); planned number of cycles; treatment days within cycle (e.g. D1, D8, D15); drug list with dose basis, standard dose, unit, route, diluent, volume, rate/duration, sequence, treatment block; mandatory premedication; mandatory hydration; mandatory supportive care; required baseline investigations; required ongoing monitoring; dose-modification rules `[CCA CONFIG]`; cumulative dose ceilings for tracked agents; special handling flags (vesicant, central access required, cardiac monitoring, extended observation); regimen version, effective date, approver, change history. |
| **Fields — Cycle context** | Cycle number (numeric, R — defaulted to previous + 1 `[DERIVED]`, editable with reason); Total planned cycles (from plan, editable with reason); Day(s) being ordered (multiselect from the regimen's treatment days, R); Planned administration date(s) (date per day, R — defaulted from last administration + cycle length `CALC-021`, editable); Treatment location (dropdown: Day Care unit / Ward / Home `[CCA CONFIG]`); First cycle (Y/N `[DERIVED]`); Delay from planned date `[DERIVED]` in days, with reason field appearing when > configured tolerance `[CCA CONFIG]`. |
| **Fields — Patient dosing context (all read-only imports with source dates; this is the evidence panel for the dose)** | Height (value, unit, date, method, age in days, staleness chip); Weight (value, unit, date, method, condition qualifier, delta from previous, delta from the weight used in the last cycle); **Dosing weight** (selector per `INT-NUR-115` — Actual / Adjusted / Ideal / Clinician-specified, with the formula named and the resulting value shown, R); BSA (value, unit, **formula name**, inputs used with their dates, capping applied Y/N with uncapped and capped values per `INT-NUR-131`); Renal function — serum creatinine (value, unit, date), creatinine clearance `[DERIVED]` (**formula named**, inputs shown including which weight was used, `CALC-100`), eGFR `[DERIVED]` (`CALC-101`); Hepatic function — bilirubin total/direct, AST, ALT, ALP, albumin (each value, unit, date, flag); Haematology — Hb, WBC, ANC (with derivation source per `LAB-040`), platelets (each value, unit, date, flag); Electrolytes where regimen-relevant; Cardiac function (LVEF or equivalent, method, date) where the regimen requires it; Pregnancy status where applicable (status, test result, test date); Cumulative prior exposure for each tracked agent (cumulative dose, unit, % of configured ceiling `[DERIVED]`, `CALC-102`); Prior infusion reactions to any component (agent, cycle, grade, management, rechallenge outcome); Active toxicities relevant to this regimen (term, grade, date); Current dose modifications in force (from prior cycles). |
| **Tables** | Regimen drug list (read-only preview); prior cycles of this course (cycle, date, doses administered, dose intensity `[DERIVED]`, toxicity, delays); cumulative exposure table (agent, cumulative dose, unit, ceiling, % of ceiling, monitoring status). |
| **Dropdowns** | Regimen (`[CCA CONFIG]`); location (`[CCA CONFIG]`); dosing weight basis (product-defined, formulae `[CCA CONFIG]`); off-plan reason, delay reason, cycle-override reason (product-defined + `[CCA CONFIG]`). |
| **Calculated** | Cycle number default; next-cycle due date; delay in days; BSA; CrCl; eGFR; ANC; cumulative exposure and % of ceiling; dose intensity of prior cycles; staleness of every imported value against the regimen's configured freshness windows `[CCA CONFIG]`. |
| **Actions** | Search · Preview regimen · Select regimen · Change dosing weight basis · Refresh clinical data (re-imports and shows what changed) · Continue to dosing · Cancel. |
| **Chips** | Regimen version currency; staleness per imported value (fresh / approaching expiry / expired); cumulative exposure band; prior reaction present; first cycle; delayed cycle. |
| **Alerts** | **Hard stop:** required baseline investigation for this regimen absent `[CCA CONFIG]`; required biomarker absent or negative where the regimen requires it; no weight within the configured window on a first cycle. **Override with reason:** cumulative exposure at/above configured ceiling; expired staleness on a value the regimen requires; regimen inactive; cycle number out of sequence. **Warning:** newer regimen version available; weight changed beyond threshold since last cycle (`INT-NUR-111`); prior infusion reaction to a component of this regimen — **displayed as a persistent banner, not a dismissible toast** (`ORD-020 [PRODUCT]`). |
| **Conditional logic** | Cardiac function panel appears only for regimens flagged as requiring it. Pregnancy panel by sex/age/`[CCA CONFIG]`. Carboplatin-style AUC dosing exposes the renal function panel as mandatory rather than informational. Delay-reason field appears past tolerance. |
| **Read-only** | All regimen master content; all clinical imports; all derived values. **ORD-030 [PRODUCT]** — regimen master content is never editable from the order screen. A clinician who needs different content changes the dose on the order (recorded as a variance) or requests a master change; they can never silently alter the protocol. |
| **Sign/approve** | None at this stage; selection is a draft state. |
| **Downstream** | Proceeds to `SCR-ORD-002`. Creates a draft order visible in "Orders & Signatures Pending". |
| **Blocked** | No active plan and no off-plan permission; no active episode; regimen master unavailable. |
| **Print/export** | Regimen information sheet (clinician); patient regimen information (`PTP-130`). |

---

## C.9.2 · `SCR-ORD-002` — Dosing Panel (the five-value screen)

| Dimension | Specification |
|---|---|
| **Role(s)** | Medical Oncologist (edit + sign); Pharmacist (view, and later annotate on `SCR-PHA-002`); Day Care nurse (view). |
| **Navigation** | From `SCR-ORD-001` → Continue to dosing. |
| **Purpose** | Establish, per drug, the standard dose, the calculated dose, and the final ordered dose — with every variance explicit and reasoned. |
| **Header** | Order strip + a **persistent dosing-context bar**: dosing weight (value, basis, date), height (value, date), BSA (value, formula, capped Y/N), CrCl (value, formula), all with staleness chips. This bar is fixed and visible while scrolling — **ORD-040 [PRODUCT]**. |
| **Layout — the core requirement** | A **drug row grid**, one row per medication, with the five dose values rendered as **five distinct, separately-labelled, non-adjacent-in-meaning columns**, each with its own visual treatment: `STANDARD` (grey, read-only, from master) → `CALCULATED` (blue, read-only, derived) → `FINAL ORDERED` (black, editable, bold — the clinician's decision) → `PHARMACY PREPARED` (populated later, greyed/empty at ordering with the label "pending pharmacy") → `ADMINISTERED` (populated later, "pending administration"). The last two columns are **present but empty** at ordering time, so that the clinician sees the full chain and no one ever mistakes the ordered dose for the administered dose — **ORD-050 [PRODUCT]**. Column headers are never abbreviated to "Dose". |
| **Table — drug rows: exact columns** | 1 Sequence (numeric, drag-reorderable) · 2 Treatment block (dropdown: Premedication / Hydration — pre / Anticancer / Hydration — post / Supportive / Rescue / Growth factor / Other — product-defined) · 3 Drug (from Formulary Master, read-only if from regimen; addable rows selectable) · 4 Formulation/strength · 5 Dose basis (dropdown: mg/m² / mg/kg / fixed dose / AUC / units/m² / units/kg / mg/m²/day / other — product-defined) · 6 **STANDARD DOSE** (value + unit, read-only from regimen master, with the master version stamped) · 7 Dosing parameter used (BSA / weight / AUC target / none — read-only, showing the actual numeric value used) · 8 **CALCULATED DOSE** `[DERIVED]` (value + unit, read-only; `CALC-110`; expandable to show `standard × parameter = result` with the parameter's source date) · 9 Dose modification % (numeric, ±, editable) · 10 Modification reason (dropdown — product-defined categories: Haematological toxicity / Non-haematological toxicity / Renal impairment / Hepatic impairment / Performance status / Age / Weight change / Prior reaction / Comorbidity / Patient preference / Protocol-specified reduction / Physician judgement / Other — plus free text, R when % ≠ 0) · 11 Rounding applied `[DERIVED]` (per Dose Rounding Rules `[CCA CONFIG]`, showing pre- and post-rounding values, `CALC-111`) · 12 **FINAL ORDERED DOSE** (numeric, editable, R) · 13 Dose unit (dropdown, defaulted, R) · 14 Variance from calculated `[DERIVED]` (% and absolute; `CALC-112`) · 15 Variance reason (R when variance exceeds configured tolerance `[CCA CONFIG]`) · 16 Route (dropdown) · 17 Diluent (dropdown from compatibility master `[CCA CONFIG]`) · 18 Diluent volume (numeric + unit) · 19 Target concentration (numeric + unit, where clinically ordered; otherwise `[DERIVED]` and shown read-only, `CALC-113`) · 20 Infusion rate (numeric + rate unit dropdown: mL/h / mg/min / mg/kg/h / units/h) · 21 Duration (numeric + unit — **rate, volume and duration are mutually constrained; entering any two derives the third and the screen must show which was entered and which was derived**, `ORD-060 [PRODUCT]`, `CALC-114`) · 22 Day(s) of cycle · 23 Date · 24 Time (planned) · 25 Special instructions (text) · 26 **PHARMACY PREPARED DOSE** (empty at ordering) · 27 **ADMINISTERED DOSE** (empty at ordering) · 28 Row actions (edit, remove — with reason for regimen-derived rows, duplicate, add note). |
| **Additional fields per row (expandable)** | Cumulative dose after this cycle `[DERIVED]` (`CALC-115`) with % of ceiling; vesicant/irritant flag (read-only from formulary); light protection required; filter required; central access required; maximum rate constraint `[CCA CONFIG]`; stability window; incompatible co-administrations `[CCA CONFIG]`. |
| **Sections beyond the drug grid** | 1 Dosing context bar (above) · 2 Anticancer drugs · 3 Premedication · 4 Hydration · 5 Antiemetics · 6 Supportive therapy · 7 Growth factors · 8 Rescue/emergency medications · 9 Sequencing & timing diagram · 10 Order-level instructions · 11 Variance summary · 12 Review & sign (→ `SCR-ORD-004`). |
| **Sequencing & timing diagram** | A horizontal timeline rendering the ordered sequence with each item's start offset, duration and overlap, so that sequence errors are visible rather than inferred from row numbers — **ORD-070 [PRODUCT]**. Displays total chair time `[DERIVED]` (`CALC-116`). |
| **Dropdowns/value sets** | Treatment block, dose basis, modification reason, variance reason, route, rate unit, dose unit (product-defined backbones, `[CCA CONFIG]` extensions); drug (Formulary Master `[CCA CONFIG]`); diluent (Compatibility/Stability Master `[CCA CONFIG]`); rounding rule set (`[CCA CONFIG]`). |
| **Calculated** | Calculated dose; rounding; variance %; concentration; the third of rate/volume/duration; cumulative dose; total chair time; total fluid volume `[DERIVED]`; dose intensity vs protocol `[DERIVED]` (`CALC-117`). Every calculation is expandable to show inputs, formula, source timestamps and rounding rule applied (per the Part E contract). |
| **Actions** | Add drug row · Remove row (reason required for protocol rows) · Apply dose modification to all anticancer rows (with single reason) · Recalculate (explicitly, showing what changed) · Apply supportive care set `[CCA CONFIG]` · Reorder sequence · Save draft · Preview patient schedule · Continue to review & sign · Cancel order. |
| **Chips** | Per row: protocol-derived vs added; modified (with %); variance beyond tolerance; vesicant; central access required; cumulative ceiling approaching/exceeded. Order level: draft; variance summary count. |
| **Alerts** | **Hard stop:** final ordered dose empty; dose unit absent; a dose exceeding the configured absolute maximum for that drug `[CCA CONFIG]`; ordering a drug to which the patient has a recorded allergy; rate exceeding the configured maximum rate; incompatible diluent per the compatibility master. **Override with reason:** variance from calculated dose beyond tolerance; cumulative dose exceeding ceiling; dose increase above protocol standard; omission of a mandatory protocol drug (e.g. removing a mandatory premedication) — **ORD-080 [PRODUCT]**: removing a protocol-mandated supportive medication requires an override with reason and is displayed on the pharmacy and nursing views. **Warning:** dosing parameter stale; weight changed since the parameter was calculated; prior reaction to this drug; interaction with current medications. |
| **Conditional logic** | AUC-based rows expose target AUC and the renal function inputs; the calculated dose formula displayed changes accordingly. Rows flagged central-access-required check the vascular access record and warn if unsuitable (`MAR-040`). Rate/volume/duration constraint logic per `ORD-060`. Rounding rules apply per drug and per formulation `[CCA CONFIG]`. |
| **Read-only** | Standard dose; calculated dose; rounding derivation; variance; concentration when derived; cumulative dose; all clinical context. |
| **Sign/approve** | Not here — signature occurs on `SCR-ORD-004`. |
| **Amendment/version** | Draft edits are free. See `SCR-ORD-005` for post-signature modification. |
| **Downstream** | Continues to review & sign. |
| **Empty/error/blocked** | Blocked if the formulary or compatibility master is unavailable — **the screen must refuse to calculate rather than calculate with a stale or partial master** (`ORD-090 [PRODUCT]`). |
| **Print/export** | Draft order preview (watermarked). |

---

## C.9.3 · `SCR-ORD-003` — Supportive Care, Premedication & Hydration Detail
**Role:** MO. **Navigation:** From dosing panel section links.
**Purpose:** Ensure protocol-mandated supportive care is explicit, timed and complete rather than assumed.
**Sections:** Antiemetic regimen · Premedication · Hydration (pre/post) · Growth factor · Anti-infective prophylaxis · Rescue/emergency medications · Take-home supportive medications · Instructions.
**Fields per item:** Drug; formulation; dose; unit; route; timing relative to the anticancer drug (numeric offset + unit + before/after/concurrent, R); duration; frequency; number of doses; day(s); mandatory per protocol (read-only flag); omitted (checkbox + reason, per `ORD-080`); dispensing location (in-unit / take-home / ward).
**Take-home supportive medications:** additionally quantity, refills, instructions to patient, counselling required — routes to Pharmacy dispensing.
**Rescue/emergency medications:** the set required to be available at the chairside per protocol `[CCA CONFIG]` (e.g. reaction management kit) — listed as an availability requirement checked at administration, not as an administered order.
**Alerts:** Missing mandatory antiemetic for a regimen with a configured emetogenic classification `[CCA CONFIG]`; hydration volume inconsistent with the protocol; growth factor ordered on a day that conflicts with the protocol's timing rule.
**Downstream:** Pharmacy preparation and dispensing; Day Care administration record; patient take-home prescription.

---

## C.9.4 · `SCR-ORD-004` — Order Review & Signature

| Dimension | Specification |
|---|---|
| **Role(s)** | Medical Oncologist (sign); trainee (submit for co-signature). |
| **Navigation** | From dosing panel → Review & sign. |
| **Purpose** | Present the complete order in a single reviewable, print-faithful layout and capture the authorising signature. |
| **Header** | Full clinical header + order strip. |
| **Sections** | 1 Patient & episode verification · 2 Regimen & cycle · 3 Dosing context (with formulas and source dates) · 4 Full order table (all rows, all five dose columns) · 5 Sequencing diagram · 6 Variance summary · 7 Readiness snapshot · 8 Consent status · 9 Attestations · 10 Signature. |
| **Fields** | Verification checkboxes (product-defined, each individually recorded): patient identity confirmed; episode and diagnosis correct; regimen and version correct; cycle and day correct; dosing parameters reviewed and current; doses reviewed; variances reviewed and justified; supportive care reviewed; allergies reviewed; cumulative exposure reviewed; readiness reviewed. Order validity/expiry (date — **ORD-100 [PRODUCT]**: every order carries an expiry beyond which it cannot be administered without re-authorisation `[CCA CONFIG]`). Order-level notes to pharmacy. Order-level notes to nursing. Signature (re-authenticated). |
| **Tables** | The complete order table exactly as it will appear to pharmacy and nursing — **ORD-110 [PRODUCT]**: the signing clinician must see the order in the same layout the downstream roles will see, not a different summary view. Variance summary table: drug · standard · calculated · final ordered · variance % · reason · attested. Readiness snapshot table (from `SCR-RDY-001`): criterion · result · date · pass/fail/override. |
| **Calculated** | All doses; total chair time; total volume; expected end time; next cycle due date `[DERIVED]`; order expiry. |
| **Actions** | Back to dosing · Print preview · Save draft · **Sign and release to pharmacy** · Sign and hold (signed but not released — for orders written in advance) · Submit for co-signature · Cancel order. |
| **Chips** | Draft / Signed / Released / Held / Superseded / Cancelled / Expired. Readiness chip. Consent chip. |
| **Alerts** | **Hard stop on sign:** any mandatory verification checkbox unchecked; unjustified variance beyond tolerance; consent absent where required; readiness failed without a recorded clinician override; order date in the past beyond tolerance; trainee attempting to release without co-signature (`MO-CON-050`). **Warning:** signing an order for a date more than n days ahead `[CCA CONFIG]`; readiness data will be stale by the administration date. |
| **Sign/approve** | Signature with re-authentication. On signature: **every calculated and imported value in the order is frozen by value** per `GEN-SIG-003` — BSA, dosing weight, CrCl, labs, cumulative doses, regimen master version, rounding rules version. |
| **Amendment/version** | A signed order cannot be edited. Changes create **Order Version n+1** via `SCR-ORD-005`, which supersedes the prior version. The superseded version remains fully viewable with a `SUPERSEDED` chip and a link to its successor. **ORD-120 [PRODUCT]** — if the superseded version had already been prepared by pharmacy, the new version must display that fact and the pharmacy must be actively notified, not merely presented with a new queue item. |
| **Current vs previous** | Version comparison view: row-by-row diff of the two order versions with changed cells highlighted and change reasons listed. |
| **Post-signature** | Order becomes read-only and consumable. Appears in Pharmacy verification queue, Day Care treatment queue, patient's treatment schedule, billing charge trigger `[CCA CONFIG]`, and the Treatment Summary source data. |
| **Downstream queues & state transitions** | `SIGNED` → (release) `RELEASED-TO-PHARMACY` → Pharmacy queue (`SCR-PHA-001`). If signed-and-held: `SIGNED-HELD`, no pharmacy queue entry until released. Day Care queue entry created at release with pharmacy status `Not yet verified`. |
| **Blocked** | Cannot release to pharmacy if the administration date exceeds the order expiry; cannot release if the patient has an active treatment hold without an override. |
| **Print/export** | Signed Treatment Order (full, print-faithful, showing all five dose columns with the last two labelled "pending"); patient treatment schedule; pharmacy worksheet. |

---

## C.9.5 · `SCR-ORD-005` — Dose Modification / Order Revision
**Role:** MO.
**Navigation:** From a signed order → "Modify"; from post-cycle review; from a pharmacy query response; from readiness failure.
**Purpose:** Change a signed order safely, with reason, versioning and downstream notification.
**Sections:** Current order (read-only) · Proposed changes · Reason · Impact · Review & sign.
**Fields:** Modification scope (radio: This cycle only / This and subsequent cycles / All future cycles — **ORD-130 [PRODUCT]**: scope must be explicit, because a dose reduction intended permanently must not silently revert next cycle); Per-row new values; Reason (dropdown as `SCR-ORD-002` column 10, R); Toxicity linkage (select the toxicity record driving the reduction, where applicable — creates the audit link between toxicity and dose change); Effective from (cycle/date); Notes to pharmacy/nursing.
**Impact panel `[DERIVED]`:** cycles affected; new dose intensity vs protocol; cumulative dose projection; whether pharmacy has already prepared (with the preparation's status and BUD).
**Alerts:** Hard stop on modifying an order already administered (must be documented as an administration variance instead — `MAR-*`); warning if pharmacy has prepared; warning if the modification would take dose intensity below a configured threshold `[CCA CONFIG]`.
**Downstream:** New order version; pharmacy notified with prior preparation status; nursing notified; toxicity record annotated; Treatment Summary updated.

## C.9.6 · `SCR-ORD-006` — Treatment Hold / Delay / Discontinuation
**Role:** MO (decide); pharmacist/nurse (view).
**Sections:** Decision type · Clinical basis · Scope · Resumption criteria · Communication · Sign.
**Fields:** Decision (radio — product-defined: Delay this cycle / Hold treatment / Discontinue regimen / Discontinue all systemic therapy / Change regimen); Reason (dropdown — product-defined categories: Haematological toxicity / Non-haematological toxicity / Infection / Organ dysfunction / Progression / Patient choice / Comorbidity / Surgical or procedural / Social/logistical / Resource unavailability / Death / Other — with free text, R); Linked toxicity record(s); Effective date; Expected duration (for delay/hold: numeric + unit, or "until criteria met"); Resumption criteria (structured repeating: parameter, threshold, source — **ORD-140 [PRODUCT]**: "resume when counts recover" must be enterable as a checkable criterion, not narrative, so that readiness can evaluate it); Review date (R); Reviewing clinician; Cumulative doses at discontinuation `[DERIVED]`; Best response achieved (for discontinuation); Next plan (dropdown: New line / Radiotherapy / Surgery / Best supportive care / Surveillance / Referral / Undecided); Patient informed (Y/N, date, by whom, understanding).
**Actions:** Save draft · Sign decision · Cancel existing hold (with reason) · Reschedule affected appointments.
**Chips:** Active hold (purple per `GEN-WLQ-003`); delay days `[DERIVED]`; resumption criteria met/not met `[DERIVED]`.
**Downstream:** Episode state → `TREATMENT INTERRUPTED` where configured; pending orders blocked with an explanatory blocked state naming the hold; Day Care and Pharmacy queues updated; appointments flagged for rescheduling; Navigator alerted; Treatment Summary records the event.
**Print/export:** Treatment Modification / Hold Decision Note (Part F).

## C.9.7 · `SCR-ORD-007` — Order Viewer (cross-role read-only)
**Role:** Pharmacist, nurse, RO, SO, inpatient clinician, Navigator.
**Purpose:** One canonical rendering of an order, identical for every role, differing only in which actions are available.
**Sections:** Identical to `SCR-ORD-004`, plus a live status column per row (Ordered → Verified → Prepared → Dispensed → Administered) and the populated `PHARMACY PREPARED` and `ADMINISTERED` columns as they fill.
**ORD-150 [PRODUCT]** — there must be exactly one order rendering shared across roles. Divergent role-specific order layouts are prohibited, because they are how transcription errors enter.
**Chips:** Version currency; superseded; expired; held.

---

# C.10 — TREATMENT READINESS / CYCLE CLEARANCE SCREENS

## C.10.1 · `SCR-RDY-001` — Treatment Readiness Assessment

| Dimension | Specification |
|---|---|
| **Role(s)** | System (evaluates); MO (reviews and decides); nurse and pharmacist (view); Navigator (view). |
| **Navigation** | From clinic worklist readiness chip; from the treatment-day clearance queue; from the order screen; from Day Care pre-administration; from Pharmacy verification. |
| **Purpose** | Present every prerequisite for this specific treatment on this specific day, with its source, value, date, threshold and outcome — as evidence, not as a verdict. |
| **Header** | Full clinical header + treatment strip: regimen, cycle/day, planned date/time, order version, location. |
| **Sections** | 1 Overall status · 2 Criteria table (grouped by category) · 3 Failed/needs-review detail · 4 Clinician decision · 5 History of prior cycles' readiness. |
| **Table — criteria (exact columns)** | 1 Category (Clinical review / Performance status / Symptoms / Toxicity / Haematology — CBC / ANC / Platelets / Haemoglobin / Renal function / Hepatic function / Electrolytes / Infection screen / Pregnancy / Cardiac / Protocol-specific monitoring / Consent / Vascular access / Financial clearance / Other) · 2 Criterion name · 3 Required for this regimen? (Y/N/Conditional — `[DERIVED]` from Regimen Master `[CCA CONFIG]`) · 4 Source record type (Lab result / Vitals / Clinical assessment / Imaging / Consent record / Order / Manual attestation) · 5 Source record link · 6 Source date/time · 7 Age in hours/days `[DERIVED]` · 8 Freshness window `[CCA CONFIG]` · 9 Within window? `[DERIVED]` · 10 Result value · 11 Unit · 12 Reference/threshold applied (**value + its source: regimen protocol / institutional default / trial protocol / clinician-specified — `RDY-010 [PRODUCT]`: the screen must name where the threshold came from**) · 13 Comparison operator · 14 Outcome `[DERIVED]` (Pass / Fail / Needs review / Pending / Not applicable / Not available) · 15 Clinician decision (Accept / Override / Defer / Order test) · 16 Override reason · 17 Decided by · 18 Decided at · 19 Comment. |
| **Fields** | Overall readiness `[DERIVED]` (`CALC-120`) — computed as: all mandatory criteria Pass → `READY`; any mandatory Fail → `NOT READY`; any Pending/Not available → `INCOMPLETE`; any override applied → `READY WITH OVERRIDE`. **The system never converts `NOT READY` to `READY` by itself; only a clinician override does that, and the resulting status is a distinct third state that remains visible on every downstream screen — `RDY-020 [PRODUCT]`.** Clinician decision (radio: Proceed / Proceed with dose modification (links to `SCR-ORD-005`) / Delay (links to `SCR-ORD-006`) / Hold / Discontinue / Order additional tests); Decision rationale (narrative, R when overriding); Signature. |
| **Calculated** | Per-criterion outcome; freshness; overall status; ANC where derived (`CALC-121`); CrCl (`CALC-100`); corrected calcium (`CALC-122`); days since last cycle; time to planned administration. |
| **Actions** | Refresh (re-evaluate against current data, showing what changed) · Order missing test (pre-filled `SCR-INV-001`) · Override criterion (individually, each with its own reason — **bulk override is prohibited, `RDY-030 [PRODUCT]`**) · Record manual attestation (for criteria with no electronic source, e.g. "clinically reviewed today") · Proceed to clearance · Delay/hold. |
| **Chips** | Per criterion: Pass (green) / Fail (red) / Needs review (amber) / Pending (blue) / Not applicable (grey) / Overridden (purple). Overall: Ready / Ready with override / Not ready / Incomplete. Freshness chips per row. |
| **Alerts** | **Hard stop:** proceeding while a criterion configured as non-overridable `[CCA CONFIG — CLINICAL SIGN-OFF]` has failed (e.g. positive pregnancy test where the regimen prohibits) — **RDY-040 [PRODUCT]**: the product must support criteria that no role can override. **Override with reason:** any other failed mandatory criterion. **Warning:** criteria that will expire before the planned administration time; results pending with a resulting time after the planned administration. |
| **Conditional logic** | The criteria set is derived per regimen, per cycle number (first-cycle-only criteria such as baseline cardiac function), per patient factors (pregnancy applicability, prior toxicity) and per trial protocol where enrolled (`TRL-010` — trial thresholds override institutional ones and the screen must say so). |
| **Read-only** | All source values, dates, thresholds and derivations. |
| **Sign/approve** | The readiness assessment is signed as part of the clearance decision (`SCR-RDY-002`), not separately. |
| **Amendment/version** | Readiness is re-evaluated whenever source data changes; each evaluation is retained with its timestamp. The evaluation **as at clearance** is frozen onto the clearance note and the administration record — `RDY-050 [PRODUCT]`. |
| **Current vs previous** | Prior cycles' readiness assessments accessible for comparison, showing which criteria have been repeatedly borderline. |
| **Downstream** | Feeds the clinic worklist chip, the Pharmacy verification screen, the Day Care pre-administration check and the clearance note. |
| **Empty/blocked** | If the regimen master defines no criteria set, the screen must display an explicit configuration error naming the gap rather than reporting "Ready" — **RDY-060 [PRODUCT]**. |
| **Print/export** | Readiness assessment record (criteria table with outcomes, thresholds and sources). |

## C.10.2 · `SCR-RDY-002` — Treatment-Day Clearance
**Role:** Medical Oncologist (or delegated clinician per `[CCA CONFIG]`).
**Navigation:** Clearance queue; from readiness; from Day Care request.
**Purpose:** Record the clinician's authorisation that this patient may receive this treatment today.
**Sections:** Patient & order verification · Interval history since last cycle (auto-generated) · Toxicity review · Readiness snapshot · Examination/assessment · Decision · Signature.
**Fields:** Interval history (auto: administrations, admissions, results, contacts, toxicity entries since last cycle — read-only, `MO-CON-060` analogue); Toxicity re-grading (each active toxicity presented for re-grading, R); Symptom review; Performance status (clinician-assessed, R); Focused examination; Readiness snapshot (read-only, frozen at decision); Decision (Proceed as ordered / Proceed with modification / Delay / Hold / Discontinue); Conditions attached to clearance (free text + structured, e.g. "proceed if platelets ≥ x on repeat" — **RDY-070 [PRODUCT]**: conditional clearance must be structured and machine-checkable at the point of administration, not narrative); Clearance validity (date/time window); Signature.
**Chips:** Cleared / Cleared with conditions / Not cleared / Cleared — expired.
**Alerts:** Hard stop on clearing without re-grading active toxicities; hard stop on clearing an order that has been superseded; warning if clearance is granted more than n hours before administration `[CCA CONFIG]`.
**Downstream:** Day Care queue clearance chip flips to `Cleared by [name] at [time]` (`MAR-010`); Pharmacy may proceed where policy gates preparation on clearance `[CCA CONFIG]`; conditions are carried to the administration screen as checkable items.
**Print/export:** Treatment-Day Review / Clearance Note (Part F).

---

# C.11 — ONCOLOGY PHARMACY SCREENS
*Exceptional depth per instruction: verification → preparation → double check → release.*

## C.11.1 · `SCR-PHA-001` — Pharmacy Worklist
Per B.12.B, seven tabs: Verification · Preparation · Prepared/Awaiting release · Queries & rejections · Oral dispensing · Cumulative surveillance · Wastage/returns/recalls.
**Columns (verification tab):** as B.12.B View 1, with **order BSA vs current BSA** dual display (`PHA-010`) and dose variance chip.
**Actions:** Open verification · Raise query · Reject · Verify · Send to preparation · Contact prescriber · Reprioritise (with reason).
**Alerts:** Order released with administration time inside the minimum preparation lead time `[CCA CONFIG]`; stock unavailable for a scheduled order; a prepared product approaching BUD expiry; an order superseded after preparation (`ORD-120`).
**Chips:** Order status; readiness; stock; preparation urgency `[DERIVED]` from administration time minus preparation duration.
**Empty state:** distinguishes "no orders released yet today" from "all verified".

---

## C.11.2 · `SCR-PHA-002` — Clinical Verification

| Dimension | Specification |
|---|---|
| **Role(s)** | Oncology Pharmacist. |
| **Navigation** | Worklist → Open verification. |
| **Purpose** | Independent clinical check of the order against the patient, before any product is compounded. |
| **Header** | Full pharmacist header per B.12.C — including order BSA vs current BSA, cumulative exposure, renal/hepatic/haematology with dates, allergies with prior infusion reactions, active toxicities, readiness result. |
| **Sections** | 1 Order summary (canonical `SCR-ORD-007` rendering) · 2 Patient parameter verification · 3 Independent dose recalculation · 4 Cumulative dose review · 5 Interaction & duplication review · 6 Allergy & prior reaction review · 7 Readiness & clearance review · 8 Supportive care completeness · 9 Route, diluent & compatibility review · 10 Per-row verification decisions · 11 Overall decision. |
| **Fields — parameter verification** | Height (displayed with source/date, verification checkbox); Weight (same, plus delta from order weight and from previous cycle); Dosing weight basis (displayed, checkbox); BSA (displayed with formula and inputs, checkbox); CrCl (displayed with formula and the weight used, checkbox); Relevant labs with dates and staleness (checkbox per panel). Each checkbox is an individually recorded verification act with timestamp — **PHA-020 [PRODUCT]**: "verified" must decompose into what was verified, not a single global tick. |
| **Fields — independent recalculation** | For each dose-based row, the system displays the pharmacist's independently recomputed calculated dose alongside the order's calculated dose (`CALC-110` recomputed from the frozen order inputs) and flags any discrepancy — **PHA-030 [PRODUCT]**. Pharmacist records agreement or raises a query. |
| **Table — per-row verification (exact columns)** | Sequence · Treatment block · Drug · Formulation · Dose basis · Standard dose · Calculated dose · Final ordered dose · Variance % · Variance reason (from order) · Pharmacist recalculated dose · Discrepancy `[DERIVED]` · Route · Diluent · Volume · Concentration `[DERIVED]` · Rate · Duration · Cumulative dose after this cycle `[DERIVED]` · % of ceiling · Compatibility status `[DERIVED]` from master · Stability window `[CCA CONFIG]` · Verification decision (dropdown: Verified / Verified with note / Query / Reject) · Note/reason · Verified by · Verified at. |
| **Fields — interaction review** | Interaction alerts (drug–drug, drug–disease, drug–lab, duplicate therapy), each with: interacting agents, severity `[CCA CONFIG]`, mechanism, recommendation, disposition (dropdown: No action — clinically acceptable / Monitor / Dose adjusted / Prescriber contacted / Order changed), disposition reason, recorded by/at. |
| **Fields — supportive completeness** | Checklist derived from the regimen master: mandatory antiemetics present, premedication present and correctly timed, hydration present, growth factor per protocol, rescue medications specified — each with present/absent/omitted-with-reason and pharmacist comment. |
| **Calculated** | Recalculated doses; discrepancies; concentrations; cumulative doses and % of ceiling; total volume; preparation time estimate; latest safe preparation start time `[DERIVED]` from administration time and stability (`CALC-130`). |
| **Actions** | Verify row · Verify all remaining · Raise query (row-level or order-level) · Reject order · Record intervention · Send to preparation · Print worksheet · Contact prescriber. |
| **Chips** | Per row: Verified / Query / Rejected / Pending. Order level: Awaiting verification / Partially verified / Verified / Query raised / Rejected. Discrepancy; cumulative ceiling; interaction severity; stability risk. |
| **Alerts** | **Hard stop on verification:** allergy to an ordered drug; dose exceeding the configured absolute maximum; incompatible diluent; order superseded or expired; order not signed; readiness failed with no clinician override; cumulative dose exceeding a hard ceiling `[CCA CONFIG — CLINICAL SIGN-OFF]`. **Override with reason:** cumulative approaching ceiling; variance beyond tolerance already justified by the prescriber (pharmacist records agreement or query); stale dosing parameter. **Warning:** newer regimen version; weight change since order; interaction alerts. |
| **Conditional logic** | AUC rows expose the renal calculation for explicit verification. Vesicant rows expose the vascular access record and require an access-suitability check. Rows requiring central access block verification if access is documented unsuitable, pending prescriber response. |
| **Read-only** | The entire order (pharmacy never edits a prescriber's order — **PHA-040 [PRODUCT]**: pharmacy proposes changes via query; only the prescriber changes the order). All clinical data. All master content. |
| **Sign/approve** | Verification is a signed act with re-authentication, recording the verifying pharmacist, timestamp, and the itemised verification decisions. |
| **Amendment/version** | If the order is superseded after verification, the verification is invalidated and the new version re-enters the queue flagged `RE-VERIFICATION REQUIRED — PRIOR VERSION PREPARED?` with the preparation status shown (`ORD-120`). |
| **Current vs previous** | Prior cycles' verification records and interventions accessible; recurring interventions surfaced. |
| **Post-signature** | Order state `VERIFIED`; enters preparation queue; Day Care pharmacy chip updates. |
| **Downstream** | Preparation queue (`SCR-PHA-004`); query → prescriber task inbox; rejection → prescriber + Day Care + Navigator. |
| **Blocked** | Cannot verify without the compatibility/stability master; cannot verify an order for a patient with an active untreated hold. |
| **Print/export** | Pharmacy verification record; preparation worksheet. |

## C.11.3 · `SCR-PHA-003` — Query / Rejection / Intervention
**Fields:** Type (dropdown — product-defined: Clarification / Dose query / Regimen query / Missing supportive care / Interaction / Allergy concern / Cumulative dose concern / Renal or hepatic dosing / Stability or compatibility / Access route / Stock unavailable / Administrative); Severity/urgency; Row(s) affected; Description; Recommendation (with proposed alternative dose/drug/route); Evidence/reference `[CCA CONFIG]`; Raised by/at; Directed to (named prescriber); Method of contact; Response received (text, by whom, at what time, `[DERIVED]` response interval); Outcome (dropdown: Order changed / Order confirmed unchanged / Order cancelled / Escalated / No response — escalated); Intervention accepted (Y/N — for pharmacy governance reporting); Closure.
**Downstream:** Prescriber task inbox with escalating reminders `[CCA CONFIG]`; Day Care informed of delay; Navigator if the treatment date is at risk; intervention register for governance.
**Print/export:** Pharmacy Query/Intervention Note.

## C.11.4 · `SCR-PHA-004` — Preparation Specification
**Role:** Pharmacist (specify), technician (execute).
**Purpose:** Convert a verified order into a compounding instruction with every physical parameter defined.
**Table — per product, exact columns:** Order row · Drug · Final ordered dose · Dose unit · Vial strengths available `[INTEGRATION inventory]` · Vials required `[DERIVED]` (`CALC-131`) · Volume to draw `[DERIVED]` (`CALC-132`) · Overfill handling · Diluent (from compatibility master) · Diluent volume · Final volume · **Prepared concentration** `[DERIVED]` (`CALC-133`) · Concentration within permitted range? `[DERIVED]` `[CCA CONFIG]` · Container type (dropdown: PVC bag / non-PVC bag / glass bottle / syringe / elastomeric device / other) · Administration set/filter required (dropdown) · Light protection (Y/N) · Storage condition (dropdown: room temperature / refrigerated / frozen) · **BUD (beyond-use date/time)** `[DERIVED]` from stability master `[CCA CONFIG]` (`CALC-134`) · Stability basis/reference · Hazardous handling class `[CCA CONFIG]` · Preparation priority · Assigned hood/isolator · Assigned compounder · Assigned checker.
**Fields:** Preparation notes; special instructions; transport requirement (cold chain, light-protected, spill kit); batch preparation grouping (where multiple patients' products are prepared in one session — each product remains individually traceable, `PHA-050 [PRODUCT]`).
**Alerts:** Concentration outside permitted range → hard stop; BUD earlier than the planned administration time → hard stop with the shortfall stated; container incompatible with the drug `[CCA CONFIG]` → hard stop.
**Downstream:** Compounding record.

## C.11.5 · `SCR-PHA-005` — Compounding Record
**Role:** Compounding pharmacist/technician.
**Purpose:** Traceable record of what was physically made.
**Table — per product:** Drug · Lot/batch number (scanned, R) · Manufacturer · Expiry date (R, validated as future) · Vial strength · Vials opened · Volume drawn per vial · Total drug volume · Diluent lot/expiry · Diluent volume added · Final volume · Final container lot where applicable · **Prepared dose (actual)** — this is dose value #4 in the five-value model (R) · Prepared concentration `[DERIVED]` · Wastage volume `[DERIVED]` · Wastage amount (drug units) `[DERIVED]` · Wastage reason (dropdown — product-defined: Vial overfill / Partial vial not reusable / Dose rounding / Preparation error / Contamination / Expired during preparation / Order cancelled after preparation / Other) · Prepared by (auto) · Preparation start/end time · Environment (hood/isolator ID) · In-process checks performed (checklist).
**Calculated:** Prepared concentration; wastage; deviation of prepared dose from final ordered dose `[DERIVED]` (`CALC-135`) with tolerance `[CCA CONFIG]` — **PHA-060 [PRODUCT]**: any deviation beyond tolerance requires pharmacist review before release, and the deviation is displayed to nursing on the administration screen.
**Alerts:** Expiry date in the past → hard stop; lot number not scanned where scanning is configured → hard stop; prepared dose deviating beyond tolerance → blocked pending pharmacist review.
**Downstream:** Double check.

## C.11.6 · `SCR-PHA-006` — Independent Double Check
**Role:** Second pharmacist/technician (must differ from compounder per `GEN-AUD-004`).
**Purpose:** Independent verification of the physical product against the order.
**Checklist (each item individually recorded, product-defined):** Patient identifiers on label match order · Drug identity matches order · Vial lot and expiry verified · Dose calculation independently recomputed and matches prepared dose · Volume drawn verified (by syringe-pullback, volumetric or gravimetric method — method recorded) · Diluent identity and volume verified · Final volume verified · Container type verified · Concentration verified · Light protection applied where required · Filter/set specified · Label content verified against order · BUD verified against planned administration time · Storage condition applied.
**Fields per item:** Checked (Y/N), discrepancy found (text), resolution, checker identity, timestamp.
**Fields overall:** Check outcome (Passed / Passed after correction / Failed — remake required); Checker signature.
**Alerts:** Hard stop if the checker is the compounder; hard stop on release if any item unchecked; a failed check creates a remake task and a discrepancy record.
**Downstream:** Labelling and release.

## C.11.7 · `SCR-PHA-007` — Labelling
**Purpose:** Define exactly what appears on the product label — a patient-safety artifact.
**Required label content (product-defined minimum, `PHA-070 [PRODUCT]`):** Patient full name; UHID; date of birth or age; ward/unit/chair; **regimen name, cycle and day**; drug name (generic, prominent); **final ordered dose and prepared dose where they differ**; total volume; diluent; route (prominent); infusion rate and duration; sequence number within the regimen; date and time of preparation; BUD (date + time); storage condition; light-protection instruction; filter requirement; hazardous-drug warning; "cytotoxic — handle with care" per `[CCA CONFIG]`; prepared by; checked by; barcode/2D code encoding the product ID for administration scanning; order number and version.
**Actions:** Preview label · Print · Reprint (reason recorded) · Void label.
**Alerts:** Reprint requires reason; voided labels are audited.

## C.11.8 · `SCR-PHA-008` — Release / Dispense
**Fields:** Product(s) released (list); Release time; Released by; Destination (Day Care unit/bay / ward / clinic / patient — take-home); Transport method and conditions; Cold-chain record where applicable; Receiving person (name + role + signature/scan at destination — **PHA-080 [PRODUCT]**: receipt is captured at the destination, not asserted by pharmacy); Receipt time `[DERIVED]` transit duration; Condition on receipt; BUD remaining at receipt `[DERIVED]`.
**Chips:** Released / In transit / Received / Returned / Wasted.
**Alerts:** BUD remaining below a configured margin at receipt; product not received within a configured interval of release.
**Downstream:** Day Care product-receipt screen (`SCR-MAR-004`); order state → `DISPENSED`.

## C.11.9 · `SCR-PHA-009` — Cumulative Dose Surveillance
**Table columns:** Patient · UHID · Agent (tracked per `[CCA CONFIG]`) · Cumulative administered dose `[DERIVED]` (`CALC-102`, computed from value #5, not #3, per `GEN-DOS-003`) · Unit · Ceiling `[CCA CONFIG]` · % of ceiling `[DERIVED]` · Doses contributing (expandable list with dates) · External/prior exposure recorded (Y/N + value + source) · Required monitoring (test, last value, date, due status) · Status chip · Last review.
**Actions:** Record prior/external exposure (with source document) · Flag for clinician review · Order monitoring test · Record clinician decision to exceed ceiling (with reason and signature).
**PHA-090 [PRODUCT]** — prior exposure received elsewhere must be enterable, because a cumulative ceiling computed only from doses given in this institution is dangerously wrong.

## C.11.10 · `SCR-PHA-010` — Wastage, Returns & Recalls
**Fields:** Event type (Wastage / Return from unit / Recall); Product; Lot; Quantity; Reason (dropdowns per type); Returned by; Received by; Condition; Disposition (Re-dispense — where permitted by stability rules / Quarantine / Destroy); Destruction witness; Documentation; Cost attribution `[CCA CONFIG]`.
**Recall-specific:** Recall notice reference; affected lots; patients who received affected lots `[DERIVED]` (traceable via the compounding record's lot capture — **PHA-100 [PRODUCT]**: lot-level traceability from vial to patient is a requirement, not an option); notification actions; clinician review.

---

## END OF DOCUMENT 4

**Continues in Document 5 — PART C, Section 3:** C.12 Day Care / MAR (identification → access → product verification → administration → reaction → discharge) · C.13 Toxicity / Adverse Events · C.14 Oral / Continuous Therapy.
