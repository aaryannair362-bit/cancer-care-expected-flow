/* CCA Cancer Care OS V12.2-PC1.3 — Structural Conformance Remediation.
   Scope: Register v1.1 Track-B Phase 1. No institutional clinical thresholds are invented here. */

const PC13_VERSION='V12.2-PC1.3';
function pc13ActiveToxicities(){return (data('toxicity').events||[]).filter(x=>!['Resolved','Resolved with sequelae'].includes(x.outcome));}
function pc13LatestResponse(){return (data('response').assessments||[]).at(-1)||{};}
function pc13History(){return data('treatment_history').episodes||[];}
function pc13DoseLedger(order){
  const infs=list('infusion'); let total=0,count=0;
  infs.forEach(inf=>(inf.data?.mar||[]).forEach(m=>{if(m.drug&&(m.actual_dose!=null)){total+=Number(m.actual_dose||0);count++}}));
  return {total,count};
}
function pc13ReadinessSummary(r){
  const d=r?.data||{},ev=d.protocol_evaluation||{},rr=ev.rule_results||[];
  const wanted=rr.filter(x=>/anc|platelet|hb|creatin|egfr|bilirubin|ast|alt|lvef|ecg|tox/i.test(`${x.field||''} ${x.category||''}`));
  return wanted.length?wanted.map(x=>`<div class="summary-line"><span>${esc(x.field||x.category||'Criterion')}</span><b>${pc12Maybe(x.current)} ${esc(x.unit||'')} • ${badge(x.status||'Review',statusColor(x.status))}</b></div>`).join(''):'<div class="muted">No structured readiness criteria available.</div>';
}
function pc13UnitSelect(label,id,current,vals){return sel(label,id,current||'', ['',...vals]);}
function pc13BpParts(d){const src=d.source_measurements||{};const m=String(d.bp||'').match(/(\d+)\s*\/\s*(\d+)/);return {sbp:src.sbp?.value??(m?m[1]:''),dbp:src.dbp?.value??(m?m[2]:''),unit:src.sbp?.unit||''}}

// --- Intake: explicit units + system-derived BMI/BSA ---
V.intake=()=>{
 const d=data('intake'),src=d.source_measurements||{},bp=pc13BpParts(d),legacy=!d.source_measurements;
 const tempVal=src.temp?.value??d.temp_c??'',weightVal=src.weight?.value??d.weight_kg??'',heightVal=src.height?.value??d.height_cm??'';
 return title('Vitals & Oncology Intake','Measured values require an explicit source unit. BMI and BSA are read-only system derivations.')+
 `${legacy?'<div class="alert amber"><b>Legacy demo measurement metadata:</b> this existing intake predates the explicit-unit contract. Re-enter measured values with source units before creating a new systemic order.</div>':''}`+
 `<div class="grid g2"><div class="card"><h3>Vitals / performance</h3><div class="grid g2">
 ${fld('Systolic BP','in_sbp',bp.sbp,'number')}${fld('Diastolic BP','in_dbp',bp.dbp,'number')}${pc13UnitSelect('BP unit','in_bp_unit',bp.unit,['mmHg'])}
 ${fld('Heart rate','in_hr',src.hr?.value??d.hr??'','number')}${pc13UnitSelect('Heart-rate unit','in_hr_unit',src.hr?.unit||'', ['/min'])}
 ${fld('Respiratory rate','in_rr',src.rr?.value??d.rr??'','number')}${pc13UnitSelect('Respiratory-rate unit','in_rr_unit',src.rr?.unit||'', ['/min'])}
 ${fld('Temperature','in_temp',tempVal,'number','step="0.1"')}${pc13UnitSelect('Temperature unit','in_temp_unit',src.temp?.unit||'', ['°C','°F'])}
 ${fld('SpO₂','in_spo2',src.spo2?.value??d.spo2??'','number')}${pc13UnitSelect('SpO₂ unit','in_spo2_unit',src.spo2?.unit||'', ['%'])}
 ${fld('Weight','in_w',weightVal,'number','step="0.1"')}${pc13UnitSelect('Weight unit','in_w_unit',src.weight?.unit||'', ['kg','lb'])}
 ${fld('Height','in_h',heightVal,'number','step="0.1"')}${pc13UnitSelect('Height unit','in_h_unit',src.height?.unit||'', ['cm','in'])}
 ${sel('ECOG','in_ecog',d.ecog||'1',['0','1','2','3','4'])}${sel('Karnofsky','in_kps',d.kps||'90',['100','90','80','70','60','50','40','30','20','10','0'])}</div>
 <div class="summary-line"><span>BMI</span><b>${esc(d.bmi??'Calculated on save')}</b></div><div class="summary-line"><span>BSA</span><b>${esc(d.bsa_m2?`${d.bsa_m2} m²`:'Calculated on save')}</b></div><div class="mini">${esc(d.bsa_formula||'Mosteller formula is displayed after save.')}</div></div>
 <div class="card"><h3>History / nursing assessment</h3>${sel('Pain instrument','in_pain_inst',d.pain_instrument||'Numeric Rating Scale 0–10',['Numeric Rating Scale 0–10','Visual Analogue Scale 0–10','Faces scale'])}${fld('Pain score','in_pain',d.pain_score??0,'number','min="0" max="10"')}${fld('Pain site','in_painsite',d.pain_site||'')}${sel('Fall-risk setting','in_fallset',d.fall_risk_setting||'OPD',['OPD','IPD'])}${fld('Fall-risk score','in_fallscore',d.fall_risk_score??0,'number')}${sel('Fall-risk level','in_falllevel',d.fall_risk_level||'Low',['Low','Moderate','High'])}${txt('Past medical history','in_pmh',d.past_medical||'')}${txt('Past surgical history','in_psh',d.past_surgical||'')}${txt('Family / social / reproductive context','in_hist',[d.family_history,d.social_history,d.hormonal_history,d.reproductive_history].filter(Boolean).join('\n'))}<button class="btn primary" data-act="save-intake">Save Measured Intake</button></div></div>`;
};

// --- Pharmacy: expose independent verification evidence, toxicity/reactions, cumulative administration context ---
V.pharmacy=()=>{
 const ph=one('pharmacy'),d=ph?.data||{},o=one('treatment_order'),ready=one('readiness'),lab=data('lab'),tox=pc13ActiveToxicities(),ledger=pc13DoseLedger(o),inf=one('infusion');
 if(!ph)return title('Oncology Pharmacy')+'No pharmacy record';
 const ps=o?.data?.patient_snapshot||{},status=ph.status||'Verification Pending';
 return title('Oncology Pharmacy','Independent verification requires the same patient-specific evidence that drove the signed order and readiness decision.')+
 `<div class="workflow-ribbon">${['Verification Pending','Query Raised','Verified','Prepared','Dispensed'].map(s=>`<span class="${pc12Norm(status).includes(pc12Norm(s).split(' ')[0])?'active':''}">${esc(s)}</span>`).join('')}</div>
 <div class="grid g4">${card('Signed order',kv('Order',esc(o?.data?.order_no||'—'))+kv('Regimen / version',esc(`${o?.data?.regimen||'—'} • ${o?.data?.protocol_version||'—'}`))+kv('Cycle / day',esc(o?`C${o.data.cycle}D${o.data.day}`:'—'))+kv('Prescriber',esc(o?.data?.signed_by?.name||o?.data?.signed_by?.role||'—')))}
 ${card('Dosing snapshot',kv('Weight',esc(ps.weight_kg!=null?`${ps.weight_kg} kg`:'—'))+kv('Height',esc(ps.height_cm!=null?`${ps.height_cm} cm`:'—'))+kv('BSA',esc(ps.bsa_m2!=null?`${ps.bsa_m2} m²`:'—'))+kv('Measured',fmt(ps.measured_at))+kv('Assessor',esc(ps.assessor?.name||ps.assessor?.role||'—')))}
 ${card('Signed readiness',kv('Status',badge(ready?.status||'Missing',statusColor(ready?.status)))+kv('Decision',esc(ready?.data?.decision||'—'))+kv('Signed by',esc(ready?.data?.signed_by?.name||ready?.data?.signed_by?.role||'—'))+kv('Signed',fmt(ready?.data?.signed_at)))}
 ${card('Exposure / toxicity',kv('Administered-dose entries',esc(ledger.count))+kv('Active toxicities',esc(tox.length))+kv('Last administration state',badge(inf?.status||'None',statusColor(inf?.status)))+kv('Cumulative-limit context',esc((o?.data?.items||[]).some(x=>x.cumulative_limit)?'Configured per item':'No configured limit in current order')))}</div><br>
 <div class="ux-two"><div>${pc12Panel('Readiness evidence visible to Pharmacy',pc13ReadinessSummary(ready))}</div><div>${pc12Panel('Relevant active toxicity / reactions',tox.length?tox.slice(-6).map(x=>`<div class="summary-line"><span>${esc(x.term||x.toxicity||x.name||'Toxicity')}</span><b>${esc(x.grade?`Grade ${x.grade}`:x.severity||'Active')} • ${esc(x.outcome||'Ongoing')}</b></div>`).join(''):'<div class="muted">No active toxicity recorded.</div>')}</div></div>
 ${pc12Panel('Clinical verification & preparation',`<div class="table-wrap"><table><thead><tr><th>Drug</th><th>Protocol → calculated → ordered</th><th>Route / diluent</th><th>Preparation volume</th><th>Batch / expiry</th><th>Compatibility / stability / BUD</th></tr></thead><tbody>${(d.items||[]).map(i=>`<tr><td><b>${esc(i.drug)}</b></td><td>${pc12Maybe(i.protocol_dose)} → ${pc12Maybe(i.calculated_dose)} → <b>${pc12Maybe(i.ordered_dose)} ${pc12Maybe(i.ordered_unit)}</b></td><td>${esc(i.route||'—')} • ${esc(i.diluent||'—')}</td><td>${i.actual_volume_ml!=null?`${esc(i.actual_volume_ml)} ${esc(i.actual_volume_unit||'mL')}`:'Pending'}</td><td>${esc(i.batch||'—')} • ${esc(i.expiry||'—')}</td><td>${esc(i.compatibility_status||'Not verified')}<div class="mini">${esc(i.stability_reference||'Stability not verified')} • use before ${esc(i.beyond_use_at||'—')}</div></td></tr>`).join('')}</tbody></table></div>`)}`+
 `<div class="action-bar"><button class="btn" data-act="pharm-query">Raise Query</button><button class="btn primary" data-act="pharm-verify">Verify</button><button class="btn" data-act="pharm-prepare">Prepare</button><button class="btn primary" data-act="pharm-release">Final Check & Dispense</button></div>`;
};

// --- Day Care: order calculation provenance + prior reaction/toxicity context ---
V.daycare=()=>{
 const inf=one('infusion'),o=one('treatment_order'),ph=one('pharmacy'),ready=one('readiness'),tox=pc13ActiveToxicities(),mar=inf?.data?.mar||[],ps=o?.data?.patient_snapshot||{};
 return title('Day Care / Infusion','Treatment-day workspace with signed dosing snapshot, readiness, prior reactions, ordered sequence and actual MAR.')+
 `<div class="stat-grid">${pc12Stat('Order',o?.data?.order_no||'—')}${pc12Stat('Pharmacy',badge(ph?.status||'Pending',statusColor(ph?.status)))}${pc12Stat('Treatment day',badge(inf?.status||'Not started',statusColor(inf?.status)))}${pc12Stat('MAR completed',`${mar.length}/${o?.data?.items?.length||0}`)}</div>
 <div class="ux-two"><div>${pc12Panel('Signed order dosing snapshot',`<div class="summary-line"><span>Weight</span><b>${esc(ps.weight_kg??'—')} kg</b></div><div class="summary-line"><span>Height</span><b>${esc(ps.height_cm??'—')} cm</b></div><div class="summary-line"><span>BSA</span><b>${esc(ps.bsa_m2??'—')} m²</b></div><div class="summary-line"><span>Measurement</span><b>${fmt(ps.measured_at)} • ${esc(ps.assessor?.name||ps.assessor?.role||'—')}</b></div><div class="mini">${esc(ps.bsa_formula||'')}</div>`)}</div>
 <div>${pc12Panel('Readiness / prior treatment alerts',`<div class="summary-line"><span>Readiness</span><b>${badge(ready?.data?.decision||ready?.status||'Missing',statusColor(ready?.status))}</b></div>${tox.length?tox.slice(-5).map(x=>`<div class="summary-line"><span>${esc(x.term||x.toxicity||'Active toxicity')}</span><b>${esc(x.grade?`Grade ${x.grade}`:x.severity||'Active')}</b></div>`).join(''):'<div class="muted">No active toxicity / reaction alert.</div>'}`)}</div></div>
 ${o?pc1TreatmentSequence(o):''}<br>${pc12Panel('Medication Administration Record',`<div class="table-wrap"><table><thead><tr><th>Seq</th><th>Medication</th><th>Ordered</th><th>Actual</th><th>Actual rate</th><th>Time</th><th>Status</th><th>Reaction / intervention</th></tr></thead><tbody>${mar.map(x=>`<tr><td>${esc(x.sequence)}</td><td><b>${esc(x.drug)}</b></td><td>${pc12Maybe(x.ordered_dose)} ${pc12Maybe(x.ordered_unit)}</td><td>${pc12Maybe(x.actual_dose)} ${pc12Maybe(x.actual_dose_unit||x.unit)}</td><td>${x.actual_rate!=null?`${esc(x.actual_rate)} ${esc(x.actual_rate_unit||'')}`:'—'}</td><td>${esc(x.start_time||'—')} → ${esc(x.end_time||'—')}</td><td>${badge(x.completion_status,statusColor(x.completion_status))}</td><td>${esc(x.reaction||'None')}<div class="mini">${esc(x.intervention||x.variance_note||'')}</div></td></tr>`).join('')||'<tr><td colspan="8">No medication administered.</td></tr>'}</tbody></table></div>`)}`+
 `<div class="action-bar"><button class="btn primary" data-act="start-infusion">Pre-check & Start</button><button class="btn" data-act="admin-next">Administer Next</button><button class="btn danger" data-act="pc12-reaction">Record Infusion Reaction</button><button class="btn primary" data-act="complete-infusion">Complete Treatment Day</button></div>`;
};

// --- MDT: prior treatment, toxicity and response visible before recommendation ---
const pc13BaseMDT=V.mdt;
V.mdt=()=>{
 const m=one('mdt'),d=m?.data||data('mdt'),dx=data('diagnosis'),path=data('pathology'),hist=pc13History(),tox=pc13ActiveToxicities(),resp=pc13LatestResponse(),canPlan=(m?.status==='MDT Recommended'||m?.status==='Final');
 return pc12Page('MDT / Tumour Board','Current disease state plus prior treatment, toxicity and response are visible before multidisciplinary recommendation.',`<div class="ux-two"><div>${pc12Panel('Case for discussion',`<div class="summary-line"><span>Diagnosis</span><b>${esc(dx.cancer_type||'—')}</b></div><div class="summary-line"><span>Stage</span><b>${esc(dx.stage_group||'—')}</b></div><div class="summary-line"><span>Histology</span><b>${esc(dx.histology||path.histology||'—')}</b></div><div class="summary-line"><span>Performance</span><b>${esc(data('intake').ecog?`ECOG ${data('intake').ecog}`:'—')}</b></div>`)}</div><div>${pc12Panel('Prior treatment / response / toxicity',`<div class="summary-line"><span>Prior treatment events</span><b>${esc(hist.length)}</b></div><div class="summary-line"><span>Latest response</span><b>${esc(resp.response_category||'Not assessed')}</b></div><div class="summary-line"><span>Active toxicities</span><b>${esc(tox.length)}</b></div>${hist.slice(-4).map(x=>`<div class="mini">${esc(x.type||'Treatment')} • ${esc(x.status||'')} • ${esc(x.date||'')}</div>`).join('')}`)}</div></div>
 ${pc12Panel('MDT decision',`<div class="decision-box"><span>Recommendation</span><b>${esc(d.recommendation||'Awaiting final recommendation')}</b></div><div class="summary-line"><span>Intent</span><b>${esc(d.intent||'—')}</b></div><div class="summary-line"><span>Consensus</span><b>${esc(d.final_consensus||'—')}</b></div><div class="summary-line"><span>Status</span><b>${badge(m?.status||'Draft',statusColor(m?.status))}</b></div>`)}`+
 `${canPlan?`<div class="callout-action"><div><b>Create the treatment plan from this MDT</b><span>Choose only the required modalities and named clinicians.</span></div><button class="btn primary" data-act="pc12-plan-builder">Build Multidisciplinary Plan</button></div>`:''}`,(S.role==='MDT Coordinator'?`<button class="btn" data-act="edit-mdt">Edit Case</button><button class="btn primary" data-act="finalize-mdt">Finalize Recommendation</button>`:''));
};

// --- Pathology: cancer episode and prior context ---
V.pathology=()=>{
 const d=data('pathology'),dx=data('diagnosis'),hist=pc13History(),eps=list('cancer_episode');
 return title('Pathology / Molecular','Specimen reporting with cancer-episode, diagnosis and prior pathology/treatment context.',S.role==='Pathology'?'<button class="btn primary" data-act="edit-pathology">Enter / Finalize Pathology</button>':'')+
 `<div class="ux-two"><div>${pc12Panel('Cancer context',`<div class="summary-line"><span>Episode</span><b>${esc(dx.episode_id||eps.at(-1)?.id||'—')}</b></div><div class="summary-line"><span>Diagnosis</span><b>${esc(dx.cancer_type||'—')}</b></div><div class="summary-line"><span>Primary site</span><b>${esc(dx.primary_site||'—')}</b></div><div class="summary-line"><span>Histology</span><b>${esc(dx.histology||'—')}</b></div>`)}</div><div>${pc12Panel('Prior oncologic context',`<div class="summary-line"><span>Prior treatment events</span><b>${esc(hist.length)}</b></div><div class="summary-line"><span>Biomarkers</span><b>${esc((dx.biomarkers||[]).map(x=>`${x.name}: ${x.value}`).join(', ')||[dx.er,dx.pr,dx.her2].filter(Boolean).join(' • ')||'—')}</b></div>`)}</div></div>${pc12Panel('Current pathology',Object.entries(d).filter(([k])=>!['signed_at'].includes(k)).map(([k,v])=>`<div class="summary-line"><span>${esc(k.replaceAll('_',' '))}</span><b>${esc(reportValue(v))}</b></div>`).join('')||'<div class="muted">No pathology entered.</div>')}`;
};

// --- RO/SO patient summary: show performance and active toxicity now that role permissions allow it ---
const pc13BaseSummary=V.summary;
V.summary=()=>{
 const base=pc13BaseSummary(),int=data('intake'),tox=pc13ActiveToxicities();
 if(!['Radiation Oncology','Surgical Oncology'].includes(S.role))return base;
 const context=`<div class="alert blue"><b>Current treatment fitness:</b> ECOG ${esc(int.ecog??'—')} • KPS ${esc(int.kps??'—')} • active toxicity events ${esc(tox.length)}${tox.length?` • ${esc(tox.slice(-3).map(x=>`${x.term||x.toxicity||'toxicity'} ${x.grade?`G${x.grade}`:''}`).join(' | '))}`:''}</div>`;
 return base.replace('<div class="patient-banner">',context+'<div class="patient-banner">');
};

// --- RT role-specific execution context ---
const pc13BaseRadiation=V.radiation;
V.radiation=()=>{
 const base=pc13BaseRadiation(),x=one('radiation'),d=x?.data||{},rx=d.prescription||{},pl=d.planning||{},fr=d.fractions||[],del=fr.filter(z=>z.status==='Delivered'),next=Math.min(del.length+1,Number(rx.fractions||0)||1);
 let roleCard='';
 if(S.role==='Radiation Technologist')roleCard=`<div class="alert blue"><b>Today's delivery context:</b> plan ${esc(pl.plan_version||'Not versioned')} • fraction ${esc(next)} of ${esc(rx.fractions||'—')} • planned ${esc(rx.dose_per_fraction_gy||'—')} Gy • IGRT ${esc(rx.image_guidance||'Not configured')} • RO approval ${esc(pl.physician_final_approval||'Pending')} • Physics ${esc(pl.physics_qa||'Pending')}</div>`;
 if(S.role==='Radiation Physicist')roleCard=`<div class="alert blue"><b>Plan-version approval context:</b> current plan ${esc(pl.plan_version||'Not versioned')} • Physics ${esc(pl.physics_qa||'Pending')} • RO final approval ${esc(pl.physician_final_approval||'Pending')} ${pl.physician_approval_at?'• '+fmt(pl.physician_approval_at):''}</div>`;
 return roleCard+base;
};

// --- Surgical role context ---
const pc13BaseSurgery=V.surgery;
V.surgery=()=>{
 const base=pc13BaseSurgery(),int=data('intake'),tox=pc13ActiveToxicities(),hist=pc13History();
 if(!['Surgical Oncology','Surgical Nurse'].includes(S.role))return base;
 return `<div class="alert blue"><b>Peri-operative oncology context:</b> ECOG ${esc(int.ecog??'—')} • active toxicity ${esc(tox.length)} • prior treatment events ${esc(hist.length)}</div>`+base;
};

// --- Action overrides for explicit intake/MAR units and Pharmacy structural checks ---
const pc13BaseHandle=handle;
handle=async function(el){
 const a=el.dataset.act;
 try{
  if(a==='save-intake'){
   const ids=['in_bp_unit','in_hr_unit','in_rr_unit','in_temp_unit','in_spo2_unit','in_w_unit','in_h_unit'];
   if(ids.some(x=>!val(x))){toast('Select an explicit unit for every measured intake value',true);return}
   await action('save_intake',id('intake'),{sbp:num('in_sbp'),dbp:num('in_dbp'),hr:num('in_hr'),rr:num('in_rr'),temp:num('in_temp'),spo2:num('in_spo2'),weight:num('in_w'),height:num('in_h'),units:{bp:val('in_bp_unit'),hr:val('in_hr_unit'),rr:val('in_rr_unit'),temp:val('in_temp_unit'),spo2:val('in_spo2_unit'),weight:val('in_w_unit'),height:val('in_h_unit')},ecog:val('in_ecog'),kps:val('in_kps'),pain_instrument:val('in_pain_inst'),pain_score:num('in_pain'),pain_site:val('in_painsite'),fall_risk_setting:val('in_fallset'),fall_risk_score:num('in_fallscore'),fall_risk_level:val('in_falllevel'),past_medical:val('in_pmh'),past_surgical:val('in_psh'),social_history:val('in_hist'),complete:true});toast('Measured intake saved; canonical units and BSA derived by server');await refresh();return;
  }
  if(a==='pharm-prepare'){
   const ph=one('pharmacy'),fm=S.formulary?.items?.filter(x=>x.status==='Active')||data('formulary').items||[],qa=!pc1ClinicianMode();
   const fields=(ph.data.items||[]).map((x,i)=>{const fi=fm.find(f=>f.drug===x.drug),forms=fi?.formulations||[];const bud=new Date(Date.now()+4*3600e3).toISOString().slice(0,16);return `<div class="card"><b>${esc(x.sequence)}. ${esc(x.drug)}</b><div class="mini">Signed order: ${esc(x.ordered_dose)} ${esc(x.ordered_unit)} • ${esc(x.route)} • ${esc(x.diluent||'')} ${esc(x.volume_ml||'')} mL</div><div class="grid g2">${sel('Formulation / strength','p13_form_'+i,forms[0]?.label||'',forms.map(f=>f.label))}${fld('Batch / lot','p13_batch_'+i,'QA-'+String(i+1).padStart(2,'0'))}${fld('Expiry','p13_exp_'+i,new Date(Date.now()+60*864e5).toISOString().slice(0,10),'date')}${fld('Actual measured volume','p13_vol_'+i,x.volume_ml||0,'number','step="0.1"')}${pc13UnitSelect('Measured volume unit','p13_volu_'+i,'',['mL'])}${sel('Compatibility decision','p13_comp_'+i,qa?'Compatible':'',['','Compatible','Not applicable'])}${fld('Stability reference','p13_stab_'+i,qa?'Synthetic QA stability reference — NOT CLINICAL':'')}${fld('Beyond-use / use-before','p13_bud_'+i,qa?bud:'','datetime-local')}${fld('Storage condition','p13_store_'+i,qa?'Synthetic QA storage condition — NOT CLINICAL':'')}${sel('Light protection','p13_light_'+i,qa?'Not required':'',['','Required','Not required'])}${fld('Filter requirement','p13_filter_'+i,qa?'Synthetic QA filter status — NOT CLINICAL':'')}${fld('Container / device','p13_container_'+i,qa?'Synthetic QA container — NOT CLINICAL':'')}${fld('Prepared by','p13_by_'+i,S.meta?.actor?.name||S.role,'text','readonly')}</div></div>`}).join('');
   modal('Pharmacy Preparation — governed handling data',`${pc1ClinicianMode()?'<div class="alert amber"><b>CCA Pharmacy content is not configured.</b> To complete a simulated preparation, switch to Product Test Mode. Clinician Review Mode will not invent compatibility/stability/BUD values.</div>':'<div class="alert amber"><b>Synthetic QA handling values only.</b> These exist solely to test workflow enforcement and are not clinical guidance.</div>'}${fields}<button class="btn primary" id="p13PrepSave">Complete Preparation</button>`);
   $('#p13PrepSave').onclick=async()=>{const items=(ph.data.items||[]).map((x,i)=>{const fi=fm.find(f=>f.drug===x.drug),form=(fi?.formulations||[]).find(f=>f.label===val('p13_form_'+i))||{};return {...x,formulation:val('p13_form_'+i),formulation_strength_mg:form.strength_mg||0,batch:val('p13_batch_'+i),expiry:val('p13_exp_'+i),prepared_by:val('p13_by_'+i),actual_volume_ml:num('p13_vol_'+i),actual_volume_unit:val('p13_volu_'+i),compatibility_status:val('p13_comp_'+i),stability_reference:val('p13_stab_'+i),beyond_use_at:val('p13_bud_'+i),storage_condition:val('p13_store_'+i),light_protection:val('p13_light_'+i),filter_requirement:val('p13_filter_'+i),container_requirement:val('p13_container_'+i),waste:'0',clinical_content_status:qa?'Synthetic QA':'CCA Approved'}});await action('pharmacy_prepare',ph.id,{items,preparation_note:qa?'Synthetic QA preparation simulation — not clinical guidance':'CCA-approved Pharmacy preparation'});closeModal();toast('Preparation record completed against required structural fields');await refresh()};return;
  }
  if(a==='admin-next'){
   const inf=one('infusion'),o=one('treatment_order'),done=new Set((inf?.data?.mar||[]).map(x=>x.item_id)),it=o?.data?.items?.find(x=>!done.has(x.item_id));if(!it){toast('All ordered items already have MAR entries',true);return}
   const isIV=it.route==='IV'||Number(it.rate_ml_hr||0)>0;
   modal('MAR — '+it.drug,`${fld('Sequence position','p13_seq',`${it.sequence} — ${it.drug}`,'text','readonly')}${fld('Ordered dose','p13_ord',`${it.ordered_dose} ${it.ordered_unit}`,'text','readonly')}${fld('Actual administered dose','p13_dose',it.ordered_dose,'number','step="0.01"')}${pc13UnitSelect('Actual dose unit','p13_dose_u','',[it.ordered_unit])}${isIV?`${fld('Actual rate','p13_rate',it.rate_ml_hr||0,'number','step="0.01"')}${pc13UnitSelect('Actual rate unit','p13_rate_u','',['mL/h'])}`:''}${fld('Access / site','p13_access',inf.data.access||'')}${fld('Start time','p13_start',new Date().toTimeString().slice(0,5),'time')}${fld('End time','p13_end',new Date(Date.now()+20*60000).toTimeString().slice(0,5),'time')}${sel('Completion status','p13_status','Administered',['Administered','Partially Administered','Held','Stopped'])}${sel('Reaction','p13_rxn','None',['None','Flushing','Rash','Hypotension','Tachycardia','Chest pain','Dyspnea','Allergic','Other'])}${txt('Intervention / variance reason','p13_note','')}${fld('Independent chairside verifier','p13_verifier','Oncology RN B')}<button class="btn primary" id="p13MarSave">Record MAR Entry</button>`);
   $('#p13MarSave').onclick=async()=>{if(!val('p13_dose_u')||(isIV&&!val('p13_rate_u'))){toast('Select explicit dose/rate units',true);return}const ant=['Antineoplastic','Targeted Therapy'].includes(it.group);await action('administer_item',inf.id,{record:{item_id:it.item_id,actual_dose:num('p13_dose'),actual_dose_unit:val('p13_dose_u'),access:val('p13_access'),start_time:val('p13_start'),end_time:val('p13_end'),actual_rate:isIV?num('p13_rate'):0,actual_rate_unit:isIV?val('p13_rate_u'):'',completion_status:val('p13_status'),reaction:val('p13_rxn'),intervention:val('p13_note'),variance_note:val('p13_note'),chairside_verification:ant?{verified_by:val('p13_verifier'),checks:Object.fromEntries(['drug','dose','volume_diluent','route','rate','expiry','physical_integrity','sequence','pump_settings'].map(k=>[k,true]))}:undefined}});closeModal();await refresh()};return;
  }
  return await pc13BaseHandle(el);
 }catch(e){toast(e.message||String(e),true);}
};

// Update navigation wording without inventing a new institutional role.
const pc13BaseBuildNav=pc12BuildNav;
pc12BuildNav=function(){pc13BaseBuildNav();if(S.role==='Nurse Navigator'){const n=[...document.querySelectorAll('.navbtn')].find(x=>x.dataset.page==='intake');if(n)n.textContent='Vitals & Intake (Intake Nurse workflow)'}};
