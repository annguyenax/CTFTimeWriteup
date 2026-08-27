# The CSSA Hackerman series — OSINT map

## Confirmed flags (user)

| # | Flag | Place (Nominatim) |
|---|------|-------------------|
| I | `bushbash{-35.2755,149.1207}` | **Skaidrite Darius / CSIT Building 108**, North Rd, **Acton ANU** (CSSA Common Room N102) |
| II | `-35.2356,149.0729` → `bushbash{-35.2356,149.0729}` | Bench **SEAT2150**, **Townsend Place, Belconnen** — Lake Ginninderra looking at Belconnen towers |

## Escape geometry
- I → II: ~**6.2 km**, bearing ~**NW (-44°)**
- III should continue “retreat” → residential Belconnen district or further NW
  (Cook / Aranda / Page / Scullin / Macquarie / Florey / Weetangera / Hawker …)

## III artifact
- Panasonic **NV-DS38** Photoshot 640×480, fake date 2000-01-01, **no GPS**
- Winter bare trees, wide residential street, person + long pole on left verge, dark SUV, white houses, curve ahead
- Reverse image: no web match
- Cubeupload user **oreophone** = GitHub **Adrian Carpio** (CSSA CompProg officer) — likely platform uploader, not necessarily author

## How to finish III (manual Street View)
1. Google Maps Street View, start at Lake Ginninderra / Townsend Place.
2. Sweep residential streets **west/NW of Belconnen** with:
   - large deciduous (plane/elm) verges bare in winter
   - white houses + hedge/fence right
   - dual street lights, power poles left
   - slight curve / mini-roundabout ahead
   - possible multi-storey block visible through trees (Belconnen apartments)
3. Phone: open III JPG → **Google Lens** with location bias **Canberra ACT**.
4. Match curb + tree spacing + house rooflines; flag person position to **4 decimals**.

## Authors
Cameron & Vals (challenge authors).

## Copilot session — Street View sweep log (checked, NOT a match)
Technique that works for automated browsing (for other agents to reuse):
1. Open `https://www.google.com/maps/@LAT,LNG,17z` (plain map first, NOT satellite — WebGL needs a beat to render, screenshot again if black).
2. Drag pegman: `mouse.move(pegmanX,pegmanY) -> mouse.down() -> mouse.move(targetX,targetY,{steps:15}) -> mouse.up()`. Pegman dock icon ~bottom-right of map canvas.
3. If it lands on a covered road it jumps straight to `.../@lat,lng,3a,75y,<heading>h,90t/data=!3m7!1e1!3m5!1s<panoid>!2e0!6shttps:...thumbnail...!7i16384!8i8192` — **must reload/renavigate to that exact full URL (including the `!6s...thumbnail...` part)** for the panorama to actually paint; the in-place drag result sometimes only shows the map with blue coverage overlay.
4. If it opens a small "Images" dialog instead of jumping, the drop point had no coverage — retry a few px away, right on the blue line.

Checked so far — no match (wrong season/vegetation/build):
- **26 Morton St, Weetangera** — native eucalypt garden, overgrown, no wide bare verge.
- **14 Luehmann St, Page** — native trees, fenced yard, caravan blocking.
- Cook (Lyttleton Cres area) — not yet entered street view (viewport/pegman drag failed, info card overlapping).

Reverse-image (Yandex CBIR + Google Lens by-URL) results are **noise**: Elmhurst IL / Christchurch NZ / Merced CA street photos, and one **Limestone Avenue (Ainslie/Braddon/Reid/Campbell)** hit — ruled out, it's a major dual-carriageway arterial, not the quiet suburban street in the photo.

Key open question: our photo's street trees are bare **deciduous** (avenue-planted), but the 2 Belconnen spots checked so far are **native eucalypt** streetscape. Belconnen suburbs mostly use natives; deciduous avenue plantings are more typical of older inner-north suburbs (Ainslie/O'Connor/Turner/Reid) or specific landscaped Belconnen streets — worth checking BOTH inner-north elm suburbs AND more Belconnen streets before assuming the II→III trajectory keeps heading NW.

Next candidate order suggested: Aranda, Macquarie, Hawker, Florey, Scullin (finish Belconnen sweep) — then if still no match, pivot to Ainslie/O'Connor backstreets (not the grand avenues) despite being "backwards" toward ANU.
