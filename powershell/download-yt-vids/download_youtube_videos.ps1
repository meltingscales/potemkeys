get-content "videos.txt" | ForEach-Object {

    write-host "downloading" $_

    python -m youtube_dl $_

}

