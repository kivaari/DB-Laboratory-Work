import streamlit as st

from app.components import display_query, display_query_formated, display_sql

QUERY_CLIENT_COUNT = '''
SELECT COUNT(*) AS client_count
FROM client;
'''

def request_client_count(db):
    query = QUERY_CLIENT_COUNT
    display_sql(query)
    display_query(db, query)


REQUESTS = {
    'Сколько клиентов на данный момент?':
        request_client_count,
}


def page_requests():
    option = st.selectbox(
        label='''Запрос''',
        options=REQUESTS.keys()
    )

    REQUESTS.get(option)(st.session_state.db)
