from flask import Flask, request, jsonify
from flask.ext.cors import CORS
import elections
import precincts
import measures
import exception
import formatter

app = Flask(__name__)
cor = CORS(app)

ctype = {'Content-Type':'application/json; charset=utf-8'}

@app.route('/precincts/<precinct_id>')
def precinct_id(precinct_id):
    return formatter.precinct_json(precincts.endpoint(request.values, direct_id = precinct_id))
    
@app.route('/precincts/')
def call_precincts():
    return formatter.precinct_json(precincts.endpoint(request.values))

@app.route('/measures/<measure_id>')
def measure_id(measure_id):
    return formatter.measure_json(measures.endpoint(request.values, direct_id = measure_id))

@app.route('/measures/')
def call_measures():
    return formatter.measure_json(measures.endpoint(request.values))

@app.route('/elections/<election_id>')
def election_id(election_id):
    return formatter.election_json(elections.endpoint(request.values, direct_id = election_id))

@app.route('/elections/')
def call_elections():
    return formatter.election_json(elections.endpoint(request.values))

@app.errorhandler(exception.BadRequestError)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

