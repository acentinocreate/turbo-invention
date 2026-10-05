"""Regression checks for Portuguese UI, zoom, cubic geometry and reference extraction."""
from pathlib import Path
import json, subprocess
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
results = []
def check(name, passed, detail=''):
    results.append(dict(check=name, passed=bool(passed), detail=detail))
    print(('PASS ' if passed else 'FAIL ') + name + ' ' + str(detail), flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width':1440,'height':1100})
    errors=[];requests=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('request',lambda r: requests.append(r.url))
    page.goto('http://127.0.0.1:8080/index.html')
    page.wait_for_function('window.Formaco !== undefined')
    check('Portuguese document and terminology',page.evaluate("""()=>document.documentElement.lang==='pt-BR'&&document.querySelector('[data-tool=direct]').textContent==='Nós'&&document.querySelector('#componentList option[value=arch]').textContent==='Arco e ombro'&&document.body.textContent.includes('Altura-x')&&document.body.textContent.includes('Bojo e contraforma')"""))
    page.click('[data-act=starter]');page.wait_for_function('Formaco.project.references.every(r=>r.data)')
    page.click('[data-act=confirm]');page.click('[data-act=analyze]')
    one=page.evaluate('Formaco.referenceConstructionProposals()')
    check('One H establishes stems, not unseen bowls', any(c['key']=='vertical' and c['char']=='H' for c in one['changes']) and any('Bojo' in s for s in one['missing']) and any('Arco' in s for s in one['missing']))
    check('Unobserved diagonal adaptation requires explicit selection',any(c['key']=='diagonal' and not c['selected'] and 'não observada' in c['confidence'] for c in one['changes']))
    check('Reference stem extraction has real dimensions',page.evaluate("""()=>{const c=Formaco.referenceConstructionProposals().changes.find(c=>c.key==='vertical'),b=Formaco.bbox(c.contours);return b.w===80&&b.h===700}"""))
    page.select_option('#componentList','diagonal');page.click('[data-act=editComponent]')
    check('Diagonal editor shows a stem instead of a square',page.evaluate('Formaco.bbox(Formaco.selectedGlyph.contours).h>Formaco.bbox(Formaco.selectedGlyph.contours).w*4'))
    page.select_option('#componentList','arch')
    check('Component selector can leave current editing mode',page.locator('#componentList').input_value()=='arch')
    page.click('[data-act=editComponent]')
    check('Arch component contains actual cubic shoulders',page.evaluate('Formaco.selectedGlyph.contours[0].some(c=>c.type==="C")'))
    page.click('[data-act=returnGlyph]')
    page.select_option('#componentList','diagonal');page.click('[data-act=editComponent]')
    page.evaluate("Formaco.ACT.selectNextPoint();document.querySelector('#nodeX').value=100;document.querySelector('#nodeY').value=0;Formaco.ACT.setNode()")
    draft=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)')
    page.select_option('#componentList','arch');page.select_option('#componentList','diagonal');page.click('[data-act=editComponent]')
    check('Switching components retains unsaved draft',page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)')==draft)
    page.click('[data-act=approveComponent]')
    check('Unsaved component edits must be saved before approval',not page.evaluate('Formaco.project.components.diagonal.approved') and 'Salve as alterações' in page.locator('#status').inner_text())
    page.click('[data-act=returnGlyph]')
    # Camera zoom around cursor must keep that font-space position under the cursor.
    box=page.locator('#editorSvg').bounding_box();cx=round(box['x']+box['width']*.6);cy=round(box['y']+box['height']*.6)
    coord="""([x,y])=>{const s=document.querySelector('#editorSvg'),p=s.createSVGPoint();p.x=x;p.y=y;const q=p.matrixTransform(s.getScreenCTM().inverse());return [q.x,q.y]}"""
    before=page.evaluate(coord,[cx,cy]);geometry=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)')
    page.mouse.move(cx,cy);page.mouse.wheel(0,-120);page.wait_for_function('document.querySelector("#zoomLevel").textContent!=="100%"');after=page.evaluate(coord,[cx,cy])
    check('Wheel zoom anchors the cursor',max(abs(a-b) for a,b in zip(before,after))<.01,{'before':before,'after':after})
    check('Wheel zoom changes magnification',page.locator('#zoomLevel').inner_text()!='100%')
    vb=page.locator('#editorSvg').get_attribute('viewBox');page.mouse.down(button='middle');page.mouse.move(cx+45,cy+30);page.mouse.up(button='middle')
    check('Middle-button pan changes viewport without outlines',page.locator('#editorSvg').get_attribute('viewBox')!=vb and page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)')==geometry)
    page.click('[data-act=fitView]');check('Fit resets zoom',page.locator('#zoomLevel').inner_text()=='100%')
    page.evaluate('for(let i=0;i<30;i++)Formaco.ACT.zoomIn()');check('Zoom maximum is bounded',page.locator('#zoomLevel').inner_text()=='3200%')
    page.click('[data-act=fitView]');page.click('[data-tool=direct]');page.click('[data-act=zoomIn]')
    radius=page.evaluate("""()=>{const s=document.querySelector('#editorSvg'),c=s.querySelector('circle[data-pi]:not([data-handle])');return Number(c.getAttribute('r'))*s.getScreenCTM().a}""")
    check('Node targets retain screen size at zoom',abs(radius-5)<.05)
    # Actual node drag at magnification and undo, with camera kept fixed.
    page.locator('.edit-controls summary').click();page.locator('#snap').uncheck();page.locator('.edit-controls summary').click();page.locator('#editorSvg').scroll_into_view_if_needed();circle=page.locator('#editorSvg circle[data-pi="0"]:not([data-handle])').first;bounds=circle.bounding_box();x=bounds['x']+bounds['width']/2;y=bounds['y']+bounds['height']/2
    old=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)');view=page.locator('#editorSvg').get_attribute('viewBox');page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+12,y+8);page.mouse.up()
    check('Node drag at zoom changes geometry without refitting',old!=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)') and view==page.locator('#editorSvg').get_attribute('viewBox'))
    page.click('[data-act=undo]');check('Zoomed edit is undoable',old==page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)'))
    page.click('[data-act=fitView]')
    # Generated circular counters retain their source curves.
    curves=page.evaluate("""()=>{const s=Formaco.selectedStyle,g=Formaco.generate('g',s),o=Formaco.generate('O',s);return {g:g.contours.map(c=>({nodes:Formaco.countNodes([c]),cubics:c.filter(p=>p.type==='C').length})),O:o.contours.map(c=>Formaco.countNodes([c]))}}""")
    check('g central counter uses four Bézier nodes',any(c['nodes']==4 and c['cubics']==4 for c in curves['g']),curves)
    check('O uses four nodes per contour',curves['O']==[4,4])
    check('Master repair retains already corresponding cubic counters',page.evaluate("""()=>{const a=Formaco.generate('g',Formaco.project.styles.find(s=>s.id==='light')),b=Formaco.generate('g',Formaco.project.styles.find(s=>s.id==='bold'));const [x,y]=Formaco.alignContours(a,b);return x.at(-1).filter(c=>c.type==='C').length===4&&y.at(-1).filter(c=>c.type==='C').length===4}"""))
    # A dense legacy contour can be fitted explicitly and undone.
    page.evaluate("""()=>{const g=Formaco.generate('g',Formaco.selectedStyle);g.contours=Formaco.flatten(g.contours).map(r=>[{type:'M',x:Math.round(r[0][0]),y:Math.round(r[0][1])},...r.slice(1,-1).map(p=>({type:'L',x:Math.round(p[0]),y:Math.round(p[1])})),{type:'Z'}]);g.status='candidate';Formaco.selectedStyle.glyphs.g=g;Formaco.setSelection('g','regular')}""")
    dense=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)');count=page.evaluate('Formaco.countNodes(Formaco.selectedGlyph.contours)')
    page.locator('.edit-controls summary').click();page.click('[data-act=reduceNodes]');page.click('#modalApply')
    check('Legacy dense glyph reduction has measured bound',page.evaluate('Formaco.selectedGlyph.nodeReduction.after<Formaco.selectedGlyph.nodeReduction.before && Formaco.selectedGlyph.nodeReduction.effectiveDeviation<=2.5'),count)
    page.click('[data-act=undo]');check('Node reduction restores exact prior contours on undo',page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)')==dense)
    page.locator('#glyphLock').check();before=page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)');page.click('[data-act=reduceNodes]');check('Locked outlines cannot be reduced',page.locator('#modal').is_hidden() and page.evaluate('JSON.stringify(Formaco.selectedGlyph.contours)')==before);page.locator('#glyphLock').uncheck()
    # Finish multiple-reference confirmations; intentionally asymmetric O remains actual source.
    for ch in ['O','n']:
        rid=page.evaluate('(ch)=>Formaco.project.references.find(r=>r.char===ch).id',ch);page.select_option('#refList',rid)
        if ch=='O':page.evaluate('Formaco.selectedGlyph.contours[0][1].x1+=27')
        page.click('[data-act=confirm]')
    page.evaluate("Formaco.setSelection('H','regular')")
    proposals=page.evaluate('Formaco.referenceConstructionProposals()')
    check('Multiple references establish bowl and shoulder sources',any(c['key']=='bowl' and c['char']=='O' for c in proposals['changes']) and any(c['key']=='arch' and c['char']=='n' for c in proposals['changes']))
    page.click('[data-act=referenceAssist]');page.click('#modalApply')
    check('Extraction retains actual asymmetric approved O',page.evaluate("""()=>{const p=Formaco.project,r=p.references.find(r=>r.char==='O');return JSON.stringify(p.components.bowl.contours)===JSON.stringify(r.reconstruction)&&!p.components.bowl.approved&&p.components.bowl.derivation.reference===r.id}"""))
    check('Generated o records the extracted O geometry source',page.evaluate("""()=>{const g=Formaco.generate('o',Formaco.selectedStyle);return g.componentVersions.bowl.source.includes('O')&&g.contours.some(p=>p.some(c=>c.type==='C'))}"""))
    # Existing base contour changes must be carried into accent proposals.
    check('Accent proposals reuse edited base outline',page.evaluate("""()=>{const s=Formaco.selectedStyle;s.glyphs.A=Formaco.generate('A',s);s.glyphs.A.contours=s.glyphs.A.contours.map(p=>p.map(c=>({...c,...('x'in c?{x:c.x+45}:{})})));s.glyphs.A.status='manual';const a=Formaco.generate('Á',s);return Math.abs(Formaco.bbox(a.contours).x-Formaco.bbox(s.glyphs.A.contours).x)<1}"""))
    # Legacy projects remain accepted without a destructive migration.
    legacy=(ROOT/'tests/fixtures/legacy-family.formaco.json').read_text()
    parsed=json.loads(legacy)
    check('Version-one project remains compatible',page.evaluate('(p)=>Formaco.validateProject(p).characters.length===136',parsed))
    page.screenshot(path=str(ROOT/'assets/editor-zoom.png'),full_page=True)
    check('No revision browser exceptions',not errors,errors)
    check('No revision runtime network calls',len(requests)==1,requests)
    browser.close()
(ROOT/'tests/revision-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
if any(not r['passed'] for r in results):raise SystemExit(1)
