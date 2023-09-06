from random import choice

import streamlit as st
from pypika import PostgreSQLQuery, Table

from app.components import (append_elements, blank, bool_compare_box,
                            bool_update_box, date_time_box,
                            date_time_compare_box, date_time_update_box,
                            default_or_value, groupby_box, limitby_box,
                            non_empty_button, non_empty_dataframe,
                            number_compare_box, number_select_update_box,
                            number_update_box, orderby_box, populate_elements,
                            text_compare_box, uuid_select_box, text_update_box)
from app.queries import (QUERY_TYPE, query_client_ids, query_client)


def client_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    client_ids = query_client_ids(db)

    client_default = (choice(client_ids))
    selected = choice([client_default])

    client_id = default_or_value(
        'client_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID клиента',
            'options': client_ids,
            'options_': client_ids,
        }
    )

    first_name = default_or_value(
        'first_name' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Имя',
            'max_chars': 64
        }
    )

    last_name = default_or_value(
        'last_name' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Фамилия',
            'max_chars': 64
        }
    )

    email = default_or_value(
        'email' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Почта',
            'max_chars': 64
        }
    )

    phone = default_or_value(
        'phone' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Телефон',
            'max_chars': 64
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            client_id,
            first_name,
            last_name,
            email,
            phone
        ),
        'Добавить'
    )


def client_select(db, query, table, fields, populate, append):
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


def client_update(db, query, table, fields, populate, append):
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


def client_delete(db, query, table, fields, populate, append):
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
    'INSERT': client_insert,
    'SELECT': client_select,
    'UPDATE': client_update,
    'DELETE': client_delete,
}


def tables_client(db):
    table = Table('client')
    query = PostgreSQLQuery()

    fields = [
        'client_id',
        'first_name',
        'last_name',
        'email',
        'phone'
    ]

    populate = {
        'client_id': (
            text_compare_box,
            {
                'label': 'ID клиента',
                'compared': table.client_id,
                'options': query_client(db),
                'uid': True
            }
        ),
        'first_name': (
            text_compare_box,
            {
                'label': 'Имя',
                'compared': table.first_name
            }
        ),
        'last_name': (
            text_compare_box,
            {
                'label': 'Фамилия',
                'compared': table.last_name
            }
        ),
        'email': (
            text_compare_box,
            {
                'label': 'Почта',
                'compared': table.email
            }
        ),
        'phone': (
            text_compare_box,
            {
                'label': 'Телефон',
                'compared': table.phone
            }
        )
    }

    append = {
        'client_id': (
            table.client_id,
            st.selectbox,
            {
                'label': 'ID клиента ',
                'options': query_client(db)
            }
        ),
        'first_name': (
            table.first_name,
            text_update_box,
            {
                'label': 'Имя '
            }
        ),
        'last_name': (
            table.last_name,
            text_update_box,
            {
                'label': 'Фамилия '
            }
        ),
        'email': (
            table.email,
            text_update_box,
            {
                'label': 'Почта '
            }
        ),
        'phone': (
            table.phone,
            text_update_box,
            {
                'label': 'Телефон '
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
