#!/usr/bin/env python3
"""Minimal reverse proxy: 127.0.0.1:4873 -> target:31567 with Host: registry.prison-pipeline.htb.
Lets local `npm publish --registry http://localhost:4873` reach the target's verdaccio.
Also rewrites the Host header of any Location redirects? (not needed here).
"""
import http.server
import socketserver
import urllib.request
import sys

UPSTREAM = "http://154.57.164.64:31567"
REG_HOST = "registry.prison-pipeline.htb"


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _forward(self):
        body = None
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length:
            body = self.rfile.read(length)
        url = UPSTREAM + self.path
        req = urllib.request.Request(url, data=body, method=self.command)
        for k, v in self.headers.items():
            if k.lower() in ("host", "content-length", "connection", "accept-encoding"):
                continue
            req.add_header(k, v)
        req.add_header("Host", REG_HOST)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                status = resp.status
                headers = resp.headers
        except urllib.error.HTTPError as e:
            data = e.read()
            status = e.code
            headers = e.headers
        self.send_response(status)
        for k, v in headers.items():
            if k.lower() in ("transfer-encoding", "connection", "content-length"):
                continue
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    do_GET = _forward
    do_PUT = _forward
    do_POST = _forward
    do_HEAD = _forward
    do_DELETE = _forward
    do_OPTIONS = _forward

    def log_message(self, fmt, *args):
        sys.stderr.write("[proxy] %s %s\n" % (self.command, self.path))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4873
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), Handler) as httpd:
        print(f"[*] proxy on 127.0.0.1:{port} -> {UPSTREAM} (Host: {REG_HOST})")
        httpd.serve_forever()
