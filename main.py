from src.db.connection import get_connection
from src.services.data_processor import realizar_insert
from src.services.from_to_last_value import dataframe_export
from src.services.update import execute_update
from src.utils.interface import confirmar_retorno_menu
import sys
import os
import msvcrt

os.system('cls')
while True:
    print('\nSelecionar função: \n')
    print('1 - Tratamento de planilha e insercao na tabela de-para.')
    print('2 - Exibir De-Para de valores externos com internos.')
    print('3 - Update de valores internos.')
    print('0 - Fechar sistema\n')

    print('pressione a tecla da opção desejada: ')
    tecla = msvcrt.getch()
    selectOptions = tecla.decode()

    if selectOptions == '1':
        os.system('cls')
        realizar_insert()
        confirmar_retorno_menu()
        
    elif selectOptions == '2':
        os.system('cls')
        print_df = dataframe_export()
        print(print_df)
        confirmar_retorno_menu()

    elif selectOptions == '3': 
        os.system('cls')
        execute_update()
        confirmar_retorno_menu()

    elif selectOptions == '0':
        os.system('cls')
        sys.exit()
        break
    else:
        print("Opção inválida. Tente novamente.")
        msvcrt.getch()
