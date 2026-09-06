# Small-Step Review Method — What CCA Reviewers Should Validate

For **every screen and every field/table column**, the reviewer should evaluate the following chain:

**1. Why is this information needed?**  Is it clinically/operationally necessary at this point?

**2. Who enters it?**  Is the owning role correct? Should another department only view it?

**3. How is it entered?**  Free text, numeric, date/time, checkbox, dropdown, multiselect, repeating table, derived value, integration result.

**4. Is it mandatory, conditional or optional?**  If conditional, what exact trigger makes it appear/required?

**5. What unit/value set applies?**  Confirm units, allowed choices, defaults and whether “Other + specify” is needed.

**6. What is the source?**  Manual measurement, clinician decision, upstream signed record, device/LIS/RIS/PACS/TPS/pharmacy integration, or calculated value.

**7. How should it be displayed?**  Single value, timeline, comparison, trend, table, status chip, planned-vs-actual pair, source/date/author badge, warning banner, printable note.

**8. Who must see it downstream?**  Confirm the receiving role can continue without asking for missing information outside the system.

**9. Can it change after signing?**  Confirm whether it freezes, creates an amendment/version, or remains a live operational state.

**10. What safety behavior applies?**  Warning, hard stop, override, second check, senior sign-off, acknowledgement, escalation.

**11. Does the generated note/report read like a real clinical document?**  Check both structured data and human-readable output.

**12. Record the verdict.**  Use: Correct — Freeze / Change Required / Missing / Should Be Conditional / Should Be Integration / Not Applicable / Needs Discussion.

The in-product **CCA Validation Center** and the Excel workbook use the same review language so feedback can be consolidated without interpretation.
