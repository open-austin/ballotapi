import json

#status_code and json_info are returned after JSON in the following functions 
#so that browsers know what type of data is being recieved.
status_code = 200
json_info = {'Content-Type':'application/json; charset=utf-8'}

#Accept election_data list and turn it into JSON formatted output.
def election_json(election_data, offset):
    return_object = {"offset":offset}
    election_list = []
    for election in election_data:
        election_dict = {}
        if election[0]:
            election_dict['id'] = election[0]
        if election[1]:
            election_dict['date'] = election[1].strftime('%Y-%m-%d')
        if election[2]:
            election_dict['info'] = election[2]
        election_list.append(election_dict)
    return_object['data'] = election_list
    return json.dumps(return_object, indent=4), status_code, json_info

#Accept measure_data list and turn it into JSON formatted output.
def measure_json(measure_data, offset):
    return_object = {"offset":offset}
    measure_list = []
    for measure in measure_data:
        measure_dict = {}
        if measure[0]:
            measure_dict['id'] = measure[0]
        if measure[1]:
            measure_dict['election_id'] = measure[1]
        if measure[2]:
            measure_dict['info'] = measure[2]
        if measure[3]:
            measure_dict['title'] = measure[3]
        if measure[4]:
            measure_dict['question'] = measure[4]
        if measure[5]:
            measure_dict['measure_type'] = measure[5]
        if measure[6]:
            measure_dict['voting_system'] = measure[6]
        if measure[7]:
            measure_dict['choices'] = measure[7]
        if measure[8]:
            measure_dict['precincts'] = measure[8]
        measure_list.append(measure_dict)
        return_object['data'] = measure_list
    return json.dumps(return_object, indent=4), status_code, json_info

#Accept precinct_data list and return JSON formatted output.
def precinct_json(precinct_data, offset):
    return_object = {"offset":offset}
    precinct_list = []
    for precinct in precinct_data:
        precinct_dict = {}
        if precinct[0]:
            precinct_dict['id'] = precinct[0]
        if precinct[1]:
            precinct_dict['election_id'] = precinct[1]
        if precinct[2]:
            precinct_dict['info'] = precinct[2]
        if precinct[3]:
            precinct_dict['confirmed'] = precinct[3]
        if precinct[4]:
            precinct_dict['geo'] = json.loads(precinct[4])
        if precinct[5]:
            precinct_dict['measures'] = precinct[5]
        precinct_list.append(precinct_dict)
        return_object['data'] = precinct_list
    return json.dumps(return_object, indent=4), status_code, json_info
