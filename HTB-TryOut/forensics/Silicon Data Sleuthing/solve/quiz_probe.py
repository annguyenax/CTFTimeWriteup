import socket, time

s = socket.create_connection(('154.57.164.75', 30628), timeout=15)
s.settimeout(4)

def rd():
    out = b''
    time.sleep(1.0)
    try:
        while True:
            d = s.recv(4096)
            if not d:
                break
            out += d
            time.sleep(0.25)
    except socket.timeout:
        pass
    return out

# Just read the initial prompt(s) without answering
for i in range(3):
    data = rd()
    if not data:
        break
    print('=== chunk %d ===' % i)
    print(data.decode(errors='replace'))
    if i == 0:
        # maybe answer Q1 to proceed and see more
        break
s.close()
