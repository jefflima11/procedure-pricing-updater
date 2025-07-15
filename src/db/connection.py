import oracledb
import streamlit as st
import os

oracledb.init_oracle_client(lib_dir=os.getenv("LIB_DIR"))

def get_connection():
    user = st.session_state.get("user")
    pw = st.session_state.get("pw")
    dsn = st.session_state.get("dsn")

    if not user or not pw or not dsn:
        st.error("Credenciais não encontradas na sessão!")
        return None

    try:
        conn = oracledb.connect(user=user, password=pw, dsn=dsn)
        return conn
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"\nErro de conexao: {error.message}")
        return None