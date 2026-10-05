# Hand-drawn icons and doodles

Extract and prepare transparent PNGs from hand-drawn sheets: 16 icons with
main, hover, and pressed states, plus 18 extra doodles.

## Run

Requires Python 3.12 or newer. Run from this folder:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m doodle_assets
python -m doodle_assets.prepare
```

## Files

- `assets/sources/` — original PNG sheets.
- `config/sheet.json` — names, crop coordinates, and transparency settings.
- `src/doodle_assets/` — cropping and preparation code.
- `build/crops/` — original crops.
- `build/transparent/` — PNGs to use in your portfolio.
- `build/*.png` — labeled previews on light and dark backgrounds.

Generated files in `build/` are ignored by Git. Rerun both commands after
changing crop coordinates.

## Use

Copy selected files from `build/transparent/` into your portfolio's assets folder.
Keep the same display width across interaction states; their positions are aligned.
These pencil drawings look best on light backgrounds.
