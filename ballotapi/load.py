"""
BallotAPI - https://ballotapi.org - This code is released to the public domain.

This file has the logic for loading a dataset into the database. The dataset can
either be in .sql backup format or our BallotAPI-specific folder structure of
YAML files. A user can provide either a local or remote location for the dataset
and it can even just be a simple name of a branch that is on the ballotapi-data
repository.
"""
import sys

def ballotapi_load(**kwargs):
    print("Load!!!!")

if __name__ == "__main__": # pragma: no cover
    from .cli import load_parser
    ballotapi_load(**vars(load_parser.parse_args(sys.argv[1:])))

