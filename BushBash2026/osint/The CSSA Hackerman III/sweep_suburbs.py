#!/usr/bin/env python3
"""Bounded historic Street View sweep over plausible old Canberra suburbs.

This deliberately samples a small regular grid and keeps spatially distinct
nearby panoramas. It is not a city-wide/full scan.
"""
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

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw
from streetview import search_panoramas

SUBURBS = ["Ainslie", "O'Connor", "Turner", "Lyneham", "Reid", "Braddon"]
UA = {"User-Agent": "BushBash-CTF-OSINT/1.0 (bounded research)"}


def distance(a, b):
    y = (a[0] - b[0]) * 111_000
    x = (a[1] - b[1]) * 91_000
    return math.hypot(x, y)


def bbox(suburb):
    q = quote(f"{suburb}, ACT, Australia")
    url = f"https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&polygon_geojson=1&q={q}"
    row = requests.get(url, headers=UA, timeout=20).json()[0]
    south, north, west, east = map(float, row["boundingbox"])
    return south, north, west, east


def grid(box, step_m=250):
    south, north, west, east = box
    dy, dx = step_m / 111_000, step_m / 91_000
    y = south
    while y <= north:
        x = west
        while x <= east:
            yield y, x
            x += dx
        y += dy


def oldest_spatial_panos(point):
    nearby = [p for p in search_panoramas(*point) if distance(point, (p.lat, p.lon)) <= 145]
    nearby.sort(key=lambda p: (p.date or "9999", distance(point, (p.lat, p.lon))))
    picked = []
    for p in nearby:
        if all(distance((p.lat, p.lon), (q.lat, q.lon)) >= 55 for q in picked):
            picked.append(p)
        if len(picked) == 1:
            break
    return picked


def thumbnail(panoid, yaw):
    url = (
        "https://streetviewpixels-pa.googleapis.com/v1/thumbnail"
        f"?panoid={quote(panoid)}&cb_client=maps_sv.tactile&w=512&h=384"
        f"&yaw={yaw:.1f}&pitch=0&thumbfov=78"
    )
    res = requests.get(url, headers=UA, timeout=20)
    res.raise_for_status()
    return Image.open(io.BytesIO(res.content)).convert("RGB")


def orb_score(target_gray, candidate):
    orb = cv2.ORB_create(nfeatures=1400, fastThreshold=8)
    kp1, d1 = orb.detectAndCompute(target_gray, None)
    gray = cv2.cvtColor(np.asarray(candidate), cv2.COLOR_RGB2GRAY)
    kp2, d2 = orb.detectAndCompute(gray, None)
    if d1 is None or d2 is None:
        return 0.0, 0
    matches = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1, d2, k=2)
    good = [m for pair in matches if len(pair) == 2 for m, n in [pair] if m.distance < 0.72 * n.distance]
    return sum(max(0, 80 - m.distance) for m in good) / 80.0, len(good)


def main():
    out = ROOT / "sv_innernorth_fast"
    out.mkdir(exist_ok=True)
    target = cv2.imread(str(ROOT / "hackerman3.jpg"), cv2.IMREAD_GRAYSCALE)
    records, seen = [], set()
    for suburb in SUBURBS:
        box = bbox(suburb)
        print(suburb, box, flush=True)
        time.sleep(1.05)
        for point in grid(box):
            try:
                panos = oldest_spatial_panos(point)
            except Exception as exc:
                print("search failed", point, exc, flush=True)
                continue
            for pano in panos:
                if pano.pano_id in seen:
                    continue
                seen.add(pano.pano_id)
                # Vehicle heading and reverse are the two useful road-facing views.
                for yaw in (round(pano.heading) % 360, round(pano.heading + 180) % 360):
                    try:
                        image = thumbnail(pano.pano_id, yaw)
                    except Exception:
                        continue
                    score, good = orb_score(target, image)
                    name = f"{len(records):05d}_{suburb}_{pano.date or 'nodate'}_{yaw}.jpg".replace("'", "")
                    image.save(out / name, quality=86)
                    records.append({"file": name, "suburb": suburb, "lat": pano.lat,
                                    "lon": pano.lon, "date": pano.date, "pano_id": pano.pano_id,
                                    "yaw": yaw, "orb_score": score, "orb_good": good})
            print(".", end="", flush=True)
    records.sort(key=lambda r: (r["orb_score"], r["orb_good"]), reverse=True)
    (out / "ranking.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    top = records[:100]
    cols, cw, ch = 5, 256, 216
    sheet = Image.new("RGB", (cols*cw, math.ceil(len(top)/cols)*ch), "white")
    draw = ImageDraw.Draw(sheet)
    for i, rec in enumerate(top):
        im = Image.open(out / rec["file"]).resize((cw, 192))
        x, y = (i % cols)*cw, (i // cols)*ch
        sheet.paste(im, (x, y))
        draw.text((x+2, y+193), f"{i:03} {rec['suburb'][:9]} {rec['date']} s={rec['orb_score']:.1f}", fill="black")
    sheet.save(out / "top100.jpg", quality=92)
    print(f"\nsaved {len(records)} views", flush=True)


if __name__ == "__main__":
    main()
