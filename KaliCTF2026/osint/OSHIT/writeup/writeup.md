# OSHIT

## 1. Summary / Flag
- Status: [x] solved (candidate — verify on platform)
- Flag: `KaliTeam{MAZEN_DARWISH_104728_OPS_C-12_SAHAB_INDUSTRIAL_ESTATE}`

## 2. Challenge files / versions
- Invoice: `files/paper.png` — Asterion Field Services, project NQ-441, domain asterion.kali-team.online, signatory M.D.

## 3. Core concept
- Multi-source corporate OSINT across surviving subdomains + robots-hidden paths + delivery photos.

## 4. Triage
1. Invoice → company domain + NQ-441 + M.D.
2. Subfinder on `kali-team.online` → `ops.`, `tenders.`, `media.` asterion hosts (main site CF-gated).
3. `ops` → login page **PORTAL CODE: OPS**.
4. `tenders/robots.txt` Disallow `/archive/` and `/vendor-docs/` → open both.
5. Award notice PDF NQ-441 → **Authorized Contact Mazen Darwish**.
6. Supplier prequalification PDF → Asterion **Registration No. 104728**.
7. Media NQ-441 images → warehouse **C-12**, sign **SAHAB INDUSTRIAL ESTATE**.

## 5. Flag fields
| Field | Value | Source |
|-------|-------|--------|
| CONTACT | MAZEN_DARWISH | award_notice_NQ441.pdf |
| REGISTRATION | 104728 | supplier_prequalification_2025.pdf |
| PORTAL | OPS | ops.asterion.kali-team.online |
| WAREHOUSE | C-12 | nq441_b.jpg final handover |
| AREA | SAHAB_INDUSTRIAL_ESTATE | wall sign on nq441_b.jpg |

## 6. Alternative warehouse note
- nq441_a.jpg shows bay **C-1**; final delivery image is **C-12**. Prefer C-12 for "receiving warehouse" / final delivery.
- If rejected try C-1 or C_12 variants.

## 7. Sources
- https://ops.asterion.kali-team.online/
- https://tenders.asterion.kali-team.online/archive/
- https://tenders.asterion.kali-team.online/vendor-docs/
- https://media.asterion.kali-team.online/projects/nq-441/
