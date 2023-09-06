import streamlit as st

from .model import tables_model
from .car import tables_car
from .client import tables_client
from .extention import tables_ext
from .serv import tables_service
from .service_history import tables_sh
from .crash_history import tables_crash
from .deal import tables_deal

TABLES = {
    'Model': tables_model,
    'Extention': tables_ext,
    'Client': tables_client,
    'Car': tables_car,
    'Service': tables_service,
    'Service history': tables_sh,
    'Crash history': tables_crash,
    'Deal': tables_deal
}


def page_tables():
    option = st.selectbox(
        label='Таблица',
        options=TABLES.keys()
    )

    TABLES.get(option)(st.session_state.db)
