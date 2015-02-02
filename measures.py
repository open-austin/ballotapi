import queries as q

#endpoint() handles '/measures/' endpoint.
def endpoint(params):
    #Initialize the query dictionary. (q_dict). The items select,from,where and order_by are
    #the base of the query that is built.
    q_dict = {'select':(' SELECT DISTINCT ON (me.measure_id) me.measure_id, me.election_id, '
                        ' me.info, me.title, me.question, me.measure_type, me.voting_system ' 
                        ' me.choices '),
              'from':' FROM measures ME ',
              'where':' WHERE TRUE ',
              'order_by':' ORDER BY me.measure_id ',
              #Clauses which may be used to build the query.
              'ids_where_clause':' AND me.measure_id IN %s ',
              'elections_where_clause': ' AND me.election_id IN %s ',
              'election_dates_from_clause':' , elections E ',
              'election_dates_where_clause':' AND e.election_id = me.election_id ',
              'll_where_clause':' AND me.election_id = p.election_id',
              'll_from_clause':' ,precincts P ' }

    #Dictionary into which parameters from the url are passed.  It also acts as a filter: any
    #parameter passed in the query url is checked against the keys in this dictionary.
    param_dict = {'ids':None,
                  'elections':None,
                  'precincts':None,
                  'geo':None,
                  'election_dates':None,
                  'll':None}
    param_dict = q.retrieve_query_parameters(params, param_dict)

    #Initialize param_list inside of param_dict.  This is done here and not inside of the
    #param_dict intialization so that url parameters cant be passed in as ?param_list=.
    param_dict['param_list'] = []

    #These calls build the query and param_list.
    q_dict, param_dict = q.ids_query(q_dict, param_dict)
    q_dict, param_dict = q.elections_query(q_dict, param_dict)
    q_dict, param_dict = q.election_dates_query(q_dict, param_dict)
    q_dict, param_dict = q.ll_query(q_dict, param_dict)
    q_dict, param_list = q.precincts_query(q_dict, param_dict)

    #Run the query that was just built.  This returns all of the data except for the list of
    #measures for each precinct.
    data = q.main_query(q_dict, param_dict)

    #list_sql contains the query to get the list of precincts for each measure the last query
    #retrieved and inserts them into our data.    
    list_sql = (' SELECT MA.precinct_id '
                ' FROM mappings MA '
                ' WHERE MA.measure_id = %s '
                ' ORDER BY MA.precinct_id ')
    data = q.list_query(data, list_sql)

    #Data returned as a list of tuples with each tuple being data for one measure.
    return data

#id_endpoint() handles /measures/<measure_id> endpoint.
def id_endpoint(measure_id):
    #Prebuilt query by id.
    q_dict = {'select':(' SELECT me.measure_id, me.election_id, me.info, me.title, me.question, '
                        ' me.measure_type, me.voting_system, me.choices '),
              'from':' FROM measures ME ',
              'where':' WHERE me.measure_id = %s ',
              'order_by':' ORDER BY me.measure_id '}
    
    #Add the precinct_id to param_list.
    param_dict = {'param_list':[measure_id]}

    #Run the main query.
    data = q.main_query(q_dict, param_dict)

    #Run query to retrieve list of precincts.
    list_sql = (' SELECT MA.precinct_id '
                ' FROM mappings MA '
                ' WHERE MA.measure_id = %s '
                ' ORDER BY MA.precinct_id ')
    data = q.list_query(data, list_sql)

    #Data returned as a list containing one tuple of measure data.
    return data
