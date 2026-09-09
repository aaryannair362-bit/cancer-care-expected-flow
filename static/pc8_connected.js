/* V12.2-PC8.0 — Connected Multidisciplinary frontend layer.
   Loaded last: extends ROLES/MENUS and wraps V.xxx/handle/renderApp/renderPage in place,
   following the same override pattern already used by pc1.js..pc1_9.js. Nothing here
   deletes or replaces earlier pages — it only adds new roles/pages and layers additional
   panels onto existing ones. */
(function(){
'use strict';

/* ---------- 1. Roles the classic backend now serves that the frontend never listed ---------- */
const PC8_NEW_ROLES=['Intake Nurse','Pathology Technologist','MDT Chair','Inpatient Oncology Clinician','Radiation Dosimetrist / Planner','Anaesthetist','Blood Bank / Transfusion','Stoma / Wound Nurse','Dietitian / Nutrition','Psycho-Oncology','Palliative Care','Clinical Trials / Research','Health Information Management'];
PC8_NEW_ROLES.forEach(r=>{if(!ROLES.includes(r))ROLES.push(r)});

const SUPPORT_TYPE_BY_ROLE={'Anaesthetist':'anaesthesia','Blood Bank / Transfusion':'blood_bank','Stoma / Wound Nurse':'stoma_wound','Dietitian / Nutrition':'nutrition','Psycho-Oncology':'psychosocial','Palliative Care':'palliative','Clinical Trials / Research':'clinical_trial','Health Information Management':'him','Pathology Technologist':'pathology_processing','Radiation Dosimetrist / Planner':'rt_planning'};
const SUPPORT_LABEL={anaesthesia:'Anaesthesia Assessment',blood_bank:'Blood Bank / Transfusion',stoma_wound:'Wound / Stoma Assessment',nutrition:'Nutrition Assessment',psychosocial:'Psycho-Oncology Assessment',palliative:'Palliative Care Assessment',clinical_trial:'Clinical Trial Screening',him:'HIM Request',pathology_processing:'Specimen Processing',rt_planning:'RT Planning Status'};
Object.keys(SUPPORT_TYPE_BY_ROLE).forEach(r=>{if(!MENUS[r])MENUS[r]=[['WORKLIST','summary','Patient Summary'],['SUPPORT','support',SUPPORT_LABEL[SUPPORT_TYPE_BY_ROLE[r]]]]});
if(!MENUS['Intake Nurse'])MENUS['Intake Nurse']=(MENUS['Nurse Navigator']||[]).slice();
if(!MENUS['MDT Chair'])MENUS['MDT Chair']=[['WORKLIST','summary','Patient Summary'],['MDT','mdt','MDT / Tumour Board — Chair Review'],['JOURNEY','journey','Patient Journey'],['HISTORY','audit','Audit']];
if(!MENUS['Inpatient Oncology Clinician'])MENUS['Inpatient Oncology Clinician']=[['WORKLIST','summary','Patient Summary'],['IPD','ipd','Inpatient Care & Medication Orders'],['TOXICITY','toxicity','Toxicity'],['JOURNEY','journey','Patient Journey']];
['Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator'].forEach(r=>{if(MENUS[r]&&!MENUS[r].some(x=>x[1]==='survivorship'))MENUS[r].push(['SURVIVORSHIP','survivorship','Treatment Completion / Survivorship'])});

/* pc1_2.js's pc12BuildNav() renders a hand-picked "Patient care" nav from PC12_PRIMARY for
   13 core roles, bypassing MENUS entirely (and pre-dates the task inbox and survivorship
   pages). Extend its whitelist in place rather than fighting/replacing that nav — this is
   the same object pc12BuildNav reads from on every render. */
if(typeof PC12_PRIMARY!=='undefined'){
 Object.keys(PC12_PRIMARY).forEach(r=>{if(!PC12_PRIMARY[r].includes('tasks'))PC12_PRIMARY[r]=PC12_PRIMARY[r].concat(['tasks'])});
 ['Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator'].forEach(r=>{if(PC12_PRIMARY[r]&&!PC12_PRIMARY[r].includes('survivorship'))PC12_PRIMARY[r]=PC12_PRIMARY[r].concat(['survivorship'])});
}
if(typeof pc12MenuLabel==='function'){
 const pc8BasePc12MenuLabel=pc12MenuLabel;
 pc12MenuLabel=function(k){if(k==='tasks')return 'My Tasks / Worklist';if(k==='survivorship')return 'Treatment Completion / Survivorship';return pc8BasePc12MenuLabel(k)};
}

/* pc1_2.js's V.order and V.daycare both call a pc1TreatmentSequence(order) helper that is
   referenced but was never defined anywhere in the bundle (a pre-existing bug, found while
   browser-testing this merge — both pages threw ReferenceError and never rendered). Supplying
   it here is the minimal fix: it doesn't touch pc1_2.js/pc1_3.js, and simply becomes available
   as a global by the time either page is first opened. */
if(typeof window.pc1TreatmentSequence==='undefined'){
 window.pc1TreatmentSequence=function(o){
  const items=(o&&o.data&&o.data.items)||[];
  if(!items.length)return '<div class="alert amber">No ordered items on this record.</div>';
  const groups=[];
  items.slice().sort((a,b)=>(a.sequence||0)-(b.sequence||0)).forEach(x=>{
   const g=x.group||'Other';let grp=groups.find(z=>z.name===g);
   if(!grp){grp={name:g,items:[]};groups.push(grp)}
   grp.items.push(x);
  });
  return groups.map(g=>`<div class="mini muted top-gap"><b>${esc(g.name)}</b></div><div class="sequence">${g.items.map(x=>`<div class="seq"><div class="n">${esc(x.sequence!=null?x.sequence:'')}</div><div class="drug">${esc(x.drug)}</div><div>${esc(x.ordered_dose!=null?x.ordered_dose:(x.calculated_dose!=null?x.calculated_dose:(x.protocol_dose!=null?x.protocol_dose:'—')))} ${esc(x.ordered_unit||x.calculated_unit||x.protocol_unit||'')} • ${esc(x.route||'')}</div>${x.administration_at?`<div class="mini">${fmt(x.administration_at)}</div>`:''}</div>`).join('<div class="arrow">→</div>')}</div>`).join('');
 };
}

/* ---------- 2. Selection-only login (no credential/PIN): picking a user or role signs you
   straight in. Both remain named/role-attributed server-side (see /api/login) -- this only
   drops the credential step from the demo UI so selecting is the entire action. ---------- */
async function pc8PopulateNamedLogin(){
 try{
  const r=await api('/api/login/users');
  const u=$('#loginUser');if(u)u.innerHTML='<option value="" selected disabled>Select individual validation user…</option>'+r.users.map(x=>`<option value="${esc(x.username)}">${esc(x.display_name)} — ${esc(x.role)} (${esc(x.username)})</option>`).join('');
 }catch(e){/* login/users not reachable yet */}
}
async function pc8NamedLogin(){
 const username=val('loginUser');if(!username)return;
 try{const j=await api('/api/login',{method:'POST',body:JSON.stringify({username})});S.token=j.token;S.role=j.actor.role;localStorage.setItem('cca_v12_token',S.token);localStorage.setItem('cca_v12_role',S.role);$('#loginErr').classList.add('hidden');await load()}catch(e){$('#loginErr').textContent=e.message;$('#loginErr').classList.remove('hidden')}
}
async function pc8QuickRoleLogin(){
 const role=val('loginRole');if(!role)return;
 try{const j=await api('/api/login',{method:'POST',body:JSON.stringify({role})});S.token=j.token;S.role=j.actor.role;localStorage.setItem('cca_v12_token',S.token);localStorage.setItem('cca_v12_role',S.role);$('#loginErr').classList.add('hidden');await load()}catch(e){$('#loginErr').textContent=e.message;$('#loginErr').classList.remove('hidden')}
}
{const u=$('#loginUser');if(u)u.onchange=pc8NamedLogin;}
{const r=$('#loginRole');if(r)r.onchange=pc8QuickRoleLogin;}
{const t=$('#loginModeToggle');if(t)t.onclick=()=>{const named=$('#loginNamed'),quick=$('#loginQuick');const showingQuick=!quick.classList.contains('hidden');if(showingQuick){quick.classList.add('hidden');named.classList.remove('hidden');t.textContent='Use quick role demo login instead'}else{named.classList.add('hidden');quick.classList.remove('hidden');t.textContent='Use individual named-user login instead'}};}
pc8PopulateNamedLogin();

const pc8BaseRenderApp=renderApp;
renderApp=function(){
 pc8BaseRenderApp();
 const a=S.meta&&S.meta.actor;
 if(a&&a.username){const el=$('#actorId');if(el)el.textContent=(a.name||'')+' • '+(a.professional_id||'')+' • '+a.username}
};

/* ---------- 3. Cross-patient task inbox with provenance, fixing the dead task-source/ ---------- */
/*    task-perform/tasks-refresh buttons and keeping the worklist unscoped to one patient. */
let PC8_TASKS=[],PC8_TASKS_LOADING=false;
async function pc8LoadTasks(){try{const r=await api('/api/tasks');PC8_TASKS=r.tasks||[]}catch(e){toast(e.message,true)}}
const TASK_PAGE={'Registration / referral':'registration','Support service referral':'support','Surveillance encounter':'survivorship','Progression confirmation':'survivorship','MDT case preparation':'mdt','Historical treatment confirmation':'survivorship','Treatment completion review':'survivorship','Survivorship planning':'survivorship','IPD medication administration':'ipd','Next-cycle decision':'survivorship','Treatment readiness':'readiness','Readiness re-evaluation':'readiness','Treatment modification':'trace','RT interruption review':'radiation','RT OTV':'radiation','RT fraction delivery':'radiation','Theatre readiness':'surgery','Surgery execution':'surgery','Adjuvant decision':'surgery','Pathology review':'pathology','Pathology accession':'pathology','Clinical trial review':'survivorship','PRD Handoff':'pc4_workflows'};

function sourceStatusWarning(ctx){
 if(ctx.consumable===false)return `<div class="alert red"><b>Not consumable.</b> ${esc(ctx.blocking_reason||'')}</div>`;
 if(ctx.source_record_id)return `<div class="alert green">Source opened with provenance. Downstream user must consume this record without re-entering upstream-owned facts.</div>`;
 return '';
}
function taskSourceHtml(ctx){
 const p=ctx.provenance||{};
 return sourceStatusWarning(ctx)+`<div class="card"><h3>Authoritative source provenance</h3>${kv('Source type',esc(ctx.source_record_type||p.source_type||'—'))}${kv('Source ID',esc(ctx.source_record_id||p.source_id||'—'))}${kv('Version',esc(ctx.source_record_version!=null?ctx.source_record_version:'—'))}${kv('Status',esc(ctx.source_record_status||'—'))}${kv('Signed / approved by',esc(ctx.signed_by||'—'))}${kv('Signed / approved at',fmt(ctx.signed_at))}${kv('Created by',esc(p.created_by||'—'))}${kv('Updated by',esc(p.updated_by||'—'))}</div>`
 +(ctx.source_record?`<div class="card top-gap"><h3>Source record (read-only)</h3><pre class="source-json">${esc(JSON.stringify(ctx.source_record.data!==undefined?ctx.source_record.data:ctx.source_record,null,2))}</pre></div>`:'<div class="alert amber top-gap">Source record content is not visible to this role.</div>')
 +(['Open','Acknowledged'].includes(ctx.status)?`<div class="row sticky-actions"><button class="btn primary" data-act="task-perform" data-id="${esc(ctx.id)}">Perform My Action</button></div>`:'');
}

V.tasks=()=>{
 const rows=PC8_TASKS;
 return title('My Tasks / Multidisciplinary Worklist','Closed-loop connected-workflow tasks across every patient assigned to this role. Upstream signed data is consumed with provenance; downstream roles do not re-enter another discipline’s facts.',`<button class="btn" data-act="tasks-refresh">Refresh Worklist</button>`)
 +`<div class="table-wrap task-table"><table><thead><tr><th>Priority</th><th>Patient / Episode</th><th>Responsibility</th><th>Workflow state</th><th>Source / provenance</th><th>Due / created</th><th>Actions</th></tr></thead><tbody>${rows.map(x=>`<tr class="${['Open','Acknowledged'].includes(x.status)?'':'task-history'}"><td>${badge(x.priority,statusColor(x.priority))}</td><td><b>${esc((x.patient&&x.patient.name)||x.patient_id||'—')}</b><div class="mini mono">${esc(x.patient_id||'')}</div></td><td><b>${esc(x.title)}</b><div class="mini">${esc(x.task_type||'')}</div><div class="mini muted">${esc(x.reason||'')}</div></td><td>${badge(x.status,statusColor(x.status))}</td><td class="mono mini">${esc(x.source_type||'')} / ${esc(x.source_id||'')}</td><td class="mini">${fmt(x.due_at||x.created_at)}</td><td><div class="task-actions">${x.status==='Open'?`<button class="btn sm" data-act="task-ack" data-id="${x.id}">Acknowledge</button>`:''}<button class="btn sm" data-act="task-source" data-id="${x.id}">Open Source Record</button>${['Open','Acknowledged'].includes(x.status)?`<button class="btn sm primary" data-act="task-perform" data-id="${x.id}">Perform My Action</button><button class="btn sm danger" data-act="task-escalate" data-id="${x.id}">Escalate</button>`:''}</div></td></tr>`).join('')||'<tr><td colspan="7">No tasks for this role yet.</td></tr>'}</tbody></table></div>`;
};

const pc8BaseRenderPage=renderPage;
renderPage=function(){
 pc8BaseRenderPage();
 if(S.page==='tasks'&&!PC8_TASKS_LOADING){
  PC8_TASKS_LOADING=true;
  pc8LoadTasks().then(()=>{PC8_TASKS_LOADING=false;if(S.page==='tasks')pc8BaseRenderPage()});
 }
};

/* ---------- 4. Generic support-service record page (10 PRD roles share one renderer) ---------- */
const SUPPORT_REQMAP={navigation:['contact_type','barriers','plan','next_step'],anaesthesia:['assessment_date','asa_class','airway_assessment','anesthesia_plan','fitness_decision'],blood_bank:['assessment_date','blood_group','antibody_screen','crossmatch_status','availability_status'],stoma_wound:['assessment_date','wound_status','drain_status','stoma_status','plan'],nutrition:['assessment_date','weight_kg','intake_assessment','nutrition_diagnosis','intervention_plan','monitoring_plan'],psychosocial:['assessment_date','distress_score','risk_level','intervention_plan','care_team_summary'],palliative:['assessment_date','symptom_summary','goals_of_care_status','plan'],clinical_trial:['trial_id','protocol_version','screening_status','consent_status'],him:['operation_type','reason','status'],pathology_processing:['accession_id','specimen_received_at','grossing_status','blocks_slides_status','ready_for_pathologist'],rt_planning:['plan_id','planning_system','plan_status']};
function pc8Label(k){return k.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())}
function pc8SupportField(field,current){
 const id='sup_'+field;
 if(field==='risk_level')return sel('Risk level',id,current||'Low',['Low','Moderate','High','Critical']);
 if(field==='goals_of_care_status')return sel('Goals of care status',id,current||'Not yet discussed',['Not yet discussed','In discussion','Established — curative-consistent','Established — comfort-focused']);
 if(field==='crossmatch_status')return sel('Crossmatch status',id,current||'Not requested',['Not requested','Pending','Compatible','Incompatible']);
 if(field==='availability_status')return sel('Availability status',id,current||'Not required',['Not required','Requested','Available','Not available']);
 if(field==='screening_status')return sel('Screening status',id,current||'Not screened',['Not screened','Screening in progress','Eligible','Not eligible','Enrolled']);
 if(field==='consent_status')return sel('Consent status',id,current||'Not obtained',['Not obtained','Pending','Signed','Declined']);
 if(field==='ready_for_pathologist')return sel('Ready for pathologist',id,current?'Yes':'No',['No','Yes']);
 if(field.indexOf('date')>=0)return fld(pc8Label(field),id,current||today(),'date');
 if(field==='distress_score'||field==='weight_kg')return fld(pc8Label(field),id,current!=null?current:'','number');
 if(['plan','intervention_plan','monitoring_plan','care_team_summary','symptom_summary','airway_assessment','anesthesia_plan','intake_assessment','nutrition_diagnosis'].includes(field))return txt(pc8Label(field),id,current||'');
 return fld(pc8Label(field),id,current||'');
}
V.support=()=>{
 const typ=SUPPORT_TYPE_BY_ROLE[S.role];
 if(!typ)return title('Support Service','No support-service record type is configured for this role.');
 const rec=one(typ),d=(rec&&rec.data)||{},fields=SUPPORT_REQMAP[typ]||[];
 const openReferral=PC8_TASKS.find(t=>t.task_type==='Support service referral'&&['Open','Acknowledged'].includes(t.status)&&t.patient_id===S.pid);
 return title(SUPPORT_LABEL[typ]||typ,'Role-owned specialist record. Signed content is consumed by the referring team with provenance; upstream facts are never re-entered here.')
 +(openReferral?`<div class="alert blue">Referred by <b>${esc((openReferral.data&&openReferral.data.referrer_role)||'—')}</b>: ${esc(openReferral.reason||'')}</div>`:'')
 +(rec?card('Current record',kv('Status',badge(rec.status,statusColor(rec.status)))+kv('Version',esc(rec.version))+(rec.status==='Signed'?kv('Signed by',esc((d.signed_by&&d.signed_by.name)||'')):'')+`<pre class="source-json">${esc(JSON.stringify(d,null,2))}</pre>`):'<div class="alert amber">No record yet — complete and save/sign below.</div>')
 +card('Assessment / record',fields.map(f=>pc8SupportField(f,d[f])).join('')+(rec&&rec.status==='Signed'?fld('Amendment reason (required to amend a signed record)','sup_amend_reason',''):'')+`<div class="row top-gap"><button class="btn" data-act="support-save" data-type="${typ}">Save Draft</button><button class="btn primary" data-act="support-sign" data-type="${typ}">Sign</button></div>`);
};

const REFERRAL_TARGETS=['Nurse Navigator','Dietitian / Nutrition','Psycho-Oncology','Palliative Care','Clinical Trials / Research','Stoma / Wound Nurse','Anaesthetist','Blood Bank / Transfusion','Health Information Management'];
const pc8BaseVSummary=V.summary;
V.summary=function(){
 let html=pc8BaseVSummary();
 if(['Medical Oncology','Surgical Oncology','Radiation Oncology','Nurse Navigator','Inpatient Oncology Clinician','Inpatient Oncology Nurse','Day Care / Infusion Nurse','Intake Nurse'].includes(S.role)){
  html+=card('Refer to Support Service',sel('Target service','refsvc_target',REFERRAL_TARGETS[0],REFERRAL_TARGETS)+txt('Reason for referral','refsvc_reason','')+sel('Priority','refsvc_priority','Routine',['Routine','High','Critical'])+`<button class="btn primary top-gap" data-act="refer-support-service">Send Referral</button>`);
 }
 return html;
};

/* ---------- 5. End-of-treatment / survivorship / surveillance / progression page ---------- */
V.survivorship=function(){
 const hist=data('treatment_history'),tc=one('treatment_completion'),sp=one('survivorship'),sv=data('surveillance');
 const completedEvents=(hist.episodes||[]).filter(x=>x.status==='Completed'&&['Systemic Therapy','Radiation Therapy','Surgery','Other Cancer-Directed Treatment'].includes(x.type));
 let html=title('Treatment Completion / Survivorship','End-of-treatment review → survivorship & surveillance plan → surveillance encounters → recurrence/progression confirmation. Each stage consumes the prior signed stage with provenance.');
 html+=card('Completed cancer-directed treatment history',`<div class="table-wrap"><table><thead><tr><th>Type</th><th>Date</th><th>Description</th><th>Recorded by</th></tr></thead><tbody>${completedEvents.map(x=>`<tr><td>${esc(x.type)}</td><td>${esc(x.date)}</td><td>${esc(x.description)}</td><td>${esc((x.recorded_by&&x.recorded_by.name)||'')}</td></tr>`).join('')||'<tr><td colspan="4">No completed treatment recorded yet.</td></tr>'}</tbody></table></div>`);
 if(['Medical Oncology','Surgical Oncology','Radiation Oncology'].includes(S.role)){
  html+=card('Record completed treatment',sel('Type','th_type','Systemic Therapy',['Systemic Therapy','Radiation Therapy','Surgery','Other Cancer-Directed Treatment'])+fld('Date','th_date',today(),'date')+txt('Description','th_desc','')+sel('Trigger End-of-Treatment Review','th_trigger','No',['No','Yes'])+`<button class="btn primary top-gap" data-act="record-treatment-history">Record</button>`);
  const d=(tc&&tc.data)||{};
  html+=card('End-of-Treatment Review / Cancer Treatment Summary',(tc?`<div class="mini muted">Status: ${badge(tc.status,statusColor(tc.status))}</div>`:'')+fld('Completion date','tc_date',d.completion_date||today(),'date')+txt('Diagnosis at completion','tc_dx',d.diagnosis_at_completion||'')+txt('Treatment received','tc_tx',d.treatment_received||'')+sel('Current disease status','tc_status',d.current_disease_status||'No evidence of disease',['No evidence of disease','Stable disease','Partial response','Complete response'])+txt('Late-effect risks','tc_late',d.late_effect_risks||'')+txt('Follow-up recommendations','tc_followup',d.follow_up_recommendations||'')+`<div class="row top-gap"><button class="btn" data-act="tc-save">Save Draft</button><button class="btn primary" data-act="tc-sign">Sign End-of-Treatment Review</button></div>`);
 }
 if(S.role==='Nurse Navigator'){
  const d=(sp&&sp.data)||{};
  html+=card('Survivorship / Surveillance Plan',(sp?`<div class="mini muted">Status: ${badge(sp.status,statusColor(sp.status))}</div>`:'')+txt('Surveillance schedule','sp_sched',d.surveillance_schedule||'')+txt('Late-effect monitoring','sp_late',d.late_effect_monitoring||'')+txt('Health promotion','sp_health',d.health_promotion||'')+txt('Red flags','sp_red',d.red_flags||'')+txt('Contact plan','sp_contact',d.contact_plan||'')+fld('Next surveillance date','sp_next','','date')+`<div class="row top-gap"><button class="btn" data-act="sp-save">Save Draft</button><button class="btn primary" data-act="sp-sign">Sign Survivorship Plan</button></div>`);
 }
 html+=card('Surveillance encounters',`<div class="table-wrap"><table><thead><tr><th>Date</th><th>Assessment</th><th>Disease status</th></tr></thead><tbody>${(sv.encounters||[]).map(x=>`<tr><td>${esc(x.date)}</td><td>${esc(x.assessment)}</td><td>${badge(x.disease_status,statusColor(x.disease_status))}</td></tr>`).join('')||'<tr><td colspan="3">No surveillance encounters recorded.</td></tr>'}</tbody></table></div>`);
 if(['Nurse Navigator','Medical Oncology','Radiation Oncology','Surgical Oncology'].includes(S.role)){
  html+=card('Record surveillance encounter',fld('Date','sv_date',today(),'date')+txt('Assessment','sv_assess','')+sel('Disease status','sv_status','No evidence of disease',['No evidence of disease','Stable','Suspected recurrence','Suspected progression'])+`<button class="btn primary top-gap" data-act="record-surveillance">Record Encounter</button>`);
 }
 if(S.role==='Medical Oncology'){
  html+=card('Confirm recurrence / progression',sel('Disease status','pg_status','No Recurrence / Stable',['No Recurrence / Stable','Confirmed Recurrence','Confirmed Progression'])+txt('Evidence summary','pg_evidence','')+`<button class="btn primary top-gap" data-act="confirm-progression">Confirm</button>`);
 }
 return html;
};

/* ---------- 6. MDT Coordinator → Chair sign-off — surfaced on top of the existing MDT page ---------- */
if(typeof V.mdt==='function'){
 const pc8BaseVMdt=V.mdt;
 V.mdt=function(){
  let html=pc8BaseVMdt();
  const m=one('mdt');
  if(S.role==='MDT Chair'){
   if(m&&m.status==='Pending Chair Approval'){
    html+=card('Chair Review',`<div class="alert blue">The MDT Coordinator submitted this recommendation for Chair review.</div>`+txt('Decision reason','chair_reason','')+`<div class="row top-gap"><button class="btn primary" data-act="mdt-chair-approve">Approve</button><button class="btn danger" data-act="mdt-chair-return">Return for Revision</button></div>`);
   }else{
    html+=card('Chair Review',`<div class="mini muted">No recommendation is currently awaiting Chair review (status: ${esc(m?m.status:'—')}).</div>`);
   }
  }
  return html;
 };
}

/* ---------- 7. Inpatient medication order / MAR — layered onto the existing IPD page ---------- */
if(typeof V.ipd==='function'){
 const pc8BaseVIpd=V.ipd;
 V.ipd=function(){
  let html=pc8BaseVIpd();
  if(['Inpatient Oncology Clinician','Inpatient Oncology Nurse'].includes(S.role)){
   const ipd=data('inpatient_care'),orders=ipd.medication_orders||[];
   html+=card('IPD Medication Orders / MAR',`<div class="table-wrap"><table><thead><tr><th>Medication</th><th>Dose</th><th>Route</th><th>Status</th><th></th></tr></thead><tbody>${orders.map(o=>`<tr><td>${esc(o.medication)}</td><td>${esc(o.dose)} ${esc(o.unit)}</td><td>${esc(o.route)}</td><td>${badge(o.status,statusColor(o.status))}</td><td>${o.status==='Active'&&S.role==='Inpatient Oncology Nurse'?`<button class="btn sm primary" data-act="ipd-mar-open" data-id="${esc(o.id)}">Administer</button>`:''}</td></tr>`).join('')||'<tr><td colspan="5">No inpatient medication orders yet.</td></tr>'}</tbody></table></div>`
   +(S.role==='Inpatient Oncology Clinician'?`<div class="top-gap">${fld('Medication','ipdmo_med','')}${fld('Dose','ipdmo_dose','','number')}${fld('Unit','ipdmo_unit','mg')}${sel('Route','ipdmo_route','IV',['IV','PO','IM','SQ','Other'])}${fld('Frequency','ipdmo_freq','Every 8 hours')}${fld('Indication','ipdmo_ind','')}<button class="btn primary top-gap" data-act="ipd-med-order">Order Medication</button></div>`:''));
  }
  return html;
 };
}

/* ---------- 8. handle() dispatch: fix the dead task buttons + wire every new action ---------- */
const pc8BaseHandle=handle;
handle=async function(el){
 const a=el.dataset.act;
 try{
  if(a==='tasks-refresh'){await pc8LoadTasks();renderPage();return}
  if(a==='task-source'){
   const t=PC8_TASKS.find(x=>x.id===el.dataset.id);
   const ctx=await api('/api/task-source?task='+encodeURIComponent(el.dataset.id));
   modal('Task Source & Provenance — '+(t?t.title:''),taskSourceHtml(ctx));
   return;
  }
  if(a==='task-perform'){
   closeModal();
   const t=PC8_TASKS.find(x=>x.id===el.dataset.id);
   S.page=(t&&TASK_PAGE[t.task_type])||'summary';localStorage.setItem('cca_v12_page',S.page);
   if(t&&t.patient_id&&t.patient_id!==S.pid){S.pid=t.patient_id;localStorage.setItem('cca_v12_pid',S.pid);await refresh()}
   else renderApp();
   return;
  }
  if(a==='task-ack'||a==='task-complete'||a==='task-escalate'){
   const op=a==='task-ack'?'acknowledge':a==='task-complete'?'complete':'escalate';
   await api('/api/task-action',{method:'POST',body:JSON.stringify({task_id:el.dataset.id,operation:op,reason:op==='escalate'?'Escalated from task worklist':''})});
   toast('Task '+op+'d');
   if(S.page==='tasks'){await pc8LoadTasks();renderPage()}else await refresh();
   return;
  }
  if(a==='refer-support-service'){await action('refer_support_service','',{target_role:val('refsvc_target'),reason:val('refsvc_reason'),priority:val('refsvc_priority')});toast('Referral sent');await refresh();return}
  if(a==='support-save'||a==='support-sign'){
   const typ=el.dataset.type,fields=SUPPORT_REQMAP[typ]||[];const payload={record_type:typ,sign:a==='support-sign'};
   fields.forEach(f=>{const v=val('sup_'+f);payload[f]=(f==='distress_score'||f==='weight_kg')?(v===''?null:Number(v)):(f==='ready_for_pathologist'?v==='Yes':v)});
   const ar=val('sup_amend_reason');if(ar)payload.amendment_reason=ar;
   await action('save_support_record','',payload);toast(a==='support-sign'?'Signed':'Saved');await refresh();return;
  }
  if(a==='record-treatment-history'){await action('record_treatment_history_event','',{type:val('th_type'),date:val('th_date'),status:'Completed',description:val('th_desc'),trigger_completion_review:val('th_trigger')==='Yes'});toast('Recorded');await refresh();return}
  if(a==='tc-save'||a==='tc-sign'){await action('save_treatment_completion','',{sign:a==='tc-sign',treatment_completed:true,completion_date:val('tc_date'),diagnosis_at_completion:val('tc_dx'),treatment_received:val('tc_tx'),current_disease_status:val('tc_status'),late_effect_risks:val('tc_late'),follow_up_recommendations:val('tc_followup')});toast(a==='tc-sign'?'Signed':'Saved');await refresh();return}
  if(a==='sp-save'||a==='sp-sign'){await action('save_survivorship_plan','',{sign:a==='sp-sign',surveillance_schedule:val('sp_sched'),late_effect_monitoring:val('sp_late'),health_promotion:val('sp_health'),red_flags:val('sp_red'),contact_plan:val('sp_contact'),next_surveillance_at:val('sp_next')});toast(a==='sp-sign'?'Signed':'Saved');await refresh();return}
  if(a==='record-surveillance'){await action('record_surveillance','',{date:val('sv_date'),assessment:val('sv_assess'),disease_status:val('sv_status')});toast('Recorded');await refresh();return}
  if(a==='confirm-progression'){await action('confirm_progression','',{disease_status:val('pg_status'),evidence_summary:val('pg_evidence')});toast('Confirmed');await refresh();return}
  if(a==='mdt-chair-approve'||a==='mdt-chair-return'){await action('mdt_chair_sign',id('mdt'),{decision:a==='mdt-chair-approve'?'Approve':'Return for revision',reason:val('chair_reason')});toast('Recorded');await refresh();return}
  if(a==='ipd-med-order'){await action('inpatient_med_order','',{medication:val('ipdmo_med'),dose:val('ipdmo_dose'),unit:val('ipdmo_unit'),route:val('ipdmo_route'),frequency:val('ipdmo_freq'),indication:val('ipdmo_ind')});toast('Order placed');await refresh();return}
  if(a==='ipd-mar-open'){
   modal('Administer IPD Medication',`${fld('Administration datetime','ipdmar_dt',new Date().toISOString().slice(0,16),'datetime-local')}${fld('Actual dose','ipdmar_dose','','number')}${fld('Variance reason (if different)','ipdmar_var','')}<button class="btn primary" id="ipdMarSave">Record Administration</button>`);
   $('#ipdMarSave').onclick=async()=>{try{await action('inpatient_mar','',{order_id:el.dataset.id,administration_datetime:val('ipdmar_dt'),actual_dose:val('ipdmar_dose'),variance_reason:val('ipdmar_var')});closeModal();toast('Administered');refresh()}catch(e2){toast(e2.message,true)}};
   return;
  }
 }catch(e){toast(e.message,true);return}
 return pc8BaseHandle(el);
};
})();
