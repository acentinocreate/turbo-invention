# Formaço

A local reference-lettering atelier. Reconstruct approved artwork as editable contours, extract reusable components, review anatomical proposals, develop separate weight and italic drawings, and export real static fonts.

**Open `index.html` directly in a browser or put it on ordinary static hosting.** It embeds its CSS, application JavaScript, dependency code and third-party licence notices. There is no end-user installation, build, account, API key, CDN or server requirement. It makes no network calls during editing or export. Supporting files are documentation and examples, not runtime dependencies.

An optional development server is `python -m http.server 8080` from this directory. Each cloud task already has an isolated checkout; use the existing checkout, without creating a Git worktree unless explicitly requested.

## Start a design

1. Import authorized PNG, JPEG or SVG artwork and identify its character and style. Alternatively, load the original H/O/n starter. Multiple references can be assigned to a character. Choose a primary reference or reassign conflicting references to different styles.
2. Correct a raster image: normalized crop, rotation, four perspective corners, contrast and foreground inversion. Apply correction, then adjust trace threshold and simplification. The original remains separate. SVG loads filled vectors directly unless you correct it first, in which case it is traced as a raster.
3. Trace/load or use the pen to draw. Compare the overlay, align it and repair the contours. Confirm the reconstruction yourself. Tracing never establishes accuracy automatically.
4. Analyze the confirmed drawing. Inspect measured bounds, candidate scanline stem widths and long-edge slant. Define missing heights, stroke contrast, curvature, terminals, openings and anatomical alternatives yourself. Each measurement records its source and descriptive confidence.
5. Capture a whole contour set or selected contour into a named component. **Extract region** intersects an approved drawing with a font-unit rectangle, useful for a stem or terminal in a connected letter. Edit the component in the same vector editor. Choose a shared component or a current-style override, its treatment policy, and approve it.
6. Approve construction decisions. Propose H/O/A/n/o/a/g first. Inspect component revisions, measurement sources and unresolved constraints in Inspection; review every representative before extending. Propose one character, a group, missing characters or the complete set. The preview shows replacements and supports selective application. Approved, manually edited, reference-derived and locked glyphs are preserved.
7. Develop Light and Bold extremes separately. References and component overrides may differ by style. Generated extremes are starting proposals, not a conclusion drawn from Regular. Approve representative extremes before interpolation. Incompatibility is reported per glyph. Use explicit contour alignment for the same topology, or draw an independent intermediate.
8. For Italic, approve the separate single-storey a/g, narrower rhythm and exit-terminal proposals, or supply independent references/drawings. Review the seven representatives before extending. Repeat extreme-master development for italics. Oblique is a separately labelled shear operation.
9. Proof Portuguese coverage, spacing and diagonals. Set bearings or advances, pair kerning and accent anchors/optical adjustments. Review accent rebuilding before applying it. Export a style or the enabled family. Disabled styles are omitted.

Use the character panel to change glyphs and the family shelf to change styles. The panel labelled **Coordinates, geometry, anchors & spacing** expands numeric controls. User-drawn SVG output is geometry; UI text uses locally available system monospace fonts.

## What construction does and does not infer

There are no stock font outlines and no hidden model. Character recipes describe anatomy and assemble vertical/horizontal/diagonal strokes, bowls, arches, terminal/serif parts and accent components. The supplied starter components are independent original drawings and remain unapproved until chosen. Captured contours preserve their source geometry before adaptation; each generated glyph saves component source/revision and measurement snapshots. One H cannot determine an O: its bowl must be supplied, drawn, or explicitly accepted as a separate proposal.

Automatic analysis measures bounds, estimates stem runs at three scanlines and finds the slant of a long straight edge. It does **not** recognize a character, establish optical stem thickness, infer serif intent, prove stylistic compatibility, or estimate a statistical confidence. Contrast, contrast axis, overshoot, proportions, anatomical alternatives and serif/corner/terminal geometry require user decisions. Conflict checks compare available numerical measurements; terminal and conceptual incompatibility still require visual review.

- **Faithful reconstruction** preserves confirmed individual drawings and disables alphabet inference.
- **Coherent extension** fits authorized components to character anatomy. Component envelope scaling and the explicit arch/bowl weight deformation are proposals requiring optical review; they can distort subtle details.
- **Regularized development** additionally rounds new candidate geometry to a two-unit grid. Existing reviewed drawings remain protected.

“Preserve exactly” forbids component resizing, incompatible bowl stroke/axis changes, slant/italic transformation and regularization. Proportional/shared/optical policies authorize proposal adaptation; shared geometry is propagated only through an explicit preview. Envelope fitting can change aspect ratio and is disclosed for review. Optical permission is not automatic professional optical correction. Design notes are stored review reminders, not an executable design program. Measured reference slant is recorded separately from requested additional slant.

Geometric/grotesque and modular display constructions are the most directly supported recipes. Humanist, rounded, serif and slab details can use custom components. Stencil, organic and experimental contours are editable and exportable, but complex contextual joins, negative-space bridges, cursive connectivity and unusual anatomies need independent drawing or substantial manual editing. Automatic faithful extension of every such construction is **not implemented**. The application rejects missing recipes rather than replacing them with a generic font.

## Editing, family links and spacing

The core consists of closed or open M/L/C/Z contours with editable on-curve points and Bézier controls, not pixels. Pen clicks add lines; drag a new point to create a cubic. Selection moves a contour; Nodes edits endpoints and handles. Numeric points and next-point/next-contour buttons support keyboard editing. Enter closes a pen path, Delete removes a selected node, arrows move selected geometry; Ctrl/Cmd-Z and Shift-Z undo/redo outside text fields.

Tools include subdivision, segment-to-cubic conversion, deleting points, connecting two open paths, open/close, duplicate, move/scale/rotate, horizontal reflection, and union/difference/intersection. Boolean operations adaptively flatten cubic segments to 0.6 font units and preserve nested counters. Resulting outlines remain the same in the editor, specimen, SVG and font exports. Canonical editable glyph coordinates have **one-font-unit precision** so CFF export does not independently round them. Requested numeric point values are retained in Inspection. Metrics record requested and effective values; editing advance applies it, while changing bearings calculates the effective advance from them.

Shared edits flag styles for review and never automatically regenerate. The modal lists affected glyphs/styles, compares old/new geometry and allows selective application with undo. Manually corrected or approved glyphs remain protected. Detach a glyph/style or use a style component override to preserve an independent direction.

Intermediate weights require equal contour counts, command types, orientation, counter nesting/order and construction decisions. These tests cannot establish semantic point correspondence. **Align extreme contours** explicitly resamples each corresponding contour to 64 points, retaining contour order. Review its preview and the resulting curves: it is not an automatic contour-order repair. Different topology must be redrawn or kept independent. Manual corrections become local overrides.

True italic proposals alter anatomy choices and terminals in addition to slant/width. Their limited recipes do not constitute a universal italic designer. Upright and italic masters interpolate separately. Oblique only shears existing outlines and is labelled accordingly.

Specimens use designed advances and GPOS pair values. Ink/paper, size, tracking, leading and monospaced proof spacing are application settings; tracking/leading/monospace are not written into the font. SVG previews fit the available screen width. Unsupported glyphs are red dashed boxes with explicit Unicode listings. Bounds-based line margins include high accents and low cedillas. Pair kerning is implemented; kerning groups are not offered.

## Coverage and exports

Default coverage is **136 mapped characters**: A–Z, a–z, 0–9, all requested Portuguese upper/lower accents including Ü/ü and Ç/ç; space/NBSP; requested punctuation, quotation marks, ordinals and currency signs; and acute, grave, circumflex, tilde, diaeresis and cedilla combining marks.

Base top/bottom anchors and per-glyph/per-style optical shifts drive accents. Review accent rebuilding from the current base and component: protected outlines are replaced only through the explicit comparison. Separate i dots can be replaced with an accent or preserved as an approved decision. Custom mappings accept single Unicode scalars or `U+E000` notation; duplicates, controls, format controls and surrogate values are rejected. Supplementary-plane mapping uses the font library's cmap support.

Export glyph/group/all SVGs, typed SVG proofs and comparison SVGs. Export installable CFF OpenType `.otf` and standards-compliant uncompressed `.woff` with identical outlines/metrics, Unicode cmap, OS/2 weights, italic flags, safe PostScript names, legacy and typographic family names, metadata, GPOS pair kerning, GDEF mark classes, and GPOS top/bottom mark-to-base anchors. GSUB `ccmp` maps supported Portuguese base+mark pairs to the corresponding editable precomposed glyphs. The app's decomposed preview follows those recorded composition pairs and otherwise uses anchors; independent HarfBuzz tests also exercise mark positioning on a non-precomposable H+acute sequence. No claim relies on preview NFC normalization.

The family ZIP contains OTF and WOFF files for each enabled style, an editable project, a coverage/style/licence README and a LICENSE.txt containing the chosen font licence. Fonts are static snapshots. Re-export after editing. A family with enabled empty styles must first develop or disable them. Export blocks open, invalid, degenerate or detected self-intersecting contours. Overhangs remain legal and are reported for review.

**Not implemented:** variable fonts, hinting, local-font import, mark-to-mark stacking, arbitrary multi-mark shaping, ligature design beyond Portuguese composition, contextual scripts, automatic kerning, vertical typography, automatic skeleton extraction, pixel/liquid/random-symbol tools. Native desktop font-manager grouping has not been tested; metadata and browser CSS family/style selection have been checked independently. Technical font validity does not establish visual quality.

## Project limits and safety

| Limit | Implemented bound |
| --- | --- |
| Reference file | 8 MB PNG/JPEG/SVG |
| Decoded reference dimensions | 4096 × 4096 maximum |
| References | 24 |
| Project JSON | 32 MB |
| Mapped glyphs | 256, including the default 136 |
| Styles | 24 |
| Commands per glyph/component | 8,000 |
| Coordinate extent | ±10,000 font units |
| Advance width | 0–4,000 |
| Undo/redo | 40 snapshots, 64 MB serialized-history budget |
| Specimen text | 12,000 characters in imported projects |
| Raster trace resolution | 220 × 280, followed by adjustable simplification |

These are ceilings, not performance guarantees. The low trace resolution prioritizes responsiveness; intricate references require manual correction. Keep practical projects smaller than the ceilings, particularly on mobile. Photograph scale and perspective are user-specified, not detected. Perspective resampling uses nearest-neighbor sampling and can lose fine raster detail. Crop bounds and simplification are explicit. Raster correction produces a 700-pixel-high image, with automatic aspect-preserving width or an explicitly selected width up to 1,200 pixels. File signatures and dimensions are checked before raster decoding. Original and corrected overlay layers can be selected separately.

SVG import permits plain filled SVG/groups/paths/rectangles/circles/ellipses/polygons/polylines/lines and rejects scripts, events, styles, resource URLs, filters, masks, images, foreign objects and entities. Visible strokes must be outlined before import. Only plain filled geometry is reconstructed; complex painted compositions should use corrected raster tracing. SVG text is rejected instead of silently converted using an unrelated font. Rounded rectangle radii should be converted to paths before import. Supplied references must be owned or authorized; there is no rights-verification service.

Autosave and theme use local storage. JSON backups preserve references, corrections, contours, components, measurements, policies, anchors, Unicode mappings, styles, master links, local overrides, metrics, kerning and approval states. Storage failure leaves editing usable and displays a backup warning. Unreadable autosave is retained verbatim; a recovery download is offered and autosaving is disabled until a healthy browser session is started. Opening malformed JSON leaves the current project unchanged. History does not survive reload. Avoid moving between file and HTTP origins without a JSON backup: their storage is separate.

## Browser support and validation

| Browser/platform | Status |
| --- | --- |
| Chromium 151, Linux x86-64, local HTTP | Tested |
| Chromium, file:// in this cloud image | Blocked by administrator URL policy; not executed |
| Recent Chrome/Edge on desktop, ordinary file:// | Expected from embedded assets; needs an unrestricted device check |
| Current Firefox / Safari | Targeted standard DOM/Canvas/SVG/Blob APIs; not executed |
| Mobile Chrome / Safari on physical devices | Not executed; 390 × 844 Chromium viewport tested |

Tests used a Linux cloud machine with four CPU cores of quota and 32 GiB memory limit. See `IMPLEMENTATION_REPORT.md` and the saved machine-readable results. Browser tests are functional automation, not professional type-design approval or an accessibility conformance certification.

For reproducible developer checks, install Python `playwright`, `fonttools` and `uharfbuzz`, provide Chromium at `/usr/bin/chromium` (or adjust the script path), then serve this directory and run:

```sh
python tests/build.py
python tests/browser_checks.py
python tests/family_checks.py
python tests/editor_checks.py
python tests/validate_fonts.py
python tests/delivery_checks.py
```

Optional `python tests/native_family_checks.py` requires Fontconfig's `fc-scan`; it scans family/slant recognition without installing fonts. Direct-file checks record administrator policy blocks instead of bypassing them.

`tests/build.py` combines the already bundled `src/vendor.js`, shell and application source. End users only need the shipped HTML. To rebuild dependencies, use the pinned package/lock manifests in `tests/` in a separate development directory, then bundle `src/vendor-entry.js` with esbuild and replace `src/vendor.js`. Runtime notices are embedded from `LICENSES.txt`; retain them when redistributing the single HTML file.

## Publication files and licensing

`assets/` contains the original logo/icon, publication card and actual desktop/mobile screenshots. `examples/` contains original starter-based candidate fonts, SVG proofs, an editable study and a full family ZIP. They demonstrate plumbing and editable geometry, not finished commercial typography. Example licences are explicit in their metadata/package README. User-imported references and user-created font licences remain the user's responsibility.

Application code, original starter contours and original publication assets: MIT (`LICENSE`). Embedded dependencies retain full upstream notices in `LICENSES.txt`; see `DEPENDENCIES.md` for versions. No third-party font or reference artwork is bundled. “Formaço” is an application identity, with no claim of trademark clearance.
