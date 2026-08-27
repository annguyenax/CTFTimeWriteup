# Kali Team - CTF 26 challenge archive

**Event:** Kali Team - CTF 26  
**CTFtime:** https://ctftime.org/event/3328  
**Platform:** https://kali-team.online/challenges  
**Scrape:** `_metadata/challenges-full.json` (2026-08-05T10:22:40.288Z)  
**Flag format:** `KaliTeam{...}`

## Layout

```text
KaliCTF2026/
  _metadata/
    challenges-full.json
    challenges-compact.json
    challenges_index.json
  <category>/<challenge>/
    challenge.md
    prompt.md
    files/
    solve/
    writeup/writeup.md
```

| CTFd category | Local folder |
|---|---|
| Warmup | `warmup/` |
| Web | `web/` |
| Guests | `guests/` |
| Pwn | `pwn/` |
| Crypto | `crypto/` |
| Reverse Engineering | `rev/` |
| OSINT | `osint/` |
| Misc | `misc/` |

## Summary

- Challenges: **21**
- With description: **21/21**
- With local files: **13/21**
- Solved by me (snapshot): **1**

### By category

| Category | Count |
|---|---:|
| Crypto | 1 |
| Guests | 3 |
| Misc | 2 |
| OSINT | 5 |
| Pwn | 3 |
| Reverse Engineering | 3 |
| Warmup | 1 |
| Web | 3 |

## Challenges

| ID | Category | Challenge | Points | Solves | Solved | Files | Ready |
|---:|---|---|---:|---:|---|---:|---|
| 39 | Crypto | [Merkle's Trapdoor](crypto/Merkle's%20Trapdoor/challenge.md) | 100 | 283 | no | 0 | desc |
| 22 | Guests | [Havok Trail](guests/Havok%20Trail/challenge.md) | 100 | 250 | no | 0 | desc |
| 48 | Guests | [JordanSec](guests/JordanSec/challenge.md) | 495 | 2 | no | 0 | desc |
| 20 | Guests | [WhoAmI? Cyber-eto](guests/WhoAmI%20Cyber-eto/challenge.md) | 425 | 16 | no | 0 | desc |
| 47 | Misc | [Symphony of Sus](misc/Symphony%20of%20Sus/challenge.md) | 460 | 9 | no | 2 | desc+files |
| 37 | Misc | [call me](misc/call%20me/challenge.md) | 270 | 47 | no | 1 | desc+files |
| 18 | OSINT | [Dead Air](osint/Dead%20Air/challenge.md) | 500 | 1 | no | 1 | desc+files |
| 19 | OSINT | [OSHIT](osint/OSHIT/challenge.md) | 500 | 0 | no | 1 | desc+files |
| 16 | OSINT | [Red Silence](osint/Red%20Silence/challenge.md) | 470 | 7 | no | 1 | desc+files |
| 15 | OSINT | [The Last Shift](osint/The%20Last%20Shift/challenge.md) | 425 | 16 | no | 1 | desc+files |
| 14 | OSINT | [The Unbroken Shelf](osint/The%20Unbroken%20Shelf/challenge.md) | 100 | 82 | no | 1 | desc+files |
| 26 | Pwn | [Leaky](pwn/Leaky/challenge.md) | 180 | 65 | no | 5 | desc+files+need-instance |
| 23 | Pwn | [Warmy](pwn/Warmy/challenge.md) | 100 | 155 | no | 5 | desc+files+need-instance |
| 24 | Pwn | [rayray](pwn/rayray/challenge.md) | 100 | 142 | no | 5 | desc+files+need-instance |
| 32 | Reverse Engineering | [Fault Cartography](rev/Fault%20Cartography/challenge.md) | 100 | 87 | no | 3 | desc+files |
| 43 | Reverse Engineering | [Mr. Beast?????](rev/Mr.%20Beast/challenge.md) | 475 | 6 | no | 3 | desc+files |
| 33 | Reverse Engineering | [The Last Scheduler](rev/The%20Last%20Scheduler/challenge.md) | 500 | 0 | no | 2 | desc+files |
| 7 | Warmup | [W3lc0me!](warmup/W3lc0me!/challenge.md) | 50 | 451 | yes | 0 | desc |
| 50 | Web | [Black Archive](web/Black%20Archive/challenge.md) | 495 | 2 | no | 0 | desc |
| 9 | Web | [Lock Out](web/Lock%20Out/challenge.md) | 100 | 143 | no | 0 | desc+need-instance |
| 8 | Web | [Robots](web/Robots/challenge.md) | 100 | 157 | no | 0 | desc+need-instance |

## Solve readiness

- **Offline-ready (desc + files):** most OSINT/Misc/Rev/Pwn binaries
- **Prompt-only OSINT/search:** Guests, Warmup
- **Crypto in-prompt:** Merkle's Trapdoor (payload in description)
- **Need live instance:** Robots, Lock Out, Warmy, rayray, Leaky (`dynamic_docker`)
- **External URL:** Black Archive → connection_info in challenge.md

## Notes

- Attachment URLs include short-lived tokens; prefer local `files/` copies.
- Disposable work: `D:\download\ctf-scratch\kalictf_<challenge>/`
