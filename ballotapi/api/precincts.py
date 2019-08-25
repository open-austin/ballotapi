from ..utils.response import json_response

def precincts_list(request):
    return json_response({"precincts": "list"})

def precincts_get(request):
    return json_response({"precincts": "get"})

