import operator

QUERY_TYPE = [
    'INSERT',
    'SELECT',
    'UPDATE',
    'DELETE'
]

QUERY_COMAPRE_OPERATORS = {
    '=': operator.eq,
    '<>': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}


def format_query(query):
    return query\
        .get_sql()\
        .replace('=', ' = ')\
        .replace('<', ' < ')\
        .replace('>', ' > ')\
        .replace('<  =', '<=')\
        .replace('>  =', '>=')\
        .replace('<  >', '<>')\
        .replace(',', ',\n    ')\
        .replace('(', '(\n    ')\
        .replace(')', '\n)')\
        .replace('"', '')\
        .replace('\'DEFAULT\'', 'DEFAULT')\
        .replace('null', 'NULL')\
        .replace(' FROM', '\nFROM')\
        .replace(' INTO', '\nINTO')\
        .replace(' WHERE', '\nWHERE')\
        .replace(' VALUES', '\nVALUES')\
        .replace(' SET', '\nSET')\
        .replace(' AND', '\n    AND')\
        .replace(' ORDER', '\nORDER')\
        .replace(' GROUP', '\nGROUP')\
        .replace(' LIMIT', '\nLIMIT')\
        .replace(' ASC,', ',')\
        .replace(' DESC,', ',')\
        + ';'


def query_model(db):
    query = 'SELECT * FROM model;'
    return [m['model_id'] for m in db.run_query(query)]


def query_client(db):
    query = 'SELECT * FROM client'
    return [c['client_id'] for c in db.run_query(query)]


def query_car(db):
    query = 'SELECT * FROM car'
    return [c['car_id'] for c in db.run_query(query)]

def query_ch(db):
    query = 'SELECT * FROM crash_history;'
    return [c['crash_id'] for c in db.run_query(query)]

def query_extention(db):
    query = 'SELECT * FROM extention;'
    return [e['ext_id'] for e in db.run_query(query)]


def query_serv(db):
    query = 'SELECT * FROM serv;'
    return [s['service_id'] for s in db.run_query(query)]


def query_sh(db):
    query = 'SELECT * FROM service_history;'
    return [s['service_history_id'] for s in db.run_query(query)]


def query_deal(db):
    query = 'SELECT * FROM deal;'
    return [d['deal_id'] for d in db.run_query(query)]


def query_model_name(db):
    query = 'SELECT model_name FROM model;'
    return [m['model_name'] for m in db.run_query(query)]


def query_car_ids(db):
    query = 'SELECT MAX(car_id) + 1 AS last_plus_one_id FROM car;'
    return [c['last_plus_one_id'] for c in db.run_query(query)]


def query_model_ids(db):
    query = 'SELECT MAX(model_id) + 1 AS last_plus_one_id FROM model;'
    return [m['last_plus_one_id'] for m in db.run_query(query)]


def query_client_ids(db):
    query = 'SELECT MAX(client_id) + 1 AS last_plus_one_id FROM client;'
    return [c['last_plus_one_id'] for c in db.run_query(query)]


def query_ext_ids(db):
    query = 'SELECT MAX(ext_id) + 1 AS last_plus_one_id FROM extention;'
    return [e['last_plus_one_id'] for e in db.run_query(query)]


def query_serv_ids(db):
    query = 'SELECT MAX(service_id) + 1 AS last_plus_one_id FROM serv;'
    return [s['last_plus_one_id'] for s in db.run_query(query)]


def query_sh_ids(db):
    query = 'SELECT MAX(service_history_id) + 1 AS last_plus_one_id FROM service_history;'
    return [s['last_plus_one_id'] for s in db.run_query(query)]


def query_ch_ids(db):
    query = 'SELECT MAX(crash_id) + 1 AS last_plus_one_id FROM crash_history;'
    return [ch['last_plus_one_id'] for ch in db.run_query(query)]


def query_deal_ids(db):
    query = 'SELECT MAX(deal_id) + 1 AS last_plus_one_id FROM deal;'
    return [d['last_plus_one_id'] for d in db.run_query(query)]


def query_model_ids_for_car(db):
    query = 'SELECT model_id FROM model ORDER BY model_id DESC;'
    return [m['model_id'] for m in db.run_query(query)]


def query_car_ids_for_sh(db):
    query = 'SELECT car_id FROM car ORDER BY car_id DESC;'
    return [c['car_id'] for c in db.run_query(query)]


def query_model_ids_for_d(db):
    query = 'SELECT model_id FROM model ORDER BY model_id DESC;'
    return [m['model_id'] for m in db.run_query(query)]


def query_client_ids_for_d(db):
    query = 'SELECT client_id FROM client ORDER BY client_id DESC;'
    return [c['client_id'] for c in db.run_query(query)]


def query_ext_ids_for_d(db):
    query = 'SELECT ext_id FROM extention ORDER BY ext_id DESC;'
    return [c['ext_id'] for c in db.run_query(query)]


def query_serv_ids_for_d(db):
    query = 'SELECT service_id FROM serv ORDER BY service_id DESC;'
    return [c['service_id'] for c in db.run_query(query)]


def query_model_id_by_name(db):
    query = 'SELECT model_id FROM model WHERE model_name = {model_name};'
