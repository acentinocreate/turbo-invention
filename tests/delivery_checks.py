"""Restore shipped projects and attempt direct-file startup without bypassing policy."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                                args=['--no-sandbox'])
    page = browser.new_page()
    page.goto('http://127.0.0.1:8080/index.html')
    for name in ['family-study.formaco.json', 'starter-study.formaco.json']:
        expected = json.loads((ROOT / 'examples' / name).read_text())
        page.locator('#fileProject').set_input_files(ROOT / 'examples' / name)
        page.wait_for_function('(n)=>Formaco.project.family===n', arg=expected['family'])
        page.wait_for_timeout(200)
        actual = page.evaluate('({family:Formaco.project.family,styles:Formaco.project.styles.length,references:Formaco.project.references.length,characters:Formaco.project.characters.length})')
        passed = all(actual[k] == len(expected[k]) for k in ['styles', 'references', 'characters'])
        results.append(dict(check=name, passed=passed, actual=actual))
        assert passed
        print('PASS restore ' + name)
    try:
        page.goto((ROOT / 'index.html').as_uri())
        page.wait_for_function('window.Formaco !== undefined')
        results.append(dict(check='file startup', passed=True, status='executed'))
    except Exception as error:
        reason = str(error).splitlines()[0]
        results.append(dict(check='file startup', status='blocked' if 'ERR_BLOCKED_BY_ADMINISTRATOR' in reason else 'failed', reason=reason))
        print('FILE STARTUP: ' + reason)
    browser.close()
(ROOT / 'tests/delivery-results.json').write_text(json.dumps(results, indent=2))
