from src.db.connection import get_connection
from src.services.from_to_last_value import updatedProcedures
from src.queries.update_queries import updateNewValuesSQL, checkUpdateSQL, cleanUpdateSQL
from src.utils.options import cleanOptions
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
  # Verifica se a tabela de de-para esta vazia
  if updatedProcedures().empty:
    print('Não existe atualização na tabela DBAHUMS.DE_PARA_HUMS')
  else:
    if verificaUpdate() == 0:
      cleanOptions()  
    else:
      df = updatedProcedures()
      df_new_value = df.copy()

      df_new_value = df_new_value[['CD_PRO_FAT', 'NEW_VALUE']]
      dados = df_new_value.to_dict(orient='records')

      try:
        con = get_connection()
        cur = con.cursor()
        cur.executemany(updateNewValuesSQL, dados)
        con.commit()
      except oracledb.Error as e:
        print(e)
      finally:
        cur.close()
        con.close()    
      print('Valores de produtos atualizados!')