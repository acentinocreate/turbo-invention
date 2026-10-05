from pathlib import Path
root=Path(__file__).resolve().parents[1]
shell=(root/'src/shell.html').read_text()
libs=(root/'src/vendor.js').read_text()
app=(root/'src/app.js').read_text()
for marker,filename in [('CURVE_HELPERS','curves.js'),('CAMERA_HELPERS','camera.js'),('REFERENCE_HELPERS','reference-assist.js')]:
    app=app.replace('// '+marker,(root/'src'/filename).read_text() if (root/'src'/filename).exists() else '')
assert '</script' not in app.lower()
notices=((root/'LICENSE').read_text()+'\n'+(root/'LICENSES.txt').read_text()).replace('-->','-- >')
shell=shell.replace('<!--LIBRARY-->','<!-- Full embedded dependency notices\n'+notices+'\n--><!--LIBRARY-->')
(root/'index.html').write_text(shell.replace('<!--LIBRARY-->','<script>'+libs.replace('</script','<\\/script')+'</script>').replace('<!--APP-->','<script>'+app+'</script>'))
