from src.queries import viewer_queries
import streamlit as st
import pandas as pd
import oracledb
import numpy as np

def viewer(con):
    # st.subheader("Ultimas atualizações")
    st.markdown("""
        ## Ultimas atualizações
        ---

    """)
    with st.form("form_date", border=False, width=800):
        from_date, to_date, tables, submitted_col = st.columns([3,3,6,2])
        with from_date:
            new_from_date = st.date_input("De:" ,width=150, format="DD/MM/YYYY", max_value="today", value=None, key="initial_date")
        with to_date: 
            new_to_date = st.date_input("Até:", value='today', width=150, format="DD/MM/YYYY", key="final-date")
        with tables:
            # new_tables = st.radio("Tabelas:",['Unimed Medicamentos Própria', 'Unimed Materiais Própria'])
            st.checkbox('Unimed Medicamentos Própria', key='tabela_medicamento')
            st.checkbox('Unimed Materiais Própria', key='tabela_materiais')
        with submitted_col:
            submitted = st.form_submit_button("Pesquisar")

    if submitted:

        if st.session_state.initial_date is None:
            st.warning("Selecione a data inicial.")
            st.stop()

        if st.session_state.tabela_medicamento == True and st.session_state.tabela_materiais == True:
            tab_fat_condition = 'CD_TAB_FAT IN (1,50)'
        elif st.session_state.tabela_medicamento == True: 
            tab_fat_condition = "CD_TAB_FAT = 1"
        elif st.session_state.tabela_materiais == True:
            tab_fat_condition = "CD_TAB_FAT = 50"
        else:
            st.warning("Selecione ao menos uma tabela.")
            st.stop()

        
        
        query_final = viewer_queries.viewer_last_update.format(tab_fat_condition=tab_fat_condition)
        dados = {
            'date_from': new_from_date.strftime("%d/%m/%Y"),
            'date_to': new_to_date.strftime("%d/%m/%Y")
        }

        try:
            cur = con.cursor()
            cur.execute(query_final, dados)
            rows = cur.fetchall()
            columns = [col[0] for col in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            df = df[['VIGENCIA', 'TABELA', 'USUARIO']]
            st.dataframe(df.set_index('VIGENCIA'))
        except oracledb.Error as e:
            st.error(e)

    