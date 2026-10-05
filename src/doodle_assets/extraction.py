"""Turn configured grid cells into named crops."""

import re


def extract_assets(image, section):
    """Return (name, image) pairs, preserving the source pixels."""
    crops = []
    names = set()
    overrides = section.get("crop_overrides", {})
    for row_index, row in enumerate(section["rows"]):
        for column_index, name in enumerate(row):
            if name is None:
                continue
            if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", name):
                raise ValueError(f"Invalid asset name: {name!r}")
            if name in names:
                raise ValueError(f"Duplicate asset name: {name}")
            names.add(name)
            left = section["grid_left"] + column_index * section["cell_width"]
            top = section["grid_top"] + row_index * section["cell_height"]
            box = overrides.get(name, [left, top, left + section["cell_width"],
                                       top + section["cell_height"]])
            if len(box) != 4 or any(type(value) is not int for value in box):
                raise ValueError(f"{name}: crop must contain four integer coordinates")
            left, top, right, bottom = box
            if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
                raise ValueError(f"{name}: crop {box} is outside the source image")
            crops.append((name, image.crop(box)))
    unknown = set(overrides) - names
    if unknown:
        raise ValueError(f"Overrides refer to unknown assets: {sorted(unknown)}")
    return crops
