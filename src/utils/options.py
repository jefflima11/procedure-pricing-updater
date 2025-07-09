from src.utils.handling_of_zero_values import handlingOfZeroValues
from src.db.connection import get_connection
from src.queries.data_processor_queries import cleanFromToSQL
from src.queries.update_queries import cleanUpdateSQL
import oracledb
import os
import msvcrt

def confirmChosenOption(dfFilter):
    os.system('cls')
    print('Amostra de valores tratados:\n')
    print(dfFilter.head())

    print('\nConfirmar inserção de valores de-para?')           
    print('1 - Sim')
    print('2 - Não, retornar ao menu.\n')

    insertOption = msvcrt.getch().decode()
    if insertOption == '1':
        os.system('cls')
        from src.services.data_processor import insertFromTo
        insertFromTo(dfFilter)
    elif insertOption == '2':
        os.system('cls')
    else:
        confirmChosenOption()

def chooseSpreadsheetType():
    os.system('cls')
    print('Por favor informe o tipo da spreadsheet:\n')
    print('1 - Medicamentos')
    print('2 - Materiais\n')

    worksheetTypeOptions = msvcrt.getch().decode()
    from src.services.data_processor import medicationsProcedures, makeSpreadsheet, materialsProcedures
    if worksheetTypeOptions == '1':
        medicationsProcedures(makeSpreadsheet())
    elif worksheetTypeOptions =='2':
        materialsProcedures(makeSpreadsheet())
    else:
        chooseSpreadsheetType()

def checkCleanlinessFromTo(msg=None):
    print('Já existe atualização para vigencia atual!\n')
    print('Deseja limpar a tabela de de-para?\n')
    print('1 - Sim.')
    print('2 - Não, retornar ao menu.\n')

    chosenCleanFromTo = msvcrt.getch().decode()

    if chosenCleanFromTo == '1':
        
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute(cleanFromToSQL)
            con.commit()
        except oracledb.Error as e:
            print('Erro ao tentar realizar limpeza da tabela DE_PARA_HUMS:')
            print(e)
        finally:    
            cur.close()
            con.close()

        os.system('cls')
        print('* Limpeza de de-para realizada! *')

    elif chosenCleanFromTo == '2':
        os.system('cls')
    else:
        os.system('cls')
        print('Opção inválida. Tente novamente!')
        checkCleanlinessFromTo()            

def cleanOptions():
    print('Valores de procedimentos já existentes com vigencia atual!\n')
    print('Deseja limpar os valores com a vigencia atual?\n')
    print('1 - Sim.')
    print('2 - Não, retornar ao menu.')

    clean_update = msvcrt.getch().decode()
    if clean_update == '1':
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute(cleanUpdateSQL)
            con.commit()
        except oracledb.Error as e:
            print(e)
        finally:
            cur.close()
            con.close()

        os.system('cls')
        print('\nLimpeza de valores realizada!')
    elif clean_update == '2':
        os.system('cls')
    else:
        os.system('cls')
        cleanOptions()

