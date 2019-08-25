from ..utils.response import json_response

def elections_list(request):
    return json_response({"elections": "list"})

def elections_get(request):
    return json_response({"elections": "get"})

