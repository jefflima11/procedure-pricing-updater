from src.services import update
from src.queries import update_queries
import src.models.fromToModel as ftm
import streamlit as st
import time


def updater(con):
    if update.exists_update_with_current_vigency(con) is not None:
        st.info("Existe uma atualização realizada hoje.")
    else:
        st.info("Não existe atualização realizada hoje.")

    st.title("Atualização de Tabelas")
    state = ftm.checkFromTo(con)

    with st.form("form_update"):
        select_table, bt_updated_pg, bt_confirm = st.columns([2,2,2], vertical_alignment="bottom")

        with select_table:
            st.selectbox("Selecione o tipo de atualização:", ["Tabela 01 (Brasindice)", "Tabela 50 (Simpro)"], index=None, key="selected_option")
            
        with bt_confirm:
            if st.form_submit_button("Confirmar"):
                selected_option = st.session_state.selected_option

                if selected_option == "Tabela 01 (Brasindice)":
                    typeSpreadsheet = 0
                elif selected_option == "Tabela 50 (Simpro)":
                    typeSpreadsheet = 1
                else:
                    st.error("Seleção inválida.")

                if typeSpreadsheet == 0 and state == 1:
                    # st.write("Atualizando tabela de procedimentos (Brasindice)...")
                    exect = update.execute_update(con, typeSpreadsheet)
                elif typeSpreadsheet == 1 and state == 2:
                    # st.write("Atualizando tabela de materiais (Simpro)...")
                    exect = update.execute_update(con, typeSpreadsheet)
                else:
                    exect = "Dados de de-para não condinzentes com o tipo de atualização selecionado."
                    
                return exect
