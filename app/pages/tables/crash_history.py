from copy import deepcopy
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
from app.queries import (QUERY_TYPE, query_ch_ids, query_ch, query_car, query_car_ids_for_sh)
from app.utils import time_now


def crash_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    ch_ids = query_ch_ids(db)
    ch_default = (choice(ch_ids))
    selected = choice([ch_default])

    crash_id = default_or_value(
        'crash_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID аварии',
            'options': ch_ids,
            'options_': ch_ids,
        }
    )

    car_ids = query_car_ids_for_sh(db)

    car_id = default_or_value(
        'car_id' in options,
        'DEFAULT',
        st.selectbox,
        {
            'label': 'ID автомобиля',
            'options': car_ids
        }
    )

    crash_date = default_or_value(
        'crash_date' in options,
        'DEFAULT',
        st.date_input,
        {
            'label': 'Дата'
        }
    )

    ctype = default_or_value(
        'ctype' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Тип аварии',
            'max_chars': 300,
        }
    )

    owners = default_or_value(
        'owners' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Владелец',
            'max_chars': 300,
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            crash_id,
            car_id,
            crash_date,
            ctype,
            owners
        ),
        'Добавить'
    )


def crash_select(db, query, table, fields, populate, append):
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


def crash_update(db, query, table, fields, populate, append):
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


def crash_delete(db, query, table, fields, populate, append):
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
    'INSERT': crash_insert,
    'SELECT': crash_select,
    'UPDATE': crash_update,
    'DELETE': crash_delete,
}


def tables_crash(db):
    table = Table('crash_history')
    query = PostgreSQLQuery()

    fields = [
        'crash_id',
        'car_id',
        'crash_date',
        'ctype',
        'owners'
    ]

    populate = {
        'crash_id': (
            text_compare_box,
            {
                'label': 'ID аварии',
                'compared': table.crash_id,
                'options': query_ch(db),
                'uid': True
            }
        ),
        'car_id': (
            text_compare_box,
            {
                'label': 'ID автомобиля',
                'compared': table.car_id,
                'options': query_car(db),
                'uid': True
            }
        ),
        'crash_date': (
            date_time_compare_box,
            {
                'label': 'Дата',
                'compared': table.crash_date
            }
        ),
        'ctype': (
            text_compare_box,
            {
                'label': 'тип аварии',
                'compared': table.ctype
            }
        ),
        'owners': (
            text_compare_box,
            {
                'label': 'Владелец',
                'compared': table.owners
            }
        )
    }

    append = {
        'crash_id': (
            table.crash_id,
            st.selectbox,
            {
                'label': 'ID аварии ',
                'options': query_ch(db)
            }
        ),
        'car_id': (
            table.car_id,
            st.selectbox,
            {
                'label': 'ID автомобиля ',
                'options': query_car(db)
            }
        ),
        'crash_date': (
            table.crash_date,
            date_time_box,
            {
                'label': 'Дата '
            }
        ),
        'ctype': (
            table.ctype,
            text_update_box,
            {
                'label': 'Тип ремонта '
            }
        ),
        'owners': (
            table.ownerstype,
            text_update_box,
            {
                'label': 'Владелец '
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
