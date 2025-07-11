from src.db.connection import get_connection
from src.queries.data_processor_queries import cleanFromToSQL, checkExistsFromToSQL, insertFromToMedSQL, insertFromToMatSQL
from src.utils.spreadsheet_data_processing import importSpreadsheet
from src.utils.checks_for_unconfigured_procedures import checksForUnconfiguredProcedures, exportForUnconfiguredProcedures
from src.utils.handling_of_zero_values import handlingOfZeroValues
from src.utils.procedures_without_brasindice import proceduresWithoutBrasindice
from src.utils.options import confirmChosenOption, chooseSpreadsheetType, checkCleanlinessFromTo
from src.services.from_to_last_value import exportUpdatedProcedures
import pandas as pd
import os
import msvcrt
import sys
import oracledb

# Confirmação da inserção de de-para
def executeInsert():
    # Tentativa de realizar a checagem e a insercao
    try:
        con = get_connection()
        cur = con.cursor()
        # Checa se existe dados na tabela de de-para
        cur.execute(checkExistsFromToSQL)
        rows = cur.fetchall()
                # Caso não exista dados na tabela de de para...
        # Escolher o tipo da planilha, material ou medicamento
        if not rows:
            chooseSpreadsheetType()
        # Caso exista dados na tabela de de para...
        else:
            # Verifica se deve ser realizada a limpeza na tabela de-para
            checkCleanlinessFromTo()    
    except oracledb.Error as e:
        print(e)
    finally:
        cur.close()
        con.close()

# Tratamento da planilha de medicamentos
def medicationsProcedures(df=None):
    if df is None:
        return None
    # Renomeia as tabelas principais a serem usadas na atualização de valores
    df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor', 'Nome e Apresentação Comercial': 'descricao', 'Código': 'codigo_brasindice'})
    # Substitui todas as virgulas por pontos e altera o tipo da coluna "valor" para float
    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    # Executa exportação de procedimentos não configurados
    newDf = df0[['tiss','codigo_brasindice', 'valor','descricao']]
    # Isola as colunas desejadas
    df0 = df0[['tiss','valor']]
    # Altera o tipo "tiss" para string
    df0['tiss'] = df0['tiss'].astype(str)
    typeSpreadsheet = 0
    # Trata os procedimentos de valores zerados
    handlingOfZeroValues(newDf, typeSpreadsheet)
    # trata os procedimentos não configurados na tela M_BRASINDI
    checksForUnconfiguredProcedures(newDf, typeSpreadsheet)
    # trata os procedimentos sem brasindice
    proceduresWithoutBrasindice(newDf)
    # Dataframe de valore não zerados e que possuem código brasindice
    dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0
    # Escolha de confirmação se deseja realizar a inserção de dados na de-para
    confirmChosenOption(dfFilter, typeSpreadsheet)
    # Exportacao dos dados atualizados
    exportUpdatedProcedures(typeSpreadsheet)

# Tratamento da planilha de materiais
def materialsProcedures(df=None):
    if df is None:
        return None
    df0 = df.rename(columns={'Código': 'tuss', 'Valor Máximo Intercâmbio Nacional': 'valor', 'Descrição do Produto': 'descricao'})
    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    newDf = df0[['tuss', 'descricao', 'valor']]
    df0 = df0[['tuss', 'valor']]
    df0['tuss'] = df0['tuss'].astype(str)
    typeSpreadsheet = 1
    handlingOfZeroValues(newDf, typeSpreadsheet)
    checksForUnconfiguredProcedures(newDf, typeSpreadsheet)
    dfFilter = df0.loc[df0['valor'] != 0, ['tuss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0
    confirmChosenOption(dfFilter, typeSpreadsheet)
    exportUpdatedProcedures(typeSpreadsheet)

def insertFromTo(dfFilter, typeSpreadsheet):
    # Transformacao do dataframe em array
    data = dfFilter.to_dict(orient='records')
    if typeSpreadsheet == 0:
        insertFromToSQL = insertFromToMedSQL
    elif typeSpreadsheet == 1:
        insertFromToSQL = insertFromToMatSQL

    try:
        con = get_connection()
        cur = con.cursor()
        cur.executemany(insertFromToSQL, data)
        con.commit()
    except oracledb.Error as e:
        print('Erro ao tentar realizar insert na tabela DE_PARA_HUMS:')
        print(e)
    finally:
        cur.close()
        con.close()

    # Exportacao dos procedimentos nao configurados em tela
    exportForUnconfiguredProcedures(typeSpreadsheet)
    print("* Tratamento de dados e inserção realizada na tabela de De-Para! *")
    print("* Relatório de inconsistencias gerado!* \n")