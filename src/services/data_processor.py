from src.db.connection import get_connection
from src.queries.data_processor_queries import cleanFromToSQL, checkExistsFromToSQL, insertFromToSQL
import glob
import pandas as pd
import os
import msvcrt
import sys

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
            med()
        elif worksheetTypeOptions =='2':
            print('tab')
        else:
            chooseSpreadsheetType()

def med():
    inputDir = os.path.join("src", "resources", "in")

    spreadsheets = glob.glob(os.path.join(inputDir, "*.xlsx"))

    if not spreadsheets:
        print("Nenhuma planilha encontrada.")
        exit()
    
    def loadSpreadsheetOptions():
        os.system('cls')
        print("Selecione a planilha para carregar:\n")
        for i, spreadsheet in enumerate(spreadsheets):
            nome = os.path.basename(spreadsheet)
            print(f"{i+1} - {nome}")
        

        chosenWorksheet = msvcrt.getch().decode()

        try:
            idx = int(chosenWorksheet) - 1
            if idx < 0 or idx >= len(spreadsheets):
                raise IndexError  
            print('')
        except:
            loadSpreadsheetOptions()
        # exit()
        return idx
    
    idx = loadSpreadsheetOptions()    

    chosenFile = spreadsheets[idx]
    print(f"\nCarregando: {chosenFile}")
    
    df = pd.read_excel(chosenFile, sheet_name="Plan1")
    df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor'})
    df0 = df0[['tiss','valor']]

    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    df0['tiss'] = df0['tiss'].astype(str)

    # Dataframe de valores zerados
    df_zero_values = df0.loc[df0['valor'] == 0.0000, ['tiss','valor']]

    # Dataframe de valore não zerados e que possuem código brasindice
    dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    dfFilter['vl_honorario'] = 0
    dfFilter['vl_operacional'] = 0

    def confirmChosenOption():
        os.system('cls')
        print('Amostra de valores tratados:\n')
        print(dfFilter.head())

        print('\nConfirmar inserção de valores de-para?')           
        print('1 - Sim')
        print('2 - Não, retornar ao menu.\n')

        insertOption = msvcrt.getch().decode()
        if insertOption == '1':
            os.system('cls')
            insertFromTo(dfFilter)
        elif insertOption == '2':
            os.system('cls')
        else:
            confirmChosenOption()
    confirmChosenOption()

def mat():
    print()
    # inputDir = os.path.join("src", "resources", "in")

    # spreadsheets = glob.glob(os.path.join(inputDir, "*.xlsx"))

    # if not spreadsheets:
    #     print("Nenhuma spreadsheet encontrada.")
    #     exit()
    
    # print("Selecione a spreadsheet para carregar:\n")
    # for i, spreadsheet in enumerate(spreadsheets):
    #     nome = os.path.basename(spreadsheet)
    #     print(f"{i+1} - {nome}")

    # chosenWorksheet = msvcrt.getch().decode()

    # try:
    #     idx = int(chosenWorksheet) - 1
    #     if idx < 0 or idx >= len(spreadsheets):
    #         raise IndexError
    # except:
    #     print("Opção inválida.")
    #     exit()
    
    # chosenFile = spreadsheets[idx]
    # print(f"\nCarregando: {chosenFile}")
    
    # df = pd.read_excel(chosenFile, sheet_name="Plan1")
    # df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor'})
    # df0 = df0[['tiss','valor']]

    # df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    # df0['tiss'] = df0['tiss'].astype(str)

    # # Dataframe de valores zerados
    # df_zero_values = df0.loc[df0['valor'] == 0.0000, ['tiss','valor']]

    # # Dataframe de valore não zerados e que possuem código brasindice
    # dfFilter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    # dfFilter['vl_honorario'] = 0
    # dfFilter['vl_operacional'] = 0

    # os.system('cls')
    # print('Amostra de valores tratados:\n')
    # print(dfFilter.head())

    # print('\nConfirmar inserção de valores de-para?')           
    # print('1 - Sim')
    # print('2 - Não\n')
    # print('Pressione a tecla da opção desejada:')
    # insertOption = msvcrt.getch().decode()
    # if insertOption == '1':
    #     inserir_de_para(dfFilter)
    # elif insertOption == '2':
    #     os.system('cls')
    #     print('')

def insertFromTo(dfFilter):
        data = dfFilter.to_dict(orient='records')

        con = get_connection()
        cur = con.cursor()

        cur.executemany(insertFromToSQL, data)
        con.commit()

        cur.close()
        con.close()

        print("Tratamento de dados e inserção realizada na tabela de De-Para!")