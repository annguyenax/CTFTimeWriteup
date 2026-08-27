import sys, collections
# digital-1_exp.bin = per-sample stream, values 0x00/0xFF
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1_exp.bin", 'rb').read()
print("len", len(data))
# Determine bit value: map 0x00->0, 0xFF->1 (also 0x01 seen)
# Build bit array
bits = [1 if b not in (0,0x00) else 0 for b in data]
# find runs
runs=[]
start=0; prev=bits[0]
for i in range(1,len(bits)):
    if bits[i]!=prev:
        runs.append((start,i,prev))
        start=i; prev=bits[i]
runs.append((start,len(bits),prev))
print("num runs", len(runs))
# length distribution of runs
lens=[r[1]-r[0] for r in runs]
c=collections.Counter(lens)
print("run length histogram (top20):", c.most_common(20))
# The bit duration = shortest run length? estimate bit period
# sample rate 25 MHz. runs of alternating 0/1 of length ~127 samples each half-period
# => period ~254 samples. That would be a very slow clock. For UART baud, bit time must be divisible.
# Let's look at transition times (in samples)
print("first 40 run lengths:", lens[:40])
