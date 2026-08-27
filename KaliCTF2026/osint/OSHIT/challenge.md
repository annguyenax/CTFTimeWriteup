# OSHIT

- **Event:** Kali Team - CTF 26
- **Challenge ID:** 19
- **Category:** OSINT
- **Type:** dynamic
- **Points:** 500 *(snapshot; dynamic scoring)*
- **Solves:** 0 *(snapshot)*
- **Solved by me:** false
- **Flag format:** `KaliTeam{...}`
- **Source page:** https://kali-team.online/challenges#OSHIT-19
- **Source:** `_metadata/challenges-compact.json`
- **Author:** Author: S1l3nt

## Prompt (verbatim)

Author: S1l3nt


Asterion Field Services disappeared from public view, but parts of its online infrastructure are still accessible.

A recovered invoice is your only starting point.

Trace the company’s surviving public footprint and correlate the records connected to project NQ-441. The information is distributed across multiple services, archived documents, and project references.

Recover the following:

- The full name of the authorized project contact
- The company registration number
- The internal operations portal identifier
- The receiving warehouse code
- The industrial area associated with the final delivery

Not every useful page is linked directly, and the complete answer cannot be recovered from a single service.

Flag Format:

KaliTeam{CONTACT_REGISTRATION_PORTAL_WAREHOUSE_AREA}

Formatting Rules:

- Use uppercase letters.
- Replace spaces with underscores.
- Preserve numbers and internal codes exactly as written.
- Do not add punctuation.

### Prompt raw (as scraped)

```
<p style="text-align: center">Author: <a href="https://www.linkedin.com/in/ayham-beshtawi-08960a3b7" style="color: #b00dea; font-weight: bold; text-decoration: none;">S1l3nt</a></p>
Asterion Field Services disappeared from public view, but parts of its online infrastructure are still accessible.

A recovered invoice is your only starting point.

Trace the company’s surviving public footprint and correlate the records connected to project NQ-441. The information is distributed across multiple services, archived documents, and project references.

Recover the following:

- The full name of the authorized project contact
- The company registration number
- The internal operations portal identifier
- The receiving warehouse code
- The industrial area associated with the final delivery

Not every useful page is linked directly, and the complete answer cannot be recovered from a single service.

Flag Format:

KaliTeam{CONTACT_REGISTRATION_PORTAL_WAREHOUSE_AREA}

Formatting Rules:

- Use uppercase letters.
- Replace spaces with underscores.
- Preserve numbers and internal codes exactly as written.
- Do not add punctuation.
```

## Attachments

- `paper.png` (2.28 MB)

### Attachment URLs

- paper.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjoyOH0.anMO8A.V-t8PuvxV334T0iyuypwQm16mfw: https://kali-team.online/files/27c200f1d811c24202c6cf86a79d829e/paper.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjoyOH0.anMO8A.V-t8PuvxV334T0iyuypwQm16mfw

## Local layout

- `files/` — original attachments
- `solve/` — solver + evidence
- `writeup/writeup.md` — writeup
- Scratch: `D:\download\ctf-scratch\kalictf______`

## Status

`[ ] unsolved`

## Notes

- Docker challenges need **Start instance** on platform for host:port.
