#!/usr/bin/env python3
"""
LIT2026 / crypto / any_secrets_could_instantly_be_imparted
Caesar (shift) cipher applied to raw ASCII byte values, not just A-Z.

Hint "Et tu, Brute?" -> Brutus -> Caesar / brute-force the shift.
The ciphertext contains letters, digits and symbols, so the shift is over
the full byte range. We brute all shifts and keep the one giving 'LITCTF'.
"""

CIPHERTEXT = 'HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y'


def shift(text, s):
    return ''.join(chr((ord(c) + s) % 256) for c in text)


def solve():
    for s in range(256):
        dec = shift(CIPHERTEXT, s)
        if dec.startswith('LITCTF{') and dec.endswith('}'):
            return s, dec
    raise ValueError('no shift produced a valid flag')


if __name__ == '__main__':
    s, flag = solve()
    print(f'shift = +{s}')
    print(f'flag  = {flag}')
    # verification: re-encrypt must reproduce the ciphertext exactly
    assert shift(flag, -s) == CIPHERTEXT, 'round-trip failed'
    print('round-trip re-encryption OK')
