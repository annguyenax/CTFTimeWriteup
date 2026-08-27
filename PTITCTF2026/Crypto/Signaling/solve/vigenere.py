def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
            plaintext += decrypted_char
            key_idx += 1
        else:
            plaintext += char
    return plaintext

# The ciphertext is:
ct = "KBKESVCDKRDHW FJLPOV BJHKLTCMUXVA DJLQINJF"

# Let's try to find the key assuming the first part starts with PTITCTF
# Or maybe the first word is something else?
# Wait, let's find the difference between PTITCTF and KBKESVC
target = "PTITCTF"
key = ""
for i in range(len(target)):
    shift = (ord(ct[i]) - ord(target[i])) % 26
    key += chr(shift + ord('A'))
print("If plaintext starts with PTITCTF, key starts with:", key)

# Let's try to find if it's a known cipher
