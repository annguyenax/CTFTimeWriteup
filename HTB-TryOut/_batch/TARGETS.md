# HTB Try Out — target snapshot (2026-08-19). Port đổi nếu reset instance → cập nhật lại.
# Team FWM: 6/37 solved. Mỗi bài = 1 agent (tránh đụng cùng docker).

## Remote (điền TARGET vào target.txt của từng folder đã có sẵn)
| Bài | TYPE | host:port | Giao agent |
|---|---|---|---|
| web/Blueprint Heist | Web | 154.57.164.68:31206 | Grok |
| web/Flag Command | Web | 154.57.164.82:32021 | Grok |
| web/Guild | Web | 154.57.164.82:31795 | Grok |
| web/HTB Proxy | Web | 154.57.164.77:32208 | Grok |
| web/Labyrinth Linguist | Web | 154.57.164.72:30986 | Grok |
| web/TimeKORP | Web | 154.57.164.82:30695 | Grok |
| pwn/Abyss | TCP | 154.57.164.67:31593 | Codex |
| pwn/Getting Started | TCP | 154.57.164.68:32156 | Codex |
| pwn/Regularity | TCP | 154.57.164.78:31832 | Codex |
| pwn/Router Web | Web | 154.57.164.68:31010 | Codex |
| pwn/Labyrinth | ? | (JSON cắt — bạn điền) | Codex |
| pwn/Void | ? | (JSON cắt — bạn điền) | Codex |
| misc/Character | TCP | 154.57.164.70:31566 | Gemini |
| misc/Chrono Mind | Web | 154.57.164.75:31416 | Gemini |
| misc/Hidden Path | Web | 154.57.164.75:32093 | Gemini |
| misc/Locked Away | TCP | 154.57.164.73:30826 | Gemini |
| misc/Prison Pipeline | Web | 154.57.164.64:31567 | Gemini |
| misc/Stop Drop and Roll | TCP | 154.57.164.75:31750 | Gemini |
| forensics/An unusual sighting | TCP | 154.57.164.69:32684 | Gemini |
| forensics/Silicon Data Sleuthing | TCP | 154.57.164.75:30628 | Gemini |
| coding/Dynamic Paths | TCP | 154.57.164.66:32355 | Codex |
| blockchain/NotADemocraticElection | TCP | 154.57.164.70:30219 (+32293) | DeepSeek |
| general/Welcome to CTF | Web | 154.57.164.82:30156 | Claude |
| crypto/Blessed | TCP | 154.57.164.66:31963 | Claude/Gemini |

## File-only (KHÔNG cần remote — flag nằm trong files/)
| Bài | Giao |
|---|---|
| crypto/Dynastic | Claude |
| forensics/Phreaky | Gemini |
| ics/Shush Protocol | DeepSeek |
| hw/Critical Flight | DeepSeek |
| hw/Debug | DeepSeek |
| hw/It's Oops PM | DeepSeek (TCP nhưng có file để phân tích trước) |
| rev/TunnelMadness | DeepSeek |

## ĐÃ SOLVED trên HTB (đừng giải lại) — 6 bài
rev/FlagCasino, rev/LootStash, rev/Don't Panic!, rev/Satellite Hijack, web/Jailbreak, web/OmniWatch
LƯU Ý: FlagCasino/LootStash/Don't Panic! có flag trên HTB nhưng LOCAL CHƯA có writeup → chỉ cần bổ sung writeup, không giải lại.
