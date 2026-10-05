# Embedded dependency credits

All runtime code is bundled inside `index.html`; no CDN or runtime installation. Full upstream notices are in `LICENSES.txt` and embedded in the HTML. JSZip uses its MIT licence option.

| Package | Version | Licence |
| --- | --- | --- |
| core-util-is | 1.0.3 | MIT |
| immediate | 3.0.6 | MIT |
| inherits | 2.0.4 | ISC |
| isarray | 1.0.0 | MIT |
| jszip | 3.10.1 | (MIT OR GPL-3.0-or-later) |
| lie | 3.3.0 | MIT |
| opentype.js | 1.3.4 | MIT |
| pako | 1.0.11 | (MIT AND Zlib) |
| polygon-clipping | 0.15.7 | MIT |
| process-nextick-args | 2.0.1 | MIT |
| readable-stream | 2.3.8 | MIT |
| robust-predicates | 3.0.3 | Unlicense |
| safe-buffer | 5.1.2 | MIT |
| setimmediate | 1.0.5 | MIT |
| splaytree | 3.2.3 | MIT |
| string.prototype.codepointat | 0.2.1 | MIT |
| string_decoder | 1.1.1 | MIT |
| svgpath | 2.6.0 | MIT |
| tiny-inflate | 1.0.3 | MIT |
| util-deprecate | 1.0.2 | MIT |

The bundled dependency graph includes browser shims and decompression helpers. Fonts and reference art are not dependencies: all starters are original contour constructions. UI type uses locally installed system monospace fonts.

Build-only: esbuild 0.25.0 (MIT). Validation-only: Python, FontTools 4.61.1, Playwright and Chromium, uharfbuzz. They are not needed or distributed as application runtime binaries.
