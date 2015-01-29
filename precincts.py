import queries as q

def endpoint(params, **kwargs):
    q_dict = {'select':(' SELECT DISTINCT ON (p.precinct_id) p.precinct_id, p.election_id, '
                        ' p.info, p.confirmed, ST_AsGeoJSON(p.geom) '),
              'from':' FROM precincts P ',
              'where':' WHERE TRUE ',
              'order_by':' ORDER BY p.precinct_id '}

    param_dict = {'ids':None,
                  'elections':None,
                  'measures':None,
                  'geo':None,
                  'election_dates':None,
                  'll':None}

    param_dict = q.retrieve_query_parameters(params, param_dict)
    if kwargs.get('direct_id'):
        param_dict['ids'] = kwargs['direct_id']

    param_list =[]

    ids_where_clause = ' AND p.precinct_id IN %s '
    q_dict, param_list = q.ids_query(q_dict, param_dict, param_list,
                                     ids_where_clause)
    
    elections_where_clause = ' AND p.election_id IN %s '
    q_dict, param_list = q.elections_query(q_dict, param_dict, param_list,
                               elections_where_clause)

    election_dates_from_clause = ' , elections E '
    election_dates_where_clause = ' AND e.election_id = p.election_id '
    q_dict, param_list = q.election_dates_query(q_dict, param_dict, param_list,
                                    election_dates_from_clause, 
                                    election_dates_where_clause)

    ll_where_clause = '' #Not needed for /precincts.
    ll_from_clause = '' #Because it doesn't need to join to precincts table.
    q_dict, param_list = q.ll_query(q_dict, param_dict, param_list,
                                    ll_where_clause, ll_from_clause)

    q_dict, param_list = q.measures_query(q_dict, param_dict, param_list)

    data = q.main_query(q_dict, param_list)

    list_sql = (' SELECT MA.measure_id '
                ' FROM mappings MA '
                ' WHERE MA.precinct_id = %s '
                ' ORDER BY MA.measure_id ')
    data = q.list_query(data, list_sql)

    return data
