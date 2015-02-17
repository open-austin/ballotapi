import sys
import logging

#This sends logging output to sys.stderr which Apache catches and sends to a log file.
logging.basicConfig(stream=sys.stderr)

#Insert the path to ballotapi.
sys.path.insert(0, '/path/to/ballotapi')

#Use the virtual environment we created for this application.
#This is different than the flask docs because we are using Python3.
activate_this = '/path/to/ballotapi/virtualenv/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

from ballotapi import app as application
