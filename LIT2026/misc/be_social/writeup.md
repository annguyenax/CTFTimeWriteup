# be_social

## Overview
An OSINT challenge involving a Bluesky profile. The challenge provides a link to `jsmithf.bsky.social` and a server endpoint.

## Solution
1. Checking the Bluesky profile reveals two posts:
    - A post celebrating a birthday on "July 25".
    - A post showcasing a dog named "Cooper".
2. Connecting to the server endpoint via HTTP reveals a login form requiring a 4-digit PIN for the user `John`.
3. The birthday "July 25" corresponds to the PIN `0725`. Logging in takes us to a "Secrets Home" page (`/home`) that asks for a password.
4. Entering the dog's name `cooper` (all lowercase) reveals the secret: `os_1nt_success_4f2a58b9`.
5. Wrapping this in the flag format gives the final flag.

**Flag:** `LITCTF{os_1nt_success_4f2a58b9}`
