import json

def election_json(election_data):
    election_list = []
    for election in election_data:
        election_dict = {}
        election_dict['id'] = election[0]
        election_dict['date'] = election[1].strftime('%Y-%m-%d')
        election_dict['info'] = election[2]
        election_list.append(election_dict)
    return json.dumps(election_list)

def measure_json(measure_data):
    measure_list = []
    for measure in measure_data:
        measure_dict = {}
        measure_dict['id'] = measure[0]
        measure_dict['election_id'] = measure[1]
        measure_dict['info'] = measure[2]
        measure_dict['title'] = measure[3]
        measure_dict['question'] = measure[4]
        measure_dict['measure_type'] = measure[5]
        measure_dict['voting_system'] = measure[6]
        measure_dict['choices'] = measure[7]
        measure_dict['precincts'] = measure[8]
        measure_list.append(measure_dict)
    return json.dumps(measure_list)

def precinct_json(precicnt_data):
    precinct_list = []
    for precinct in precinct_data:
        precinct_dict = {}
        precinct_dict['id'] = precinct[0]
        precinct_dict['election_id'] = precinct[1]
        precinct_dict['info'] = precinct[2]
        precinct_dict['confirmed'] = precinct[3]
        precinct_dict['geo'] = precinct[4]
        precinct_dict['measures'] = precinct[5]
        precinct_list.append(precinct_dict)
    return json.dumps(measure_list)
