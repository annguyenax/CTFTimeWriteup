#!/usr/bin/env python3
"""Bounded Street View sweep for the named Hackerman III candidates."""
from __future__ import annotations

import io
import json
import math
import sys
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "solve_vendor"))

import requests
from PIL import Image, ImageDraw
from streetview import search_panoramas


STREETS = [
    ("Aranda", "Bandjalong Crescent"),
    ("Aranda", "Wybalena Grove"),
    ("Aranda", "Bindubi Street"),
    ("Hawker", "Hodgson Crescent"),
    ("Hawker", "Hodgkinson Street"),
    ("Hawker", "Springvale Drive"),
    ("Florey", "Southern Cross Drive"),
    ("Florey", "Maiden Street"),
    ("Florey", "Downie Street"),
    ("Scullin", "Miller Street"),
    ("Scullin", "Schlich Street"),
    ("Cook", "Templeton Street"),
    ("Cook", "Bage Place"),
    ("Cook", "Northcote Crescent"),
    ("Ainslie", "Mackennal Street"),
    ("Ainslie", "Donaldson Street"),
    ("O'Connor", "Dryandra Street"),
]
UA = {"User-Agent": "BushBash-CTF-OSINT/1.0 (bounded research)"}


def haversine(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371000 * 2 * math.asin(math.sqrt(h))


def flatten_geometry(g: dict) -> list[list[tuple[float, float]]]:
    typ, coords = g.get("type"), g.get("coordinates", [])
    if typ == "LineString":
        return [[(float(y), float(x)) for x, y in coords]]
    if typ == "MultiLineString":
        return [[(float(y), float(x)) for x, y in line] for line in coords]
    return []


def sample_line(lines: list[list[tuple[float, float]]], maximum: int = 5) -> list[tuple[float, float]]:
    pts = [p for line in lines for p in line]
    if not pts:
        return []
    # Preserve endpoints/curves but cap requests per street.
    ids = sorted(set(round(i * (len(pts) - 1) / max(1, maximum - 1)) for i in range(min(maximum, len(pts)))))
    return [pts[i] for i in ids]


def geocode(suburb: str, street: str) -> list[tuple[float, float]]:
    q = quote(f"{street}, {suburb}, ACT, Australia")
    url = f"https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&polygon_geojson=1&q={q}"
    rows = requests.get(url, headers=UA, timeout=20).json()
    for row in rows:
        if row.get("category") == "highway" and row.get("geojson"):
            return sample_line(flatten_geometry(row["geojson"]))
    return [(float(rows[0]["lat"]), float(rows[0]["lon"]))] if rows else []


def choose_panos(point: tuple[float, float]):
    near = [p for p in search_panoramas(*point) if haversine(point, (p.lat, p.lon)) < 90]
    if not near:
        return []
    dated = [p for p in near if p.date]
    chosen = []
    if dated:
        chosen += [min(dated, key=lambda p: p.date), max(dated, key=lambda p: p.date)]
    else:
        chosen.append(near[0])
    out = []
    for p in chosen:
        if p.pano_id not in {x.pano_id for x in out}:
            out.append(p)
    return out


def thumbnail(pano_id: str, yaw: float) -> Image.Image:
    url = (
        "https://streetviewpixels-pa.googleapis.com/v1/thumbnail"
        f"?panoid={quote(pano_id)}&cb_client=maps_sv.tactile&w=512&h=384"
        f"&yaw={yaw:.2f}&pitch=0&thumbfov=92"
    )
    response = requests.get(url, headers=UA, timeout=25)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content)).convert("RGB")


def main() -> None:
    outdir = ROOT / "sv_round2"
    outdir.mkdir(exist_ok=True)
    records = []
    seen = set()
    for suburb, street in STREETS:
        points = geocode(suburb, street)
        print(street, "points", points)
        time.sleep(1.05)  # Nominatim policy-friendly pacing.
        for point in points:
            for pano in choose_panos(point):
                for direction, yaw in (("f", pano.heading), ("b", pano.heading + 180)):
                    sig = (pano.pano_id, direction)
                    if sig in seen:
                        continue
                    seen.add(sig)
                    try:
                        image = thumbnail(pano.pano_id, yaw)
                    except Exception as exc:
                        print("thumbnail failed", pano.pano_id, exc)
                        continue
                    name = f"{len(records):04d}_{suburb}_{street}_{direction}.jpg".replace(" ", "_")
                    image.save(outdir / name, quality=90)
                    records.append({
                        "file": name, "suburb": suburb, "street": street,
                        "lat": pano.lat, "lon": pano.lon, "date": pano.date,
                        "pano_id": pano.pano_id, "yaw": yaw % 360,
                    })
    (outdir / "metadata.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    cell_w, cell_h = 256, 216
    cols = 5
    rows = math.ceil(len(records) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, rec in enumerate(records):
        image = Image.open(outdir / rec["file"]).resize((cell_w, 192))
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        sheet.paste(image, (x, y))
        label = f"{i:03d} {rec['street'][:15]} {rec['date'] or '?'} {rec['lat']:.5f},{rec['lon']:.5f}"
        draw.text((x + 2, y + 194), label, fill="black")
    sheet.save(outdir / "contact_sheet.jpg", quality=92)
    print("saved", len(records), "views", outdir / "contact_sheet.jpg")


if __name__ == "__main__":
    main()
