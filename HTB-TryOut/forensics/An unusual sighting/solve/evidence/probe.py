import socket, time, sys

HOST='154.57.164.69'; PORT=32684
s=socket.create_connection((HOST,PORT),timeout=15)
s.settimeout(4)

def read():
    time.sleep(1.0)
    out=b''
    try:
        while True:
            d=s.recv(4096)
            if not d: break
            out+=d
            time.sleep(0.25)
    except socket.timeout:
        pass
    except Exception as e:
        out+=b'<%s>'%str(e).encode()
    return out

def send(x):
    s.sendall((x+'\n').encode())

def q(ans=None):
    r=read()
    sys.stdout.write('\n---SRV---\n'+r.decode(errors='replace')+'\n')
    if ans is not None:
        send(ans)
        sys.stdout.write('[sent] '+ans+'\n')
        time.sleep(1.2)
        r2=read()
        sys.stdout.write('---AFTER---\n'+r2.decode(errors='replace')+'\n')
    return r

q('100.107.36.130:2221')
q('2024-02-13 11:29:50')
q('2024-02-19 04:00:14')
q('OPkBSs6okUKraq8pYo4XwwBg55QSo210F09FCe1-yj4')
q('whoami')
q('./setup')
q()  # read next
