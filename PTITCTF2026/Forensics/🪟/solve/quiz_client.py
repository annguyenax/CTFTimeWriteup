import socket
import sys
import time

HOST = '144.79.188.39'
PORT = 42978

def connect_and_start():
    s = socket.create_connection((HOST, PORT), timeout=15)
    def recv_prompt():
        buf = b''
        while True:
            c = s.recv(1)
            if not c: break
            buf += c
            if b'> ' in buf: break
        return buf.decode('utf-8', errors='ignore')

    def send_ans(ans):
        print(f'Sending: {ans}')
        s.sendall(f'{ans}
'.encode('utf-8'))
        time.sleep(0.3)
        res = s.recv(4096).decode('utf-8', errors='ignore')
        print(f'Response:
{res}')
        return res

    p1 = recv_prompt()
    print(p1)
    send_ans('12')
    return s

if __name__ == '__main__':
    connect_and_start()
