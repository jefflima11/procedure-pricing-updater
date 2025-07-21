from src.queries.data_processor_queries import cleanFromToSQL, checkExistsFromToSQL, insertFromToMedSQL, insertFromToMatSQL
from src.utils.spreadsheet_data_processing import importSpreadsheet
from src.utils.checks_for_unconfigured_procedures import checksForUnconfiguredProcedures, exportForUnconfiguredProcedures
from src.utils.handling_of_zero_values import handlingOfZeroValues
from src.utils.procedures_without_brasindice import proceduresWithoutBrasindice
from src.utils.options import confirmChosenOption, chooseSpreadsheetType
from src.services.from_to_last_value import exportUpdatedProcedures
from src.utils import states
import pandas as pd
import oracledb
import streamlit as st  


def check_from_to_table(con=None):
    try:
        cur = con.cursor()
        cur.execute(checkExistsFromToSQL)
        rows = cur.fetchall()

        if not rows:
            return None
        else:
            return 0
    except oracledb.Error as e:
        return (e)

def medicationsProcedures(df, con):
    typeSpreadsheet = 0

    df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor', 'Nome e Apresentação Comercial': 'descricao', 'Código': 'codigo_brasindice'})
    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    newDf = df0[['tiss','codigo_brasindice', 'valor','descricao']]
    df0 = df0[['tiss','valor']]
    df0['tiss'] = df0['tiss'].astype(str)

    
    zero = handlingOfZeroValues(newDf, typeSpreadsheet)
    unconf = checksForUnconfiguredProcedures(newDf, typeSpreadsheet, con)
    brasind = proceduresWithoutBrasindice(newDf)

    
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
        insertFromToSQL = insertFromToMedSQL
    elif typeSpreadsheet == 1:
        insertFromToSQL = insertFromToMatSQL

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