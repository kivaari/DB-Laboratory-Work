import streamlit as st

from .database import database
from .pages import PAGES
from .components import blank


def init():
    st.set_page_config(
        page_title='9 laba',
        page_icon='💀'
    )

    global_values = {
        'db': database(),
        'sql': True
    }

    for key, value in global_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def run():
    with st.sidebar:
        st.header('''Здесь полегло немало хороших ребят...''')

        app_page = st.selectbox(
            label='Страница',
            label_visibility='collapsed',
            options=PAGES.keys()
        )

        st.session_state.sql = st.checkbox(
            label='Отображать SQL',
            value=True
        )

        blank()

        st.write('Kivaari also known as Egor Belousov')

    PAGES.get(app_page)()
