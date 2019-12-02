"""
BallotAPI - https://ballotapi.org - This code is released to the public domain.

This file is what sets up and runs the actual BallotAPI http server. The actual
server response functions are in the /api folder.
"""
import os, re, sys, time, json, subprocess, tempfile

from . import __version__
from .utils.db import DB_URI_REGEX, DatabaseConfigurationError
from .api import elections
from .api import precincts
from .api import contests

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 1776

URLS = [
    (re.compile("^/elections$"),       elections.elections_list),
    (re.compile("^/elections/[^/]+$"), elections.elections_get),
    (re.compile("^/precincts$"),       precincts.precincts_list),
    (re.compile("^/precincts/[^/]+$"), precincts.precincts_get),
    (re.compile("^/contests$"),        contests.contests_list),
    (re.compile("^/contests/[^/]+$"),  contests.contests_get),
]

# wsgi app
def application(request, start_response):
    """
    This is the wsgi function that builds responses to requests. It uses the
    list of URLS for API endpoints and 404's if an invalid url is requested.
    """
    # loop through valid urls
    for url_re, view in URLS:
        if url_re.match(request['PATH_INFO']):
            # found valid url, so call that view function
            status, headers, data = view(request)
            start_response(status, headers)
            return [data]
    # 404 if no matching url found
    start_response('404 Not Found', [('Content-type', 'application/json')])
    return [json.dumps({
        "error": "404 Not Found",
        "error_description": "This is not a valid url on the API.",
        "error_uri": "https://ballotapi.org/docs/api",
    }, indent=4).encode("utf8")]

# uwsgi server
def _uwsgi_server(host=None, port=None, db_uri=None, cache_uri=None,
                  uwsgi_ini=None):
    """
    This function starts a child uwsgi process and returns that subprocess.
    """
    # find uwsgi executable
    uwsgi_bin = subprocess.check_output(["which uwsgi"], shell=True).strip()
    # custom uwsgi ini file
    if uwsgi_ini:
        uwsgi_command = [uwsgi_bin, uwsgi_ini]
    # default uwsgi command
    else:
        uwsgi_command = [
            uwsgi_bin,
            "--http",
            "{}:{}".format(host or DEFAULT_HOST, port or DEFAULT_PORT),
            "--module",
            "ballotapi.runserver"
        ]
    # start uwsgi subprocess
    uwsgi_process = subprocess.Popen(
        uwsgi_command,
        env={
            "BALLOTAPI_DB_URI": db_uri or "",
            "BALLOTAPI_CACHE_URI": cache_uri or "",
        },
        # working directory is parent directory of this file
        # (so uwsgi can import the ballotapi.runserver module)
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    )
    return uwsgi_process

# main entry point
def ballotapi_runserver(db_uri=None, cache_uri=None, uwsgi_ini=None, func=None,
                        host=None, port=None, daemon=False, stop_fn=None):
    """
    This is the main http server controller. It spins up a uwsgi subprocess
    and listens for signals from the system to control the server.
    """
    # validate db uri
    if db_uri is None:
        db_uri = os.environ.get("BALLOTAPI_DB_URI", "")
    if not DB_URI_REGEX.search(db_uri):
        raise DatabaseConfigurationError(
            "Your --db-uri or $BALLOTAPI_DB_URI don't appear to follow the "
            "proper schema: "
            "postgresql://<user>:<password>@<host>:<port>/<database> (e.g. "
            "postgresql://user:pass@localhost:5432/ballotapi)"
        )

    # daemonize
    #TODO

    # start uwsgi server directly if not daemonizing
    print("BallotAPI Server v{}".format(__version__))
    print("Listening on http://{}:{}...".format(host, port))
    print("Press ctrl+c to stop.")
    uwsgi_process = _uwsgi_server(
        host=host,
        port=port,
        db_uri=db_uri,
        cache_uri=cache_uri,
        uwsgi_ini=uwsgi_ini,
    )
    try:
        # check the uwsgi to see if still running ever 0.1 sec
        while uwsgi_process.poll() is None:
            time.sleep(0.1)
            # check to see if received a signal to stop
            # (used during tests)
            if stop_fn is not None and stop_fn():
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("Stopping...")
        uwsgi_process.terminate()
        uwsgi_process.wait()
        print("Stopped!")
        return

if __name__ == "__main__": # pragma: no cover
    from .cli import runserver_parser
    ballotapi_runserver(**vars(runserver_parser.parse_args(sys.argv[1:])))

