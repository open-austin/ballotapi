import queries as q

#endpoint() handles '/elections/' endpoint.
def endpoint(params):
    #Initialize the query dictionary. (q_dict). The items select,from,where and order_by are
    #the base of the query that is built.
    q_dict = {'select':' SELECT DISTINCT e.election_id, e.election_date, e.info ',
              'from':' FROM elections E ',
              'where':' WHERE TRUE ',
              'order_by':' ORDER BY e.election_id ',
              #Clauses that might be used to build the query.
              'ids_where_clause': ' AND e.election_id IN %s ',
              'election_dates_from_clause':'', #Not needed for /elections
              'election_dates_where_clause':'', #Because it doesn't need to join elections table.
              'll_where_clause':' AND p.election_id = e.election_id ',
              'll_from_clause':' ,precincts P '}

    #Dictionary into which parameters from the url are passed.  It also acts as a filter: any
    #parameter passed in the query url is checked against the keys in this dictionary.
    param_dict = {'ids':None,
                  'geo':None,
                  'election_dates':None,
                  'll':None}
    param_dict = q.retrieve_query_parameters(params, param_dict)

    #Initialize param_list inside of param_dict.  This is done here and not inside of the
    #param_dict intialization so that url parameters cant be passed in as ?param_list=.
    param_dict['param_list'] =[]

    #These calls build the query and param_list.
    q_dict, param_dict = q.ids_query(q_dict, param_dict)
    q_dict, param_dict = q.election_dates_query(q_dict, param_dict)
    q_dict, param_dict = q.ll_query(q_dict, param_dict)

    #Run the query that was just built.
    data = q.main_query(q_dict, param_dict)

    #Data returned as a list of tuples with each tuple being data for one election.
    return data

#Handles /elections/election_id> endpoint.
def id_endpoint(election_id):
    #Prebuilt query by id.
    q_dict = {'select':' SELECT e.election_id, e.election_date, e.info ',
              'from':' FROM elections E ',
              'where':' WHERE e.election_id = %s ',
              'order_by':' ORDER BY e.election_id '}
    
    #Add the election_id to param_list.
    param_dict = {'param_list':[election_id]}

    #Run the main query.
    data = q.main_query(q_dict, param_dict)

    #Data returned as a list containing one tuple of election data.
    return data
