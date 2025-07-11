from src.utils.handling_of_zero_values import handlingOfZeroValues
from src.utils import messages
from src.db.connection import get_connection
from src.queries.data_processor_queries import cleanFromToSQL
from src.queries.update_queries import cleanUpdateSQL
import oracledb
import os
import msvcrt

def confirmChosenOption(dfFilter, typeSpreadsheet):

    while True:
        messages.confirmChosenOption()

        insertOption = msvcrt.getch().decode()
        if insertOption == '1':
            messages.terminalCleaning()

            from src.services.data_processor import insertFromTo
            insertFromTo(dfFilter, typeSpreadsheet)  
            return          
        elif insertOption == '0':
            messages.terminalCleaning()
            return

def chooseSpreadsheetType():
    messages.terminalCleaning()

    while True:
        from src.services.data_processor import medicationsProcedures, materialsProcedures
        from src.utils.spreadsheet_data_processing import importSpreadsheet
        messages.chooseSpreadsheetType()

        worksheetTypeOptions = msvcrt.getch().decode()        
        if worksheetTypeOptions == '1':
            medicationsProcedures(importSpreadsheet("med"))
            return
        elif worksheetTypeOptions =='2':
            materialsProcedures(importSpreadsheet("mat"))
            return
        elif worksheetTypeOptions == '0':
            return
        else:
            messages.terminalCleaning()

def checkCleanlinessFromTo(msg=None):
    messages.checkCleanlinessFromTo()    

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

        messages.terminalCleaning()
        print('* Limpeza de de-para realizada! *')

    elif chosenCleanFromTo == '2':
        messages.terminalCleaning()
    else:
        messages.terminalCleaning()
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

        messages.terminalCleaning()
        print('\nLimpeza de valores realizada!')
    elif clean_update == '2':
        messages.terminalCleaning()
    else:
        messages.terminalCleaning()
        cleanOptions()

