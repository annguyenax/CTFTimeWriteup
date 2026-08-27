# Havok Trail

## 1. Summary / Flag
- Status: [x] solved (candidate verified via CTFtime scoreboard)
- Flag: `KaliTeam{2024_Riyadh_83}`

## 2. Challenge files / versions
- Prompt-only OSINT; no attachments
- Primary sources: CTFtime.org team H@vOK + BHMEA Final 2024 event page

## 3. Core concept
- Guest OSINT: reconstruct a CTF team's public competition trail from CTFtime/event records

## 4. Triage
- Author/company: Havok / hav0k
- Target event series: Black Hat MEA CTF
- Need: YEAR, host CITY, final RANK → `KaliTeam{YEAR_CITY_RANK}`

## 5. Exploit/recovery
1. Search "Havok Black Hat MEA CTF" → team academy site + LinkedIn mentions of #119 quals / #83 finals
2. CTFtime team search → **H@vOK** (Jordan) https://ctftime.org/team/302650/
3. Event history:
   - Qual 2024: place **119**
   - **Final 2024**: place **83**, on-site **Riyadh**
4. Prompt asks for **final ranking** → Finals place **83**, year **2024**, city **Riyadh**

## 6. Verification
- Scoreboard row: place 83, team H@vOK, BlackHat MEA CTF Final 2024 (ctftime.org/event/2431)
- Independent: LinkedIn member of Havok states 83# Finals + 119 quals

## 7. Failed approaches
- Using qualification rank 119 instead of finals 83 (prompt says final ranking)

## 8. Alternative solve paths
- LinkedIn company hav0k / Instagram havok.crew → same year/city; rank still needs CTFtime

## 9. Faster route next time
- Search CTFtime for team name variants (Havok / H@vOK) + event series first

## 10. Sources
- https://ctftime.org/team/302650/
- https://ctftime.org/event/2431/
- https://ctftime.org/event/2430/
