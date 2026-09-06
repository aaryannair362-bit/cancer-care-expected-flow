# CCA CANCER CARE — ONCOLOGY HIS + EMR
# MASTER FUNCTIONAL & CLINICAL PRODUCT REQUIREMENT INVENTORY
## Document 2 of N — PART B continued: Roles 7–21

**Conventions carried forward from Document 1:** `[PRODUCT]`, `[CCA CONFIG]`, `[CCA CONFIG — CLINICAL SIGN-OFF]`, `[DERIVED]`, `[INTEGRATION]`. All cross-cutting platform rules (GEN-*) apply to every role in this document without restatement — in particular GEN-AUD-001/002 (attribution and non-destructive edit), GEN-SIG-001/003 (signature model and frozen-value rule), GEN-DSP-002 (superseded display), GEN-ALT-001 (alert tiers), GEN-WLQ-001/003 (worklist and chip conventions), GEN-DOS-001 (five-value dose principle).

---

## B.7 — RADIOLOGIST

### B.7.A Role purpose

**Why this role uses the system.** The Radiologist interprets imaging in an oncological frame of reference. In a cancer service, radiology output is not a narrative opinion — it is a *measurement dataset* that drives staging, response assessment, treatment continuation decisions and MDT recommendations. The system must therefore capture radiology as structured, comparable, lesion-level data, not only as report text.

**Clinical/operational responsibility owned.**
- Protocolling of oncological imaging requests (technique, contrast, phases, coverage) against the clinical question.
- Interpretation and structured reporting.
- Baseline lesion selection and measurement; target/non-target designation.
- Follow-up lesion measurement against the same baseline and the same measurement convention.
- Detection and reporting of new lesions.
- Proposed response category using the named criteria set.
- Detection and communication of critical/unexpected findings.
- Comparison against prior studies and reconciliation of external imaging.
- Addendum and amendment governance.

**Entry point.** On receipt of an imaging order from MO/RO/SO/Inpatient/MDT, or on referral of an external study for review.

**Where responsibility ends.** At report finalisation and, where applicable, documented communication of a critical result. The Radiologist **proposes** a response category; the treating clinician **confirms** it. The system must preserve both as distinct records — **RAD-010 [PRODUCT]**.

**Receives work from.** MO, RO, SO, Inpatient clinicians, MDT Coordinator (imaging review requests), Radiology Coordinator (scheduled/acquired studies), external referrers (outside studies for second read).

**Sends work to.** Ordering clinician (report + acknowledgement requirement), Response Assessment module (lesion measurements), MDT (imaging review record), Radiology Coordinator (protocol changes, repeat/recall), Interventional pathway (biopsy target recommendation), Pathology (image-guided biopsy correlation).

### B.7.B Role home / worklist / queue

Five views.

#### View 1 — Reporting Worklist

| Column | Type | Notes |
|---|---|---|
| Accession number | text | Barcode-searchable; primary identifier for the study |
| Patient name / UHID / age / sex | mixed | |
| Modality | coded | CT / MRI / PET-CT / PET-MRI / US / X-ray / Mammography / Nuclear medicine / Bone scan / Interventional |
| Body region / study name | coded | From Radiology Catalogue `[CCA CONFIG]` |
| Contrast | chip | None / IV / Oral / IV+Oral / Intrathecal / Other |
| Study date/time acquired | datetime | |
| Time since acquisition | `[DERIVED]` | Threshold colouring against reporting TAT target `[CCA CONFIG]` |
| Priority | chip | Routine / Urgent / STAT / Same-day / MDT-deadline. Value set `[CCA CONFIG]` |
| Clinical indication | text | From order — must be present, not "as per clinician" |
| Cancer episode / primary site | coded | |
| Purpose of study | chip | **Product-defined value set**: Diagnostic / Staging / Restaging / Response assessment / Surveillance / Complication assessment / Procedure planning / Image-guided procedure / Radiotherapy planning |
| Response criteria applicable | chip | Named criteria set `[CCA CONFIG]` — drives whether the structured lesion module is mandatory |
| Prior comparison available | chip + count | Lists prior studies with dates, auto-linked |
| Baseline study designated | chip | Yes (date) / No / Not applicable |
| Reporting status | chip | Unassigned / Assigned / Draft / Preliminary issued / Awaiting second read / Finalised / Addendum pending / Amended |
| Assigned radiologist | text | |
| Second read required | chip | `[CCA CONFIG]` rule-driven |
| Critical finding flag | chip | Raised / Communicated / Acknowledged |
| MDT-linked | chip | Study attached to an MDT case, with MDT date |
| Ordering clinician / department | text | |
| Quick actions | menu | Open viewer · Open report · Assign to me · Mark preliminary · Request prior · Raise critical finding · Return to coordinator (protocol/quality) · Attach to MDT |

**Filters:** modality, body region, priority, status, assigned radiologist, purpose of study, primary site, date range, critical-finding flag, MDT deadline, overdue TAT, second-read required, external study.

**Sorting:** priority then acquisition time (default); TAT overdue descending; MDT deadline.

**Drill-down:** opens the **Reporting Workspace** — a split view of image viewer `[INTEGRATION with PACS]`, structured reporting form, prior report panel and lesion-tracking table. **RAD-020 [PRODUCT]** — the prior report and prior lesion measurements must be visible *within* the reporting workspace without navigating away.

#### View 2 — Critical Findings Register
Every critical finding raised: patient, finding, raised by, raised at, communicated to (name + role), method (call/secure message/in-person), communication time, acknowledgement received, acknowledger, acknowledgement time, escalation events, closure. **RAD-030 [PRODUCT]** — a critical finding cannot be closed without a recorded, named, timestamped acknowledgement by a clinician.

#### View 3 — MDT Preparation List
Studies for cases on an upcoming MDT agenda, with MDT date, case question, images pre-loaded, whether radiology review note has been authored.

#### View 4 — Addenda / Amendments Pending

#### View 5 — External Study Reconciliation
Outside imaging received: source institution, study date, modality, media type (CD/DVD/upload/network), import status, reconciliation status (matched to patient/episode), whether formally re-reported, whether measurements re-derived for baseline use. **RAD-040 [PRODUCT]** — external studies used as a response-assessment baseline must be explicitly designated as baseline with the measuring radiologist recorded, because measurement convention differences materially affect derived percentage change.

### B.7.C Patient header for Radiologist

The Radiologist needs the clinical *question* and the treatment *context* — not the full chart.

**Displayed:** identifiers; age; sex; episode; primary site + laterality; histology; current clinical and pathological stage (both, distinguished); treatment intent; current treatment modality and phase (regimen + cycle/day, or RT site + fraction n/m, or post-op day n); date of last treatment administration (critical for timing interpretation, e.g. post-treatment inflammatory change); relevant biomarkers where they affect interpretation `[CCA CONFIG]`; clinical indication text from the order; specific question asked; prior imaging list with dates, modalities and links; designated baseline study; current target/non-target lesion set with prior measurements; prior surgery (procedure + date) and prior RT (site + dose + dates) — both essential for interpreting post-treatment change; renal function (creatinine + eGFR `[DERIVED]` with date) for contrast decisions; contrast allergy/prior reaction; pregnancy status where applicable; implanted devices (pacemaker/ICD, MR-conditional status) for MR safety; weight (for contrast dose and table limits); mobility/positioning constraints; diabetes/metformin status where local policy requires `[CCA CONFIG]`.

**Not displayed by default:** full narrative notes, MDT deliberation, prognosis, financial data.

### B.7.D Radiologist screens and fields

#### `RAD-100` — Study Protocolling screen

| Field | Type | Required | Notes |
|---|---|---|---|
| Accession | auto | — | System-generated |
| Requested study | coded (from Radiology Catalogue) | R | `[CCA CONFIG]` catalogue |
| Protocol assigned | dropdown | R | Protocol Master `[CCA CONFIG]`; product-defined structure |
| Contrast decision | radio | R | None / IV / Oral / Both / Other |
| Contrast agent | dropdown | C (if contrast) | Formulary-linked `[CCA CONFIG]` |
| Contrast volume | numeric | C | mL |
| Contrast rate | numeric | C | mL/s |
| Phases required | multiselect | C | `[CCA CONFIG]` |
| Coverage / anatomical extent | text + coded | R | |
| Renal function check | `[DERIVED]` display + acknowledgement | R if contrast | Shows creatinine, eGFR, date, staleness; threshold `[CCA CONFIG — CLINICAL SIGN-OFF]` |
| Contrast allergy check | `[DERIVED]` display + acknowledgement | R if contrast | Premedication protocol reference `[CCA CONFIG]` |
| Sedation/anaesthesia required | radio | O | |
| Special instructions to technologist | free text | O | |
| Protocolled by / at | auto | R | |
| Protocol change reason | dropdown + free text | C | If different from requested |

#### `RAD-200` — Structured Oncology Report

Sections (each with defined fields; full field dictionary in Part D and Part O):

1. **Study identification** — accession, study name, modality, date/time acquired, equipment/unit, technologist, site/location.
2. **Indication** — clinical indication (imported from order, read-only), specific question, cancer episode, purpose of study, response criteria applicable.
3. **Technique** — protocol used, sequences/phases performed, contrast agent, volume, route, rate, radiation dose index where applicable `[INTEGRATION]` (CTDIvol, DLP, or equivalent — canonical units in Part H), deviations from protocol with reason, image quality (dropdown: diagnostic / limited — reason / non-diagnostic — reason), limitations.
4. **Comparison** — prior study/studies used (accession, date, modality), whether external, baseline study designation.
5. **Findings — by organ/system.** Structured, template-driven per body region `[CCA CONFIG]` with product-defined structure: each organ/system carries a normal/abnormal toggle, and abnormal expands to structured descriptors.
6. **Lesion table** — the core oncological dataset. Per lesion:

| Field | Type | Notes |
|---|---|---|
| Lesion ID | auto | Persistent across the episode — **RAD-210 [PRODUCT]**: a lesion identifier once assigned is never reused or reassigned |
| Lesion label | text | Radiologist-assigned readable name |
| Organ / anatomical site | coded | `[CCA CONFIG]` anatomy value set, standard-terminology backed where available |
| Laterality | dropdown | Left / Right / Bilateral / Midline / Not applicable — **product-defined** |
| Lesion type | dropdown | Primary / Nodal / Metastatic / Indeterminate / Benign-incidental — product-defined |
| Target / Non-target / New | dropdown | Product-defined, criteria-driven |
| Measurable? | radio | Yes / No — with reason if no |
| Measurement method | dropdown | Long axis / Short axis (nodes) / Bidimensional / Volume — product-defined; which applies is driven by criteria set `[CCA CONFIG]` |
| Long axis | numeric | mm (canonical) |
| Short axis | numeric | mm |
| Third dimension | numeric | mm, conditional |
| Volume | numeric or `[DERIVED]` | cm³ |
| Series / image / slice reference | text | Required for reproducibility — **RAD-220 [PRODUCT]** |
| Measurement date | date | = study date |
| Measured by | auto | |
| Prior measurement(s) | display | Value + date + measurer for every prior timepoint |
| Absolute change from prior | `[DERIVED]` | mm |
| Percentage change from baseline | `[DERIVED]` | % |
| Percentage change from nadir | `[DERIVED]` | % |
| Lesion status | dropdown | New / Increased / Stable / Decreased / Resolved / Not evaluable — product-defined |
| Non-evaluable reason | dropdown + text | C |
| Metabolic parameter | numeric | Conditional for PET: SUVmax, SUVpeak, MTG/TLG where used `[CCA CONFIG]` |
| Comment | free text | O |

7. **Sum of target lesions** — `[DERIVED]` (see Part E). Displayed with baseline sum, nadir sum, current sum, % change from baseline, % change from nadir.
8. **Non-target lesion assessment** — dropdown per criteria set: Complete resolution / Persistent — non-progressive / Unequivocal progression / Not evaluable.
9. **New lesions** — yes/no; if yes, itemised with site and description; unequivocal vs equivocal.
10. **Treatment-related findings** — radiation change, post-surgical change, drug-related findings (pneumonitis, colitis, hepatotoxicity imaging correlates) `[CCA CONFIG]` value set, with severity descriptor.
11. **Incidental and non-oncological findings** — with actionability flag and recommended follow-up.
12. **Complications** — thrombosis, obstruction, perforation, haemorrhage, effusion, fracture, cord compression, etc. `[CCA CONFIG]`, each with critical-finding escalation option.
13. **Impression** — narrative, mandatory, must address the specific question asked.
14. **Proposed response category** — dropdown driven by named criteria set (product-defined structure; permitted categories `[CCA CONFIG]` per criteria set). Includes: criteria set name and version, proposed category, whether confirmation scan is required, radiologist's confidence/qualifier. **RAD-230 [PRODUCT]** — labelled explicitly as *proposed*; visually distinct from the treating clinician's confirmed response.
15. **Recommendations** — further imaging (type + interval), biopsy target recommendation, clinical correlation, MDT referral suggestion.
16. **Critical result** — flag, finding, communicated to, method, time, acknowledgement.
17. **Attestation** — reported by, credentials, preliminary vs final, second reader (where required), finalised date/time, addendum/amendment history.

**Required documents:** Structured Radiology Report; Preliminary Report; Addendum; Amended Report; Critical Result Communication Record; Radiology MDT Review Note; Image-Guided Procedure Report. All specified section-by-section in **PART O**.

---

## B.8 — RADIOLOGY COORDINATOR

### B.8.A Role purpose

**Why this role uses the system.** The Radiology Coordinator converts imaging *orders* into completed, reported *studies* — scheduling, preparation, patient instruction, contrast safety screening, acquisition tracking, repeat/recall management, external study import, and turnaround-time management against oncology deadlines (particularly MDT dates and treatment-decision dates, which are hard dates).

**Responsibility owned.** Order triage and scheduling; slot and modality capacity management; patient preparation instructions and confirmation (fasting, hydration, bowel prep, blood glucose for PET, metformin, sedation escort); safety screening (MR safety questionnaire, contrast screening, pregnancy screening, renal function availability); acquisition confirmation; repeat/recall; external image import and reconciliation; TAT monitoring; report distribution confirmation.

**Entry point.** On order placement. **Ends** at study finalisation and delivery of the report to the ordering clinician's inbox.

**Receives from.** Ordering clinicians, Nurse Navigator (urgency escalation), MDT Coordinator (deadline-driven imaging), Radiologist (protocol change, repeat request), Front Desk.
**Sends to.** Radiologist (acquired studies), patient (instructions), Front Desk (appointment), ordering clinician (report ready), Navigator (barriers, non-attendance), Financial Counsellor (authorisation).

### B.8.B Worklist views

1. **Unscheduled Orders** — order date, ordering clinician, patient, study, priority, clinical indication, purpose, requested-by date, MDT deadline `[DERIVED from linked MDT date]`, days waiting `[DERIVED]`, financial clearance, safety screening status, prerequisite status (e.g. creatinine required before contrast — with value/date/staleness), barrier flags.
2. **Scheduled** — appointment date/time, modality/unit, preparation instructions issued (yes/no/date/method), preparation confirmed by patient, transport/portering required, isolation precautions, sedation booked, escort confirmed.
3. **In Progress / Acquired Not Reported** — arrival time, acquisition start/end, technologist, images sent to PACS status `[INTEGRATION]`, exceptions.
4. **Repeats / Recalls / Incomplete** — reason (patient factor / technical / contrast reaction / motion / coverage / equipment fault — product-defined value set with `[CCA CONFIG]` extensions), rebooking status.
5. **TAT Monitoring** — order→schedule, schedule→acquisition, acquisition→preliminary, acquisition→final, against configured targets `[CCA CONFIG]`, with breach chips.
6. **External Studies Inbox** — as described in B.7.

### B.8.C Patient header for Radiology Coordinator

Operational subset: identifiers, age, sex, contact, preferred language, episode and primary site (for protocol relevance), ordered study and indication, priority, MDT deadline, mobility/transport needs, isolation precautions, weight (table/bore limits), implanted devices and MR-safety status, contrast allergy, renal function value + date, pregnancy screening status, diabetes/glucose (PET), sedation requirement, payer/authorisation status, inpatient vs outpatient and ward/bed. **Not displayed:** stage, biomarkers, prognosis, notes.

### B.8.D Key screens

| ID | Screen | Core fields |
|---|---|---|
| `RADC-100` | Order triage | Order details (read-only), priority confirmation/upgrade with reason, prerequisite checklist `[DERIVED]`, protocol referral to radiologist, hold with reason |
| `RADC-200` | Scheduling | Modality, unit, slot, duration, date/time, preparation set applied `[CCA CONFIG]`, sedation, escort, transport, interpreter, isolation, special equipment |
| `RADC-300` | Safety screening | MR safety questionnaire (item-level, `[CCA CONFIG]` item set, product-defined structure with per-item yes/no/unknown + detail + clearance outcome), contrast screening (prior reaction, asthma, renal function, metformin, thyroid therapy where relevant), pregnancy screening (applicable/not applicable + reason, LMP, test result/date), clearance decision, cleared by, date/time, restrictions |
| `RADC-400` | Preparation instruction issue | Instruction set + version, language, delivery method, delivered to, delivered at, confirmation received |
| `RADC-500` | Acquisition record | Arrival, start, end, technologist, unit, contrast administered (agent, volume, route, rate, lot/expiry, administered by, time), adverse contrast event (with link to reaction record), exceptions, images sent status |
| `RADC-600` | Repeat / recall | Reason, authorised by, additional exposure justification `[CCA CONFIG]`, rebooking |
| `RADC-700` | External import | Source, media, study date, modality, imported by, matched patient/episode, duplicate check, radiologist review requested, outcome |
| `RADC-800` | Report distribution | Report finalised, routed to ordering clinician inbox, navigator notified, MDT pack attached, patient copy issued (where policy permits `[CCA CONFIG]`), acknowledgement tracking |

---

## B.9 — PATHOLOGIST

### B.9.A Role purpose

**Why this role uses the system.** Pathology produces the *defining* dataset of an oncology record: the diagnosis itself, the grade, the pathological stage, margin status and the predictive biomarkers that determine drug eligibility. This must be captured as a **synoptic, discrete-field dataset**, not as a narrative paragraph, because it is consumed by staging logic, treatment-eligibility logic, MDT, registry export and the Treatment Summary.

**Responsibility owned.** Specimen accession and adequacy; gross examination and description; block/section management; histological diagnosis, morphology coding and grading; tumour dimensions and extent; margin assessment including individual margin distances; lymphovascular and perineural invasion; nodal counts; treatment effect and pathological response after neoadjuvant therapy; pT/pN/pM assignment; ancillary and molecular testing, methodology and interpretation; frozen-section/intra-operative consultation; addenda and amendments; critical/unexpected diagnosis communication.

**Entry point.** On specimen receipt or on request for intra-operative consultation. **Ends** at final report sign-out, including any addenda.

**Receives from.** Surgical Oncology (resection and biopsy specimens), Interventional Radiology (image-guided biopsies), MO (biomarker requests, re-biopsy), MDT (review requests, second opinion), external laboratories (referred blocks/slides).
**Sends to.** SO, MO, RO, MDT, Response Assessment (pathological response), Registry export, Pharmacy (biomarker-driven eligibility, indirectly via the clinical record).

### B.9.B Worklist views

1. **Accession / Receipt Queue** — accession number, patient, UHID, specimen(s) received, receipt date/time, requesting clinician, procedure, priority, container count, fixative, cold-ischaemia time `[DERIVED]` where recorded (critical for biomarker validity), discrepancy flags (mislabel, leak, absent requisition, insufficient fixative), adequacy.
2. **Grossing Queue** — cases awaiting gross examination, with specimen type, complexity, expected blocks, prosector assigned.
3. **Reporting Queue** — cases with slides available: accession, patient, specimen, procedure, primary site, priority, days since receipt `[DERIVED]`, TAT target `[CCA CONFIG]`, synoptic template required `[DERIVED]` from specimen + site, ancillary tests pending, status chip (Accessioned / Grossed / Processing / Slides ready / Draft / Awaiting ancillary / Awaiting second opinion / Signed out / Addendum pending / Amended), assigned pathologist, MDT deadline.
4. **Ancillary / Molecular Tracking** — test ordered, block used, method, sent date, internal/external lab, expected date, result received, interpretation status, days outstanding.
5. **Frozen Section / Intra-operative** — live queue: patient, theatre, surgeon, time received, question asked, time reported `[DERIVED]` turnaround, result communicated to (name), method, time.
6. **Amendments / Addenda / Critical Diagnoses.**

**Columns unique to pathology worklists:** accession, block count, slide count, stain set, decalcification (yes/type/duration — affects biomarker validity), cold ischaemia time, fixation duration, referral status, second-opinion status.

### B.9.C Patient header for Pathologist

Identifiers; age; sex; episode; known/suspected primary site; laterality; clinical stage; prior pathology (accession, date, diagnosis, morphology, grade — with direct link, essential for comparison and for confirming a new primary vs recurrence); **neoadjuvant treatment received** (regimen, cycles, completion date, and interval to surgery `[DERIVED]`) — mandatory for treatment-effect reporting — **PAT-010 [PRODUCT]**; prior radiotherapy to the specimen site; prior biomarker results (to avoid unnecessary repeat and to flag discordance); requesting clinician and the clinical question; operative findings summary and surgeon's orientation instructions; specimen inventory; relevant imaging findings; known germline/family history where relevant `[CCA CONFIG]`.

### B.9.D Pathology screens and the synoptic framework

**PAT-020 [PRODUCT]** — The product must implement a **generic synoptic oncology pathology framework**: a versioned template engine in which CCA defines disease-specific datasets as ordered collections of typed elements. Templates are `[CCA CONFIG — CLINICAL SIGN-OFF]`; the engine, element types, validation, versioning, rendering, staging derivation and downstream consumption are `[PRODUCT]`. Proprietary third-party datasets are not embedded; CCA supplies content under its own licensing.

**Element types the engine must support:** single-select, multi-select, numeric with unit, numeric range, free text, date, boolean, conditional group (shown only when a parent value matches), repeating group (e.g. per-margin, per-node-station, per-lesion), calculated element, coded element (standard-terminology backed), and "not applicable / cannot be assessed / not submitted" as universally available responses on every element — **PAT-030 [PRODUCT]**.

#### Core synoptic dataset (site-agnostic backbone — every template inherits this)

| ID | Element | Type | Notes |
|---|---|---|---|
| `PAT-100` | Accession number | auto | Unique, barcode |
| `PAT-101` | Specimen(s) received | repeating group | Per container: label as received, anatomical designation, laterality, orientation markers/sutures, fixative, container integrity |
| `PAT-102` | Procedure | single-select | Biopsy (core/incisional/excisional/endoscopic) / Resection (named) / FNA / Cytology / Lymph node dissection / Re-excision / Metastasectomy / Autopsy — product-defined backbone, `[CCA CONFIG]` extensions |
| `PAT-103` | Specimen site | coded | Topography value set, standard-terminology backed |
| `PAT-104` | Laterality | single-select | Left / Right / Bilateral / Midline / Not applicable — product-defined |
| `PAT-105` | Date/time of collection | datetime | |
| `PAT-106` | Date/time placed in fixative | datetime | Drives cold-ischaemia `[DERIVED]` |
| `PAT-107` | Cold ischaemia time | `[DERIVED]` | minutes; validity thresholds `[CCA CONFIG]` |
| `PAT-108` | Fixation duration | `[DERIVED]` | hours |
| `PAT-109` | Decalcification | conditional group | Performed y/n, agent, duration — flags biomarker validity |
| `PAT-110` | Gross description | narrative + structured | Dimensions of specimen (3 axes, mm), weight (g), appearance, tumour visible y/n, distance to nearest margin on gross, inking scheme, sectioning approach, blocks submitted (key, count) |
| `PAT-120` | Histological tumour type | coded | Morphology value set, standard-terminology backed `[CCA CONFIG]` per site |
| `PAT-121` | Histological grade | single-select | Grading system named + grade + component scores where the system is composite (product-defined structure; systems `[CCA CONFIG]`) |
| `PAT-130` | Tumour size — greatest dimension | numeric | mm; canonical |
| `PAT-131` | Additional dimensions | numeric ×2 | mm |
| `PAT-132` | Tumour focality | single-select | Unifocal / Multifocal (n foci, size of largest) / Diffuse |
| `PAT-133` | Tumour extent / local invasion | multi-select | Site-specific `[CCA CONFIG]`; drives pT |
| `PAT-140` | Margins — overall status | single-select | Negative / Positive / Cannot be assessed / Not applicable |
| `PAT-141` | Individual margins | repeating group | Per named margin: margin name `[CCA CONFIG]` per site, status (negative/positive/close/not assessable), distance to tumour (mm), type of tumour at margin (invasive/in-situ), extent of involvement (focal/extensive, mm) — **PAT-142 [PRODUCT]**: individual margin distances must be discrete numeric fields, never narrative only |
| `PAT-150` | Lymphovascular invasion | single-select | Present / Absent / Cannot be assessed / Indeterminate |
| `PAT-151` | Perineural invasion | single-select | Same value set |
| `PAT-160` | Lymph nodes examined | numeric | Integer, total |
| `PAT-161` | Lymph nodes positive | numeric | Integer; validation: ≤ examined |
| `PAT-162` | Nodes by station/level | repeating group | Station name `[CCA CONFIG]`, examined, positive |
| `PAT-163` | Size of largest metastatic deposit | numeric | mm |
| `PAT-164` | Extranodal extension | single-select | Present / Absent / Cannot be assessed / Not applicable; extent (mm) conditional |
| `PAT-165` | Isolated tumour cells / micrometastases | single-select | Where the site's staging system distinguishes them |
| `PAT-166` | Sentinel node information | conditional group | Number retrieved, mapping agent, status per node |
| `PAT-170` | Treatment effect | single-select + system | Applicable only when neoadjuvant therapy recorded. Named grading/regression system `[CCA CONFIG]` + grade + % viable tumour (numeric) + % fibrosis/necrosis |
| `PAT-171` | Pathological complete response | `[DERIVED]` + confirm | Derived per template rule `[CCA CONFIG]`; pathologist confirms |
| `PAT-172` | Residual tumour burden metrics | `[DERIVED]` | Where CCA configures a named index; inputs and formula per Part E |
| `PAT-180` | pT | single-select | Staging system + edition named; value set driven by system `[CCA CONFIG]` |
| `PAT-181` | pN | single-select | As above |
| `PAT-182` | pM | single-select | Assigned only where tissue confirmation exists; otherwise "not applicable — see clinical M" — **PAT-183 [PRODUCT]** |
| `PAT-184` | Prefix/suffix modifiers | multi-select | y (post-neoadjuvant), r (recurrent), a (autopsy), m (multiple) — product-defined, system-dependent |
| `PAT-185` | Pathological stage group | `[DERIVED]` | Derived from pT/pN/pM per the named staging system's table `[CCA CONFIG — the table]`; pathologist confirms or overrides with reason |
| `PAT-190` | Ancillary studies | repeating group | Test name, method (IHC/ISH/FISH/PCR/NGS/flow/other), antibody/clone/probe, block used, control validity, result value, units, scoring system named, score, interpretation (positive/negative/equivocal/not evaluable), cutoff applied `[CCA CONFIG]`, laboratory, accreditation reference `[CCA CONFIG]`, performed date, reported date, interpreting pathologist |
| `PAT-191` | Molecular / genomic results | repeating group | Panel name + version, gene, variant nomenclature, variant type, allele frequency, coverage, classification, actionability, method, platform, reference genome, laboratory, report attachment, germline vs somatic designation — **PAT-192 [PRODUCT]**: germline results require separate consent linkage and separate access permissions |
| `PAT-200` | Microscopic description | narrative | Optional per template `[CCA CONFIG]` |
| `PAT-210` | Comment / note | narrative | |
| `PAT-220` | Final diagnosis | narrative + coded | Coded morphology + topography mandatory alongside the narrative line |
| `PAT-230` | Critical / unexpected finding | conditional group | Finding, communicated to, method, time, acknowledged by, time |
| `PAT-240` | Consultation / second opinion | conditional group | Internal/external, consultant, date, opinion, concordance |
| `PAT-250` | Pathologist sign-out | signature | Name, credentials, registration `[CCA CONFIG]`, date/time |
| `PAT-260` | Addendum | repeating | Reason, content, author, date/time, signature |
| `PAT-261` | Amendment | repeating | Reason (product-defined value set: transcription error / additional material / revised interpretation / ancillary result changes diagnosis / patient identification error), prior version retained and viewable, notification to all prior consumers — **PAT-262 [PRODUCT]** |

#### `PAT-300` — Frozen Section / Intra-operative Consultation

Fields: request received time, surgeon, theatre, question asked, specimen(s), gross findings, sections examined, diagnosis rendered, result, time reported, communicated to (named person), method, read-back confirmation, deferred-to-permanent flag, concordance with final diagnosis `[DERIVED comparison]`, discordance reason. **PAT-310 [PRODUCT]** — frozen-section result must be recorded as a distinct object from the final report, and the system must generate a concordance record when the final report is signed.

**Required documents:** Surgical Pathology Report (synoptic + narrative); Cytopathology Report; Frozen Section Report; Biomarker/Ancillary Report; Molecular Report; Addendum; Amended Report; Second Opinion/Consultation Report; Pathology MDT Review Note. Full section specification in **PART N**.

---

## B.10 — MDT COORDINATOR

### B.10.A Role purpose

**Why this role uses the system.** The MDT Coordinator ensures that the right cases reach the right meeting with complete information, that the meeting is quorate, that decisions are captured accurately and completely, and — most importantly — that **recommendations are converted into actions with named owners and completion tracking**. An MDT recommendation that nobody actions is the most common failure mode in cancer services, and the software must prevent it structurally.

**Responsibility owned.** Case listing and agenda construction; completeness checking before listing; participant invitation and attendance recording; quorum determination; minute capture during discussion; action item assignment; chair sign-off routing; distribution of the signed record; action follow-up and closure; deferral management.

**Entry point.** On case submission by any clinician, or by pathway rule (e.g. all new diagnoses of a given site must be discussed `[CCA CONFIG]`).
**Ends.** When every action item from a discussed case is closed.

**Receives from.** All clinicians (case submissions), pathway rules engine (auto-listing), Navigator, Chair (returns for correction).
**Sends to.** All participants (agenda + case packs), Chair (for sign-off), action owners (task assignment), Navigator (coordination), submitting clinician (outcome), patient-facing communication where configured `[CCA CONFIG]`.

### B.10.B Worklist views

1. **Submissions Inbox** — submitted date, submitter, patient, episode, primary site, question asked, urgency, requested meeting, **completeness chip** `[DERIVED]`.

**MDT-010 [PRODUCT]** — Completeness is computed against a configurable per-meeting dataset requirement `[CCA CONFIG]`, and displayed item-by-item: histology confirmed (accession + date), biomarkers available (list, with pending items named), staging imaging available (modality + date), staging recorded (cTNM), performance status recorded (value + date), prior treatment recorded, comorbidities recorded, specific question stated. Incomplete cases can be listed only with a recorded override and reason.

2. **Meeting Agenda Builder** — meeting date/time, meeting type/tumour stream `[CCA CONFIG]`, venue/virtual link, expected duration, case order (drag), time allocation per case, case category (new diagnosis / post-operative / progression / complex management / re-discussion / trial screening / rapid-access), presenter assigned, radiology review required (yes → radiologist assigned + studies attached), pathology review required (yes → pathologist assigned + slides/blocks), deferred-from-previous flag.
3. **Live Meeting Screen** — attendance capture, quorum indicator `[DERIVED]`, current case, timer, case pack display, minute entry, outcome capture, action assignment.
4. **Post-Meeting** — cases pending chair sign-off, cases returned for correction, minutes distributed status.
5. **Action Tracker** — action, owner (named person + role), due date, status (Open / In progress / Completed / Overdue / Cancelled with reason / Blocked), days overdue `[DERIVED]`, evidence of completion (linked record), escalation events.
6. **Deferrals** — cases deferred with reason, awaited item, expected availability, re-listing date.

### B.10.C Patient header for MDT Coordinator

Operational-clinical subset: identifiers, age, sex, episode, primary site, laterality, histology, grade, cTNM/pTNM (both), biomarker availability status, performance status, prior treatment summary, current treatment status, referring/submitting clinician, question asked, urgency, previous MDT discussions (dates + recommendation summaries + action status), attached documents inventory, consent status, trial eligibility screening flag `[CCA CONFIG]`.

### B.10.D MDT Coordinator screens and fields

| ID | Screen | Fields |
|---|---|---|
| `MDT-100` | Case submission review | Submission (read-only), completeness checklist `[DERIVED]` per item with source record link, accept / return to submitter with reason / defer, meeting assignment, priority, time allocation |
| `MDT-110` | Case pack assembly | Auto-assembled from the record — **MDT-111 [PRODUCT]**: the case pack is generated from live data, never re-keyed. Contents: demographics, episode, diagnosis, pathology (synoptic summary + link), biomarkers, imaging (reports + viewer links + lesion table), staging, performance status, comorbidities, current medications, prior treatment with dates and doses, treatment response history, toxicity history, current question, submitter's summary narrative, outstanding investigations |
| `MDT-120` | Participant management | Invited participants: name, discipline (dropdown — product-defined backbone: Medical Oncology, Radiation Oncology, Surgical Oncology, Radiology, Pathology, Nuclear Medicine, Palliative Care, Nursing/Navigation, Pharmacy, Genetics, Trials, Allied Health, Other; `[CCA CONFIG]` extensions), role in meeting (core/extended/observer/presenter), attendance status (Present / Present remotely / Absent — apologies / Absent — no apologies / Delegated to [named]), arrival/departure time where partial attendance, conflict-of-interest declaration `[CCA CONFIG]` |
| `MDT-130` | Quorum determination | `[DERIVED]` — quorum rule is `[CCA CONFIG — CLINICAL SIGN-OFF]` (which disciplines, minimum counts, per meeting type). System displays: rule applied, disciplines required, disciplines present, quorum met yes/no, and **blocks final chair sign-off of recommendations made without quorum unless an explicit non-quorate override with reason is recorded — MDT-131 [PRODUCT]** |
| `MDT-140` | Minute capture | Per case: presenter, time started/ended, evidence reviewed (checkboxes with links: imaging reviewed by [radiologist], pathology reviewed by [pathologist], prior treatment reviewed, trial options considered), discussion narrative, options/alternatives considered (repeating: option, considered by, arguments for, arguments against, reason not selected), recommendation (structured + narrative), rationale, consensus status (Unanimous / Majority / No consensus — product-defined), dissent (repeating: dissenting participant, discipline, dissenting view, rationale) — **MDT-141 [PRODUCT]**: dissent must be recordable and must appear in the rendered minutes; it must never be silently discarded |
| `MDT-150` | Recommendation structuring | Responsible specialty (dropdown), treatment intent, recommended modality sequence (ordered multi-select), recommended systemic regimen (linked to Regimen Master, optional), recommended RT (site, intent), recommended surgery (procedure, intent), further investigations required (linked orderables), referrals required, trial consideration, re-discussion required (yes + trigger + expected date), patient discussion required, prognosis/goals discussion flagged |
| `MDT-160` | Action assignment | Repeating: action description, action type (dropdown: order investigation / refer / commence treatment / obtain consent / arrange appointment / obtain further pathology / re-list for MDT / communicate to patient / other), owner (named user), owner role, due date, priority, linked record, status, completion evidence, closed by/at |
| `MDT-170` | Chair routing & sign-off | Submit to chair, chair queue, return-for-correction with comments, chair signature capture |
| `MDT-180` | Distribution | Recipients (participants, submitter, treating team, referrer, navigator), method, sent date/time, acknowledgement tracking, patient copy `[CCA CONFIG]` |

**Required document: SIGNED MDT / TUMOUR BOARD NOTE (MINUTES)** — rendered in the mandated order: **QUESTION → EVIDENCE REVIEWED → DISCUSSION → OPTIONS CONSIDERED → RECOMMENDATION → RATIONALE → DISSENT → ACTION OWNER(S) → CHAIR SIGNATURE**. Full specification in **PART P**.

---

## B.11 — MDT CHAIR

### B.11.A Role purpose

**Why this role uses the system.** The Chair is the clinical guarantor of the meeting record. The Chair confirms that the recommendation as written reflects what the meeting actually decided, that the evidence base was adequate, that quorum was met, that dissent is fairly represented, and that actions are correctly owned. The Chair's signature converts a draft minute into an authoritative clinical instruction that other clinicians will act upon.

**Responsibility owned.** Meeting conduct and quorum; adjudication of consensus; accuracy of the recorded recommendation and rationale; approval or return of minutes; escalation of unresolved disagreement; oversight of overdue action items; governance reporting on meeting performance.

**Entry point.** At meeting start; formally at minute review. **Ends** at signature and at closure of escalated items.

**Receives from.** MDT Coordinator (draft minutes), participants (dissent, corrections).
**Sends to.** Coordinator (returns), action owners (via signed record), governance/administration (meeting metrics).

### B.11.B Worklist views

1. **Minutes Awaiting My Signature** — meeting date, tumour stream, case count, patient, question, recommendation summary, quorum status chip, dissent-present chip, completeness-override-used chip, days since meeting `[DERIVED]` against configured signing target `[CCA CONFIG]`.
2. **Returned to Coordinator** — with my comments, awaiting correction.
3. **Overdue Actions Across My Meetings** — action, owner, days overdue, patient, escalation status.
4. **Meeting Performance Dashboard** — cases discussed, quorate/non-quorate meetings, mean time meeting→signature, mean time recommendation→action completion, deferral rate, re-discussion rate, completeness-override rate. All `[DERIVED]`; targets `[CCA CONFIG]`.

### B.11.C Patient header for MDT Chair

Full clinical header equivalent to a treating oncologist's expandable panel (the Chair must be able to verify that the recommendation is clinically coherent), plus the meeting-specific block: question asked, evidence reviewed checklist with reviewer names, options considered, draft recommendation and rationale, consensus status, recorded dissent, proposed action owners, quorum computation with the rule displayed.

### B.11.D Chair screens

| ID | Screen | Behaviour |
|---|---|---|
| `MDT-200` | Minute review | Side-by-side: draft minute and source evidence. Chair can annotate but **cannot silently edit the discussion narrative** — corrections are made by return-to-coordinator or by a chair-attributed amendment with reason — **MDT-201 [PRODUCT]** |
| `MDT-210` | Quorum attestation | Displays rule, attendance, computed result; chair attests or records non-quorate override with reason |
| `MDT-220` | Dissent adjudication | Confirms dissent text as recorded, or requests correction from the dissenting participant; dissent cannot be removed by the Chair — **MDT-221 [PRODUCT]** |
| `MDT-230` | Sign-off | Signature with re-authentication; on signature the record becomes immutable, actions are dispatched to owners' task inboxes, the recommendation is written to the episode as an `MDT RECOMMENDATION` object consumable by Treatment Planning, and all recipients are notified |
| `MDT-240` | Return for correction | Structured reason (dropdown: factual error / incomplete evidence / recommendation unclear / owner not assigned / dissent misrepresented / quorum issue / other) + free text; returns to coordinator with audit |
| `MDT-250` | Amendment after signature | Permitted with reason; prior version retained and viewable; **all downstream consumers who acted on the prior version are notified** — **MDT-251 [PRODUCT]** |

---

## B.12 — ONCOLOGY PHARMACIST

*Given equal weight to Medical Oncology per instruction. Full module specification in PART J; role-level specification here.*

### B.12.A Role purpose

**Why this role uses the system.** The Oncology Pharmacist is the independent clinical check between prescribing and administration of drugs with a narrow therapeutic index and high harm potential. The pharmacist verifies that the order is clinically appropriate for *this* patient on *this* day — correct regimen, correct cycle and day, correct dose against the correct BSA/weight/renal function, appropriate given cumulative exposure, appropriate given labs and toxicity, free of significant interactions, with correct supportive care — and then governs safe preparation: diluent, volume, concentration, stability, beyond-use date, storage, light protection, filtration, container, labelling, second check, and release.

**Responsibility owned.** Clinical verification of the signed order; medication reconciliation and interaction review; cumulative-dose surveillance; dose-band and rounding policy application; preparation specification; compounding supervision and in-process checks; independent double check; batch/lot and expiry traceability; wastage accounting; labelling; release/dispensing; query and rejection back to the prescriber; recall management; adverse-drug-event reporting `[CCA CONFIG]`.

**Entry point.** On order release to pharmacy. **Ends** at dispensing/release to the administering area, and at post-administration reconciliation of wastage and returns.

**Receives from.** Medical Oncologist (signed orders), Day Care nurse (administration queries, returns, wastage), Inpatient clinicians, Radiation Oncology (concurrent chemotherapy orders), Intake/Labs (readiness data), Formulary/inventory `[INTEGRATION]`.
**Sends to.** Day Care / Inpatient nursing (verified and prepared products), Medical Oncologist (queries, rejections, dose recommendations), Billing, inventory, Navigator (supply delays affecting scheduling).

### B.12.B Worklist views

#### View 1 — Order Verification Queue

| Column | Type | Notes |
|---|---|---|
| Priority / scheduled administration time | time | Sorted ascending by default |
| Patient name / UHID / age / sex | mixed | |
| Location | chip | Day Care bay / Ward + bed / Outpatient |
| Diagnosis (short) + primary site | coded | |
| Regimen name + version | text | Regimen Master version stamped on order |
| Cycle / Day | text | `C3 D1` |
| Treatment intent | chip | Affects acceptable-risk judgements |
| Order status | chip | Awaiting verification / Under verification / Query raised / Rejected / Verified / In preparation / Prepared / Released / Administered / Cancelled / Returned |
| Order signed by / signed at | text/datetime | |
| Readiness status | `[DERIVED]` chip | Pass / Fail (n criteria) / Overridden by clinician (with reason on hover) / Pending |
| Key labs | value + date | ANC, platelets, Hb, creatinine + CrCl `[DERIVED]`, bilirubin, AST/ALT — each with staleness chip |
| Weight / BSA on order vs current | dual display | **PHA-010 [PRODUCT]** — shows order BSA and current BSA side by side with delta % where a newer weight exists |
| Allergy | chip | Substance-level, with prior infusion-reaction indicator |
| Cumulative exposure alerts | chip | Anthracycline/other tracked agents against configured ceilings `[CCA CONFIG]` |
| Dose variance from protocol | `[DERIVED]` chip | % variance of final ordered vs standard; colour-banded `[CCA CONFIG]` |
| Interaction alerts | count chip | |
| Preparation complexity / time required | `[DERIVED]` | For workload scheduling |
| Stock availability | chip `[INTEGRATION]` | Available / Partial / Unavailable — with expected availability |
| Financial clearance | chip | Where policy gates preparation `[CCA CONFIG]` |
| Quick actions | menu | Open verification · Raise query · Reject with reason · Verify · Send to preparation · View full order · Contact prescriber |

#### View 2 — Preparation Queue
Verified orders awaiting compounding: patient, drug(s), preparation sequence, hood/isolator assignment, compounder assigned, checker assigned, target start time (back-calculated from administration time and stability window `[DERIVED]`), stability/BUD countdown, special handling flags (hazardous, light-protected, cold chain, filter required).

#### View 3 — Prepared / Awaiting Release
Prepared products with BUD countdown chip, storage location, transport requirement, destination, release status.

#### View 4 — Queries & Rejections
Open queries with prescriber, raised at, response time `[DERIVED]`, escalation status.

#### View 5 — Oral / Take-home Dispensing
Oral anticancer prescriptions: drug, dose, quantity, refills remaining, counselling status, adherence review due, monitoring labs due, interaction review date.

#### View 6 — Cumulative Dose & Surveillance Register
Patients approaching or exceeding configured cumulative thresholds for tracked agents `[CCA CONFIG]`, with current cumulative dose `[DERIVED]`, threshold, % of threshold, required monitoring status (e.g. cardiac function date and value).

#### View 7 — Wastage, Returns and Recalls

### B.12.C Patient header for Oncology Pharmacist

The pharmacist requires a genuinely clinical header — this is not a dispensing role.

**Displayed:** identifiers, age, sex, height + date, weight + date + delta since last cycle, dosing weight and basis, BSA + formula + inputs + date (**order BSA and current BSA shown as a pair**), episode, diagnosis, primary site, histology, stage, treatment intent, line of therapy, regimen + version + cycle/day + planned cycles, protocol source/reference `[CCA CONFIG]`, full current order (all rows), previous cycle's administered doses and any variance, cumulative doses of all tracked agents with thresholds, allergies with substance-level detail and prior infusion reactions (agent, cycle, grade, management, rechallenge outcome, premedication used), current medication list including comorbidity drugs and anticoagulants, interaction alerts, renal function (creatinine, CrCl `[DERIVED]` with the named formula and the weight used, eGFR `[DERIVED]`), hepatic function (bilirubin total/direct, AST, ALT, ALP, albumin), haematology (Hb, WBC, ANC, platelets) with dates and staleness, electrolytes where regimen-relevant, cardiac function (LVEF, date, method) where regimen-relevant, active toxicities with grades and attribution, current holds/modifications with reasons, readiness result with per-criterion breakdown, pregnancy status where applicable, trial enrolment and protocol-specific dosing rules `[CCA CONFIG]`, vascular access type (affects vesicant route decisions), and treatment location.

### B.12.D Pharmacist screens (summary; full field detail in PART J)

| ID | Screen | Purpose |
|---|---|---|
| `PHA-100` | Order verification | Clinical review of every order row against patient parameters; per-row accept/query; documented verification |
| `PHA-110` | Dose recalculation check | Independent recomputation of calculated dose from order inputs; discrepancy display |
| `PHA-120` | Cumulative dose review | Tracked agents, lifetime totals, threshold status, required monitoring |
| `PHA-130` | Interaction & duplication review | Drug–drug, drug–disease, drug–lab, duplicate therapy; alert disposition recorded |
| `PHA-140` | Query / rejection | Structured reason + free text + recommended alternative + urgency; routed to prescriber |
| `PHA-200` | Preparation specification | Per product: diluent, final volume, concentration `[DERIVED]`, container, filter, light protection, storage, BUD, stability source `[CCA CONFIG]` |
| `PHA-210` | Compounding record | Vials used (lot, expiry, volume), calculated draw volumes, overfill handling, wastage and reason, compounder, in-process checks |
| `PHA-220` | Independent double check | Second checker identity, items checked (itemised), discrepancies found, resolution |
| `PHA-230` | Labelling | Label content specification (patient identifiers, drug, dose, diluent, volume, route, rate, time, BUD, hazard warnings, barcode) |
| `PHA-240` | Release / dispense | Release time, released by, destination, transport, receiving signature |
| `PHA-250` | Returns, wastage, recall | |
| `PHA-300` | Oral therapy dispensing & counselling | Quantity, refills, counselling checklist, adherence, monitoring |

**Required documents:** Pharmacy Clinical Verification Record; Pharmacy Query/Intervention Note; Preparation & Double-Check Record; Dispensing/Release Record; Cumulative Dose Surveillance Note; Oral Therapy Counselling Record; Wastage/Recall Record; Adverse Drug Event Report. Specified in **PART F** and **PART J**.

---

## B.13 — DAY CARE / INFUSION NURSE

*Full module specification in PART K; role-level specification here.*

### B.13.A Role purpose

**Why this role uses the system.** The infusion nurse is the last safety barrier before a hazardous drug enters a patient, and the only observer during administration. This role performs identity and order verification, confirms consent and clearance, establishes and assesses vascular access, administers in the correct sequence at the correct rate, recognises and manages reactions and extravasation, records what was *actually* given (which is not always what was ordered), and documents the patient's condition on discharge with the next steps.

**Responsibility owned.** Patient identification; order currency verification; consent and clearance confirmation; pre-administration assessment and vitals; vascular access establishment, patency and site assessment; independent double check of the product against the order; sequence and rate adherence; reaction surveillance and immediate management; interruption, restart and cessation decisions within protocol; extravasation management; actual administered dose recording including wastage and partial administration; post-treatment observation and vitals; patient education and discharge instructions; escalation to the oncologist.

**Entry point.** Patient arrival in Day Care. **Ends** at discharge from the unit with documented condition and next appointment.

**Receives from.** Front Desk/Intake (arrival, vitals, weight), Medical Oncologist (signed order + clearance), Pharmacy (verified, prepared, released product), previous cycle's records.
**Sends to.** Medical Oncologist (reactions, clearance queries, post-treatment events), Pharmacy (returns, wastage, additional product requests), Toxicity record, Navigator (next appointment, unmet needs), Inpatient/Emergency (escalation), Billing (administered items).

### B.13.B Worklist views

#### View 1 — Today's Treatment Queue

| Column | Type | Notes |
|---|---|---|
| Scheduled time | time | |
| Chair/bay assignment | coded | |
| Patient / UHID / age / sex | mixed | |
| Regimen + cycle/day | text | |
| Expected duration | `[DERIVED]` | Sum of infusion durations + observation + premedication time |
| Arrival status | chip | Not arrived / Arrived / In assessment / Ready / In treatment / Post-treatment observation / Discharged / Deferred / Cancelled |
| Clearance status | chip | **MAR-010 [PRODUCT]** — Cleared by [clinician] at [time] / Not cleared / Conditional (condition text) |
| Readiness | `[DERIVED]` chip | With per-criterion expansion |
| Pharmacy status | chip | Not sent / Verified / In preparation / Prepared / Released / Received in unit / Returned |
| Consent status | chip | |
| Vascular access | chip | Type + site + patency status |
| Allergy / prior reaction | icon | Substance-level; prior infusion reaction highly visible |
| Vitals status | chip | Recorded (time) / Due / Overdue |
| Weight recorded today | chip | Value + delta from order weight |
| Active toxicity | grade chip | |
| Nurse assigned | text | |
| Alerts | icon stack | Extravasation risk (vesicant), reaction risk, fall risk, isolation, interpreter |
| Quick actions | menu | Start assessment · Verify identity · Scan product · Start administration · Record vitals · Record reaction · Pause · Complete · Discharge · Escalate |

#### View 2 — Active Infusions (live board)
Per patient in treatment: drug currently running, sequence position (n of m), start time, elapsed time `[DERIVED]`, expected end time `[DERIVED]`, remaining time `[DERIVED]`, rate, volume remaining `[DERIVED]`, next vitals due `[DERIVED]` with overdue flag, reaction status, interruption status. **MAR-020 [PRODUCT]** — the live board must make an overdue observation and an unattended running infusion visually unmissable.

#### View 3 — Post-treatment Observation
Patients in the observation window with observation end time `[DERIVED]`, vitals due, discharge criteria status `[DERIVED]`.

#### View 4 — Reactions & Incidents
Active and recent reactions, extravasations, and their management status.

#### View 5 — Tomorrow / Upcoming
For preparation planning: expected patients, regimens, chair-time demand `[DERIVED]`, pending readiness items, pending clearance.

### B.13.C Patient header for Day Care Nurse

Identifiers with photograph; age; sex; **allergy and prior infusion reaction banner with the highest visual priority**; episode and diagnosis; regimen name, cycle n of m, day n; treatment intent; order status and signing clinician; clearance status with clinician name and time; readiness breakdown; today's weight and the order's BSA/weight with delta; height; vascular access (type, site, insertion date, patency, last assessment); premedication requirements and administration status; the ordered sequence with per-drug status; prepared product inventory received (with BUD countdown); last cycle's administration summary including any reaction, interruption, dose reduction or delayed completion; active toxicities; current vitals and today's series; supportive medications available (rescue/emergency medications per protocol `[CCA CONFIG]`); isolation precautions; mobility/fall risk; interpreter requirement; next appointment; emergency contact.

### B.13.D Day Care screens (summary; full detail in PART K)

| ID | Screen |
|---|---|
| `MAR-100` | Arrival & identity verification (two-identifier minimum, product-defined; barcode/wristband scanning) |
| `MAR-110` | Pre-administration assessment (vitals, symptoms, toxicity screen, weight, consent, clearance, readiness confirmation) |
| `MAR-120` | Vascular access assessment & establishment |
| `MAR-130` | Product receipt & double check against order |
| `MAR-140` | Administration record (per medication, per the five-value model) |
| `MAR-150` | Reaction / adverse event during administration |
| `MAR-160` | Extravasation management |
| `MAR-170` | Interruption / restart / cessation |
| `MAR-180` | Post-treatment observation & vitals |
| `MAR-190` | Discharge assessment, education, instructions, next appointment |
| `MAR-200` | Nursing escalation to clinician |

**Required document: FULL INFUSION NURSING NOTE** — every section specified in **PART K**.

---

## B.14 — RADIATION PHYSICIST

### B.14.A Role purpose

**Why this role uses the system.** The Physicist guarantees that what the Radiation Oncologist prescribed is what the machine will deliver. This role performs or supervises independent dose calculation verification, plan checking against prescription and constraints, machine-parameter deliverability checks, patient-specific QA measurement, and the documented release of a plan for treatment. Physics is a **verification** role: it must have complete visibility of the prescription and plan, and must be structurally prevented from altering the clinical prescription.

**Responsibility owned.** Independent monitor-unit/dose verification; plan-versus-prescription concordance check; OAR constraint verification; deliverability and machine parameter validation; patient-specific QA measurement and analysis; imaging/IGRT protocol verification; discrepancy raising and resolution; QA sign-off; in-vivo dosimetry where used `[CCA CONFIG]`; equipment QA records; incident/near-miss reporting `[CCA CONFIG]`.

**Entry point.** On plan submission for QA. **Ends** at documented QA pass and release, or at documented rejection back to planning.

**Receives from.** Dosimetry/Planning (plan for QA), Radiation Oncologist (approved prescription and plan), RTT (delivery discrepancies, machine issues).
**Sends to.** Radiation Oncologist (QA outcome, discrepancies), RTT (released plan and delivery parameters), Planning (rejections), governance (incident reports).

### B.14.B Worklist views

1. **QA Queue** — patient, UHID, site, plan version, planner, RO approval status and timestamp, prescription version, plan submitted at, target treatment start date, days/hours to first fraction `[DERIVED]` with urgency colouring, QA type required (calculation check / measurement / both / end-to-end) `[CCA CONFIG]`, assigned physicist, status chip (Awaiting QA / In progress / Discrepancy raised / Failed / Passed / Released), priority.
2. **Discrepancies Open** — discrepancy description, raised at, raised by, category, severity, assigned to, response, resolution, re-check status.
3. **Plans Released** — audit view.
4. **Machine QA / Equipment** — daily/weekly/monthly QA status per unit, last performed, next due, tolerance status, out-of-tolerance actions `[CCA CONFIG]`.
5. **In-vivo Dosimetry Results** where applicable.
6. **Incidents / Near-misses.**

### B.14.C Patient header for Radiation Physicist

Identifiers; age; sex; diagnosis and primary site (for plan plausibility); **current prescription version in full** (site, laterality, phase, total dose, fractions, dose per fraction, modality, technique, energy, image-guidance protocol, immobilisation, OAR constraints); prescription version history; current plan version and version history with planner and timestamps; RO approval status per version; prior RT (site, dose, dates, technique) and any documented cumulative-dose constraints; implanted devices (pacemaker/ICD — mandatory display, drives special procedure `[CCA CONFIG]`); pregnancy status where applicable; patient weight/height and any change since simulation (affects setup and dosimetry); concurrent systemic therapy (may alter constraint tolerance); treatment unit assigned; scheduled start date.

**Physicist must NOT be able to edit:** the prescription, the target volumes, the intent, the diagnosis, the clinical constraints. **PHY-010 [PRODUCT]** — physics write access is limited to QA records, discrepancy records, calculation verification results, machine parameter validation, equipment QA and incident reports. Any change to the prescription must be made by the Radiation Oncologist and creates a new prescription version, which invalidates the QA status of any plan built on the superseded version — **PHY-011 [PRODUCT]**.

### B.14.D Physicist screens and fields

| ID | Screen | Fields |
|---|---|---|
| `PHY-100` | Prescription–plan concordance check | Prescription version + hash/reference; plan version; per-parameter comparison table (site, laterality, total dose, fractions, dose/fraction, technique, energy, modality, phases) with match/mismatch per row; mismatch reason; outcome (concordant / discrepancy raised) |
| `PHY-110` | Independent dose/MU verification | Method (independent calculation software / manual / secondary algorithm) `[CCA CONFIG]`, software + version, calculated value, planned value, deviation % `[DERIVED]`, tolerance applied `[CCA CONFIG — CLINICAL SIGN-OFF]`, pass/fail, performed by, date/time, comments |
| `PHY-120` | OAR constraint verification | Repeating per OAR: OAR name `[CCA CONFIG]`, constraint metric (e.g. max dose, mean dose, volume-at-dose — structure product-defined), constraint value and unit, achieved value, unit, met/not met, deviation, acceptable-variation applied, clinical justification if exceeded (authored by RO, displayed read-only to physics), reviewed by |
| `PHY-130` | Target coverage verification | Per target volume: volume name, prescribed dose, coverage metric and achieved value, conformity/homogeneity indices where used `[CCA CONFIG]`, met/not met |
| `PHY-140` | Machine parameter/deliverability check | Unit, energy, beam/arc count, MU per beam, gantry/collimator/couch values, MLC deliverability, dose rate, field size limits, couch clearance/collision check, bolus, wedges/accessories, imaging fields, tolerance table applied, R&V transfer verification `[INTEGRATION]` |
| `PHY-150` | Patient-specific QA measurement | QA method, phantom, detector, measurement date/time, analysis criteria (agreement criteria and threshold — `[CCA CONFIG — CLINICAL SIGN-OFF]`), result value, pass/fail, repeat measurements, performed by |
| `PHY-160` | Imaging/IGRT protocol verification | Imaging modality, frequency, matching structures, action levels/tolerances `[CCA CONFIG]`, imaging dose accounted, verified by |
| `PHY-170` | Discrepancy record | Category (dropdown — product-defined: prescription mismatch / calculation deviation / constraint exceeded / deliverability / data transfer / documentation / other), description, severity, raised by/at, notified to, response, resolution, re-verification result, closure |
| `PHY-180` | QA sign-off & release | Overall outcome, all sub-checks displayed with individual outcomes, physicist signature (re-authenticated), date/time, plan released to R&V `[INTEGRATION]`, release reference. **PHY-181 [PRODUCT]** — release requires: RO-approved prescription version, RO-approved plan version, all mandatory QA sub-checks passed or explicitly waived with recorded authority and reason |
| `PHY-190` | Equipment QA register | Unit, test, frequency, tolerance, result, pass/fail, performed by, date, action taken |

**Required documents:** Physics QA Report (per plan); Discrepancy/Deviation Record; Plan Release Record; In-vivo Dosimetry Report; Equipment QA Record; Radiation Incident/Near-miss Report. Sections in **PART L**.

---

## B.15 — RADIATION TECHNOLOGIST / THERAPIST (RTT)

### B.15.A Role purpose

**Why this role uses the system.** The RTT delivers each fraction. This role verifies patient identity and treatment site, reproduces the simulated position using the recorded immobilisation and setup parameters, performs and evaluates verification imaging within defined tolerance, delivers the fraction, records exactly what was delivered (including partial or aborted delivery), documents acute skin/site reactions observed, and escalates deviations.

**Responsibility owned.** Identity and site verification before every fraction; setup reproduction and setup-parameter recording; verification imaging acquisition, matching and action-level application; delivery execution and confirmation; interruption/abort documentation; cumulative fraction accounting; observed toxicity reporting; machine issue reporting; patient support and instruction during the course.

**Entry point.** On plan release to the treatment unit. **Ends** at completion of the final fraction and handover to RO for completion documentation.

**Receives from.** Physicist (released plan), RO (prescription, authorisation to treat, changes), Simulation (setup data), Nursing (patient condition).
**Sends to.** RO (delivery record, toxicity observations, setup deviations), Physicist (machine and dosimetric concerns), Nursing (skin care needs), Scheduling (missed fractions), Navigator.

### B.15.B Worklist views

1. **Today's Treatment Schedule (per unit)** — appointment time, patient, UHID, photograph (identity verification), treatment site + laterality, phase, fraction n of m, prescribed dose/fraction, plan version, immobilisation devices required, setup notes, imaging required today (protocol-driven `[DERIVED]`), estimated slot duration, arrival status, special instructions (bladder/bowel prep, breath-hold, contrast, sedation), isolation, mobility, interpreter, status chip (Scheduled / Arrived / In room / Imaging / Delivering / Complete / Interrupted / Not treated — reason).
2. **On-Treatment Patient List** — all patients on active courses with fractions delivered/prescribed, cumulative delivered dose `[DERIVED]`, missed fractions, next OTV due, active toxicity observed.
3. **Missed / Interrupted Fractions** — with reason, make-up scheduling, gap days `[DERIVED]`.
4. **Setup Deviations & Imaging Out-of-Tolerance** — with action taken and escalation.
5. **Machine Status / Downtime** — affecting today's list, with reallocation.

### B.15.C Patient header for RTT

Identifiers with photograph; age; sex; **treatment site and laterality with maximum visual prominence**; diagnosis (short); phase and fraction n of m; prescription summary read-only (total dose, fractions, dose/fraction, technique, energy, modality); plan version and release status; immobilisation devices (type, ID, index positions); setup parameters (isocentre coordinates, shifts from reference marks, couch values, SSD, bolus specification, accessories); imaging protocol (modality, frequency, matching structures, action levels); daily preparation requirements; skin markings/tattoos description; allergies (relevant to contrast, tape, dressings); implanted devices; pregnancy status where applicable; mobility, transfer and positioning constraints; interpreter; current observed skin/site reaction grade and photographs where captured `[CCA CONFIG]`; delivery history table (every fraction: date, delivered dose, unit, imaging performed, deviations); cumulative delivered dose `[DERIVED]`; missed fractions and reasons; next OTV due; alerts from RO.

**RTT must NOT be able to edit:** prescription, plan, target volumes, constraints, dose, fractionation, or the delivered-dose values transferred from the R&V system. **RTT-010 [PRODUCT]** — RTT write access covers setup records, imaging acquisition and match results, delivery execution records, interruption/abort records, observed toxicity and patient-condition notes, machine issue reports, and patient instruction records.

### B.15.D RTT screens and fields

| ID | Screen | Fields |
|---|---|---|
| `RTT-100` | Pre-treatment verification | Identity verification method (photograph + two identifiers minimum, product-defined; barcode/biometric where configured), verified by, time; site and laterality confirmation (explicit affirmative action, not a passive display) — **RTT-101 [PRODUCT]**; prescription version confirmation; plan version and release status confirmation; scheduled fraction number confirmation `[DERIVED]` with mismatch hard stop; daily preparation confirmed; pregnancy re-check where applicable `[CCA CONFIG]` |
| `RTT-110` | Setup record | Immobilisation devices used (each with ID and index), positioning aids, couch values (lateral, longitudinal, vertical, rotation), shifts applied (x, y, z in mm, with direction convention explicit), SSD, bolus applied (type, thickness, location), accessories, setup performed by, second person verification where required `[CCA CONFIG]`, setup photographs where captured, deviations from documented setup with reason |
| `RTT-120` | Verification imaging | Imaging modality (kV/MV planar, CBCT, surface guidance, other), acquisition time, matching structures used, match values per axis (mm, and rotation in degrees), automatic vs manual match, action level applied `[CCA CONFIG]`, within tolerance y/n, corrective shift applied (per axis), re-imaging performed y/n, reviewed by, approved by (where RO/physics approval required for out-of-tolerance) |
| `RTT-130` | Delivery record | Fraction number, date, planned dose for fraction, unit/machine, beams/arcs delivered, MU delivered per field `[INTEGRATION from R&V]`, delivery start time, delivery end time, delivered dose for the fraction, completion status (Complete / Partial / Aborted / Not delivered), partial delivery detail (fields delivered, MU delivered, fraction of prescribed dose delivered `[DERIVED]`), reason for partial/abort (dropdown — product-defined: patient movement / patient distress / patient request / machine fault / imaging out of tolerance / clinical decision / power failure / other + free text), action taken, delivered by, second operator |
| `RTT-140` | Cumulative accounting | `[DERIVED]` — fractions delivered, cumulative delivered dose, remaining fractions, remaining dose, elapsed treatment days, gap days, projected completion date. See Part E |
| `RTT-150` | Observed toxicity / patient condition | Site-specific observation set `[CCA CONFIG]`, grade where the RTT is authorised to grade `[CCA CONFIG]`, description, photograph, escalated to (RO/nursing), time |
| `RTT-160` | Missed fraction record | Date, reason (dropdown), notified to, make-up plan, rescheduled date, cumulative gap impact `[DERIVED]` |
| `RTT-170` | Machine/equipment issue | Unit, issue, time, impact on treatment, physics notified, resolution |
| `RTT-180` | Patient instruction / support record | Skin care advice, positioning instructions, preparation reminders, delivered by, date |

**Required documents:** Daily Treatment Delivery Record; Setup and Imaging Record; Interruption/Missed Fraction Record; RTT Observation Note; Machine Issue Report. Sections in **PART L**.

---

## B.16 — INPATIENT ONCOLOGY CLINICIAN

### B.16.A Role purpose

**Why this role uses the system.** Oncology inpatients are admitted for treatment delivery, for complications of treatment, for complications of disease, or for terminal care — and the admitting clinician must reconcile the acute problem with the ongoing cancer treatment plan. The system must therefore make the outpatient oncology context (regimen, cycle, cumulative dose, RT status, toxicity history) fully present at the bedside, and must ensure that inpatient events (dose delays, toxicity, discontinuation) write back to the episode rather than being trapped in an admission record.

**Responsibility owned.** Admission decision and admission H&P; problem list and working diagnoses; daily assessment and plan; inpatient medication orders including inpatient systemic therapy; investigation ordering and result action; cross-specialty consultation requests and integration of responses; deterioration recognition and escalation; goals-of-care discussions; transfer decisions; discharge readiness determination, discharge medication reconciliation and discharge summary; communication with the outpatient oncology team.

**Entry point.** Admission request (from clinic, Day Care, emergency, or direct). **Ends** at discharge, transfer or death, with a completed summary and a defined follow-up plan.

**Receives from.** MO/RO/SO (admission requests, treatment context), Day Care (acute events), Emergency, Nursing (escalations, observations), Laboratory/Radiology/Pathology, consultants.
**Sends to.** Inpatient Nursing (orders and plan), Pharmacy, consultants, outpatient oncology team (discharge handover), Navigator, Palliative Care, Discharge/Billing.

### B.16.B Worklist views

1. **My Inpatients** — ward + bed, patient, UHID, age, sex, admission date, length of stay `[DERIVED]`, primary oncological diagnosis, admission reason (dropdown — product-defined categories: planned treatment / febrile neutropenia / other infection / treatment toxicity / disease complication / pain control / procedure / terminal care / other), current treatment status (regimen + cycle/day; RT fraction n/m; post-op day n), acuity/escalation flag, isolation status, active problems count, new results unacknowledged, pending consults, VTE prophylaxis status `[CCA CONFIG]`, antibiotic day n and review due, discharge readiness `[DERIVED]` chip, planned discharge date, code status/goals of care `[CCA CONFIG]`, last ward round documented (time), tasks outstanding.
2. **Admission Requests Pending** — requesting clinician, reason, urgency, bed requested, bed allocated, waiting time `[DERIVED]`.
3. **Deteriorating Patients** — triggered by early-warning score `[DERIVED]` where configured `[CCA CONFIG]`, critical results, nursing escalation.
4. **Results Inbox (inpatient)**.
5. **Discharges Today / Tomorrow** — with summary completion status, medication reconciliation status, follow-up booked status, transport, education delivered.
6. **Consults Requested by Me** — specialty, question, urgency, requested at, responded at `[DERIVED]`, response summary, acted upon.

### B.16.C Patient header for Inpatient Oncology Clinician

Full oncology header (as B.4.C) **plus** the inpatient block: ward, bed, admission date/time, LOS `[DERIVED]`, admitting clinician, consultant of record, admission reason, working problem list with status, isolation/precautions, code status/goals of care `[CCA CONFIG]`, allergy banner, current inpatient medications (with systemic anticancer therapy visually distinct), infusions running, fluid balance (24h in/out and cumulative `[DERIVED]`), latest and trended vitals with early-warning score `[DERIVED]`, latest labs with trends and critical flags, microbiology results and current antimicrobials with day count `[DERIVED]`, oxygen requirement, nutrition status and intake, mobility, pressure-area risk, fall risk, VTE risk and prophylaxis, drains/lines/devices with insertion dates and day counts `[DERIVED]`, wounds/stomas, pending investigations, pending consults, planned procedures, discharge plan and barriers.

### B.16.D Inpatient clinician screens

| ID | Screen | Contents |
|---|---|---|
| `IPD-100` | Admission request / bed request | Reason, urgency, expected LOS, isolation requirement, monitoring level, bed type, requesting clinician, accepting clinician |
| `IPD-110` | Admission H&P | Full section list in Part Q |
| `IPD-120` | Daily progress / ward round note | Section list in Part Q |
| `IPD-130` | Problem list management | Problem, onset, status, priority, owner, linked orders and notes |
| `IPD-140` | Inpatient orders | Medication (including inpatient systemic therapy routed through the same order/verification/administration chain as Day Care — **IPD-141 [PRODUCT]**: inpatient chemotherapy must not bypass pharmacy verification or the five-value dose model), fluids, blood products, diet, activity, monitoring frequency, oxygen, VTE prophylaxis, investigations, procedures, nursing instructions |
| `IPD-150` | Consult request | Specialty, question, urgency, clinical summary, response required by; response capture is by the consulting clinician |
| `IPD-160` | Escalation / deterioration note | Trigger, assessment, intervention, response, escalation to, outcome |
| `IPD-170` | Goals of care / ACP discussion | `[CCA CONFIG — whether and how captured]`; participants, content, decisions, documentation of patient/family understanding |
| `IPD-180` | Transfer | Reason, from/to location or facility, clinical status at transfer, accepting clinician, handover content, transport mode, accompanying staff |
| `IPD-190` | Discharge readiness & discharge | Criteria `[CCA CONFIG]`, medication reconciliation, discharge medications with counselling, follow-up appointments, investigations to follow, red flags, contact instructions, home care/community referrals |
| `IPD-200` | Death documentation | `[CCA CONFIG]` — time, certification, notifications, episode state change, bereavement pathway |

**Required documents:** Admission H&P; Daily Oncology Progress/Ward Round Note; Escalation/Deterioration Note; Cross-specialty Consultation Note (request + response); Procedure Note; Transfer Note; Goals of Care Note; Discharge Summary; Death Summary. Section-by-section in **PART Q**.

---

## B.17 — INPATIENT NURSE

### B.17.A Role purpose

**Why this role uses the system.** The inpatient nurse maintains the continuous observational record, administers all medications including hazardous drugs, performs risk assessments and their interventions, manages devices, wounds, drains and stomas, recognises deterioration, and executes escalation. In oncology this role additionally manages neutropenic precautions, cytotoxic handling and spill response, extravasation, mucositis and nutrition support.

**Responsibility owned.** Nursing assessment on admission and per shift; vital signs and early-warning scoring; medication administration and the MAR; fluid balance; risk assessments (falls, pressure area, VTE where nursing-owned, nutrition, pain) and interventions; device/line/drain/wound/stoma care; specimen collection; patient and carer education; handover; escalation; discharge nursing checklist.

**Entry point.** On admission/transfer to the ward. **Ends** at discharge, transfer or death, with handover documented.

**Receives from.** Inpatient clinician (orders, plan), Pharmacy (medications), Day Care/theatre/emergency (transfers), previous shift (handover).
**Sends to.** Inpatient clinician (escalations, observations), Pharmacy (queries, returns), next shift (handover), allied health (referrals), Discharge coordination.

### B.17.B Worklist views

1. **My Patients This Shift** — bed, patient, age/sex, diagnosis, acuity, allergy, isolation, code status, next medication due `[DERIVED]` with overdue chip, next observation due `[DERIVED]`, current early-warning score `[DERIVED]` with trend, active infusions with remaining time `[DERIVED]`, pending tasks, risk assessment due/overdue, fall/pressure/VTE status, devices with day counts, fluid balance status, pending specimen collection, pending education.
2. **Medication Due / MAR Board** — due, overdue, PRN available, held, refused, omitted with reason; hazardous-drug items visually distinct.
3. **Observations Due**.
4. **Escalations & Deteriorations**.
5. **Admissions/Transfers/Discharges Today**.

### B.17.C Patient header for Inpatient Nurse

Identifiers, age, sex, photograph, bed; allergy banner with substance detail; isolation/precautions; code status `[CCA CONFIG]`; diagnosis and treatment context (regimen/cycle/day, RT fraction, post-op day); active toxicities including neutropenia status with ANC value and date (drives precautions); current orders (medications, fluids, diet, activity, monitoring frequency, oxygen); infusions running with rate and remaining time; devices/lines/drains with type, site, insertion date, day count `[DERIVED]`, last dressing; wounds/stomas with last assessment; latest vitals and EWS `[DERIVED]`; fluid balance; last bowel movement; mobility and transfer requirements; fall/pressure risk with interventions in place; nutrition status and intake; pain score and last analgesia; pending investigations requiring nursing action; scheduled procedures; patient/family communication notes; interpreter requirement.

### B.17.D Inpatient nursing screens

| ID | Screen | Contents |
|---|---|---|
| `IPN-100` | Nursing admission assessment | Full systems assessment, risk assessments, baseline measurements, belongings, orientation, education needs |
| `IPN-110` | Observation flowsheet | All vitals per B.2.D field set, plus EWS `[DERIVED]`, oxygen delivery, neurological observations where ordered, blood glucose, pain, sedation score where relevant |
| `IPN-120` | MAR — administration | Per dose: medication, dose ordered, dose administered, route, site, time due, time given, administered by, second checker where required, patient identification verified, product scanned where configured, omission/refusal with reason (dropdown — product-defined: patient refused / patient absent / clinically held / not available / NBM / adverse reaction / other), PRN indication and effect assessment |
| `IPN-130` | Fluid balance | Intake (oral, IV, feed, flush, blood products) and output (urine, drains per drain, stoma, vomit, stool, insensible where estimated) with 24h totals and running balance `[DERIVED]` |
| `IPN-140` | Risk assessments & interventions | Falls, pressure area, VTE, nutrition, mucositis, neutropenic precautions, delirium `[CCA CONFIG — instruments]`; each with item scores, `[DERIVED]` total and band, triggered interventions, review interval, next due |
| `IPN-150` | Device/line/drain/wound/stoma care | Per device: type, site, insertion date, day count `[DERIVED]`, dressing status, site assessment (dropdown per site condition), patency, complication, care performed, removal date and reason |
| `IPN-160` | Nursing progress note | Structured per shift + narrative |
| `IPN-170` | Escalation | Trigger, observation, action, clinician notified (name, time, method), response time `[DERIVED]`, outcome |
| `IPN-180` | Handover | Structured handover content, giving nurse, receiving nurse, time |
| `IPN-190` | Patient/carer education | Topic, material, delivered to, comprehension |
| `IPN-200` | Cytotoxic handling / spill / exposure | `[CCA CONFIG]` — PPE used, spill event, exposure event, action, reporting |

**Required documents:** Nursing Admission Assessment; Shift Nursing Note; Observation Chart; MAR; Fluid Balance Chart; Risk Assessment Records; Device/Wound/Stoma Care Record; Nursing Escalation Note; Handover Record; Nursing Discharge Checklist. Sections in **PART Q**.

---

## B.18 — FINANCIAL COUNSELLOR / BILLING

### B.18.A Role purpose

**Why this role uses the system.** Oncology treatment is long, expensive and modality-dependent; financial failure is a common cause of treatment abandonment. This role establishes payer coverage, produces treatment-course estimates, obtains pre-authorisations, tracks approvals against the actual treatment plan, counsels patients, arranges scheme/trust support, and reconciles charges against what was actually delivered.

**Responsibility owned.** Payer/eligibility verification; cost estimation per treatment plan and per cycle/fraction; pre-authorisation submission and tracking; co-payment and deposit handling; scheme/trust/charity application support; financial counselling documentation; charge capture reconciliation; claims and denials management; refunds; financial barrier escalation to Navigator.

**Entry point.** At registration, at treatment plan finalisation, and before each high-cost episode. **Ends** at claim settlement.

**Receives from.** Front Desk, MO/RO/SO (treatment plans and orders — the cost driver), Pharmacy (high-cost drug requirements), Navigator (identified barriers), Administration.
**Sends to.** Patient/family, payers, Navigator, treating team (authorisation status affecting scheduling), Pharmacy (clearance to prepare where policy requires `[CCA CONFIG]`), Administration.

### B.18.B Worklist views

1. **New Estimates Required** — patients with a signed treatment plan or order lacking a current estimate: plan date, modality, regimen, planned cycles, planned RT fractions, planned surgery, payer, urgency (linked to planned treatment start date `[DERIVED]` days remaining).
2. **Authorisations Pending** — payer, submitted date, expected decision date, days pending `[DERIVED]`, treatment start date at risk, status (Draft / Submitted / Additional information requested / Approved / Partially approved / Denied / Appeal submitted / Expired), approved scope (drug/cycles/fractions/procedures), approval validity dates, approved amount.
3. **Authorisation Expiring / Exhausted** — **FIN-010 [PRODUCT]** — the system must alert when approved cycles/fractions are nearly consumed by actual delivery, comparing authorised quantity against administered/delivered quantity `[DERIVED]`.
4. **Counselling Due**.
5. **Denials & Appeals**.
6. **Outstanding Balances / Payment Plans**.
7. **Charge Reconciliation Exceptions** — administered items without charges, charged items without administration records, wastage charges, cancelled preparations.

### B.18.C Patient header for Financial Counsellor

Deliberately bounded: identifiers, age, sex, contact, address, payer(s) with policy details and validity, scheme/trust enrolment, employment/income category where captured `[CCA CONFIG]`, family/dependant information where relevant to schemes, **treatment plan at modality level only** (intent category, planned modalities, planned number of cycles/fractions, planned procedures, planned high-cost drugs by name), estimated cost and approved amount, delivered-to-date quantities, outstanding balance, payment history, authorisation status, financial barriers logged, counselling history.

**FIN-020 [PRODUCT]** — Diagnosis-level detail visible to this role is limited to what is required for coding and authorisation (diagnosis code and stage where the payer requires it). Narrative clinical notes, toxicity, prognosis and biomarker detail beyond authorisation requirements must be role-gated.

### B.18.D Screens

| ID | Screen | Fields |
|---|---|---|
| `FIN-100` | Payer & eligibility | Payer, plan/scheme, policy number, validity from/to, coverage type, exclusions, co-pay %, deductible, annual/lifetime limits, dependants covered, verification method, verified by/at, verification reference |
| `FIN-110` | Treatment cost estimate | Auto-assembled from the signed plan: per modality, per cycle, per fraction, per procedure, itemised (drugs with quantities derived from dose and vial sizes, consumables, chair/bed time, imaging, labs, professional fees per tariff `[CCA CONFIG]`), subtotal, taxes, estimated patient share, validity period, prepared by, issued to patient, acknowledgement |
| `FIN-120` | Pre-authorisation | Payer, request type, clinical documentation attached (auto-selected from record), diagnosis code, staging, proposed treatment, requested quantity, submitted by/at, reference number, status, decision date, approved scope and amount, conditions, validity, denial reason, appeal record |
| `FIN-130` | Financial counselling record | Attendees, topics covered, estimate discussed, patient understanding, options presented (payment plan, scheme, charity, generic/biosimilar substitution referral to clinician), decisions, follow-up, counsellor, date |
| `FIN-140` | Scheme/trust application | Scheme, eligibility criteria checklist `[CCA CONFIG]`, documents required and received, submitted, status, approved amount, validity |
| `FIN-150` | Charge capture reconciliation | Delivered items from clinical records vs charged items; exceptions; adjustments with reason |
| `FIN-160` | Payments, deposits, refunds | |
| `FIN-170` | Claims & denials | Claim submission, status, settlement, denial reason, appeal, write-off with authority |

**Required documents:** Cost Estimate; Financial Counselling Record; Pre-authorisation Request and Decision Record; Payment Plan Agreement; Claim/Denial Record.

---

## B.19 — HOSPITAL / CLINICAL ADMINISTRATOR

### B.19.A Role purpose

**Why this role uses the system.** The Administrator maintains the operational and configuration integrity of the system — users, roles, facilities, resources, schedules, masters, templates, and the governance dashboards that show whether the service is functioning. Critically, this role also **owns the change control over clinical content masters**, which in an oncology system are patient-safety artifacts.

**Responsibility owned.** User and role administration; access review; facility, ward, bed, chair, theatre, treatment-unit masters; scheduling templates and capacity; catalogue and master management with versioning and approval routing; template management; audit review; incident and complaint registers `[CCA CONFIG]`; operational and clinical governance reporting; registry and statutory reporting `[CCA CONFIG]`; downtime procedures; data quality management including duplicate/merge governance.

**Entry point.** Continuous. **Ends** — not patient-bound.

### B.19.B Worklist / dashboard views

1. **Configuration Change Queue** — master, proposed change, proposer, clinical approver required `[CCA CONFIG]`, approval status, effective date, version, affected screens, rollback plan. **ADM-010 [PRODUCT]** — clinical content masters (regimens, thresholds, dose rules, consent text, pathology templates, RT templates) cannot be activated by an administrator alone; they require the configured clinical approver's signature and carry an effective-from date and a version number visible wherever the content is consumed.
2. **User & Access Review** — users, roles, last login, dormant accounts, break-glass events, privilege changes, pending access reviews.
3. **Operational Dashboards** — clinic utilisation, Day Care chair utilisation and turnaround, pharmacy verification and preparation turnaround, RT unit utilisation and downtime, theatre utilisation, bed occupancy and LOS, imaging and pathology TAT, MDT metrics, waiting times per pathway milestone. All `[DERIVED]`, targets `[CCA CONFIG]`.
4. **Clinical Governance Dashboards** — pathway breach rates, readiness override rates and reasons, dose variance distribution, pharmacy intervention rates and categories, reaction and extravasation rates, RT interruption rates and gap days, unplanned admission rates, 30-day post-treatment events `[CCA CONFIG]`, incident register, critical result acknowledgement times, unsigned document ageing.
5. **Data Quality** — duplicate candidates, merge requests and history, incomplete registrations, unmapped codes, orphan records, unsigned notes beyond target, missing mandatory dataset items for registry export.
6. **Audit Review** — access to sensitive records, override events, amendments and retractions, after-the-fact entries.
7. **Registry / Statutory Reporting** — dataset completeness, export status `[CCA CONFIG]`.

### B.19.C Patient context for Administrator

Administrators operate on aggregates. Individual patient access must be exception-based, reason-recorded and audited (GEN-PRM-003). Where a patient must be opened (merge resolution, complaint investigation), the administrator sees an **administrative view**: identifiers, encounters, documents inventory, access log — not clinical content, unless a clinical-administrator role with explicit clinical permission is configured. **ADM-020 [PRODUCT]** — "Administrator" must be decomposable into at least: System Administrator (no clinical content), Clinical Content Administrator (masters and templates, with clinical approver routing), Operations Manager (dashboards, scheduling, capacity), Privacy/Audit Officer (audit and access review), and Medical Records/HIM (merge, document management, registry export).

### B.19.D Administrator screens

| ID | Screen |
|---|---|
| `ADM-100` | User management (create, role assignment, scope, credentials, registration numbers, signature setup, deactivation) |
| `ADM-110` | Role & permission management (per-object view/create/edit/sign matrix) |
| `ADM-120` | Facility, ward, bed, chair, theatre, treatment unit masters |
| `ADM-130` | Scheduling templates, slot types, capacity, holidays, blackouts |
| `ADM-140` | Clinical content master management with versioning, approval routing, effective dating, and impact analysis (which orders/plans/documents reference the version being changed) |
| `ADM-150` | Document/note template management |
| `ADM-160` | Alert rule management with clinical approval |
| `ADM-170` | Audit log review and export |
| `ADM-180` | Incident/complaint register `[CCA CONFIG]` |
| `ADM-190` | Reporting and registry export |
| `ADM-200` | Downtime management and reconciliation |
| `ADM-210` | Data quality, duplicate resolution, merge/unmerge with full audit |

---

## B.20 — PATIENT-FACING

### B.20.A Purpose

**Why this exists.** Patients and carers need reliable, understandable, timely information about appointments, preparation, medications, side-effect management, when to seek help, and their own results — and the service needs verifiable evidence that safety-critical information was delivered and understood.

**PTP-010 [PRODUCT]** — Every patient-facing artifact is versioned, language-tagged, reading-level-tagged where configured, and its delivery is recorded against the patient (what, which version, to whom, by whom, when, in what language, by what method, with what comprehension confirmation).

### B.20.B Patient-facing artifacts and their required content

| ID | Artifact | Required content |
|---|---|---|
| `PTP-100` | Appointment slip / reminder | Date, time, department, clinician, location with directions, what to bring, preparation instructions, contact number, cancellation instructions |
| `PTP-110` | Investigation preparation instruction | Test, date/time, location, fasting/hydration/bowel prep/glucose/medication instructions, duration, contrast information, escort requirement, what to bring, contact |
| `PTP-120` | Consent information sheet | Procedure/treatment, purpose, what it involves, expected benefits, common and serious risks, alternatives, right to withdraw, contact for questions. Content `[CCA CONFIG — CLINICAL SIGN-OFF]`; structure and versioning `[PRODUCT]` |
| `PTP-130` | Chemotherapy/systemic therapy information | Regimen name in lay terms, schedule, what to expect on treatment day, expected duration, common side effects and their management, **red-flag symptoms with explicit thresholds and instructions to seek urgent care** `[CCA CONFIG — CLINICAL SIGN-OFF]`, 24-hour contact number, precautions (handling body fluids, contraception, vaccination, dental, sun exposure) `[CCA CONFIG]` |
| `PTP-140` | Oral therapy instruction | Drug, dose, how and when to take, food instructions, storage, missed-dose instruction, what not to take with it, monitoring appointments, refill process, side effects, red flags, contact |
| `PTP-150` | Radiotherapy information | Course length, daily routine, preparation (bladder/bowel), skin care, expected site-specific effects and timing, red flags, contact |
| `PTP-160` | Surgery information & post-op instructions | Procedure, preparation, fasting, medication instructions (especially anticoagulants), expected stay, wound/drain/stoma care, activity restrictions, red flags, follow-up |
| `PTP-170` | Discharge instructions | Diagnosis in lay terms, what was done, medications with purpose and instructions, what to watch for, red flags with thresholds, follow-up appointments, contacts, community services |
| `PTP-180` | Treatment Summary (patient version) | Lay rendering of the Cancer Treatment Summary (Part R) |
| `PTP-190` | Survivorship Care Plan (patient version) | Lay rendering (Part R): what treatment was received, possible late effects, surveillance schedule, who to contact, health maintenance |
| `PTP-200` | Result communication | Where policy permits `[CCA CONFIG]`; with clinician-controlled release and an explicit rule preventing automatic release of results whose delivery requires clinical context — **PTP-201 [PRODUCT]** |
| `PTP-210` | Patient-reported outcome / symptom questionnaire | Instrument `[CCA CONFIG]`; item-level responses stored discretely; scores `[DERIVED]`; alert thresholds `[CCA CONFIG]`; results routed to the clinical team's inbox, not to an unmonitored queue |
| `PTP-220` | Financial estimate and payment information | Per Part B.18 |

---

## B.21 — ADDITIONAL ROLES

These roles exist in a mature oncology service and must not be folded into others.

### B.21.1 Laboratory Technologist / Laboratory `[INTEGRATION-heavy]`
**Purpose:** Sample receipt, analysis, result release, critical value communication.
**Worklist:** pending collections, received samples, in-analysis, results pending release, critical values pending communication, rejected samples with reason, add-on requests, TAT breaches.
**Header:** identifiers, ordered tests, indication, priority, sample type/collection time, prior results for delta check, patient location, isolation status, treatment context where it affects interpretation (e.g. growth factor administration affecting counts).
**Key requirements:** `LAB-010 [PRODUCT]` — sample collection time, receipt time and analysis time recorded separately; `LAB-020` — delta check against prior results with defined thresholds `[CCA CONFIG]`; `LAB-030` — critical value register with named recipient, read-back and acknowledgement, identical in structure to `RAD-030`; `LAB-040` — ANC handling: whether ANC is reported by the analyser or `[DERIVED]` from WBC × (neutrophils% + bands%)/100 must be explicit on every result, because readiness logic depends on it (Part E).
**Documents:** Laboratory Report; Critical Value Communication Record; Sample Rejection Record; Addendum/Corrected Report — with mandatory notification to all consumers of the corrected value, including any readiness assessment that used it — `LAB-050 [PRODUCT]`.

### B.21.2 Palliative Care Clinician
**Purpose:** Symptom control, goals of care, advance care planning, end-of-life care, family support — running *concurrently* with active treatment, not only after it.
**Worklist:** referrals received (with urgency, reason, referrer), active caseload with symptom burden scores `[DERIVED]`, inpatient consults, community/home care patients, deteriorating patients, bereavement follow-ups.
**Header:** identifiers, diagnosis, stage, disease status, treatment status and intent, prognosis discussion status, symptom scores and trends (pain, nausea, dyspnoea, fatigue, appetite, sleep, mood — instrument `[CCA CONFIG]`), current analgesia with opioid dose and `[DERIVED]` oral morphine equivalent where configured `[CCA CONFIG — CLINICAL SIGN-OFF]`, other symptom medications, functional status, goals of care and code status, family/carer situation, preferred place of care/death where recorded, spiritual/cultural needs.
**Screens:** Palliative referral; Comprehensive symptom assessment; Symptom management plan; Goals-of-care/ACP discussion; Opioid titration record; Terminal care plan; Family meeting record; Bereavement contact.
**Documents:** Palliative Care Consultation Note; Symptom Review Note; Goals of Care Note; Family Meeting Note; Terminal Care Plan; Bereavement Note.

### B.21.3 Dietitian / Nutrition
**Purpose:** Nutrition assessment and intervention across treatment, particularly for head/neck, upper GI and RT patients.
**Header additions:** weight trend with % change over defined intervals `[DERIVED]`, BMI, nutrition screening score, dysphagia status, feeding route (oral/oral+supplement/NG/PEG/parenteral), intake records, biochemistry (albumin, electrolytes), treatment site and RT field (affects swallowing), mucositis grade, nausea/vomiting grade, bowel status.
**Screens/fields:** nutrition assessment (anthropometry, intake history, symptoms affecting intake, requirements `[DERIVED]` from configured formulae `[CCA CONFIG — CLINICAL SIGN-OFF]`), nutrition diagnosis, intervention plan (diet texture, supplements with product/quantity/frequency, enteral feed regimen with rate and volume, parenteral), monitoring plan, review.
**Documents:** Nutrition Assessment Note; Nutrition Review Note; Enteral/Parenteral Feeding Plan.

### B.21.4 Psycho-oncology / Counsellor / Social Worker
**Header additions:** distress score and trend, identified psychosocial issues, risk flags, social circumstances, caregiver status, financial barriers, employment, dependants.
**Screens:** referral, psychosocial assessment, risk assessment `[CCA CONFIG — instrument]` with escalation pathway, intervention plan, session notes (with elevated access restriction — `PSY-010 [PRODUCT]`: psychosocial session content must support a restricted-access classification separate from general clinical notes), outcome measures.
**Documents:** Psychosocial Assessment; Session Note; Risk Assessment and Safety Plan; Discharge from Service Note.

### B.21.5 Clinical Trials Coordinator
**Purpose:** Screening, consent, enrolment, protocol-specific scheduling and data capture, deviation and SAE reporting.
**Worklist:** open trials with slots, patients screened, eligibility checklists in progress, consented, enrolled, on treatment, in follow-up, deviations open, SAEs pending report, visits due per protocol calendar.
**Header additions:** trial ID, protocol version, arm (where unblinded), enrolment date, consent version and date, protocol-specific dosing and monitoring rules `[CCA CONFIG]`, protocol visit schedule with windows and `[DERIVED]` due/overdue status, deviations recorded, SAE history.
**Key requirements:** `TRL-010 [PRODUCT]` — trial-specific dosing, readiness thresholds and monitoring must override standard configuration for enrolled patients, and the override source must be visible on the order and readiness screens; `TRL-020` — protocol visit windows are `[DERIVED]` date ranges with in-window/out-of-window status; `TRL-030` — deviation register with category, description, date identified, reported to sponsor/ethics, corrective action.
**Documents:** Eligibility Checklist; Trial Consent Record; Enrolment Record; Protocol Deviation Report; SAE Report; Trial Visit Note.

### B.21.6 Medical Records / HIM
**Purpose:** Record completeness, coding, merge/unmerge, release of information, registry submission, retention.
**Worklist:** unsigned documents by clinician with ageing, incomplete records, coding queue, merge requests, release-of-information requests, registry export exceptions.
**Key requirements:** `HIM-010 [PRODUCT]` — merge/unmerge is an HIM-only function with dual authorisation, full audit, and reversible linkage; `HIM-020` — record release with requester, authority, scope, redaction applied, released items, date; `HIM-030` — retention and legal-hold flags.

### B.21.7 Stoma / Wound Care Nurse
**Header additions:** stoma type, site, formation date, output volume and consistency, peristomal skin condition, appliance in use; wound location, type, dimensions (L×W×D mm), tissue type percentages, exudate, odour, peri-wound skin, dressing regimen, pain, infection signs, photographs with date `[CCA CONFIG]`.
**Screens:** stoma assessment and education record; wound assessment with structured measurement and photograph; dressing plan; supply/appliance prescription.
**Documents:** Stoma Care Note; Wound Assessment and Management Note.

### B.21.8 Anaesthetist / Pre-anaesthesia
**Purpose:** Fitness assessment, anaesthetic plan, intra-operative record, post-anaesthesia recovery.
**Header additions:** planned procedure, ASA or equivalent `[CCA CONFIG]`, airway assessment, comorbidities, functional capacity, medications especially anticoagulants and antihypertensives, allergies, previous anaesthesia history and complications, investigations (ECG, echo, PFT, bloods) with dates, fasting status, consent for anaesthesia.
**Screens/fields:** pre-anaesthesia assessment (systems review, airway examination — Mallampati or equivalent `[CCA CONFIG]`, dentition, spine for regional, IV access, risk scores `[CCA CONFIG]`), anaesthetic plan (technique, airway plan, monitoring, post-op analgesia plan, HDU/ICU requirement, blood requirement), fitness decision (fit / fit with optimisation / not fit — with required optimisation and re-review date), intra-operative anaesthetic record (times, agents, doses, airway, ventilation parameters, fluids, blood products, vitals series, events, drugs administered with times), recovery record (score, vitals, pain, nausea, discharge-from-recovery criteria `[CCA CONFIG]`).
**Documents:** Pre-anaesthesia Assessment; Anaesthetic Plan; Intra-operative Anaesthetic Record; Post-anaesthesia Care Record.

### B.21.9 Blood Bank / Transfusion
**Purpose:** Group and screen, crossmatch, issue, transfusion reaction management — high-volume in oncology.
**Key requirements:** `BLD-010 [PRODUCT]` — transfusion order (component, volume/units, indication with pre-transfusion value, urgency, special requirements: irradiated, CMV-negative, leucodepleted, phenotype-matched `[CCA CONFIG]`, consent status), sample validity window `[CCA CONFIG]`, crossmatch result, unit identification (component, unit number, blood group, expiry), issue record, bedside two-person verification with both identities, start/stop times, volume transfused, observations at defined intervals `[CCA CONFIG]`, reaction record with type/severity/management/reporting, post-transfusion value.
**Documents:** Transfusion Request; Compatibility Report; Transfusion Administration Record; Transfusion Reaction Report.

---

## END OF DOCUMENT 2

**Part B is now complete (roles 1–21).**

**Continues in Document 3:** PART C — Screen-by-screen requirements, beginning with Registration and Intake screens and proceeding through every module.
