# Formaço — historical version-one implementation and test report

Current release: see RELATORIO_ATUALIZACAO.md and README.md for version 2.0.

Delivery date: 2026-10-05. The self-contained application is `index.html`. Its CSS, JavaScript, runtime dependencies and full licence notices are embedded. The source, README, credits, complete licence notices, publication assets, editable examples and ten pairs of OTF/WOFF exports accompany it. Supporting documents are not needed to run the application. No website deployment was performed. GitHub delivery is recorded separately in the accompanying conversation.

## Implemented

- Versioned project model, bounded undo/redo, local autosave, JSON backup/restore, raw corrupt-autosave recovery, storage-failure warnings and persistent themes.
- PNG/JPEG and restricted sanitized SVG import, reference identity/style assignments, multiple references, primary selection, numerical conflict warnings, original/corrected overlays, crop, rotation, projective correction, contrast/separation, threshold tracing and simplification. Confirmation precedes measurement. Raster tracing is a reconstruction proposal.
- Editable M/L/C/Z contours, pen and selection tools, endpoints/handles and numeric coordinates, point subdivision/deletion, contour split/join/open/close, transforms, duplication, adaptive-flattened polygon booleans with counters, guides, snapping, metrics and anchors. The editor automatically fits extended outlines and reference overlays.
- Measured bounds, scanline stem estimates and straight-edge slant; user-defined measurements and component policies; editable/captured/extracted components with provenance and style overrides. Anatomical recipes assemble those components instead of importing finished typeface outlines. Faithful mode disables inference; coherent and regularized modes produce explicitly unreviewed proposals. Representatives, construction approval and selective undoable regeneration protect edited/approved outlines.
- All 136 requested default mappings, editable accent parts and per-glyph/style anchors, Portuguese proof text, single-scalar supplementary mappings, side bearings/advances, pair kerning, multiline SVG proofs and two-style comparisons.
- Five weights and corresponding italic styles, additional/disabled styles, separate extreme approvals, compatibility checks, explicit contour-resampling repair, interpolation of compatible outlines, independent/local corrections, relationship tracking and selective propagation. Italic proposals change limited anatomical forms/terminals as well as slant; separately labelled Oblique performs shear.
- Glyph/group/set/proof/comparison SVG exports, CFF OTF and valid uncompressed WOFF, family ZIP with project/README/licence, Unicode maps, naming/weight/italic metadata, GPOS pair kerning and mark-to-base positioning, GDEF marks and Portuguese GSUB composition. Exports use the same canonical outlines and designed metrics as previews.
- Responsive independently scrollable panels, keyboard editing controls, light/dark themes, optional technical inspection and original starter drawings/identity/publication assets. No remote editing or export service, stock font outlines, analytics or runtime downloads.

## Tests actually executed

Latest saved results: **281 passing assertions**, plus **10 independent native font scans**. Tests are reproducible from README instructions and the scripts in `tests/`. These are functional and technical checks, not expert visual-quality approval.

| Suite | Passed | Evidence |
| --- | ---: | --- |
| Browser workflow | 24 | `tests/browser-results.json` |
| Reference/vector editor | 21 | `tests/editor-results.json` |
| Masters/family/storage | 14 | `tests/family-results.json` |
| Independent FontTools/HarfBuzz validation | 220 | `tests/font-results.json` |
| Delivered project restores | 2 | `tests/delivery-results.json` |
| Native Fontconfig family/slant recognition | 10 | `tests/native-family-results.json` |

Chromium 151.0.7922.173 ran on Linux x86-64 in this cloud workspace, over local HTTP. Desktop viewport: 1440 × 1100; phone simulation: 390 × 844. Resource allocation: four CPU cores of quota and 32 GiB memory limit. Generating the complete 136-character candidate set took approximately **0.13 seconds** in the final browser run. This is a small-project observation, not a maximum-size or mobile-device performance guarantee. Actual desktop/mobile screenshots are in `assets/`.

Executed workflows cover startup; original and imported SVG/PNG/JPEG references; correction/tracing and retained originals; confirmed measurement; one/multiple reference component extraction; conflicting references; all three fidelity modes; approval gates; protected overrides; points/handles/booleans/counters; transforms and undo/redo; accents and supplementary mappings; master repair/interpolation; structural italic versus actual Oblique shear; shared propagation; preview advances/kerning; all ten browser-loaded WOFF styles; family ZIP; malformed imports; text injection rejection; unavailable storage and raw recovery; themes and phone overflow. Recorded reference/editor/family workflows produced no uncaught browser exceptions. The ordinary-editing request log contained only the initial local HTML request.

Independent FontTools and HarfBuzz checks validate every example font's mappings, real outlines, opposite-winding counters, designed bearings, names, weight values, italic flags, licence metadata, checksums, pair kerning, mark coverage and anchors. All 26 Portuguese precomposed/decomposed pairs shape consistently. **H + combining acute**, without a precomposed equivalent, separately exercises actual GPOS positioning. WOFF table checksums, mappings and metrics match their OTF snapshots. Fontconfig recognizes the family and italic/upright classification; this does not establish grouping in every desktop font menu.

The master fixture explicitly repaired 40 equal-topology contour pairs and produced 375 compatible intermediate glyphs. **D, e, 4, é, ê, @, &, $, €, ª** remained topologically incompatible; **?** failed the interpolated self-intersection check. Across three intermediate styles this blocked 33 glyphs. The example-fixture script explicitly supplied independent proposals for those missing glyphs. The application never silently substitutes those proposals for failed interpolation. Published family project approval flags are cleared: automated test approvals are not designer approval.

## Specific defects fixed

- Sanitized SVG imports incorrectly rejected standard namespace declarations; viewport/aspect validation and corrected-raster aspect handling were repaired.
- Narrow-screen controls and glyph/reference bounds could clip or overflow; wrapping and editor fitting were corrected.
- Compound boolean operations could lose nested counters; compound operands and contour orientation are now handled explicitly.
- Accented lowercase i retained its dot; separate-dot replacement, actual-base anchors and lowercase cedilla anchors were corrected.
- Family proposals could reuse upright anatomy decisions or overlook protected overrides; per-style choices and review/propagation gates were added.
- Interpolation could create invalid crossing contours despite matching command topology; self-intersections now block that candidate.
- Exported left side bearings and WOFF head-table checksum handling were corrected and independently parsed.
- Invalid numeric geometry and project/import values had insufficient guards; coordinate/complexity/advance checks now retain the current project on rejection.

## Tests not executed

`file://` startup was attempted and **blocked by Chromium administrator URL policy (`ERR_BLOCKED_BY_ADMINISTRATOR`)**. The policy was not bypassed. All assets are embedded and the application is designed for direct-file operation, but that mode still needs a check on an unrestricted device. Firefox, Safari, physical phones/tablets, desktop installation/font-menu grouping, exhaustive accessibility auditing, maximum-limit stress tests and external designer review were not executed. The shipped examples are technical candidate studies, not approved professional fonts.

## Remaining limitations

Universal automatic reconstruction and faithful alphabet inference are not implemented. Measurement is geometric and modest: bounds, three scanline stem estimates and a long straight edge. Character identification, optical thickness, contrast intent, terminals, serifs, overshoot, ambiguous anatomy and acceptance of missing construction parts require the user. Numerical conflict checks do not recognize every visual incompatibility. Captured components can be envelope-fitted, which may alter subtle proportions; exact-preservation policies reject incompatible transformations.

Humanist, serif/slab, stencil, organic and experimental artwork can be reconstructed and edited, but complex contextual joins, stencil bridges, cursive connectivity and unusual anatomies need manual components or independent glyph drawings. Weight deformation and structural italic recipes are editable starting proposals, not automatic professional family development. Point-count compatibility and explicit resampling cannot prove semantic correspondence or optical quality. Different-topology intermediates require repair or independent drawing.

Coordinates have one-font-unit canonical precision. Booleans flatten curves at 0.6-unit tolerance. Raster tracing is limited to 220 × 280 and perspective correction uses nearest-neighbor sampling. These choices can lose fine detail. SVG import supports plain filled geometry, with strokes/text/filters/resources and nested viewports rejected. Contour self-intersection detection is advisory geometry screening rather than a formal proof for every pathological curve.

No variable-font export, hinting, local-font import, mark-to-mark stacking, arbitrary multi-mark/contextual-script shaping, kerning groups, automatic kerning, vertical typography or optional liquid/pixel tools are offered. Limits and browser support are published in README. Technical validity does not establish visual continuity; overlays, repeated-component comparisons, counter/aperture checks and designer review remain essential.

## Reproduce and inspect

Serve the repository with `python -m http.server 8080`, then run the scripts listed in README. `python tests/native_family_checks.py` additionally requires Fontconfig's `fc-scan`. The FontTools/HarfBuzz validator reads the delivered font files independently from the application's JavaScript writer. To inspect visually, restore `examples/family-study.formaco.json`, compare references/components in Inspection, and review representatives and Portuguese proofs. Download a JSON backup before changing origins or clearing browser storage.
