# Fetch Daemon

Daemon for downloading files. Paths to download are passed to socket and
queued by the deamon. Queue is handled in FIFO order. Files are downloaded using
rsync. Paths need to be signed with itsdangerous.


# Example commands

fetchd/server.py 'security-key' /home/user/sync-here user@example.com

fetchd/client.py 'sucurity-key' '/path/to/sync'

# Compatibility

python3.5 or newer
