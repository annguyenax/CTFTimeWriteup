#!/bin/sh
# Welcome to CTF (HTB TryOut, general, sanity check)
# The flag is printed directly in the onboarding page body.
TARGET="${1:-154.57.164.82:30352}"
curl -s -m 15 "http://$TARGET/" | grep -oE 'HTB\{[^}]*\}'
