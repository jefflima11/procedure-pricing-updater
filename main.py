from streamlit_option_menu import option_menu
from src.pages import login_page, home_page, menu_page
import streamlit as st


def main():
    st.set_page_config(page_title="Sistema de Atualização", layout="wide")

    if "user" not in st.session_state:
        login_page.login()
    else:
        
        menu_page.menu(st.session_state.con)

if __name__ == "__main__":
    main()