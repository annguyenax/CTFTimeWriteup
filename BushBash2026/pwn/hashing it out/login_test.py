import socket
import sys

def recvall(s):
    data = b''
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    return data.decode(errors='replace')

def try_login(host, port, username, password):
    s = socket.create_connection((host, port), timeout=8)
    s.settimeout(3)
    out = recvall(s)
    s.sendall(username.encode() + b'\n')
    out += recvall(s)
    s.sendall(password.encode() + b'\n')
    out += recvall(s)
    s.close()
    return out

if __name__ == '__main__':
    host = '34.40.133.67'
    port = 4434
    username = sys.argv[1] if len(sys.argv) > 1 else 'admin'
    password = sys.argv[2] if len(sys.argv) > 2 else ''
    print(try_login(host, port, username, password))
