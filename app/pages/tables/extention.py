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
from app.queries import (QUERY_TYPE, query_ext_ids, query_extention, query_model_ids_for_car, query_model)


def ext_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    ext_ids = query_ext_ids(db)
    model_ids = query_model_ids_for_car(db)
    ext_default = (choice(ext_ids))
    selected = choice([ext_default])

    ext_id = default_or_value(
        'ext_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID допа',
            'options': ext_ids,
            'options_': ext_ids,
        }
    )

    model_id = default_or_value(
        'model_id' in options,
        'DEFAULT',
        st.selectbox,
        {
            'label': 'ID модели',
            'options': model_ids
        }
    )

    ext_name = default_or_value(
        'ext_name' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Название допа',
            'max_chars': 64
        }
    )

    ext_price = default_or_value(
        'ext_price' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Цена допа',
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
            ext_id,
            model_id,
            ext_name,
            ext_price
        ),
        'Добавить'
    )


def ext_select(db, query, table, fields, populate, append):
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


def ext_update(db, query, table, fields, populate, append):
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


def ext_delete(db, query, table, fields, populate, append):
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
    'INSERT': ext_insert,
    'SELECT': ext_select,
    'UPDATE': ext_update,
    'DELETE': ext_delete,
}


def tables_ext(db):
    table = Table('extention')
    query = PostgreSQLQuery()

    fields = [
        'ext_id',
        'model_id',
        'ext_name',
        'ext_price'
    ]

    populate = {
        'client_id': (
            text_compare_box,
            {
                'label': 'ID допа',
                'compared': table.ext_id,
                'options': query_extention(db),
                'uid': True
            }
        ),
        'model_id': (
            text_compare_box,
            {
                'label': 'ID модели',
                'compared': table.model_id,
                'options': query_model(db),
                'uid': True
            }
        ),
        'ext_name': (
            text_compare_box,
            {
                'label': 'Название допа',
                'compared': table.ext_name
            }
        ),
        'ext_price': (
            number_compare_box,
            {
                'label': 'Цена допа',
                'compared': table.ext_price
            }
        )
    }

    append = {
        'ext_id': (
            table.ext_id,
            st.selectbox,
            {
                'label': 'ID допа ',
                'options': query_extention(db)
            }
        ),
        'model_id': (
            table.model_id,
            st.selectbox,
            {
                'label': 'ID модели ',
                'options': query_model(db)
            }
        ),
        'ext_name': (
            table.ext_name,
            text_update_box,
            {
                'label': 'Название допа '
            }
        ),
        'ext_price': (
            table.ext_price,
            number_update_box,
            {
                'label': 'Цена допа '
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
