import sys, collections
path = sys.argv[1]
data = open(path, 'rb').read()
print("len", len(data))
# byte histogram of first 4096
cnt = collections.Counter(data[:8192])
print("first 8192 byte hist (top):", cnt.most_common(10))
# check for 0x00/0xff runs and transitions
# assume each byte is a sample (0 or 1 represented as 0/1, or 0x00/0xFF)
runs=[]
start=0
prev=data[0]
for i in range(1,len(data)):
    if data[i]!=prev:
        runs.append((start,i-1,prev))
        start=i; prev=data[i]
runs.append((start,len(data)-1,prev))
print("num runs", len(runs))
print("first 30 runs:", runs[:30])
