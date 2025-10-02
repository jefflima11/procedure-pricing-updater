import src.models.fromToModel as ftm
import src.services.data_processor as dp
from src.services import cleanup_tasks
from src.db import connection
import oracledb
import streamlit as st
import pandas as pd
import os

def insert(con=None):
    state = ftm.checkFromTo(con)
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
                    cur.execute("""
                        SELECT 
                            CD_TISS TISS, 
                            CD_TUSS TUSS, 
                            DT_VIGENCIA VIGENCIA, 
                            VL_HONORARIO HONORARIO, 
                            VL_OPERACIONAL OPERACIONAL, 
                            VL_TOTAL TOTAL, 
                            NM_USUARIO USUARIO  
                        FROM 
                            DBAHUMS.DE_PARA_HUMS""");
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
            
            msg = cleanup_tasks.cleaner(con)
            st.info(msg)
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
                    dp.medicationsProcedures(df, con)

                elif "mat" in uploaded_file.name.lower():
                    dp.materialsProcedures(df, con)

                else:
                    st.write("Tipo de planilha não identificado. Por favor, verifique o nome do arquivo.")

                

            st.button("Processar", on_click=process_data, args=(df, con, state, uploaded_file))    