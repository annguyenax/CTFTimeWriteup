# The Last Shift

- **Event:** Kali Team - CTF 26
- **Challenge ID:** 15
- **Category:** OSINT
- **Type:** dynamic
- **Points:** 425 *(snapshot; dynamic scoring)*
- **Solves:** 16 *(snapshot)*
- **Solved by me:** false
- **Flag format:** `KaliTeam{...}`
- **Source page:** https://kali-team.online/challenges#The%20Last%20Shift-15
- **Source:** `_metadata/challenges-compact.json`
- **Author:** Author: S1l3nt

## Prompt (verbatim)

Author: S1l3nt


Someone shared more than they intended from backstage.

By the time the organizers noticed, the post had already been deleted. All that remains is a captured copy and whatever traces its author forgot to clean up elsewhere online.

Identify the volunteer’s full name, volunteer ID, assigned work zone, and the exact neighborhood associated with their online activity.

Flag Format:
KaliTeam{FIRST_LAST_VOLUNTEER_ID_ZONE_NEIGHBORHOOD}

Example Flag:
KaliTeam{ALEX_JACKSON_VT26-904_D7_SHMEISANI}

### Prompt raw (as scraped)

```
<p style="text-align: center">Author: <a href="https://www.linkedin.com/in/ayham-beshtawi-08960a3b7" style="color: #b00dea; font-weight: bold; text-decoration: none;">S1l3nt</a></p>
Someone shared more than they intended from backstage.

By the time the organizers noticed, the post had already been deleted. All that remains is a captured copy and whatever traces its author forgot to clean up elsewhere online.

Identify the volunteer’s full name, volunteer ID, assigned work zone, and the exact neighborhood associated with their online activity.

Flag Format:
KaliTeam{FIRST_LAST_VOLUNTEER_ID_ZONE_NEIGHBORHOOD}

Example Flag:
KaliTeam{ALEX_JACKSON_VT26-904_D7_SHMEISANI} 
```

## Attachments

- `evidence.png` (1.42 MB)

### Attachment URLs

- evidence.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjoyNn0.anMO7w.dQVXWGneKAhMp5BI7sD2B7UrVvg: https://kali-team.online/files/2d06107cdd1a1ae866d5945dabfd714c/evidence.png?token=eyJ1c2VyX2lkIjoyMjc5LCJ0ZWFtX2lkIjoxMTczLCJmaWxlX2lkIjoyNn0.anMO7w.dQVXWGneKAhMp5BI7sD2B7UrVvg

## Local layout

- `files/` — original attachments
- `solve/` — solver + evidence
- `writeup/writeup.md` — writeup
- Scratch: `D:\download\ctf-scratch\kalictf_______________`

## Status

`[ ] unsolved`

## Notes

- Docker challenges need **Start instance** on platform for host:port.
