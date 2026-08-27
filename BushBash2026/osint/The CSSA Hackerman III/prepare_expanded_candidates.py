#!/usr/bin/env python3
"""Bounded sweep of older Canberra streets with many exotic deciduous trees."""
from pathlib import Path
from urllib.parse import quote
import argparse
import json
import math
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "solve_vendor"))

import requests
from streetview import search_panoramas

STREETS = [
    ("Downer", "Atherton Street"), ("Downer", "Blacket Street"),
    ("Duffy", "Somerset Street"), ("Duffy", "Tullaroop Street"),
    ("Duffy", "Burdekin Street"), ("Duffy", "Kallara Close"),
    ("Deakin", "Strickland Crescent"), ("Deakin", "Newdegate Street"),
    ("Deakin", "Macgregor Street"), ("Deakin", "Grey Street"),
    ("Deakin", "Canterbury Crescent"),
    ("Hughes", "Goble Street"), ("Hughes", "Bamford Street"),
    ("Hughes", "Groom Street"),
    ("Lyons", "Burnie Street"), ("Lyons", "Deloraine Street"),
    ("Lyons", "Ulverstone Street"),
    ("Torrens", "Brookman Street"), ("Torrens", "Jefferis Street"),
    ("Curtin", "Allan Street"),
    ("Chifley", "Gledden Street"), ("Chifley", "Wilsmore Crescent"),
    ("Chifley", "Maclaurin Crescent"),
    ("Fisher", "Rossarden Street"), ("Fisher", "Chillagoe Street"),
    ("Waramanga", "Nangor Street"), ("Waramanga", "Woralul Street"),
    ("Waramanga", "Alawa Street"),
    ("Mawson", "Hurley Street"), ("Mawson", "Wilkins Street"),
    ("Mawson", "Hoseason Street"),
    ("Kambah", "Ivo Whitton Circuit"), ("Kambah", "McDermott Street"),
    ("Kambah", "Wyselaskie Circuit"),
    ("Red Hill", "Golden Grove"), ("Red Hill", "Torres Street"),
    ("Red Hill", "Investigator Street"),
    ("Campbell", "Blamey Crescent"),
    ("Watson", "A'Beckett Street"), ("Watson", "Irvine Street"),
    ("Watson", "Piddington Street"),
]

UA = {"User-Agent": "BushBash-CTF-OSINT/1.0 (bounded research)"}


def flatten(geometry):
    coords = geometry.get("coordinates", [])
    if geometry.get("type") == "LineString":
        return [(y, x) for x, y in coords]
    if geometry.get("type") == "MultiLineString":
        return [(y, x) for line in coords for x, y in line]
    return []


def sample(points, n=6):
    if not points:
        return []
    indices = sorted(set(round(j * (len(points) - 1) / max(1, n - 1)) for j in range(min(n, len(points)))))
    return [points[i] for i in indices]


def distance(a, b):
    return math.hypot((a[0] - b[0]) * 111_000, (a[1] - b[1]) * 91_000)


def choose_panos(point):
    nearby = [p for p in search_panoramas(*point) if p.date and distance(point, (p.lat, p.lon)) < 90]
    if not nearby:
        return []
    nearby.sort(key=lambda p: p.date)
    chosen = [nearby[0]]
    winter = [p for p in nearby if p.date[5:7] in {"06", "07", "08"}]
    if winter:
        chosen.append(winter[-1])
    result = []
    for pano in chosen:
        if pano.pano_id not in {p.pano_id for p in result}:
            result.append(pano)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--streets-json", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "expanded_candidates.json")
    args = parser.parse_args()
    streets = STREETS
    if args.streets_json:
        streets = [tuple(item) for item in json.loads(args.streets_json.read_text(encoding="utf-8"))]
    out = []
    seen = set()
    for suburb, street in streets:
        query = quote(f"{street}, {suburb}, ACT, Australia")
        rows = requests.get(
            f"https://nominatim.openstreetmap.org/search?format=jsonv2&limit=3&polygon_geojson=1&q={query}",
            headers=UA, timeout=20,
        ).json()
        points = []
        for row in rows:
            points = flatten(row.get("geojson", {}))
            if points:
                break
        points = sample(points)
        print(suburb, street, len(points), flush=True)
        time.sleep(1.05)
        for point in points:
            for pano in choose_panos(point):
                if pano.pano_id in seen:
                    continue
                seen.add(pano.pano_id)
                for yaw in (pano.heading, (pano.heading + 180) % 360):
                    out.append({"suburb": suburb, "street": street, "lat": pano.lat, "lon": pano.lon,
                                "date": pano.date, "panoid": pano.pano_id, "yaw": yaw})
    args.output.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("views", len(out), flush=True)


if __name__ == "__main__":
    main()
