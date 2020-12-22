#!/bin/sh

hashcat -a 0 -m 1420 django-salted-sha256.hash example.dict -r best64.rule
# We use mode 1420 here because the format from the database was 'hash(salt); hash(password)'
# Run `man hashcat` for more info

# --show 
# --force