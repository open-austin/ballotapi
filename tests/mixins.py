import os
import sys
import time
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import ballotapi.runserver

class BallotAPITestMixin(object):
    """
    These are general testing helper methods that are used by
    multiple test cases.
    """

    # test server defaults (to run tests in parallel, you need
    # to specify different env variables for each process)
    TEST_PORT = os.environ.get("BALLOTAPI_TEST_PORT", 26401)
    TEST_DB_URI = os.environ.get("BALLOTAPI_TEST_DB_URI", "postgresql://user:pass@localhost:5432/ballotapi")

    def _request(self, path):
        """ Shortcut function to make a request to a wsgi endpoint. """
        # build a mock request
        request = {
            "REQUEST_METHOD": "GET",
            "SCRIPT_NAME": "",
            "PATH_INFO": path.split("?", 1)[0],
            "QUERY_STRING": path.split("?", 1)[1] if "?" in path else "",
            "SERVER_NAME": "127.0.0.1",
            "SERVER_PORT": self.TEST_PORT,
            "SERVER_PROTOCOL": "HTTP/1.1",
            "HTTP_": "", # no additional headers in request
        }
        # make the request to the internal wsgi application
        resp = {"status": None, "headers": {}, "data": "".encode("utf8")}
        def start_response_fn(status, headers):
            resp['status'] = status
            resp['headers'] = headers
        for data_chunk in ballotapi.runserver.application(request, start_response_fn):
           resp['data'] += data_chunk
        return resp['status'], resp['headers'], resp['data']

    def _capture_output(self):
        """ Patch stdout and stderr to capture output """
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def _revert_capture_output(self):
        """ Revert stdout and stderr patches """
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def _flush_stdout(self):
        """ Flush current buffer of stdout """
        sys.stdout.seek(0)
        out = sys.stdout.read()
        sys.stdout = StringIO()
        return out

    def _flush_stderr(self):
        """ Flush current buffer of stderr """
        sys.stderr.seek(0)
        err = sys.stderr.read()
        sys.stderr = StringIO()
        return err

