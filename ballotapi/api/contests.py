from ..utils.response import json_response

def contests_list(request):
    return json_response({"contests": "list"})

def contests_get(request):
    return json_response({"contests": "get"})

