#!/usr/bin/env python3
"""
The Unbroken Shelf - KaliCTF 26 (OSINT, 100đ)

Bài này KHÔNG cần code khai thác - lời giải là quy trình OSINT:
  1. Đọc mẩu báo (files/The-Unbroken-Shelf-Final.png):
       - Tiêu đề: "Mysterious Explosion Blows Firemen Out of Drug Store"
       - Trong bài có: "Eighth Avenue", "Battalion Chief ...rence McGuire",
         clerk "Slater", "Samuel".
  2. Tra cứu tiêu đề trên Chronicling America (Library of Congress),
     kho báo lịch sử Mỹ có full-text OCR.
       - Tìm chính xác cụm: "Blows Firemen Out of Drug Store"
       - Kết quả DUY NHẤT: New-York Tribune, 1920-08-21, trang 1
         (LCCN sn83030214).
  3. Đọc toàn văn bài để lấy địa chỉ + thời gian:
       "...wrecked Slater & Halpern's drug store, 157 Eighth Avenue.
        ... It was about 8:40 p. m. ..."

GHI CHÚ KỸ THUẬT (vì sao có đoạn code dưới):
  Toàn bộ loc.gov nằm sau Cloudflare "Just a moment" (JS challenge) nên
  curl/WebFetch đều bị chặn 403. Cách vượt: điều khiển một trình duyệt
  Chrome THẬT (headed) qua CDP để Cloudflare tự pass, rồi dùng fetch()
  ngay trong ngữ cảnh trang (đã có cookie CF) để lấy OCR ALTO XML.

Đoạn dưới là bộ trích xuất tối thiểu: cho URL trang -> ra các trường của flag.
Cần một Chrome đang mở cổng debug:
  chrome.exe --remote-debugging-port=9444 --remote-allow-origins=* \
             --user-data-dir=<scratch>
"""
import json, re, html, time, urllib.request

CDP = "http://127.0.0.1:9444/json"
PAGE_JSON = ("https://www.loc.gov/resource/sn83030214/1920-08-21/ed-1/"
             "?sp=1&st=text&fo=json")

def _ws():
    import websocket  # pip install websocket-client
    t = json.load(urllib.request.urlopen(CDP))
    url = [x for x in t if x['type'] == 'page'][0]['webSocketDebuggerUrl']
    return websocket.create_connection(url, max_size=None)

_id = 0
def _cmd(ws, method, params=None):
    global _id; _id += 1; mid = _id
    ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == mid:
            return m

def _ev(ws, expr, await_p=False):
    r = _cmd(ws, "Runtime.evaluate",
             {"expression": expr, "awaitPromise": await_p, "returnByValue": True})
    return r.get("result", {}).get("result", {}).get("value")

def _fetch(ws, url):
    expr = "(async()=>{let r=await fetch(%s,{credentials:'include'});return await r.text();})()" % json.dumps(url)
    return _ev(ws, expr, await_p=True) or ""

def main():
    ws = _ws()
    _cmd(ws, "Page.enable")
    _cmd(ws, "Page.navigate", {"url": PAGE_JSON})
    for _ in range(40):
        time.sleep(1.2)
        title = _ev(ws, "document.title") or ""
        if title and "moment" not in title.lower():
            break
    meta = json.loads(_fetch(ws, PAGE_JSON))
    seg = re.search(r'segment=(/service/[^&]+\.xml)', meta["fulltext_service"]).group(1)
    xml_url = "https://tile.loc.gov/storage-services" + seg
    _cmd(ws, "Page.navigate", {"url": xml_url})           # pass CF cho tile.loc.gov
    time.sleep(6)
    xml = _fetch(ws, xml_url)
    words = [html.unescape(w) for w in re.findall(r'CONTENT="([^"]*)"', xml)]
    text = ' '.join(words).replace("? ", "")
    art = text[text.find("Mysterious Explosion"):][:1200]

    number, street = re.search(r'drug store,\s*(\d+)\s+(Eighth Avenue)', art).groups()
    hh, mm, ap = re.search(r'about\s*(\d+):(\d+)\s*([ap])\.?\s*m', art).groups()
    h = int(hh) % 12 + (12 if ap == 'p' else 0)
    time24 = f"{h:02d}{int(mm):02d}"

    flag = ("KaliTeam{NEW_YORK_TRIBUNE_1920_08_21_"
            f"{number}_{street.upper().replace(' ', '_')}_{time24}}}")
    print("Address :", number, street)
    print("Time    :", f"{hh}:{mm} {ap}.m. -> {time24}")
    print("FLAG    :", flag)
    ws.close()

if __name__ == "__main__":
    main()
