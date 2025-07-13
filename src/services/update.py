from src.db.connection import get_connection
from src.services.from_to_last_value import updatedProcedures
from src.queries.update_queries import updateNewValuesSQL, checkUpdateSQL, cleanUpdateSQL
from src.utils.options import UpdatedCleanOptions
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
  # Verifica o tipo de atualização
  typeSpreadsheet = checkTheUpdateType()
  # Verifica se a tabela de de-para esta vazia
  if updatedProcedures(typeSpreadsheet).empty:
    if typeSpreadsheet == 0:
      msg = print('Não existe importação da tabela Brasindice.')
    elif typeSpreadsheet == 1:
      msg =print('Não existe importação da tabela Simpro.')
    return msg
  else:
    if verificaUpdate() == 0:
      UpdatedCleanOptions()  
      
    else:
      df = updatedProcedures(typeSpreadsheet)
      df_new_value = df.copy()

      df_new_value = df_new_value[['CD_PRO_FAT', 'NEW_VALUE']]

      if typeSpreadsheet == 0:
        df_new_value['CD_TAB_FAT'] = 1
      elif typeSpreadsheet == 1:
        df_new_value['CD_TAB_FAT'] = 50

      dados = df_new_value.to_dict(orient='records')
      try:
        con = get_connection()
        cur = con.cursor()
        cur.executemany(updateNewValuesSQL, dados)
        con.commit()
        print('Valores de produtos atualizados!')
      except oracledb.Error as e:
        print(e)
      finally:
        cur.close()
        con.close()   
      
def checkTheUpdateType():
  messages.checkTheUpdateType()
  key = msvcrt.getch().decode()

  if key == '1':
    typeSpreadsheet = 0
  elif key == '2':
    typeSpreadsheet = 1
  else:
    return
  
  return typeSpreadsheet