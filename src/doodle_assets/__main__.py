"""Run from the repository root with python -m doodle_assets."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .extraction import extract_assets


def save_contact_sheet(assets, path, background="#eeeeee"):
    """Make a labeled preview; resizing here never changes the saved crops."""
    columns = 6
    tile_width, tile_height = 210, 235
    rows = (len(assets) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * tile_width, rows * tile_height), background)
    draw = ImageDraw.Draw(sheet)
    for index, (label, crop) in enumerate(assets):
        x = (index % columns) * tile_width
        y = (index // columns) * tile_height
        preview = ImageOps.contain(crop, (200, 200))
        mask = preview.getchannel("A") if preview.mode == "RGBA" else None
        sheet.paste(preview, (x + (tile_width - preview.width) // 2,
                             y + (200 - preview.height) // 2), mask)
        # A white label strip stays readable on both preview backgrounds.
        draw.rectangle((x, y + 202, x + tile_width - 1, y + tile_height - 1), fill="white")
        draw.text((x + 6, y + 208), label, fill="black")
    sheet.save(path)


def main():
    config = json.loads(Path("config/sheet.json").read_text())
    output = Path("build")
    output.mkdir(exist_ok=True)
    for state, source in config["sources"].items():
        preview_assets = []
        with Image.open(source) as image:
            for section in config["sections"]:
                if state not in section["states"]:
                    continue
                crops = extract_assets(image, section)
                folder = output / "crops" / state / section["name"]
                folder.mkdir(parents=True, exist_ok=True)
                for name, crop in crops:
                    crop.save(folder / f"{name}.png")
                    preview_assets.append((f"{section['name']}/{name}", crop))
        save_contact_sheet(preview_assets, output / f"contact_{state}.png")
        print(f"{state}: saved {len(preview_assets)} crops and build/contact_{state}.png")


if __name__ == "__main__":
    main()
