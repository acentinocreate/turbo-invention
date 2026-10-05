"""Independently scan example fonts with Fontconfig; does not install fonts."""
from pathlib import Path
import json, os, subprocess

ROOT = Path(__file__).resolve().parents[1]
cache = Path('/tmp/formaco-fontconfig-cache')
cache.mkdir(exist_ok=True)
env = dict(os.environ, XDG_CACHE_HOME=str(cache))
results = []
for font in sorted((ROOT / 'examples').glob('*.otf')):
    scan = subprocess.run(
        ['fc-scan', '--format', '%{family}\n%{style}\n%{weight}\n%{slant}\n', str(font)],
        env=env, capture_output=True, text=True, check=True)
    family, style, weight, slant = scan.stdout.strip().splitlines()
    passed = 'Formaço Study' in family and (slant == '100') == ('italic' in font.stem)
    results.append(dict(file=font.name, family=family, style=style,
                        weight=weight, slant=slant, passed=passed))
    print(('PASS ' if passed else 'FAIL ') + font.name)
(ROOT / 'tests/native-family-results.json').write_text(json.dumps(results, indent=2))
assert len(results) == 10 and all(r['passed'] for r in results)
