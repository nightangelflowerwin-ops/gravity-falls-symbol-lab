# Gravity Falls symbol and runic calendar lab

Open the live dashboard at https://nightangelflowerwin-ops.github.io/gravityfallssymbollab/ in Chrome or Edge, or open **index.html** locally. It is a standalone file and works offline. No installation, API key, server, or image upload to an external service is required.

## Use it

1. Choose a supplied sample, or upload an image.
2. For a larger image, drag around one line of geometric symbols and click **Use selection**.
3. Choose **Russian adaptation**, **Bill Cipher · English**, or **Compare both**.
4. Click **Translate image**. Adjust contrast for faint strokes, or rotate/mirror the crop.
5. Click any detected symbol to review its three closest matches. You can correct the result or teach the dictionary a new glyph. Export your dictionary to keep those additions.
6. Run the image tests and filter their outputs by dictionary. Export results as JSON.

## Included dictionaries

- **Bill Cipher English:** all 26 letters from a community reference chart, with seven additional glyph examples from the supplied image.
- **Russian adaptation:** 27 distinct Russian letters found in this artwork, plus the word-separator symbol and a recorded unresolved glyph. It is a partial, custom adaptation. It is not a complete official Cyrillic Gravity Falls alphabet.
- **English meanings:** the published Russian phrases and a small Russian word glossary. New sentences receive word glosses; unfamiliar words remain in brackets. This is not a general machine-translation service.

Image recognition uses local contrast, glyph segmentation, shape normalization, and template matching. It does not select characters from the expected text. Match scores are shape similarities, not calibrated probabilities. The adaptation and English key must stay separate: identical shapes can represent different letters.

## Verification on 2026 10 05

Six supplied image crops reproduce the expected text. These are **same-image checks** because templates include examples from that artwork. The right-border check preserves its final mark as unresolved; a 100% text match does not decipher that mark.

Two stricter checks expose the remaining recognition limits:

| Check | Recognized text | Character accuracy |
| --- | --- | --- |
| Russian lower-left crop, with its own templates excluded | `сумма двув чисел` | 92.9% |
| Tuesday crop, using only the separate English alphabet chart | `MFESDAY` | 71.4% |
| Blank white image | No characters | Pass |

The Russian held-out check still uses other glyphs from the same artwork. The English chart-only check compares two drawing styles. Neither result establishes accuracy on arbitrary photographs, handwriting, backgrounds, or other Gravity Falls alphabets. Crop closely, review alternatives, and add examples when needed.

Thirteen browser checks passed: sample switching, English meaning, dictionary comparison, correction, dictionary export/import, malformed-import rejection, rotation and mirroring round trips, upload and drag crop, test filtering, result export, and a 390-pixel mobile layout without page overflow. No browser script errors occurred.

## Files

- `gravity-falls-image-dictionary.html`: complete local application, image samples, dictionaries, and test bench.
- `gravity-falls-dictionary.json`: importable template dictionary exported by the application.
- `gravity-falls-sample-result.json`: example output for the lower-left crop, including symbol matches and test results.
- `gravity-falls-test-report.json`: recorded test outputs and browser verification.

## Sources

- [Readings of this exact image](https://github.com/HomelessPhD/BLM_0.2BTC/blob/main/README.md)
- [Russian mapping analysis](https://github.com/rarsn4/blm-0.2btc-analysis/blob/main/STATUS.md)
- [Community Bill Cipher alphabet chart](https://i.pinimg.com/originals/d4/09/61/d40961eb7207d99d5eec4b9d9069d018.jpg)
- [Bill Cipher alphabet description](https://www.dcode.fr/gravity-falls-bill-cipher)

The symbol dictionary retains provenance labels. Russian assignments are based on community plaintext readings and repeated glyphs, not an author-supplied key. User additions are labeled annotations. Uploaded image content is treated as data, not instructions.


## Runic calendar experiment

The calendar panel compares six supplied sections against five interpretations: golden numbers 1–19, the attested l/m order variant, the seven-symbol weekday row, Younger Futhark letters, and an Elder Futhark comparison. Unknown positions remain visible. Ingwaz ᛜ/ᛝ belongs to the Elder comparison and has no value in the 19-symbol calendar key.

The recorded audit contains 360 comparisons: six sections × four whole-line orientations × three score/lead settings × five interpretations. At 78% shape similarity and an 8% lead over the next value, the calendar and Younger keys accepted no artwork glyphs. At permissive 55%/0%, some rows reach complete shape coverage. These forced assignments do not establish language, a calendar row, or a hidden date. No verified calendar interpretation was found. This only tests the included font variants and matching method; it is not proof that every possible runic interpretation is impossible.

Thirteen calendar controls pass, including a rendered 19-rune reference image, unknown preservation, rejected lookalikes, Ingwaz handling, order variants, date validation, and 19-year arithmetic. Modern Gregorian checks independently give Monday for 2020-05-25 and Tuesday for 2020-11-03, with golden number 7 in both cases. They are not readings extracted from the symbols.

Open the recorded sensitivity audit to filter by settings and interpretation. Review candidates or enter an actual rune transcription. Typed identities are annotations, not image recognition evidence. Export the experiment to retain scores, alternatives, unknown positions, controls and the recorded audit. Images are processed locally.

## Rebuild and test

Run `python build.py` to recreate `index.html` from `src/`. The build uses only the Python standard library. To verify in a browser, install Node.js, run `npm install`, `npx playwright install chromium`, then `npm test`. Set `BROWSER_CHANNEL=chrome` to use an installed Chrome browser. CI rebuilds the app and runs these browser checks.

Reports live in `reports/`. The template dictionary is separate from the calendar reference key. Reference-font image controls are reproduction controls, not measured accuracy on historic carvings or arbitrary images.

## Calendar sources and attribution

- [Unicode Runic block](https://www.unicode.org/charts/PDF/U16A0.pdf): character identities and the three additional golden-number runes.
- [Helmer Gustavson, Situne Dei 2013](https://www.raa.se/app/uploads/2017/08/SD2013-HG.pdf): historical calendar rows, 19-year cycle and rune-order variations.
- [Sörmlands museum calendar staff](https://sokisamlingar.sormlandsmuseum.se/objects/c24-363410/): day and golden-number rows.
- [US Naval Observatory calendar introduction](https://aa.usno.navy.mil/faq/calendars): the Metonic cycle and golden numbers.
- [Noto Sans Runic](https://github.com/googlefonts/noto-fonts): embedded reference font, under the SIL Open Font License, copied in `licenses/`.

The supplied artwork and community reference chart retain their respective rights. Their inclusion does not assert ownership or grant redistribution rights. Source image attribution was not supplied. This repository is public at the uploader's request. Consult rights holders before further redistribution. No credentials are included.
