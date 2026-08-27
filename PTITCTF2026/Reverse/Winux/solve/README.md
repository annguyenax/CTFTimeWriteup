# Winux solver

```
python crack_key.py
```

Reads `files/_extracted/lib/winuxsvc.dll` (memory-mapped PE), dumps the SHA-256 proof tables, brute-forces each of 64 package-key bytes. Writes `package_key.txt`.

`decrypt_wux.py` is a negative test: WUX2 record bodies do not AES/XOR to the flag.
