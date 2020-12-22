#!/bin/sh

hashcat -a 0 -m 1420 django-salted-sha256.hash example.dict -r best64.rule
# --show 
# --force