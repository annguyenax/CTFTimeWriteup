# Subleq Scramble

- **Event:** L3akCTF 2026
- **Challenge ID:** rev_Subleq Scramble
- **Category:** rev
- **Tags:** 
- **Points:** 110 *(snapshot; dynamic scoring)*
- **Solves:** 57 *(snapshot)*
- **Author:** Shatterbox
- **Scoring:** decay
- **Has flag:** True
- **Instancer lifetime:** none
- **Source page:** https://ctf.l3ak.team/challenges?challenge=rev_Subleq%20Scramble
- **Captured at:** 2026-08-01T13:09:32Z

## Prompt (verbatim)

Some dude's been trying to hide even more secrets behind yet another one of his "all-new, totally one-of-a-kind encryption algorithms" that he'd been yapping about.

Apparently it's some sort of "subleq emulator" that runs thousands of iterations of an image encryption algorithm...
before straight-up _memdumping_ the entire program state into a binary file when it's done.

_All of it._

Given that he was kind enough to send us an encrypted file, that probably means the algorithm's open-source now.

Nobody tell him.

Note: Flag format is /L3AK{[A-Z0-9?'_,]+}/

## Attachments

| Name | Size | Local status | SHA-256 | Download URL |
|---|---:|---|---|---|
| rev_subleq-scramble.tar.gz | 1.07 KiB | present | 55d65f7c366fd7b5f04038bd8e1b6498cb85a20f05110afa7f43c5634f3b6ab5 | https://l3akctf-2026-uploads-europe-west1.storage.googleapis.com/uploads/55d65f7c366fd7b5f04038bd8e1b6498cb85a20f05110afa7f43c5634f3b6ab5/rev_subleq-scramble.tar.gz |

## Local layout

- Original files: files/
- Solver and minimal evidence: solve/
- Human-readable writeup: writeup/writeup.md
- Disposable work only: D:\download\ctf-scratch\l3akctf_rev_Subleq Scramble

## Notes

- Metadata and scores are a snapshot and may change during dynamic scoring.
- Do not store venvs, package caches, browser profiles, common wordlists, extracted duplicates, or bulk tool output in this directory.