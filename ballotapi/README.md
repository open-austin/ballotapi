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

Alternatively, you can run from source directly:
```bash
git clone https://github.com/open-austin/ballotapi.git
cd ballotapi
pip install -r requirements.txt
python3 -m ballotapi.cli --help
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
ballotapi load "testdata-default"
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
usage: ballotapi runserver [-h] [--db-uri URI] [--cache-uri URI] [--host HOST]
                           [--port PORT] [--uwsgi-ini FILE] [--daemon]

This command is what you use to actually run a ballotapi server. By default,
it spins up a uwsgi server in a child process and listens on port 1776. The
data served is from the specified database, so if you haven't loaded any data
yet, you should run the `ballotapi load` command first.

optional arguments:
  -h, --help        show this help message and exit
  --db-uri URI      connection uri to the postgres database (default is
                    BALLOTAPI_DB_URI env variable)
  --cache-uri URI   connection uri to a cache server (default is None)
  --host HOST       listen for this host (default localhost)
  --port PORT       listen on this port (default 1776)
  --uwsgi-ini FILE  settings for uwsgi (default is a simple http server)
  --daemon          detach server to run in background as a daemon (optional)

==Documentation==
https://ballotapi.org/docs

==Examples==
BALLOTAPI_DB_URI="postgresql://user:pass@localhost:5432/ballotapi"
ballotapi runserver
ballotapi runserver --daemon
ballotapi runserver --daemon --uwsgi-ini uwsgi.ini
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
usage: ballotapi [-h] [-V] <subcommand> ...

This is a simple http server for serving up U.S. election ballot information
via REST API.

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit

available subcommands:
  <subcommand>
    runserver    Run the web server
    load         Load in a database from a source location
    export       Dump the database as a sql file

==Documentation==
https://ballotapi.org/docs

==Examples==
BALLOTAPI_DB_URI="postgresql://user:pass@localhost:5432/ballotapi"
ballotapi load testdata-default
ballotapi runserver
ballotapi export > backup.sql
```

## Contributing

Help us out! If you find a bug or want to improving this codebase,
feel free to submit an
[issue](https://github.com/open-austin/ballotapi/issues)
or [pull request](https://github.com/open-austin/ballotapi/pulls).
Check out our [CONTRIBUTING](../CONTRIBUTING.md) docs for more details.

