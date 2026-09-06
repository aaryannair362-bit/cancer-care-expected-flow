# PC4.0 Master Field Dictionary

Atomic executable field/table-column requirements represented: **4669**

| Screen | Module | Container | Field | Type | Required | Read-only | Unit |
|---|---|---|---|---|---:|---:|---|
| SCR-REG-001 | C.1 Registration | field | Date / date range | date | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Department | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Clinician | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Visit type | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Appointment status | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Payer | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Financial clearance | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Location | select | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Waiting-time threshold | number | No | No |  |
| SCR-REG-001 | C.1 Registration | field | toggles: Arrived-not-seen only, No-shows only, Walk-ins only, Has pending action. Free-text search (name / UHID / phone / national ID / appointment… | text | No | No |  |
| SCR-REG-001 | C.1 Registration | field | Age (Part E CALC-001) | readonly | No | Yes |  |
| SCR-REG-001 | C.1 Registration | field | Waiting time = now − check-in time (CALC-002) | readonly | No | Yes |  |
| SCR-REG-001 | C.1 Registration | field | counts strip aggregates | readonly | No | Yes |  |
| SCR-REG-001 | C.1 Registration | field | no-show derivation = appointment time + configured grace elapsed with no check-in (CALC-003) — system proposes No-show | readonly | No | Yes |  |
| SCR-REG-001 | C.1 Registration | field | Front Desk confirms. | readonly | No | Yes |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Per B.1.B View 1 — Appointment time | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Patient name | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | UHID | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Age | number | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Sex | select | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Contact (masked per ) | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Visit type | select | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Department | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Clinician | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Appointment status | select | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Check-in time | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Waiting time | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Current location | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Payer | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Financial clearance | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Pending action | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Alerts | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Referring dept/clinician | text | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Prior visit date | date | No | No |  |
| SCR-REG-001 | C.1 Registration | table:Table columns | Row actions. | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Identity: Title | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Given name | text | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Middle name | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Family name | text | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Preferred name | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Name in local script | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Date of birth | date | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Age at registration , read-only | readonly | No | Yes |  |
| SCR-REG-002 | C.1 Registration | field | Sex | select | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Gender identity | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Marital status | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Photograph (capture/upload, O ). Demographics: Nationality | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Religion | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Occupation | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Education level | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Ethnicity — all dropdowns, optionality . Contact: Mobile | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Alternate phone | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Email | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Preferred contact method | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Consent to contact by SMS/email/call (checkboxes, each timestamped) | datetime-local | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Address line 1/2, area, city, district, state, postcode, country (R per ). NOK: Name (R) | number | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Relationship | select | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Phone (R) | text | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Address | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Is legal representative (checkbox) | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Authorised to receive clinical information (checkbox + scope ). ID documents: Document type | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Number | number | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Issuing authority | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Expiry | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Verified (checkbox) + verification method + verified by/at | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Scan attachment. Payer: per SCR-FIN-001 embedded panel. Referral: Source | datetime-local | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Referring facility | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Referring clinician | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Referral date | date | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Referral reason | textarea | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Referral document upload | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Suspected cancer flag (checkbox → routes to Navigator). Consents: Registration/treat consent ( wording, versioned) — status, version, obtained by, … | datetime-local | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Data privacy consent | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Consent to photography . Preferences: Preferred language | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Interpreter required (checkbox + language) | number | Yes | No |  |
| SCR-REG-002 | C.1 Registration | field | Mobility assistance | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Communication needs | select | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Cultural/religious requirements. | text | No | No |  |
| SCR-REG-002 | C.1 Registration | field | Age from DOB (CALC-001) | readonly | No | Yes |  |
| SCR-REG-002 | C.1 Registration | field | Duplicate match score (CALC-004) — algorithm product-defined, threshold . | readonly | No | Yes |  |
| SCR-REG-002 | C.1 Registration | table:ID documents (type, number, expiry, verified, attachment, actions) | Entry | text | No | No |  |
| SCR-REG-002 | C.1 Registration | table:ID documents (type, number, expiry, verified, attachment, actions) | Date / time | datetime-local | No | No |  |
| SCR-REG-002 | C.1 Registration | table:ID documents (type, number, expiry, verified, attachment, actions) | Source / owner | text | No | No |  |
| SCR-REG-002 | C.1 Registration | table:Payer list (payer, policy, validity, priority, verified) | Entry | text | No | No |  |
| SCR-REG-002 | C.1 Registration | table:Payer list (payer, policy, validity, priority, verified) | Date / time | datetime-local | No | No |  |
| SCR-REG-002 | C.1 Registration | table:Payer list (payer, policy, validity, priority, verified) | Source / owner | text | No | No |  |
| SCR-REG-002 | C.1 Registration | table:Duplicate candidates (see below). | Entry | text | No | No |  |
| SCR-REG-002 | C.1 Registration | table:Duplicate candidates (see below). | Date / time | datetime-local | No | No |  |
| SCR-REG-002 | C.1 Registration | table:Duplicate candidates (see below). | Source / owner | text | No | No |  |
| SCR-REG-003 | C.1 Registration | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-REG-003 | C.1 Registration | field | Assessment / decision / outcome | select | No | No |  |
| SCR-REG-004 | C.1 Registration | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-REG-004 | C.1 Registration | field | Assessment / decision / outcome | select | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Patient (search/select, R) | select | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Appointment type | select | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Department (R) | text | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Resource (clinician/chair/machine/room, R) | text | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Date (R) | date | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Start time (R) | datetime-local | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Duration | select | No | No | min |
| SCR-REG-005 | C.1 Registration | field | Priority | select | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Reason for visit | textarea | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Linked order (select — e.g. the imaging order or treatment order this appointment fulfils) | select | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Preparation set | readonly | No | Yes |  |
| SCR-REG-005 | C.1 Registration | field | Interpreter required | readonly | Yes | Yes |  |
| SCR-REG-005 | C.1 Registration | field | Transport required | text | Yes | No |  |
| SCR-REG-005 | C.1 Registration | field | Isolation precautions | readonly | No | Yes |  |
| SCR-REG-005 | C.1 Registration | field | Accompanying person | text | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Notes to the receiving department | textarea | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Notification method(s). | select | No | No |  |
| SCR-REG-005 | C.1 Registration | field | Expected duration — for Day Care, from the regimen's summed administration time + premedication + observation (CALC-020) | readonly | No | Yes | min |
| SCR-REG-005 | C.1 Registration | field | Next-cycle due date from last administration + cycle length (CALC-021) | readonly | No | Yes |  |
| SCR-REG-005 | C.1 Registration | field | Slot utilisation % | readonly | No | Yes |  |
| SCR-REG-005 | C.1 Registration | field | Days waiting. | readonly | No | Yes |  |
| SCR-REG-005 | C.1 Registration | table:Slot grid (resource × time) | Entry | text | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Slot grid (resource × time) | Date / time | datetime-local | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Slot grid (resource × time) | Source / owner | text | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Waitlist (patient, requested type, requested by, urgency, requested-by date, days waiting ) | Entry | text | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Waitlist (patient, requested type, requested by, urgency, requested-by date, days waiting ) | Date / time | datetime-local | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Waitlist (patient, requested type, requested by, urgency, requested-by date, days waiting ) | Source / owner | text | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Conflicts. | Entry | text | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Conflicts. | Date / time | datetime-local | No | No |  |
| SCR-REG-005 | C.1 Registration | table:Conflicts. | Source / owner | text | No | No |  |
| SCR-REG-006 | C.1 Registration | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-REG-006 | C.1 Registration | field | Assessment / decision / outcome | select | No | No |  |
| SCR-REG-008 | C.1 Registration | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-REG-008 | C.1 Registration | field | Assessment / decision / outcome | select | No | No |  |
| SCR-REG-009 | C.1 Registration | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-REG-009 | C.1 Registration | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Height | number | Yes | No | cm |
| SCR-INT-002 | C.2 Intake | field | Height method | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Height source unit | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Height measurement date/time | datetime-local | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Height source | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Height comment | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Weight | number | Yes | No | kg |
| SCR-INT-002 | C.2 Intake | field | Weight method | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Weight condition qualifier | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Weight source unit | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Weight measurement date/time | datetime-local | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Weight source | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Dosing weight basis | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | BMI | readonly | No | Yes | kg/m² |
| SCR-INT-002 | C.2 Intake | field | BSA | readonly | No | Yes | m² |
| SCR-INT-002 | C.2 Intake | field | BSA formula name | readonly | No | Yes |  |
| SCR-INT-002 | C.2 Intake | field | BSA uncapped | readonly | No | Yes | m² |
| SCR-INT-002 | C.2 Intake | field | BSA capped | readonly | No | Yes | m² |
| SCR-INT-002 | C.2 Intake | field | BP systolic | number | No | No | mmHg |
| SCR-INT-002 | C.2 Intake | field | BP diastolic | number | No | No | mmHg |
| SCR-INT-002 | C.2 Intake | field | BP site | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | BP position | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Cuff size | text | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Mean arterial pressure | readonly | No | Yes | mmHg |
| SCR-INT-002 | C.2 Intake | field | Pulse rate | number | No | No | beats/min |
| SCR-INT-002 | C.2 Intake | field | Pulse rhythm | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Temperature | number | No | No | °C |
| SCR-INT-002 | C.2 Intake | field | Temperature site | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Respiratory rate | number | No | No | breaths/min |
| SCR-INT-002 | C.2 Intake | field | SpO₂ | number | No | No | % |
| SCR-INT-002 | C.2 Intake | field | Oxygen support | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Oxygen delivery device | text | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Oxygen flow rate | number | No | No | L/min |
| SCR-INT-002 | C.2 Intake | field | Pain score | number | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Pain instrument | text | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Vitals measurement date/time | datetime-local | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Allergy status | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Medication reconciliation status | select | Yes | No |  |
| SCR-INT-002 | C.2 Intake | field | Performance status instrument | text | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Performance status score | number | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Symptom / toxicity screen | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Infection / isolation screen | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Pregnancy applicability | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Last menstrual period | date | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Pregnancy test required | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Pregnancy test result | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Pregnancy test date/time | datetime-local | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Lactation status | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Fall-risk instrument / responses | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Fall-risk total | readonly | No | Yes |  |
| SCR-INT-002 | C.2 Intake | field | Nutrition screen | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Distress / psychosocial screen | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Vascular access summary | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Escalation finding / reason | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Escalated to | text | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Escalation severity | select | No | No |  |
| SCR-INT-002 | C.2 Intake | field | Escalation response / outcome | textarea | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Previous values panel per measurement (last 5 values | Entry | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Previous values panel per measurement (last 5 values | Date / time | datetime-local | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Previous values panel per measurement (last 5 values | Source / owner | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Medication reconciliation table (drug, strength, dose, route, frequency, indication, source, status, action taken | Entry | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Medication reconciliation table (drug, strength, dose, route, frequency, indication, source, status, action taken | Date / time | datetime-local | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Medication reconciliation table (drug, strength, dose, route, frequency, indication, source, status, action taken | Source / owner | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Allergy table | Entry | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Allergy table | Date / time | datetime-local | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Allergy table | Source / owner | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Symptom screen table (symptom, present, severity, onset, change since last visit, action). | Entry | text | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Symptom screen table (symptom, present, severity, onset, change since last visit, action). | Date / time | datetime-local | No | No |  |
| SCR-INT-002 | C.2 Intake | table:Symptom screen table (symptom, present, severity, onset, change since last visit, action). | Source / owner | text | No | No |  |
| SCR-INT-003 | C.2 Intake | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INT-003 | C.2 Intake | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INT-004 | C.2 Intake | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INT-004 | C.2 Intake | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INT-005 | C.2 Intake | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INT-005 | C.2 Intake | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INT-006 | C.2 Intake | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INT-006 | C.2 Intake | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INT-007 | C.2 Intake | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INT-007 | C.2 Intake | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INT-008 | C.2 Intake | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INT-008 | C.2 Intake | field | Assessment / decision / outcome | select | No | No |  |
| SCR-NAV-002 | C.3 Nurse Navigation | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-NAV-002 | C.3 Nurse Navigation | field | Assessment / decision / outcome | select | No | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Contact date/time | datetime-local | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Direction | select | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Method | select | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Contacted party | select | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Purpose | text | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Content summary | textarea | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Outcome | textarea | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Follow-up required | select | Yes | No |  |
| SCR-NAV-004 | C.3 Nurse Navigation | field | Next contact date | date | No | No |  |
| SCR-NAV-005 | C.3 Nurse Navigation | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-NAV-005 | C.3 Nurse Navigation | field | Assessment / decision / outcome | select | No | No |  |
| SCR-NAV-006 | C.3 Nurse Navigation | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-NAV-006 | C.3 Nurse Navigation | field | Assessment / decision / outcome | select | No | No |  |
| SCR-NAV-007 | C.3 Nurse Navigation | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-NAV-007 | C.3 Nurse Navigation | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Referral source / referrer | text | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Referral date | date | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Referral reason / question | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Documents reviewed | multiselect | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Presenting complaints | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | History of present illness | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Cancer chronology | readonly | No | Yes |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Prior systemic therapy | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Prior radiotherapy | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Prior surgery | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Comorbidities | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Current medications | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Family history | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Tobacco history | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Alcohol history | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Occupation / exposures | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Reproductive / menstrual history | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Pregnancy / lactation status | readonly | No | Yes |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Fertility preservation discussion | select | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Performance status instrument | select | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Performance status score | text | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Assessed by / date | text | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | General examination | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Site-specific tumour examination | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Systemic examination | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Pathology reviewed / source | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Imaging reviewed / source | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Laboratory results reviewed | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Biomarkers reviewed | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Cancer diagnosis / primary site | text | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Histology / morphology | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Clinical stage / staging system | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Disease status | select | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Treatment intent | select | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Assessment / problem list | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Treatment / investigation plan | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Investigations ordered | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Referrals | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | MDT required | select | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Follow-up interval / date | text | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Patient discussion / shared decision-making | textarea | Yes | No |  |
| SCR-MO-002 | C.4 Medical Oncology | field | Interpreter / attendees | textarea | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:Complaints | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:Complaints | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:Complaints | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:chronology | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:chronology | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:chronology | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:previous treatments (one per modality) | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:previous treatments (one per modality) | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:previous treatments (one per modality) | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:comorbidities | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:comorbidities | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:comorbidities | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:medications | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:medications | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:medications | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:allergies | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:allergies | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:allergies | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:family history | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:family history | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:family history | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:investigations reviewed (test, date, source, key result, link) | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:investigations reviewed (test, date, source, key result, link) | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:investigations reviewed (test, date, source, key result, link) | Source / owner | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:orders raised this visit. | Entry | text | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:orders raised this visit. | Date / time | datetime-local | No | No |  |
| SCR-MO-002 | C.4 Medical Oncology | table:orders raised this visit. | Source / owner | text | No | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Interval history since last visit | readonly | No | Yes |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Clinician interval narrative | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Symptoms and toxicity review | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Treatment tolerance | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Adherence | textarea | No | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Examination | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Results review | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Response assessment | textarea | No | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Assessment | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Plan decision | select | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Plan rationale | textarea | Yes | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Orders / referrals | textarea | No | No |  |
| SCR-MO-003 | C.4 Medical Oncology | field | Patient discussion | textarea | Yes | No |  |
| SCR-DX-001 | C.5 Diagnosis & Staging | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-DX-001 | C.5 Diagnosis & Staging | field | Assessment / decision / outcome | select | No | No |  |
| SCR-DX-002 | C.5 Diagnosis & Staging | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-DX-002 | C.5 Diagnosis & Staging | field | Assessment / decision / outcome | select | No | No |  |
| SCR-DX-003 | C.5 Diagnosis & Staging | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-DX-003 | C.5 Diagnosis & Staging | field | Assessment / decision / outcome | select | No | No |  |
| SCR-DX-004 | C.5 Diagnosis & Staging | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-DX-004 | C.5 Diagnosis & Staging | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Test/study | select | Yes | No |  |
| SCR-INV-001 | C.6 Investigations | field | Quantity/frequency | date | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Priority | select | Yes | No |  |
| SCR-INV-001 | C.6 Investigations | field | Requested date/time | datetime-local | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Required-by date (drives coordinator prioritisation, R for treatment-gating tests) | date | Yes | No |  |
| SCR-INV-001 | C.6 Investigations | field | Clinical indication (coded + narrative, mandatory, minimum length enforced, "routine" alone rejected — MO-INV-020 ) | textarea | Yes | No |  |
| SCR-INV-001 | C.6 Investigations | field | Specific question | textarea | Yes | No |  |
| SCR-INV-001 | C.6 Investigations | field | Purpose | select | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Relevant clinical details | readonly | No | Yes |  |
| SCR-INV-001 | C.6 Investigations | field | Body region / specimen site / laterality (conditional, R for imaging and pathology) | select | Yes | No |  |
| SCR-INV-001 | C.6 Investigations | field | Contrast requested (conditional) | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Isolation/precautions | readonly | No | Yes |  |
| SCR-INV-001 | C.6 Investigations | field | Interpreter/mobility | readonly | No | Yes |  |
| SCR-INV-001 | C.6 Investigations | field | Fasting required | readonly | Yes | Yes |  |
| SCR-INV-001 | C.6 Investigations | field | Linked appointment | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Copy results to | select | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Order set applied (name + version ). | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | field | Prerequisite status (e.g. creatinine present and within validity for a contrast study — CALC-070) | readonly | No | Yes |  |
| SCR-INV-001 | C.6 Investigations | field | expected result date from catalogue TAT | readonly | No | Yes |  |
| SCR-INV-001 | C.6 Investigations | field | conflict with scheduled treatment date . | readonly | No | Yes |  |
| SCR-INV-001 | C.6 Investigations | table:Catalogue results (test, code, specimen/modality, TAT, prerequisites, cost where displayed , add) | Entry | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Catalogue results (test, code, specimen/modality, TAT, prerequisites, cost where displayed , add) | Date / time | datetime-local | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Catalogue results (test, code, specimen/modality, TAT, prerequisites, cost where displayed , add) | Source / owner | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Selected orders (test, priority, required-by, indication, scheduling status, remove) | Entry | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Selected orders (test, priority, required-by, indication, scheduling status, remove) | Date / time | datetime-local | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Selected orders (test, priority, required-by, indication, scheduling status, remove) | Source / owner | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Recent duplicates panel — MO-INV-030 | Entry | text | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Recent duplicates panel — MO-INV-030 | Date / time | datetime-local | No | No |  |
| SCR-INV-001 | C.6 Investigations | table:Recent duplicates panel — MO-INV-030 | Source / owner | text | No | No |  |
| SCR-INV-002 | C.6 Investigations | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INV-002 | C.6 Investigations | field | Assessment / decision / outcome | select | No | No |  |
| SCR-INV-003 | C.6 Investigations | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-INV-003 | C.6 Investigations | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Meeting: Tumour stream / meeting type | select | Yes | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Target meeting date | date | Yes | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Urgency | select | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Reason for urgency | textarea | Yes | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Case category. Question: Specific question(s), question type) — MDT-020 : a submission without a specific question is rejected | select | Yes | No | kg/m² |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | "for discussion" is not an acceptable question. Clinical summary: Narrative (R, templated , seeded from the latest consultation note but editable, … | datetime-local | Yes | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Key clinical points (repeating short statements) | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Patient's own views/preferences recorded | date | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Comorbidities affecting treatment | readonly | No | Yes |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Performance status | readonly | No | Yes |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Prognosis considerations (optional narrative). Evidence: auto-assembled checklist (see Tables) with per-item include/exclude and comment | readonly | No | Yes |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Additional documents (upload/select). Logistics: Presenter | select | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Radiology review required | select | Yes | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Pathology review required (checkbox → accession selector + slides/blocks availability + pathologist assignment request) | select | Yes | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Patient/family attending (checkbox ) | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Estimated discussion time | select | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Conflict of interest declaration . | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | Completeness score and per-item status (CALC-080) against the meeting's required dataset | readonly | Yes | Yes |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | submission deadline = meeting date − configured lead time | readonly | No | Yes | kg/m² |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | days until meeting | readonly | No | Yes |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | field | evidence age per item. | readonly | No | Yes |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Evidence checklist | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Evidence checklist | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Evidence checklist | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Required for this meeting type () | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Required for this meeting type () | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Required for this meeting type () | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Present (Y/N) | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Present (Y/N) | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Present (Y/N) | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Source record | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Source record | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Source record | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Date | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Date | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Date | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Age in days | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Age in days | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Age in days | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Within validity window | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Within validity window | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Within validity window | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Include in pack | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Include in pack | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Include in pack | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Comment. Rows minimally | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Comment. Rows minimally | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Comment. Rows minimally | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Meeting | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Meeting | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Meeting | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Question | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Question | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Question | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Recommendation summary | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Recommendation summary | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Recommendation summary | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Action status | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Action status | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Action status | Source / owner | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Link. | Entry | text | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Link. | Date / time | datetime-local | No | No |  |
| SCR-MDT-001 | C.7 MDT / Tumour Board | table:Link. | Source / owner | text | No | No |  |
| SCR-MDT-003 | C.7 MDT / Tumour Board | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MDT-003 | C.7 MDT / Tumour Board | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Per participant: Name | readonly | No | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Discipline | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Role in meeting (Core / Extended / Observer / Presenter / Chair / Scribe) | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Attendance status (Present in person / Present remotely / Absent — apologies / Absent — no apologies / Delegated to ) | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Arrival time | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Departure time (for partial attendance — MDT-040 : a participant who leaves before a case is discussed must not be counted toward that case's quorum) | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Conflict of interest declared (checkbox + detail). Add ad-hoc attendee. | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Presenter | readonly | No | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Discussion started/ended | readonly | No | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Evidence reviewed (checklist, each with reviewer attribution: Imaging reviewed — by ; Pathology reviewed — by ; Prior treatment reviewed; Toxicity … | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Discussion narrative | textarea | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Key points (repeating). | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Repeating group: Option | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Proposed by | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Arguments for | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Arguments against | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Evidence cited | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Selected | select | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Reason not selected (R for non-selected options) — MDT-042 : options considered and rejected must be recorded with reasons | select | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | a minute showing only the chosen option is not an MDT record. | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Recommendation narrative (R) | textarea | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Structured recommendation: Responsible specialty | select | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Treatment intent | select | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Recommended modality sequence | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Recommended systemic regimen (link to Regimen Master, optional) | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Recommended RT (site, intent, optional) | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Recommended surgery (procedure, intent, optional) | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Further investigations required (linked orderables, repeating) | text | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Referrals required (repeating) | text | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Trial recommended | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Re-discussion required | date | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Patient discussion required (checkbox + who) | textarea | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Prognosis discussion flagged (checkbox) | textarea | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Rationale | number | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Guideline/evidence reference . | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Consensus | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Dissent, discipline, dissenting view, rationale, whether the dissenter wishes it recorded in distributed minutes (checkbox, default yes)) — dissent… | datetime-local | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Repeating: Action description (R) | textarea | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Action type | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Owner (named user, R — not a department, MDT-043 ) | text | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Owner role | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Due date (R) | date | Yes | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Priority | select | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Linked orderable/record | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Notes. | textarea | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | Quorum met (CALC-081) — rule, required disciplines, present disciplines, result, recomputed per case using presence at the time of that case | readonly | Yes | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | case elapsed time | readonly | No | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | meeting running time vs allocation | readonly | No | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | field | cases remaining. | readonly | No | Yes |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:Attendance table | Entry | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:Attendance table | Date / time | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:Attendance table | Source / owner | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:case list with per-case status chip | Entry | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:case list with per-case status chip | Date / time | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:case list with per-case status chip | Source / owner | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:options table | Entry | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:options table | Date / time | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:options table | Source / owner | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:dissent table | Entry | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:dissent table | Date / time | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:dissent table | Source / owner | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:actions table. | Entry | text | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:actions table. | Date / time | datetime-local | No | No |  |
| SCR-MDT-004 | C.7 MDT / Tumour Board | table:actions table. | Source / owner | text | No | No |  |
| SCR-MDT-005 | C.7 MDT / Tumour Board | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MDT-005 | C.7 MDT / Tumour Board | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Basis: Derived from MDT | readonly | No | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Deviation from MDT recommendation (checkbox → mandatory reason, and notification back to the MDT Coordinator and Chair — PLN-010 ) | textarea | Yes | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Basis if not MDT. Diagnosis snapshot: auto, read-only, frozen at signature (site, laterality, histology, grade, cTNM, pTNM, biomarkers, disease sta… | readonly | Yes | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Goals of treatment | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Expected benefit discussed | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Prognosis discussed. Modality sequence: ordered repeating group — Sequence number | date | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Modality | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned start | date | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned duration | number | No | No | min |
| SCR-PLN-001 | C.8 Treatment Plan | field | Dependency | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Owning specialty | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Status (Planned / In progress / Completed / Cancelled / Modified). Systemic component: Regimen (link to Regimen Master with version, R if systemic … | select | Yes | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Intent | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Line | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned number of cycles | number | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Cycle length | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned start date | date | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Dose modifications planned upfront (with reason, e.g. organ dysfunction) | number | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Route/access requirement (peripheral acceptable / central required) | select | Yes | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Required baseline investigations | readonly | Yes | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Required ongoing monitoring. RT component: Site(s) | readonly | Yes | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Intent | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Modality | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned total dose and fractions (indicative — the authoritative prescription lives in SCR-RO-002) | number | No | No | Gy |
| SCR-PLN-001 | C.8 Treatment Plan | field | Concurrent systemic therapy (Y/N + regimen) | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned start. Surgical component: Planned procedure | textarea | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Site/laterality | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Intent | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned timing | textarea | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Prerequisites. Supportive: Antiemetic strategy | number | No | No | mL/h |
| SCR-PLN-001 | C.8 Treatment Plan | field | Growth factor support (Y/N + criteria) | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Anti-infective prophylaxis | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Bone-modifying therapy | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Fertility preservation | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Nutrition | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Psychosocial | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Palliative care referral | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Dental assessment where indicated | textarea | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Cardiac monitoring plan | textarea | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Vaccination . Monitoring: Repeating — investigation, frequency, trigger, owner. Duration & milestones: Expected total duration | number | No | No | min |
| SCR-PLN-001 | C.8 Treatment Plan | field | Key milestone dates | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Planned response assessment points (after cycle n / at week n / post-RT + n weeks). Consent: Required consentswith status per consent. Patient disc… | readonly | Yes | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Interpreter | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Materials issued (with versions) | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Patient decision | select | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Patient-stated preferences. Financial: Estimate required (checkbox → routes to Finance) | select | Yes | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | High-cost drug flag . | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | Expected duration | readonly | No | Yes | min |
| SCR-PLN-001 | C.8 Treatment Plan | field | milestone dates | readonly | No | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | baseline investigation completeness | readonly | No | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | high-cost flag | readonly | No | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | cycles × cycle length projection | readonly | No | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | field | planned end date. | readonly | No | Yes |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:Modality sequence | Entry | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:Modality sequence | Date / time | datetime-local | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:Modality sequence | Source / owner | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:monitoring schedule | Entry | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:monitoring schedule | Date / time | datetime-local | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:monitoring schedule | Source / owner | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:consent requirements (consent type, required by, status, obtained date, version, obtained by) | Entry | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:consent requirements (consent type, required by, status, obtained date, version, obtained by) | Date / time | datetime-local | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:consent requirements (consent type, required by, status, obtained date, version, obtained by) | Source / owner | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:required baseline investigations with status | Entry | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:required baseline investigations with status | Date / time | datetime-local | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:required baseline investigations with status | Source / owner | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:MDT linkage history. | Entry | text | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:MDT linkage history. | Date / time | datetime-local | No | No |  |
| SCR-PLN-001 | C.8 Treatment Plan | table:MDT linkage history. | Source / owner | text | No | No |  |
| SCR-PLN-002 | C.8 Treatment Plan | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PLN-002 | C.8 Treatment Plan | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PLN-003 | C.8 Treatment Plan | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PLN-003 | C.8 Treatment Plan | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Active treatment plan version (read-only, linked) | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | On-plan / off-plan— off-plan requires reasonper PLN-030 | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Treatment intent | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Line of therapy. | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Search | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Filter by disease site / intent / line / modality | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Regimen (select from Regimen Master , R) | select | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Regimen version | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Protocol source/reference (read-only from master) | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Regimen status (Active / Inactive / Under review — inactive regimens are selectable only with permission and reason). | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Regimen name | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | alternative names | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | protocol code | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | disease/indication | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | intent(s) | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | line(s) | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | cycle length (days) | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | planned number of cycles | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | treatment days within cycle (e.g. D1, D8, D15) | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | drug list with dose basis, standard dose, unit, route, diluent, volume, rate/duration, sequence, treatment block | select | No | No | mL |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | mandatory premedication | text | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | mandatory hydration | text | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | mandatory supportive care | text | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | required baseline investigations | text | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | required ongoing monitoring | text | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | dose-modification rules | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | cumulative dose ceilings for tracked agents | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | special handling flags (vesicant, central access required, cardiac monitoring, extended observation) | text | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | regimen version, effective date, approver, change history. | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Cycle number | number | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Total planned cycles (from plan, editable with reason) | textarea | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Day(s) being ordered | select | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Planned administration date(s) | date | Yes | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Treatment location | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | First cycle (Y/N ) | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Delay from planned date in days, with reason field appearing when > configured tolerance . | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Height | date | No | No | cm |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Weight | date | No | No | kg |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Dosing weight (selector per INT-NUR-115 — Actual / Adjusted / Ideal / Clinician-specified, with the formula named and the resulting value shown, R) | select | Yes | No | kg |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | BSA | select | No | No | m² |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Renal function — serum creatinine, creatinine clearance (formula named, inputs shown including which weight was used, CALC-100), eGFR (CALC-101) | date | No | No | kg |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Hepatic function — bilirubin total/direct, AST, ALT, ALP, albumin | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Haematology — Hb, WBC, ANC (with derivation source per LAB-040), platelets | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Electrolytes where regimen-relevant | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Cardiac functionwhere the regimen requires it | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Pregnancy status where applicable | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Cumulative prior exposure for each tracked agent (cumulative dose, unit, % of configured ceiling , CALC-102) | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Prior infusion reactions to any component (agent, cycle, grade, management, rechallenge outcome) | select | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Active toxicities relevant to this regimen | date | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Current dose modifications in force (from prior cycles). | number | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | Cycle number default | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | next-cycle due date | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | delay in days | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | BSA | readonly | No | Yes | m² |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | CrCl | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | eGFR | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | ANC | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | cumulative exposure and % of ceiling | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | dose intensity of prior cycles | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | field | staleness of every imported value against the regimen's configured freshness windows . | readonly | No | Yes |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:Regimen drug list (read-only preview) | Entry | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:Regimen drug list (read-only preview) | Date / time | datetime-local | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:Regimen drug list (read-only preview) | Source / owner | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:prior cycles of this course (cycle, date, doses administered, dose intensity , toxicity, delays) | Entry | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:prior cycles of this course (cycle, date, doses administered, dose intensity , toxicity, delays) | Date / time | datetime-local | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:prior cycles of this course (cycle, date, doses administered, dose intensity , toxicity, delays) | Source / owner | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:cumulative exposure table (agent, cumulative dose, unit, ceiling, % of ceiling, monitoring status). | Entry | text | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:cumulative exposure table (agent, cumulative dose, unit, ceiling, % of ceiling, monitoring status). | Date / time | datetime-local | No | No |  |
| SCR-ORD-001 | C.9 Systemic Treatment Order | table:cumulative exposure table (agent, cumulative dose, unit, ceiling, % of ceiling, monitoring status). | Source / owner | text | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | Cumulative dose after this cycle (CALC-115) with % of ceiling | number | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | vesicant/irritant flag (read-only from formulary) | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | light protection required | text | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | filter required | text | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | central access required | text | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | maximum rate constraint | number | No | No | mL/h |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | stability window | text | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | incompatible co-administrations . | text | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | Calculated dose | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | rounding | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | variance % | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | concentration | readonly | No | Yes | mg/mL |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | the third of rate/volume/duration | readonly | No | Yes | mL |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | cumulative dose | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | total chair time | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | total fluid volume | readonly | No | Yes | mL |
| SCR-ORD-002 | C.9 Systemic Treatment Order | field | dose intensity vs protocol (CALC-117). Every calculation is expandable to show inputs, formula, source timestamps and rounding rule applied (per th… | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Sequence | number | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Treatment block | select | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Drug (from Formulary Master, read-only if from regimen; addable rows selectable) | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Formulation/strength | text | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Dose basis | select | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | STANDARD DOSE (value + unit, read-only from regimen master, with the master version stamped) | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Dosing parameter used | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | CALCULATED DOSE | readonly | No | Yes |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Dose modification % | number | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Modification reason | select | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Rounding applied (per Dose Rounding Rules , showing pre- and post-rounding values, CALC-111) | number | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | FINAL ORDERED DOSE | number | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Dose unit | select | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Variance from calculated (% and absolute; CALC-112) | number | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Variance reason (R when variance exceeds configured tolerance ) | textarea | Yes | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Route | select | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Diluent | select | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Diluent volume | number | No | No | mL |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Target concentration | readonly | No | Yes | mg/mL |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Infusion rate | select | No | No | mL/h |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Duration | readonly | No | Yes | min |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Day(s) of cycle | text | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Date | date | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Time (planned) | textarea | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Special instructions | textarea | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | PHARMACY PREPARED DOSE (empty at ordering) | datetime-local | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | ADMINISTERED DOSE (empty at ordering) | datetime-local | No | No |  |
| SCR-ORD-002 | C.9 Systemic Treatment Order | table:Table — drug rows: exact columns | Row actions (edit, remove — with reason for regimen-derived rows, duplicate, add note). | readonly | No | Yes |  |
| SCR-ORD-003 | C.9 Systemic Treatment Order | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORD-003 | C.9 Systemic Treatment Order | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | Verification checkboxes (product-defined, each individually recorded): patient identity confirmed | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | episode and diagnosis correct | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | regimen and version correct | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | cycle and day correct | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | dosing parameters reviewed and current | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | doses reviewed | number | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | variances reviewed and justified | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | supportive care reviewed | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | allergies reviewed | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | cumulative exposure reviewed | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | readiness reviewed. Order validity/expiry. Order-level notes to pharmacy. Order-level notes to nursing. Signature (re-authenticated). | date | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | All doses | readonly | No | Yes |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | total chair time | readonly | No | Yes |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | total volume | readonly | No | Yes | mL |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | expected end time | readonly | No | Yes |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | next cycle due date | readonly | No | Yes |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | field | order expiry. | readonly | No | Yes |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:The complete order table exactly as it will appear to pharmacy and nursing — ORD-110 | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:The complete order table exactly as it will appear to pharmacy and nursing — ORD-110 | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:The complete order table exactly as it will appear to pharmacy and nursing — ORD-110 | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:standard | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:standard | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:standard | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:calculated | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:calculated | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:calculated | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:final ordered | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:final ordered | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:final ordered | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:variance % | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:variance % | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:variance % | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:reason | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:reason | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:reason | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:attested. Readiness snapshot table (from SCR-RDY-001) | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:attested. Readiness snapshot table (from SCR-RDY-001) | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:attested. Readiness snapshot table (from SCR-RDY-001) | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:result | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:result | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:result | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:date | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:date | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:date | Source / owner | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:pass/fail/override. | Entry | text | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:pass/fail/override. | Date / time | datetime-local | No | No |  |
| SCR-ORD-004 | C.9 Systemic Treatment Order | table:pass/fail/override. | Source / owner | text | No | No |  |
| SCR-ORD-005 | C.9 Systemic Treatment Order | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORD-005 | C.9 Systemic Treatment Order | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORD-006 | C.9 Systemic Treatment Order | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORD-006 | C.9 Systemic Treatment Order | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORD-007 | C.9 Systemic Treatment Order | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORD-007 | C.9 Systemic Treatment Order | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | Overall readiness (CALC-120) — computed as: all mandatory criteria Pass → READY | text | Yes | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | any mandatory Fail → NOT READY | text | Yes | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | any Pending/Not available → INCOMPLETE | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | any override applied → READY WITH OVERRIDE. The system never converts NOT READY to READY by itself | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | only a clinician override does that, and the resulting status is a distinct third state that remains visible on every downstream screen — RDY-020 .… | select | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | Decision rationale (narrative, R when overriding) | select | Yes | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | Signature. | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | Per-criterion outcome | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | freshness | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | overall status | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | ANC where derived (CALC-121) | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | CrCl (CALC-100) | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | corrected calcium (CALC-122) | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | days since last cycle | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | field | time to planned administration. | readonly | No | Yes |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Category (Clinical review / Performance status / Symptoms / Toxicity / Haematology — CBC / ANC / Platelets / Haemoglobin / Renal function / Hepatic… | select | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Criterion name | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Required for this regimen? (Y/N/Conditional — from Regimen Master ) | select | Yes | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Source record type (Lab result / Vitals / Clinical assessment / Imaging / Consent record / Order / Manual attestation) | datetime-local | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Source record link | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Source date/time | datetime-local | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Age in hours/days | number | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Freshness window | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Within window? | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Result value | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Unit | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Reference/threshold applied (value + its source: regimen protocol / institutional default / trial protocol / clinician-specified — RDY-010 : the sc… | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Comparison operator | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Outcome (Pass / Fail / Needs review / Pending / Not applicable / Not available) | select | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Clinician decision (Accept / Override / Defer / Order test) | select | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Override reason | textarea | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Decided by | text | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Decided at | datetime-local | No | No |  |
| SCR-RDY-001 | C.10 Treatment Readiness | table:Table — criteria (exact columns) | Comment. | textarea | No | No |  |
| SCR-RDY-002 | C.10 Treatment Readiness | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RDY-002 | C.10 Treatment Readiness | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Height | date | No | No | cm |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Weight (same, plus delta from order weight and from previous cycle) | number | No | No | kg |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Dosing weight basis (displayed, checkbox) | number | No | No | kg |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | BSA (displayed with formula and inputs, checkbox) | text | No | No | m² |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | CrCl (displayed with formula and the weight used, checkbox) | number | No | No | kg |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Relevant labs with dates and staleness (checkbox per panel). Each checkbox is an individually recorded verification act with timestamp — PHA-020 : … | datetime-local | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | For each dose-based row, the system displays the pharmacist's independently recomputed calculated dose alongside the order's calculated dose (CALC-… | readonly | No | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Interaction alerts (drug–drug, drug–disease, drug–lab, duplicate therapy), each with: interacting agents, severity , mechanism, recommendation, dis… | select | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Checklist derived from the regimen master: mandatory antiemetics present, premedication present and correctly timed, hydration present, growth fact… | readonly | Yes | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | Recalculated doses | readonly | No | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | discrepancies | readonly | No | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | concentrations | readonly | No | Yes | mg/mL |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | cumulative doses and % of ceiling | readonly | No | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | total volume | readonly | No | Yes | mL |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | preparation time estimate | readonly | No | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | field | latest safe preparation start time from administration time and stability (CALC-130). | readonly | No | Yes |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Sequence | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Treatment block | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Drug | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Formulation | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Dose basis | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Standard dose | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Calculated dose | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Final ordered dose | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Variance % | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Variance reason (from order) | textarea | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Pharmacist recalculated dose | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Discrepancy | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Route | select | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Diluent | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Volume | number | No | No | mL |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Concentration | text | No | No | mg/mL |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Rate | number | No | No | mL/h |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Duration | number | No | No | min |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Cumulative dose after this cycle | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | % of ceiling | number | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Compatibility status from master | select | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Stability window | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Verification decision | select | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Note/reason | textarea | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Verified by | text | No | No |  |
| SCR-PHA-002 | C.11 Oncology Pharmacy | table:Table — per-row verification (exact columns) | Verified at. | datetime-local | No | No |  |
| SCR-PHA-003 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-003 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-004 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-004 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-005 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-005 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-006 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-006 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-007 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-007 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-008 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-008 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-009 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-009 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHA-010 | C.11 Oncology Pharmacy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHA-010 | C.11 Oncology Pharmacy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | field | Expected duration (CALC-020) | readonly | No | Yes | min |
| SCR-MAR-001 | C.12 Day Care / MAR | field | expected finish | readonly | No | Yes |  |
| SCR-MAR-001 | C.12 Day Care / MAR | field | chair occupancy and turnover | readonly | No | Yes |  |
| SCR-MAR-001 | C.12 Day Care / MAR | field | waiting time | readonly | No | Yes |  |
| SCR-MAR-001 | C.12 Day Care / MAR | field | weight delta vs order weight (CALC-013) | readonly | No | Yes | kg |
| SCR-MAR-001 | C.12 Day Care / MAR | field | gate status derivation (CALC-140). | readonly | No | Yes |  |
| SCR-MAR-001 | C.12 Day Care / MAR | field | Unit, chair, nurse, regimen, arrival status, gate blocked (which gate), pharmacy status, cleared/not cleared, has prior reaction, first cycle, dela… | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Scheduled time | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Chair/bay | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Patient name | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | UHID | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Age | number | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Sex | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Photograph thumbnail | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Regimen (short name) | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Cycle/Day | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Order version | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Expected duration | number | No | No | min |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Expected finish time | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Arrival status chip | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Gate status strip — eight micro-chips in fixed order: Identity | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Consent | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Clearance | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Readiness | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Product | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Verification | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Access | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Premed (each green/amber/red/grey) — MAR-005 | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Pharmacy status chip | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Allergy/prior-reaction icon | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Vitals status | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Today's weight (value + delta vs order weight) | number | No | No | kg |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Active toxicity max grade | select | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Assigned nurse | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Alerts icon stack | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Waiting time | text | No | No |  |
| SCR-MAR-001 | C.12 Day Care / MAR | table:Table columns (exact) | Row actions. | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Arrival: Arrival date/time | datetime-local | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Arrived from | select | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Mode of arrival (Ambulant / Wheelchair / Stretcher / Assisted) | select | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Accompanied by (name, relationship) | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Interpreter present. Identity verification: Verification method: Full name stated by patient | readonly | Yes | Yes |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Date of birth stated by patient | date | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | UHID on wristband scanned | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Photograph matched | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Photo ID document | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Address stated | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Carer confirmation (only where the patient cannot self-identify, with reason). Each selected method records: value confirmed (Y/N), and for scannin… | readonly | No | Yes |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Verified at. Wristband applied/present (Y/N; if applied now, printed by, at). Immediate concerns: Any new symptoms since last contact | readonly | No | Yes |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Feels well enough to proceed | select | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Fasting/preparation instructions followed where applicable. | textarea | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | Barcode match result | readonly | No | Yes |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | time since last cycle | readonly | No | Yes |  |
| SCR-MAR-002 | C.12 Day Care / MAR | field | waiting time start. | readonly | No | Yes |  |
| SCR-MAR-002 | C.12 Day Care / MAR | table:Identity verification log (method, value, result, timestamp) — retained on the administration record. | Entry | text | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | table:Identity verification log (method, value, result, timestamp) — retained on the administration record. | Date / time | datetime-local | No | No |  |
| SCR-MAR-002 | C.12 Day Care / MAR | table:Identity verification log (method, value, result, timestamp) — retained on the administration record. | Source / owner | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Order number and version (read-only) | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Order status (read-only — must be SIGNED/RELEASED, not draft, not superseded, not expired) | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Regimen, cycle, day (read-only, nurse confirms each with an explicit checkbox — MAR-009 : cycle and day confirmation is an affirmative act, because… | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Planned administration date matches today | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Order expiry not passed | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Any order changes since last cycle. | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Consent type required | readonly | Yes | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Consent status | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Consent version and date (read-only) | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Patient re-affirms willingness to proceed today (Y/N — a separate, per-visit act distinct from the formal consent document, MAR-011 ) | select | No | No | mL/h |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Reason if declined. | textarea | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Clearance status | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Clearing clinician name and timestamp (read-only) | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Conditions attached to clearance (read-only, rendered as a checkable list per RDY-070 — each condition must be individually marked met/not met by t… | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Request clearance action (where absent — routes to MO clearance queue with urgency). | select | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Readiness snapshot | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Readiness evaluated at (timestamp) | datetime-local | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Re-evaluate action | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Any criterion now expired flag. | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Weight today | select | Yes | No | kg |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Weight delta vs order weight (absolute and %) | number | No | No | kg |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Dose review required flag when delta exceeds tolerance (INT-NUR-111) — routes to MO, blocks administration until resolved or overridden | select | Yes | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Height (display, carry-forward action). | number | No | No | cm |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Full INT-NUR-200 set with reason for observation = "Pre-administration" | textarea | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | baseline for the day (this set is the comparator for all intra-infusion observations — MAR-012 ). | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Regimen-specific symptom checklist | multiselect | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | each active toxicity presented for re-grading | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | new symptoms captured | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | each entry writes to the longitudinal toxicity record (SCR-TOX-002). | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Where applicable per sex/age/: applicability, LMP, test required this cycle (Y/N per protocol), test result, test date/time. | datetime-local | Yes | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Fever in preceding period, symptoms of infection, current antimicrobials, isolation requirement, recent contacts . | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Nurse assessment summary (narrative) | textarea | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Fit to proceed (Y/N) | select | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | If no — reason and action (escalate / defer / cancel) | textarea | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Escalation record. | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | Weight delta | readonly | No | Yes | kg |
| SCR-MAR-003 | C.12 Day Care / MAR | field | readiness expiry | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | field | BSA recomputed with today's weight (displayed alongside the order BSA, not replacing it — MAR-013 ) | readonly | No | Yes | kg |
| SCR-MAR-003 | C.12 Day Care / MAR | field | time since clearance. | readonly | No | Yes |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:Readiness criteria | Entry | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:Readiness criteria | Date / time | datetime-local | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:Readiness criteria | Source / owner | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:clearance conditions | Entry | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:clearance conditions | Date / time | datetime-local | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:clearance conditions | Source / owner | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:active toxicities for re-grading | Entry | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:active toxicities for re-grading | Date / time | datetime-local | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:active toxicities for re-grading | Source / owner | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:vitals comparison (today vs last cycle). | Entry | text | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:vitals comparison (today vs last cycle). | Date / time | datetime-local | No | No |  |
| SCR-MAR-003 | C.12 Day Care / MAR | table:vitals comparison (today vs last cycle). | Source / owner | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Received from (Pharmacy / Ward / External) | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Received by | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Received at | datetime-local | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Transport condition | select | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Number of items expected vs received | number | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Condition on receipt. | select | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Second nurse identity (must differ from first — GEN-AUD-004) | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | itemised checklist mirroring the columns above | multiselect | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | discrepancies found | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | resolution | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | both signatures. MAR-014 — the double check is required for every hazardous/anticancer product | text | Yes | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | which products require it is but the *capability and enforcement* is product. | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | Barcode match | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | prepared-vs-ordered deviation | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | BUD remaining | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | field | projected BUD at planned start and at projected end of infusion (a product whose BUD expires mid-infusion must be flagged before starting — MAR-015 ). | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Sequence | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Treatment block | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Drug name | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Label barcode scanned (scan field + match result) | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Patient identifiers on label match patient (checkbox) | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Order number/version on label matches active order | number | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Drug matches order row (checkbox) | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Prepared dose on label (read-only, value #4) | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Final ordered dose (read-only, value #3) | readonly | No | Yes |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Prepared-vs-ordered deviation with tolerance status (CALC-135) | select | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Volume | number | No | No | mL |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Diluent | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Concentration | text | No | No | mg/mL |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Route on label matches order (checkbox) | select | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | BUD | datetime-local | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | BUD remaining at receipt and projected at planned start | datetime-local | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Storage condition maintained (checkbox) | number | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Light protection present where required (checkbox) | text | Yes | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Filter/set supplied where required (checkbox) | text | Yes | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Container intact (checkbox) | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Visual inspection | select | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Verification outcome (Accepted / Query / Rejected) | select | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Verified by | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Second checker | text | No | No |  |
| SCR-MAR-004 | C.12 Day Care / MAR | table:Table — per product (exact columns) | Timestamps. | datetime-local | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Full SCR-INT-007 field set. | date | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Device type | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Site | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Laterality — with automatic contraindication check against recorded lymphoedema, axillary dissection, AV fistula, ipsilateral surgery (MAR-016 ) | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Gauge | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Attempts | datetime-local | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Inserted by | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Insertion date/time | datetime-local | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Local anaesthetic used | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Ultrasound guided (Y/N) | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Insertion successful (Y/N) | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Complication at insertion | datetime-local | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Dressing applied | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Device lot where captured. | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Flushes freely (Y/N) | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Blood return present (Y/N) | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Resistance felt (Y/N) | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Site appearance | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Phlebitis/infiltration score where configured (item scores + total + band) | number | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Pain at site (score) | datetime-local | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Patient sensation on flush. | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Suitable for this order's requirements | select | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Basis for determination | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Determined by | text | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Determined at | datetime-local | No | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Vesicant drugs in this order | readonly | No | Yes |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Central access required by protocol . | text | Yes | No |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | Days in situ | readonly | No | Yes |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | suitability requirement derivation | readonly | No | Yes |  |
| SCR-MAR-005 | C.12 Day Care / MAR | field | contraindicated-limb check. | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | Session start time | datetime-local | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | nurse | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | chair | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | emergency medications available and in date (checklist, R — MAR-018 : availability of the protocol-required rescue medications is verified before t… | date | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | spill kit available | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | extravasation kit available | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | resuscitation equipment checked | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | patient positioned and comfortable | select | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | call bell in reach | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | patient briefed on what to report. | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | Observation schedule from the regimen's monitoring requirements (e.g. baseline, 15 min after start of drug X, every 30 min, at completion). Each ob… | datetime-local | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | All rows in a terminal state | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | total volume administered | number | No | No | mL |
| SCR-MAR-006 | C.12 Day Care / MAR | field | total session duration | number | No | No | min |
| SCR-MAR-006 | C.12 Day Care / MAR | field | post-treatment vitals (link to SCR-MAR-010) | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | patient condition | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | access device (flushed / removed / retained — with details) | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | disposal of cytotoxic waste per policy (checkbox) | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | session end time | datetime-local | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | nurse signature. | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | Actual duration | readonly | No | Yes | min |
| SCR-MAR-006 | C.12 Day Care / MAR | field | duration variance | readonly | No | Yes | min |
| SCR-MAR-006 | C.12 Day Care / MAR | field | volume infused | readonly | No | Yes | mL |
| SCR-MAR-006 | C.12 Day Care / MAR | field | fraction of dose administered on partial | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | administered-vs-ordered variance | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | cumulative administered dose update (CALC-102, using value #5) | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | session totals | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | next observation due | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | field | projected end time. | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Sequence | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Treatment block | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Drug | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Formulation | text | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | STANDARD DOSE (read-only) | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | CALCULATED DOSE (read-only) | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | FINAL ORDERED DOSE (read-only) | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | PHARMACY PREPARED DOSE (read-only, from SCR-PHA-005) | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | ACTUAL ADMINISTERED DOSE (editable, R — pre-filled from prepared dose but requiring affirmative confirmation per MAR-002) | number | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Dose unit | number | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Administered-vs-ordered variance (% and absolute, CALC-150) | number | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Variance reason | select | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Route (read-only from order; change requires prescriber authorisation) | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Access device used | select | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Diluent/volume (read-only) | readonly | No | Yes | mL |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Ordered rate (read-only) | readonly | No | Yes | mL/h |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Actual rate | number | Yes | No | mL/h |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Rate changes during infusion (expandable sub-table) | number | No | No | mL/h |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Volume infused | number | No | No | mL |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Start date/time | datetime-local | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | End date/time | datetime-local | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Actual duration (CALC-151) | number | No | No | min |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Duration variance vs ordered | number | No | No | min |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Administration status | select | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Partial administration detail (fraction of dose given , volume remaining, reason) | number | No | No | mL |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Administered by | readonly | No | Yes |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Independent checker (second nurse, where required) | text | Yes | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Product barcode scanned at administration ( match) | datetime-local | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Patient identity re-verified at administration (checkbox + method) | datetime-local | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Row notes | textarea | No | No |  |
| SCR-MAR-006 | C.12 Day Care / MAR | table:Table — administration rows: exact columns | Row actions. | text | No | No |  |
| SCR-MAR-007 | C.12 Day Care / MAR | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MAR-007 | C.12 Day Care / MAR | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Reaction onset time (button-captured, editable) | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Suspected agent | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Infusion stopped (toggle + time) | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Symptoms | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Severity impression (initial). | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Repeating time-stamped entries: time, observation/vitals, symptom change, intervention given, responder present. Vitals sets link to the observatio… | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | volume/dose infused at onset . | datetime-local | No | No | mL |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Prior exposure to this agent | readonly | No | Yes |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | prior reactions to this agent | readonly | No | Yes |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | premedication given this cycle | readonly | No | Yes |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | infusion rate at onset | datetime-local | No | No | mL/h |
| SCR-MAR-008 | C.12 Day Care / MAR | field | concurrent medications | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | reaction grade ( terminology, R) | select | Yes | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | reaction type | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | attribution to agent. | datetime-local | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Repeating: intervention, drug interventions with drug/dose/route/time/administered by, response to intervention, time. | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Outcome | datetime-local | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Resolution time duration | number | No | No | min |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Observation period extended (Y/N + duration) | select | No | No | min |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Discharged / admitted | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Follow-up arranged. | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Rechallenge attempted today (Y/N) | datetime-local | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | If yes: restart time, restart rate, premedication given, outcome | datetime-local | No | No | mL/h |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Future rechallenge | select | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Decided by | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Future precautions (structured + narrative) — written back to the allergy/reaction record (SCR-INT-004) so it appears on every future order and adm… | textarea | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Adverse drug reaction report required (Y/N) | select | Yes | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | report reference | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | serious criteria met (checkboxes) | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | reported to (pharmacovigilance / sponsor for trial patients / institutional incident system) | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | reported by/at. | text | No | No |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | Time to onset | readonly | No | Yes |  |
| SCR-MAR-008 | C.12 Day Care / MAR | field | dose/volume at onset | readonly | No | Yes | mL |
| SCR-MAR-008 | C.12 Day Care / MAR | field | duration of reaction | readonly | No | Yes | min |
| SCR-MAR-008 | C.12 Day Care / MAR | field | cumulative reaction count for this agent for this patient. | readonly | No | Yes |  |
| SCR-MAR-009 | C.12 Day Care / MAR | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MAR-009 | C.12 Day Care / MAR | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MAR-010 | C.12 Day Care / MAR | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MAR-010 | C.12 Day Care / MAR | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MAR-011 | C.12 Day Care / MAR | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MAR-011 | C.12 Day Care / MAR | field | Assessment / decision / outcome | select | No | No |  |
| SCR-MAR-012 | C.12 Day Care / MAR | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-MAR-012 | C.12 Day Care / MAR | field | Assessment / decision / outcome | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | Days since onset | readonly | No | Yes |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | peak grade | readonly | No | Yes |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | trend | readonly | No | Yes |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | days since last grading | readonly | No | Yes |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | duration of each grade level | readonly | No | Yes | min |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | cumulative days at grade ≥ threshold | readonly | No | Yes |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | field | count of toxicity-driven dose modifications. | readonly | No | Yes |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Toxicity term (coded terminology) | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Category/system | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Onset date | date | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Days since onset | number | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Grade at onset | datetime-local | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Current grade | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Peak grade | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Grade trend (improving / stable / worsening, from the last two gradings) | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Last graded date | date | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Last graded by | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Days since last grading (overdue flag ) | number | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Attribution | datetime-local | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Suspected agent(s) | number | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Treatment cycle/fraction at onset | datetime-local | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Current status (Active / Improving / Resolved / Resolved with sequelae / Chronic / Unknown) | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Interventions in place | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Treatment impact (none / dose reduced / delayed / held / discontinued) | number | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Linked records | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — active toxicities (exact columns) | Actions. | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Date | date | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Toxicity | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Grade | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Decision (reduce/delay/hold/discontinue) | select | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Magnitude (e.g. −25%) | number | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Decided by | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Linked order version | text | No | No |  |
| SCR-TOX-001 | C.13 Toxicity / Adverse Events | table:Table — treatment impact log | Outcome. | select | No | No |  |
| SCR-TOX-002 | C.13 Toxicity / Adverse Events | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-TOX-002 | C.13 Toxicity / Adverse Events | field | Assessment / decision / outcome | select | No | No |  |
| SCR-TOX-003 | C.13 Toxicity / Adverse Events | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-TOX-003 | C.13 Toxicity / Adverse Events | field | Assessment / decision / outcome | select | No | No |  |
| SCR-TOX-004 | C.13 Toxicity / Adverse Events | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-TOX-004 | C.13 Toxicity / Adverse Events | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Regimen/protocol (from Regimen Master where the oral agent is part of a named regimen, else standalone) | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Drug (Formulary, R) | text | Yes | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Formulation and strength | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Dose basis (fixed / mg/m² / mg/kg) | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Standard dose (from master) | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Calculated dose | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Dose modification % and reason | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Final prescribed dose | number | Yes | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Dose unit | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Achievable from available strengths (Y/N — with the tablet combination shown, CALC-160) | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Dose per administration | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Number of units per administration . | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Frequency | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Timing | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Schedule pattern | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Cycle length (days, conditional) | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Days on/off (conditional, R for cyclical) | number | Yes | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Cycle number | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Start date (R) | date | Yes | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Planned duration or number of cycles | number | No | No | min |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Planned end date | date | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | First-dose date and time. | date | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Food instruction | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Fluid | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Swallow whole / may crush (from formulary) | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Handling precautions (hazardous drug handling for the patient and household ) | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Storage | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Missed-dose instruction (structured, from the drug's patient-information master , R — ORL-020 : this must be a structured, drug-specific, versioned… | number | Yes | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Vomited-dose instruction | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | What to do if a dose is late. | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Quantity to dispense | number | Yes | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Days supply | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Refills authorised | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Refill interval | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Dispense-to-next-review constraint — the system must not authorise a supply extending beyond the next monitoring review without an explicit overrid… | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Dispensing location | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Patient collection or delivery. | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Required baseline investigations | readonly | Yes | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Ongoing monitoring schedule (repeating: test, frequency, next due ) | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Clinical review interval | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Specific monitoring for this drug (e.g. blood pressure, ECG, ophthalmic, dermatological, thyroid — per drug) | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Toxicity thresholds for dose modification displayed for reference. | number | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Interaction check results (drug–drug including OTC and herbal, drug–food including specific foods , drug–disease) | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Disposition per alert | select | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Medications to avoid (listed for the patient sheet). | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | Calculated dose | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | achievable-dose combination | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | days supply | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | planned end date | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | next monitoring due | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | cumulative exposure where tracked | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | field | adherence-expected pill count for reconciliation at review (CALC-162). | readonly | No | Yes |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:Dose history (date, dose, reason for change, prescriber) | Entry | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:Dose history (date, dose, reason for change, prescriber) | Date / time | datetime-local | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:Dose history (date, dose, reason for change, prescriber) | Source / owner | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:dispensing history (date, quantity, days supply, dispensed by, collected by) | Entry | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:dispensing history (date, quantity, days supply, dispensed by, collected by) | Date / time | datetime-local | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:dispensing history (date, quantity, days supply, dispensed by, collected by) | Source / owner | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:monitoring schedule with due/overdue status | Entry | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:monitoring schedule with due/overdue status | Date / time | datetime-local | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:monitoring schedule with due/overdue status | Source / owner | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:interaction alerts. | Entry | text | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:interaction alerts. | Date / time | datetime-local | No | No |  |
| SCR-ORL-001 | C.14 Oral / Continuous Therapy | table:interaction alerts. | Source / owner | text | No | No |  |
| SCR-ORL-002 | C.14 Oral / Continuous Therapy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORL-002 | C.14 Oral / Continuous Therapy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORL-003 | C.14 Oral / Continuous Therapy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORL-003 | C.14 Oral / Continuous Therapy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORL-004 | C.14 Oral / Continuous Therapy | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-ORL-004 | C.14 Oral / Continuous Therapy | field | Assessment / decision / outcome | select | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Decision | select | Yes | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Reason | select | Yes | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Clinical rationale | textarea | Yes | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Interruption start date | date | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Last dose taken date | date | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Restart criteria | textarea | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Review date | date | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Restart date | date | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Restart dose | text | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Remaining supply disposition | select | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Patient instruction issued | select | Yes | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Patient contacted | select | Yes | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Contact date/time | datetime-local | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Contact method | select | No | No |  |
| SCR-ORL-005 | C.14 Oral / Continuous Therapy | field | Understanding confirmed | select | Yes | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | Pathway state (CALC-170) | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | days in state | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | fractions delivered | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | cumulative delivered dose (CALC-171) | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | fractions remaining | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | gap days (CALC-172) | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | projected completion (CALC-173) | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | elapsed treatment days (CALC-174). | readonly | No | Yes |  |
| SCR-RO-001 | C.15 Radiation Oncology | field | Pathway state, treatment site, intent, modality, technique, unit, treating RO, concurrent chemo Y/N, interrupted, target-interval breach, QA status… | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Patient name | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | UHID | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Age/Sex | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Primary site & histology | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Stage (c and p, distinguished) | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Treatment intent | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Treatment site(s) and laterality | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Modality | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Technique | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Phase (n of m) | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Prescribed total dose | number | No | No | Gy |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Prescribed fractions | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Dose per fraction | number | No | No | Gy |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Pathway state chip (Consult done → Prescription signed → Simulation booked → Simulated → Contouring in progress → Contouring complete → Planning in… | textarea | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Days in current state with target interval colouring | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Blocking item (named) | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Prescription version | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Plan version | textarea | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | QA status | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Fractions delivered / prescribed | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Cumulative delivered dose | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Missed fractions count | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Gap days | number | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Projected completion date | date | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Concurrent systemic therapy (regimen, cycle/day) | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Next OTV due | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Current max toxicity grade | select | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Assigned unit | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Alerts | text | No | No |  |
| SCR-RO-001 | C.15 Radiation Oncology | table:Table columns (Pathway Board — exact) | Row actions. | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Prior RT received | select | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Repeating group per prior course: Treating centre | readonly | No | Yes |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Site treated (coded anatomical) | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Laterality | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Technique | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Modality | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Total dose | number | No | No | Gy |
| SCR-RO-002 | C.15 Radiation Oncology | field | Fractions | number | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Dose per fraction | number | No | No | Gy |
| SCR-RO-002 | C.15 Radiation Oncology | field | Start date | date | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | End date | date | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Concurrent systemic therapy | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Documentation available (Y/N + attachment) | datetime-local | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Anatomical overlap with the currently proposed target | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Cumulative dose considerations to specific OARs (repeating: OAR, prior dose, source of information, remaining tolerance assessment) | number | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Assessment of re-irradiation feasibility (narrative, R when overlap ≠ none). | textarea | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Cardiac implantable electronic device (None / Pacemaker / ICD / CRT / Loop recorder — R) | textarea | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Device manufacturer/model | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Pacing dependency | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Device management plan | select | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Other implants (prosthesis, expander, spacer, marker seeds, stents) with material and location. RO-020 — a prescription cannot be signed for a pati… | number | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Indication | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Target site(s) (repeating: site, laterality, coded) | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Evidence basis / protocol reference | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Alternatives considered (repeating with reasons) | textarea | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Contraindications assessed (checklist: pregnancy, prior RT overlap, connective tissue disease, inability to lie still or position, active infection… | datetime-local | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Fitness for the planned course | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Anticipated acute toxicity | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Anticipated late toxicity | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Expected benefit | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Estimated course duration. | number | No | No | min |
| SCR-RO-002 | C.15 Radiation Oncology | field | Topics covered (checklist) | multiselect | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Risks discussed with specifics | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Alternatives including no treatment | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Fertility/gonadal dose discussion where relevant | number | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Pregnancy status confirmed where applicable | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Patient decision | select | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Interpreter | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Materials issued (version) | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Consent required (Y/N → creates consent task linked to the prescription per PLN-040). | select | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Recommendation (Proceed to prescription / Defer pending investigation / Not indicated — with reason / Refer back to MDT) | textarea | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Investigations required before simulation (linked orderables) | text | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Dental/nutrition/other pre-RT assessments required (e.g. dental review before head-and-neck RT, gastrostomy consideration) | textarea | Yes | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Simulation urgency | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Target start date | date | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Concurrent systemic therapy coordination (regimen, timing relative to RT). | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | Dose per fraction of prior courses | readonly | No | Yes | Gy |
| SCR-RO-002 | C.15 Radiation Oncology | field | interval since prior RT | readonly | No | Yes |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | interval since surgery | readonly | No | Yes |  |
| SCR-RO-002 | C.15 Radiation Oncology | field | interval since last systemic cycle . | readonly | No | Yes |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:Prior RT courses | Entry | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:Prior RT courses | Date / time | datetime-local | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:Prior RT courses | Source / owner | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:target sites | Entry | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:target sites | Date / time | datetime-local | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:target sites | Source / owner | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:imaging reviewed (study, date, key findings, link) | Entry | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:imaging reviewed (study, date, key findings, link) | Date / time | datetime-local | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:imaging reviewed (study, date, key findings, link) | Source / owner | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:pre-RT assessment requirements with status. | Entry | text | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:pre-RT assessment requirements with status. | Date / time | datetime-local | No | No |  |
| SCR-RO-002 | C.15 Radiation Oncology | table:pre-RT assessment requirements with status. | Source / owner | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Course ID | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Course intent | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Number of phases | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Course start target date | date | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Treating unit(s) | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Treating RO | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Backup RO. | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Diagnosis, primary site, laterality, histology, grade | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | cTNM and pTNM with systems | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | disease status | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | performance status with date | date | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | prior RT summary | textarea | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | CIED status and management plan | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | pregnancy status | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | concurrent systemic therapy. | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Phase number | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Phase label | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Treatment site (coded anatomical, R) | text | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Laterality (R) | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Phase intent | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Phase sequence (concurrent with / following phase n) | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Modality | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Technique | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Energy | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Total dose for phase | number | Yes | No | Gy |
| SCR-RO-003 | C.15 Radiation Oncology | field | Number of fractions (integer, R) | number | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Dose per fraction (CALC-175 = total dose ÷ fractions, displayed to configured precision; or the RO may enter dose/fraction and fractions, with tota… | readonly | No | Yes | Gy |
| SCR-RO-003 | C.15 Radiation Oncology | field | Fractions per day (integer, default 1) | number | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Inter-fraction interval | number | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Treatment days per week | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Planned schedule pattern | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Planned start date | date | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Planned end date | date | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Prescription point / normalisation | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Dose specification convention noted. | number | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Volume type | select | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | Volume label | number | Yes | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | Anatomical description | textarea | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Derived-from | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Margin specification | number | No | No | mm |
| SCR-RO-003 | C.15 Radiation Oncology | field | Prescribed dose to this volume | number | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | Coverage objective (e.g. "≥ x% of volume receives ≥ y% of prescribed dose" — structured: metric, operator, value, unit) | number | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | Priority. RO-040 — target volume names are structured and must match the structure set names used in planning | select | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | free-text-only volume naming is prohibited because it breaks automated concordance checking. | number | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | OAR name (coded from OAR Master , R) | text | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Laterality | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Constraint (repeating per OAR): constraint type/ Volume receiving a dose (Vx Gy) / Dose to a volume in cc (Dxcc) / Other), metric parameter, operat… | select | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | Patient position | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Arm position | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Head position | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Immobilisation deviceswith device ID and index positions | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Bolus required (Y/N; material, thickness in mm, location, frequency — every fraction / alternate / specified) | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Skin marks/tattoos (description) | textarea | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Motion managementwith parameters | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Bladder/bowel/stomach preparation protocol | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Special positioning notes. | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | IGRT modality | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Frequency | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Matching structures | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Action levels/tolerances | select | Yes | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Imaging dose consideration | number | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Who may approve an out-of-tolerance match (role). | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Concurrent systemic therapy (Y/N; regimen link; timing relative to fractions; coordinating MO) | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Other concurrent modality | select | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Sequencing constraints. | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Instructions to simulation | textarea | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | to planning/dosimetry | textarea | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | to physics | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | to RTT | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | to nursing (skin care, supportive medication) | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | contraindications and cautions | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | supportive medications prescribed for the course. | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Total course dose (sum across phases where volumes overlap — the screen must state whether phases are additive to the same volume or to different v… | select | No | No | mL |
| SCR-RO-003 | C.15 Radiation Oncology | field | Total fractions | number | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Overall treatment time in days | number | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | EQD2/BED where CCA configures the capability (CALC-176, inputs, formula and α/β displayed). | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | Dose per fraction or total dose (whichever is derived) | readonly | No | Yes | Gy |
| SCR-RO-003 | C.15 Radiation Oncology | field | planned end date | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | total course dose | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | total fractions | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | overall treatment time | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | EQD2/BED where configured | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | field | consistency checks (see alerts). | readonly | No | Yes |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:Phases | Entry | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:Phases | Date / time | datetime-local | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:Phases | Source / owner | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:target volumes per phase | Entry | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:target volumes per phase | Date / time | datetime-local | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:target volumes per phase | Source / owner | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:OAR constraint table (OAR, constraint type, parameter, operator, value, unit, class, source, prior-dose adjustment) | Entry | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:OAR constraint table (OAR, constraint type, parameter, operator, value, unit, class, source, prior-dose adjustment) | Date / time | datetime-local | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:OAR constraint table (OAR, constraint type, parameter, operator, value, unit, class, source, prior-dose adjustment) | Source / owner | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:immobilisation devices | Entry | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:immobilisation devices | Date / time | datetime-local | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:immobilisation devices | Source / owner | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:version history. | Entry | text | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:version history. | Date / time | datetime-local | No | No |  |
| SCR-RO-003 | C.15 Radiation Oncology | table:version history. | Source / owner | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Requested by | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | requested date | date | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | urgency | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | target simulation date | date | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | scan protocol required | select | Yes | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Additional imaging for fusion required (MR, PET — with modality, protocol, whether same-position acquisition needed) | select | Yes | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | special requirements (sedation, anaesthesia, interpreter, mobility, isolation) | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | pre-simulation preparation (bladder filling, bowel preparation, fasting, oral contrast timing). | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Identity verified (two identifiers, method) | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Pregnancy check performed where applicable | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Prior RT confirmed | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | CIED confirmed and plan noted | textarea | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Allergy check for contrast | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Renal function for contrast | date | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Consent status | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Preparation instructions followed (Y/N + detail) | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Patient able to maintain position for the required duration (Y/N + notes). | select | Yes | No | min |
| SCR-RO-004 | C.15 Radiation Oncology | field | Position (as prescribed — confirm or record deviation with reason) | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Arm/head position | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Immobilisation devices used with device ID and index/serial positions (repeating: device type, ID, index values per axis, notes) — RO-090 : device … | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Headrest type and index | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Vac-bag ID | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Mask ID and fixation points | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Knee/ankle fix index | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Wing board index | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Bolus applied at simulation (Y/N, spec) | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Positioning aids | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Comfort measures | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Position tolerance assessment. | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Scanner/unit | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Protocol used | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Scan date/time | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Slice thickness (mm) | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Scan extent (superior and inferior anatomical limits) | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Field of view | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | D acquisition (Y/N, phases, respiratory trace quality) | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Breath-hold (type, achieved duration, reproducibility) | select | No | No | min |
| SCR-RO-004 | C.15 Radiation Oncology | field | Number of scans acquired | number | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Additional datasets acquired for fusion | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Images transferred to TPS (Y/N, timestamp) | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Acquisition performed by | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | RO present (Y/N). | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Reference/setup point definition (anatomical description) | textarea | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Marks appliedwith count and locations | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Coordinates of reference point relative to the scan origin (x, y, z in mm) | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Shift from reference to planned isocentre (to be completed at planning, or recorded here if isocentre set at simulation) | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Photographs of setup (with consent ) | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Setup description narrative. | textarea | Yes | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Agent, volume, route, rate, timing, administered by, lot/expiry, adverse reaction (Y/N, link to reaction record). | select | No | No | mL |
| SCR-RO-004 | C.15 Radiation Oncology | field | Type, number, insertion date, inserting clinician, location, imaging confirmation. | date | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Deviation from prescribed position or immobilisation (Y/N + description + reason + RO notified) | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Patient tolerance issues | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Repeat scan required (Y/N + reason) | select | Yes | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Additional dose from repeat imaging. | number | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Simulation acceptable for planning (Y/N — RO or delegated) | select | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Approved by | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Approved at | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Notes to planning. | textarea | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | Time in position | readonly | No | Yes |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | scan extent length | readonly | No | Yes |  |
| SCR-RO-004 | C.15 Radiation Oncology | field | interval from prescription to simulation . | readonly | No | Yes |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:Immobilisation device table (type, ID, index values, notes) | Entry | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:Immobilisation device table (type, ID, index values, notes) | Date / time | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:Immobilisation device table (type, ID, index values, notes) | Source / owner | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:datasets acquired (type, date, purpose, transferred) | Entry | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:datasets acquired (type, date, purpose, transferred) | Date / time | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:datasets acquired (type, date, purpose, transferred) | Source / owner | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:reference marks. | Entry | text | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:reference marks. | Date / time | datetime-local | No | No |  |
| SCR-RO-004 | C.15 Radiation Oncology | table:reference marks. | Source / owner | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | Structure set version | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | source simulation dataset | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | fusion registrations used (repeating: secondary dataset, registration method, rigid/deformable, quality assessment, approved by) | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | Required-structure completeness against the prescription and the site template | text | Yes | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | Missing structures listed | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | Peer review performed (Y/N per rules by technique/site), reviewer, findings, changes made | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | RO approval statement | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | Notes to planning. | textarea | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | Completeness against required set | readonly | Yes | Yes |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | structure count | readonly | No | Yes |  |
| SCR-RO-005 | C.15 Radiation Oncology | field | total target volume | readonly | No | Yes | mL |
| SCR-RO-005 | C.15 Radiation Oncology | field | days from simulation to contour approval . | readonly | No | Yes |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Structure name (must match the prescription's declared volume names, RO-040) | number | No | No | mL |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Structure type (GTV / CTV / ITV / PTV / OAR / PRV / Support / Bolus / Avoidance / Other) | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Phase applicability | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Laterality | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Volume (cc) | number | No | No | mL |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Drawn by | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Drawn on | date | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Derived-from and margin (for expanded volumes) | readonly | No | Yes | mL |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Imaging used (primary dataset + fused datasets with fusion method and quality assessment) | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Auto-segmented | readonly | No | Yes |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Reviewed by | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Review outcome (Accepted / Edited / Rejected) | select | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Approved by | text | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Approved at | datetime-local | No | No |  |
| SCR-RO-005 | C.15 Radiation Oncology | table:Table — structure register (exact columns) | Status (Draft / Complete / Approved / Superseded). | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Plan ID and version | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Prescription version used (R, read-only link) | readonly | Yes | Yes |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Structure set version used (R) | text | Yes | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Simulation dataset used | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | TPS name and version | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Dose calculation algorithm and version | number | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Dose grid resolution (mm) | number | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Heterogeneity correction (Y/N) | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Planner | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Plan created date | date | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Plan status. | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Repeating per beam/arc: beam ID, modality, energy, technique, gantry angle or arc range, collimator angle, couch angle, isocentre coordinates (x, y… | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | number of beams/arcs | number | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | estimated delivery time . | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Conformity index, homogeneity index, gradient index where used — each with the definition/formula applied, since these indices have multiple defini… | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Global maximum dose and its location | number | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Hot spots outside target | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Integral dose where reported. | number | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Planner narrative describing compromises made | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Alternative plans generated and why rejected | number | No | No | mL/h |
| SCR-RO-006 | C.15 Radiation Oncology | field | Constraints prioritised | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Known limitations | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Deliverability concerns | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Notes to physics | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Notes to RTT. | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | For multi-phase courses: composite plan constructed (Y/N), method, phases included, summed dose to each OAR , summed target coverage. RO-140 — wher… | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | Objective/constraint met flags | readonly | No | Yes |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | deviations | readonly | No | Yes |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | total MU | readonly | No | Yes |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | estimated delivery time | readonly | No | Yes |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | plan sum values | readonly | No | Yes |  |
| SCR-RO-006 | C.15 Radiation Oncology | field | days from contour approval to plan submission . | readonly | No | Yes | kg/m² |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Structure | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Objective type | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Metric | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Prescribed/required value | text | Yes | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Operator | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Achieved value | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Unit | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Met (Y/N) | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Deviation | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Acceptable variation applied | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — dose objectives vs achieved (exact columns) | Comment. | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | OAR | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Constraint (type, parameter, operator, value, unit) | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Constraint class (hard/optimal/acceptable) | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Source protocol | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Achieved value | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Met (Y/N) | select | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Deviation | text | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Clinical justification where exceeded (narrative — authored by the RO, not the planner, RO-120 ) | textarea | No | No |  |
| SCR-RO-006 | C.15 Radiation Oncology | table:Table — OAR constraints vs achieved | Prior-dose adjustment applied. | number | No | No |  |
| SCR-RO-007 | C.15 Radiation Oncology | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RO-007 | C.15 Radiation Oncology | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RO-008 | C.15 Radiation Oncology | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RO-008 | C.15 Radiation Oncology | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Fractions delivered with dates | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | fractions missed with dates and reasons | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | cumulative delivered dose per phase and total (CALC-171) | select | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | dose remaining | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | treatment days elapsed vs planned | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | gap days (CALC-172) | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | projected completion date (CALC-173) | date | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | compensation required for gaps per rules with the rule named. | text | Yes | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Auto-generated: fractions delivered since last OTV, setup deviations, out-of-tolerance images, interruptions, concurrent chemo administered, unsche… | readonly | No | Yes | mL/h |
| SCR-RO-009 | C.15 Radiation Oncology | field | Site-specific acute toxicity set (e.g. for head and neck: mucositis, dysphagia, dysgeusia, xerostomia, dermatitis, pain, weight loss, aspiration; f… | select | No | No | kg |
| SCR-RO-009 | C.15 Radiation Oncology | field | general symptoms | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | pain score and analgesia | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | skin assessment with photograph where captured | textarea | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | each entry writes to the longitudinal toxicity record. | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Site examination | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | performance status | select | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | weight (R at OTV ) with cumulative weight change from baseline and % (CALC-177) — with a configured threshold triggering nutrition referral and a r… | datetime-local | Yes | No | kg |
| SCR-RO-009 | C.15 Radiation Oncology | field | nutrition status | select | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | hydration. | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Number of out-of-tolerance matches since last OTV | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | systematic shift trend per axis | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | RTT concerns raised | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | re-simulation or re-planning indicated (Y/N + reason). | select | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Medications prescribed/changed | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | skin care | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | nutrition support | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | analgesia | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | antiemetics | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | referrals (dietitian, speech and language, psycho-oncology, dental) | number | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | admission required. | text | Yes | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Decision/ Re-simulate and re-plan / Discontinue — with reason / Complete early as planned) | select | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Rationale | textarea | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Next OTV date | date | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Instructions to RTT | textarea | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Instructions to nursing. | textarea | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | Cumulative dose | readonly | No | Yes |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | % complete | readonly | No | Yes |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | elapsed and gap days | readonly | No | Yes |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | projected completion | readonly | No | Yes |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | weight change | readonly | No | Yes | kg |
| SCR-RO-009 | C.15 Radiation Oncology | field | toxicity grade trajectory | readonly | No | Yes |  |
| SCR-RO-009 | C.15 Radiation Oncology | field | number of out-of-tolerance matches. | readonly | No | Yes |  |
| SCR-RO-009 | C.15 Radiation Oncology | table:toxicity grades over time (matrix | Entry | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | table:toxicity grades over time (matrix | Date / time | datetime-local | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | table:toxicity grades over time (matrix | Source / owner | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | table:weight trend. | Entry | text | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | table:weight trend. | Date / time | datetime-local | No | No |  |
| SCR-RO-009 | C.15 Radiation Oncology | table:weight trend. | Source / owner | text | No | No |  |
| SCR-RO-010 | C.15 Radiation Oncology | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RO-010 | C.15 Radiation Oncology | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RO-011 | C.15 Radiation Oncology | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RO-011 | C.15 Radiation Oncology | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RO-012 | C.15 Radiation Oncology | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RO-012 | C.15 Radiation Oncology | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-002 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-002 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-003 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-003 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-004 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-004 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-005 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-005 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-006 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-006 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-007 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-007 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-008 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-008 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-PHY-010 | C.16 Radiation Physics | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-PHY-010 | C.16 Radiation Physics | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-001 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-001 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-002 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-002 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-003 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-003 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-004 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-004 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-005 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-005 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-006 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-006 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-007 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-007 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-RTT-008 | C.17 Radiation Therapy Delivery | field | Structured clinical / operational findings | textarea | No | No |  |
| SCR-RTT-008 | C.17 Radiation Therapy Delivery | field | Assessment / decision / outcome | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | Pathway state (CALC-200) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | days in state | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | interval since neoadjuvant completion (CALC-191) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | post-operative day (CALC-190) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | days pathology outstanding (CALC-196) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | days since pathology report to handoff (CALC-197) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | adjuvant-handoff target countdown (CALC-202). | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | field | Pathway state, planned procedure category, site, intent, surgeon, neoadjuvant status, target-interval breach, complication present, pathology statu… | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Patient name | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | UHID | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Age/Sex | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Primary site & histology | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Stage — cTNM and pTNM distinguished (GEN-CMP-001) | number | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Treatment intent | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Planned procedure | textarea | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Site & laterality (high visual prominence) | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Neoadjuvant status (None / In progress / Completed interval since completion) | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Pathway state chip — Consulted → Plan signed → Pre-op workup ordered → Workup complete → Anaesthesia cleared → Consent obtained → Scheduled → Pre-o… | number | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Days in current state with target-interval colouring | number | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Blocking item (named, with owning role) | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Plan version | textarea | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Scheduled date from SCR-SO-006 | date | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Anaesthesia fitness status (read-only import) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Consent status | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Blood availability status (read-only import) | readonly | No | Yes |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Post-op day (CALC-190, where applicable) | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Complication flag (max grade, colour-banded ) | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Pathology status (Awaited / Received / Reported / Addendum) | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | pStage vs cStage concordance | number | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Adjuvant handoff status | select | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Assigned surgeon(s) | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Alerts icon stack | text | No | No |  |
| SCR-SO-001 | C.18 Surgical Oncology | table:Table columns — Pathway Board (exact) | Row actions. | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Referring clinician/service | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Referral date | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Referral question | textarea | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Urgency. | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Auto-assembled timelineshared with SCR-MO-002 chronology object — not re-typed (MO-CON-060 pattern). | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Repeating: regimen, cycles received, completion date, best response (link to SCR-RSP-001), toxicities, dose modifications, reason for stopping | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Interval since completion of last cycle (CALC-191) — displayed prominently because it governs the surgical-window discussion. | textarea | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Site, dose, fractionation, dates, technique, facility, overlap with the planned surgical field— SO-021 : a surgical plan proposing an incision thro… | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Repeating: procedure, date, approach, findings, complications, adhesion risk, facility, operative note link where internal. | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Auto from SCR-DX-004 (read-only) with clinician confirmation | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | sites of disease | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | resectability-relevant metastatic status. | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Repeating: accession, date, diagnosis, grade, biomarkers, reviewed personally (Y/N) — SO-022 : the surgeon must affirmatively record having persona… | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Repeating: study, date, modality, key findings relevant to resectability (extent, vascular involvement, nodal disease, distant disease), viewer lin… | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Repeating complaint, duration, severity, progression — shared structure with SCR-MO-002. | select | No | No | min |
| SCR-SO-002 | C.18 Surgical Oncology | field | Instrument, score, assessed by, date (distinct field from nurse-assessed PS per MO-CON convention). | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | General | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | systemic examination by system | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | site-specific tumour examination — measurable lesion size(s) with method and units, mobility/fixation to adjacent structures, nodal stations examin… | select | No | No | mm |
| SCR-SO-002 | C.18 Surgical Oncology | field | Coded problem list (shared GEN-LNG-003), auto-supplemented, with a surgical-relevance flag per problem (cardiac, pulmonary, renal, hepatic, diabete… | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Full medication list (shared GEN-LNG-002) with the anticoagulant/antiplatelet sub-flag surfaced as its own reviewed panel here (not buried) — drug,… | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Shared GEN-LNG-001, including latex allergy (surgically material) as a discrete, always-visible item. | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Screening tool result , weight trend, albumin where available, dysphagia/intake concerns, referral to Dietitian (Y/N). | select | No | No | kg |
| SCR-SO-002 | C.18 Surgical Oncology | field | Prior anaesthesia complications (patient-reported/record) | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | airway concerns known to date | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | explicit statement that full fitness assessment is owned by Anaesthesia and not concluded here (SO-006). | textarea | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Resectability assessment | select | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Operability assessment | select | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Basis (narrative, R) | textarea | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | SO-024 : resectability (disease-based) and operability (patient-based) are captured as two distinct fields and must never be collapsed into one "fi… | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Dropdown (product-defined): Curative — primary / Cytoreductive / Diagnostic (biopsy/staging only) / Palliative — symptom control / Prophylactic / R… | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Proposed procedure (coded from Procedure Master , R) | text | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Anatomical site | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Laterality (R) | select | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Approach | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Alternatives considered (repeating: alternative, why not chosen) | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Non-operative alternative discussed (Y/N + detail, R — including "no treatment"). | select | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Expected oncological benefit (narrative) | textarea | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Expected functional outcome | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Risks discussed | multiselect | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | general surgical risks (bleeding, infection, VTE, anaesthetic risk, adjacent organ injury) and procedure-specific risks . | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Reconstruction anticipated (Y/N) | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | type anticipated | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | reconstructive surgeon involvement required (Y/N + referral). | select | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Planned nodal approachspecified / Both, staged) | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | rationale. | textarea | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Fertility-preservation discussionfor the configured age band — shares the MO-CON-030 discrete-field requirement | date | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | anticipated functional loss (e.g. continence, speech, limb function) discussed (Y/N + detail) | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | stoma possibility discussed (Y/N — feeds SO-025). | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Discussed at MDT already (Y/N, link) | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | MDT discussion required before proceeding (Y/N + reason) | select | Yes | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | SO-026 : where institutional pathway rules require MDT discussion before a given procedure category , the plan cannot be signed without either the … | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Topics covered | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | attendees | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | interpreter | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | materials issued (version) | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | patient understanding. | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Dropdown (product-defined): Agreed to proceed / Agreed with modification / Wants second opinion / Declines surgery / Deferred. | select | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Launches SCR-INV-001 | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | referrals (Anaesthesia pre-assessment, Cardiology, Pulmonology, Dietitian, Stoma nurse, Reconstructive surgery, Genetics, Fertility). | textarea | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Recommendation | textarea | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Target timing. | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | Age | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | BMI | readonly | No | Yes | kg/m² |
| SCR-SO-002 | C.18 Surgical Oncology | field | interval since neoadjuvant completion (CALC-191) | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | interval since prior surgery/RT (CALC-062/analogue) | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | field | PS trend. | readonly | No | Yes |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:Chronology | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:Chronology | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:Chronology | Source / owner | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:prior treatments per modality | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:prior treatments per modality | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:prior treatments per modality | Source / owner | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:comorbidities | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:comorbidities | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:comorbidities | Source / owner | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:medications with anticoagulant sub-table | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:medications with anticoagulant sub-table | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:medications with anticoagulant sub-table | Source / owner | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:pathology reviewed | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:pathology reviewed | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:pathology reviewed | Source / owner | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:imaging reviewed | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:imaging reviewed | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:imaging reviewed | Source / owner | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:investigations/referrals raised. | Entry | text | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:investigations/referrals raised. | Date / time | datetime-local | No | No |  |
| SCR-SO-002 | C.18 Surgical Oncology | table:investigations/referrals raised. | Source / owner | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Site, laterality, histology, grade, cTNM, pTNM where already available, biomarkers, disease status, line of therapy, neoadjuvant status and complet… | date | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Surgical intent (from consultation, confirmable) | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Priority | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Priority reason (R when not Elective — routine). | select | Yes | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Procedure (coded from Procedure Master , R) | text | Yes | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Procedure short name | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Anatomical site (coded, R) | text | Yes | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Laterality (R, product-defined value set: Left / Right / Bilateral / Midline / Not applicable) | select | Yes | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Proposed extent | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Second/staged procedure (Y/N, with the relationship to this plan specified — e.g. "Stage 1 of 2"). | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Approach | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Planned conversion threshold/criteria (narrative, optional) | textarea | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Estimated duration | number | No | No | min |
| SCR-SO-003 | C.18 Surgical Oncology | field | Estimated blood loss category (for resource planning, distinct from the actual intra-operative value recorded later). | select | No | No | mL |
| SCR-SO-003 | C.18 Surgical Oncology | field | Planned nodal approach (None / Sentinel node biopsy / Regional lymphadenectomy — level(s) / Both — staged) | number | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Node stations planned. | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Reconstruction planned (Y/N) | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Type | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Reconstruction surgeon (named, distinct from primary surgeon where a joint case) | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Timing (Immediate / Delayed — with planned interval). | textarea | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Joint procedure (Y/N) | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Other surgical specialties involvedwith named surgeon per specialty and their role in the case. | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Expected date | date | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Post-neoadjuvant minimum interval check (CALC-191 compared against minimum, with override + reason where violated — SO-030 ) | textarea | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Target interval from decision to surgery with countdown . | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Auto-assembled required set from Procedure Master + anaesthesia-driven standard set , each launchable to SCR-INV-001, with status . | readonly | Yes | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Anticipated anaesthesia type | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Anaesthesia referral raised | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Blood product requirement | select | Yes | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | rationale where crossmatch requested. | textarea | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Anticipated post-op level of care | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | bed request raised. | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Repeating: item category (Mesh / Prosthesis / Expander / Fiducial marker / Energy device / Robotic platform / Other), specific item where known, av… | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Frozen section anticipated (Y/N) | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Anticipated question (e.g. margin assessment, nodal status) | select | No | No | mm |
| SCR-SO-003 | C.18 Surgical Oncology | field | Specimen handling/orientation instructions to pathology. | textarea | Yes | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Stoma possible (Y/N) | select | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | If yes — stoma-site marking required pre-operatively. | readonly | Yes | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Required consent type(s)with status per consent (from SCR-SO-005). | readonly | Yes | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | Interval since neoadjuvant completion (CALC-191) | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | target-interval countdowns | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | field | pre-op investigation completeness . | readonly | No | Yes |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:Multidisciplinary involvement (specialty, surgeon, role) | Entry | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:Multidisciplinary involvement (specialty, surgeon, role) | Date / time | datetime-local | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:Multidisciplinary involvement (specialty, surgeon, role) | Source / owner | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:pre-op investigations required with status | Entry | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:pre-op investigations required with status | Date / time | datetime-local | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:pre-op investigations required with status | Source / owner | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:implants/equipment requested with availability | Entry | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:implants/equipment requested with availability | Date / time | datetime-local | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:implants/equipment requested with availability | Source / owner | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:version history. | Entry | text | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:version history. | Date / time | datetime-local | No | No |  |
| SCR-SO-003 | C.18 Surgical Oncology | table:version history. | Source / owner | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Since the surgical consultation/plan: new symptoms, weight change, functional status change, new results, any change to disease status. | readonly | No | Yes | kg |
| SCR-SO-004 | C.18 Surgical Oncology | field | Auto-linked with dates | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | flag if imaging predates the operation by more than a configured validity window (staleness per GEN-DSP-003). | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | cTNM (and pTNM if already available) read-only from SCR-DX-002. | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Regimen, cycles, completion date, interval since completion (CALC-191, re-displayed here as the safety-critical figure it is), best response, ongoi… | date | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Active toxicities relevant to surgical fitness (e.g. neutropenia, thrombocytopenia, cardiotoxicity, wound-healing-relevant agents such as anti-angi… | number | Yes | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Shared lists, surgically-relevant flags surfaced | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | full medication reconciliation status. | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Drug | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | last dose date/time | datetime-local | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | bridging plan | select | Yes | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | planned stop date | date | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | planned restart date and criteria (R — SO-041 : an anticoagulation plan without both a stop and a restart plan is incomplete and blocks readiness). | date | Yes | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Shared GEN-LNG-001, latex status explicit. | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Full blood count, coagulation profile, renal function, liver function, electrolytes, group & save/crossmatch result — each value, unit, date, flag,… | date | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Blood group | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | antibody screen result | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | crossmatch status | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | units held | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | expiry of crossmatch validity . | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | ASA grade or equivalent | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | fitness decision (Fit / Fit with optimisation / Not fit) | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | required optimisation and re-review date where applicable | date | Yes | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | airway assessment summary | textarea | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | anaesthetic plan reference. SO-006 applies: this panel is never editable from Surgical Oncology. | textarea | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | ECG, echocardiogram/LVEF, pulmonary function test results where ordered, each with date and read-only source. | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Screening score, weight trend, albumin, Dietitian input where referred. | number | No | No | kg |
| SCR-SO-004 | C.18 Surgical Oncology | field | Active infection screen | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | MRSA/other colonisation status | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | temperature trend. | number | No | No | °C |
| SCR-SO-004 | C.18 Surgical Oncology | field | Status, test result, test date, where applicable by sex/age. | date | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Read-only chip from SCR-SO-005 with link. | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Explicit affirmative re-confirmation action, distinct from the plan's original entry (SO-002). | textarea | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Instruction issued (Y/N), fasting window , patient confirmed understanding. | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Mechanical (Y/N + device), pharmacological (agent, dose, timing) for the actual protocol content | select | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | the *field structure* is . | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Agent, dose, timing relative to incision . | number | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Read-only from Stoma Nurse record | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | marked (Y/N), site, marked by, date. | date | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | roll-up of the Blood Bank panel into a single readiness chip. | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Read-only roll-up from SCR-SO-003 implant/equipment requests, availability status. | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Dropdown: Ready for theatre / Ready with conditions (named) / Not ready — optimisation required/ Cancel/postpone (with reason). | date | Yes | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | Interval since neoadjuvant completion | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | washout-interval compliance (SO-040) | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | staleness of every imported value against configured windows | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | field | overall readiness completeness gauge . | readonly | No | Yes |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:Laboratory results | Entry | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:Laboratory results | Date / time | datetime-local | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:Laboratory results | Source / owner | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:medication reconciliation | Entry | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:medication reconciliation | Date / time | datetime-local | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:medication reconciliation | Source / owner | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:anticoagulation timeline | Entry | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:anticoagulation timeline | Date / time | datetime-local | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:anticoagulation timeline | Source / owner | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:pre-op investigation status. | Entry | text | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:pre-op investigation status. | Date / time | datetime-local | No | No |  |
| SCR-SO-004 | C.18 Surgical Oncology | table:pre-op investigation status. | Source / owner | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Consent type | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Template + version | readonly | No | Yes |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Procedure/Surgical Plan version consented to | readonly | No | Yes |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Site & laterality | readonly | No | Yes |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Planned extent as stated to patient. | readonly | No | Yes |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Checklist from template , each individually acknowledged: general surgical risks (bleeding requiring transfusion, infection, VTE, anaesthetic risk,… | multiselect | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | each item: discussed (Y/N), specific detail given. | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Expected benefit | readonly | No | Yes |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Alternatives discussed including no treatment (R) | text | Yes | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Alternative treatment modalities discussed (checklist: non-operative management, different extent, different approach). | multiselect | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Reconstruction consent sub-item (where applicable) — type, risks specific to reconstruction, alternative reconstruction options declined | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Nodal procedure consent sub-item — risks (lymphoedema etc. ) | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Possibility of stoma — explicit consent item where the plan flags stoma possibility (Y/N, discussed, patient understanding) — SO-043 : consent for … | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Consent to blood product administration if required (Y/N) | select | Yes | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | alternatives to transfusion discussed where relevant (e.g. cell salvage ) | number | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | specific objection recorded (e.g. on religious grounds) with the resulting clinical plan cross-referenced to SCR-SO-003. | textarea | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Read-only status chip confirming Anaesthesia's own consent (owned by Anaesthetist, B.21.8) is separately obtained — not duplicated here (SO-006), o… | readonly | No | Yes | mL/h |
| SCR-SO-005 | C.18 Surgical Oncology | field | Capacity assessed (Y/N, assessor, basis) | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Consent given by (Patient / Legal representative — relationship + authority basis) | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Emergency consent exception invoked (Y/N + two-clinician justification where used ). | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Interpreter used (Y/N, name/service, language) | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Information material issued (version) | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Questions answered (Y/N + summary). | select | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Distinct, timestamped, explicit affirmative action separate from the auto-populated display (SO-002) — this is the second of the five reconfirmatio… | readonly | No | Yes | mL/h |
| SCR-SO-005 | C.18 Surgical Oncology | field | Patient/representative signature (capture) | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Clinician name/signature | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Witness (conditional per ) | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Date/time | datetime-local | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Validity period . | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | field | Withdrawal date, reason, recorded by — a new event, never a deletion (REG-FD-090 pattern). | date | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:Risk acknowledgement checklist | Entry | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:Risk acknowledgement checklist | Date / time | datetime-local | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:Risk acknowledgement checklist | Source / owner | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:consent version history | Entry | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:consent version history | Date / time | datetime-local | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:consent version history | Source / owner | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:linked Surgical Plan version history. | Entry | text | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:linked Surgical Plan version history. | Date / time | datetime-local | No | No |  |
| SCR-SO-005 | C.18 Surgical Oncology | table:linked Surgical Plan version history. | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Patient (R) | text | Yes | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Surgical Plan version | readonly | Yes | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Planned procedure, site, laterality | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Priority (from plan) | select | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Requested date/date range | date | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Estimated duration (from plan, editable with reason) | number | No | No | min |
| SCR-SO-006 | C.18 Surgical Oncology | field | Theatre | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Order in list (sequence) | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Anaesthesia type (from plan) | select | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Special equipment/implants | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Blood product hold status | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Consent status | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Fasting instruction issued | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Pre-op checklist status . | select | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | Ready-for-theatre aggregate chip (CALC-201) | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | list total time vs theatre session length | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | days waiting | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | field | interval-since-neoadjuvant compliance flag (CALC-191 vs minimum). | readonly | No | Yes |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Operating list — exact columns | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Operating list — exact columns | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Operating list — exact columns | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Time (estimated) | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Time (estimated) | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Time (estimated) | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Patient | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Patient | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Patient | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:UHID | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:UHID | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:UHID | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Age/Sex | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Age/Sex | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Age/Sex | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Planned procedure | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Planned procedure | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Planned procedure | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Site & laterality (high prominence) | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Site & laterality (high prominence) | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Site & laterality (high prominence) | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Approach | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Approach | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Approach | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Estimated duration | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Estimated duration | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Estimated duration | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Surgeon(s) | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Surgeon(s) | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Surgeon(s) | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthetist assigned | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthetist assigned | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthetist assigned | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthesia type | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthesia type | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthesia type | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Blood requirement & availability status | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Blood requirement & availability status | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Blood requirement & availability status | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Implant/equipment requirement & availability | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Implant/equipment requirement & availability | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Implant/equipment requirement & availability | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Frozen-section requirement flag | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Frozen-section requirement flag | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Frozen-section requirement flag | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Special equipment | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Special equipment | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Special equipment | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Consent status | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Consent status | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Consent status | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Fasting status | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Fasting status | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Fasting status | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthesia fitness status | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthesia fitness status | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Anaesthesia fitness status | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Pre-op checklist status | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Pre-op checklist status | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Pre-op checklist status | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:"Ready for theatre" chip (SO-046 , aggregating every gate) | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:"Ready for theatre" chip (SO-046 , aggregating every gate) | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:"Ready for theatre" chip (SO-046 , aggregating every gate) | Source / owner | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Row actions. Waitlist — patient, requested procedure, priority, requested-by date, days waiting . | Entry | text | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Row actions. Waitlist — patient, requested procedure, priority, requested-by date, days waiting . | Date / time | datetime-local | No | No |  |
| SCR-SO-006 | C.18 Surgical Oncology | table:Row actions. Waitlist — patient, requested procedure, priority, requested-by date, days waiting . | Source / owner | text | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Interval history since pre-op workup | readonly | No | Yes |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Focused examination relevant to the planned procedure and to anaesthesia | textarea | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Vitals and weight today (imported, with delta from workup) | readonly | No | Yes | kg |
| SCR-SO-007 | C.18 Surgical Oncology | field | Fasting confirmed (time last ate/drank, R) | datetime-local | Yes | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Bowel/bladder preparation confirmed where the procedure requires it | text | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Site/laterality reconfirmation (explicit affirmative action, R — checkpoint 3 of 5) | select | Yes | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Consent reconfirmed present and unaltered since capture | text | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Anticoagulant last-dose status re-checked against the bridging plan | select | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Outstanding results check (any pending investigation that could change the decision — SO-047 : a critical result received after workup but before s… | select | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Final fitness confirmation. | select | No | No |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | Time since last fasting intake | readonly | No | Yes |  |
| SCR-SO-007 | C.18 Surgical Oncology | field | interval since workup. | readonly | No | Yes |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Identity confirmed (patient states name/DOB or two-identifier method, R) | select | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Site and laterality confirmed by the patient/representative where possible and marked on the patient (R — hard stop if unmarked where marking is re… | select | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Consent confirmed present and correct | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Anaesthesia safety check completed (owned by Anaesthetist — read-only reference here, SO-006) | readonly | No | Yes |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Allergy status confirmed | select | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Difficult airway/aspiration risk assessed (owned by Anaesthetist) | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Blood loss risk assessed and blood availability confirmed where required | text | Yes | No | mL |
| SCR-SO-008 | C.18 Surgical Oncology | field | Pulse oximeter functioning and on patient. Each item: confirmed by (role), time. | number | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | All team members introduce themselves by name and role (R, team roster confirmed) | text | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Surgeon, Anaesthetist and Nurse verbally confirm patient identity, site, laterality and procedure (R, each role individually attests — SO-048 : Tim… | datetime-local | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Anticipated critical events reviewed (surgeon: critical/unexpected steps, operative duration, anticipated blood loss; anaesthetist: patient-specifi… | number | No | No | mL |
| SCR-SO-008 | C.18 Surgical Oncology | field | Antibiotic prophylaxis given within the required window confirmed (Y/N + time, window check against ) | select | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Essential imaging displayed (Y/N, where relevant) | select | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | VTE prophylaxis confirmed. Each item: confirmed by (role), time. | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Procedure performed recorded (name of procedure actually done — first capture of the actual procedure, feeding the Operative Note, SO-001) | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Instrument, sponge/swab and needle counts confirmed correct or discrepancy resolution recorded (R — SO-010, SO-049 : a Sign-Out cannot close with a… | number | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Specimen labelling confirmed (specimen name matched to patient, matched to orientation instructions, R) | textarea | Yes | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Equipment problems to be addressed identified | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Key concerns for recovery and management reviewed by surgeon, anaesthetist and nurse. Each item: confirmed by (role), time. | number | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | Antibiotic-timing compliance | readonly | No | Yes |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | phase completion percentage | readonly | No | Yes |  |
| SCR-SO-008 | C.18 Surgical Oncology | field | time between phases. | readonly | No | Yes |  |
| SCR-SO-008 | C.18 Surgical Oncology | table:Team roster (name, role, arrival/departure time — mirrors MDT attendance pattern MDT-040) | Entry | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | table:Team roster (name, role, arrival/departure time — mirrors MDT attendance pattern MDT-040) | Date / time | datetime-local | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | table:Team roster (name, role, arrival/departure time — mirrors MDT attendance pattern MDT-040) | Source / owner | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | table:count record (item type, count 1, count 2, match Y/N, discrepancy action). | Entry | text | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | table:count record (item type, count 1, count 2, match Y/N, discrepancy action). | Date / time | datetime-local | No | No |  |
| SCR-SO-008 | C.18 Surgical Oncology | table:count record (item type, count 1, count 2, match Y/N, discrepancy action). | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Primary surgeon | readonly | Yes | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Assistant surgeon(s) (repeating, with role: First assistant / Second assistant / Trainee — operating / Trainee — assisting, R per assistant) | text | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Anaesthetist | readonly | Yes | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Scrub nurse | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Circulating nurse | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Other specialists presentwith role. SO-052 : trainee operating role is a distinct, auditable field (not inferred from "assistant"), because supervi… | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Anaesthesia type | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | airway management summary | number | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | major intra-operative anaesthetic events — sourced from the Anaesthetist's own Intra-operative Anaesthetic Record (B.21.8), displayed read-only her… | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | link to the full anaesthetic record. | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Patient position | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Positioning aids used | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Skin preparation agent | number | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Draping method | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Prophylactic antibiotics | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | VTE prophylaxis applied in theatre (mechanical device confirmed in use) | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Active warming device used (Y/N + type) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Pressure-area protection devices | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Urinary catheter inserted (Y/N, type, time). | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Approach actually used (Open / Laparoscopic / Robotic / Thoracoscopic / Hybrid / Other) displayed against the planned approach (GEN-CMP-001) | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Conversion (Y/N — R) | select | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | where Y: reason for conversionand conversion timestamp. | datetime-local | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Incision type/location | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Incision length where relevant | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Access technique (for laparoscopic/robotic: port placement — repeating: port number, size, location, instrument). | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Tumour location (confirmed vs pre-op imaging, concordant Y/N) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Tumour extent as visualised | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Local invasion | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Metastatic disease found intra-operatively (Y/N — repeating: site, appearance, biopsied Y/N) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Adhesions (none/mild/moderate/dense, location) | select | No | No | mL/h |
| SCR-SO-009 | C.18 Surgical Oncology | field | Nodal findings (stations visualised, appearance, palpable disease) | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Adjacent structures — status of each structure at risk for the procedure (preserved / involved / sacrificed, per structure, list scoped to procedure) | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Unexpected findings. | textarea | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Structured ordered key-steps list (repeating: step number, step name from a procedure-specific step template , narrative detail, structures identif… | number | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Extent of resection achieved | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Completeness of resection as assessed intra-operatively— distinct from, and not to be confused with, the pathological margin status determined late… | select | No | No | mm |
| SCR-SO-009 | C.18 Surgical Oncology | field | Margins — surgeon's intra-operative assessment per margin (site, distance where visually/palpably estimated, orientation marking applied) | textarea | No | No | mm |
| SCR-SO-009 | C.18 Surgical Oncology | field | Intra-operative margin assessment method (None / Frozen section / Gross visual only / Intra-operative imaging) | readonly | No | Yes | mm |
| SCR-SO-009 | C.18 Surgical Oncology | field | Nodal procedure performed (Sentinel node biopsy — technique, number retrieved, intra-operative result if rapid method used; and/or Regional lymphad… | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | En bloc structures removed | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Tumour rupture/spillage (Y/N — R for applicable tumour types , with management if occurred — SO-054 : tumour spillage is a discrete, mandatory, str… | select | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Intra-operative frozen section requested (Y/N — link to SCR-SO-021) | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Frozen section result (read-only from pathology response) | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | How the frozen result changed the procedure (structured: No change / Extended resection / Changed nodal approach / Aborted planned reconstruction /… | readonly | Yes | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Reconstruction performed (Y/N, against the plan's reconstruction-planned flag per GEN-CMP-001) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Type | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Technique | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Graft/flap type and donor site where applicable | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Reconstruction surgeon (may differ from primary surgeon, attributed) | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Implant/device used (link to Implants table below) | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Viability assessment at closure (e.g. flap perfusion check) where applicable. | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Specimen number | readonly | Yes | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Specimen label (as physically labelled, R) | text | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Anatomical site | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Laterality | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Orientation (structured description + optional diagram/photo attachment, consumed by SO-031's pathology handling instructions) | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Margin designation applied (which margins are marked, with which marking method — suture/ink/clip ) | select | No | No | mm |
| SCR-SO-009 | C.18 Surgical Oncology | field | Fresh or fixed | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Special test requested at time of excision | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Destination (Histopathology / Microbiology / Research — with consent status where research / Cytogenetics) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Sent to pathology time | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Pathology accession number (SO-004 traceability link) | number | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Accession confirmation status (Sent / Received — with discrepancy flag if a specimen sent is not accessioned within a configured interval, SO-056 ). | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Item | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Category (Mesh / Prosthesis / Expander / Fiducial / Port / Other) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Manufacturer | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Model | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Serial/lot number (R, scanned where configured) | number | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Site of implantation | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Implanting surgeon. | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Estimated blood loss | select | Yes | No | mL |
| SCR-SO-009 | C.18 Surgical Oncology | field | Fluids administered (crystalloid/colloid volumes — cross-reference to anaesthetic record) | number | No | No | mL |
| SCR-SO-009 | C.18 Surgical Oncology | field | Blood products transfused (repeating: component, units, batch/lot — cross-reference to Blood Bank's own transfusion record per BLD-010, displayed r… | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Urine output during the case where measured. | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Repeating: type | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | number | number | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | location | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | laterality | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | exit site | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | suction or gravity | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | plan (e.g. "remove when output < x mL/24h" — feeds SCR-SO-013's removal-criteria field) | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | each drain assigned its own device identifier (SO-008) that the post-operative drain record (SCR-SO-013) will track thereafter. | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Read-only import from the Theatre Safety Gate Sign-Out count record (SO-051) | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | count type (swab/needle/instrument) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | correct/incorrect | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | where incorrect, the recorded discrepancy-resolution action (SO-049) displayed here for completeness — not re-entered. | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Repeating: complication | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | severity (per the configured intra-operative complication scale , distinct from the post-operative grading in SCR-SO-015) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | management | number | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | outcome. Where any complication is recorded, the "Affects adjuvant timing" flag (SO-009) is presented for the surgeon's immediate assessment (may b… | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Closure layers and technique per layer | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Suture/staple material per layer | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Wound classification where used (e.g. clean/clean-contaminated/contaminated/dirty — a recognised infection-risk stratification, content and thresho… | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Dressing applied (type). | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Immediate post-operative destination (PACU / Ward / HDU / ICU — actual, compared against the plan's anticipated level of care per GEN-CMP-001) | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Ventilated on transfer (Y/N) | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Accompanying staff. | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Analgesia plan | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Antibiotic continuation plan | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | VTE prophylaxis continuation plan | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Diet/fluid plan | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Mobilisation plan | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Drain care instructions (per drain) | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Wound care instructions | textarea | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Investigations ordered for the post-operative period (launches SCR-INV-001) | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Activity/positioning restrictions | select | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Pathology follow-up plan | date | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Next clinical review (surgeon ward round timing). | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Primary surgeon signature (R, re-authenticated) | text | Yes | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Assistant surgeon co-signature where the institution requires it for trainee-operated cases | number | No | No | mL/h |
| SCR-SO-009 | C.18 Surgical Oncology | field | date/time of signature (distinct from operation end time). | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | Operative duration (CALC-194 = end time − start time) | readonly | No | Yes | min |
| SCR-SO-009 | C.18 Surgical Oncology | field | Estimated blood loss aggregation where multiple sub-estimates are entered (CALC-193) | readonly | No | Yes | mL |
| SCR-SO-009 | C.18 Surgical Oncology | field | specimen-accession discrepancy flag (SO-056) | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | field | planned-vs-actual concordance flags for procedure, approach, and level of care (GEN-CMP-001, ). | readonly | No | Yes |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:Team roster | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:Team roster | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:Team roster | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:procedure steps (structured) | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:procedure steps (structured) | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:procedure steps (structured) | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:specimens | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:specimens | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:specimens | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:implants | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:implants | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:implants | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:blood products | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:blood products | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:blood products | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:drains placed | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:drains placed | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:drains placed | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:counts (read-only) | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:counts (read-only) | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:counts (read-only) | Source / owner | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:complications. | Entry | text | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:complications. | Date / time | datetime-local | No | No |  |
| SCR-SO-009 | C.18 Surgical Oncology | table:complications. | Source / owner | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Condition on arrival (vitals imported from PACU record, read-only) | readonly | No | Yes |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Consciousness level | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Pain score | number | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Nausea | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Analgesia given in PACU (cross-referenced from PACU nursing/anaesthetic record) | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Drains/lines status confirmed present and functioning (per device, from SCR-SO-009's drain rows) | select | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Wound dressing status | select | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Urine output | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Orders confirmed/updated for the ward: analgesia, antibiotics, VTE prophylaxis, IV fluids, diet, mobilisation, drain management, wound care, monito… | number | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Escalation criteria (early-warning thresholds cross-referenced from the inpatient observation module, C.21) | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Named responsible surgical team contact. | text | No | No |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | Time from operation end to PACU arrival | readonly | No | Yes |  |
| SCR-SO-010 | C.18 Surgical Oncology | field | time in PACU . | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Post-operative day | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Interval events | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Symptoms (pain, nausea, bowel function, appetite) | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Examination findings by system, with wound/drain/stoma status pulled read-only from SCR-SO-012/013/014 (not re-entered, SO-059 ) | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Vitals trend (imported) | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Investigation results reviewed (imported, with acknowledgement) | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Analgesia adequacy and plan | textarea | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Mobility level achieved today vs target | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Diet stage (Nil by mouth / Clear fluids / Free fluids / Light diet / Normal diet) with progression criteria | number | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | VTE prophylaxis continuing status | select | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Antibiotic day n of course | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Assessment (narrative + structured complication check — "any new complication today?" Y/N, R, routing to SCR-SO-015 if Y) | select | Yes | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Plan | date | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Discharge planning items (home support, equipment, community referrals) progressing. | textarea | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | Post-operative day | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | days on antibiotics | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | days to anticipated discharge | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | field | mobility-vs-target variance. | readonly | No | Yes |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:Vitals trend | Entry | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:Vitals trend | Date / time | datetime-local | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:Vitals trend | Source / owner | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:medication changes log | Entry | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:medication changes log | Date / time | datetime-local | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:medication changes log | Source / owner | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:drain/line summary (cross-referenced status only). | Entry | text | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:drain/line summary (cross-referenced status only). | Date / time | datetime-local | No | No |  |
| SCR-SO-011 | C.18 Surgical Oncology | table:drain/line summary (cross-referenced status only). | Source / owner | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Wound identifier (linked to the operative note's incision/closure record) | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Location | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Assessment date/time | datetime-local | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Appearance | select | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Dimensions (length × width × depth, mm, where dehisced/open) | text | No | No | mm |
| SCR-SO-012 | C.18 Surgical Oncology | field | Wound edges (approximated / gaping / undermined) | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Exudate amount and type | select | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Odour | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Peri-wound skin condition | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Pain at wound site | datetime-local | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Dressing type and last change date/time | datetime-local | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Signs of infection (checklist, feeding a wound-infection flag) | multiselect | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Photograph | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Sutures/staples/clips present and removal plan | date | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Action taken | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Assessed by. | text | No | No |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | Days since surgery | readonly | No | Yes |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | days since last dressing change | readonly | No | Yes |  |
| SCR-SO-012 | C.18 Surgical Oncology | field | trend (improving/static/worsening) from the last two assessments . | readonly | No | Yes |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Drain ID (from Operative Note) | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Site | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Type (e.g. closed suction, gravity, Penrose ) | select | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Laterality | select | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Insertion date/time (from Operative Note) | datetime-local | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Suction or gravity | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Planned removal criteria (from Operative Note plan field). | textarea | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Date/time | datetime-local | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Output volume (this interval) | number | No | No | mL |
| SCR-SO-013 | C.18 Surgical Oncology | field | Cumulative output (CALC-192) | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Output colour/character | select | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Site condition | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Complication (blocked, dislodged, leaking) with action | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Recorded by. | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Removal criteria met (compared against the plan's structured criteria, thresholds) with a clinician/nurse confirmation | readonly | No | Yes |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Removal date/time | datetime-local | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Removed by | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Site condition post-removal | text | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | Complication at removal. | datetime-local | No | No |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | hour output | readonly | No | Yes |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | cumulative output (CALC-192) | readonly | No | Yes |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | trend (declining/static/rising) | readonly | No | Yes |  |
| SCR-SO-013 | C.18 Surgical Oncology | field | days in situ . | readonly | No | Yes |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Stoma ID | text | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Type (Colostomy / Ileostomy / Urostomy / Other ) | select | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Site | text | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Temporary or permanent (R — feeds discharge and survivorship planning) | textarea | Yes | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Formation date (from Operative Note) | date | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Planned reversal date where temporary. | date | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Date/time | datetime-local | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Output volume and consistency | number | No | No | mL |
| SCR-SO-014 | C.18 Surgical Oncology | field | Colour/viability of stoma (pink/healthy, dusky, necrotic — R, safety-critical) | text | Yes | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Peristomal skin condition (structured: intact, erythema, excoriation, breakdown) | text | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Appliance type in use | select | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Appliance change frequency | text | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Patient/carer independence level | select | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Education session delivered (link to education log, mirrors MAR/ORL counselling pattern) | text | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Complication (retraction, prolapse, parastomal hernia, necrosis, mucocutaneous separation) with action. | text | No | No |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | Days since formation | readonly | No | Yes |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | output trend | readonly | No | Yes |  |
| SCR-SO-014 | C.18 Surgical Oncology | field | independence progression . | readonly | No | Yes |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Complication (coded terminology, R) | text | Yes | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Category/system | select | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Onset date/post-operative day | date | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Onset context (during admission / after discharge — readmission) | text | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Severity grade | select | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Grading basis (clinical / laboratory / imaging / re-operative finding) | text | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Supporting evidence (linked result/imaging) | text | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Attribution to the index procedure (Definite / Probable / Possible / Unlikely / Unrelated) | datetime-local | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Investigations performed | text | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Intervention requiredwith detail | date | Yes | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Outcome (Resolved / Resolved with sequelae / Ongoing / Chronic / Contributed to death) | select | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Effect on discharge (None / Discharge delayed — n days / Readmission required) | number | Yes | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Effect on adjuvant timing (SO-009 structured flag: None / Adjuvant therapy delayed — estimated duration / Adjuvant therapy modality reconsidered / … | select | No | No | min |
| SCR-SO-015 | C.18 Surgical Oncology | field | Patient informed (Y/N) | select | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Follow-up plan. | textarea | No | No |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | Post-operative day at onset | readonly | No | Yes |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | days of discharge delay attributable | readonly | No | Yes |  |
| SCR-SO-015 | C.18 Surgical Oncology | field | cumulative complication count and highest grade for the episode . | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Actual surgery performed (read-only, from SCR-SO-009) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Specimen(s) (read-only list from SCR-SO-009/pathology accession, with links to the full synoptic report per specimen) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Histology (coded, read-only from pathology) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Grade | select | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Tumour size | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Tumour extent (pT-relevant descriptors) | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Margins — per margin: distance, status (Clear / Close / Involved), closest margin identified (CALC-195) | select | No | No | mm |
| SCR-SO-016 | C.18 Surgical Oncology | field | Nodes examined | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Nodes positive | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Extranodal extension (Y/N) | select | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Lymphovascular invasion (LVI) | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Perineural invasion (PNI) | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Treatment effect (where neoadjuvant therapy given — regression grading scale, read-only from pathology) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Pathological response category (where applicable, read-only from SCR-RSP-001/pathology) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Biomarkers relevant to adjuvant decision-making (read-only, linked to SCR-DX-003) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | pT / pN / pM (read-only from pathology) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Pathological stage (read-only, SCR-DX-002) displayed side by side with the pre-operative clinical stage (GEN-CMP-001, SO-005) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Concordance (: Concordant / Upstaged / Downstaged) | number | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Surgeon's interpretation/implication (narrative, R) | textarea | Yes | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Further surgery needed? (Y/N + detail) | select | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | MDT re-discussion required? | readonly | Yes | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | MO referral required? (Y/N) | select | Yes | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | RO referral required? (Y/N) | select | Yes | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Surveillance-only pathway appropriate? (Y/N) | select | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Patient informed. | date | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | Closest margin distance across all specimens (CALC-195) | readonly | No | Yes | mm |
| SCR-SO-016 | C.18 Surgical Oncology | field | days from surgery to pathology report (CALC-196) | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | field | concordance flag. | readonly | No | Yes |  |
| SCR-SO-016 | C.18 Surgical Oncology | table:stage comparison (system, cTNM, pTNM, stage group each, concordance). | Entry | text | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | table:stage comparison (system, cTNM, pTNM, stage group each, concordance). | Date / time | datetime-local | No | No |  |
| SCR-SO-016 | C.18 Surgical Oncology | table:stage comparison (system, cTNM, pTNM, stage group each, concordance). | Source / owner | text | No | No |  |
| SCR-SO-017 | C.18 Surgical Oncology | field | As SCR-DX-002: Staging system, basis = "Pathology", pT/pN/pM, prefix/suffix modifiers, site-specific required factors, Stage group (CALC-060), over… | date | Yes | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Surgery performed | text | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | surgical date | date | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | approach | text | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | complications summary (read-only from SCR-SO-015, with the "affects adjuvant timing" flag surfaced prominently). | readonly | No | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Current status (Discharged — recovered / Discharged — with ongoing issues / Still inpatient / Readmitted) | select | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | wound status | select | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | drains removed (Y/N, or "not applicable") | select | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | infection present (Y/N) | select | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | post-op performance status. | select | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Pathological stage (read-only from SCR-SO-017) | readonly | No | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | margins | text | No | No | mm |
| SCR-SO-018 | C.18 Surgical Oncology | field | nodes | text | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | biomarkers — auto-assembled, not re-typed. | readonly | No | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Readiness for adjuvant discussion | date | Yes | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Responsible specialty for the adjuvant decision | select | Yes | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | MDT required?. | readonly | Yes | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Target datewith countdown (CALC-202) | date | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Action owner (named clinician/service, R) | text | Yes | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Due date (editable with reason) | date | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Handoff method (Direct referral / MDT submission / Both). | select | No | No | kg/m² |
| SCR-SO-018 | C.18 Surgical Oncology | field | Acknowledged by receiver | datetime-local | Yes | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Receiver's initial plan. | date | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | Days elapsed since surgery/pathology | readonly | No | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | target-date countdown (CALC-202) | readonly | No | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | field | overdue flag against target. | readonly | No | Yes |  |
| SCR-SO-018 | C.18 Surgical Oncology | table:Handoff history (for cases with more than one handoff event, e.g. handed to MO then re-routed to MDT). | Entry | text | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | table:Handoff history (for cases with more than one handoff event, e.g. handed to MO then re-routed to MDT). | Date / time | datetime-local | No | No |  |
| SCR-SO-018 | C.18 Surgical Oncology | table:Handoff history (for cases with more than one handoff event, e.g. handed to MO then re-routed to MDT). | Source / owner | text | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Post-op interval (weeks/months since surgery, ) | text | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Symptoms | text | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Wound status (read-only summary from SCR-SO-012, or direct examination if the wound record was community-managed) | readonly | No | Yes |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Drain/stoma status (read-only summary, or "not applicable — removed") | readonly | No | Yes |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Pain (score + management) | number | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Nutrition (weight trend, intake) | number | No | No | kg |
| SCR-SO-019 | C.18 Surgical Oncology | field | Mobility/function (compared to pre-operative baseline where relevant, e.g. return to baseline mobility Y/N) | select | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Complications since discharge (repeating, linked to SCR-SO-015 if new entries created) | text | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Pathology status | date | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Adjuvant therapy status | readonly | Yes | Yes |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Rehabilitation referrals and progress | text | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Restrictions in place (lifting, driving, work) with planned lift dates | textarea | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Return-to-activity/work status | select | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Recurrence surveillance plan (imaging schedule, tumour marker schedule, clinical review interval — feeds C.24 Surveillance) | textarea | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Next review date. | date | No | No |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | Post-op interval | readonly | No | Yes |  |
| SCR-SO-019 | C.18 Surgical Oncology | field | time since adjuvant completion where applicable. | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Diagnosis | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Operation performed | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Operation date | date | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Surgeon. | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Auto-assembled narrative from daily progress notes (MO-CON-060/SO-059 pattern — assembled, not re-typed), editable summary layer on top. | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Auto-listed from SCR-SO-015 with grade and resolution status | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | "None" is an affirmative, attributed statement, not an empty section (GEN-LNG-001 NKDA-pattern applied to complications). | datetime-local | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Read-only current status from SCR-SO-012/013/014: wound(s) status and planned suture/staple removal date and location (community/clinic) | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | drains remaining in situ (Y/N, with take-home management plan) or "all removed" | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | stoma status and independence level, with supply prescription reference. | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Discharge medication list (from reconciled GEN-LNG-002), with anticoagulation restart plan re-stated explicitly (cross-referenced from SCR-SO-004's… | textarea | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | analgesia | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | antibiotics | date | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | other new/changed medications. | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Diet at discharge | datetime-local | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | mobility status | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | activity restrictions — lifting limit and duration, driving restriction and duration, return-to-work guidance (with an occupation-specific note whe… | number | No | No | min |
| SCR-SO-020 | C.18 Surgical Oncology | field | Structured, versioned instruction set for content | textarea | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | product structure requires: what to look for, what is normal, what is not, who to contact. | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Result available and reviewed with patient (Y/N) | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | result pending (Y/N — with the plan for communicating it once available, R if pending — SO-065 : a discharge occurring before final pathology is av… | select | Yes | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Structured, mandatory, versioned red-flag symptom list and thresholds (mirrors MAR-025's discipline exactly — never narrative advice) | textarea | Yes | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | hour surgical contact number | number | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | nearest-emergency-department instruction. | textarea | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Follow-up appointment | date | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Adjuvant/MDT plan status (read-only roll-up from SCR-SO-018) | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Investigations to be done before follow-up (list with booking status). | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Education delivered (checklist with material versions: wound care, drain/stoma care, medication, red flags, activity restrictions, follow-up) | multiselect | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Comprehension confirmed (method: teach-back / verbal / written) | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Carer/family involved in education. | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Dropdown (product-defined): Recovered as expected / Recovering with ongoing minor issues / Discharged with unresolved complication (link to SCR-SO-… | select | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | Length of stay | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | field | days to first follow-up . | readonly | No | Yes |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:Discharge medication list | Entry | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:Discharge medication list | Date / time | datetime-local | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:Discharge medication list | Source / owner | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:red-flag list | Entry | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:red-flag list | Date / time | datetime-local | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:red-flag list | Source / owner | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:follow-up appointment list. | Entry | text | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:follow-up appointment list. | Date / time | datetime-local | No | No |  |
| SCR-SO-020 | C.18 Surgical Oncology | table:follow-up appointment list. | Source / owner | text | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Specimen description | textarea | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Anatomical site/laterality | select | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Specific question (R — e.g. "margin clearance", "nodal involvement" — mirrors MDT-020's no-vague-question discipline) | textarea | Yes | No | mm |
| SCR-SO-021 | C.18 Surgical Oncology | field | Requesting surgeon | text | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Request time | text | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Urgency (always time-critical — no priority selector needed) | select | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Clinical context auto-assembled (diagnosis, procedure in progress). | readonly | No | Yes |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Received time transit duration | number | No | No | min |
| SCR-SO-021 | C.18 Surgical Oncology | field | Processing start time | datetime-local | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Result (structured per the question type, e.g. margin: clear/involved/close with distance where determinable on frozen tissue; nodal: positive/nega… | readonly | No | Yes | mm |
| SCR-SO-021 | C.18 Surgical Oncology | field | Limitations of frozen assessment stated (narrative, R — freezing artefact, sampling limitation) | readonly | Yes | Yes |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Result time | text | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Reported by (named pathologist) | text | No | No |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Deferred to permanent section (Y/N, where frozen assessment is inconclusive). | readonly | No | Yes |  |
| SCR-SO-021 | C.18 Surgical Oncology | field | Turnaround time (request to result) — tracked for departmental performance reporting. | readonly | No | Yes |  |
| SCR-PAT-001 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-001 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-001 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Accession | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Patient / UHID | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Specimen | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Procedure | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Primary site | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Priority | select | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Receipt date/time | datetime-local | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | TAT | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Status | select | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Ancillary pending | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | MDT deadline | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Assigned pathologist | text | No | No |  |
| SCR-PAT-001 | C.19 Pathology | table:Pathology cases | Actions | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-002 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-002 | C.19 Pathology | field | Collection date/time | datetime-local | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Receipt date/time | datetime-local | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Container count | number | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Fixative | select | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Labelling concordant | select | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Requisition concordant | select | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Specimen adequacy | select | Yes | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Discrepancy type | multiselect | No | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Discrepancy resolution | textarea | No | No |  |
| SCR-PAT-002 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-002 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Container ID | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Label as received | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Anatomical designation | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Laterality | select | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Orientation markers | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Fixative | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Integrity | text | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Received at | datetime-local | No | No |  |
| SCR-PAT-002 | C.19 Pathology | table:Containers | Barcode | text | No | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-003 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-003 | C.19 Pathology | field | Specimen type | text | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Specimen dimensions — X | number | No | No | mm |
| SCR-PAT-003 | C.19 Pathology | field | Specimen dimensions — Y | number | No | No | mm |
| SCR-PAT-003 | C.19 Pathology | field | Specimen dimensions — Z | number | No | No | mm |
| SCR-PAT-003 | C.19 Pathology | field | Specimen weight | number | No | No | g |
| SCR-PAT-003 | C.19 Pathology | field | Tumour visible | select | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Tumour dimension — maximum | number | No | No | mm |
| SCR-PAT-003 | C.19 Pathology | field | Distance to nearest margin | number | No | No | mm |
| SCR-PAT-003 | C.19 Pathology | field | Inking scheme | textarea | No | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Gross description | textarea | Yes | No |  |
| SCR-PAT-003 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-003 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-003 | C.19 Pathology | table:Blocks submitted | Block ID | text | No | No |  |
| SCR-PAT-003 | C.19 Pathology | table:Blocks submitted | Tissue / site | text | No | No |  |
| SCR-PAT-003 | C.19 Pathology | table:Blocks submitted | Orientation | text | No | No |  |
| SCR-PAT-003 | C.19 Pathology | table:Blocks submitted | Margin represented | text | No | No |  |
| SCR-PAT-003 | C.19 Pathology | table:Blocks submitted | Special processing | text | No | No |  |
| SCR-PAT-003 | C.19 Pathology | table:Blocks submitted | Comment | textarea | No | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-004 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-004 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Accession | text | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Block ID | text | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Slide ID | text | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Tissue | text | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Processing status | select | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Stain | text | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Created at | datetime-local | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | QC status | select | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Location | text | No | No |  |
| SCR-PAT-004 | C.19 Pathology | table:Blocks / slides | Assigned | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-005 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-005 | C.19 Pathology | field | Procedure | select | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Final diagnosis | textarea | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Histological type | text | Yes | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Morphology code | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Grade | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Tumour size — greatest dimension | number | No | No | mm |
| SCR-PAT-005 | C.19 Pathology | field | Tumour extent | textarea | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Lymphovascular invasion | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Perineural invasion | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Margin status | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Nodes examined | number | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Nodes positive | number | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Treatment effect present | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Pathological response grade / category | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | pT | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | pN | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | pM | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | pStage group | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Staging system / version | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Pathologist comment | textarea | No | No |  |
| SCR-PAT-005 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-005 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Marker / test | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Method | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Result | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Unit / score | number | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Interpretation | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Specimen / block | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Quality / adequacy | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Biomarkers / ancillary | Report date | date | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Margins | Margin | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Margins | Status | select | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Margins | Distance | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Margins | Unit | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Margins | Involved structure | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Margins | Comment | textarea | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Lymph node groups | Station / group | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Lymph node groups | Examined | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Lymph node groups | Positive | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Lymph node groups | Largest metastasis | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Lymph node groups | Extranodal extension | text | No | No |  |
| SCR-PAT-005 | C.19 Pathology | table:Lymph node groups | Comment | textarea | No | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-006 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-006 | C.19 Pathology | field | Overall margin status | select | Yes | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Closest margin | text | No | No |  |
| SCR-PAT-006 | C.19 Pathology | field | Closest margin distance | number | No | No | mm |
| SCR-PAT-006 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-006 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Margin ID | text | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Margin name | text | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Status | select | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Distance | text | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Unit | text | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Tumour at ink | datetime-local | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Orientation / specimen | text | No | No |  |
| SCR-PAT-006 | C.19 Pathology | table:Per-margin assessment | Comment | textarea | No | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-007 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-007 | C.19 Pathology | field | Total nodes examined | number | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Total nodes positive | number | Yes | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Largest metastatic deposit | number | No | No | mm |
| SCR-PAT-007 | C.19 Pathology | field | Extranodal extension | select | No | No |  |
| SCR-PAT-007 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-007 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Station / group | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Examined | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Positive | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Isolated tumour cells | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Micrometastases | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Macrometastases | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Largest deposit | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | ENE | text | No | No |  |
| SCR-PAT-007 | C.19 Pathology | table:Per-node station | Comment | textarea | No | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-008 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-008 | C.19 Pathology | field | Neoadjuvant therapy received | readonly | No | Yes |  |
| SCR-PAT-008 | C.19 Pathology | field | Therapy completion date | readonly | No | Yes |  |
| SCR-PAT-008 | C.19 Pathology | field | Interval to specimen | readonly | No | Yes |  |
| SCR-PAT-008 | C.19 Pathology | field | Residual tumour dimensions | text | No | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Treatment effect description | textarea | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Response grading system | text | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Response grade / category | text | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Pathologic complete response | select | Yes | No |  |
| SCR-PAT-008 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-008 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-009 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-009 | C.19 Pathology | field | Staging system | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Staging version / edition | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | pT | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | pN | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | pM | text | No | No |  |
| SCR-PAT-009 | C.19 Pathology | field | pStage group | text | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Stage assignment rationale | textarea | Yes | No |  |
| SCR-PAT-009 | C.19 Pathology | field | Clinical stage comparison | readonly | No | Yes |  |
| SCR-PAT-009 | C.19 Pathology | field | Concordance | readonly | No | Yes |  |
| SCR-PAT-009 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-009 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-010 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-010 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Test | text | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Block / specimen | text | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Method | select | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Ordered at | datetime-local | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Sent at | datetime-local | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Laboratory | text | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Expected date | date | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Result status | select | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Result | text | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Interpretation status | select | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Owner | text | No | No |  |
| SCR-PAT-010 | C.19 Pathology | table:Ancillary / biomarker tests | Days outstanding | number | No | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-011 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-011 | C.19 Pathology | field | Assay / panel | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Assay version | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Specimen / block | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Tumour content / adequacy | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Methodology | text | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Reference genome / transcript | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Overall interpretation | textarea | Yes | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Limitations | textarea | No | No |  |
| SCR-PAT-011 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-011 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Gene / locus | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Alteration | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Variant classification | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Allele fraction | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Copy number / expression | number | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Clinical significance | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Therapy / trial relevance | text | No | No |  |
| SCR-PAT-011 | C.19 Pathology | table:Molecular findings | Source / evidence | text | No | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-012 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-012 | C.19 Pathology | field | Theatre / OR | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Question from surgeon | textarea | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Specimen received at | datetime-local | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Frozen impression | textarea | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Result communicated to | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Communication method | select | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Communicated at | datetime-local | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Acknowledged by | text | Yes | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Permanent result concordance | select | No | No |  |
| SCR-PAT-012 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-012 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-013 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-013 | C.19 Pathology | field | External institution | text | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | External accession | text | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Material received | multiselect | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Prior diagnosis | textarea | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | CCA review diagnosis | textarea | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Concordance | select | Yes | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Clinical impact of discrepancy | textarea | No | No |  |
| SCR-PAT-013 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-013 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-014 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-014 | C.19 Pathology | field | Change type | select | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Reason | select | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Added / corrected content | textarea | Yes | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Clinical impact | textarea | No | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Consumers notified | multiselect | No | No |  |
| SCR-PAT-014 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-014 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-015 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-015 | C.19 Pathology | field | Critical / unexpected finding | textarea | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Severity / urgency | select | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Communicated to | text | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Communicated at | datetime-local | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Method | select | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Acknowledged by | text | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Acknowledged at | datetime-local | Yes | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Action / escalation | textarea | No | No |  |
| SCR-PAT-015 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-015 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-016 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-016 | C.19 Pathology | field | MDT meeting / case | text | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Material reviewed | textarea | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Key pathology findings | textarea | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Diagnostic / staging statement | textarea | Yes | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Uncertainty / limitations | textarea | No | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Recommendation / further pathology work | textarea | No | No |  |
| SCR-PAT-016 | C.19 Pathology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-PAT-016 | C.19 Pathology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-017 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-017 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Accession | text | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Block / slide ID | text | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Item type | select | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Current location | text | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Custody status | select | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Released to | text | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Released at | datetime-local | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Expected return | text | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Returned at | datetime-local | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Disposition | select | No | No |  |
| SCR-PAT-017 | C.19 Pathology | table:Custody items | Audit | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Cancer episode ID | text | Yes | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Accession number | text | Yes | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Requesting clinician / service | text | Yes | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Specimen / procedure date | datetime-local | Yes | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Primary site | text | Yes | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Laterality | select | No | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Clinical indication / question | textarea | Yes | No |  |
| SCR-PAT-018 | C.19 Pathology | field | Neoadjuvant treatment summary | readonly | No | Yes |  |
| SCR-PAT-018 | C.19 Pathology | field | Prior pathology comparison | readonly | No | Yes |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Metric | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Period | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Target | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Actual | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Status | select | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Trend | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Owner | text | No | No |  |
| SCR-PAT-018 | C.19 Pathology | table:Quality metrics | Action | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-001 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Accession | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Patient / UHID | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Modality | select | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Study | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Acquired at | datetime-local | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Priority | select | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Purpose | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Baseline | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Status | select | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Assigned radiologist | select | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | TAT | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Critical flag | text | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | MDT date | date | No | No |  |
| SCR-RAD-001 | C.20 Radiology | table:Reporting queue | Actions | text | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-002 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Requested study | text | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Protocol assigned | text | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Contrast decision | select | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Contrast agent | text | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Contrast volume | number | No | No | mL |
| SCR-RAD-002 | C.20 Radiology | field | Contrast rate | number | No | No | mL/s |
| SCR-RAD-002 | C.20 Radiology | field | Phases required | multiselect | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Anatomical coverage | textarea | Yes | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Creatinine / eGFR status | readonly | No | Yes |  |
| SCR-RAD-002 | C.20 Radiology | field | Contrast allergy status | readonly | No | Yes |  |
| SCR-RAD-002 | C.20 Radiology | field | Pregnancy status | readonly | No | Yes |  |
| SCR-RAD-002 | C.20 Radiology | field | Sedation / anaesthesia required | select | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Special instructions | textarea | No | No |  |
| SCR-RAD-002 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-002 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-003 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Protocol used | text | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Contrast details | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Image quality | select | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Limitations | textarea | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Comparison studies | textarea | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Organ/system findings | textarea | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Impression | textarea | Yes | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Proposed response category | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Response criteria set / version | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Recommendation | textarea | No | No |  |
| SCR-RAD-003 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-003 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Lesion ID | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Label | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Organ / site | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Laterality | select | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Type | select | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Target / non-target / new | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Measurable | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Measurement method | select | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Long axis | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Short axis | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Unit | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Series / image / slice | number | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Prior measurement | text | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Baseline change % | number | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Nadir change % | number | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Lesion status | select | No | No |  |
| SCR-RAD-003 | C.20 Radiology | table:Lesion table | Comment | textarea | No | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-004 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-004 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Lesion ID | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Study date | date | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Site | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Target status | select | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Long axis | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Short axis | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Unit | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Baseline | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Nadir | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Absolute change | text | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | % from baseline | number | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | % from nadir | number | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Status | select | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Image reference | number | No | No |  |
| SCR-RAD-004 | C.20 Radiology | table:Persistent lesions | Measured by | text | No | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-005 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Criteria set | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Criteria version | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Baseline study | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Target lesion sum — baseline | readonly | No | Yes |  |
| SCR-RAD-005 | C.20 Radiology | field | Target lesion sum — current | readonly | No | Yes |  |
| SCR-RAD-005 | C.20 Radiology | field | Change from baseline | readonly | No | Yes | % |
| SCR-RAD-005 | C.20 Radiology | field | New lesion present | select | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Proposed response | text | Yes | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Confidence / qualifier | textarea | No | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Confirmation scan required | select | No | No |  |
| SCR-RAD-005 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-005 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-006 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Critical finding | textarea | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Clinical urgency | select | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Communicated to | text | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Method | select | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Communication time | datetime-local | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Acknowledged by | text | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Acknowledgement time | datetime-local | Yes | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Escalation events | textarea | No | No |  |
| SCR-RAD-006 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-006 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-007 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Change type | select | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Reason | textarea | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Added / corrected content | textarea | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Clinical impact | textarea | No | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Ordering clinician re-notified | select | Yes | No |  |
| SCR-RAD-007 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-007 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-008 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Source institution | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Study date | date | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Modality | select | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Media / transfer method | select | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Import status | select | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Matched patient | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Episode | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Duplicate status | select | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Formal reread | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Baseline designated | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Reviewer | text | No | No |  |
| SCR-RAD-008 | C.20 Radiology | table:External studies | Outcome | select | No | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-009 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-009 | C.20 Radiology | field | MDT meeting / case | text | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Studies reviewed | textarea | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Key imaging findings | textarea | Yes | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Resectability / response statement | textarea | No | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Uncertainty / limitations | textarea | No | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Recommendation / further imaging | textarea | No | No |  |
| SCR-RAD-009 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-009 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-010 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Procedure | text | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Target lesion / site | text | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Laterality | select | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Consent status | readonly | No | Yes |  |
| SCR-RAD-010 | C.20 Radiology | field | Coagulation / platelet readiness | readonly | No | Yes |  |
| SCR-RAD-010 | C.20 Radiology | field | Technique / guidance modality | text | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Local anaesthetic / sedation | text | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Samples obtained | textarea | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Immediate complication | textarea | No | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Post-procedure instructions | textarea | Yes | No |  |
| SCR-RAD-010 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-010 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-011 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Contrast agent | text | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Lot / expiry | text | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Volume administered | number | Yes | No | mL |
| SCR-RAD-011 | C.20 Radiology | field | Route | select | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Reaction occurred | select | Yes | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Reaction onset time | datetime-local | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Reaction manifestations | multiselect | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Reaction severity | select | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Management | textarea | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Outcome | textarea | No | No |  |
| SCR-RAD-011 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-011 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-012 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Designated baseline study | text | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Baseline designation reason | textarea | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Measurement criteria / convention | text | Yes | No |  |
| SCR-RAD-012 | C.20 Radiology | field | Designated by | readonly | No | Yes |  |
| SCR-RAD-012 | C.20 Radiology | field | Designated at | readonly | No | Yes |  |
| SCR-RAD-012 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-012 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | Study | text | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | Date | date | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | Modality | select | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | External | text | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | Eligible for comparison | text | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | Reason | textarea | No | No |  |
| SCR-RAD-012 | C.20 Radiology | table:Comparison studies | Selected | select | No | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-013 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Second reader | text | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Review outcome | select | Yes | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Discrepancy detail | textarea | No | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Clinical impact | textarea | No | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Resolution | textarea | No | No |  |
| SCR-RAD-013 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-013 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-014 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Metric | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Period | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Target | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Actual | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Status | select | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Trend | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Owner | text | No | No |  |
| SCR-RAD-014 | C.20 Radiology | table:Quality metrics | Action | text | No | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Cancer episode ID | text | Yes | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Accession number | text | Yes | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Study / modality | text | Yes | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Study date/time | datetime-local | Yes | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Clinical indication | textarea | Yes | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Specific clinical question | textarea | Yes | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Primary site | text | No | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Treatment phase | readonly | No | Yes |  |
| SCR-RAD-015 | C.20 Radiology | field | Baseline study | text | No | No |  |
| SCR-RAD-015 | C.20 Radiology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RAD-015 | C.20 Radiology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Recipient | text | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Role | text | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Delivery method | select | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Delivered at | datetime-local | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Acknowledgement required | text | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Acknowledged at | datetime-local | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Status | select | No | No |  |
| SCR-RAD-015 | C.20 Radiology | table:Distribution / acknowledgement | Escalation | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Ward / bed | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Patient | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | UHID | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Admission reason | textarea | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | LOS | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Primary cancer | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Treatment phase | select | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Acuity / EWS | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Critical results | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Active therapies | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Pending consults | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Discharge barrier | text | No | No |  |
| SCR-IPD-001 | C.21 Inpatient Oncology | table:Inpatient worklist | Actions | text | No | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Requested by | text | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Reason for admission | textarea | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Urgency | select | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Expected length of stay | number | No | No | days |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Bed type | select | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Monitoring level | text | Yes | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Isolation requirement | text | No | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Accepting clinician | text | No | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Acceptance decision | select | No | No |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-002 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Ward | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Bed | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Source / referring location | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Admission diagnosis / reason | textarea | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Identity verified | select | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Allergies reconciled | select | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Handover received from | text | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Handover summary | textarea | Yes | No |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-003 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Chief concern / reason for admission | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | History of present illness | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Cancer history / current status | readonly | No | Yes |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Current treatment / last administration | readonly | No | Yes |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Comorbidities | textarea | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Medication reconciliation | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Review of systems | textarea | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Physical examination | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Working diagnosis / assessment | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Initial problem list | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Plan by problem | textarea | Yes | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | VTE assessment / prophylaxis plan | textarea | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Infection / isolation plan | textarea | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Nutrition plan | textarea | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Goals-of-care status | text | No | No |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-004 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Problem | text | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Onset | text | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Status | select | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Priority | select | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Owner | text | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Assessment | textarea | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Plan | textarea | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Linked orders | text | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Last reviewed | text | No | No |  |
| SCR-IPD-005 | C.21 Inpatient Oncology | table:Problem list | Resolution date | date | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Order type | select | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Item / instruction | textarea | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Dose / parameter | number | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Route | select | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Frequency | text | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Start | text | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Stop | text | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Priority | select | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Indication | text | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Owner | text | No | No |  |
| SCR-IPD-006 | C.21 Inpatient Oncology | table:Inpatient orders | Status | select | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Medication | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Order version | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Standard dose | number | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Calculated dose | number | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Final ordered dose | number | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Pharmacy prepared dose | number | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Actual administered dose | number | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Unit | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Route | select | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Scheduled time | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Actual time | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Status | select | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Variance | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Reason | textarea | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Administered by | text | No | No |  |
| SCR-IPD-007 | C.21 Inpatient Oncology | table:Medication administration | Second check | text | No | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Interval events | readonly | No | Yes |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Subjective / symptoms | textarea | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Examination | textarea | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Results reviewed | textarea | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Problem-oriented assessment | textarea | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Plan by problem | textarea | Yes | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Oncology treatment decision | textarea | No | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Discharge readiness / barriers | textarea | No | No |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-008 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Shift date/time | datetime-local | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Neurological / consciousness | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Respiratory assessment | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Cardiovascular assessment | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Pain score | number | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Nutrition / intake | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Fluid balance summary | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Mobility / falls risk | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Skin / pressure risk | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Patient education | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Escalation required | select | Yes | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Device ID | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Type | select | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Site | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Insertion date | date | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Assessment | textarea | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Output | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Care | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Lines / drains / devices | Action | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | Date/time | datetime-local | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | BP | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | Pulse | number | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | RR | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | Temp | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | SpO2 | number | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | Oxygen | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | Pain | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | EWS | text | No | No |  |
| SCR-IPD-009 | C.21 Inpatient Oncology | table:Observations | Action | text | No | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Trigger | select | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Clinical time | datetime-local | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Assessment | textarea | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Immediate interventions | textarea | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Escalated to | text | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Escalation time | datetime-local | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Response / outcome | textarea | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Disposition | select | Yes | No |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-010 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Consulting specialty | text | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Specific question | textarea | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Urgency | select | Yes | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Response required by | datetime-local | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Consultant response | textarea | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Recommendations | textarea | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Response date/time | datetime-local | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Requesting team action / acknowledgement | textarea | No | No |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-011 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Discussion date/time | datetime-local | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Participants | textarea | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Interpreter | text | No | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Patient goals / values | textarea | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Treatment preferences | textarea | Yes | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Resuscitation / escalation decision | text | No | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Decision-maker / surrogate | text | No | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Review trigger / date | text | No | No |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-012 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | From location | text | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | To location / facility | text | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Reason | textarea | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Clinical status at transfer | textarea | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Active treatments / infusions | textarea | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Lines / drains / devices | textarea | No | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Pending results / tasks | textarea | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Accepting clinician | text | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Handover communicated at | datetime-local | Yes | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Transport mode / accompanying staff | text | No | No |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-013 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Ward / bed | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Patient | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Acuity / EWS | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Oxygen | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Active infusions | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Systemic therapy today | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Isolation | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Pending results | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Pending consults | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Escalation | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Discharge target | text | No | No |  |
| SCR-IPD-014 | C.21 Inpatient Oncology | table:Live inpatient board | Assigned nurse / clinician | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Patient | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Target date | date | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Clinical stability | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Medication reconciliation | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Discharge summary | textarea | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Follow-up booked | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Pending results plan | textarea | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Education | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Transport | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Home support | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Barrier | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Owner | text | No | No |  |
| SCR-IPD-015 | C.21 Inpatient Oncology | table:Discharge readiness | Status | select | No | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Principal discharge diagnosis | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Other diagnoses / problems | textarea | No | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Hospital course | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Oncology treatment delivered | readonly | No | Yes |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Procedures | textarea | No | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Complications | textarea | No | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Key results | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Discharge medication reconciliation | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Discharge medications | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Follow-up appointments | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Pending investigations and owner | textarea | No | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Red flags / contact instructions | textarea | Yes | No |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-016 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Cancer episode ID | text | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Admission ID | text | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Ward / bed | text | No | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Admission date/time | datetime-local | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Consultant of record | text | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Admission reason | textarea | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Allergy status | readonly | No | Yes |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Date/time of death | datetime-local | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Place of death | text | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Clinician confirming death | text | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Cause / certification details | textarea | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Family / next-of-kin notified | select | Yes | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Notification details | textarea | No | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Organ / tissue donation pathway | text | No | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Cancer episode closure reason | readonly | No | Yes |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Bereavement referral / support | textarea | No | No |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-IPD-017 | C.21 Inpatient Oncology | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-001 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-001 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Patient | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Episode | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Treatment / line | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Assessment due | textarea | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Trigger | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Latest imaging | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Radiology proposal | select | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Clinical components | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Status | select | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Days overdue | number | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Owner | text | No | No |  |
| SCR-RSP-001 | C.22 Response Assessment | table:Response worklist | Actions | text | No | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Assessment reason | select | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Baseline date | date | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Baseline imaging / pathology / marker source | textarea | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Criteria / framework | text | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Criteria version | text | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Assessment components required | multiselect | Yes | No |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-002 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Radiology report / study | text | Yes | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Baseline target sum | readonly | No | Yes |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Current target sum | readonly | No | Yes |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Change from baseline | readonly | No | Yes | % |
| SCR-RSP-003 | C.22 Response Assessment | field | Change from nadir | readonly | No | Yes | % |
| SCR-RSP-003 | C.22 Response Assessment | field | Non-target assessment | text | No | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | New lesion status | select | Yes | No |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Radiologist-proposed response | readonly | No | Yes |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-003 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-004 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Lesion ID | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Site | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Baseline date | date | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Baseline measurement | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Nadir date | date | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Nadir measurement | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Current date | date | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Current measurement | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Unit | text | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | % from baseline | number | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | % from nadir | number | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Status | select | No | No |  |
| SCR-RSP-004 | C.22 Response Assessment | table:Target lesion comparison | Source image | number | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-005 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-005 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Date | date | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Treatment phase | select | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Source | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Component | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Value / category | select | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Proposed / confirmed | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Criteria | text | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Decision | select | No | No |  |
| SCR-RSP-005 | C.22 Response Assessment | table:Response timeline | Owner | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Symptoms | textarea | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Examination | textarea | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Measurable clinical lesions | textarea | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Performance status | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Clinician impression | textarea | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Biochemical marker / test | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Biochemical baseline | number | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Biochemical nadir | number | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Biochemical current | number | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Biochemical unit | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Biochemical trend | readonly | No | Yes |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Pathology specimen / source | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Response system / version | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Pathological grade / category | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Residual tumour | text | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Pathologic complete response | select | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Overall component interpretation | textarea | No | No |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-006 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Radiologist-proposed response | readonly | No | Yes |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Clinical response component | readonly | No | Yes |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Biochemical response component | readonly | No | Yes |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Pathological response component | readonly | No | Yes |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Clinician-confirmed response | select | Yes | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Confirmation rationale | textarea | Yes | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Disease status event | select | Yes | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Next treatment decision | select | Yes | No |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-007 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Discordance type | multiselect | Yes | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Uncertainty / limitation | textarea | Yes | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Additional evidence required | textarea | No | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Resolution decision | textarea | Yes | No |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Resolved by | readonly | No | Yes |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-008 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Event type | select | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Event date | date | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Sites involved | textarea | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Supporting evidence | textarea | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Episode disposition | select | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | New line of therapy required | select | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Clinical rationale | textarea | Yes | No |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-009 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Cancer episode ID | text | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Assessment date | date | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Line of therapy | text | No | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Treatment phase / cycle | text | No | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Criteria / framework name | text | No | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Criteria version | text | No | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Confirmed response | readonly | No | Yes |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Recommended next step | select | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Responsible specialty | text | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Due date | date | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | MDT discussion required | select | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Handoff note | textarea | Yes | No |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-RSP-010 | C.22 Response Assessment | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Patient | text | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Episode | text | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Modality | select | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Last treatment date | date | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Completion reason | textarea | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Outstanding source records | text | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Summary status | select | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Signatory | text | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Distribution status | select | No | No |  |
| SCR-CMP-001 | C.23 Treatment Completion | table:Completion worklist | Actions | text | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Completion type | select | Yes | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Current disease / response status | text | Yes | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Key residual toxicities / complications | textarea | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Ongoing supportive needs | textarea | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Next care phase | select | Yes | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Next review / assessment date | date | No | No |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-CMP-002 | C.23 Treatment Completion | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Diagnosis & staging snapshot | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Treatment intent and plan history | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Systemic therapy — planned vs actually administered | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Radiotherapy — prescribed vs actually delivered | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Surgery — planned vs actual procedure | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Final pathology / pathological stage | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Response history | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Significant toxicities / complications | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Cumulative exposure | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Ongoing medications | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Follow-up and surveillance plan | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Late-effect considerations | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Care-team contacts | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Clinician synthesis / completion narrative | textarea | Yes | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Outstanding unresolved issue | textarea | No | No |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-CMP-003 | C.23 Treatment Completion | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-CMP-004 | C.23 Treatment Completion | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Modality | select | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Planned value / course | textarea | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Actual delivered value / course | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Start | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | End | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Completed | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Variance | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Authorised modification source | text | No | No |  |
| SCR-CMP-004 | C.23 Treatment Completion | table:Modality reconciliation | Unresolved discrepancy | text | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Cardiac baseline at completion | textarea | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Renal baseline at completion | textarea | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Hepatic baseline at completion | textarea | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Neurological / functional baseline | textarea | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-CMP-005 | C.23 Treatment Completion | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Agent / modality | select | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Exposure metric | text | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Actual cumulative exposure | text | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Unit | text | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Source administrations / fractions | number | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Known late-effect domain | text | No | No |  |
| SCR-CMP-005 | C.23 Treatment Completion | table:Cumulative exposure | Monitoring plan | textarea | No | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Handoff destination | select | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Handoff summary | textarea | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Outstanding investigations / results | textarea | No | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Owner | text | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Due date | date | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Receiving clinician / service | text | Yes | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Acceptance / acknowledgement | text | No | No |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-CMP-006 | C.23 Treatment Completion | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Cancer episode ID | text | Yes | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Treatment plan version | text | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Treatment intent | select | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Treatment start date | date | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Treatment end date | date | Yes | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Reason for completion / discontinuation | textarea | Yes | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-CMP-007 | C.23 Treatment Completion | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Recipient | text | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Role / relationship | text | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Document version | text | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Method | select | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Sent at | datetime-local | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Acknowledgement required | text | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Acknowledged at | datetime-local | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Status | select | No | No |  |
| SCR-CMP-007 | C.23 Treatment Completion | table:Summary distribution | Reissue reason | textarea | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Patient | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Episode | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Primary cancer | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Last treatment | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Disease status | select | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Follow-up due | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Days overdue | number | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Planned investigations | textarea | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Late-effect flags | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Assigned clinician | text | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Recall status | select | No | No |  |
| SCR-SURV-001 | C.24 Surveillance / Survivorship | table:Surveillance worklist | Actions | text | No | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Interval history | textarea | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Recurrence red-flag symptoms | multiselect | No | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Physical examination | textarea | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Late effects reviewed | textarea | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Surveillance results reviewed | textarea | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Disease status | select | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Health maintenance / risk reduction | textarea | No | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Next review interval | text | Yes | No |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-SURV-002 | C.24 Surveillance / Survivorship | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Surveillance intent / goal | textarea | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Follow-up frequency | text | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Duration of specialist surveillance | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Late-effect monitoring plan | textarea | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Recurrence red flags / escalation | textarea | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Responsible clinician / service | text | Yes | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Primary-care handoff requirement | select | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Investigation | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Frequency / trigger | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Start | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Stop | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Owner | text | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Rationale | textarea | No | No |  |
| SCR-SURV-003 | C.24 Surveillance / Survivorship | table:Planned surveillance investigations | Status | select | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Investigation | text | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Clinical rationale | textarea | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Frequency | text | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Due date | date | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Status | select | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Ordered | text | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Resulted | text | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Result summary | textarea | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Next due | text | No | No |  |
| SCR-SURV-004 | C.24 Surveillance / Survivorship | table:Surveillance investigations | Owner | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Late effect / concern | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Onset | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Severity / grade | select | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Attribution | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Status | select | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Intervention | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Owner | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Last reviewed | text | No | No |  |
| SCR-SURV-005 | C.24 Surveillance / Survivorship | table:Late effects | Next review | text | No | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Diagnosis and treatment summary | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Care team contacts | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Treatments received | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Ongoing medications | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Late effects to watch | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Follow-up schedule | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Planned tests and rationale | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Red-flag symptoms | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Rehabilitation / nutrition / psychosocial resources | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Fertility / sexual-health support | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Health maintenance | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Next appointments | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Language / template version | text | Yes | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Interpreter / translation governance | text | No | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Patient / carer education delivered | select | Yes | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Comprehension / teach-back | select | Yes | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Date issued | date | Yes | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Re-issue reason | textarea | No | No |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-SURV-006 | C.24 Surveillance / Survivorship | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Recurrence suspicion trigger | select | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Trigger detail | textarea | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Date identified | date | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Urgency | select | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Immediate investigations / actions | textarea | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Re-entry destination | select | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Same episode vs possible new primary | select | Yes | No |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-SURV-007 | C.24 Surveillance / Survivorship | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Patient | text | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Follow-up due | text | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Days overdue | number | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Risk / priority | select | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Preferred contact | text | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Contact attempts | datetime-local | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Barrier | text | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Next attempt | datetime-local | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Escalation level | text | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Outcome | select | No | No |  |
| SCR-SURV-008 | C.24 Surveillance / Survivorship | table:Recall queue | Owner | text | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Domain | text | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Need / reason | textarea | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Service / provider | text | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Priority | select | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Referral date | date | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Appointment | text | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Status | select | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Outcome | select | No | No |  |
| SCR-SURV-009 | C.24 Surveillance / Survivorship | table:Support referrals | Follow-up owner | text | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | field | Cancer episode ID | text | Yes | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | field | Surveillance phase | text | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | field | Last treatment date | date | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | field | Current disease status | select | Yes | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | field | Next review date | date | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Date | date | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Event | text | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Category | select | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Disease status | select | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Result / outcome | select | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Responsible service | text | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Next milestone | text | No | No |  |
| SCR-SURV-010 | C.24 Surveillance / Survivorship | table:Surveillance timeline | Source | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-001 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-001 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-001 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Patient | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | UHID | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Payer | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Treatment / order reference | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Estimate status | select | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Authorisation status | select | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Deposit status | select | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Financial barrier | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Due date | date | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Owner | text | No | No |  |
| SCR-FIN-001 | C.25 Finance | table:Financial worklist | Actions | text | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-002 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-002 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-002 | C.25 Finance | field | Policy / member number | text | Yes | No |  |
| SCR-FIN-002 | C.25 Finance | field | Coverage start | date | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Coverage end | date | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Sum insured / limit | number | No | No | INR |
| SCR-FIN-002 | C.25 Finance | field | Network / plan | text | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Verification status | select | Yes | No |  |
| SCR-FIN-002 | C.25 Finance | field | Verification reference | text | No | No |  |
| SCR-FIN-002 | C.25 Finance | field | Primary / secondary payer | select | Yes | No |  |
| SCR-FIN-002 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-002 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-003 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-003 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Estimate number | readonly | No | Yes |  |
| SCR-FIN-003 | C.25 Finance | field | Source treatment plan / order | text | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Estimate date | date | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Valid until | date | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Estimated gross amount | number | Yes | No | INR |
| SCR-FIN-003 | C.25 Finance | field | Estimated payer share | number | No | No | INR |
| SCR-FIN-003 | C.25 Finance | field | Estimated patient share | number | No | No | INR |
| SCR-FIN-003 | C.25 Finance | field | Estimate assumptions / exclusions | textarea | Yes | No |  |
| SCR-FIN-003 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-003 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Service / drug / procedure | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Quantity | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Unit / basis | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Rate | number | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Amount | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Coverage | number | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Patient share | text | No | No |  |
| SCR-FIN-003 | C.25 Finance | table:Estimate lines | Source master | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-004 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-004 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-004 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-004 | C.25 Finance | field | Total estimated treatment cost | readonly | No | Yes | INR |
| SCR-FIN-004 | C.25 Finance | field | Clinical decision fields are read-only | readonly | No | Yes |  |
| SCR-FIN-004 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-004 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Sequence | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Drug / service | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Clinical order reference | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Ordered quantity / basis | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Chargeable quantity | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Tariff / rate | number | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Amount | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Payer eligibility | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Patient share | text | No | No |  |
| SCR-FIN-004 | C.25 Finance | table:Treatment costing | Source master / version | text | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-005 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-005 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-005 | C.25 Finance | field | Preauthorisation number | text | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Requested amount | number | Yes | No | INR |
| SCR-FIN-005 | C.25 Finance | field | Requested services / treatment | textarea | Yes | No |  |
| SCR-FIN-005 | C.25 Finance | field | Clinical administrative summary | textarea | Yes | No |  |
| SCR-FIN-005 | C.25 Finance | field | Supporting documents | multiselect | Yes | No |  |
| SCR-FIN-005 | C.25 Finance | field | Submitted at | datetime-local | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Payer decision | select | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Approved amount | number | No | No | INR |
| SCR-FIN-005 | C.25 Finance | field | Validity / conditions | textarea | No | No |  |
| SCR-FIN-005 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-005 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-006 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-006 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-006 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-006 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Patient | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Reference | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Payer | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Query / denial reason | textarea | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Received at | datetime-local | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Response due | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Owner | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Appeal status | select | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Documents required | text | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Status | select | No | No |  |
| SCR-FIN-006 | C.25 Finance | table:Queries / appeals | Actions | text | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-007 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-007 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-007 | C.25 Finance | field | Amount received | number | Yes | No | INR |
| SCR-FIN-007 | C.25 Finance | field | Payment method | select | Yes | No |  |
| SCR-FIN-007 | C.25 Finance | field | Transaction / reference number | text | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Receipt number | readonly | No | Yes |  |
| SCR-FIN-007 | C.25 Finance | field | Received at | datetime-local | Yes | No |  |
| SCR-FIN-007 | C.25 Finance | field | Allocated to invoice / estimate | text | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Refundable / non-refundable policy reference | text | No | No |  |
| SCR-FIN-007 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-007 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-008 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-008 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-008 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-008 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Source clinical / operational event | text | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Service code | text | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Charge description | text | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Quantity | number | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Rate | number | Yes | No | INR |
| SCR-FIN-008 | C.25 Finance | field | Gross charge | readonly | No | Yes | INR |
| SCR-FIN-008 | C.25 Finance | field | Payer share | number | No | No | INR |
| SCR-FIN-008 | C.25 Finance | field | Patient share | number | No | No | INR |
| SCR-FIN-008 | C.25 Finance | field | Posting status | select | Yes | No |  |
| SCR-FIN-008 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-008 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-009 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-009 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-009 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-009 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Package / contract | text | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Version | text | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Eligibility status | select | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Eligibility reason | textarea | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Inclusion / exclusion result | textarea | Yes | No |  |
| SCR-FIN-009 | C.25 Finance | field | Limit / cap applied | number | No | No | INR |
| SCR-FIN-009 | C.25 Finance | field | Override reason | textarea | No | No |  |
| SCR-FIN-009 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-009 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Drug / service | text | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Source order / plan | text | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Estimated amount | number | Yes | No | INR |
| SCR-FIN-010 | C.25 Finance | field | Approval type | select | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Requested at | datetime-local | Yes | No |  |
| SCR-FIN-010 | C.25 Finance | field | Decision | select | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Decision reason / conditions | textarea | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Valid until | date | No | No |  |
| SCR-FIN-010 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-010 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Counselling date/time | datetime-local | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Attendees | textarea | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Estimate explained | select | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Coverage / exclusions explained | select | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Financial barriers | textarea | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Assistance / options discussed | textarea | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Patient / family understanding | textarea | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Agreed financial plan | textarea | Yes | No |  |
| SCR-FIN-011 | C.25 Finance | field | Follow-up date | date | No | No |  |
| SCR-FIN-011 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-011 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-012 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-012 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-012 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-012 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Claim number | number | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Payer | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Service period | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Submitted amount | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Submitted at | datetime-local | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Status | select | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Approved amount | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Paid amount | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Query / denial | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Next action | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Owner | text | No | No |  |
| SCR-FIN-012 | C.25 Finance | table:Claims | Days outstanding | number | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-013 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-013 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-013 | C.25 Finance | field | Original receipt / charge | text | Yes | No |  |
| SCR-FIN-013 | C.25 Finance | field | Refund / credit reason | select | Yes | No |  |
| SCR-FIN-013 | C.25 Finance | field | Amount | number | Yes | No | INR |
| SCR-FIN-013 | C.25 Finance | field | Approval required | select | Yes | No |  |
| SCR-FIN-013 | C.25 Finance | field | Approver | text | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Approval status | select | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Refund method | text | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Posting reference | text | No | No |  |
| SCR-FIN-013 | C.25 Finance | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-FIN-013 | C.25 Finance | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-FIN-014 | C.25 Finance | field | Patient / UHID | text | Yes | No |  |
| SCR-FIN-014 | C.25 Finance | field | Cancer episode ID | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | field | Payer category | select | Yes | No |  |
| SCR-FIN-014 | C.25 Finance | field | Payer / insurer | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | field | Authorisation status | select | No | No |  |
| SCR-FIN-014 | C.25 Finance | field | Currency | select | Yes | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Metric | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Period | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Target | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Actual | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Status | select | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Trend | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Owner | text | No | No |  |
| SCR-FIN-014 | C.25 Finance | table:Finance metrics | Action | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-001 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-001 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-001 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | User ID | text | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Display name | text | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Professional registration number | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | field | Assigned roles | multiselect | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Facility / department scope | multiselect | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Account status | select | Yes | No |  |
| SCR-ADM-001 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-001 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Role | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Object / screen | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | View | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Create | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Edit | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Sign | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Approve / override | text | No | No |  |
| SCR-ADM-001 | C.26 Administration | table:Role permissions | Facility scope | text | No | No |  |
| SCR-ADM-002 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-002 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-002 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-002 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Facility code | text | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Facility name | text | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Address / timezone | text | Yes | No |  |
| SCR-ADM-002 | C.26 Administration | field | Operating hours | textarea | No | No |  |
| SCR-ADM-002 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-002 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Location code | text | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Name | text | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Type | select | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Parent | text | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Capacity | text | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Status | select | No | No |  |
| SCR-ADM-002 | C.26 Administration | table:Locations / resources | Operating hours | number | No | No |  |
| SCR-ADM-003 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-003 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-003 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-003 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-003 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-003 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-003 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-003 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-003 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-003 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Code | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Name | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Parent | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Clinical / administrative | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Default location | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Responsible role | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Routing destinations | text | No | No |  |
| SCR-ADM-003 | C.26 Administration | table:Departments / services | Status | select | No | No |  |
| SCR-ADM-004 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-004 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-004 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-004 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-004 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-004 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-004 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-004 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-004 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-004 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | User / clinician | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Specialty | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Registration no. | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Facility | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Department | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Roster date | date | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Start | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | End | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Location | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Availability | text | No | No |  |
| SCR-ADM-004 | C.26 Administration | table:Clinicians / roster | Status | select | No | No |  |
| SCR-ADM-005 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-005 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-005 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-005 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Regimen code | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Regimen name | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Disease / indication | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Intent / setting | multiselect | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Line of therapy applicability | multiselect | No | No |  |
| SCR-ADM-005 | C.26 Administration | field | Cycle length | number | Yes | No | days |
| SCR-ADM-005 | C.26 Administration | field | Planned cycles / duration | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | field | Protocol / source reference | text | Yes | No |  |
| SCR-ADM-005 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-005 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Sequence | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Block | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Drug / item | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Dose basis | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Standard dose | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Dose unit | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Route | select | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Diluent | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Volume | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Concentration | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Rate | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Duration | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Day(s) | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Premed / hydration / treatment / supportive | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Treatment sequence | Mandatory | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Criterion | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Source test / field | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Operator | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Threshold / rule | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Unit | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Freshness | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Hard stop / override / warning | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Readiness rules | Exception | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Monitoring requirements | Investigation / assessment | textarea | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Monitoring requirements | Baseline | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Monitoring requirements | Frequency | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Monitoring requirements | Trigger | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Monitoring requirements | Owner | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Trigger | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Grade / value | select | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Action | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Dose % / new dose | number | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Delay / hold | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Restart criteria | text | No | No |  |
| SCR-ADM-005 | C.26 Administration | table:Dose modification rules | Approval role | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-006 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-006 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-006 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Drug / generic name | text | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Brand / formulary display | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | field | Drug code | text | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Hazardous / antineoplastic | select | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Vesicant / irritant classification | select | No | No |  |
| SCR-ADM-006 | C.26 Administration | field | Routes allowed | multiselect | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Dose units allowed | multiselect | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Dose basis allowed | multiselect | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Cumulative dose tracking required | select | Yes | No |  |
| SCR-ADM-006 | C.26 Administration | field | Compatibility / stability source | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-006 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Diluent | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Final concentration range | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Container | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Filter | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Light protection | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Stability / BUD | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Storage | number | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Preparation rules | Source / version | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Strength | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Unit | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Container size | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Concentration | text | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Route | select | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Storage | number | No | No |  |
| SCR-ADM-006 | C.26 Administration | table:Formulations / vials | Status | select | No | No |  |
| SCR-ADM-007 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-007 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-007 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-007 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Rule-set name | text | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Applicable regimen / therapy | text | Yes | No |  |
| SCR-ADM-007 | C.26 Administration | field | Applicable cycle / day | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-007 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Criterion | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Clinical source | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Test / field | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Operator | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Value / range | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Unit | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Freshness window | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Missing-data behavior | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Tier | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Override role | text | No | No |  |
| SCR-ADM-007 | C.26 Administration | table:Readiness criteria | Reason options | textarea | No | No |  |
| SCR-ADM-008 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-008 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-008 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-008 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-008 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-008 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-008 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-008 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-008 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-008 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Drug / regimen | text | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Trigger type | select | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Trigger value / grade | select | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Dose action | number | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Reduction % / dose | number | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Rounding rule | text | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Max variance | text | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Delay / hold | text | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Restart criteria | text | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Override role | text | No | No |  |
| SCR-ADM-008 | C.26 Administration | table:Dose modification / rounding rules | Source | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-009 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-009 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-009 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-009 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-009 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-009 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-009 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-009 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-009 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Code | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Test name | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Specimen | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Canonical unit | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Allowed source units | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Conversion rule | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Reference range policy | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Plausibility min | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Plausibility max | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Critical rule | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | LOINC / standard code | text | No | No |  |
| SCR-ADM-009 | C.26 Administration | table:Laboratory catalogue | Status | select | No | No |  |
| SCR-ADM-010 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-010 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-010 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-010 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-010 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-010 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-010 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-010 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-010 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-010 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Code | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Study | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Modality | select | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Body region | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Protocol | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Contrast options | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Preparation | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Renal prerequisite | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Pregnancy screen | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | MR safety | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Duration | number | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Standard code | text | No | No |  |
| SCR-ADM-010 | C.26 Administration | table:Radiology catalogue / protocols | Status | select | No | No |  |
| SCR-ADM-011 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-011 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-011 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-011 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Template name | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Disease / indication | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Intent | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Technique / modality | text | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Peer review required | select | Yes | No |  |
| SCR-ADM-011 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-011 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Phase | select | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Site | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Laterality | select | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Target volumes | number | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Total dose | number | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Fractions | number | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Dose / fraction | number | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:RT phases | Schedule | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | OAR | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Laterality | select | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Constraint type | select | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Parameter | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Operator | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Value | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Unit | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Class | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:OAR constraints | Source / protocol version | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:IGRT / setup rules | Modality | select | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:IGRT / setup rules | Frequency | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:IGRT / setup rules | Matching structure | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:IGRT / setup rules | Translation tolerance | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:IGRT / setup rules | Rotation tolerance | text | No | No |  |
| SCR-ADM-011 | C.26 Administration | table:IGRT / setup rules | Action if exceeded | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-012 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-012 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-012 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-012 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-012 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-012 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-012 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-012 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-012 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Procedure code | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Procedure name | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Disease / site | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Laterality required | select | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Approach options | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Nodal options | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Reconstruction options | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Pre-op prerequisites | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Consent type | select | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Specimen schema | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Post-op pathway | text | No | No |  |
| SCR-ADM-012 | C.26 Administration | table:Surgical procedures | Status | select | No | No |  |
| SCR-ADM-013 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-013 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-013 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-013 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Synoptic template name | text | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Disease / primary site | text | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Specimen / procedure applicability | multiselect | Yes | No |  |
| SCR-ADM-013 | C.26 Administration | field | Staging system / version | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-013 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Order | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Element ID | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Label | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Type | select | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Required | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Unit / value set | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Conditional parent / rule | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Repeating | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Standard code | text | No | No |  |
| SCR-ADM-013 | C.26 Administration | table:Synoptic elements | Downstream mapping | text | No | No |  |
| SCR-ADM-014 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-014 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-014 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-014 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Template type | select | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Document / consent name | text | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Applicability rule | textarea | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Language | text | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Template body / schema | textarea | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Signature requirement | text | Yes | No |  |
| SCR-ADM-014 | C.26 Administration | field | Witness requirement | select | No | No |  |
| SCR-ADM-014 | C.26 Administration | field | Validity / expiry rule | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-015 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-015 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-015 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-015 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-015 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-015 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-015 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-015 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-015 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Value set | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Local code | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Display | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Standard system | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Standard code | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Synonyms | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Order | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Active | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Effective from | text | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Retired at | datetime-local | No | No |  |
| SCR-ADM-015 | C.26 Administration | table:Value set terms | Replacement | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-016 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-016 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-016 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-016 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-016 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-016 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-016 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-016 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-016 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Concept / analyte | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Canonical unit | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Source unit | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Conversion formula / factor | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Precision | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Rounding | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Plausibility min | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Plausibility max | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Display rule | text | No | No |  |
| SCR-ADM-016 | C.26 Administration | table:Units / normalisation | Approval | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-017 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-017 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-017 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-017 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-017 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-017 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-017 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-017 | C.26 Administration | field | Author / accountable owner | readonly | No | Yes |  |
| SCR-ADM-017 | C.26 Administration | field | Clinical / operational date-time | datetime-local | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Rule ID | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Context | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Trigger expression | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Tier | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Presented to roles | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Hard stop | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Override roles | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Required reason | textarea | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Escalation target | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Escalation interval | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Effective version | text | No | No |  |
| SCR-ADM-017 | C.26 Administration | table:Alert / escalation rules | Status | select | No | No |  |
| SCR-ADM-018 | C.26 Administration | field | Master record ID | readonly | No | Yes |  |
| SCR-ADM-018 | C.26 Administration | field | Name / display label | text | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Status | select | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Version | text | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Effective from | date | No | No |  |
| SCR-ADM-018 | C.26 Administration | field | Effective to | date | No | No |  |
| SCR-ADM-018 | C.26 Administration | field | Owner / approving authority | text | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Change reason | textarea | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Release attestation | textarea | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Clinical sign-off complete | select | Yes | No |  |
| SCR-ADM-018 | C.26 Administration | field | Deployment / activation note | textarea | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Release ID | text | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Masters / versions included | text | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Submitted by | text | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Clinical reviewers | text | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Approval status | select | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Effective date | date | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Activation status | select | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Rollback target | text | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Change summary | textarea | No | No |  |
| SCR-ADM-018 | C.26 Administration | table:Configuration releases | Audit link | text | No | No |  |