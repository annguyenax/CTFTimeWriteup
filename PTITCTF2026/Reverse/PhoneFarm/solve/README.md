# PhoneFarm solver

```text
python disasm_change.py   # ARM64 Main::changeDevice @ 0x147a0
```

License compare is length 5 against `"hello"`.

```
python -c "import hashlib; print(hashlib.md5(b'hello').hexdigest())"
```

APK: `files/PhoneFarm.zip` → `maxchangev2.apk`. Native lib:
`apk_extract/lib/arm64-v8a/libOctopus.so`.
