from flask import Flask
import precincts

app = Flask(__name__)

params = request.values

@app.route('/precincts/<precinct_id>')
def precinct_id(precinct_id, params):
    return precincts.endpoint(direct_id = precinct_id)
    
@app.route('/precincts/')
def precincts(params):
    return precincts.endpoint()

@app.route('/measures/<measure_id>')
def measure_id(measure_id):
    pass

@app.route('/measures/')
def measures():
    pass

@app.route('/elections/<election_id>')
def election_id(election_id):
    pass

@app.route('/elections/')
def elections():
    pass

app.run(host='0.0.0.0', debug=True)
