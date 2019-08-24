"""
BallotAPI - https://ballotapi.org - This code is released to the public domain.

This file is where the BallotAPI command line functionality lives. All the command
and subcommand options are defined here. This is the file that is used when you
run the basic `ballotapi ...` command. Alternatively, you can run this file by
simply importing it as a module (e.g. `python3 -m ballotapi.cli --help`). The
functionality for each subcommand is located in sibling files (e.g. runserver.py,
load.py, export.py).
"""
import sys, argparse, textwrap

from . import __version__
from .runserver import ballotapi_runserver
from .load import ballotapi_load
from .export import ballotapi_export

class ParagraphFormatter(argparse.HelpFormatter):
    """ Allows for paragraphs in descriptions using the ¶ character. """
    def _fill_text(self, text, width, indent):
        return "".join([
            "{}\n".format(textwrap.fill(p, width, initial_indent=indent, subsequent_indent=indent)) \
            for p in self._whitespace_matcher.sub(' ', text).strip().split('¶')
        ])

cli_parser = argparse.ArgumentParser(
    prog="ballotapi",
    formatter_class=ParagraphFormatter,
    description=(
        "This is a simple http server for serving up U.S. election ballot "
        "information via REST API."
    ),
    epilog=(
        "==Documentation==¶"
        "https://ballotapi.org/docs¶¶"
        "==Examples==¶"
        "BALLOTAPI_DB_URI=\"postgresql://user:pass@localhost:5432/ballotapi\"¶"
        "ballotapi load testdata-default¶"
        "ballotapi runserver¶"
        "ballotapi export > backup.sql"
    ))
cli_parser.add_argument("-V", "--version", action="version",
    version=__version__)
cli_subparsers = cli_parser.add_subparsers(title="available subcommands",
    metavar="<subcommand>")

# runserver
runserver_parser = cli_subparsers.add_parser(
    "runserver",
    formatter_class=ParagraphFormatter,
    help="Run the web server",
    description=(
        "This command is what you use to actually run a ballotapi server. "
        "By default, it spins up a uwsgi server in a child process and listens "
        "on port 1776. The data served is from the specified database, so if "
        "you haven't loaded any data yet, you should run the `ballotapi load` "
        "command first."
    ),
    epilog=(
        "==Documentation==¶"
        "https://ballotapi.org/docs¶¶"
        "==Examples==¶"
        "BALLOTAPI_DB_URI=\"postgresql://user:pass@localhost:5432/ballotapi\"¶"
        "ballotapi runserver¶"
        "ballotapi runserver --daemon¶"
        "ballotapi runserver --daemon --uwsgi-ini uwsgi.ini¶"
    ))
runserver_parser.set_defaults(func="runserver")
runserver_parser.add_argument("--db-uri", metavar="URI", default=None,
    help="connection uri to the postgres database (default is BALLOTAPI_DB_URI env variable)")
runserver_parser.add_argument("--cache-uri", metavar="URI", default=None,
    help="connection uri to a cache server (default is None)")
runserver_parser.add_argument("--host", metavar="HOST", default="localhost",
    help="listen for this host (default localhost)")
runserver_parser.add_argument("--port", metavar="PORT", default="1776",
    help="listen on this port (default 1776)")
runserver_parser.add_argument("--uwsgi-ini", metavar="FILE", default=None,
    help="settings for uwsgi (default is a simple http server)")
runserver_parser.add_argument("--daemon", action="store_true", default=False,
    help="detach server to run in background as a daemon (optional)")

# load
load_parser = cli_subparsers.add_parser(
    "load",
    formatter_class=ParagraphFormatter,
    help="Load in a database from a source location",
    description=(
        "This command imports a dataset to the specified database "
        "The source data can either be a previously dumped .sql file (e.g. "
        "from `ballotapi export`) or a folder that contains a BallotAPI-specific "
        "structure of YAML files (see ballotapi-data repo). For the location "
        "you can specify a local filesystem path (e.g. \"/tmp/dump.sql\"), a url "
        "from which the data can be downloaded (e.g. \"https://.../dump.sql\"), "
        "or a branch/tag name on the ballotapi-data project (e.g. \"testdata-default\")."
    ),
    epilog=(
        "==Documentation==¶"
        "https://ballotapi.org/docs¶¶"
        "==Examples==¶"
        "BALLOTAPI_DB_URI=\"postgresql://user:pass@localhost:5432/ballotapi\"¶"
        "ballotapi load testdata-default¶"
        "ballotapi load /path/to/backup.sql¶"
        "ballotapi load https://dumps.ballotapi.org/latest/testdata-default.sql¶"
        "ballotapi load git://github.com/myuser/myfork/tree/master¶"
    ))
load_parser.set_defaults(func="load")
load_parser.add_argument("--db-uri", metavar="URI", default=None,
    help="connection uri to the postgres database (default is BALLOTAPI_DB_URI env variable)")
load_parser.add_argument("location", metavar="PATH_URL_OR_GIT", nargs=1,
    help="where the data to be loaded is located (can be a path, url, or git reference)")

# export
export_parser = cli_subparsers.add_parser(
    "export",
    formatter_class=ParagraphFormatter,
    help="Dump the database as a sql file",
    description=(
        "This command dumps the current database as a sql backup file. You typcially "
        "want to redirect stdout to a .sql file (e.g. `ballotapi export > backup.sql`)."
    ),
    epilog=(
        "==Documentation==¶"
        "https://ballotapi.org/docs¶¶"
        "==Examples==¶"
        "BALLOTAPI_DB_URI=\"postgresql://user:pass@localhost:5432/ballotapi\"¶"
        "ballotapi export > backup.sql"
    ))
export_parser.set_defaults(func="export")
export_parser.add_argument("--db-uri", metavar="URI", default=None,
    help="connection uri to the postgres database (default is BALLOTAPI_DB_URI env variable)")

def main(argv=None):
    arg_dict = vars(cli_parser.parse_args(argv))
    func = arg_dict.pop("func")
    {
        "runserver": ballotapi_runserver,
        "load": ballotapi_load,
        "export": ballotapi_export,
    }[func](**arg_dict)

if __name__ == "__main__": # pragma: no cover
    main(sys.argv[1:])

