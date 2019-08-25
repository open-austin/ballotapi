import json

def json_response(data, status="200 OK", headers=None):
    headers = headers or {}
    headers['Content-Type'] = "application/json"
    return status, headers.items(), json.dumps(data, indent=4, sort_keys=True)

