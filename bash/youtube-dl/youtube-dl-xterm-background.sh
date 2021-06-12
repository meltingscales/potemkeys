#!/usr/bin/env bash

while read p; do
    command="youtube-dl '$p'";
    echo "Running $command";
    xterm -e "$command && sleep 999" &
done <urls.txt

