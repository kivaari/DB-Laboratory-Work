from copy import deepcopy

import streamlit as st

from app.components import display_sql
from app.queries import query_model

def procedure_update_price(db, model_id, percentage):
    models = query_model(db)

    if len(models) < 1:
        st.write('Не хватает моделей')
        return

    query = f'CALL increase_model_prices({model_id}, {percentage});'
    display_sql(query)

    def call():
        db.call_proc(query)

    st.button(
        label='Выполнить процедуру',
        on_click=call
    )


PROCEDURES = {
    'Обновить цену на все машины определенной модели': procedure_update_price,
}

def query_model(db):
    query = '''
        SELECT DISTINCT Model.model_id, Model.model_name
        FROM Model
        INNER JOIN Car ON Model.model_id = Car.model_id
        WHERE Car.stat <> 0;
    '''
    model_list = db.run_query(query)
    return model_list

def page_procedures():
    option = st.selectbox(
        label='Процедура',
        options=PROCEDURES.keys()
    )
    models = query_model(st.session_state.db)
    model_ids = [model['model_id'] for model in models]
    model_id = st.selectbox(
        label='Выберите модель',
        options=model_ids
    )
    percentage = st.number_input(
        label='Введите процент',
        min_value=0.0,
        step=0.5
    )

    PROCEDURES.get(option)(st.session_state.db, model_id, percentage)


