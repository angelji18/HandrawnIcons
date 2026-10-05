# Icons and doodles: handoff for a new repository

## Goal

Turn a PNG sheet of hand-drawn icons and doodles into individual assets for a
portfolio and other projects. The drawings are arranged in a known grid.
Keep the implementation small, readable, and educational.

```text
PNG sheet → named cell crops → transparent PNGs → optional SVG outlines
                                  ↓                     ↓
                            use in a website       scale smoothly
```

- **PNG:** a pixel image that can preserve colors and transparency.
- **SVG:** shapes described by lines and curves that scale smoothly.
- **Transparency:** removes the sheet background so a drawing can sit on a page.

Transparent PNGs are the first usable deliverable. SVG conversion is a later
step, and the PNG may remain the better version for textured or shaded doodles.
Font generation is not needed for these assets.

## Working preferences

- Explain each new concept briefly before implementing it.
- Give short progress updates at each step.
- Prefer small functions, clear names, and ordinary loops.
- Implement one working milestone at a time; inspect its output before continuing.
- Use Python, Pillow, Git, and `pyproject.toml`.
- Add VTracer only when reaching SVG conversion. No fontTools is needed.
- No OCR, machine learning, automatic naming, web framework, database, or Docker.
- No TDD or pytest scaffolding. Verify the actual outputs and use small synthetic
  images for focused checks when useful.
- Do not commit or push unless explicitly asked. Suggest a commit message at
  each meaningful milestone.

## What to reuse from HandwrittenFont

The reference project is https://github.com/angelji18/HandwrittenFont.

- `extraction.py`: calculate a rectangle from row/column indices and crop with Pillow.
- `__main__.py`: read JSON, create folders, and save named PNGs.
- `vectorize.py`: prepare pixels and call VTracer when SVG conversion is needed.

Use these ideas rather than copying the whole project. There are no character
codes, alphabet styles, spaces, baselines, font metrics, or TTF files here.
An asset is identified by a name such as `sun`, `arrow_right`, or `flower`.

## Initial structure

```text
assets/source/doodles.png
config/sheet.json
src/doodle_assets/__init__.py
src/doodle_assets/__main__.py
src/doodle_assets/extraction.py
pyproject.toml
README.md
.gitignore
build/crops/                 # generated named PNGs
```

Add `prepare.py`, `vectorize.py`, `build/transparent/`, and `build/svg/` only
when their milestone starts. Use Python 3.12, which worked with a prebuilt
VTracer package in the reference project. Pillow is the only initial dependency.
Ignore `.venv/`, `__pycache__/`, `*.egg-info/`, `build/`, and `.DS_Store`.

## Configuration

Use arrays of asset names rather than alphabet strings. This is an example,
not measured coordinates for the new sheet:

```json
{
  "sections": [
    {
      "name": "doodles",
      "grid_left": 20,
      "grid_top": 30,
      "cell_width": 200,
      "cell_height": 200,
      "rows": [
        ["sun", "moon", "star"],
        ["flower", "heart", null]
      ],
      "crop_overrides": {}
    }
  ]
}
```

`null` means an empty cell: skip saving it, but keep its column position.
Names should be unique within a section and use lowercase letters, digits,
and underscores. Save as `build/crops/doodles/sun.png`.
Separate sections allow different layouts or groups on one sheet.

The grid starts at `grid_left`, `grid_top`. Cells include surrounding blank
space; visible grid lines are not required. If cells have separate gaps, add
`column_gap` and `row_gap` only when the actual sheet needs them.
`crop_overrides` can specify exceptional rectangles by asset name.

## Milestone 1: extract grid cells

1. Inspect the new repository and PNG. Measure its actual dimensions and layout.
2. Visually identify the drawings and assign descriptive names. Ask about
   ambiguous drawings rather than inventing their intended meanings.
3. Add the minimal package setup and measured `sheet.json`.
4. Implement `extract_assets(image, section)` and a command that saves the crops.
5. Run it and create a labeled contact sheet under `build/` for review.

Core calculation:

```python
left = grid_left + column_index * cell_width
top = grid_top + row_index * cell_height
box = (left, top, left + cell_width, top + cell_height)
crop = image.crop(box)
```

Pillow excludes the right and bottom edges. Check for duplicate names and
rectangles outside the source image so assets are not silently overwritten
or padded. Confirm each crop contains the intended drawing and no neighbors.
Keep the original colors and pixels at this stage.

Suggested command: `python -m doodle_assets`

Commit point: `feat: extract named doodles from configured grid`

## Milestone 2: prepare transparent PNGs

Start by inspecting the sheet background. For a clean white background, the
simplest method sets near-white pixels' alpha to zero while preserving the
other pixels' colors. Alpha is a pixel's opacity: zero is fully transparent.

This method also removes white inside the artwork. Make background removal
opt-in per asset and skip drawings where white is intentional. If the paper
has shadows or texture, inspect that problem before adding more processing.
Do not promise that a single threshold will clean every drawing.

Save prepared versions separately under `build/transparent/`. Keep the original
crops for comparison. Optionally trim transparent margins and add a small
padding border; preserve aspect ratio instead of stretching drawings.

Verify on both light and dark backgrounds. Look for missing pale colors,
white halos, cut-off strokes, and excessive empty space.

Suggested command: `python -m doodle_assets.prepare`

Commit point: `feat: prepare transparent doodle PNGs`

## Milestone 3: optionally trace SVGs

Start with one drawing. Add [VTracer 0.6.11](https://pypi.org/project/vtracer/0.6.11/),
the version used successfully in the reference project.

- For black line drawings, prepare a black-and-white image and trace in binary mode.
- For colored drawings, preserve colors and use color tracing; inspect the result
  rather than applying the font pipeline's black-and-white threshold.
- Preserve holes, transparent backgrounds, and the original proportions.
- Add a matching SVG `viewBox` so the drawing scales correctly.

Compare the original and traced drawing at small and large sizes. Check thin
lines, enclosed holes, colors, and transparency before processing the whole sheet.
Keep PNGs available if tracing changes a drawing too much.

Suggested command: `python -m doodle_assets.vectorize`

Commit point: `feat: trace selected doodles into SVG assets`

## Milestone 4: use the assets

Copy selected PNGs or SVGs into the portfolio repository's public asset folder,
such as `public/doodles/`. Keep these chosen final assets in that repository's
Git history; intermediate output in this extraction project stays under `build/`.

```html
<img src="/doodles/sun.svg" alt="Hand-drawn sun" width="64" height="64">
```

Use `alt=""` for purely decorative drawings. Display images at their natural
aspect ratio. No JavaScript package or icon font is required.

Commit point: `feat: add portfolio doodle assets`

## First prompt for the new coding session

> Read ICONS_HANDOFF.md and inspect this repository and my PNG sheet. Start
> with milestone 1 only: explain the minimal setup, configure names and grid
> coordinates, crop individual PNGs, and create a contact sheet. Keep functions
> small and explanations short. Do not add transparency, SVG conversion, tests,
> or a website yet. Do not commit or push automatically.
