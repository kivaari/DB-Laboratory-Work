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
                            text_compare_box, uuid_select_box, text_update_box)
from app.queries import (QUERY_TYPE, query_sh_ids, query_sh, query_car_ids_for_sh, query_car)


def sh_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    sh_ids = query_sh_ids(db)
    sh_default = (choice(sh_ids))
    selected = choice([sh_default])

    service_history_id = default_or_value(
        'service_history_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID истории сервиса',
            'options': sh_ids,
            'options_': sh_ids,
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

    service_date = default_or_value(
        'service_date' in options,
        'DEFAULT',
        st.date_input,
        {
            'label': 'Дата'
        }
    )

    stype = default_or_value(
        'stype' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Тип ремонта',
            'max_chars': 300,
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            service_history_id,
            car_id,
            service_date,
            stype
        ),
        'Добавить'
    )


def sh_select(db, query, table, fields, populate, append):
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


def sh_update(db, query, table, fields, populate, append):
    if not warning():
        blank()
    else:
        return

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


def sh_delete(db, query, table, fields, populate, append):
    if not warning():
        blank()
    else:
        return

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
    'INSERT': sh_insert,
    'SELECT': sh_select,
    'UPDATE': sh_update,
    'DELETE': sh_delete,
}


def tables_sh(db):
    table = Table('service_history')
    query = PostgreSQLQuery()

    fields = [
        'service_history_id',
        'car_id',
        'service_date',
        'stype'
    ]

    populate = {
        'service_history_id': (
            text_compare_box,
            {
                'label': 'ID истории сервиса',
                'compared': table.service_history_id,
                'options': query_sh(db),
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
        'service_date': (
            date_time_compare_box,
            {
                'label': 'Дата',
                'compared': table.service_date
            }
        ),
        'stype': (
            text_compare_box,
            {
                'label': 'Тип ремонта',
                'compared': table.stype
            }
        )
    }

    append = {
        'service_history_id': (
            table.service_history_id,
            st.selectbox,
            {
                'label': 'ID истории сервиса ',
                'options': query_sh(db)
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
        'service_date': (
            table.service_date,
            date_time_box,
            {
                'label': 'Дата '
            }
        ),
        'stype': (
            table.stype,
            text_update_box,
            {
                'label': 'Тип ремонта '
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
