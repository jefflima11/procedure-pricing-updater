from src.services import data_processor, update
import streamlit as st


def updater(con):

    state = data_processor.check_from_to_table(con)
    
    exists_update = update.exists_update_with_current_vigency(con)

    if exists_update == []:
        
        if st.button("Atualizar pagina"):
                    st.rerun()

        st.success("Não existem atualizações com vigência atual.")
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
                        st.write("Atualizando tabela de procedimentos (Brasindice)...")
                        exect = update.execute_update(con, typeSpreadsheet)
                        st.write(exect)
                    elif typeSpreadsheet == 1 and state == 2:
                        st.write("Atualizando tabela de materiais (Simpro)...")
                        exect = update.execute_update(con, typeSpreadsheet)
                        st.write(exect)
                    else:
                        st.error("Dados de de-para não condinzentes com o tipo de atualização selecionado.")
           
    
            
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