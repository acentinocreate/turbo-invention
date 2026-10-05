# Original candidate studies

These are original starter/component constructions and automated test fixtures, not polished fonts or externally supplied artwork. No third-party typeface outlines were used.

`FormacoStudy-family.zip` contains the ten 300/400/500/600/700 upright/italic snapshots, editable project and coverage/licence README. Individual `.otf` and `.woff` copies are provided. `family-study.formaco.json` opens the same editable family with unreviewed candidate states; approval flags used by automated master tests are cleared before packaging. A style's independent drawings and compatible interpolations are recorded in glyph relationships. The fixture explicitly retains independently generated proposals where Light/Bold topology differed; the production app never silently fills interpolation failures.

`starter-study.formaco.json` and SVG proofs were produced by the reference/import tests. They also include deliberately modified test references and are examples of saved state, not a visual-quality endorsement. `regular-O.svg` is a contour export. `portuguese-proof.svg` demonstrates the required repertoire.

Original application starter drawings and generated example candidates are distributed under the MIT licence in the repository's LICENSE. Family fixture font metadata records that licence. Some earlier single-style diagnostic artifacts/project metadata may retain the application's conservative default “All rights reserved”; the final family fonts and ZIP are the intended MIT publication examples. No user's reference material is included.

Regenerate these files with the browser/family tests and independently inspect them with `tests/validate_fonts.py`. Technical parsing and shaping success is not professional visual approval.
