# The Unbroken Shelf

- **Event:** Kali Team - CTF 26
- **Challenge ID:** 14
- **Category:** OSINT
- **Type:** dynamic
- **Points:** 100 *(snapshot; dynamic scoring)*
- **Solves:** 82 *(snapshot)*
- **Solved by me:** false
- **Flag format:** `KaliTeam{...}`
- **Source page:** https://kali-team.online/challenges#The%20Unbroken%20Shelf-14
- **Source:** `_metadata/challenges-compact.json`
- **Author:** Author: S1l3nt

## Prompt (verbatim)

Author: S1l3nt


Most of the column was destroyed, the storefront disappeared.
The date was torn away.
One shelf remained untouched.

Find the original issue and reconstruct where and when the blast occurred.

Flag Format:
KaliTeam{NEWSPAPER_YYYY_MM_DD_STREET_NUMBER_STREET_TIME}

Use uppercase letters, replace spaces with underscores, and write the time in 24-hour format.

Example:
KaliTeam{THE_DAILY_RECORD_1918_04_12_72_MAIN_2130}

### Prompt raw (as scraped)

```
<p style="text-align: center">Author: <a href="https://www.linkedin.com/in/ayham-beshtawi-08960a3b7" style="color: #b00dea; font-weight: bold; text-decoration: none;">S1l3nt</a></p>
Most of the column was destroyed, the storefront disappeared.
The date was torn away.
One shelf remained untouched.

Find the original issue and reconstruct where and when the blast occurred.

Flag Format:
KaliTeam{NEWSPAPER_YYYY_MM_DD_STREET_NUMBER_STREET_TIME}

Use uppercase letters, replace spaces with underscores, and write the time in 24-hour format.

Example:
KaliTeam{THE_DAILY_RECORD_1918_04_12_72_MAIN_2130}
```

## Attachments

- `The-Unbroken-Shelf-Final.png` (2.04 MB)

### Attachment URLs

- The-Unbroken-Shelf-Final.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjoyNX0.anMO7g.4ZZXIuiwtCJ1RNoaZAxn6s69cBU: https://kali-team.online/files/32535e5ff5a3cd5d4e14431a696e0349/The-Unbroken-Shelf-Final.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjoyNX0.anMO7g.4ZZXIuiwtCJ1RNoaZAxn6s69cBU

## Local layout

- `files/` — original attachments
- `solve/` — solver + evidence
- `writeup/writeup.md` — writeup
- Scratch: `D:\download\ctf-scratch\kalictf___________________`

## Status

`[x] solved` — `KaliTeam{NEW_YORK_TRIBUNE_1920_08_21_157_EIGHTH_AVENUE_2040}`
(New-York Tribune, 1920-08-21, p.1 — Slater & Halpern's drug store, 157 Eighth Avenue, ~8:40 p.m.)

## Notes

- Docker challenges need **Start instance** on platform for host:port.
