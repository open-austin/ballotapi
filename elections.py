import queries as q

def endpoint(params, **kwargs):
    q_dict = {'select':(' SELECT DISTINCT e.election_id, e.election_date,'
                        ' e.info '),
              'from':' FROM elections E ',
              'where':' WHERE TRUE ',
              'order_by':' ORDER BY e.election_id '}

    param_dict = {'ids':None,
                  'geo':None,
                  'election_dates':None,
                  'll':None}
    param_dict = q.retrieve_query_parameters(params, param_dict)
    if kwargs.get('direct_id'):
        param_dict['ids'] = kwargs['direct_id']

    param_list =[]

    ids_where_clause = ' AND e.election_id IN %s '
    q_dict, param_list = q.ids_query(q_dict, param_dict, param_list,
                                     ids_where_clause)

    election_dates_from_clause = '' #Not needed for /elections
    election_dates_where_clause = '' #Because it doesn't need to join elections table.
    q_dict, param_list = q.election_dates_query(q_dict, param_dict, param_list,
                                    election_dates_from_clause, 
                                    election_dates_where_clause)

    ll_where_clause = ' AND p.election_id = e.election_id ' 
    ll_from_clause = ' ,precincts P '
    q_dict, param_list = q.ll_query(q_dict, param_dict, param_list,
                                    ll_where_clause, ll_from_clause)

    data = q.main_query(q_dict, param_list)

    return data
