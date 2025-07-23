from src.services import data_processor, update
from src.queries import update_queries
from src.utils import states
from src.db import connection
import streamlit as st
import pandas as pd
import oracledb
import os


def login_page():
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
                        st.rerun()
                    return conn

def insert_page(con=None):
    state = data_processor.check_from_to_table(con)
    out_path = "src/resources/out"
    files = [f for f in os.listdir(out_path) if os.path.isfile(os.path.join(out_path, f))]

    if state != 3:
        st.warning("Existem logs anteriores.", icon="⚠️")
        bt1, bt2, bt3 = st.columns([4.28,4.28,1])
        if bt1.button("Visualizar logs", use_container_width=True):
            def viwew_logs(con=None):
                try:
                    con = connection.get_connection(st.session_state.user, st.session_state.pw, st.session_state.dsn)
                    cur = con.cursor()
                    cur.execute("SELECT CD_TISS TISS, CD_TUSS TUSS, DT_VIGENCIA VIGENCIA, VL_HONORARIO HONORARIO, VL_OPERACIONAL OPERACIONAL, VL_TOTAL TOTAL, NM_USUARIO USUARIO  FROM DBAHUMS.DE_PARA_HUMS")
                    logs = cur.fetchall()
                    if logs:
                        df_logs = pd.DataFrame(logs, columns=[col[0] for col in cur.description])
                        st.dataframe(df_logs)
                        return
                    else:
                        st.info("Nenhum log encontrado.")
                except oracledb.Error as e:
                    st.error(f"Erro ao buscar logs: {e}")
            viwew_logs(con)
            
        if bt2.button("Limpar logs", use_container_width=True):
            def cleaner(con=None):
                try:
                    cur = con.cursor()
                    cur.execute("DELETE FROM DBAHUMS.DE_PARA_HUMS")
                    con.commit()
                    msg = {
                        'type': "S",
                        'msg': "Logs de de-para limpos com sucesso!"
                    }
                except oracledb.Error as e:
                    msg = {
                        'type': "E",
                        'msg': f"Erro ao limpar logs de de-para: {e}"
                    }
                return msg
            cleaner(con)
            st.rerun()

        if bt3.button("Exportar logs", use_container_width=True, disabled=files == [], help="Não há logs disponíveis para exportação."):
            

            # Garante que a pasta existe
            if not os.path.exists(out_path):
                st.warning("Pasta de saída não encontrada.")
            else:
                st.subheader("📁 Arquivos disponíveis para download")

                

                if not files:
                    st.info("Nenhum arquivo encontrado.")
                else:
                    for file_name in files:
                        file_path = os.path.join(out_path, file_name)

                        with open(file_path, "rb") as f:
                            file_bytes = f.read()

                        # Define tipo MIME automático (ou define fixo se preferir)
                        ext = file_name.split(".")[-1].lower()
                        mime_types = {
                            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "csv": "text/csv",
                            "txt": "text/plain",
                            "json": "application/json",
                            "zip": "application/zip"
                        }
                        mime = mime_types.get(ext, "application/octet-stream")

                        st.download_button(
                            label=f"📥 Baixar: {file_name}",
                            data=file_bytes,
                            file_name=file_name,
                            mime=mime
                        )
    else:
        uploaded_file = st.file_uploader("Envie o documento de atualização:", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            st.write("---")
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        
            def process_data(df, con, state, uploaded_file):       
                if "med" in uploaded_file.name.lower():
                    data_processor.medicationsProcedures(df, con)

                elif "mat" in uploaded_file.name.lower():
                    data_processor.materialsProcedures(df, con)

                else:
                    st.write("Tipo de planilha não identificado. Por favor, verifique o nome do arquivo.")

                

            st.button("Processar", on_click=process_data, args=(df, con, state, uploaded_file))    

def update_page(con=None):
    if st.button("Atualizar pagina"):
        st.rerun()

    state = data_processor.check_from_to_table(con)
    
    exists_update = update.exists_update_with_current_vigency(con)
    # st.write(exists_update)
    if exists_update == []:
        
        st.success("Não existem atualizações com vigência atual.", icon="✅")
        st.selectbox("Selecione o tipo de atualização:", ["Tabela 01 (Brasindice)", "Tabela 50 (Simpro)"], index=None, key="selected_option",)
        if st.button("Confirmar"):
            selected_option = st.session_state.selected_option
            if selected_option == "Tabela 01 (Brasindice)":
                typeSpreadsheet = 0
            elif selected_option == "Tabela 50 (Simpro)":
                typeSpreadsheet = 1
            else:
                st.error("Seleção inválida.")

            if typeSpreadsheet == 0 and state == 1:
                st.write("Atualizando tabela de procedimentos (Brasindice)...")
                exect = update.execute_update(con, typeSpreadsheet)
                st.write(exect)
            elif typeSpreadsheet == 1 and state == 2:
                st.write("Atualizando tabela de materiais (Simpro)...")
                exect = update.execute_update(con, typeSpreadsheet)
                st.write(exect)
            else:
                st.error("Dados de de-para não condinzentes com o tipo de atualização selecionado.")
        # st.rerun()
            
    else:
        st.warning("Existem atualizações.", icon="⚠️")
        st.write("Deseja limpar as atualizações com vigência atual?")
        if st.button("Sim"):
            try:
                cur = con.cursor()
                cur.execute(update_queries.clean_updateSQL)
                con.commit()
                st.success("Atualizações limpas com sucesso!")
            except Exception as e:
                st.error(f"Erro ao limpar atualizações: {e}")
            
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

    escolha = st.sidebar.selectbox("Processos:", ["Inserir", "Atualizar"], index=None)

    if escolha == "Inserir":
        title("Inserir Dados")
        con = connection.get_connection(st.session_state.user, st.session_state.pw, st.session_state.dsn)
        insert_page(con)
    elif escolha == "Atualizar":
        title("Atualizar Dados")
        con = connection.get_connection(st.session_state.user, st.session_state.pw, st.session_state.dsn)
        update_page(con)
    else:
        home_page()

    st.sidebar.write("---")
    # st.select_box("Selecione uma página:", ["Home", "Inserir Dados", "Atualizar Dados"], index=None, key="selected_page")
    st.sidebar.write("Configurações:")


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