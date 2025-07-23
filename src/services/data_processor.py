from src.queries import data_processor_queries
from src.utils import procedures_without_brasindice, handling_of_zero_values, checks_for_unconfigured_procedures, states
from src.services.from_to_last_value import exportUpdatedProcedures
import pandas as pd
import oracledb
import streamlit as st  


def check_from_to_table(con=None):
    try:
        cur = con.cursor()
        cur.execute(data_processor_queries.check_exists_from_toSQL)
        rows = cur.fetchall()

        if rows[0][0] == 1:
            return 1
        elif rows[0][0] == 2:
            return 2
        else:
            return 3
    except oracledb.Error as e:
        return (e)

def medicationsProcedures(df, con):
    typeSpreadsheet = 0

    df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor', 'Nome e Apresentação Comercial': 'descricao', 'Código': 'codigo_brasindice'})
    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    newDf = df0[['tiss','codigo_brasindice', 'valor','descricao']]
    df0 = df0[['tiss','valor']]
    df0['tiss'] = df0['tiss'].astype(str)

    
    zero = handling_of_zero_values.handlingOfZeroValues(newDf, typeSpreadsheet)
    unconf = checks_for_unconfigured_procedures.checks_for_unconfigured_procedures(newDf, typeSpreadsheet, con)
    brasind = procedures_without_brasindice.procedures_without_brasindice(newDf)

    dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0

    fromTo = insertFromTo(dfFilter, typeSpreadsheet, con)
    updated = exportUpdatedProcedures(typeSpreadsheet, con)
    st.warning(f"{zero['msg']} procedimentos zerados, {unconf['msg']} não configurados, {brasind['msg']} sem Brasindice e {fromTo['msg']} inseridos", icon="⚠️")

def materialsProcedures(df, con):
    typeSpreadsheet = 1

    df0 = df.rename(columns={'Código': 'tuss', 'Valor Máximo Intercâmbio Nacional': 'valor', 'Descrição do Produto': 'descricao'})
    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    newDf = df0[['tuss', 'descricao', 'valor']]
    df0 = df0[['tuss', 'valor']]
    df0['tuss'] = df0['tuss'].astype(str)

    zero = handlingOfZeroValues(newDf, typeSpreadsheet)
    unconf = checksForUnconfiguredProcedures(newDf, typeSpreadsheet, con)

    dfFilter = df0.loc[df0['valor'] != 0, ['tuss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0

    fromTo = insertFromTo(dfFilter, typeSpreadsheet, con)
    updated = exportUpdatedProcedures(typeSpreadsheet, con)

    st.warning(f"{zero['msg']} procedimentos zerados, {unconf['msg']} não configurados e {fromTo['msg']} inseridos", icon="⚠️")

def insertFromTo(dfFilter, typeSpreadsheet, con=None):
    data = dfFilter.to_dict(orient='records')
    
    if typeSpreadsheet == 0:
        insertFromToSQL = data_processor_queries.insert_from_to_medSQL
    elif typeSpreadsheet == 1:
        insertFromToSQL = data_processor_queries.insert_from_to_matSQL

    try:
        cur = con.cursor()
        cur.executemany(insertFromToSQL, data)
        con.commit()
        msg = {
            'type': 'S',
            'msg': len(data)
        }
    except oracledb.Error as e:
        msg = {
            'type': 'E',
            'msg': f'Erro ao inserir dados na tabela de de-para: {e}'
        }
    return msg

    states.state_function(exportForUnconfiguredProcedures(typeSpreadsheet, con))