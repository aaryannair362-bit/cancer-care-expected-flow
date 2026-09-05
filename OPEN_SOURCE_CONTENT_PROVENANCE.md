# Open-Source Clinical Content Provenance — V12.2

## Purpose

V12 demonstrates how an oncology HIS/EMR can ingest historical/open-source regimen structures without allowing source material to silently become an executable patient order.

## Imported OpenMRS Oncology reference set

All 12 YAML files in the historical repository regimen directory are normalized into `clinical_content/openmrs_historical_regimens.json`. Every row is seeded with:

- `source_id = SRC-OPENMRS-ONC`
- original source file path;
- source repository and branch;
- source blob SHA where collected;
- source-license label;
- `status = Imported Draft`;
- `orderable = false`;
- explicit clinical limitations.

Representative records include AC, CHOP, Carboplatin + Taxol, CMF, COP, 5-FU/Leucovorin, single-agent cyclophosphamide/doxorubicin and weekly/q3-week paclitaxel historical references.

## What V12 preserves

Useful structural concepts preserved from source include regimen/order-set name, recommended cycle count/interval, relative treatment day, medication category, medication identity, dose and unit, route, timing, dilution/administration instructions where present, and source path/blob provenance.

V12 does **not** infer missing clinical content. For example, if a historical artifact lacks a computable current readiness rule or an AUC target/dose value, it stays missing/pending review rather than being invented.

## License

The repository license is **Mozilla Public License 2.0** with an **OpenMRS Healthcare Disclaimer**. `clinical_content/OPENMRS_NOTICE.txt` records the local notice and use boundary. Any commercial packaging should preserve applicable source notices and satisfy MPL obligations; legal review is recommended.

## Clinical-currency rule

Historical availability is not evidence of current clinical correctness. Imported rows are immutable and cannot be reviewed/activated in place. The required path is:

> **Historical source → CCA working-copy clone → local normalization → formulary mapping → current safety criteria → Medical Oncology review → Oncology Pharmacy review → explicit Admin activation.**

The acceptance suite exercises this path using temporary acceptance-test local mappings, then `reset_demo.py` removes those mutations before packaging. The clean distributed database therefore does not present any historical OpenMRS regimen as a production-ready treatment order set.


## Separation from V12.2 synthetic QA content

The synthetic institutional QA templates used by the 41-case software test pack are authored test fixtures under `SRC-CCA-QA`; they are not derived from the historical OpenMRS regimen imports described above. Activating those synthetic fixtures for product testing does not change the non-orderable status or provenance rules of the historical source material.
