# Tiger Bạc SESSION

Prompt (user): AI-abused software; after drinking with the dev team, **luonginfosec** accidentally pushed the project. Things happened quickly; maybe nobody noticed.

No attachment in `files/` (empty). Treat as OSINT → reverse.

## Entities

- Handle: `luonginfosec` (LuongVD / Vũ Đức Lương, PTIT)
- GitHub: https://github.com/luonginfosec
- FB: https://www.facebook.com/luongptit/
- TG: https://t.me/Luong7474
- Email: luonginfosec@gmail.com

## Leak: `luonginfosec/key`

License dump hosted as `key.html`, then wiped.

Current HEAD `key.html`:
```json
{ "key": [ ] }
```

Commit `85ff9ff4` (2026-07-31) **deleted** the serial.
Older commit `834a83c3` / `298bdfce` still have:

```
1694532157069890…09594612221|6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL
```

- Left: 617-digit **2048-bit** integer
- Right: 32-byte hex + `_VDL`
- SHA256 of neither half equals the hex (checksum is app-side)

`onoroff` toggled `on`/`off` (license server switch). HEAD = `off`.

Also in repo: `LSPosed-v1.9.2-7299-Irena-release.zip` (Android hooking).

## Other public projects (probably not this chall)

- `ActiveGolike` — cracked C# Golike farmer (`crack151` path, minsoftware `activation.php?code=&hwid=&hash=`). Serial string in EXE is **not** the leaked 2048-bit blob.
- `CTF` writeups (PTIT 2024/2025 only, no 2026 Tiger)
- No public Create/DeleteEvent for a Tiger repo in last ~90 days of `/users/luonginfosec/events/public`

## Blocker

Reverse 500 pts almost certainly needs the **crackme binary** (CTFd attachment) that validates this serial / fetches `key.html`. Folder `files/` is empty.

Next: drop the zip into `files/` or confirm challenge is key-only.

## `_VDL` is NOT a git commit

It is LuongVD's **custom flag closer** (Vũ Đức Lương).

Commit `3c1fffec97d4718735eaa08eaeb80dc467f22c57` (2026-03-14) wraps the hex as:

```
LuongVD{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL}
```

Same shape as `PTITCTF{...}`:
- prefix `LuongVD{`
- 64 hex chars (SHA-256 length, not a 40-char git SHA)
- suffix `_VDL}`

Timeline of `key.html`:
1. `298bdfce` — `number|HASH_VDL`
2. `3c1fffec` — `number|LuongVD{HASH_VDL}`  ← format leak
3. `834a83c3` — JSON array, `HASH_VDL` without wrapper
4. `85ff9ff4` — key array emptied

## HTTP-Request-Risk-Scoring-Decision-Tree (BTL_AI leak)

Repo: `luonginfosec/HTTP-Request-Risk-Scoring-Decision-Tree` (path `C:\Users\toanv\OneDrive\Desktop\BTL_AI\...`).

`grep PTITCTF\{` on the tree misses the flag: it is **base64** inside Burp XML.

`data/raw/samplectf.xml` item 1, HTTP 200 body after double-encoded `..../flag.txt` traversal:

```
PTITCTF{double_decode_traversal_in_tetos}
```

Provenance: Burp 2025.8.7 export `Fri May 22 21:58:20 ICT 2026`, `localhost:3000`. Looks like a **sample CTF solve** (tetos), not necessarily “Tiger Bạc”. Only `PTITCTF{...}` in the cloned repos.

Do **not** use leaked `AIzaSy*` / `sk-*` from CSVs against live Google/OpenAI.

Candidate flags (still unverified on scoreboard):

Already listed:
- `LuongVD{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL}`
- `PTITCTF{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb}`

Extra 3:
1. `PTITCTF{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL}`
   — hash + suffix `_VDL` trong wrapper PTITCTF
2. `PTITCTF{LuongVD{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL}}`
   — nguyên chuỗi sau `|` ở commit `3c1fffec`
3. `PTITCTF{3c1fffec97d4718735eaa08eaeb80dc467f22c57}`
   — SHA commit bọc `LuongVD{..._VDL}`

## Re-exam after wrong submit (2026-08-22)

Submitted and **rejected**: `PTITCTF{double_decode_traversal_in_tetos}`.

The body itself is the tell: `_in_tetos` = leftover from a previous web chall (double-encoded `flag.txt` traversal on `localhost:3000`, Burp 2026-05-22). Not Tiger Bạc.

### Gemini/OpenAI/HF key harvest — killed locally, not used live

Do **not** curl `generativelanguage.googleapis.com` / OpenAI / HF with keys from this tree. They are third-party secrets, not a planted CTF oracle.

Provenance (count only, keys not dumped):

| Pattern | Unique | Files |
|---|---|---|
| `AIzaSy...` | 5 | only `legitimate_normal_requests.csv`, `modsec_learn_legitimate_requests.csv`, plus processed/report copies |
| `sk-` + 20 | 1 | only `legitimate_normal_requests.csv` + processed copies |
| `hf_` | 0 | — |
| AIza/sk in `luongvd_*`, `qldt*`, `samplectf.xml`, `*.py`, `*.ipynb` | 0 | — |

GitHub search hit `AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw` in those same CSVs — that is Chrome's public Suggest `sugkey`, not a Gemini project key. Source tags: `openappsec_legitimate` / `modsec_learn_legitimate`. Author-named traffic (`import_luongvd_positive`, QLDT Burp) has none.

No `generativelanguage` / `tunedModels` / `cachedContents` in source.

### Other GitHub

- `nglong05` = Nguyễn Văn Long (LUGIA teammate). Original HTTP-risk repo (2026-05-21); luonginfosec copy 2026-05-23 (nested folder, notebook path `C:\Users\toanv\...BTL_AI`). Same `samplectf.xml`. Bio: "God dammit Jarvis, I need more alcohol."
- Public HF models `nglong05/fit-ollama-*` are May 2025 LLaMA-3 education fine-tunes. No PTITCTF on model cards. Not queried.
- `luonginfosec` 15 public repos, 0 gists. Recent events: Portswigger / key / CTF only. No DeleteEvent in last ~90 days.
- `key.html` format leak still the only planted-looking secret: commit `3c1fffec` → `LuongVD{6defc111…a101bb_VDL}`.

### Submit next (unverified)

1. `PTITCTF{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL}`
2. `PTITCTF{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb}`
3. `LuongVD{6defc111d43145653c9d3e6312c5cd0d36fd8c9f435650c5d0cff5ca15a101bb_VDL}`

If still wrong: challenge is Reverse 500 — likely needs the crackme zip that `key.html` feeds. `files/` originally empty.
