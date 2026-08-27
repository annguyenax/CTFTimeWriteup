# pw_zip

## Solution
The challenge provides a ZIP file `pw.zip` that is password-protected. The description says the password is "one of the 100 most used passwords of 2025".

Since standard Python `zipfile` module doesn't support AES-encrypted zips (which this zip uses), we can use `pyzipper` or `7z` to extract it. Using the SecLists `10k-most-common.txt` wordlist, we can brute-force the password.

The password was found to be `1234qwer`. 

Extracting the zip with this password gives `flag.txt`.

## Flag
`LITCTF{password_123456_103flkj3}`
