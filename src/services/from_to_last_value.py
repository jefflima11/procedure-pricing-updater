from src.db.connection import get_connection
from src.queries.from_to_last_value_queries import fromToLastValueMedSQL, fromToLastValueMatSQL
import pandas as pd
import msvcrt
import os
import oracledb
import datetime
from openpyxl import load_workbook

def updatedProcedures(typeSpreadsheet):
  if typeSpreadsheet == 0:
    fromToLastValueSQL = fromToLastValueMedSQL
  elif typeSpreadsheet == 1:
    fromToLastValueSQL = fromToLastValueMatSQL

  
  try:
    con = get_connection()
    cur = con.cursor()
    cur.execute(fromToLastValueSQL)
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]

    df = pd.DataFrame(rows, columns=columns)
  except oracledb.Error as e:
    print(e)
  finally:
    cur.close()
    con.close()

  return df


def exportUpdatedProcedures(typeSpreadsheet):
  df = updatedProcedures(typeSpreadsheet)

  if typeSpreadsheet == 0:
    typeS = "medicamentos"
  elif typeSpreadsheet == 1:
    typeS = "materiais"

  df['diff'] = df['NEW_VALUE'] - df['OLD_VALUE']
  df['percent'] = ((df['NEW_VALUE'] - df['OLD_VALUE']) / df['OLD_VALUE']) * 100
  # print(df.head().dtypes)
  data = df.to_dict(orient='records')

  now = datetime.datetime.now()
  now_formated = now.strftime('%d%m%Y')

  path = f'./src/resources/out/relatório-{typeS}{now_formated}.xlsx'

  try:
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
      df.to_excel(writer, sheet_name='Proced_atualizados', index=False)
  except:
      print('Erro ao importar os procedimentos atualizados!')
