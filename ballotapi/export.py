"""
BallotAPI - https://ballotapi.org - This code is released to the public domain.

This file has the logic for exporting the current database to a sql dump file.
"""
import sys

def ballotapi_export(**kwargs):
    print("Export!!!!")

if __name__ == "__main__": # pragma: no cover
    from cli import export_parser
    ballotapi_export(**vars(export_parser.parse_args(sys.argv[1:])))

