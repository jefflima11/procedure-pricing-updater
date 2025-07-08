from src.db.connection import get_connection
from src.queries.data_processor_queries import cleanFromToSQL, checkExistsFromToSQL, insertFromToSQL
from src.utils.spreadsheet_data_processing import importSpreadsheet
from src.utils.checks_for_unconfigured_procedures import checksForUnconfiguredProcedures, exportForUnconfiguredProcedures
from src.utils.handling_of_zero_values import handlingOfZeroValues
from src.utils.options import confirmChosenOption
import pandas as pd
import os
import msvcrt
import sys
import oracledb

def confirmInsert():

    def checkInsert():
        connect = get_connection()
        cursor = connect.cursor()

        cursor.execute(checkExistsFromToSQL)
        rows = cursor.fetchall()

        if not rows:
            checked = 0
        else:
            checked = 1

        cursor.close()
        connect.close()
        checkInsertOptions(checked)
    
    def checkInsertOptions(checked):
        if checked == 0:
            chooseSpreadsheetType()    
        else:
            def checkCleanlinessFromTo(msg=None):
                print('Já existe atualização para vigencia atual!\n')
                print('Deseja limpar a tabela de de-para?\n')
                print('1 - Sim.')
                print('2 - Não, retornar ao menu.\n')

                chosenCleanFromTo = msvcrt.getch().decode()
                if chosenCleanFromTo == '1':
                    
                    con = get_connection()
                    cur = con.cursor()
                    cur.execute(cleanFromToSQL)
                    con.commit()
                    cur.close()
                    con.close()

                    os.system('cls')
                    print('Limpeza de de-para realizada!')
                elif chosenCleanFromTo == '2':
                    os.system('cls')
                else:
                    os.system('cls')
                    print('Opção inválida. Tente novamente!')
                    checkCleanlinessFromTo()
            checkCleanlinessFromTo()
    checkInsert()

def chooseSpreadsheetType():
        os.system('cls')
        print('Por favor informe o tipo da spreadsheet:\n')
        print('1 - Medicamentos')
        print('2 - Materiais\n')

        worksheetTypeOptions = msvcrt.getch().decode()
        if worksheetTypeOptions == '1':
            medicationsProcedures(makeSpreadsheet())
        elif worksheetTypeOptions =='2':
            materialsProcedures(makeSpreadsheet())
        else:
            chooseSpreadsheetType()

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

    # Dataframe de valore não zerados e que possuem código brasindice
    dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0
    
    confirmChosenOption(dfFilter)

def materialsProcedures(df):
    print() 

def insertFromTo(dfFilter):
    data = dfFilter.to_dict(orient='records')

    con = get_connection()
    cur = con.cursor()

    cur.executemany(insertFromToSQL, data)
    con.commit()

    cur.close()
    con.close()

    exportForUnconfiguredProcedures()

    print("* Tratamento de dados e inserção realizada na tabela de De-Para! *")
    print("* Relatório de inconsistencias gerado!* \n")

