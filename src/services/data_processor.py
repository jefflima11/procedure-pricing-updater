from src.db.connection import get_connection
from src.queries.data_processor_queries import cleanFromToSQL, checkExistsFromToSQL, insertFromToSQL
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

def confirmInsert():
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(checkExistsFromToSQL)
        rows = cur.fetchall()

        if not rows:
            chooseSpreadsheetType()
        else:
            checkCleanlinessFromTo()
            
    except oracledb.Error as e:
        print(e)
    finally:
        cur.close()
        con.close()

def makeSpreadsheet():
    df = importSpreadsheet()
    return df

def medicationsProcedures(df):

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

    # Trata os procedimentos de valores zerados
    handlingOfZeroValues(newDf)

    # trata os procedimentos não configurados na tela M_BRASINDI
    checksForUnconfiguredProcedures(newDf)

    # trata os procedimentos sem brasindice
    proceduresWithoutBrasindice(newDf)

    # Dataframe de valore não zerados e que possuem código brasindice
    dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0
    
    confirmChosenOption(dfFilter)

    exportUpdatedProcedures()

def materialsProcedures(df):
    print() 

def insertFromTo(dfFilter):
    data = dfFilter.to_dict(orient='records')

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

    exportForUnconfiguredProcedures()

    print("* Tratamento de dados e inserção realizada na tabela de De-Para! *")
    print("* Relatório de inconsistencias gerado!* \n")

