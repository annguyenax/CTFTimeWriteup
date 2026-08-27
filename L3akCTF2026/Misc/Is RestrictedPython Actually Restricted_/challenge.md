# Is RestrictedPython Actually Restricted?

- **Event:** L3akCTF 2026
- **Challenge ID:** misc_Is RestrictedPython Actually Restricted?
- **Category:** misc
- **Tags:** 
- **Points:** 500 *(snapshot; dynamic scoring)*
- **Solves:** 1 *(snapshot)*
- **Author:** 0x1622
- **Scoring:** decay
- **Has flag:** True
- **Instancer lifetime:** none
- **Source page:** https://ctf.l3ak.team/challenges?challenge=misc_Is%20RestrictedPython%20Actually%20Restricted%3F
- **Captured at:** 2026-08-01T13:09:32Z

## Prompt (verbatim)

As the title says.

Submit one base64-encoded UTF-8 Python program per connection, followed by `EOL` on its own line. Base64 padding is optional.

> [!CONNECTION]
> ncat --ssl restrictedpython.instances.ctf.l3ak.team 1337

## Attachments

| Name | Size | Local status | SHA-256 | Download URL |
|---|---:|---|---|---|
| chall.zip | 2.54 KiB | present | bd22084a05c41096205402c2da98bfefcd39c32a5becf914dc671d7f2c6bd163 | https://l3akctf-2026-uploads-europe-west1.storage.googleapis.com/uploads/bd22084a05c41096205402c2da98bfefcd39c32a5becf914dc671d7f2c6bd163/chall.zip |

## Local layout

- Original files: files/
- Solver and minimal evidence: solve/
- Human-readable writeup: writeup/writeup.md
- Disposable work only: D:\download\ctf-scratch\l3akctf_misc_Is RestrictedPython Actually Restricted?

## Notes

- Metadata and scores are a snapshot and may change during dynamic scoring.
- Do not store venvs, package caches, browser profiles, common wordlists, extracted duplicates, or bulk tool output in this directory.