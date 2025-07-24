import streamlit as st
from src.db import connection

def login():
    st.set_page_config(page_title="Login", layout="centered")
    st.title("Login")

    
    if "user" not in st.session_state:
        with st.form("login_form"):
            user = st.text_input("Usuário")
            pw = st.text_input("Senha", type="password")
            dsn = st.text_input("String de conexão")
            submitted = st.form_submit_button("Logar")

            if submitted:
                if not user or not pw or not dsn:
                    st.error("Preencha todos os campos!")
                else:
                    conn = connection.get_connection(user, pw, dsn)
                    if conn:
                        st.session_state.user = user
                        st.session_state.pw = pw
                        st.session_state.dsn = dsn
                        st.session_state.con = conn
                        st.rerun()
                    return conn