from pathlib import Path
root=Path(__file__).resolve().parents[1]
shell=(root/'src/shell.html').read_text()
libs=(root/'src/vendor.js').read_text()
app=(root/'src/app.js').read_text()
assert '</script' not in app.lower()
notices=((root/'LICENSE').read_text()+'\n'+(root/'LICENSES.txt').read_text()).replace('-->','-- >')
shell=shell.replace('<!--LIBRARY-->','<!-- Full embedded dependency notices\n'+notices+'\n--><!--LIBRARY-->')
(root/'index.html').write_text(shell.replace('<!--LIBRARY-->','<script>'+libs.replace('</script','<\\/script')+'</script>').replace('<!--APP-->','<script>'+app+'</script>'))
