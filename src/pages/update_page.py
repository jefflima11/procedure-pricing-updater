from src.services import data_processor, update
import streamlit as st


def updater(con):
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