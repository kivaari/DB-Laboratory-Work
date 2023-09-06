from random import choice

import streamlit as st
from pypika import PostgreSQLQuery, Table

from app.components import (append_elements, blank, bool_compare_box,
                            bool_update_box, date_time_box,
                            date_time_compare_box, default_or_value,
                            groupby_box, limitby_box, non_empty_button,
                            non_empty_dataframe, number_compare_box,
                            number_update_box, orderby_box, populate_elements,
                            text_compare_box, text_update_box, uuid_select_box)
from app.queries import (QUERY_TYPE, query_serv_ids, query_serv)
from app.utils import get_nanoid, time_now


def service_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    serv_ids = query_serv_ids(db)
    serv_default = (choice(serv_ids))
    selected = choice([serv_default])

    service_id = default_or_value(
        'service_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID сервиса',
            'options': serv_ids,
            'options_': serv_ids,
        }
    )

    serv_name = default_or_value(
        'serv_name' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Название сервиса',
            'max_chars': 64
        }
    )

    service_price = default_or_value(
        'service_price' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Цена сервиса',
            'max_value': 100000,
            'min_value': 0,
            'value': 100,
            'step': 1
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            service_id,
            serv_name,
            service_price
        ),
        'Добавить'
    )


def service_select(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.from_(table).select(
        *options if len(options) > 0 else '*'
    )

    if st.checkbox('Уникальные'):
        query = query.distinct()

    blank()

    if st.checkbox('Критерии'):
        conditions = st.multiselect(
            label='Критерии',
            options=fields,
            default=None,
            label_visibility='collapsed'
        )

        query = populate_elements(query, conditions, populate)

    blank()

    if st.checkbox('Группировка'):
        query = groupby_box(query, fields)

    blank()

    if st.checkbox('Порядок'):
        query = orderby_box(query, fields)

    blank()

    if st.checkbox('Ограничить'):
        query = limitby_box(query)

    blank()

    non_empty_dataframe(db, query)


def service_update(db, query, table, fields, populate, append):
    conditions = st.multiselect(
        label='Критерии',
        options=fields,
        default=None
    )

    query = query.update(table)

    query = populate_elements(query, conditions, populate)

    blank()

    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    values = append_elements(options, append)

    blank()

    for value in values:
        query = query.set(*value)

    non_empty_button(db, query, 'Обновить')


def service_delete(db, query, table, fields, populate, append):
    conditions = st.multiselect(
        label='Критерии',
        options=fields,
        default=None
    )

    query = query.from_(table).delete()

    query = populate_elements(query, conditions, populate)

    blank()

    non_empty_button(db, query, 'Удалить')


QUERIES = {
    'INSERT': service_insert,
    'SELECT': service_select,
    'UPDATE': service_update,
    'DELETE': service_delete,
}


def tables_service(db):
    table = Table('serv')
    query = PostgreSQLQuery()

    fields = [
        'service_id',
        'serv_name',
        'service_price'
    ]

    populate = {
        'service_id': (
            text_compare_box,
            {
                'label': 'ID сервиса',
                'compared': table.service_id,
                'options': query_serv(db),
                'uid': True
            }
        ),
        'serv_name': (
            text_compare_box,
            {
                'label': 'Название сервиса',
                'compared': table.serv_name
            }
        ),
        'service_price': (
            number_compare_box,
            {
                'label': 'Цена сервиса',
                'compared': table.service_price
            }
        )
    }

    append = {
        'service_id': (
            table.service_id,
            st.selectbox,
            {
                'label': 'ID сервиса ',
                'options': query_serv(db)
            }
        ),
        'serv_name': (
            table.serv_name,
            text_update_box,
            {
                'label': 'Название сервиса '
            }
        ),
        'service_price': (
            table.service_price,
            number_update_box,
            {
                'label': 'Цена сервиса '
            }
        )
    }

    query_type = st.radio(
        label='Тип',
        label_visibility='collapsed',
        options=QUERY_TYPE,
        horizontal=True
    )

    blank()

    QUERIES.get(query_type)(db, query, table, fields, populate, append)
