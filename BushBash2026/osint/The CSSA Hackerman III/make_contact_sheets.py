import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", type=Path)
    parser.add_argument("images", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.metadata.read_text(encoding="utf-8"))
    groups = {}
    for i, row in enumerate(rows):
        groups.setdefault(row["suburb"], []).append((i, row))
    args.output.mkdir(exist_ok=True)
    for suburb, items in groups.items():
        cols, width, image_height, label_height = 4, 256, 192, 28
        sheet = Image.new("RGB", (cols * width, math.ceil(len(items) / cols) * (image_height + label_height)), "white")
        draw = ImageDraw.Draw(sheet)
        for n, (i, row) in enumerate(items):
            safe_suburb = row["suburb"].replace("'", "").replace(" ", "_")
            safe_street = row["street"].replace("'", "").replace(" ", "_")
            name = f"{i:04d}_{safe_suburb}_{safe_street}_{round(row['yaw']) % 360}.jpg"
            path = args.images / name
            if not path.exists():
                continue
            image = Image.open(path).convert("RGB").resize((width, image_height))
            x = (n % cols) * width
            y = (n // cols) * (image_height + label_height)
            sheet.paste(image, (x, y))
            draw.text((x + 2, y + image_height + 1), f"{i:04d} {row['street'][:20]} {row['date']}", fill="black")
        sheet.save(args.output / f"{suburb.replace(' ', '_')}.jpg", quality=92)


if __name__ == "__main__":
    main()
