import io
import sys
import unittest

import ballotapi.cli

class CommandlineTestCase(unittest.TestCase):

    def setUp(self):
        """ Patch stdout and stderr to capture output """
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

    def tearDown(self):
        """ Revert stdout and stderr patches """
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def _flush_stdout(self):
        """ Flush current buffer of stdout """
        sys.stdout.seek(0)
        out = sys.stdout.read()
        sys.stdout = io.StringIO()
        return out

    def _flush_stderr(self):
        """ Flush current buffer of stderr """
        sys.stderr.seek(0)
        err = sys.stderr.read()
        sys.stderr = io.StringIO()
        return err

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


