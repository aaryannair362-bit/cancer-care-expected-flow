# Clinical Content Governance — V12.2

## Institution-master principle

Treatment-critical templates and formulary definitions belong to an **institution content master**, not to an individual patient record.

```text
Institution Clinical Content Master
├── Regimen Templates
├── Workflow Templates
├── Report Templates
├── RT Templates
├── Surgical Templates
├── Terminology / Value Sets
└── Institution Formulary

              ↓ instantiate exact approved version

Patient Treatment Plan / Order / Course / Administration
```

Patient-specific orders store the exact template ID/version/source. Later master changes never silently rewrite signed historical orders.

## External-content lifecycle

```text
External / Historical Source (immutable)
→ Clone to CCA Working Copy
→ Local clinical normalization
→ Institution formulary mapping
→ Server-owned readiness/safety criteria
→ Medical Oncology / specialty review
→ Oncology Pharmacy review where medication content exists
→ Admin activation
→ Active
→ New version / Retired
```

An external import cannot be edited or activated directly.

## Systemic regimen editing

- Medical Oncology owns the clinical drug sequence, dose basis, protocol dose/unit and route in a Draft CCA working copy.
- Oncology Pharmacy owns preparation-oriented fields such as diluent, volume, timing/duration and preparation notes; Pharmacy cannot alter the clinician-owned drug/dose/route fields.
- Editing clinical content invalidates prior clinical and Pharmacy review.
- Editing Pharmacy preparation content invalidates Pharmacy review.
- Active/orderable templates are immutable; changes require a new version.

## Institution formulary lifecycle

```text
Draft Formulary Version
→ Oncology Pharmacy Review
→ Admin Activation
→ Active
→ New Version or Retired
```

The master stores local code/code-system, display name, version, formulations/strengths, permitted routes, permitted diluents, rounding policy, source reference and review evidence.

The exact same **Active** formulary master is used by:

1. regimen activation (every medication must map), and
2. Oncology Pharmacy preparation (formulation/strength/route/diluent verification).

This prevents content governance and dispensing from using contradictory masters.

## Patient-specific order rule

A regimen template is clinical content, not a signed patient order. The oncologist still reviews current patient variables, readiness evidence and patient-specific calculated/final doses and explicitly authorizes the Treatment Order. Variance is stored against the ordered item and never changes the master template.

## Role ownership

- **Medical Oncology:** systemic clinical-content review and patient-specific systemic order authorization.
- **Oncology Pharmacy:** medication/formulary and preparation-content review; verification/preparation/dispensing of signed patient orders.
- **Radiation Oncology:** RT prescription/template clinical review.
- **Radiation Physicist:** independent physics/QA template review, not physician prescription approval.
- **Surgical Oncology:** surgical-plan/pathway template review.
- **Hospital Management/Admin:** lifecycle activation/retirement administration, not substitute clinical approval.

## Specialist sign-off

The role-surface contract supports explicit specialist review with `Accepted / Minor Gap / Major Gap / Critical Gap`. The product does not self-declare a role surface clinically complete; each deployment should obtain the corresponding practising-specialist review.


## Synthetic institutional QA content

V12.2 contains a separate `SRC-CCA-QA` content family used only for product execution tests and hospital demonstrations. QA templates may be Active/orderable inside the synthetic demo environment solely to exercise workflow behavior. Their labels/source/disclaimer must remain visible and they must never be represented as approved patient-care clinical guidance.

The QA pack contains 21 systemic regimens, 16 RT templates, 14 surgical templates and 2 continuous-therapy templates, plus 5 synthetic formulary items. Historical/open-source reference content is still governed independently and remains non-orderable by default.
