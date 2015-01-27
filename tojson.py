import json

def election_json(election_data):
    election_list = []
    for election in election_data:
        election_dict = {}
        election_dict['id'] = election[0]
        election_dict['date'] = election[1]
        election_dict['info'] = election[2]
        election_list.append(election_dict)
    return json.dumps(election_list)
