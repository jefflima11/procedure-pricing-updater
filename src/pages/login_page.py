from src.db import connection
from src.utils import pre_config
import streamlit as st
import json

def login():

    with open("src/json/string_connection.json", "r") as f:
        data = json.load(f)
    
    st.set_page_config(page_title="Login", layout="centered")
    st.title("Login")

    
    if "user" not in st.session_state:
        with st.form("login_form"):
            user = st.text_input("Usuário")
            pw = st.text_input("Senha", type="password")
            dsn = st.selectbox("Banco", data)
            submitted = st.form_submit_button("Logar")

            if submitted:
                strings = data[dsn][0]["string"]
                
                if not user or not pw or not dsn:
                    st.error("Preencha todos os campos!")
                else:
                    conn = connection.get_connection(user, pw, strings)
                    if conn:
                        st.session_state.user = user
                        st.session_state.pw = pw
                        st.session_state.dsn = strings
                        st.session_state.con = conn

                        erro = pre_config.start(st.session_state.con)
                        if erro:
                            st.inf(erro)
                            
                        st.rerun()
                    return conn