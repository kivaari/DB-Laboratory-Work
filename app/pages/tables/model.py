import streamlit as st
from random import choice
from pypika import PostgreSQLQuery, Table

from app.components import (append_elements, blank, bool_compare_box,
                            bool_update_box, default_or_value, groupby_box,
                            limitby_box, non_empty_button, non_empty_dataframe,
                            number_compare_box, number_update_box, orderby_box,
                            populate_elements, text_compare_box, text_update_box,
                            uuid_select_box)
from app.queries import (QUERY_TYPE, query_model_ids, query_model)


def model_insert(db, query, table, fields, populate, append):
    options = st.multiselect(
        label='Поля',
        options=fields,
        default=None
    )

    query = query.into(table)
    model_ids = query_model_ids(db)
    model_default = (choice(model_ids))
    selected = choice([model_default])

    model_id = default_or_value(
        'model_id' in options,
        selected,
        uuid_select_box,
        {
            'label': 'ID модели',
            'selected': model_ids,
            'options_': model_ids,
        }
    )

    brand = default_or_value(
        'brand' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Название бренда',
            'max_chars': 64
        }
    )

    model_name = default_or_value(
        'model_name' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Название модели',
            'max_chars': 64
        }
    )

    yearofmanufacture = default_or_value(
        'yearofmanufacture' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Год выпуска',
            'value': 1980,
            'max_value': 2023,
            'min_value': 1980,
            'step': 1
        }
    )

    safetyrating = default_or_value(
        'safetyrating' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Рейтинг безопасности',
            'value': 0,
            'min_value': 0,
            'max_value': 5,
            'step': 1
        }
    )

    garantee = default_or_value(
        'garantee' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Гарантия',
            'max_chars': 64
        }
    )

    engine = default_or_value(
        'engine' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Количество цилиндров',
            'value': 4,
            'min_value': 0,
            'max_value': 16,
            'step': 1
        }
    )

    power = default_or_value(
        'power' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Мощность(в лс.)',
            'value': 100,
            'min_value': 20,
            'max_value': 1000,
            'step': 1
        }
    )

    fuel = default_or_value(
        'fuel' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Расход топлива',
            'value': 0,
            'min_value': 0,
            'max_value': 100,
            'step': 1
        }
    )

    gearbox = default_or_value(
        'gearbox' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Тип коробки передач',
            'max_chars': 64
        }
    )

    seats = default_or_value(
        'seats' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Количество мест',
            'value': 1,
            'min_value': 1,
            'max_value': 8,
            'step': 1
        }
    )

    trunck = default_or_value(
        'trunck' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Объем багажника(в л.)',
            'value': 0,
            'min_value': 0,
            'max_value': 1000,
            'step': 1
        }
    )

    fueltype = default_or_value(
        'fueltype' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Тип топлива',
            'max_chars': 64
        }
    )

    avgowningprice = default_or_value(
        'avgowningprice' in options,
        'DEFAULT',
        st.number_input,
        {
            'label': 'Средняя цена владения',
            'value': 0,
            'min_value': 0,
            'max_value': 1000000,
            'step': 1
        }
    )

    comments = default_or_value(
        'comments' in options,
        'DEFAULT',
        st.text_input,
        {
            'label': 'Комментарий',
            'max_chars': 1000
        }
    )

    blank()

    non_empty_button(
        db,
        query.insert(
            model_id,
            brand,
            model_name,
            yearofmanufacture,
            safetyrating,
            garantee,
            engine,
            power,
            fuel,
            gearbox,
            seats,
            trunck,
            fueltype,
            avgowningprice,
            comments
        ),
        'Добавить'
    )


def model_select(db, query, table, fields, populate, append):
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


def model_update(db, query, table, fields, populate, append):  #  Решить проблему с UPDATE в функции tabel_model
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


def model_delete(db, query, table, fields, populate, append):
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
    'INSERT': model_insert,
    'SELECT': model_select,
    'UPDATE': model_update,
    'DELETE': model_delete,
}


def tables_model(db):
    table = Table('model')
    query = PostgreSQLQuery()

    fields = [
        'model_id',
        'brand',
        'model_name',
        'yearofmanufacture',
        'safetyrating',
        'garantee',
        'engine',
        'power',
        'fuel',
        'gearbox',
        'seats',
        'trunck',
        'fueltype',
        'avgowningprice',
        'comments',
    ]

    populate = {
        'model_id': (
            text_compare_box,
            {
                'label': 'Model ID',
                'compared': table.model_id,
                'options': query_model(db),
                'uid': True
            }
        ),
        'brand': (
            text_compare_box,
            {
                'label': 'Brand',
                'compared': table.brand
            }
        ),
        'model_name': (
            text_compare_box,
            {
                'label': 'Model name',
                'compared': table.model_name
            }
        ),
        'yearofmanufacture': (
            number_compare_box,
            {
                'label': 'Year of manufacture',
                'compared': table.yearofmanufacture
            }
        ),
        'safetyrating': (
            number_compare_box,
            {
                'label': 'Safety rating',
                'compared': table.safetyrating
            }
        ),
        'garantee': (
            text_compare_box,
            {
                'label': 'Garantee',
                'compared': table.garantee
            }
        ),
        'engine': (
            number_compare_box,
            {
                'label': 'Engine',
                'compared': table.engine
            }
        ),
        'power': (
            number_compare_box,
            {
                'label': 'Power',
                'compared': table.power
            }
        ),
        'fuel': (
            number_compare_box,
            {
                'label': 'Fuel',
                'compared': table.fuel
            }
        ),
        'gearbox': (
            text_compare_box,
            {
                'label': 'Gearbox',
                'compared': table.gearbox
            }
        ),
        'seats': (
            number_compare_box,
            {
                'label': 'Seats',
                'compared': table.seats
            }
        ),
        'trunck': (
            number_compare_box,
            {
                'label': 'Trunk',
                'compared': table.trunck
            }
        ),
        'fueltype': (
            text_compare_box,
            {
                'label': 'Fuel type',
                'compared': table.fueltype
            }
        ),
        'avgowningprice': (
            number_compare_box,
            {
                'label': 'Avg owning price',
                'compared': table.avgowningprice
            }
        ),
        'comments': (
            text_compare_box,
            {
                'label': 'Comments',
                'compared': table.comments
            }
        )
    }

    append = {
        'model_id': (
            table.model_id,
            st.selectbox,
            {
                'label': 'ID ',
                'options': query_model(db)
            }
        ),
        'brand': (
            table.brand,
            text_update_box,
            {
                'label': 'Brand '
            }
        ),
        'model_name': (
            table.model_name,
            text_update_box,
            {
                'label': 'Model name '
            }
        ),
        'yearofmanufacture': (
            table.yearofmanufacture,
            number_update_box,
            {
                'label': 'Year of manufacture '
            }
        ),
        'safetyrating': (
            table.safetyrating,
            number_update_box,
            {
                'label': 'Safety rating '
            }
        ),
        'garantee': (
            table.garantee,
            text_update_box,
            {
                'label': 'Garantee '
            }
        ),
        'engine': (
            table.engine,
            number_update_box,
            {
                'label': 'Engine '
            }
        ),
        'power': (
            table.power,
            number_update_box,
            {
                'label': 'Power '
            }
        ),
        'fuel': (
            table.fuel,
            number_update_box,
            {
                'label': 'Fuel '
            }
        ),
        'gearbox': (
            table.gearbox,
            text_update_box,
            {
                'label': 'Gearbox '
            }
        ),
        'seats': (
            table.seats,
            number_update_box,
            {
                'label': 'Seats '
            }
        ),
        'trunck': (
            table.trunck,
            number_update_box,
            {
                'label': 'Trunk '
            }
        ),
        'fueltype': (
            table.fueltype,
            text_update_box,
            {
                'label': 'Fuel type '
            }
        ),
        'avgowningprice': (
            table.avgowningprice,
            number_update_box,
            {
                'label': 'Avg owning price '
            }
        ),
        'comments': (
            table.comments,
            text_update_box,
            {
                'label': 'Comment '
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
