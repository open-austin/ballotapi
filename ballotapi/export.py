"""
BallotAPI - https://ballotapi.org - This code is released to the public domain.

This file has the logic for exporting the current database to a sql dump file.
"""
import sys

def ballotapi_export(**kwargs):
    print("Export!!!!")

def _main(argv):
    from cli import export_parser
    arg_dict = vars(export_parser.parse_args(argv))
    ballotapi_export(**arg_dict)

if __name__ == "__main__": # pragma: no cover
    _main(sys.argv[1:])

