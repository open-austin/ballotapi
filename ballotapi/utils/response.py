import json

def json_response(data, status="200 OK", headers=None):
    headers = headers or {}
    headers['Content-type'] = "application/json"
    response_data = json.dumps(data, indent=4, sort_keys=True).encode("utf8")
    return status, list(headers.items()), response_data

