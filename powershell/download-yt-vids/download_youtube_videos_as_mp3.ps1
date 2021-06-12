get-content "videos.txt" | ForEach-Object {

    write-host "downloading" $_ " as mp3"

    python -m youtube_dl -x --audio-format mp3 $_

}

