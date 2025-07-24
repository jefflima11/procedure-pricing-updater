from streamlit_option_menu import option_menu
from src.pages import insert_page, home_page, update_page, viewer_page
import streamlit as st

def menu(con):
    with st.sidebar:
        selected = option_menu(
            menu_title=f" {st.session_state.user.upper()}",
            options=["Home", "Inserir", "Atualizar", "Visualizar", "Sair"],
            icons=["house", "plus", "pencil", "eye", "power"],
            # default_index=1,
            key="main_menu",
            orientation="vertical",
            menu_icon="pencil"
        )

    if selected == "Home":
        home_page.home()
    elif selected == "Inserir":
        insert_page.insert(con)
    elif selected == "Atualizar":
        update_page.updater(con)
    elif selected == "Visualizar":
        viewer_page.viewer(con)
    elif selected == "Sair":
        st.session_state.clear()
        st.rerun()