import oracledb
import streamlit as st
import os
import dotenv 

dotenv.load_dotenv()

oracledb.init_oracle_client(lib_dir=os.getenv(""))

def get_connection(user, pw, dsn):
    try:
        conn = oracledb.connect(user=user, password=pw, dsn=dsn)
        return conn
    except oracledb.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None