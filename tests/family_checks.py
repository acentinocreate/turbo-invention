from pathlib import Path
import json,time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];results=[]
def check(name,ok,detail=''):
 results.append({'check':name,'passed':bool(ok),'detail':detail});print(('PASS ' if ok else 'FAIL ')+name+' '+detail,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1100},accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8080/index.html')
 page.evaluate('text=>window.fixtureLicense=text',(ROOT/'LICENSE').read_text())
 page.evaluate("""()=>{let p=Formaco.project;p.license=window.fixtureLicense;Object.values(p.components).forEach(c=>c.approved=true);p.decisions.approved=true;for(const s of p.styles.filter(s=>s.kind==='upright'&&(s.weight===300||s.weight===700)))for(const ch of p.characters)s.glyphs[ch]=Formaco.generate(ch,s)}""")
 check('Different weights change arches and stems',page.evaluate("""()=>{const [a,b]=[300,700].map(w=>Formaco.project.styles.find(s=>s.weight===w&&s.kind==='upright'));return JSON.stringify(a.glyphs.n.contours)!==JSON.stringify(b.glyphs.n.contours)&&JSON.stringify(a.glyphs.H.contours)!==JSON.stringify(b.glyphs.H.contours)}"""))
 # Explicit topology alignment is a tested geometric repair, not automatic designer approval.
 repair=page.evaluate("""()=>{const [a,b]=[300,700].map(w=>Formaco.project.styles.find(s=>s.weight===w&&s.kind==='upright'));let repaired=0,blocked=[];for(const ch of Formaco.project.characters){if(Formaco.compatible(a.glyphs[ch],b.glyphs[ch])){try{const [x,y]=Formaco.alignContours(a.glyphs[ch],b.glyphs[ch]);a.glyphs[ch].contours=x;b.glyphs[ch].contours=y;repaired++}catch(e){blocked.push(ch+': '+e.message)}}}for(const s of [a,b]){for(const ch of 'HOAnoag')s.glyphs[ch].status='approved';s.masterApproved=true}const r=Formaco.interpolateStyles('upright');for(const c of r.changes)Formaco.project.styles.find(s=>s.id===c.style).glyphs[c.char]=c.next;return {repaired,blocked,interpolated:r.changes.length,errors:r.errors}}""")
 check('Compatible-master interpolation executes',repair['interpolated']>100,json.dumps(repair))
 # Missing or topologically incompatible characters remain independent proposals, explicitly logged.
 fixture=page.evaluate("""()=>{const errors=[];for(const s of Formaco.project.styles){for(const ch of Formaco.project.characters)if(!s.glyphs[ch]){try{s.glyphs[ch]=Formaco.generate(ch,s)}catch(e){errors.push(s.name+'/'+ch+': '+e.message)}}s.kerning.AV=-60;}Formaco.render();return errors}""")
 check('All ten style fixtures generated',not fixture,str(fixture))
 check('Structural italic vs oblique',page.evaluate("""()=>{const p=Formaco.project,regular=p.styles.find(s=>s.id==='regular'),italic=p.styles.find(s=>s.id==='regular-italic');p.decisions.a='double';regular.glyphs.a=Formaco.generate('a',regular);Formaco.ACT.proposeItalic();const found=document.querySelectorAll('#modalBody .checklist label').length===7;return found&&italic.kind==='italic'&&italic.glyphs.a.contours.length>0}"""));page.click('#modalCancel')
 # Shared edit preservation of manual and approved overrides.
 check('Shared propagation identifies protected overrides',page.evaluate("""()=>{const s=Formaco.project.styles.find(s=>s.id==='regular');s.glyphs.A.status='approved';s.glyphs.B.status='manual';const a=JSON.stringify(s.glyphs.A);Formaco.ACT.propagate();return JSON.stringify(s.glyphs.A)===a&&!Array.from(document.querySelectorAll('#modalBody .checklist label')).some(l=>l.textContent.startsWith('A · Regular ·')||l.textContent.startsWith('B · Regular ·'))}"""));page.click('#modalCancel')
 check('Oblique is an actual shear of the upright',page.evaluate("""()=>{Formaco.setSelection('H','regular');const upright=Formaco.clone(Formaco.selectedStyle.glyphs.H);Formaco.ACT.oblique();const id=Formaco.selectedStyle.id,g=Formaco.selectedGlyph,t=Math.tan(12*Math.PI/180);const ok=Formaco.selectedStyle.kind==='oblique'&&g.contours.every((p,i)=>p.every((c,j)=>c.type==='Z'||(c.y===upright.contours[i][j].y&&c.x===Math.round(upright.contours[i][j].x+t*c.y))));Formaco.project.styles=Formaco.project.styles.filter(s=>s.id!==id);Formaco.setSelection('H','regular');return ok;}"""))
 check('Preview uses exported advance and kerning',page.evaluate("""()=>{const s=Formaco.selectedStyle,p=Formaco.project.preview,old=[p.tracking,p.mono];p.tracking=0;p.mono=false;const r=Formaco.specimenSvg(s,'AV',1000);p.tracking=old[0];p.mono=old[1];return r.positions[1].x-r.positions[0].x===s.glyphs.A.advance+s.kerning.AV;}"""))
 # Browser font loader and CSS style selection test, independent of app SVG preview.
 loaded=page.evaluate("""async()=>{const names=[];for(const s of Formaco.project.styles){const face=new FontFace('FormacoTest',Formaco.toWoff(Formaco.exportFont(s)),{weight:String(s.weight),style:s.kind==='italic'?'italic':'normal'});await face.load();document.fonts.add(face);names.push(s.id)}const canvas=document.createElement('canvas'),c=canvas.getContext('2d');c.font='400 1000px FormacoTest';const normal=c.measureText('H').width;c.font='italic 400 1000px FormacoTest';return {count:names.length,normal,italic:c.measureText('H').width}}""")
 check('Browser loads ten WOFF styles and selects italic',loaded['count']==10 and loaded['normal']!=loaded['italic'],json.dumps(loaded))
 page.evaluate("Object.values(Formaco.project.components).forEach(c=>c.approved=false);Formaco.project.decisions.approved=false;for(const s of Formaco.project.styles){s.masterApproved=false;for(const g of Object.values(s.glyphs))g.status='candidate'}")
 for id in page.evaluate('Formaco.project.styles.map(s=>s.id)'):
  binaries=page.evaluate("""id=>{const s=Formaco.project.styles.find(s=>s.id===id),otf=Formaco.exportFont(s);return {otf:Array.from(otf),woff:Array.from(Formaco.toWoff(otf))}}""",id)
  for ext,data in binaries.items():(ROOT/'examples'/f'FormacoStudy-{id}.{ext}').write_bytes(bytes(data))
 with page.expect_download() as info:page.evaluate('Formaco.ACT.familyZip()')
 dl=info.value;dl.save_as(ROOT/'examples'/'FormacoStudy-family.zip')
 import zipfile
 with zipfile.ZipFile(ROOT/'examples'/'FormacoStudy-family.zip') as z:check('Family ZIP contains fonts, project and README',len(z.namelist())==23 and 'LICENSE.txt' in z.namelist() and 'README.txt' in z.namelist() and 'project.json' in z.namelist())
 (ROOT/'examples'/'family-study.formaco.json').write_text(page.evaluate('JSON.stringify(Formaco.project,null,2)'))
 # Storage failure remains recoverable and does not prevent edits.
 page.evaluate("Storage.prototype.setItem=function(){throw new DOMException('Quota exceeded','QuotaExceededError')};Formaco.save()")
 page.wait_for_timeout(500);check('Storage failure warning',page.locator('#saveState').inner_text()=='Backup required')
 check('Edits remain usable after storage failure',page.evaluate("""()=>{Formaco.setSelection('H','regular');const r=Formaco.project.revision;Formaco.ACT.selectNextContour();Formaco.ACT.duplicate();return Formaco.project.revision===r+1}"""))
 # Bad autosave must survive untouched, with a raw recovery download.
 recovery=b.new_page();recovery.goto('http://127.0.0.1:8080/index.html');recovery.evaluate("localStorage.setItem('formaco.project.v1','{unreadable');");recovery.reload();recovery.wait_for_timeout(400)
 check('Unreadable autosave retained',recovery.evaluate("localStorage.getItem('formaco.project.v1') === '{unreadable'"))
 recovery.locator('summary').filter(has_text='Inspection').click()
 with recovery.expect_download() as info:recovery.click('[data-act=recovery]')
 info.value.save_as('/tmp/formaco-recovered-raw.json');check('Raw recovery download',Path('/tmp/formaco-recovered-raw.json').read_text()=='{unreadable')
 check('No family browser exceptions',not errors,str(errors))
 b.close()
(ROOT/'tests'/'family-results.json').write_text(json.dumps(results,indent=2))
if any(not r['passed'] for r in results):raise SystemExit(1)
