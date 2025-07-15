import streamlit as st
from src.db.connection import get_connection

def login_page():
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
                    st.session_state.user = user
                    st.session_state.pw = pw
                    st.session_state.dsn = dsn
                    st.success("Login realizado com sucesso!")
                    st.rerun()

    else:
        st.success(f"Bem-vindo, {st.session_state.user}!")

def menu_page():
    st.title("Menu Principal")

    escolha = st.selectbox("Selecione a função:", ["Inserir", "Atualizar", "Sair"])

    if escolha == "Inserir":
        st.write("Chamaria função de Inserção aqui.")
        # executeInsert()
    elif escolha == "Atualizar":
        st.write("Chamaria função de Atualização aqui.")
    elif escolha == "Sair":
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    st.set_page_config(page_title="Sistema de Atualização", layout="wide")

    if "user" not in st.session_state:
        login_page()
    else:
        menu_page()

if __name__ == "__main__":
    main()
