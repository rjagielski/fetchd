# Fetch Daemon

Daemon for downloading files. Paths to download are passed to socket and
queued for the download. Queue is handled in FIFO order. Files are downloaded using
rsync. Other featuers:

- Paths are signed with itsdangerous
- Configurable through ~/.config/fetchd/config.py

# Authentication

Set TOKEN in ~/.config/fetchd/config.py

```
TOKEN='123456789'
```

# Installing dependencies

Create and activate virtualenv. Run `make init`

# Running tests

`make test`

# Running the daemon
`make run`
