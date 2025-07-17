import streamlit as st
import pandas as pd
import dotenv
import oracledb
import os
from src.services import data_processor

dotenv.load_dotenv()

oracledb.init_oracle_client(lib_dir=os.getenv(""))

def login_page():
    def get_connection(user, pw, dsn):
        try:
            conn = oracledb.connect(user=user, password=pw, dsn=dsn)
            return conn
        except oracledb.Error as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

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
                    # Aqui você pode validar no banco se quiser
                    conn = get_connection(user, pw, dsn)
                    if conn:
                        st.session_state.user = user
                        st.rerun()

def executeInsert():
    # uploaded_file = st.file_uploader("Envie um documento", type=["csv", "xlsx"])
    # if uploaded_file is not None:
    #     df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    #     st.write("Dados carregados:")
        # st.write(insertFromToMatSQL)
    st.write("Tratamento de dados de medicamentos iniciado...a", data_processor.executeInsert())


def menu_page():
    def title(text):
        st.title(text)

    def home_page():
        st.markdown(f"""
            # 🏥 HospUpdate
            ######

            Bem-vindo ao **HospUpdate**, seu sistema de atualização centralizada de informações hospitalares.

            Você está conectado como **`{st.session_state.user}`**.

            Este sistema permite:

            - 🔄 Atualizar tabelas de procedimentos, valores e vigências
            - 🧩 Integrar dados diretamente com o banco Oracle
            - 📁 Gerenciar atualizações com rastreabilidade por usuário

            Use o menu lateral para navegar pelas funcionalidades disponíveis.

            ---
        """)

    st.sidebar.title(f" {st.session_state.user}")
    st.sidebar.write("---")

    escolha = st.sidebar.selectbox("Selecione a função:", ["Inserir", "Atualizar", "",], index=2)

    if escolha == "Inserir":
        title("Inserir Dados")
        st.write("Chamaria função de Inserção aqui.")
        executeInsert()
    elif escolha == "Atualizar":
        title("Atualizar Dados")
        st.write("Chamaria função de Atualização aqui.")
    else:
        home_page()

    st.sidebar.write("---")
    
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()


def main():
    st.set_page_config(page_title="Sistema de Atualização", layout="wide")

    if "user" not in st.session_state:
        login_page()
    else:
        menu_page()

if __name__ == "__main__":
    main()