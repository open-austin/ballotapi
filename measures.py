import queries as q

def endpoint(params, **kwargs):
    q_dict = {'select':(' SELECT DISTINCT ON (me.measure_id) me.measure_id, me.election_id, '
                        ' me.info, me.title, '
                        ' me.question, me.measure_type, me.voting_system, me.choices '),
              'from':' FROM measures ME ',
              'where':' WHERE TRUE ',
              'order_by':' ORDER BY me.measure_id '}

    param_dict = {'ids':None,
                  'elections':None,
                  'precincts':None,
                  'geo':None,
                  'election_dates':None,
                  'll':None}
    param_dict = q.retrieve_query_parameters(params, param_dict)
    if kwargs.get('direct_id'):
        param_dict['ids'] = kwargs['direct_id']

    param_list =[]

    ids_where_clause = ' AND me.measure_id IN %s '
    q_dict, param_list = q.ids_query(q_dict, param_dict, param_list,
                                     ids_where_clause)
    
    elections_where_clause = ' AND me.election_id IN %s '
    q_dict, param_list = q.elections_query(q_dict, param_dict, param_list,
                               elections_where_clause)

    election_dates_from_clause = ' , elections E '
    election_dates_where_clause = ' AND e.election_id = me.election_id '
    q_dict, param_list = q.election_dates_query(q_dict, param_dict, param_list,
                                    election_dates_from_clause, 
                                    election_dates_where_clause)

    ll_where_clause = ' AND me.election_id = p.election_id'
    ll_from_clause = ' ,precincts P '
    q_dict, param_list = q.ll_query(q_dict, param_dict, param_list,
                                    ll_where_clause, ll_from_clause)

    q_dict, param_list = q.precincts_query(q_dict, param_dict, param_list)

    data = q.main_query(q_dict, param_list)
    
    list_sql = (' SELECT MA.precinct_id '
                ' FROM mappings MA '
                ' WHERE MA.measure_id = %s '
                ' ORDER BY MA.precinct_id ')
    data = q.list_query(data, list_sql)

    return data
