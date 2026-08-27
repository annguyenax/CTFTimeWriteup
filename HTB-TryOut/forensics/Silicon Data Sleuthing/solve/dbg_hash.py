import re
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\forensics\Silicon Data Sleuthing\files\_work\chal_router_dump.bin", 'rb').read()
print('dump size', len(data))

# look for shadow/passwd-like content and hash patterns in raw dump
patterns = [rb'\$6\$', rb'\$1\$', rb'\$2[aby]\$', rb'\$5\$']
for p in patterns:
    cnt = 0
    for m in re.finditer(p, data):
        s = max(0, m.start()-40)
        print('HASH %s: %r' % (p, data[s:m.end()+40]))
        cnt += 1
        if cnt >= 3:
            break
    if cnt == 0:
        print('HASH %s: none' % p)

# shadow file content search
for m in re.finditer(rb'root:[^:\n]{0,80}:', data):
    print('ROOTLINE:', repr(data[max(0, m.start()-8):m.end()+25]))
