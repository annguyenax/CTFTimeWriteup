# Evidence Manifest

## Challenge: PipBoy (HTB Web, remote)

Target: http://154.57.164.73:31701
Goal: read `/flag.txt` (HTB{...})

### Files
| File | Claim | Source/Tool | Repro |
|---|---|---|---|
| xxe_test2.txt | XXE resolves external entity; flag reflected in `Version` | POST /api/update + curl (Invoke-WebRequest) | `solve.py` |
| verify.txt | Flag extracted twice, identical | two independent POSTs | `solve.py` |

### Vulnerability
XXE (XML External Entity) in `/api/update` — Flask (Werkzeug/3.0.3, Python/3.12.3),
lxml-based parser resolves `file://` entities. Root cause: `<!DOCTYPE>` with
`SYSTEM "file:///flag.txt"` entity injected into `Version` field.

### Flag
HTB{b1om3tric_l0cks_4nd_fl1cker1ng_l1ghts_6d45d44e5c2034af11b95b9d6def5c48}
