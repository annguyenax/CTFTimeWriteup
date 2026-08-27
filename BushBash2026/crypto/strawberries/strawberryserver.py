#!/usr/bin/env python3

import sys
from time import sleep
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad

# 64 byte messages, with 16 byte AES padding.
MSG_SIZE = 64 + 16

# Integrity check for security reasons
CHECK = b'\x89\x1fr\xd8\x90\xb2\x91\x1c\xfb\x98t\x01s\xd2J\xbf\xe5\xe4\x80\x07\xcfQz\xad-\xea\x80\xdc(\x90Z\xdf'

PREMIUM_USER = b"\x00\x00\x00\x00\x024\xf9\x23d\x3a\x95\x20\xefv'\x77"

strawberry_count = 0

def get_cipher():
    ivf = open("iv", "rb")
    iv = ivf.read()
    keyf = open("key", "rb")
    key = keyf.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)

    keyf.close()
    ivf.close()
    return cipher;
    
def parse_request(request):

    t = request[0:8].decode("utf-8", errors="replace")
    n = int.from_bytes(request[8:16], byteorder="big")
    u = request[16:32]
    i = request[32:]

    print("transaction ID:", t)
    print("requested strawberries:", n)
    print("user ID:", u)

    return t, n, u, i 

def displayFlag():
    flagtxt = open("flag.txt", "r")
    print(flagtxt.read())

def process_request(t,n,u,i):
    global strawberry_count
    if i != CHECK:
        while True:
            print("STOP STEALING MY STRAWBERRIES >:(", end=" ", flush=True)
    if u != PREMIUM_USER and n > 5:
        print("You know gluttony is a sin... right?", flush=True)
        exit(6767)

    print("Here's your yummy strawberries: 🍓🍓🍓🍓", flush=True)
    strawberry_count += n
    print(f"You now have {strawberry_count} strawberries", flush=True)
    if strawberry_count > (1 << 32):
        print("How DARE you >:(", flush=True) 
        displayFlag()
    

def encrypt(pt):
    cipher = get_cipher() 
    ct = cipher.encrypt(pad(pt, AES.block_size))
    return ct

def decrypt(ct):
    cipher = get_cipher()
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

def main():
    while True:
        data = sys.stdin.buffer.read(MSG_SIZE)
        if len(data) < MSG_SIZE:
            break
        print("growing more strawberries...", flush=True) 
        for i in range(3):
            print(i+1, flush=True)
            sleep(1) 
        pt = decrypt(data)
        t,n,u,i = parse_request(pt)
        process_request(t,n,u,i) 

if __name__ == "__main__":
    main()
