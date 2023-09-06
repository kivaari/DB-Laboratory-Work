import streamlit as st
from random import choice
from pypika import PostgreSQLQuery, Table

from app.components import (append_elements, blank, default_or_value,
                            groupby_box, limitby_box, non_empty_button,
                            non_empty_dataframe, number_compare_box,
                            number_select_update_box, orderby_box,
                            populate_elements, text_compare_box, text_update_box, 
                            uuid_select_box, date_time_box, date_time_compare_box)
from app.queries import (QUERY_TYPE, query_deal_ids, query_deal, query_car, 
                         query_car_ids_for_sh, query_client, query_client_ids_for_d,
                         query_model, query_model_ids_for_d, query_extention,
                         query_ext_ids_for_d, query_serv, query_serv_ids_for_d)


def deal_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    deal_ids = query_deal_ids(db)
    deal_default = (choice(deal_ids))
    selected = choice([deal_default])

    deal_id = default_or_value(
        'deal_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID сделки',
            'options': deal_ids,
            'options_': deal_ids,
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

    client_ids = query_client_ids_for_d(db)

    client_id = default_or_value(
        'client_id' in options,
        'DEFAULT',
        st.selectbox,
        {
            'label': 'ID клиента',
            'options': client_ids
        }
    )

    service_ids = query_serv_ids_for_d(db)

    service_id = default_or_value(
        'service_id' in options,
        'null',
        st.selectbox,
        {
            'label': 'ID сервиса',
            'options': service_ids
        }
    )

    ext_ids = query_ext_ids_for_d(db)

    ext_id = default_or_value(
        'ext_id' in options,
        'null',
        st.selectbox,
        {
            'label': 'ID допа',
            'options': ext_ids
        }
    )

    model_ids = query_model_ids_for_d(db)

    model_id = default_or_value(
        'model_id' in options,
        'DEFAULT',
        st.selectbox,
        {
            'label': 'ID модели',
            'options': model_ids
        }
    )

    deal_date = default_or_value(
        'deal_date' in options,
        'DEFAULT',
        st.date_input,
        {
            'label': 'Дата'
        }
    )

    discount_amount = default_or_value(
        'discount_amount' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Объем скидки',
            'max_value': 35,
            'min_value': 0,
            'value': 0,
            'step': 1
        }
    )

    deal_price = default_or_value(
        'deal_price' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Цена',
            'max_value': 10000000,
            'min_value': 0,
            'value': 10000,
            'step': 1
        }
    )

    dtype = default_or_value(
        'dtype' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Тип оплаты',
            'max_chars': 30,
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            deal_id,
            car_id,
            client_id,
            service_id,
            ext_id,
            model_id,
            deal_date,
            discount_amount,
            deal_price,
            dtype
        ),
        'Добавить'
    )


def deal_select(db, query, table, fields, populate, append):
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


def deal_update(db, query, table, fields, populate, append):
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


def deal_delete(db, query, table, fields, populate, append):
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
    'INSERT': deal_insert,
    'SELECT': deal_select,
    'UPDATE': deal_update,
    'DELETE': deal_delete,
}


def tables_deal(db):
    table = Table('deal')
    query = PostgreSQLQuery()

    fields = [
        'deal_id',
        'car_id',
        'client_id',
        'service_id',
        'ext_id',
        'model_id',
        'deal_date',
        'discount_amount',
        'deal_price',
        'dtype'
    ]

    populate = {
        'deal_id': (
            text_compare_box,
            {
                'label': 'ID сделки',
                'compared': table.deal_id,
                'options': query_deal(db),
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
        'client_id': (
            text_compare_box,
            {
                'label': 'ID клиента',
                'compared': table.client_id,
                'options': query_client(db),
                'uid': True
            }
        ),
        'service_id': (
            text_compare_box,
            {
                'label': 'ID сервиса',
                'compared': table.service_id,
                'options': query_serv(db),
                'uid': True
            }
        ),
        'ext_id': (
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
        'deal_date': (
            date_time_compare_box,
            {
                'label': 'Дата',
                'compared': table.deal_date
            }
        ),
        'discount_amount': (
            number_compare_box,
            {
                'label': 'оБъем скидки',
                'compared': table.discount_amount,
            }
        ),
        'deal_price': (
            number_compare_box,
            {
                'label': 'Цена',
                'compared': table.deal_price,
            }
        ),
        'dtype': (
            text_compare_box,
            {
                'label': 'тип оплаты',
                'compared': table.dtype
            }
        )
    }

    append = {
        'deal_id': (
            table.deal_id,
            st.selectbox,
            {
                'label': 'ID сделки ',
                'options': query_deal(db)
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
        'client_id': (
            table.client_id,
            st.selectbox,
            {
                'label': 'ID клиента ',
                'options': query_client(db)
            }
        ),
        'service_id': (
            table.service_id,
            st.selectbox,
            {
                'label': 'ID сервиса ',
                'options': query_serv(db)
            }
        ),
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
        'deal_date': (
            table.deal_date,
            date_time_box,
            {
                'label': 'Дата '
            }
        ),
        'discount_amount': (
            table.discount_amount,
            st.selectbox,
            {
                'label': 'Объем скидки '
            }
        ),
        'deal_price': (
            table.deal_price,
            st.selectbox,
            {
                'label': 'Цена '
            }
        ),
        'dtype': (
            table.dtype,
            text_update_box,
            {
                'label': 'Тип оплаты '
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
