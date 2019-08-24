"""
BallotAPI - https://ballotapi.org - This code is released to the public domain.

This file is what sets up and runs the actual BallotAPI http server. The actual
server response functions are in the /api folder.
"""
import sys

def ballotapi_runserver(**kwargs):
    print("Runserver!!!!")

def _main(argv):
    from cli import runserver_parser
    arg_dict = vars(runserver_parser.parse_args(argv))
    ballotapi_runserver(**arg_dict)

if __name__ == "__main__": # pragma: no cover
    _main(sys.argv[1:])

