import streamlit as st

from app.components import display_sql

QUERY_MODELS_IN_STOCK = '''
SELECT DISTINCT Model.model_name
FROM Model
INNER JOIN Car ON Model.model_id = Car.model_id
WHERE Car.stat <> 0;
'''

def view_player_counts(db):
    query = QUERY_MODELS_IN_STOCK
    display_sql(query)

    st.dataframe(
        data=db.run_query(query),
        use_container_width=True
    )


VIEWS = {
    'Cписок моделей которые в данный момент есть в наличии': view_player_counts,
}


def page_views():
    option = st.selectbox(
        label='Представление',
        options=VIEWS.keys()
    )

    VIEWS.get(option)(st.session_state.db)
