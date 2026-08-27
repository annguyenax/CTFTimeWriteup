# PhoneFarm (PTITCTF2026 Reverse) — session notes

## Challenge
Find the license/API key of cracked device-spoofing APK `maxchangev2.apk` (ViChanger / Octopus), convert it to MD5. Flag `PTITCTF{md5hex}`.

APK: `D:\download\ctf-scratch\ptitctf2026_phonefarm\PhoneFarm\maxchangev2.apk`
Extract: `D:\download\ctf-scratch\ptitctf2026_phonefarm\apk_extract`

## App identity
- Package: `vn.vichanger.app`
- Version: `25.01.01`
- Xposed/LSPosed module (`assets/xposed_init` → `vn.vichanger.app.Xposed.MainHook`)
- Native lib: `libOctopus.so` (`System.loadLibrary("Octopus")` from `MainTask`)
- Login UI: `LoginActivity.txtAPIKey` saved as SharedPreferences `setting` / `apiKey`

Java only checks non-empty. Real validation is native:

`MainTask.changeDevice(Context, apiKey, brand, country)` → JNI `Main::changeDevice`.

## Native check (`libOctopus.so` ARM64)

`JNI_OnLoad` registers native `changeDevice` at `0x143d0`.
C++ `Main::changeDevice` is at `0x147a0` (size `0x774`).

At function entry, first `std::string` argument (API key) is tested:

```
cmp  length, #5
load 4 bytes, compare to 0x6c6c6568  ; "hell" LE
ccmp 5th byte, #0x6f                 ; 'o'
b.eq  continue_request
else  return "Invalid API Key"
```

So the cracked master key is the literal **`hello`**.

On success the native code builds:

`default_url + "?apiKey=" + <user key>`  
(`?apiKey=` is immediate `0x3d79456b6970613f`)

and POSTs to `https://vichanger.com/api/changeDevice` (`Main::OCRequest`).

Response is `cryptor::decrypt` = base64 decode + XOR with compile-time key
`8F3K5nX29tZaQ1BpYrW7JL6Cd4EmHo` (`cryptor_static_base::m_key`). That XOR key is **not** the software license; it only unwraps the JSON device payload.

## MD5 / flag
```
MD5("hello") = 5d41402abc4b2a76b9719d911017c592
```

Candidate flag: `PTITCTF{5d41402abc4b2a76b9719d911017c592}`

## Rejected candidates
| String | Role | MD5 |
|---|---|---|
| `8F3K5nX29tZaQ1BpYrW7JL6Cd4EmHo` | cryptor XOR key for responses | `5651971678d1307bb41e69311febfbee` |
| `luongvd` | flavor-text name only; not in APK | `8a11abe247ce0ebecd25a8b2ff0b6387` |

No `luongvd` / `license` / `premium` / `crack` string in DEX or native. The “crack” is the hardcoded `"hello"` backdoor.

## Evidence files
- DEX bytecode dump: `D:\download\ctf-scratch\ptitctf2026_phonefarm\vichanger_bytecode.txt`
- Native analysis: `analyze_octopus*.py`, `octopus_hello.txt`, `octopus_main.txt`
