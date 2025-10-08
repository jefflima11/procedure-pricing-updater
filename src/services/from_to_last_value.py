from src.queries import from_to_last_value_queries
from openpyxl import load_workbook
import pandas as pd
import streamlit as st
import oracledb
import datetime


def updatedProcedures(typeSpreadsheet, con):
  def runQuery(query):
    try:
      cur = con.cursor()
      cur.execute(query)
      rows = cur.fetchall()
      columns = [col[0] for col in cur.description]

      df = pd.DataFrame(rows, columns=columns)
      return df
    except oracledb.Error as e:
      print(f"Erro ao executar a consulta: {e}")
    
  if typeSpreadsheet == 0:
    fromToLastValueSQL = from_to_last_value_queries.from_to_last_value_medSQL
  elif typeSpreadsheet == 1:
    fromToLastValueSQL = from_to_last_value_queries.from_to_last_value_matSQL
  else:
    print('Erro na definição do tipo de planilha!')

  try:
    return runQuery(fromToLastValueSQL)
  except Exception as e:
    print(f"Erro ao executar a consulta: {e}")

def exportUpdatedProcedures(typeSpreadsheet, con):
  now = datetime.datetime.now()
  now_formated = now.strftime('%d%m%Y')

  df = updatedProcedures(typeSpreadsheet, con)

  if typeSpreadsheet == 0:
    typeS = "medicamentos"
  elif typeSpreadsheet == 1:
    typeS = "materiais"

  print("Calculando diferenças e percentuais...")
  
  df['diff'] = df['NEW_VALUE'] - df['OLD_VALUE']
  df['percent'] = ((df['NEW_VALUE'] - df['OLD_VALUE']) / df['OLD_VALUE']) * 100
  data = df.to_dict(orient='records')

  
  path = f'./src/resources/out/relatório-{typeS}{now_formated}.xlsx'

  try:
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
      df.to_excel(writer, sheet_name='Proced_atualizados', index=False)

      print(f'Procedimentos atualizados exportados com sucesso para {path}')
  except:
      print('Erro ao importar os procedimentos atualizados!')

