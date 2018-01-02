# Fetch Daemon

Daemon for downloading files. Paths to download are passed to socket and
queued for the download. Queue is handled in FIFO order. Files are downloaded using
rsync. Paths are signed with itsdangerous
