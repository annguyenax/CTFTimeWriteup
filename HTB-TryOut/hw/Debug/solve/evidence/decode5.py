import collections, struct
# Examine digital-1_exp.bin byte distribution and structure
data = open(r"D:\download\CTFTimeWriteup\HTB-TryOut\hw\Debug\files\_work\sal_extracted\digital-1_exp.bin", 'rb').read()
c = collections.Counter(data)
print("whole-file byte histogram:", c.most_common())
# Print first 200 bytes
print("first 200:", data[:200])
