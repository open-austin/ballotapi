# BallotAPI Tests

This folder has the tests for the BallotAPI server.

## Running Tests

To run the test suite, you need to download the source repository,
install the base and test dependencies, and run python's test runner.
```bash
git clone https://github.com/open-austin/ballotapi.git
cd ballotapi
pip install -r requirements.txt -r tests/requirements.txt
python3 -m unittest discover
```

## Code Coverage

If you want to run tests with code coverage, simply replace `python3`
with the `coverage` package.
```bash
# run tests with coverage (will create a .coverage file)
coverage run -m unittest discover
# print code coverage report (will print to terminal)
coverage report -m
# generate html report (will make index.html in folder)
coverage html -d /tmp/ballotapi_coverage
```

