import queries as q

#endpoint() handles '/precincts/' endpoint.
def endpoint(params):
    #Initialize the query dictionary. (q_dict). The items select,from,where and order_by are
    #the base of the query that is built.
    q_dict = {'select':(' SELECT DISTINCT ON (p.precinct_id) p.precinct_id, p.election_id, '
                        ' p.info, p.confirmed, ST_AsGeoJSON(p.geom) '),
              'from':' FROM precincts P ',
              'where':' WHERE TRUE ',
              'order_by':' ORDER BY p.precinct_id ',
              #Clauses that might get used to build our query.
              'ids_where_clause':' AND p.precinct_id IN %s ',
              'elections_where_clause':' AND p.election_id IN %s ',
              'election_dates_from_clause':' , elections E ',
              'election_dates_where_clause':' AND e.election_id = p.election_id ',
              'coords_where_clause':'', #Not needed for /precincts.
              'coords_from_clause':''} #Because it doesn't need to join to precincts table.

    #Dictionary into which parameters from the url are passed.  It also acts as a filter: any
    #parameter passed in the query url is checked against the keys in this dictionary.
    param_dict = {'ids':None,
                  'elections':None,
                  'measures':None,
                  'geo':None,
                  'election_dates':None,
                  'coords':None}
    param_dict = q.retrieve_query_parameters(params, param_dict)

    #Initialize param_list inside of param_dict.  This is done here and not inside of the
    #param_dict intialization so that url parameters cant be passed in as ?param_list=.
    param_dict['param_list'] = []

    #These calls build the query and param_list.
    q_dict, param_dict = q.ids_query(q_dict, param_dict)     
    q_dict, param_dict = q.elections_query(q_dict, param_dict)
    q_dict, param_dict = q.election_dates_query(q_dict, param_dict)
    q_dict, param_dict = q.coords_query(q_dict, param_dict)
    q_dict, param_dict = q.measures_query(q_dict, param_dict)

    #Run the query that was just built.  This returns all of the  data except for the list of
    #measures for each precinct.
    data = q.main_query(q_dict, param_dict)

    #list_sql contains the query to get the list of measures for each precinct the last query
    #retrieved and inserts them into our data.
    list_sql = (' SELECT MA.measure_id '
                ' FROM mappings MA '
                ' WHERE MA.precinct_id = %s '
                ' ORDER BY MA.measure_id ')
    data = q.list_query(data, list_sql)

    #Data returned as a list of tuples with each tuple being data for one precinct.
    return data

#id_endpoint() handles /precincts/<precinct_id> endpoint.
def id_endpoint(precinct_id):
    #Prebuilt query by id.
    q_dict = {'select':(' SELECT p.precinct_id, p.election_id, '
                        ' p.info, p.confirmed, ST_AsGeoJSON(p.geom) '),
              'from':' FROM precincts P ',
              'where':' WHERE p.precinct_id = %s ',
              'order_by':' ORDER BY p.precinct_id '}
    
    #Add the precinct_id to param_list.
    param_dict = {'param_list':[precinct_id]}

    #Run the main query.
    data = q.main_query(q_dict, param_dict)

    #Run query to retrieve list of measuers.
    list_sql = (' SELECT MA.measure_id '
                ' FROM mappings MA '
                ' WHERE MA.precinct_id = %s '
                ' ORDER BY MA.measure_id ')
    data = q.list_query(data, list_sql)

    #Data returned as a list with one tuple of precinct data.
    return data
