import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];results=[]
def check(name,passed,detail=''):
 results.append({'check':name,'passed':bool(passed),'detail':detail});print(('PASS ' if passed else 'FAIL ')+name+' '+detail,flush=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':1100});errs=[];console=[];page.on('pageerror',lambda e:errs.append(str(e)));page.on('console',lambda e:console.append(e.text) if e.type=='error' else None);page.goto('http://127.0.0.1:8080/index.html');page.click('[data-act=starter]');page.wait_for_function('Formaco.project.references.every(r=>r.data)')
 # Derive actual components from three approved starter reconstructions.
 for ch,key,region in [('H','vertical','55,0,80,700'),('H','horizontal','55,315,550,70'),('O','bowl',None),('n','arch',None)]:
  page.evaluate('ch=>Formaco.setSelection(ch,"regular")',ch)
  refs=page.evaluate('Formaco.project.references.map(r=>({id:r.id,ch:r.char}))');rid=next(r['id'] for r in refs if r['ch']==ch);page.select_option('#refList',rid);page.click('[data-act=confirm]');page.select_option('#componentList',key)
  if region:page.fill('#componentRegion',region);page.click('[data-act=extractRegion]')
  else:page.click('[data-act=capture]')
  page.click('[data-act=approveComponent]')
 check('One/multiple reference geometry extraction',page.evaluate("""()=>{const p=Formaco.project,d=Formaco.generate('D',Formaco.selectedStyle);return d.componentVersions.vertical.source.includes('H')&&d.componentVersions.bowl.source.includes('O')&&p.components.bowl.contours.length===2}"""))
 check('Exact-preservation constraint rejects resizing',page.evaluate("""()=>{const c=Formaco.project.components.bowl,old=c.policy;c.policy='exact';let rejected=false;try{Formaco.generate('o',Formaco.selectedStyle)}catch(e){rejected=e.message.includes('preservar exatamente')}c.policy=old;return rejected}"""))
 # Per-style override does not mutate shared component geometry.
 page.select_option('#componentScope','style');page.select_option('#componentList','bowl');page.click('[data-act=capture]')
 check('Style component override separate from shared',page.evaluate("""()=>{const p=Formaco.project,s=Formaco.selectedStyle;return s.components.bowl!==p.components.bowl&&s.components.bowl.source!==p.components.bowl.source}"""))
 page.select_option('#componentScope','shared')
 page.evaluate('Formaco.setSelection("Z","regular")');page.locator('.edit-controls summary').click()
 # Numeric keyboard-compatible path construction, then editing and true contour splitting.
 for x,y in [(55,0),(400,0),(400,500),(55,500)]:
  page.fill('#nodeX',str(x));page.fill('#nodeY',str(y));page.click('[data-act=addNumericPoint]')
 page.click('[data-act=closePath]');check('Numeric pen/closed contour construction',page.evaluate('Formaco.selectedGlyph.contours[0].length===5'))
 page.click('[data-act=selectNextPoint]');page.click('[data-act=selectNextPoint]');page.click('[data-act=curve]');page.click('[data-act=split]')
 check('Editable cubic handles and subdivision',page.evaluate('Formaco.selectedGlyph.contours[0].filter(c=>c.type==="C").length===2'))
 page.click('[data-act=splitContour]');check('Real contour splitting',page.evaluate('Formaco.selectedGlyph.contours.length===2&&Formaco.selectedGlyph.contours.every(p=>p.at(-1).type!=="Z")'))
 page.click('[data-act=join]');page.click('[data-act=closePath]');check('Contour joining/closure',page.evaluate('Formaco.selectedGlyph.contours.length===1&&Formaco.selectedGlyph.contours[0].at(-1).type==="Z"'))
 page.fill('#advance','720');page.click('[data-act=metrics]');check('Advance control applied',page.evaluate('Formaco.selectedGlyph.advance===720'))
 # Fractional requested coordinate is preserved while canonical contour is integer.
 page.click('[data-act=selectNextPoint]');page.fill('#nodeX','55.4');page.fill('#nodeY','10.6');page.click('[data-act=setNode]')
 check('Requested/effective node values retained',page.evaluate('Formaco.selectedGlyph.requestedPoint.x===55.4&&Formaco.selectedGlyph.contours[0][0].x===55'))
 # Boolean preserving an original compound hole while welding a separate solid.
 page.evaluate("""()=>{const s=Formaco.selectedStyle,g=s.glyphs.O;s.glyphs.Z=Formaco.clone(g);s.glyphs.Z.locked=false;s.glyphs.Z.contours.push([{type:'M',x:590,y:200},{type:'L',x:680,y:200},{type:'L',x:680,y:400},{type:'L',x:590,y:400},{type:'Z'}]);Formaco.setSelection('Z','regular');}""")
 page.click('[data-act=union]');check('Boolean union retains compound counter',page.evaluate('Formaco.selectedGlyph.contours.length===2'))
 # Decomposed preview takes explicit composition records, not hidden normalization.
 page.evaluate("""()=>{const s=Formaco.selectedStyle;s.glyphs.i=Formaco.generate('i',s);s.glyphs['í']=Formaco.generate('í',s);s.glyphs['\u0301']=Formaco.generate('\u0301',s)}""")
 check('Accented i has separate dot removed',page.evaluate('Formaco.selectedStyle.glyphs["í"].contours.length===2'))
 check('Preview composed/decomposed agreement',page.evaluate('Formaco.specimenSvg(Formaco.selectedStyle,"í").svg===Formaco.specimenSvg(Formaco.selectedStyle,"i\\u0301".replace("\\\\u0301","\\u0301")).svg'))
 # Synthetic authorized raster references (not third-party art).
 for mime,name in [('image/png','ring.png'),('image/jpeg','ring.jpg')]:
  data=page.evaluate("""mime=>{const c=document.createElement('canvas');c.width=160;c.height=200;const x=c.getContext('2d');x.fillStyle='white';x.fillRect(0,0,160,200);x.fillStyle='black';x.fillRect(20,20,120,160);x.fillStyle='white';x.fillRect(45,50,70,100);return c.toDataURL(mime).split(',')[1]}""",mime)
  import base64
  page.fill('#refChar','O');page.locator('#fileRef').set_input_files({'name':name,'mimeType':mime,'buffer':base64.b64decode(data)});page.wait_for_function('(name)=>Formaco.project.references.some(r=>r.name===name)',arg=name)
  page.click('[data-act=correct]');page.wait_for_function('(name)=>Formaco.project.references.find(r=>r.name===name).corrected',arg=name);page.click('[data-act=trace]');page.wait_for_timeout(100)
  check(name+' import and counter tracing',page.evaluate('Formaco.selectedGlyph.contours.length===2'))
 original=page.evaluate('Formaco.project.references.at(-1).data');corrected=page.evaluate('Formaco.project.references.at(-1).corrected');page.fill('#refRotation','10');page.fill('#crop','0.05,0.05,0.9,0.9');page.fill('#perspective','0,0;1,0.05;0.95,1;0.05,0.95');page.click('[data-act=correct]');page.wait_for_timeout(200)
 check('Real crop/rotation/perspective, original retained',page.evaluate('Formaco.project.references.at(-1).data')==original and page.evaluate('Formaco.project.references.at(-1).corrected')!=corrected)
 before=page.evaluate('JSON.stringify(Formaco.project)');page.locator('#fileProject').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"format":"wrong"}' });page.wait_for_timeout(150)
 check('Actual failed file import retains current project',before==page.evaluate('JSON.stringify(Formaco.project)'))
 # Safe content handling in metadata and imported filenames.
 page.evaluate("document.querySelector('#designer').value='<img src=x onerror=alert(1)>';document.querySelector('#designer').dispatchEvent(new Event('change'))")
 check('Imported/typed text is not executable HTML',page.locator('img[src=x]').count()==0)
 page.locator('summary').filter(has_text='Ampliar e atualizar').click();page.fill('#customChar','U+1F701');page.click('[data-act=addChar]');check('Supplementary Unicode scalar accepted',page.evaluate('Formaco.project.characters.includes(String.fromCodePoint(0x1f701))'))
 custom=page.evaluate("() => {const ch=String.fromCodePoint(0x1f701);Formaco.selectedStyle.glyphs[ch]=Formaco.clone(Formaco.selectedStyle.glyphs.H);return Array.from(Formaco.exportFont(Formaco.selectedStyle));}");Path('/tmp/Formaco-custom.otf').write_bytes(bytes(custom))
 from fontTools.ttLib import TTFont
 customfont=TTFont('/tmp/Formaco-custom.otf');check('Independent supplementary cmap extraction',0x1f701 in customfont.getBestCmap());customfont.close()
 check('No console errors in reference/editor workflow',not console,str(console));check('No uncaught editor exceptions',not errs,str(errs));b.close()
(ROOT/'tests'/'editor-results.json').write_text(json.dumps(results,indent=2))
if any(not r['passed'] for r in results):raise SystemExit(1)
