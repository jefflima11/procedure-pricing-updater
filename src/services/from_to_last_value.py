from src.db.connection import get_connection
from src.queries.from_to_last_value_queries import fromToLastValueSQL
import pandas as pd
import msvcrt
import os

def dataframe_export():
  connect = get_connection()
  cursor = connect.cursor()

  cursor.execute(fromToLastValueSQL)
  rows = cursor.fetchall()
  columns = [col[0] for col in cursor.description]

  connect = get_connection()
  cursor = connect.cursor()

  df = pd.DataFrame(rows, columns=columns)
  cursor.close()
  connect.close()
  
  return df

def dataframe_view(df=None):
  options(df)

def options(df=None):
    print(df)
    print('\nRetornar ao menu?\n')
    print('1 - Sim.')
    option = msvcrt.getch().decode()

    if option == '1':
      os.system('cls')
    else:
      os.system('cls')
      print('Opção inválida. Por favor tente novamente!\n')
      dataframe_view(dataframe_export())
      options()