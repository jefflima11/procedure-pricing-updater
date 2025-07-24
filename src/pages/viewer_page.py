from src.queries import viewer_queries
import streamlit as st
import pandas as pd
import oracledb
import numpy as np

def viewer(con):
    st.subheader("Ultimas atualizações")
    from_date = st.date_input("De:" ,width=150, format="DD/MM/YYYY", max_value="today")
    to_date = st.date_input("Até:", value='today', width=150, format="DD/MM/YYYY")

    new_from_date = from_date.strftime("%d/%m/%Y")
    new_to_date = to_date.strftime("%d/%m/%Y")
    st.write(new_from_date, new_to_date)
    args = {
        'from': new_from_date,
        'to': new_to_date
    }

    st.write(args)
    try:
        cur = con.cursor()
        cur.execute(viewer_queries.viewer_last_update)
        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        df = df[['VIGENCIA', 'TABELA', 'USUARIO']]
        st.write(df)
    except oracledb.Error as e:
        st.error(e)