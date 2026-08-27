# Bug bounty? — SESSION

Instance 144.79.188.39:35259 **expired** (connection refused). Spawn a new one; quiz is TCP not HTTP.

## Quiz

Banner: `PCAP FORENSICS QUIZ`, Vietnamese, sequential questions.
Q1: `Sau khi chiếm quyền truy cập vào một máy, hacker đã tải một tool về, tên file là gì?`
Retries stay on Q1 (`Chưa đúng. Hãy thử lại.`). "5 lượt thử" in the prompt did **not** hard-lock after 5 wrong Q1 answers.

### Q1 tried (WRONG)

- `gobuster_3.8.2-1_amd64.deb`
- `gobuster`
- `openssl`
- `masscan_1.3.2+ds1-2_amd64.deb`
- `masscan`
- `seclists_2025.3-0kali1_all.deb`

Spray after that was incomplete (instance died / recv timeout). **Not fairly tested:** `seclists`, `wget`, `password_list`, `common.txt`, `README.md`, csv, `/usr/share/seclists/Discovery/Web-Content/common.txt`.

## Artifact

`files/chall.pcapng.gz` → `ctf-scratch/chall.pcapng` 705176836 B
SHB: `Linux 6.12.38+kali-amd64` / `Dumpcap (Wireshark) 4.6.6` / `eth0` / Intel i5-8250U
399417 EPB, 60105 TCP streams, linktype Ethernet.

## Actors

| IP | Role |
|---|---|
| 10.10.10.154 | Kali attacker (DHCP hostname `kali`, Firefox 128) |
| 10.10.10.132 | Mod platform nginx `:5665` |
| 10.10.10.1 | Windows Chrome 150 user `longhd` |

Hint planted as failed login password: `"tcp.stream eq 60053 "` (Wireshark).
Stream 60053 = `10.10.10.154:50040 -> 10.10.10.132:80` SYN, **0 payload** (port 80 closed). Next streams are gobuster to `:5665`. Stream 60052 is the 544MB seclists download.

## Timeline

1. Kali apt update (`InRelease`, `Packages.gz`, `Contents-amd64.gz`)
2. `GET /kali/pool/main/m/masscan/masscan_1.3.2+ds1-2_amd64.deb`
3. masscan from `:47646` against `10.10.10.132` (many dest ports, 6 null-byte “payload”)
4. Chrome `longhd` / `25012005` / `Duy Long` registers + logs in
5. Firefox `anhcd05` / `longhdwillbepwnhahaha` / `Chu Duc Anh` registers; first login uses wireshark filter then real password
6. apt: `gobuster_3.8.2-1_amd64.deb` then `seclists_2025.3-0kali1_all.deb` (544MB, kali.download CF 104.17.254.239)
7. gobuster/3.8.2 vs `:5665` with SecLists `Discovery/Web-Content/common.txt` (~4750 reqs)
8. Uploads to `POST /api/mods/7/builds/{4-8}/upload/` filenames:
   - `password_list` (LongHD@2005 / Long250105 / 1..6)
   - `README.md` (TLS ML-KEM lab)
   - `server.crt`
   - `openssl` (ELF ~3.7MB)
   - `ram_tls_results_2gb_2026-05-20_00-00-58.csv`

## App facts (later quiz answers)

- Users: longhd id=2, anhcd05 id=3
- longhd: platform `win25` “Windows 64-bit”; mod id=6 `Test mod` 25.0.1 “Test bản mod mới của longhd”
- anhcd05: platform `pwn` “Windows64-bit” “anhcd05 hacker top 1 PTIT”; mod id=7 title `anhcd05`
- Stock Palworld mods: Neon Pals Graphics Overhaul, Coop Server Slots Unlocker, Faster Breeding & Hatching, Legendary Pal Skins Pack, More Pals Per Base
- Release notes mention **Palpagos** — flavor “Mảnh đất thiêng liêng này, cõi này, chính là flag”
- Flag is **per-instance** after answering all quiz Qs (no PTITCTF in pcap)

## Q1 next guesses (new instance)

1. `common.txt`
2. `/usr/share/seclists/Discovery/Web-Content/common.txt`
3. `password_list`
4. `seclists`
5. `ram_tls_results_2gb_2026-05-20_00-00-58.csv`
6. `README.md`

Run: `python ctf-scratch/quiz_client.py <ans1> <ans2> ...` against new host:port.

## Likely later answers

- attacker IP `10.10.10.154`
- victim `10.10.10.132`
- port `5665`
- hostname `kali`
- user `anhcd05` / pass `longhdwillbepwnhahaha`
- victim user `longhd` / `25012005`
- scan tool `masscan`
- dirbust `gobuster` 3.8.2
- wordlist `common.txt`
- wireshark `tcp.stream eq 60053`
