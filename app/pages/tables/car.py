from copy import deepcopy
from random import choice

import streamlit as st
from pypika import PostgreSQLQuery, Table

from app.components import (append_elements, blank, default_or_value,
                            groupby_box, limitby_box, non_empty_button,
                            non_empty_dataframe, number_compare_box,
                            number_update_box, orderby_box, populate_elements,
                            text_compare_box, text_compare_box, text_update_box,
                            uuid_select_box)
from app.queries import (QUERY_TYPE, query_model_name, 
                         query_car_ids, query_car, query_model, 
                         query_model_id_by_name, query_model_ids_for_d)


def car_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    model_ids = query_model_ids_for_d(db)
    query = query.into(table)
    car_ids = query_car_ids(db)

    car_default = (choice(car_ids))
    selected = choice([car_default])

    car_id = default_or_value(
        'car_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID автомобиля',
            'selected': car_ids,
            'options_': car_ids,
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

    price = default_or_value(
        'price' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Цена автомобиля',
            'value': 10000,
            'min_value': 5000,
            'step': 1
        }
    )

    mileage = default_or_value(
        'mileage' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Пробег',
            'value': 1,
            'min_value': 0,
            'step': 1
        }
    )

    color = default_or_value(
        'color' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Цвет',
            'max_chars': 64
        }
    )

    testdrive = default_or_value(
        'testdrive' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Тест-драйв',
            'value': 1,
            'max_value': 1,
            'min_value': 0,
            'step': 1
        }
    )

    vincode = default_or_value(
        'vincode' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Вин-номер',
            'max_chars': 64
        }
    )

    condition = default_or_value(
        'condition' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Состояние(0-б\у, 1-новый)',
            'value': 1,
            'max_value': 1,
            'min_value': 0,
            'step': 1
        }
    )

    stat = default_or_value(
        'stat' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Статус(0-продан, 1-в наличии)',
            'value': 1,
            'max_value': 1,
            'min_value': 0,
            'step': 1
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            car_id,
            model_id,
            price,
            mileage,
            color,
            testdrive,
            vincode,
            condition,
            stat,
        ),
        'Добавить'
    )


def car_select(db, query, table, fields, populate, append):
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


def car_update(db, query, table, fields, populate, append):
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


def car_delete(db, query, table, fields, populate, append):
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
    'INSERT': car_insert,
    'SELECT': car_select,
    'UPDATE': car_update,
    'DELETE': car_delete,
}


def tables_car(db):
    table = Table('car')
    query = PostgreSQLQuery()

    fields = [
        'car_id',
        'model_id',
        'price',
        'mileage',
        'color',
        'testdrive',
        'vincode',
        'condition',
        'stat'
    ]

    populate = {
        'car_id': (
            text_compare_box,
            {
                'label': 'ID автомобиля',
                'compared': table.car_id,
                'options': query_car(db),
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
        'price': (
            number_compare_box,
            {
                'label': 'Цена автомобиля',
                'compared': table.price,
            }
        ),
        'mileage': (
            number_compare_box,
            {
                'label': 'Пробег',
                'compared': table.mileage,
            }
        ),
        'color': (
            text_compare_box,
            {
                'label': 'Цвет',
                'compared': table.color,
            }
        ),
        'testdrive': (
            number_compare_box,
            {
                'label': 'Тест-драйв',
                'compared': table.testdrive,
            }
        ),
        'condition': (
            number_compare_box,
            {
                'label': 'Состояние',
                'compared': table.condition,
            }
        ),
        'stat': (
            number_compare_box,
            {
                'label': 'Статус',
                'compared': table.stat,
            }
        )
    }

    append = {
        'car_id': (
            table.car_id,
            st.selectbox,
            {
                'label': 'ID автомобиля ',
                'options': query_car(db)
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
        'price': (
            table.price,
            st.selectbox,
            {
                'label': 'Цена '
            }
        ),
        'mileage': (
            table.mileage,
            st.selectbox,
            {
                'label': 'Пробег '
            }
        ),
        'color': (
            table.color,
            st.selectbox,
            {
                'label': 'Цвет '
            }
        ),
        'testdrive': (
            table.testdrive,
            st.selectbox,
            {
                'label': 'Тест-драйв '
            }
        ),
        'condition': (
            table.condition,
            st.selectbox,
            {
                'label': 'Состояние '
            }
        ),
        'stat': (
            table.stat,
            st.selectbox,
            {
                'label': 'Статус '
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
