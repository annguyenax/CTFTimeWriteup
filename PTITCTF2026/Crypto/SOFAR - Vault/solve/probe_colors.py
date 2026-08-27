import cv2, numpy as np, os, sys, json

base = r'D:\download\CTFTimeWriteup\PTITCTF2026\Crypto\SOFAR - Vault\files\extracted\SOFAR - Vault'
name = sys.argv[1]
img = cv2.imread(os.path.join(base, name+'.png'))
h, w = img.shape[:2]
print(name, img.shape, img.dtype)
# Look at color structure: sample some pixels
sample = img[::50, ::50].reshape(-1,3)
print('unique-ish colors sample:')
for c in np.unique(sample.reshape(-1,3), axis=0)[:20]:
    print('  ', c.tolist())
