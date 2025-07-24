import streamlit as st
from streamlit_option_menu import option_menu
from src.pages import menu_page

def home():
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

    home_page()