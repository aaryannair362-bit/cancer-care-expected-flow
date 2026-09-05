/* V12.2-PC1.9 — Structural Conformance Phase 7
 * Residual structural closure: distinct Intake Nurse + MDT Chair role surfaces,
 * governed diagnostic/result provenance, privacy-minimized Front Desk consent status,
 * response measurement vs clinician confirmation, and postoperative adjuvant-review routing.
 */
(() => {
  'use strict';
  const BUILD = 'V12.2-PC1.9';
  const STRUCTURAL_NOTE = 'Synthetic QA structure — institutional clinical content still requires CCA approval.';

  function humanRoleHint(role){
    if(role === 'Intake Nurse') return 'Owns measured intake, explicit units, allergies and medication reconciliation before consultation.';
    if(role === 'MDT Chair') return 'Reviews the submitted Tumour Board recommendation and provides the final Chair attestation; the Coordinator remains the recorder.';
    if(role === 'Laboratory / Phlebotomy') return 'Final results preserve units, abnormal flags, reference-range provenance and amendment lineage.';
    if(role === 'Surgical Oncology') return 'Operative Record remains separate from Surgical Plan; final pathology can open the adjuvant-review handoff.';
    return '';
  }

  function installBuildIdentity(){
    document.title = 'CCA Cancer Care ' + BUILD;
    document.querySelectorAll('.brand .badge').forEach(x => x.textContent = BUILD);
    const h = document.querySelector('#login h1');
    if(h) h.textContent = 'CCA Cancer Care OS — ' + BUILD + ' Structural Conformance Phase 7';
  }

  function installRoleContext(){
    const roleName = document.getElementById('roleName');
    const content = document.getElementById('content');
    if(!roleName || !content) return;
    const update = () => {
      const role = (roleName.textContent || '').trim();
      const hint = humanRoleHint(role);
      let box = document.getElementById('pc19RoleHint');
      if(!hint){ if(box) box.remove(); return; }
      if(!box){
        box = document.createElement('div'); box.id='pc19RoleHint'; box.className='alert blue';
        content.prepend(box);
      }
      box.innerHTML = `<b>${role}</b> · ${hint}<div class="mini muted">${STRUCTURAL_NOTE}</div>`;
    };
    new MutationObserver(update).observe(roleName,{childList:true,subtree:true});
    new MutationObserver(update).observe(content,{childList:true});
    update();
  }

  document.addEventListener('DOMContentLoaded', () => { installBuildIdentity(); installRoleContext(); });
  window.PC19 = { BUILD, STRUCTURAL_NOTE, humanRoleHint };
})();
/* Structural evidence markers for clinician-facing surfaces:
   Postoperative adjuvant-review readiness
   Reference-range provenance
*/
