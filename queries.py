import datetime
import psycopg2
import exception

#Input: parameter_dictionary that has empty keys.
#Output: parameter_dictionary filled with values from query url.
#This function retrieves the query data and also makes sure that
#the url query has proper parameter names as defined by the keys
#in the parameter dictionary.
def retrieve_query_parameters(params, param_dict):
    #Retrieve parameter data.
    for key in params:
        if key in param_dict:
            param_dict[key] = params.getlist(key)
        else:
            message = ('Invalid Parameter Name: ' + key + '\n'
                       'Valid Parameter Names are: ' + str(param_dict.keys()))
            raise exception.BadRequestError(message)
    return param_dict

def ids_query(q_dict, param_dict, param_list, where_clause):
    #Check if there is an id query.
    if param_dict['ids']:
        #Check that there is only one ids= instance.
        if len(param_dict['ids']) > 1:
            raise exception.BadRequestError('Error: Only one instance of "ids=" is allowed')
        try:
            #Split query string on commas and cast pieces to ints.
            #Then wrap into a tuple as that is what psycopg2 accepts.
            param_list.append(tuple(int(x) for x in param_dict['ids'][0].split(',')))
        except (TypeError, ValueError) as e:
            message = ('Error: Invalid parameter value in "ids=" clause: ' + param_dict['ids'][0] +
                       '\nValues must be comma seperated integers.')
            raise exception.BadRequestError(message)
        q_dict['where'] += where_clause
    return q_dict, param_list

def elections_query(q_dict, param_dict, param_list, where_clause):
    #Check if there is an elections query.
    if param_dict['elections']:
        #Check that there is only one elections= instance.
        if len(param_dict['elections']) > 1:
            raise exception.BadRequestError('Error: Only one instance of "elections=" is allowed')
        try:
            #Split query string on commas and cast pieces to ints.
            #Then wrap into a tuple as that is what psycopg2 accepts.
            param_list.append(tuple(int(x) for x in param_dict['elections'][0].split(',')))
        except (TypeError, ValueError) as e:
            message = ('Error: Invalid parameter value in "elections=" clause: ' +
                       param_dict['elections'][0] + '\nValues must be comma seperated integers.')
        q_dict['where']+= where_clause
    return q_dict, param_list

def election_dates_query(q_dict, param_dict, param_list, from_clause, where_clause):
    #Check if there is an election_dates query.
    if param_dict['election_dates']:
        #Check that there is only one election_dates= instance.
        if len(param_dict['election_dates']) > 1:
            message = ('Error: Only one instance of "election_dates=" is permitted')
            raise exception.BadRequestError(message)
        q_dict['from'] += from_clause
        q_dict['where'] += where_clause
        #Split date string into two lists: single_dates and date_ranges.
        #Add to base_where_clause and param_list for each list seperately.
        date_ranges = []
        single_dates = []
        for date in param_dict['election_dates'][0].split(','):
            if ':' in date:
                date_ranges.append(date)
            else:
                single_dates.append(date)
        if date_ranges:
            for date_range in date_ranges:
                try:
                    for date in date_range.split(':'):
                        param_list.append(datetime.datetime.strptime(date, '%Y-%m-%d').date())
                    q_dict['where'] += ' AND e.election_date BETWEEN %s AND %s '
                except (TypeError, ValueError) as e:
                    message = ('Error: Invalid Parameter Value in "election_dates=" clause: ' + 
                               str(date_ranges) + 'Date ranges must be in YYYY-MM-DD:YYYY-MM-DD'
                               'format.')
                    raise exception.BadRequestError(message)
        if single_dates:
            try:
                dl=[datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in single_dates]
                param_list.append(tuple(dl))
                q_dict['where'] += ' AND e.election_date IN %s '
            except (TypeError, ValueError) as e:
                message = ('Error: Invalid Parameter Value in "election_dates=" clause: ' +
                           str(single_dates) + 'Dates must be in YYYY-MM-DD format.')
                raise exception.BadRequestError(message)
    return q_dict, param_list

def ll_query(q_dict, param_dict, param_list, where_clause, from_clause):
    if param_dict['ll']:
        coords = param_dict['ll'][0].split(',')
        if len(coords) % 2 != 0:
            message = ('Error: You have entered an odd number of coordinates.  Coordinates '
                       'must be entered in pairs')
            raise exception.BadRequestError(message)
        try:
            for num in coords:
                param_list.append(float(num))
        except (TypeError, ValueError) as e:    
            raise exception.BadRequestError('Error: Not a floating point number')
        #ST_Collect is seen by PostgreSQL as an aggregate function if it is only given one
        #input.  If there is only one coordinate pair, don't use ST_Collect.
        if len(coords) == 2:
            q_dict['where'] += ' AND ST_Intersects(p.geom, ST_MakePoint(%s,%s)) '
        else:
            #Add an ST_MakePoint for each pair of coordinates.  The [:-1] removes
            #the comma on the last one.
            collect_clause = ('ST_MakePoint(%s,%s),' * (len(coords)//2))[:-1]
            q_dict['where'] += ' AND ST_Intersects(p.geom,ST_Collect({})) '.format(collect_clause)
        q_dict['from'] += from_clause
        q_dict['where'] += where_clause
    return q_dict, param_list

def measures_query(q_dict, param_dict, param_list):                    
    if param_dict['measures']:
        for index, query_string in enumerate(param_dict['measures'], start=1):
            try:
                param_list.append(tuple(int(x) for x in query_string.split(',')))
                q_dict['from'] += ', mappings MA{} '.format(index)
                q_dict['where'] += ' AND p.precinct_id = ma{}.precinct_id '.format(index)
                q_dict['where'] += ' AND ma{}.measure_id IN %s '.format(index)
            except (NameError, TypeError) as e:
                message =  'Error: measures must be given as comma delineated integers.'
                raise exception.BadRequestError(message)
    return q_dict, param_list

def precincts_query(q_dict, param_dict, param_list):
    if param_dict['precincts']:
        for index, query_string in enumerate(param_dict['precincts'], start=1):
            try:
                param_list.append(tuple(int(x) for x in query_string.split(',')))
                q_dict['from'] += ', mappings MA{} '.format(index)
                q_dict['where'] += ' AND me.measure_id = ma{}.measure_id '.format(index)
                q_dict['where'] += ' AND ma{}.precinct_id IN %s '.format(index)
            except (NameError, TypeError) as e:
                message = 'Error: precincts must be given as comma delineated integers.'
                raise exception.BadRequestError(message)
    return q_dict, param_list

db_login_string = 'dbname=ballotdb user=postgres'

def main_query(q_dict, param_list):
    sql = q_dict['select'] + q_dict['from'] + q_dict['where'] + q_dict['order_by']
    data = []
    with psycopg2.connect(db_login_string) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, param_list)
            except psycopg2.ProgrammingError:
                print(cur.mogrify(sql, param_list)) #TODO: add logging.
                raise
            for record in cur:
                data.append(record)
    return data

def list_query(data, sql):
    with psycopg2.connect(db_login_string) as conn:
        with conn.cursor() as cur:
            for index, row in enumerate(data):
                cur.execute(sql, (row[0],))
                list_ = []
                for record in cur:
                    list_.append(record[0])
                row += (measure_list,)
                data[index] = row
    return data

