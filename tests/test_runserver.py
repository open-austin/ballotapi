import os
import time
import unittest
import threading
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from .mixins import BallotAPITestMixin
import ballotapi.utils.db
import ballotapi.runserver

class CommandlineTestCase(BallotAPITestMixin, unittest.TestCase):

    def test_uwsgi(self):
        """ Verify the uwsgi server will start and respond to requests """
        # spin up a uwsgi server
        stop_event = threading.Event()
        stop_fn = stop_event.is_set
        runserver_thread = threading.Thread(
            target=ballotapi.runserver.ballotapi_runserver,
            kwargs={
                "port": self.TEST_PORT,
                "db_uri": self.TEST_DB_URI,
                "stop_fn": stop_fn,
            },
        )
        runserver_thread.start()
        time.sleep(1) # wait for uwsgi server to start

        # make a request to the server
        resp = urlopen("http://127.0.0.1:{}/elections".format(self.TEST_PORT))
        self.assertEqual(resp.getcode(), 200)
        self.assertEqual(resp.read(), "{\n    \"elections\": \"list\"\n}".encode("utf8"))

        # stop the server
        stop_event.set()
        runserver_thread.join()

    def test_invalid_db_uri(self):
        """ Invalid DB URIs raise an error """
        self.assertRaises(
            ballotapi.utils.db.DatabaseConfigurationError,
            ballotapi.runserver.ballotapi_runserver,
            port=self.TEST_PORT,
            db_uri="bad_db_uri",
        )

    def test_404(self):
        """ Return a 404 for non-existent urls """
        resp_status, resp_headers, resp_data = self._request("/ballot-stuffing")
        self.assertEqual("404 Not Found", resp_status)

    def test_200(self):
        """ Return a 200 for a valid url """
        resp_status, resp_headers, resp_data = self._request("/elections")
        self.assertEqual("200 OK", resp_status)

