from flask import Flask, request, jsonify
import elections
import precincts
import exception

app = Flask(__name__)

@app.route('/precincts/<precinct_id>')
def precinct_id(precinct_id):
    return precincts.endpoint(request.values, direct_id = precinct_id)
    
@app.route('/precincts/')
def call_precincts():
    return precincts.endpoint(request.values)

@app.route('/measures/<measure_id>')
def measure_id(measure_id):
    pass

@app.route('/measures/')
def measures():
    pass

@app.route('/elections/<election_id>')
def election_id(election_id):
    return elections.endpoint(request.values, direct_id = election_id)

@app.route('/elections/')
def call_elections():
    return elections.endpoint(request.values)

@app.errorhandler(exception.BadRequestError)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(host='0.0.0.0', debug=True)
