from src.db.connection import get_connection
from src.services.from_to_last_value import dataframe_export
from src.queries.update_queries import updateNewValuesSQL, checkUpdateSQL, cleanUpdateSQL
import os
import msvcrt

def verifica_update():

  connect = get_connection()
  cursor = connect.cursor()
  cursor.execute(checkUpdateSQL)
  result = cursor.fetchall()
  
  if result:
    verificador = 0
  else:
    verificador = 1

  return verificador

def execute_update():
  # Verifica se a tabela de de-para esta vazia
  if dataframe_export().empty:
    print('Não existe atualização na tabela DBAHUMS.DE_PARA_HUMS')
  else:
    if verifica_update() == 0:
      def clean_options():
        print('Valores de procedimentos já existentes com vigencia atual!\n')
        print('Deseja limpar os valores com a vigencia atual?\n')
        print('1 - Sim.')
        print('2 - Não, retornar ao menu.')

        clean_update = msvcrt.getch().decode()
        if clean_update == '1':
          connect = get_connection()
          cursor = connect.cursor()
          cursor.execute(cleanUpdateSQL)
          connect.commit()
          cursor.close()
          connect.close()

          os.system('cls')
          print('\nLimpeza de valores realizada!')
        elif clean_update == '2':
          os.system('cls')
        else:
          os.system('cls')
          clean_options()
      clean_options()  
    else:
      df = dataframe_export()
      df_new_value = df.copy()

      df_new_value = df_new_value[['CD_PRO_FAT', 'NEW_VALUE']]
      dados = df_new_value.to_dict(orient='records')
 
      connect = get_connection()
      cursor = connect.cursor()

      cursor.executemany(updateNewValuesSQL, dados)
      connect.commit()

      cursor.close()
      connect.close()    
      print('Valores de produtos atualizados!')