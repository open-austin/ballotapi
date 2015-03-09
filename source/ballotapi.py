from flask import Flask, request, jsonify
from flask.ext.cors import CORS
import elections
import precincts
import measures
import exception
import formatter

#Create our Flask object.
app = Flask(__name__)
#Make our app compatible with Cross Origin Resource Sharing.
cor = CORS(app)

#The app.route('/route/') defines which urls the following functions respond to.  Each function
#can process url base queries at that endpoint and return JSON formatted data.
@app.route('/api/precincts/<precinct_id>')
@app.route('/api/precincts.json/<precinct_id>')
def precinct_id(precinct_id):
    return formatter.precinct_json(precincts.id_endpoint(precinct_id))
    
@app.route('/api/precincts/')
@app.route('/api/precincts.json')
def call_precincts():
    return formatter.precinct_json(precincts.endpoint(request.values))

@app.route('/api/measures/<measure_id>')
@app.route('/api/measures.json/<measure_id>')
def measure_id(measure_id):
    return formatter.measure_json(measures.id_endpoint(measure_id))

@app.route('/api/measures/')
@app.route('/api/measures.json')
def call_measures():
    return formatter.measure_json(measures.endpoint(request.values))

@app.route('/api/elections/<election_id>')
@app.route('/api/elections.json/<election_id>')
def election_id(election_id):
    return formatter.election_json(elections.id_endpoint(election_id))

@app.route('/api/elections/')
@app.route('/api/elections.json')
def call_elections():
    return formatter.election_json(elections.endpoint(request.values))

#Catch BadRequestErrors and return the error message.
@app.errorhandler(exception.BadRequestError)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#Only call app.run if our program is run directly.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

