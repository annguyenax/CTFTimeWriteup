# PhoneFarm

- **Event:** PTITCTF2026
- **Category / tags:** Reverse / Android / native license check
- **Flag format:** `PTITCTF{md5(key)}`
- **Attachments:** `PhoneFarm.zip` → `maxchangev2.apk`
- **Status:** solved

## Prompt (verbatim)

Gần đây công an Đột kích "trang trại" 2.000 điện thoại ở Đà Nẵng: Chuyên "nuôi" tài khoản Zalo, Tinder ảo để phục vụ lừa đảo Campuchia. Đã thu được 1 phần mềm có tác dụng đổi thông tin thiết bị để gian lận. Qua quá trình khai thác đã biết một đối tượng tên luongvd đã crack phần mềm này. Tìm ra key của phần mềm mà không cần mua. Hãy tìm ra nó và chuyển sang dạng MD5

## Recon

APK package `vn.vichanger.app` (ViChanger / Octopus device spoof, Xposed module). Login UI stores SharedPreferences `apiKey`. Java only checks that the field is non-empty.

Native: `libOctopus.so`, `Main::changeDevice` at ARM64 `0x147a0`.

## Key check

At function entry the first `std::string` (API key):

```
cmp  length, #5
load 4 bytes, compare to 0x6c6c6568   ; "hell" LE
ccmp 5th byte, #0x6f                  ; 'o'
b.eq  continue
else  return "Invalid API Key"
```

On success it appends immediate `?apiKey=` (`0x3d79456b6970613f`) to `https://vichanger.com/api/changeDevice`.

The cracked master key is the literal **`hello`**.

**Decoy:** `8F3K5nX29tZaQ1BpYrW7JL6Cd4EmHo` sits in `.rodata` next to nlohmann/json noise and is `cryptor_static_base::m_key` (XOR/base64 of the JSON **response**), not the license.

## MD5 / flag

```
MD5("hello") = 5d41402abc4b2a76b9719d911017c592
PTITCTF{5d41402abc4b2a76b9719d911017c592}
```

## Verification

Independent ARM64 disassembly of `changeDevice` at `0x147a0` in `libOctopus.so` (length `#5`, `movk` build of `0x6c6c6568`, `ccmp` with `#0x6f`). Python `hashlib.md5(b"hello")`.

## Dead ends

- Submitting MD5 of the 30-char cryptor static key (`5651971678d1307bb41e69311febfbee`).
- Searching GitHub/OSINT for `luongvd` (not in the APK; the crack is the hardcoded `hello` compare).
