from src.utils import procedures_without_brasindice, handling_of_zero_values, checks_for_unconfigured_procedures
import src.services.from_to_last_value as ftlv
import src.models.fromToModel as ftm
import pandas as pd
import oracledb
import streamlit as st  
import time

def medicationsProcedures(df, con):
    typeSpreadsheet = 0

    df0 = df.rename(columns={
        'Cod TISS Brasindice': 'tiss', 
        'Preço Máximo Intercâmbio Nacional': 'valor', 
        'Nome e Apresentação Comercial': 'descricao', 
        'Código': 'codigo_brasindice'
    })
    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    newDf = df0[['tiss','codigo_brasindice', 'valor','descricao']]
    df0 = df0[['tiss','valor']]
    df0['tiss'] = df0['tiss'].astype(str)

    dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0

    with st.status("Processando dados...", expanded=True) as status:
        try:
            st.write("Tratando procedimentos sem valor...")
            time.sleep(2)
            handling_of_zero_values.handling_of_zero_values(newDf, typeSpreadsheet)
        except Exception as e:
            st.error(f"Erro ao separar procedimentos sem valor: {e}")

        try:
            st.write("Tratando procedimentos sem Brasindice...")
            time.sleep(2)
            procedures_without_brasindice.procedures_without_brasindice(newDf)    
        except Exception as e:
            st.error(f"Erro ao separar procedimentos sem Brasindice: {e}")

        try:
            time.sleep(2)
            ftm.insertFromTo(dfFilter, typeSpreadsheet, con)
        except Exception as e:
            st.error(f"Erro ao inserir dados na tabela de de-para: {e}")

        try:
            st.write("Exportando procedimentos não configurados...")
            time.sleep(2)
            checks_for_unconfigured_procedures.checks_for_unconfigured_procedures(newDf,typeSpreadsheet, con)
        except Exception as e:
            st.error(f"Erro ao exportar procedimentos não configurados: {e}")

        try:
            st.success("Compilando informações de procedimentos em planilha excel...")
            time.sleep(2)
            ftlv.exportUpdatedProcedures(typeSpreadsheet, con)
        except Exception as e:
            st.error(f"Erro ao exportar informações: {e}")

        time.sleep(5)

        status.update(label="Processamento concluído!", state="complete", expanded=False)

def materialsProcedures(df, con):
    typeSpreadsheet = 1

    df0 = df.rename(columns={
        'Código': 'tuss', 
        'Valor Máximo Intercâmbio Nacional': 'valor', 
        'Descrição do Produto': 'descricao'
    });

    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    newDf = df0[['tuss', 'descricao', 'valor']]
    df0 = df0[['tuss', 'valor']]
    df0['tuss'] = df0['tuss'].astype(str)

    dfFilter = df0.query("valor > 0.000")[['tuss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0

    with st.status("Processando dados...", expanded=True) as status:
        try:
            st.write("Exportando procedimentos sem valor...")
            time.sleep(3)

            handling_of_zero_values.handling_of_zero_values(newDf, typeSpreadsheet)
        except Exception as e:
            st.error(f"Erro ao separar procedimentos sem valor: {e}")

        try:
            st.write("Inserindo dados na tabela de de-para...")
            time.sleep(2)
            ftm.insertFromTo(dfFilter, typeSpreadsheet, con)
        except Exception as e:
            st.error(f"Erro ao inserir dados na tabela de de-para: {e}")

        try:
            st.write("Exportando procedimentos não configurados...")
            time.sleep(2)
            checks_for_unconfigured_procedures.checks_for_unconfigured_procedures(newDf, typeSpreadsheet, con)
        except Exception as e:
            st.error(f"Erro ao separar procedimentos não configurados: {e}")

        try:
            st.write("Exportando informações dos procedimentos para planilha excel...")
            time.sleep(2)
            ftlv.exportUpdatedProcedures(typeSpreadsheet, con)
        except Exception as e:
            st.error(f"Erro ao exportar informações: {e}")
        st.stop()
        
        status.update(label="Processamento concluído!", state="complete", expanded=False)
