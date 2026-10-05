"""Remove a white background and trim matching interaction states together."""

import json
from pathlib import Path

from PIL import Image

from .__main__ import save_contact_sheet


def remove_white(image, threshold=254):
    """Replace a white matte with alpha, retaining appearance on white."""
    pixels = []
    source = image.convert("RGBA")
    for red, green, blue, original_alpha in source.get_flattened_data():
        white = min(red, green, blue)
        if white >= threshold or original_alpha == 0:
            pixels.append((0, 0, 0, 0))
            continue
        # Reverse the blend: visible color = foreground * alpha + white * (1-alpha).
        strength = 255 - white
        color = tuple(round((channel - white) * 255 / strength)
                      for channel in (red, green, blue))
        alpha = round(strength * original_alpha / 255)
        pixels.append((*color, alpha))
    result = Image.new("RGBA", image.size)
    result.putdata(pixels)
    return result


def trim_states(images, padding=12):
    """Use one shared bounding box so all states keep their size and position."""
    if len({image.size for image in images.values()}) != 1:
        raise ValueError("Interaction states must have matching crop sizes")
    boxes = [image.getchannel("A").getbbox() for image in images.values()]
    boxes = [box for box in boxes if box is not None]
    if not boxes:
        raise ValueError("Background removal left an empty drawing")
    box = (min(b[0] for b in boxes), min(b[1] for b in boxes),
           max(b[2] for b in boxes), max(b[3] for b in boxes))
    trimmed = {}
    for state, image in images.items():
        crop = image.crop(box)
        canvas = Image.new("RGBA", (crop.width + 2 * padding,
                                    crop.height + 2 * padding))
        canvas.paste(crop, (padding, padding))
        trimmed[state] = canvas
    return trimmed


def main():
    config = json.loads(Path("config/sheet.json").read_text())
    settings = config.get("preparation", {})
    threshold = settings.get("white_threshold", 254)
    padding = settings.get("padding", 12)
    if type(threshold) is not int or not 1 <= threshold <= 255:
        raise ValueError("white_threshold must be an integer from 1 to 255")
    if type(padding) is not int or padding < 0:
        raise ValueError("padding must be a nonnegative integer")
    previews = {state: [] for state in config["sources"]}
    for section in config["sections"]:
        names = {name for row in section["rows"] for name in row if name is not None}
        selected = section.get("remove_white", [])
        if len(selected) != len(set(selected)) or set(selected) - names:
            raise ValueError(f"{section['name']}: remove_white has duplicate or unknown names")
        for name in selected:
            images = {}
            for state in section["states"]:
                path = Path("build/crops") / state / section["name"] / f"{name}.png"
                if not path.exists():
                    raise FileNotFoundError(f"Missing {path}; run python -m doodle_assets first")
                with Image.open(path) as image:
                    images[state] = remove_white(image, threshold)
            for state, image in trim_states(images, padding).items():
                folder = Path("build/transparent") / state / section["name"]
                folder.mkdir(parents=True, exist_ok=True)
                image.save(folder / f"{name}.png")
                previews[state].append((f"{section['name']}/{name}", image))
    for state, assets in previews.items():
        if not assets:
            continue
        for theme, background in [("light", "#f7f4ef"), ("dark", "#242730")]:
            path = Path("build") / f"transparent_{state}_{theme}.png"
            save_contact_sheet(assets, path, background)
        print(f"{state}: saved {len(assets)} transparent PNGs and light/dark previews")


if __name__ == "__main__":
    main()
