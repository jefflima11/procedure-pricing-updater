from src.queries.from_to_last_value_queries import fromToLastValueMedSQL, fromToLastValueMatSQL
import pandas as pd
import os
import oracledb
import datetime
from openpyxl import load_workbook

def updatedProcedures(typeSpreadsheet=None, con=None):
  def runQuery(query):
    try:
      cur = con.cursor()
      cur.execute(query)
      rows = cur.fetchall()
      columns = [col[0] for col in cur.description]

      df = pd.DataFrame(rows, columns=columns)
      return df
    except oracledb.Error as e:
      orint(f"Erro ao executar a consulta: {e}")

  if typeSpreadsheet == 0:
    fromToLastValueSQL = fromToLastValueMedSQL
    return runQuery(fromToLastValueSQL)
  elif typeSpreadsheet == 1:
    fromToLastValueSQL = fromToLastValueMatSQL
    return runQuery(fromToLastValueSQL)
  else:
    return 'Erro na definição do tipo de planilha!'


def exportUpdatedProcedures(typeSpreadsheet, con):
  df = updatedProcedures(typeSpreadsheet, con)

  if typeSpreadsheet == 0:
    typeS = "medicamentos"
  elif typeSpreadsheet == 1:
    typeS = "materiais"

  df['diff'] = df['NEW_VALUE'] - df['OLD_VALUE']
  df['percent'] = ((df['NEW_VALUE'] - df['OLD_VALUE']) / df['OLD_VALUE']) * 100
  data = df.to_dict(orient='records')

  now = datetime.datetime.now()
  now_formated = now.strftime('%d%m%Y')

  path = f'./src/resources/out/relatório-{typeS}{now_formated}.xlsx'

  try:
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
      df.to_excel(writer, sheet_name='Proced_atualizados', index=False)
  except:
      print('Erro ao importar os procedimentos atualizados!')
