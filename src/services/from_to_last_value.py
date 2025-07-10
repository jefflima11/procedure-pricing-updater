from src.db.connection import get_connection
from src.queries.from_to_last_value_queries import fromToLastValueSQL, fromToLastValueMatSQL
import pandas as pd
import msvcrt
import os
import oracledb
import datetime
from openpyxl import load_workbook

def updatedProcedures():
  try:
    con = get_connection()
    cur = con.cursor()
    cur.execute(fromToLastValueMatSQL)
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]

    df = pd.DataFrame(rows, columns=columns)
  except oracledb.Error as e:
    print(e)
  finally:
    cur.close()
    con.close()
  
  return df

def exportUpdatedProcedures():
  df = updatedProcedures()
  df['diff'] = df['NEW_VALUE'] - df['OLD_VALUE']
  df['percent'] = ((df['NEW_VALUE'] - df['OLD_VALUE']) / df['OLD_VALUE']) * 100
  # print(df.head().dtypes)
  data = df.to_dict(orient='records')

  now = datetime.datetime.now()
  now_formated = now.strftime('%d%m%Y')

  path = f'./src/resources/out/relatório-materiais{now_formated}.xlsx'

  try:
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
      df.to_excel(writer, sheet_name='Proced_atualizados', index=False)
  except:
      print('Erro ao importar os procedimentos atualizados!')