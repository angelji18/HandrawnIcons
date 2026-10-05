# Hand-drawn icons and doodles

Extract named PNGs, then prepare transparent versions for a portfolio.
The 16 interactive icons share crop coordinates across main, hover, and pressed
states. The other 18 doodles exist only on the main sheet.

## Run

From this folder, create a local Python environment and install the package:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m doodle_assets
python -m doodle_assets.prepare
```

The virtual environment (`.venv`) keeps this project's Python dependencies local.
The editable install (`-e`) lets Python use the code in `src` as you change it.

## Where things live

- `assets/sources/`: original sheets; leave these untouched.
- `config/sheet.json`: names, states, and crop coordinates in source pixels.
- `src/doodle_assets/extraction.py`: grid calculation and crop validation.
- `src/doodle_assets/__main__.py`: save crops and labeled contact sheets.
- `src/doodle_assets/prepare.py`: white background removal and shared trimming.
- `build/crops/main/icons/home.png`: example extracted asset.
- `build/transparent/main/icons/home.png`: prepared asset for your portfolio.
- `build/contact_main.png`, `contact_hover.png`, `contact_pressed.png`: previews.
- `build/transparent_main_light.png` and `transparent_main_dark.png`: transparency
  previews; hover and pressed have matching preview files.

## Adjusting a crop

Each position in `rows` is one grid cell. `null` skips a cell without shifting
the next drawing. A name identifies a drawing, not its meaning in the portfolio;
rename generic names such as `frame_1` when you decide how to use them.

Grid crops use `left + column × cell_width` and `top + row × cell_height`.
For drawings that do not fit the grid, use `crop_overrides` with
`[left, top, right, bottom]`. Right and bottom edges are excluded by Pillow.
The same override applies to every state in that section, keeping interaction
images aligned. Rerun the command after edits; renamed assets leave old files
in `build`, so remove those old files yourself if needed.

## Transparent PNGs

After extracting crops, run `python -m doodle_assets.prepare`. Original crops
stay in `build/crops`; prepared files go in `build/transparent`.

Each section's `remove_white` list explicitly selects drawings for preparation.
Remove a name from that list to skip it if white is intentional inside the art.
Skipping a name does not delete an already generated file.

Alpha is opacity: 0 is transparent and 255 is opaque. Rather than leaving pale
white edges, the tool reverses the artwork's blend with white into foreground
color and partial alpha. On white, this reproduces the source appearance to
within rounding, except for almost-white pixels removed by the threshold.
Stored RGB values change, while the visible pencil texture and colored washes
remain. The original foreground color and opacity cannot be recovered uniquely
from a flattened image; this is a practical approximation for these sheets.

`preparation.white_threshold` is 254: pixels whose red, green, and blue channels
are all at least 254 become fully transparent. Use 255 to retain the faintest
nonwhite marks. Lower values remove more pale marks and can erase soft shading.
`preparation.padding` adds 12 transparent pixels around each trimmed drawing.

The tool combines the visible bounds of main, hover, and pressed before trimming.
Every state then gets the same rectangle and padding, so interaction stays aligned.
Use the same display width for all three states and let height follow naturally.

Check the light and dark previews. The dark pencil lines suit light surfaces;
transparency does not make them brighter on dark ones. Faint stray marks already
in the source remain, and intentional white fills are removed too. SVG tracing
is optional later. No website, icon font, or JavaScript package is needed here.
