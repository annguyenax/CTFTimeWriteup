cipher = 'HQGFPN{elzlyho_eedlxrg_ev_cltmyv_wvq_yazfh}'
key = 'WIND'
key_idx = 0
flag = ''

for c in cipher:
    if c.isalpha():
        is_upper = c.isupper()
        c_val = ord(c.lower()) - 97
        k_val = ord(key[key_idx % len(key)].lower()) - 97
        p_val = (c_val - k_val) % 26
        char = chr(p_val + 97)
        if is_upper: char = char.upper()
        flag += char
        key_idx += 1
    else:
        flag += c

print('FLAG:', flag)
