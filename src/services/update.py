from src.db.connection import get_connection
from src.services.from_to_last_value import updatedProcedures
from src.queries.update_queries import updateNewValuesSQL, checkUpdateSQL, cleanUpdateSQL
from src.utils.options import updatedCleanOptions
from src.utils import messages
import os
import msvcrt
import oracledb

def verificaUpdate():
  try:
    con = get_connection()
    cur = con.cursor()
    cur.execute(checkUpdateSQL)
    r = cur.fetchall()
    if r:
      verif = 0
    else:
      verif = 1
  except oracledb.Error as e:
    print(e)
  finally:
    cur.close()
    con.close()
    
  return verif

def executeUpdate():
  while True:
    # Verifica o tipo de atualização
    typeSpreadsheet = checkTheUpdateType()
    dfUpdate = updatedProcedures(typeSpreadsheet)

    if typeSpreadsheet == 3:
      messages.terminalCleaning()
      return

    # Verifica se a tabela de de-para esta vazia
    if dfUpdate is None:
      messages.terminalCleaning()
      messages.invalidOption()
    elif dfUpdate.empty:
      messages.terminalCleaning()
      if typeSpreadsheet == 0:
        print('* Não existe importação da tabela Brasindice *\n')
      elif typeSpreadsheet == 1:
        print('* Não existe importação da tabela Simpro *\n')
    else:
      if verificaUpdate() == 0:
        updatedCleanOptions()  
      else:
        messages.terminalCleaning()
        dfNewValue = dfUpdate.copy()

        dfNewValue = dfNewValue[['CD_PRO_FAT', 'NEW_VALUE']]

        if typeSpreadsheet == 0:
          dfNewValue['CD_TAB_FAT'] = 1
        elif typeSpreadsheet == 1:
          dfNewValue['CD_TAB_FAT'] = 50

        dados = dfNewValue.to_dict(orient='records')
        try:
          con = get_connection()
          cur = con.cursor()
          cur.executemany(updateNewValuesSQL, dados)
          con.commit()
          print('* Valores de produtos atualizados! *\n')
        except oracledb.Error as e:
          print(e)
        finally:
          cur.close()
          con.close()   
      # return
    

    
      
def checkTheUpdateType():
  messages.checkTheUpdateType()
  key = msvcrt.getch().decode()

  if key == '1':
    typeSpreadsheet = 0
  elif key == '2':
    typeSpreadsheet = 1
  elif key == '0':
    typeSpreadsheet = 3
  else:
    typeSpreadsheet = 4

  return typeSpreadsheet