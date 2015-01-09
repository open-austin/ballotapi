from flask import Flask, request
import json
import psycopg2

db_login_string = 'dbname=ballotdb user=postgres'

app = Flask(__name__)

with psycopg2.connect(db_login_string) as conn:

    def build_precinct_data(precinct_id):
        with conn.cursor() as cur:
            precinct_data = []
            #Retrieve precinct data                                                             
            sql = (' SELECT P.precinct_id, P.election_id, P.info, P.confirmed '
                   ' FROM precincts P '
                   ' WHERE P.precinct_id = %s ')
            cur.execute(sql, (precinct_id,))
            for record in cur:
                for item in record:
                    precinct_data.append(item)
            #Retrieve measure list
            sql = (' SELECT MA.measure_id '
                   ' FROM mappings MA '
                   ' WHERE MA.precinct_id = %s ')
            cur.execute(sql, (precinct_id,))
            measure_list = []
            for record in cur:
                for item in record:
                    measure_list.append(item)
            precinct_data.append(sorted(measure_list))
            return precinct_data

    @app.route('/precincts/<int:precinct_id>')
    def pass_through_id(precinct_id):
        return build_precinct_data(precinct_id)

    @app.route('/precincts/')
    def get_precinct_ids():
        #Initialize parameter dictionary.
        param_dict = {'ids':None,
                      'elections':None,
                      'measures':None,
                      'geo':None,
                      'election_dates':None}
        param_list = []
        #Initialize our SQL clauses.
        select_clause = ' SELECT DISTINCT p.precinct_id '
        from_clause = ' FROM precincts P '
        where_clause = ' WHERE TRUE '
        order_by_clause = ' ORDER BY p.precinct_id '
        #Retrieve parameter data.
        for key in request.args.keys():
            if key in param_dict:
                param_dict[key] = request.values.getlist(key)
            else:
                return 'Invalid Parameter Name: ' + key                
        #Format and validate.
        #?ids=
        if param_dict['ids']:
            if len(param_dict['ids']) > 1:
                return "Error: Only one instance of 'ids=' is allowed."
            where_clause += ' AND p.precinct_id IN %s '
            param_list.append(tuple(int(x) for x in param_dict['ids'][0].split(',')))
            #TODO Error: Invalid Parameter Data if above fails.
        #?elections=
        if param_dict['elections']:
            if len(param_dict['elections']) > 1:
                return "Error: Only one instance of 'elections=' is allowed."
            where_clause += ' AND p.election_id IN %s '
            param_list.append(tuple(int(x) for x in param_dict['elections'][0].split(',')))
        #?measures=
        if param_dict['measures']:
            for index, item in enumerate(param_dict['measures'], start=1):
                from_clause += ', mappings M{} '.format(index)
                where_clause += ' AND p.precinct_id = m{}.precinct_id '.format(index)
                where_clause += ' AND m{}.measure_id IN %s '.format(index)
                param_list.append(tuple(int(x) for x in item.split(',')))
        #?geo=
        if param_dict['geo']:
            geo_list = json.loads('[{}]'.format(param_dict['geo'][0]))
            geo_clause = ' OR ST_Intersects(p.geom, %s) '
            where_clause += 'AND (ST_Intersects(p.geom, %s) {} ) '.format(geo_clause * \
                                                                        len(geo_list[1:]))
            param_list += geo_list
        #?election_dates=
        if param_dict['election_dates']:
            from_clause += ', elections E '
            where_clause += ' AND e.election_date BETWEEN %s AND %s '
            param_list.append(x for x in param_dict['election_dates'][0].split(':'))
        
        #Main Query.
        sql = select_clause + from_clause + where_clause + order_by_clause
        precinct_id_list = []
        precinct_data = []
        with conn.cursor() as cur:
            cur.execute(sql, param_list)
            for record in cur:
                precinct_id_list.append(record[0])
        for id in precinct_id_list:
            precinct_data.append(build_precinct_data(id))
        return str(precinct_data)

app.run(host='0.0.0.0', debug=True)
