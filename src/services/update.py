from src.services import from_to_last_value
from src.queries import update_queries
import os
import msvcrt
import oracledb

def exists_update_with_current_vigency(con):
  try:
    cur = con.cursor()
    cur.execute(update_queries.check_updateSQL)
    r = cur.fetchall()
    return r
  except oracledb.Error as e:
    return e

def execute_update(con, typeSpreadsheet):  
  # Verifica o tipo de atualização
  dfUpdate = from_to_last_value.updatedProcedures(typeSpreadsheet, con)
  dfNewValue = dfUpdate.copy()

  dfNewValue = dfNewValue[['CD_PRO_FAT', 'NEW_VALUE']]

  if typeSpreadsheet == 0:
    dfNewValue['CD_TAB_FAT'] = 1
  elif typeSpreadsheet == 1:
    dfNewValue['CD_TAB_FAT'] = 50

  dados = dfNewValue.to_dict(orient='records')
  try:
    cur = con.cursor()
    cur.executemany(update_queries.update_new_valuesSQL, dados)
    con.commit()
    return (f"Atualização realizada com sucesso! {len(dados)} registros atualizados.")
  except oracledb.Error as e:
    return e