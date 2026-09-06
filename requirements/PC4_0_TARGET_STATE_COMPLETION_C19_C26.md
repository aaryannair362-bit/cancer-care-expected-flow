# CCA Oncology HIS + EMR — PC4.0 Target-State Completion for C.19-C.26

This file does **not** claim recovery of the lost Claude prose. It records the executable C.19-C.26 specification reconstructed from the supplied Part A/B role requirements and the already established CCA clinical workflow principles.

## SCR-PAT-001 — Pathology Worklist / Case Board
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** worklist
**Sections:** Reporting queue · Ancillary pending · Frozen section · Amendments / critical

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
**Repeatable tables:**
- Pathology cases: Accession · Patient / UHID · Specimen · Procedure · Primary site · Priority · Receipt date/time · TAT · Status · Ancillary pending · MDT deadline · Assigned pathologist · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-PAT-002 — Specimen Receipt & Accession
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Request verification · Container receipt · Identity / labelling · Fixation / adequacy · Discrepancy

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Collection date/time — datetime-local — required
- Receipt date/time — datetime-local — required
- Container count — number — required
- Fixative — select — required
- Labelling concordant — select — required
- Requisition concordant — select — required
- Specimen adequacy — select — required
- Discrepancy type — multiselect
- Discrepancy resolution — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Containers: Container ID · Label as received · Anatomical designation · Laterality · Orientation markers · Fixative · Integrity · Received at · Barcode
**Actions:** Save draft · View source provenance · Print / export · Generate accession · Print specimen/barcode labels · Quarantine discrepancy · Accept specimen · Sign / finalize · Create amendment / new version

## SCR-PAT-003 — Gross Examination / Macroscopy
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Specimen orientation · Measurements · Tumour / lesion · Margins / inking · Blocks submitted

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Specimen type — text — required
- Specimen dimensions — X — number — mm
- Specimen dimensions — Y — number — mm
- Specimen dimensions — Z — number — mm
- Specimen weight — number — g
- Tumour visible — select — required
- Tumour dimension — maximum — number — mm
- Distance to nearest margin — number — mm
- Inking scheme — textarea
- Gross description — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Blocks submitted: Block ID · Tissue / site · Orientation · Margin represented · Special processing · Comment
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-004 — Block / Slide Management & Processing Queue
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** worklist
**Sections:** Processing queue · Block register · Slide register · Special stains

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
**Repeatable tables:**
- Blocks / slides: Accession · Block ID · Slide ID · Tissue · Processing status · Stain · Created at · QC status · Location · Assigned
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-PAT-005 — Synoptic Oncology Pathology Report
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Specimen / procedure · Tumour · Histology / grade · Invasion · Margins · Nodes · Treatment effect · pTNM · Ancillary / biomarkers · Final diagnosis · Sign-out

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Procedure — select — required
- Final diagnosis — textarea — required
- Histological type — text — required
- Morphology code — text
- Grade — text
- Tumour size — greatest dimension — number — mm
- Tumour extent — textarea
- Lymphovascular invasion — select
- Perineural invasion — select
- Margin status — select
- Nodes examined — number
- Nodes positive — number
- Treatment effect present — select
- Pathological response grade / category — text
- pT — text
- pN — text
- pM — text
- pStage group — text
- Staging system / version — text
- Pathologist comment — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Biomarkers / ancillary: Marker / test · Method · Result · Unit / score · Interpretation · Specimen / block · Quality / adequacy · Report date
- Margins: Margin · Status · Distance · Unit · Involved structure · Comment
- Lymph node groups: Station / group · Examined · Positive · Largest metastasis · Extranodal extension · Comment
**Actions:** Save draft · View source provenance · Print / export · Validate synoptic completeness · Sign final report · Create addendum · Create amendment · Communicate critical result · Sign / finalize · Create amendment / new version
**Safety/alerts:** Block final sign-out when required synoptic elements are missing. · Do not replace cTNM with pTNM; publish a new pathological staging event.

## SCR-PAT-006 — Margin Assessment
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Margin inventory · Measurements · Overall margin conclusion

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Overall margin status — select — required
- Closest margin — text
- Closest margin distance — number — mm
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Per-margin assessment: Margin ID · Margin name · Status · Distance · Unit · Tumour at ink · Orientation / specimen · Comment
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-007 — Lymph Node Assessment
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Node inventory · Station / group assessment · Overall nodal conclusion

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Total nodes examined — number — required
- Total nodes positive — number — required
- Largest metastatic deposit — number — mm
- Extranodal extension — select
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Per-node station: Station / group · Examined · Positive · Isolated tumour cells · Micrometastases · Macrometastases · Largest deposit · ENE · Comment
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-008 — Treatment Effect / Pathological Response
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Pre-treatment context · Residual tumour · Response system · Pathological response

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Neoadjuvant therapy received — readonly — read-only/derived
- Therapy completion date — readonly — read-only/derived
- Interval to specimen — readonly — read-only/derived
- Residual tumour dimensions — text
- Treatment effect description — textarea — required
- Response grading system — text — required
- Response grade / category — text — required
- Pathologic complete response — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-009 — Pathological TNM Assignment
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Staging basis · pT · pN · pM · Stage group · Source evidence

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Staging system — text — required
- Staging version / edition — text — required
- pT — text — required
- pN — text — required
- pM — text
- pStage group — text — required
- Stage assignment rationale — textarea — required
- Clinical stage comparison — readonly — read-only/derived
- Concordance — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-010 — Ancillary / IHC / Biomarker Testing Tracker
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** worklist
**Sections:** Pending tests · Sent-outs · Resulted / interpretation pending

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
**Repeatable tables:**
- Ancillary / biomarker tests: Test · Block / specimen · Method · Ordered at · Sent at · Laboratory · Expected date · Result status · Result · Interpretation status · Owner · Days outstanding
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-PAT-011 — Molecular / Genomic Reporting
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Specimen / assay · Quality · Variants / alterations · Interpretation · Clinical significance · Sign-out

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Assay / panel — text — required
- Assay version — text — required
- Specimen / block — text — required
- Tumour content / adequacy — text
- Methodology — text — required
- Reference genome / transcript — text
- Overall interpretation — textarea — required
- Limitations — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Molecular findings: Gene / locus · Alteration · Variant classification · Allele fraction · Copy number / expression · Clinical significance · Therapy / trial relevance · Source / evidence
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-012 — Frozen Section / Intra-operative Pathology
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Theatre request · Specimen · Question · Frozen impression · Communication · Permanent reconciliation

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Theatre / OR — text — required
- Question from surgeon — textarea — required
- Specimen received at — datetime-local — required
- Frozen impression — textarea — required
- Result communicated to — text — required
- Communication method — select — required
- Communicated at — datetime-local — required
- Acknowledged by — text — required
- Permanent result concordance — select
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-013 — Second Opinion / External Pathology Review
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** External material · Prior diagnosis · Review findings · Concordance · Disposition

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- External institution — text — required
- External accession — text — required
- Material received — multiselect — required
- Prior diagnosis — textarea — required
- CCA review diagnosis — textarea — required
- Concordance — select — required
- Clinical impact of discrepancy — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-014 — Pathology Addendum / Amendment
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Original report · Change type · Change content · Reason · Notification · Signature

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Change type — select — required
- Reason — select — required
- Added / corrected content — textarea — required
- Clinical impact — textarea
- Consumers notified — multiselect
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-015 — Pathology Critical / Unexpected Result Communication
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** Critical finding · Communication · Acknowledgement · Escalation · Closure

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- Critical / unexpected finding — textarea — required
- Severity / urgency — select — required
- Communicated to — text — required
- Communicated at — datetime-local — required
- Method — select — required
- Acknowledged by — text — required
- Acknowledged at — datetime-local — required
- Action / escalation — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-016 — Pathology MDT Review Note
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** form
**Sections:** MDT case · Material reviewed · Key findings · Diagnostic/stage statement · Questions / recommendations

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
- MDT meeting / case — text — required
- Material reviewed — textarea — required
- Key pathology findings — textarea — required
- Diagnostic / staging statement — textarea — required
- Uncertainty / limitations — textarea
- Recommendation / further pathology work — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-PAT-017 — Specimen / Block / Slide Archive & Custody
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** worklist
**Sections:** Custody inventory · Location · Loan / release · Return / disposal

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
**Repeatable tables:**
- Custody items: Accession · Block / slide ID · Item type · Current location · Custody status · Released to · Released at · Expected return · Returned at · Disposition · Audit
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-PAT-018 — Pathology Quality / TAT Dashboard
**Module:** C.19 Pathology
**Role(s):** Pathology
**Kind:** worklist
**Sections:** Turnaround time · Backlog · Critical communications · Amendments · Quality events

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Requesting clinician / service — text — required
- Specimen / procedure date — datetime-local — required
- Primary site — text — required
- Laterality — select
- Clinical indication / question — textarea — required
- Neoadjuvant treatment summary — readonly — read-only/derived
- Prior pathology comparison — readonly — read-only/derived
**Repeatable tables:**
- Quality metrics: Metric · Period · Target · Actual · Status · Trend · Owner · Action
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-RAD-001 — Reporting Worklist
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** worklist
**Sections:** Reporting worklist · Critical findings · MDT preparation · Amendments

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
**Repeatable tables:**
- Reporting queue: Accession · Patient / UHID · Modality · Study · Acquired at · Priority · Purpose · Baseline · Status · Assigned radiologist · TAT · Critical flag · MDT date · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-RAD-002 — Study Protocolling
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Requested study · Protocol · Contrast · Safety · Coverage · Special instructions

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Requested study — text — required
- Protocol assigned — text — required
- Contrast decision — select — required
- Contrast agent — text
- Contrast volume — number — mL
- Contrast rate — number — mL/s
- Phases required — multiselect
- Anatomical coverage — textarea — required
- Creatinine / eGFR status — readonly — read-only/derived
- Contrast allergy status — readonly — read-only/derived
- Pregnancy status — readonly — read-only/derived
- Sedation / anaesthesia required — select
- Special instructions — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-003 — Structured Oncology Report
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Study identification · Indication · Technique · Comparison · Findings · Lesions · Response proposal · Impression · Recommendations · Critical result · Attestation

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Protocol used — text — required
- Contrast details — text
- Image quality — select — required
- Limitations — textarea
- Comparison studies — textarea
- Organ/system findings — textarea — required
- Impression — textarea — required
- Proposed response category — text
- Response criteria set / version — text
- Recommendation — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Lesion table: Lesion ID · Label · Organ / site · Laterality · Type · Target / non-target / new · Measurable · Measurement method · Long axis · Short axis · Unit · Series / image / slice · Prior measurement · Baseline change % · Nadir change % · Lesion status · Comment
**Actions:** Save draft · View source provenance · Print / export · Open image viewer · Designate baseline · Finalize report · Raise critical finding · Create addendum / amendment · Sign / finalize · Create amendment / new version

## SCR-RAD-004 — Lesion Tracking & Measurement Workspace
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Baseline · Target lesions · Non-target lesions · New lesions · Trend

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Persistent lesions: Lesion ID · Study date · Site · Target status · Long axis · Short axis · Unit · Baseline · Nadir · Absolute change · % from baseline · % from nadir · Status · Image reference · Measured by
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-005 — Radiologist Response Proposal
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Criteria · Target lesions · Non-target lesions · New lesions · Proposal · Uncertainty

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Criteria set — text — required
- Criteria version — text — required
- Baseline study — text — required
- Target lesion sum — baseline — readonly — read-only/derived
- Target lesion sum — current — readonly — read-only/derived
- Change from baseline — readonly — read-only/derived — %
- New lesion present — select — required
- Proposed response — text — required
- Confidence / qualifier — textarea
- Confirmation scan required — select
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-006 — Critical Finding Communication
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Finding · Communication · Acknowledgement · Escalation · Closure

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Critical finding — textarea — required
- Clinical urgency — select — required
- Communicated to — text — required
- Method — select — required
- Communication time — datetime-local — required
- Acknowledged by — text — required
- Acknowledgement time — datetime-local — required
- Escalation events — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-007 — Radiology Addendum / Amendment
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Original report · Change type · Reason · Content · Clinical impact · Notification

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Change type — select — required
- Reason — textarea — required
- Added / corrected content — textarea — required
- Clinical impact — textarea
- Ordering clinician re-notified — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-008 — External Imaging Reconciliation
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** worklist
**Sections:** External study inbox · Identity reconciliation · Import · Baseline eligibility · Review

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
**Repeatable tables:**
- External studies: Source institution · Study date · Modality · Media / transfer method · Import status · Matched patient · Episode · Duplicate status · Formal reread · Baseline designated · Reviewer · Outcome
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-RAD-009 — Radiology MDT Review Note
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** MDT case · Studies reviewed · Key findings · Resectability / response · Uncertainty · Recommendation

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- MDT meeting / case — text — required
- Studies reviewed — textarea — required
- Key imaging findings — textarea — required
- Resectability / response statement — textarea
- Uncertainty / limitations — textarea
- Recommendation / further imaging — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-010 — Image-Guided Procedure Note
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Procedure indication · Pre-procedure safety · Target / site · Technique · Samples / devices · Complications · Post-procedure

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Procedure — text — required
- Target lesion / site — text — required
- Laterality — select
- Consent status — readonly — read-only/derived
- Coagulation / platelet readiness — readonly — read-only/derived
- Technique / guidance modality — text — required
- Local anaesthetic / sedation — text
- Samples obtained — textarea
- Immediate complication — textarea
- Post-procedure instructions — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-011 — Contrast Safety / Reaction Record
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Pre-contrast screening · Administration · Reaction · Management · Outcome

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Contrast agent — text — required
- Lot / expiry — text
- Volume administered — number — required — mL
- Route — select — required
- Reaction occurred — select — required
- Reaction onset time — datetime-local
- Reaction manifestations — multiselect
- Reaction severity — select
- Management — textarea
- Outcome — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-012 — Imaging Comparison / Baseline Designation
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Candidate studies · Baseline designation · Comparison convention · Measurement provenance

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Designated baseline study — text — required
- Baseline designation reason — textarea — required
- Measurement criteria / convention — text — required
- Designated by — readonly — read-only/derived
- Designated at — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Comparison studies: Study · Date · Modality · External · Eligible for comparison · Reason · Selected
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-013 — Second Read / Peer Review
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Primary report · Second reader · Agreement · Discrepancy · Resolution

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Second reader — text — required
- Review outcome — select — required
- Discrepancy detail — textarea
- Clinical impact — textarea
- Resolution — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RAD-014 — Radiology TAT / Quality Dashboard
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** worklist
**Sections:** TAT · Backlog · Critical finding closure · Amendments · Peer review

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
**Repeatable tables:**
- Quality metrics: Metric · Period · Target · Actual · Status · Trend · Owner · Action
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-RAD-015 — Report Distribution & Acknowledgement
**Module:** C.20 Radiology
**Role(s):** Radiologist
**Kind:** form
**Sections:** Recipients · Delivery · Acknowledgement · Escalation

**Structured fields:**
- Cancer episode ID — text — required
- Accession number — text — required
- Study / modality — text — required
- Study date/time — datetime-local — required
- Clinical indication — textarea — required
- Specific clinical question — textarea — required
- Primary site — text
- Treatment phase — readonly — read-only/derived
- Baseline study — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Distribution / acknowledgement: Recipient · Role · Delivery method · Delivered at · Acknowledgement required · Acknowledged at · Status · Escalation
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-001 — Inpatient Oncology Worklist
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** worklist
**Sections:** Current inpatients · Admission requests · Deteriorating · Results · Discharges

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
**Repeatable tables:**
- Inpatient worklist: Ward / bed · Patient · UHID · Admission reason · LOS · Primary cancer · Treatment phase · Acuity / EWS · Critical results · Active therapies · Pending consults · Discharge barrier · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-IPD-002 — Admission Request / Bed Request
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Request · Clinical need · Bed / monitoring requirements · Acceptance

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Requested by — text — required
- Reason for admission — textarea — required
- Urgency — select — required
- Expected length of stay — number — days
- Bed type — select — required
- Monitoring level — text — required
- Isolation requirement — text
- Accepting clinician — text
- Acceptance decision — select
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-003 — Bed Assignment & Admission
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Bed allocation · Admission identity · Initial safety · Handover

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Ward — text — required
- Bed — text — required
- Admission date/time — datetime-local — required
- Source / referring location — text — required
- Admission diagnosis / reason — textarea — required
- Identity verified — select — required
- Allergies reconciled — select — required
- Handover received from — text — required
- Handover summary — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-004 — Inpatient Oncology Admission H&P
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Chief concern · Cancer history · Current treatment · Past medical history · Medication reconciliation · Allergies · Symptoms / ROS · Examination · Vitals · Labs / imaging · Problem list · Assessment · Plan · VTE / infection / nutrition / goals · Sign

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Chief concern / reason for admission — textarea — required
- History of present illness — textarea — required
- Cancer history / current status — readonly — read-only/derived
- Current treatment / last administration — readonly — read-only/derived
- Comorbidities — textarea
- Medication reconciliation — textarea — required
- Review of systems — textarea
- Physical examination — textarea — required
- Working diagnosis / assessment — textarea — required
- Initial problem list — textarea — required
- Plan by problem — textarea — required
- VTE assessment / prophylaxis plan — textarea
- Infection / isolation plan — textarea
- Nutrition plan — textarea
- Goals-of-care status — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-005 — Problem List Management
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Active problems · Resolved problems · Ownership · Linked orders

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Problem list: Problem · Onset · Status · Priority · Owner · Assessment · Plan · Linked orders · Last reviewed · Resolution date
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-006 — Inpatient Orders
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Medications · Fluids · Blood products · Diet / activity · Monitoring · Oxygen · VTE prophylaxis · Investigations · Procedures · Nursing instructions

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Inpatient orders: Order type · Item / instruction · Dose / parameter · Route · Frequency · Start · Stop · Priority · Indication · Owner · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-007 — Inpatient Medication Administration / Systemic Therapy Link
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Active medication orders · Systemic therapy authorisation · MAR · Five-value dose trace · Infusion events

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Medication administration: Medication · Order version · Standard dose · Calculated dose · Final ordered dose · Pharmacy prepared dose · Actual administered dose · Unit · Route · Scheduled time · Actual time · Status · Variance · Reason · Administered by · Second check
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version
**Safety/alerts:** Systemic anticancer therapy requires a signed order, pharmacy release and bedside verification before administration.

## SCR-IPD-008 — Daily Progress / Ward Round Note
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Interval events · Problem-oriented assessment · Vitals / trends · Labs / results · Treatment / toxicity · Consults · Plan · Discharge planning · Sign

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Interval events — readonly — read-only/derived
- Subjective / symptoms — textarea — required
- Examination — textarea — required
- Results reviewed — textarea — required
- Problem-oriented assessment — textarea — required
- Plan by problem — textarea — required
- Oncology treatment decision — textarea
- Discharge readiness / barriers — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-009 — Inpatient Nursing Assessment & Flowsheet
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Shift assessment · Vitals / EWS · Pain · Intake/output · Lines / drains · Skin / wounds · Falls / pressure injury · Medications / infusions · Education · Escalation · Handover

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Shift date/time — datetime-local — required
- Neurological / consciousness — textarea
- Respiratory assessment — textarea
- Cardiovascular assessment — textarea
- Pain score — number
- Nutrition / intake — textarea
- Fluid balance summary — textarea
- Mobility / falls risk — textarea
- Skin / pressure risk — textarea
- Patient education — textarea
- Escalation required — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Lines / drains / devices: Device ID · Type · Site · Insertion date · Assessment · Output · Care · Action
- Observations: Date/time · BP · Pulse · RR · Temp · SpO2 · Oxygen · Pain · EWS · Action
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-010 — Deterioration / Escalation Note
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Trigger · Assessment · Immediate intervention · Escalation · Response · Disposition

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Trigger — select — required
- Clinical time — datetime-local — required
- Assessment — textarea — required
- Immediate interventions — textarea — required
- Escalated to — text — required
- Escalation time — datetime-local — required
- Response / outcome — textarea — required
- Disposition — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-011 — Consult Request & Response
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Consult request · Clinical question · Response · Action / acknowledgement

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Consulting specialty — text — required
- Specific question — textarea — required
- Urgency — select — required
- Response required by — datetime-local
- Consultant response — textarea
- Recommendations — textarea
- Response date/time — datetime-local
- Requesting team action / acknowledgement — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-012 — Goals of Care / Advance Care Planning
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Participants · Capacity / communication · Goals / values · Treatment preferences · Decisions · Documentation / review

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Discussion date/time — datetime-local — required
- Participants — textarea — required
- Interpreter — text
- Patient goals / values — textarea — required
- Treatment preferences — textarea — required
- Resuscitation / escalation decision — text
- Decision-maker / surrogate — text
- Review trigger / date — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-013 — Transfer / Clinical Handover
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Transfer request · Clinical status · Handover · Receiving team · Transport

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- From location — text — required
- To location / facility — text — required
- Reason — textarea — required
- Clinical status at transfer — textarea — required
- Active treatments / infusions — textarea — required
- Lines / drains / devices — textarea
- Pending results / tasks — textarea — required
- Accepting clinician — text — required
- Handover communicated at — datetime-local — required
- Transport mode / accompanying staff — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-014 — Inpatient Live Board
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** worklist
**Sections:** Ward board · Acuity · Active therapies · Pending tasks · Escalations

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
**Repeatable tables:**
- Live inpatient board: Ward / bed · Patient · Acuity / EWS · Oxygen · Active infusions · Systemic therapy today · Isolation · Pending results · Pending consults · Escalation · Discharge target · Assigned nurse / clinician
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-IPD-015 — Discharge Readiness Worklist
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** worklist
**Sections:** Discharge candidates · Readiness gates · Medication reconciliation · Follow-up / transport

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
**Repeatable tables:**
- Discharge readiness: Patient · Target date · Clinical stability · Medication reconciliation · Discharge summary · Follow-up booked · Pending results plan · Education · Transport · Home support · Barrier · Owner · Status
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-IPD-016 — Inpatient Oncology Discharge Summary
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Admission details · Diagnoses · Hospital course · Procedures / treatment · Complications · Results · Medication reconciliation · Discharge medications · Follow-up · Pending results · Red flags · Sign

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Principal discharge diagnosis — textarea — required
- Other diagnoses / problems — textarea
- Hospital course — textarea — required
- Oncology treatment delivered — readonly — read-only/derived
- Procedures — textarea
- Complications — textarea
- Key results — textarea — required
- Discharge medication reconciliation — textarea — required
- Discharge medications — textarea — required
- Follow-up appointments — textarea — required
- Pending investigations and owner — textarea
- Red flags / contact instructions — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-IPD-017 — Death Documentation
**Module:** C.21 Inpatient Oncology
**Role(s):** Inpatient Oncology Clinician; Inpatient Oncology Nurse; Day Care / Infusion Nurse
**Kind:** form
**Sections:** Death event · Certification · Notifications · Devices / property · Episode state · Bereavement

**Structured fields:**
- Cancer episode ID — text — required
- Admission ID — text — required
- Ward / bed — text
- Admission date/time — datetime-local — required
- Consultant of record — text — required
- Admission reason — textarea — required
- Allergy status — readonly — read-only/derived
- Date/time of death — datetime-local — required
- Place of death — text — required
- Clinician confirming death — text — required
- Cause / certification details — textarea — required
- Family / next-of-kin notified — select — required
- Notification details — textarea
- Organ / tissue donation pathway — text
- Cancer episode closure reason — readonly — read-only/derived
- Bereavement referral / support — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-001 — Response Assessment Worklist
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** worklist
**Sections:** Due assessments · Proposed imaging responses · Unconfirmed · Overdue

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
**Repeatable tables:**
- Response worklist: Patient · Episode · Treatment / line · Assessment due · Trigger · Latest imaging · Radiology proposal · Clinical components · Status · Days overdue · Owner · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-RSP-002 — Response Assessment Initiation / Baseline
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Assessment reason · Baseline · Criteria · Source set · Planned components

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Assessment reason — select — required
- Baseline date — date — required
- Baseline imaging / pathology / marker source — textarea — required
- Criteria / framework — text — required
- Criteria version — text — required
- Assessment components required — multiselect — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-003 — Imaging Response Assessment
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Radiology source · Target lesions · Non-target lesions · New lesions · Radiology proposal

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Radiology report / study — text — required
- Baseline target sum — readonly — read-only/derived
- Current target sum — readonly — read-only/derived
- Change from baseline — readonly — read-only/derived — %
- Change from nadir — readonly — read-only/derived — %
- Non-target assessment — text
- New lesion status — select — required
- Radiologist-proposed response — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-004 — Target Lesion Comparison
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Target lesions · Baseline / nadir / current · Measurement provenance

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Target lesion comparison: Lesion ID · Site · Baseline date · Baseline measurement · Nadir date · Nadir measurement · Current date · Current measurement · Unit · % from baseline · % from nadir · Status · Source image
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-005 — Response Timeline Dashboard
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** worklist
**Sections:** Timeline · Treatment milestones · Imaging response · Clinical response · Biomarkers · Decisions

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
**Repeatable tables:**
- Response timeline: Date · Treatment phase · Source · Component · Value / category · Proposed / confirmed · Criteria · Decision · Owner
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-RSP-006 — Clinical / Biochemical / Pathological Response Components
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Clinical response · Biochemical response · Pathological response · Overall component interpretation

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Symptoms — textarea
- Examination — textarea
- Measurable clinical lesions — textarea
- Performance status — text
- Clinician impression — textarea
- Biochemical marker / test — text
- Biochemical baseline — number
- Biochemical nadir — number
- Biochemical current — number
- Biochemical unit — text
- Biochemical trend — readonly — read-only/derived
- Pathology specimen / source — text
- Response system / version — text
- Pathological grade / category — text
- Residual tumour — text
- Pathologic complete response — select
- Overall component interpretation — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-007 — Overall Response Confirmation
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Source evidence · Radiology proposal · Other components · Discordance · Clinician confirmation · Plan

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Radiologist-proposed response — readonly — read-only/derived
- Clinical response component — readonly — read-only/derived
- Biochemical response component — readonly — read-only/derived
- Pathological response component — readonly — read-only/derived
- Clinician-confirmed response — select — required
- Confirmation rationale — textarea — required
- Disease status event — select — required
- Next treatment decision — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Confirm response · Create progression / recurrence event · Create new line of therapy · Submit to MDT · Sign / finalize · Create amendment / new version

## SCR-RSP-008 — Response Discordance / Uncertainty Review
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Discordant components · Uncertainty · Additional evidence · Resolution

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Discordance type — multiselect — required
- Uncertainty / limitation — textarea — required
- Additional evidence required — textarea
- Resolution decision — textarea — required
- Resolved by — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-009 — Progression / Recurrence Event
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Event type · Evidence · Date / site · Same episode vs new primary · Line-of-therapy consequence · Notification

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Event type — select — required
- Event date — date — required
- Sites involved — textarea — required
- Supporting evidence — textarea — required
- Episode disposition — select — required
- New line of therapy required — select — required
- Clinical rationale — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-RSP-010 — Response Decision Handoff / MDT
**Module:** C.22 Response Assessment
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Confirmed response · Decision · Handoff owner · MDT requirement · Tasks

**Structured fields:**
- Cancer episode ID — text — required
- Assessment date — date — required
- Line of therapy — text
- Treatment phase / cycle — text
- Criteria / framework name — text
- Criteria version — text
- Confirmed response — readonly — read-only/derived
- Recommended next step — select — required
- Responsible specialty — text — required
- Due date — date — required
- MDT discussion required — select — required
- Handoff note — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-CMP-001 — Treatment Completion Worklist
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** worklist
**Sections:** Completion due · Summary incomplete · Awaiting sign · Distribution pending

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
**Repeatable tables:**
- Completion worklist: Patient · Episode · Modality · Last treatment date · Completion reason · Outstanding source records · Summary status · Signatory · Distribution status · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-CMP-002 — End-of-Treatment Clinical Review
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Reason for completion · Disease / response status · Treatment delivered · Toxicity / complications · Residual issues · Follow-up / surveillance · Decision

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
- Completion type — select — required
- Current disease / response status — text — required
- Key residual toxicities / complications — textarea
- Ongoing supportive needs — textarea
- Next care phase — select — required
- Next review / assessment date — date
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-CMP-003 — Cancer Treatment Summary
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Diagnosis & stage · Treatment intent · Systemic therapy delivered · Radiotherapy prescribed vs delivered · Surgery planned vs actual · Pathology · Response · Toxicity / complications · Cumulative exposure · Ongoing medications · Follow-up · Late effects / surveillance · Care team · Sign

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
- Diagnosis & staging snapshot — readonly — read-only/derived
- Treatment intent and plan history — readonly — read-only/derived
- Systemic therapy — planned vs actually administered — readonly — read-only/derived
- Radiotherapy — prescribed vs actually delivered — readonly — read-only/derived
- Surgery — planned vs actual procedure — readonly — read-only/derived
- Final pathology / pathological stage — readonly — read-only/derived
- Response history — readonly — read-only/derived
- Significant toxicities / complications — readonly — read-only/derived
- Cumulative exposure — readonly — read-only/derived
- Ongoing medications — readonly — read-only/derived
- Follow-up and surveillance plan — readonly — read-only/derived
- Late-effect considerations — readonly — read-only/derived
- Care-team contacts — readonly — read-only/derived
- Clinician synthesis / completion narrative — textarea — required
- Outstanding unresolved issue — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Reconcile source records · Generate final Treatment Summary · Sign Treatment Summary · Issue patient copy · Sign / finalize · Create amendment / new version

## SCR-CMP-004 — Modality Completion Reconciliation
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Systemic · Radiation · Surgery · Oral / continuous · Variance / unresolved discrepancy

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Modality reconciliation: Modality · Planned value / course · Actual delivered value / course · Start · End · Completed · Variance · Authorised modification source · Unresolved discrepancy
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-CMP-005 — Cumulative Exposure & Late-Effect Baseline
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Cumulative antineoplastic exposure · Organ-function baseline · Late-effect risk · Monitoring handoff

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
- Cardiac baseline at completion — textarea
- Renal baseline at completion — textarea
- Hepatic baseline at completion — textarea
- Neurological / functional baseline — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Cumulative exposure: Agent / modality · Exposure metric · Actual cumulative exposure · Unit · Source administrations / fractions · Known late-effect domain · Monitoring plan
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-CMP-006 — Treatment Completion Handoff
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Destination · Clinical handoff · Outstanding tasks · Responsible owner · Acceptance

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
- Handoff destination — select — required
- Handoff summary — textarea — required
- Outstanding investigations / results — textarea
- Owner — text — required
- Due date — date — required
- Receiving clinician / service — text — required
- Acceptance / acknowledgement — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-CMP-007 — Treatment Summary Distribution & Acknowledgement
**Module:** C.23 Treatment Completion
**Role(s):** Medical Oncology
**Kind:** form
**Sections:** Recipients · Patient copy · External providers · Acknowledgement · Reissue

**Structured fields:**
- Cancer episode ID — text — required
- Treatment plan version — text
- Treatment intent — select
- Treatment start date — date
- Treatment end date — date — required
- Reason for completion / discontinuation — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Summary distribution: Recipient · Role / relationship · Document version · Method · Sent at · Acknowledgement required · Acknowledged at · Status · Reissue reason
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-001 — Surveillance / Survivorship Worklist
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** worklist
**Sections:** Due today · Overdue · Investigations due · Late effects · Recall

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
**Repeatable tables:**
- Surveillance worklist: Patient · Episode · Primary cancer · Last treatment · Disease status · Follow-up due · Days overdue · Planned investigations · Late-effect flags · Assigned clinician · Recall status · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-SURV-002 — Surveillance Follow-up Visit
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** form
**Sections:** Interval history · Symptoms / red flags · Examination · Late effects · Results · Disease status · Health maintenance · Plan

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
- Interval history — textarea — required
- Recurrence red-flag symptoms — multiselect
- Physical examination — textarea — required
- Late effects reviewed — textarea — required
- Surveillance results reviewed — textarea — required
- Disease status — select — required
- Health maintenance / risk reduction — textarea
- Next review interval — text — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-003 — Surveillance / Survivorship Care Plan
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** form
**Sections:** Cancer / treatment summary · Surveillance schedule · Investigations · Late effects · Health promotion · Psychosocial / rehabilitation · Recurrence triggers · Ownership

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
- Surveillance intent / goal — textarea — required
- Follow-up frequency — text — required
- Duration of specialist surveillance — text
- Late-effect monitoring plan — textarea — required
- Recurrence red flags / escalation — textarea — required
- Responsible clinician / service — text — required
- Primary-care handoff requirement — select
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Planned surveillance investigations: Investigation · Frequency / trigger · Start · Stop · Owner · Rationale · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-004 — Surveillance Investigation Planner
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** form
**Sections:** Investigation schedule · Due / overdue · Results · Next due

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Surveillance investigations: Investigation · Clinical rationale · Frequency · Due date · Status · Ordered · Resulted · Result summary · Next due · Owner
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-005 — Late Effects Register
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** worklist
**Sections:** Active late effects · Risk domains · Interventions · Longitudinal follow-up

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
**Repeatable tables:**
- Late effects: Late effect / concern · Onset · Severity / grade · Attribution · Status · Intervention · Owner · Last reviewed · Next review
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-SURV-006 — Patient Survivorship Care Plan
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** form
**Sections:** Diagnosis and treatment summary · Care team contacts · Treatments received · Ongoing medications · Late effects to watch · Follow-up schedule · Planned tests and rationale · Red-flag symptoms · Rehabilitation / nutrition / psychosocial resources · Fertility / sexual-health support · Health maintenance · Next appointments · Issuance

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
- Diagnosis and treatment summary — readonly — read-only/derived
- Care team contacts — readonly — read-only/derived
- Treatments received — readonly — read-only/derived
- Ongoing medications — readonly — read-only/derived
- Late effects to watch — readonly — read-only/derived
- Follow-up schedule — readonly — read-only/derived
- Planned tests and rationale — readonly — read-only/derived
- Red-flag symptoms — readonly — read-only/derived
- Rehabilitation / nutrition / psychosocial resources — readonly — read-only/derived
- Fertility / sexual-health support — readonly — read-only/derived
- Health maintenance — readonly — read-only/derived
- Next appointments — readonly — read-only/derived
- Language / template version — text — required
- Interpreter / translation governance — text
- Patient / carer education delivered — select — required
- Comprehension / teach-back — select — required
- Date issued — date — required
- Re-issue reason — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-007 — Recurrence Suspicion / Re-entry
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** form
**Sections:** Trigger · Symptoms / findings · Evidence · Urgency · Re-entry destination · Episode decision

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
- Recurrence suspicion trigger — select — required
- Trigger detail — textarea — required
- Date identified — date — required
- Urgency — select — required
- Immediate investigations / actions — textarea — required
- Re-entry destination — select — required
- Same episode vs possible new primary — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-008 — Lost-to-Follow-up / Recall Queue
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** worklist
**Sections:** Overdue patients · Contact attempts · Barriers · Escalation · Outcome

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
**Repeatable tables:**
- Recall queue: Patient · Follow-up due · Days overdue · Risk / priority · Preferred contact · Contact attempts · Barrier · Next attempt · Escalation level · Outcome · Owner
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-SURV-009 — Survivorship Referrals & Support
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** form
**Sections:** Needs assessment · Referrals · Appointments · Outcomes

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Support referrals: Domain · Need / reason · Service / provider · Priority · Referral date · Appointment · Status · Outcome · Follow-up owner
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-SURV-010 — Surveillance Timeline / Dashboard
**Module:** C.24 Surveillance / Survivorship
**Role(s):** Medical Oncology; Nurse Navigator
**Kind:** worklist
**Sections:** Treatment history · Surveillance visits · Investigations · Late effects · Recurrence events

**Structured fields:**
- Cancer episode ID — text — required
- Surveillance phase — text
- Last treatment date — date
- Current disease status — select — required
- Next review date — date
**Repeatable tables:**
- Surveillance timeline: Date · Event · Category · Disease status · Result / outcome · Responsible service · Next milestone · Source
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-FIN-001 — Financial Counselling Worklist
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** worklist
**Sections:** Counselling queue · Authorisation pending · Estimates due · Financial barriers

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
**Repeatable tables:**
- Financial worklist: Patient · UHID · Payer · Treatment / order reference · Estimate status · Authorisation status · Deposit status · Financial barrier · Due date · Owner · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-FIN-002 — Payer / Policy Profile
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Payer identity · Policy · Coverage · Validity · Priority · Verification

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Policy / member number — text — required
- Coverage start — date
- Coverage end — date
- Sum insured / limit — number — INR
- Network / plan — text
- Verification status — select — required
- Verification reference — text
- Primary / secondary payer — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-003 — Patient Estimate
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Estimate basis · Treatment / service lines · Assumptions · Patient share · Validity · Approval

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Estimate number — readonly — read-only/derived
- Source treatment plan / order — text — required
- Estimate date — date — required
- Valid until — date — required
- Estimated gross amount — number — required — INR
- Estimated payer share — number — INR
- Estimated patient share — number — INR
- Estimate assumptions / exclusions — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Estimate lines: Service / drug / procedure · Quantity · Unit / basis · Rate · Amount · Coverage · Patient share · Source master
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-004 — Treatment Costing / Drug Estimate
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Treatment source · Drug / service costing · Prepared vs planned quantity · Non-drug charges · Total

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Total estimated treatment cost — readonly — read-only/derived — INR
- Clinical decision fields are read-only — readonly — read-only/derived
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Treatment costing: Sequence · Drug / service · Clinical order reference · Ordered quantity / basis · Chargeable quantity · Tariff / rate · Amount · Payer eligibility · Patient share · Source master / version
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-005 — Preauthorisation Request
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Payer / policy · Clinical administrative summary · Requested services · Documents · Submission · Decision

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Preauthorisation number — text
- Requested amount — number — required — INR
- Requested services / treatment — textarea — required
- Clinical administrative summary — textarea — required
- Supporting documents — multiselect — required
- Submitted at — datetime-local
- Payer decision — select
- Approved amount — number — INR
- Validity / conditions — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-006 — Query / Denial / Appeal Queue
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** worklist
**Sections:** Open queries · Denied claims / preauth · Appeals · Deadlines

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
**Repeatable tables:**
- Queries / appeals: Patient · Reference · Payer · Query / denial reason · Received at · Response due · Owner · Appeal status · Documents required · Status · Actions
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-FIN-007 — Deposit / Payment Receipt
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Payment context · Amount · Method · Receipt · Allocation

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Amount received — number — required — INR
- Payment method — select — required
- Transaction / reference number — text
- Receipt number — readonly — read-only/derived
- Received at — datetime-local — required
- Allocated to invoice / estimate — text
- Refundable / non-refundable policy reference — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-008 — Billable Event / Charge Capture
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Source event · Charge · Coding · Payer split · Posting

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Source clinical / operational event — text — required
- Service code — text — required
- Charge description — text — required
- Quantity — number — required
- Rate — number — required — INR
- Gross charge — readonly — read-only/derived — INR
- Payer share — number — INR
- Patient share — number — INR
- Posting status — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-009 — Package / Contract Rule Application
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Contract / package · Eligibility · Included / excluded · Limits · Rule result

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Package / contract — text — required
- Version — text — required
- Eligibility status — select — required
- Eligibility reason — textarea — required
- Inclusion / exclusion result — textarea — required
- Limit / cap applied — number — INR
- Override reason — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-010 — High-Cost Drug / Special Approval
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** High-cost trigger · Treatment source · Approval route · Decision · Validity

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Drug / service — text — required
- Source order / plan — text — required
- Estimated amount — number — required — INR
- Approval type — select — required
- Requested at — datetime-local — required
- Decision — select
- Decision reason / conditions — textarea
- Valid until — date
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-011 — Financial Counselling Note
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Financial understanding · Estimate / coverage explained · Options · Barriers · Decision / plan · Follow-up

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Counselling date/time — datetime-local — required
- Attendees — textarea — required
- Estimate explained — select — required
- Coverage / exclusions explained — select — required
- Financial barriers — textarea
- Assistance / options discussed — textarea
- Patient / family understanding — textarea — required
- Agreed financial plan — textarea — required
- Follow-up date — date
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-012 — Claim Tracking Queue
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** worklist
**Sections:** Submitted claims · Queries · Approved / paid · Denied · Outstanding

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
**Repeatable tables:**
- Claims: Claim number · Payer · Service period · Submitted amount · Submitted at · Status · Approved amount · Paid amount · Query / denial · Next action · Owner · Days outstanding
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-FIN-013 — Refund / Credit Note
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** form
**Sections:** Original transaction · Reason · Amount · Approval · Posting

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
- Original receipt / charge — text — required
- Refund / credit reason — select — required
- Amount — number — required — INR
- Approval required — select — required
- Approver — text
- Approval status — select
- Refund method — text
- Posting reference — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-FIN-014 — Finance Operations Dashboard
**Module:** C.25 Finance
**Role(s):** Finance / Billing
**Kind:** worklist
**Sections:** Revenue / charge capture · Authorisation TAT · Claims · Receivables · Financial barriers

**Structured fields:**
- Patient / UHID — text — required
- Cancer episode ID — text
- Payer category — select — required
- Payer / insurer — text
- Authorisation status — select
- Currency — select — required
**Repeatable tables:**
- Finance metrics: Metric · Period · Target · Actual · Status · Trend · Owner · Action
**Actions:** Open · Filter · Sort · Refresh · Export

## SCR-ADM-001 — User, Role & Permission Administration
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Users · Roles · Object permissions · Facility scope · Delegation · Break-glass · Audit

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- User ID — text — required
- Display name — text — required
- Professional registration number — text
- Assigned roles — multiselect — required
- Facility / department scope — multiselect — required
- Account status — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Role permissions: Role · Object / screen · View · Create · Edit · Sign · Approve / override · Facility scope
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-002 — Facility / Location Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Facility · Locations · Units · Beds / chairs / rooms · Operating hours

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Facility code — text — required
- Facility name — text — required
- Address / timezone — text — required
- Operating hours — textarea
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Locations / resources: Location code · Name · Type · Parent · Capacity · Status · Operating hours
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-003 — Department / Service Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Departments · Services · Routing · Ownership

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Departments / services: Code · Name · Parent · Clinical / administrative · Default location · Responsible role · Routing destinations · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-004 — Clinician / Roster Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Clinicians · Credentials · Specialty · Rosters · Leave / absence

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Clinicians / roster: User / clinician · Specialty · Registration no. · Facility · Department · Roster date · Start · End · Location · Availability · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-005 — Regimen Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Regimen identity · Indication / intent · Cycle schedule · Treatment sequence · Dosing rules · Premeds / hydration / supportive · Readiness · Monitoring · Dose modification · Version / approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Regimen code — text — required
- Regimen name — text — required
- Disease / indication — text — required
- Intent / setting — multiselect — required
- Line of therapy applicability — multiselect
- Cycle length — number — required — days
- Planned cycles / duration — text
- Protocol / source reference — text — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Treatment sequence: Sequence · Block · Drug / item · Dose basis · Standard dose · Dose unit · Route · Diluent · Volume · Concentration · Rate · Duration · Day(s) · Premed / hydration / treatment / supportive · Mandatory
- Readiness rules: Criterion · Source test / field · Operator · Threshold / rule · Unit · Freshness · Hard stop / override / warning · Exception
- Monitoring requirements: Investigation / assessment · Baseline · Frequency · Trigger · Owner
- Dose modification rules: Trigger · Grade / value · Action · Dose % / new dose · Delay / hold · Restart criteria · Approval role
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version
**Safety/alerts:** Synthetic/demo regimen content must never be represented as CCA-approved clinical content.

## SCR-ADM-006 — Formulary Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Drug identity · Formulations · Dosing metadata · Preparation · Compatibility / stability · Hazard flags · Inventory linkage · Approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Drug / generic name — text — required
- Brand / formulary display — text
- Drug code — text — required
- Hazardous / antineoplastic — select — required
- Vesicant / irritant classification — select
- Routes allowed — multiselect — required
- Dose units allowed — multiselect — required
- Dose basis allowed — multiselect — required
- Cumulative dose tracking required — select — required
- Compatibility / stability source — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Preparation rules: Diluent · Final concentration range · Container · Filter · Light protection · Stability / BUD · Storage · Source / version
- Formulations / vials: Strength · Unit · Container size · Concentration · Route · Storage · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-007 — Treatment Readiness Rule Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Rule set identity · Regimen / context · Criteria · Freshness · Severity / override · Approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Rule-set name — text — required
- Applicable regimen / therapy — text — required
- Applicable cycle / day — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Readiness criteria: Criterion · Clinical source · Test / field · Operator · Value / range · Unit · Freshness window · Missing-data behavior · Tier · Override role · Reason options
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-008 — Dose Modification & Rounding Rule Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Rule identity · Trigger · Modification action · Rounding · Restart · Approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Dose modification / rounding rules: Drug / regimen · Trigger type · Trigger value / grade · Dose action · Reduction % / dose · Rounding rule · Max variance · Delay / hold · Restart criteria · Override role · Source
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-009 — Laboratory Catalogue & Unit Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Test catalogue · Specimen · Units · Reference / plausibility · Critical results · Mapping

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Laboratory catalogue: Code · Test name · Specimen · Canonical unit · Allowed source units · Conversion rule · Reference range policy · Plausibility min · Plausibility max · Critical rule · LOINC / standard code · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-010 — Radiology Catalogue / Protocol Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Study catalogue · Modality · Protocol · Preparation · Safety prerequisites · Duration

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Radiology catalogue / protocols: Code · Study · Modality · Body region · Protocol · Contrast options · Preparation · Renal prerequisite · Pregnancy screen · MR safety · Duration · Standard code · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-011 — RT Template / OAR Constraint Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** RT template identity · Indication · Phases / targets · Dose/fractions · Technique · OAR constraints · IGRT · Peer review · Approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Template name — text — required
- Disease / indication — text — required
- Intent — text — required
- Technique / modality — text — required
- Peer review required — select — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- RT phases: Phase · Site · Laterality · Target volumes · Total dose · Fractions · Dose / fraction · Schedule
- OAR constraints: OAR · Laterality · Constraint type · Parameter · Operator · Value · Unit · Class · Source / protocol version
- IGRT / setup rules: Modality · Frequency · Matching structure · Translation tolerance · Rotation tolerance · Action if exceeded
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-012 — Surgery Procedure / Template Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Procedure master · Site/laterality · Pre-op requirements · Consent · Specimens · Devices · Post-op templates

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Surgical procedures: Procedure code · Procedure name · Disease / site · Laterality required · Approach options · Nodal options · Reconstruction options · Pre-op prerequisites · Consent type · Specimen schema · Post-op pathway · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-013 — Pathology Synoptic Template Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Template identity · Disease / specimen · Elements · Conditional rules · Staging · Version / approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Synoptic template name — text — required
- Disease / primary site — text — required
- Specimen / procedure applicability — multiselect — required
- Staging system / version — text
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Synoptic elements: Order · Element ID · Label · Type · Required · Unit / value set · Conditional parent / rule · Repeating · Standard code · Downstream mapping
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-014 — Consent / Document Template Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Document / consent identity · Content · Applicability · Language · Signature / witness · Expiry · Approval

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Template type — select — required
- Document / consent name — text — required
- Applicability rule — textarea — required
- Language — text — required
- Template body / schema — textarea — required
- Signature requirement — text — required
- Witness requirement — select
- Validity / expiry rule — text
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-015 — Value Set / Terminology Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Value sets · Terms · Codes · Synonyms · Mappings · Retirement

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Value set terms: Value set · Local code · Display · Standard system · Standard code · Synonyms · Order · Active · Effective from · Retired at · Replacement
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-016 — Unit / Normalisation Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Canonical units · Allowed source units · Conversions · Precision · Plausibility

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Units / normalisation: Concept / analyte · Canonical unit · Source unit · Conversion formula / factor · Precision · Rounding · Plausibility min · Plausibility max · Display rule · Approval
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-017 — Alert / Escalation Rule Master
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Alert identity · Trigger · Tier · Roles · Override · Escalation · Audit

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Author / accountable owner — readonly — read-only/derived
- Clinical / operational date-time — datetime-local
**Repeatable tables:**
- Alert / escalation rules: Rule ID · Context · Trigger expression · Tier · Presented to roles · Hard stop · Override roles · Required reason · Escalation target · Escalation interval · Effective version · Status
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version

## SCR-ADM-018 — Configuration Version, Audit & Release Manager
**Module:** C.26 Administration
**Role(s):** Hospital Management / Admin
**Kind:** form
**Sections:** Pending changes · Clinical review · Approvals · Release bundle · Activation · Rollback · Audit

**Structured fields:**
- Master record ID — readonly — read-only/derived
- Name / display label — text — required
- Status — select — required
- Version — text — required
- Effective from — date
- Effective to — date
- Owner / approving authority — text — required
- Change reason — textarea — required
- Release attestation — textarea — required
- Clinical sign-off complete — select — required
- Deployment / activation note — textarea
**Repeatable tables:**
- Configuration releases: Release ID · Masters / versions included · Submitted by · Clinical reviewers · Approval status · Effective date · Activation status · Rollback target · Change summary · Audit link
**Actions:** Save draft · View source provenance · Print / export · Sign / finalize · Create amendment / new version
