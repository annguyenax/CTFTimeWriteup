#!/usr/bin/env python3
import argparse
import json
import time
from pathlib import Path
from urllib.parse import quote

import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.metadata.read_text(encoding="utf-8"))
    args.output.mkdir(exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0", "Referer": "https://www.google.com/maps/"})
    for i, row in enumerate(rows):
        safe_suburb = row["suburb"].replace("'", "").replace(" ", "_")
        safe_street = row["street"].replace("'", "").replace(" ", "_")
        name = f"{i:04d}_{safe_suburb}_{safe_street}_{round(row['yaw']) % 360}.jpg"
        path = args.output / name
        if path.exists():
            continue
        url = ("https://streetviewpixels-pa.googleapis.com/v1/thumbnail"
               f"?panoid={quote(row['panoid'])}&cb_client=maps_sv.tactile&w=512&h=384"
               f"&yaw={row['yaw']:.1f}&pitch=0&thumbfov=78")
        response = None
        for attempt in range(4):
            response = session.get(url, timeout=20)
            if response.ok:
                break
            if response.status_code not in {429, 500, 502, 503, 504}:
                response.raise_for_status()
            time.sleep(1.5 * (attempt + 1))
        if response is None or not response.ok:
            print(f"skip {i}: HTTP {getattr(response, 'status_code', 'none')}", flush=True)
            continue
        path.write_bytes(response.content)
        if (i + 1) % 100 == 0:
            print(f"downloaded {i + 1}/{len(rows)}", flush=True)


if __name__ == "__main__":
    main()
