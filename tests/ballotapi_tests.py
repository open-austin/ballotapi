import sys
import urllib
import unittest
import json
import pytest


def HasResponse(response):
    data = json.load(response)
    return len(data)

class TestAPI:
    HOST_NAME = 'http://50.116.6.242/'
    
    def test_HasElections(self):
        assert HasResponse(urllib.urlopen(self.HOST_NAME+'api/elections/'))
        
    def test_HasPrecincts(self):
        assert HasResponse(urllib.urlopen(self.HOST_NAME+'api/precincts/'))
        
    def test_has_measures(self):
        assert HasResponse(urllib.urlopen(self.HOST_NAME+'api/precincts/'))
