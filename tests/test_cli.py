import unittest

from .mixins import BallotAPITestMixin
import ballotapi.cli

class CommandlineTestCase(BallotAPITestMixin, unittest.TestCase):

    def setUp(self):
        """ Patch stdout and stderr to capture output """
        self._capture_output()

    def tearDown(self):
        """ Revert stdout and stderr patches """
        self._revert_capture_output()

    def test_cli_help(self):
        """ Successfully print the command-line interface help text """

        # ballotapi --help
        with self.assertRaises(SystemExit) as sys_exit:
            ballotapi.cli.main(["--help"])
        self.assertEqual(sys_exit.exception.code, 0)
        self.assertIn("usage: ballotapi [-h] [-V] <subcommand> ...", self._flush_stdout())

        # ballotapi runserver --help
        with self.assertRaises(SystemExit) as sys_exit:
            ballotapi.cli.main(["runserver", "--help"])
        self.assertEqual(sys_exit.exception.code, 0)
        self.assertIn("usage: ballotapi runserver [-h]", self._flush_stdout())

        # ballotapi load --help
        with self.assertRaises(SystemExit) as sys_exit:
            ballotapi.cli.main(["load", "--help"])
        self.assertEqual(sys_exit.exception.code, 0)
        self.assertIn("usage: ballotapi load [-h]", self._flush_stdout())

        # ballotapi export --help
        with self.assertRaises(SystemExit) as sys_exit:
            ballotapi.cli.main(["export", "--help"])
        self.assertEqual(sys_exit.exception.code, 0)
        self.assertIn("usage: ballotapi export [-h]", self._flush_stdout())

    def test_cli_export(self):
        """ Running export from the command line works """
        ballotapi.cli.main(["export"])
        self.assertIn("Export!!!!", self._flush_stdout()) # this will fail once load actually works

