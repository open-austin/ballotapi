# BallotAPI Server

**WARNING: THE CODE FOR THIS README HASN'T BEEN WRITTEN YET**

This folder has the code for the BallotAPI server itself. If you
want to run your own mirror of our ballot API, this is the code
you are looking for.

## Installation

### 1. Install the BallotAPI server

The easiest way to install is via [PyPI](https://pypi.org/project/ballotapi/):
```bash
pip install ballotapi
```

To update, just add the `-U` flag.
```bash
pip install -U ballotapi
```

Alternatively, you can install directly from source:
```bash
git clone https://github.com/open-austin/ballotapi.git
pip install -e ballotapi/
```

### 2. Setup your database

The BallotAPI server requires a database of ballot data be loaded.
You can download a copy of various
[test databases](#TODO),
the [full production database](#TODO),
or [build your own](#TODO).

You can skip this step if you already have your database loaded.

```bash
# Install PostgreSQL and PostGIS plugin
sudo apt-get install postgresql postgis

# Create a BallotAPI database and user
sudo -u postgres psql -c "CREATE DATABASE ballotapi;"
sudo -u postgres psql -c "CREATE USER ballotapiuser WITH ENCRYPTED PASSWORD 'yourpasswordhere';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ballotapi TO ballotapiuser;"

# Set database connection uri environmental variable
export BALLOTAPI_DB_URI="postgresql://ballotapiuser:yourpasswordhere@localhost:5432/ballotapi"

# Load a dataset into your database
ballotapi load "https://dumps.ballotapi.org/latest/ballotapi_testdata_default.sql"
```

## Usage

Now that the BallotAPI server is installed and a database is loaded,
you are ready to run the server!

```bash
ballotapi runserver
```

To customize the settings of your server, check out which options
there are using `ballotapi runserver --help`.

```bash
usage: ballotapi runserver [-h] [--db-uri DB] [--cache-uri CACHE]
                           [--host H] [--port N] [--uwsgi-ini FILE]
                           [--daemon] [--pidfile FILE]

optional arguments:
  -h, --help         show this help message and exit
  --db-uri DB        connection information to the postgres database (default
                     is to look at the BALLOTAPI_DB_URI environmental variable)
  --cache-uri CACHE  connection information to a cache server (default is None)
  --host H           listen for this host (default localhost)
  --port N           listen on this port (default 1776)
  --uwsgi-ini FILE   settings for uwsgi (default is a simple http server)
  --daemon           detach server to run in background as a daemon (optional)
  --pidfile FILE     set a pidfile for the daemon server (default is None)
```

To stop the server when you're running it directly from the command line,
simply use `Ctrl+C`. To stop/reload a server that's running in the background
as a daemon, send signals to the process.

```bash
# gracefully reload
killall -s SIGHUP ballotapi

# gracefully stop
killall -s SIGTERM ballotapi

# brutally reload
killall -s SIGINT ballotapi

# brutally stop
killall -s SIGKILL ballotapi
```

## Commands

```
usage: ballotapi [-h] COMMAND [args]

BallotAPI is an API for election and ballot information.

The server itself uses various subcommands:
  runserver   Run the web server
  load        Load in a database from a source location
  export      Dump the database into a backup file

You can see options for a command by putting --help after each command.
(e.g. ballotapi runserver --help)

Documentation for the API is online:
https://ballotapi.org/docs
```

## Contributing

Help us out! If you find a bug or want to improving this codebase,
feel free to submit an
[issue](https://github.com/open-austin/ballotapi/issues)
or [pull request](https://github.com/open-austin/ballotapi/pulls).
Check out our (CONTRIBUTING)[../CONTRIBUTING.md] docs for more details.

