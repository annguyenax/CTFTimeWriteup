# Dead Air

- **Event:** Kali Team - CTF 26
- **Challenge ID:** 18
- **Category:** OSINT
- **Type:** dynamic
- **Points:** 500 *(snapshot; dynamic scoring)*
- **Solves:** 1 *(snapshot)*
- **Solved by me:** false
- **Flag format:** `KaliTeam{...}`
- **Source page:** https://kali-team.online/challenges#Dead%20Air-18
- **Source:** `_metadata/challenges-compact.json`
- **Author:** Author: S1l3nt

## Prompt (verbatim)

Author: S1l3nt


Two damaged records were recovered from an abandoned airport operations desk.

The passenger document no longer identifies its carrier, flight number, or destination. The accompanying operations log is incomplete, and its final station and runway values were deliberately removed.

Reconstruct the movement using the remaining visual evidence and publicly available aviation sources.

Follow the record chronologically. An operational amendment may replace information written earlier in the log, and a runway family or arrival configuration does not necessarily identify the exact runway.

Recover the origin, identify the flight and destination, verify the published schedule, and resolve the final operational record against authoritative aeronautical information.

Preserve official aviation notation.

Flag Format:

KaliTeam{ORIGIN_ICAO_FLIGHT_DESTINATION_IATA_DESTINATION_ICAO_DEPARTURE_ARRIVAL_FREQUENCY_EQUIPMENT_DURATION_OBSERVATION_RECIPROCAL_RUNWAY_ACTIVE_RUNWAY_ELEVATION}

Formatting Rules:

- Use uppercase letters.
- Do not include colons in scheduled times.
- Use the timetable’s equipment code exactly as published.
- Write the flight duration as a number followed by MIN.
- Keep the complete observation group in Zulu notation.
- Write the elevation as a number followed by FT.
- Do not include spaces.

### Prompt raw (as scraped)

```
<p style="text-align: center">Author: <a href="https://www.linkedin.com/in/ayham-beshtawi-08960a3b7" style="color: #b00dea; font-weight: bold; text-decoration: none;">S1l3nt</a></p>
Two damaged records were recovered from an abandoned airport operations desk.

The passenger document no longer identifies its carrier, flight number, or destination. The accompanying operations log is incomplete, and its final station and runway values were deliberately removed.

Reconstruct the movement using the remaining visual evidence and publicly available aviation sources.

Follow the record chronologically. An operational amendment may replace information written earlier in the log, and a runway family or arrival configuration does not necessarily identify the exact runway.

Recover the origin, identify the flight and destination, verify the published schedule, and resolve the final operational record against authoritative aeronautical information.

Preserve official aviation notation.

Flag Format:

KaliTeam{ORIGIN_ICAO_FLIGHT_DESTINATION_IATA_DESTINATION_ICAO_DEPARTURE_ARRIVAL_FREQUENCY_EQUIPMENT_DURATION_OBSERVATION_RECIPROCAL_RUNWAY_ACTIVE_RUNWAY_ELEVATION}

Formatting Rules:

- Use uppercase letters.
- Do not include colons in scheduled times.
- Use the timetable’s equipment code exactly as published.
- Write the flight duration as a number followed by MIN.
- Keep the complete observation group in Zulu notation.
- Write the elevation as a number followed by FT.
- Do not include spaces.
```

## Attachments

- `deadair.png` (3.21 MB)

### Attachment URLs

- deadair.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjo1NX0.anMO8A.cqhbdax0io03bZtE4c7qL45KSjk: https://kali-team.online/files/b5a7d98f79a19d5806c547f044f8b596/deadair.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjo1NX0.anMO8A.cqhbdax0io03bZtE4c7qL45KSjk

## Local layout

- `files/` — original attachments
- `solve/` — solver + evidence
- `writeup/writeup.md` — writeup
- Scratch: `D:\download\ctf-scratch\kalictf_________`

## Status

`[ ] unsolved`

## Notes

- Docker challenges need **Start instance** on platform for host:port.
