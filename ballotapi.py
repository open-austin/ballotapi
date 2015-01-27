from flask import Flask, request, jsonify
from flask.ext.cors import CORS
import elections
import precincts
import measures
import exception
import tojson

app = Flask(__name__)
cor = CORS(app)

@app.route('/precincts/<precinct_id>')
def precinct_id(precinct_id):
    return precincts.endpoint(request.values, direct_id = precinct_id)
    
@app.route('/precincts/')
def call_precincts():
    return precincts.endpoint(request.values)

@app.route('/measures/<measure_id>')
def measure_id(measure_id):
    return measures.endpoint(request.values, direct_id = measure_id)

@app.route('/measures/')
def call_measures():
    return measures.endpoint(request.values)

@app.route('/elections/<election_id>')
def election_id(election_id):
    return tojson.election_json(elections.endpoint(request.values, direct_id = election_id))

@app.route('/elections/')
def call_elections():
    return tojson.election_json(elections.endpoint(request.values))

@app.errorhandler(exception.BadRequestError)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(host='0.0.0.0', debug=True)
