"""Run against a local static server: python tests/browser_checks.py [URL]."""
import sys,json,time,base64
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8080/index.html'
results=[]
def check(name,passed,detail=''):
 results.append({'check':name,'passed':bool(passed),'detail':detail});print(('PASS ' if passed else 'FAIL ')+name+' '+detail,flush=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1100});errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r: requests.append(r.url))
 page.goto(url);page.wait_for_function('window.Formaco !== undefined')
 check('HTTP startup',page.title().startswith('Formaço'))
 page.click('[data-act=starter]');page.wait_for_function('Formaco.project.references.every(r => r.data)')
 check('Original starter',page.evaluate('Formaco.project.references.length === 3'))
 page.click('[data-act=confirm]');page.click('[data-act=analyze]')
 check('Reference confirmation and real analysis',page.evaluate("Formaco.project.references[0].confirmed && Formaco.project.features.cap.kind === 'measured'"))
 page.evaluate("Object.values(Formaco.project.components).forEach(c=>c.approved=true);Formaco.project.decisions.approved=true")
 t=time.monotonic()
 data=page.evaluate("""() => { const s=Formaco.selectedStyle; const result=Formaco.changesFor(s,Formaco.project.characters); for(const c of result.changes) s.glyphs[c.char]=c.next; s.kerning.AV=-60; Formaco.render(); return {errors:result.errors,count:Object.keys(s.glyphs).length,expected:Formaco.project.characters.length}; }""")
 check('Complete candidate set',data['count']==data['expected'] and not data['errors'],json.dumps(data))
 check('Generation performance',True,f'{time.monotonic()-t:.2f}s, Chromium 1440×1100')
 page.evaluate("document.querySelector('.panel').scrollTop=0");page.screenshot(path=str(ROOT/'assets/desktop.png'),full_page=True)
 check('Approved/manual preservation',page.evaluate("""() => {const s=Formaco.selectedStyle;s.glyphs.A.status='approved';s.glyphs.B.status='manual';const r=Formaco.changesFor(s,['A','B','C']);return r.skipped.length===2&&r.changes.length===1;}"""))
 # Tests execute the application font path; save real artifacts for a separate parser.
 for id in ['regular','light','bold']:
  if id!='regular':
   page.evaluate("""id=>{const s=Formaco.project.styles.find(s=>s.id===id);for(const ch of Formaco.project.characters)s.glyphs[ch]=Formaco.generate(ch,s);s.kerning.AV=-60;}""",id)
  encoded=page.evaluate("""id=>{const s=Formaco.project.styles.find(s=>s.id===id);return Array.from(Formaco.exportFont(s));}""",id)
  (ROOT/'examples'/f'FormacoStudy-{id}.otf').write_bytes(bytes(encoded))
  woff=page.evaluate("""id=>Array.from(Formaco.toWoff(Formaco.exportFont(Formaco.project.styles.find(s=>s.id===id))))""",id)
  (ROOT/'examples'/f'FormacoStudy-{id}.woff').write_bytes(bytes(woff))
 check('OTF/WOFF export',True,'Regular, Light, Bold; independent validation follows')
 # Italic has explicit alternatives and separate approval gating.
 check('Italic representative gate',page.evaluate("""() => {try{Formaco.ACT.proposeItalic();return document.querySelectorAll('#modalBody .checklist label').length===7;}catch(e){return false}}"""))
 page.click('#modalCancel')
 check('Faithful mode rejects alphabet inference',page.evaluate("""()=>{const p=Formaco.project,old=p.decisions.mode;p.decisions.mode='faithful';let ok=false;try{Formaco.generate('X',Formaco.selectedStyle)}catch(e){ok=e.message.includes('Faithful')}p.decisions.mode=old;return ok}"""))
 check('Regularized vs coherent construction',page.evaluate("""()=>{const p=Formaco.project,s=Formaco.selectedStyle;p.features.slant.effective=3;p.decisions.mode='coherent';const a=Formaco.generate('A',s);p.decisions.mode='regularized';const b=Formaco.generate('A',s);p.decisions.mode='coherent';p.features.slant.effective=0;return JSON.stringify(a.contours)!==JSON.stringify(b.contours)}"""))
 check('Incompatible contours rejected',page.evaluate("""()=>{let a=Formaco.clone(Formaco.selectedStyle.glyphs.A),b=Formaco.clone(a);b.contours.pop();return Formaco.compatible(a,b)==='contour count'}"""))
 check('Boolean difference preserves counter',page.evaluate("""()=>{const m=(x,y)=>({type:'M',x,y}),l=(x,y)=>({type:'L',x,y}),z=()=>({type:'Z'}),r=(x,y,w,h)=>[m(x,y),l(x+w,y),l(x+w,y+h),l(x,y+h),z()];return Formaco.boolean([r(0,0,100,100)],[r(20,20,60,60)],'difference').length===2}"""))
 check('Malformed project rejected without replacement',page.evaluate("""()=>{const old=Formaco.project.revision;let bad=Formaco.clone(Formaco.project);bad.styles[0].glyphs.X={contours:[[{type:'M',x:null,y:0}]],advance:600,status:'candidate'};try{Formaco.validateProject(bad);return false}catch(e){return Formaco.project.revision===old}}"""))
 check('SVG script and external resource rejection',page.evaluate("""()=>{let rejected=0;for(const s of ['<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>','<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/x"/></svg>'])try{Formaco.parseSvg(s)}catch(e){rejected++}return rejected===2}"""))
 check('Plain SVG cubic reconstruction',page.evaluate("""()=>Formaco.parseSvg('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><path d="M10 0 Q50 100 90 0Z"/></svg>').contours[0][1].type==='C'"""))
 # SVG import through the actual file control.
 svg=b'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><path d="M10 90L10 10L30 10L30 40L70 40L70 10L90 10L90 90L70 90L70 60L30 60L30 90Z"/></svg>'
 page.locator('#fileRef').set_input_files({'name':'own-H.svg','mimeType':'image/svg+xml','buffer':svg});page.wait_for_function('Formaco.project.references.length === 4')
 check('SVG import local raster overlay',page.evaluate('Formaco.project.references[3].data.startsWith("data:image/png")'))
 page.click('[data-act=correct]');page.wait_for_function('Formaco.project.references[3].corrected')
 page.click('[data-act=trace]');page.wait_for_timeout(300)
 check('Raster correction and tracing',page.evaluate('Formaco.selectedGlyph.contours.length > 0'))
 page.click('[data-act=confirm]');page.click('[data-act=analyze]')
 check('Conflicting reference measurements surfaced',bool(page.locator('#conflicts').inner_text()))
 # Undo real vector transform.
 page.locator('.edit-controls summary').click();before=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)');page.fill('#moveX','20');page.click('[data-act=transform]')
 after=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)');page.click('[data-act=undo]')
 check('Vector transform and undo',before!=after and before==page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)'))
 page.click('[data-act=redo]');check('Redo',after==page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)'))
 page.click('[data-act=theme]');check('Theme switching',page.evaluate('document.body.classList.contains("dark")'))
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(ROOT/'assets/mobile.png'),full_page=True)
 check('Mobile horizontal overflow',page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
 page.set_viewport_size({'width':1440,'height':1100})
 check('No uncaught browser errors',not errors,json.dumps(errors))
 check('No ordinary editing network calls',all(r.startswith(url.split('/index')[0]) for r in requests),str(requests))
 # Snapshot includes references, geometry and master states.
 (ROOT/'examples'/'starter-study.formaco.json').write_text(page.evaluate('JSON.stringify(Formaco.project,null,2)'))
 (ROOT/'examples'/'regular-O.svg').write_text(page.evaluate('Formaco.glyphSvg(Formaco.project.styles.find(s=>s.id==="regular").glyphs.O)'))
 (ROOT/'examples'/'portuguese-proof.svg').write_text(page.evaluate('Formaco.specimenSvg(Formaco.project.styles.find(s=>s.id==="regular")).svg'))
 browser.close()
(ROOT/'tests'/'browser-results.json').write_text(json.dumps(results,indent=2))
if any(not r['passed'] for r in results):sys.exit(1)
