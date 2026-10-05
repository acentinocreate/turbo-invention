"""Exercise new-project confirmation, backup, history and storage recovery."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
results=[]
def check(name, passed):
    results.append({'check':name,'passed':bool(passed)})
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1100}); errors=[]; requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto('http://127.0.0.1:8080/index.html');page.wait_for_function('window.Formaco')
    page.click('[data-act=starter]');page.wait_for_function('Formaco.project.references.length>0 && Formaco.project.references.every(r=>r.data)')
    page.click('[data-act=theme]');page.fill('#crop','.1,.2,.5,.6');page.fill('#designNote','nota anterior')
    page.evaluate("Formaco.project.styles[0].kerning.AV=-70;Formaco.project.notes=[{text:'teste'}];Formaco.project.characters.push('\\uE000')")
    original=page.evaluate('JSON.stringify(Formaco.project)')
    page.click('[data-act=resetProject]')
    check('Opening confirmation preserves project',page.evaluate('JSON.stringify(Formaco.project)')==original)
    page.click('#modalCancel');check('Cancel preserves project',page.evaluate('JSON.stringify(Formaco.project)')==original)
    page.click('[data-act=resetProject]')
    with page.expect_download() as event: page.get_by_role('button',name='Salvar projeto atual',exact=True).click()
    data=json.loads(Path(event.value.path()).read_text());check('Backup contains prior project',data==json.loads(original))
    page.click('#newProjectConfirm')
    check('Reset removes references glyphs notes and kerning',page.evaluate("Formaco.project.references.length===0&&!Formaco.project.notes&&Formaco.project.styles.every(s=>!Object.keys(s.glyphs).length&&!Object.keys(s.kerning).length)"))
    check('Defaults are unapproved with ten enabled styles',page.evaluate('Formaco.project.styles.length===10&&Formaco.project.styles.every(s=>s.enabled&&!s.masterApproved)&&!Formaco.project.decisions.approved&&Object.values(Formaco.project.components).every(c=>!c.approved)'))
    check('Custom Unicode mappings are removed',page.evaluate("!Formaco.project.characters.includes('\\uE000')"))
    check('Reference controls reset',page.locator('#crop').input_value()=='0,0,1,1' and page.locator('#designNote').input_value()=='')
    check('Theme preserved',page.evaluate("document.body.classList.contains('dark')"))
    page.click('[data-act=undo]');check('Undo recovers entire prior project',page.evaluate('JSON.stringify(Formaco.project)')==original)
    page.click('[data-act=redo]');page.wait_for_timeout(600)
    check('Autosave contains empty project',page.evaluate("JSON.parse(localStorage.getItem('formaco.project.v1')).references.length===0"))
    page.reload();page.wait_for_function('window.Formaco');check('Reload keeps new empty project',page.evaluate('Formaco.project.references.length===0'))
    page.set_viewport_size({'width':390,'height':844});check('Mobile has no page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.evaluate("localStorage.setItem('formaco.project.v1','{broken')");page.reload();page.wait_for_function('window.Formaco')
    page.click('[data-act=resetProject]');page.click('#newProjectConfirm');page.wait_for_timeout(600)
    check('Corrupt autosave is preserved after reset',page.evaluate("localStorage.getItem('formaco.project.v1')==='{broken'"))
    check('Recovery remains available',page.locator('#rawRecovery').is_visible())
    check('No JavaScript errors',not errors)
    check('No remote requests',all(r.startswith('http://127.0.0.1:8080/') for r in requests))
    other=browser.new_context();other.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('Full','QuotaExceededError')}")
    pg=other.new_page();pg.goto('http://127.0.0.1:8080/index.html');pg.wait_for_function('window.Formaco');pg.click('[data-act=resetProject]');pg.click('#newProjectConfirm');pg.wait_for_timeout(600)
    check('Storage failure keeps editing usable and requests backup',pg.evaluate('Formaco.project.references.length===0') and 'Cópia de segurança' in pg.locator('#saveState').inner_text())
    browser.close()
(ROOT/'tests/reset-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
assert all(r['passed'] for r in results)
