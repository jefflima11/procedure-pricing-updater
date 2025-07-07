from src.db.connection import get_connection, user
from src.services.data_processor import confirmInsert
from src.services.from_to_last_value import dataframe_export, dataframe_view
from src.services.update import execute_update
import sys
import os
import msvcrt


def menu_inicial():
    if get_connection():
        while True:
            print('Usuario: ', user)
            print('\nSelecionar função: \n')
            print('1 - Tratamento de planilha e insercao na tabela de-para.')
            print('2 - Exibir De-Para de valores externos com internos.')
            print('3 - Update de valores internos.\n')
            print('0 - Fechar sistema\n')

            print('pressione a tecla da opção desejada: ')
            selectOptions = msvcrt.getch().decode()

            if selectOptions == '1':
                os.system('cls')
                confirmInsert()
                
            elif selectOptions == '2':
                os.system('cls')
                dataframe_view(dataframe_export())

            elif selectOptions == '3': 
                os.system('cls')
                execute_update()

            elif selectOptions == '0':
                os.system('cls')
                sys.exit()
                break
            else:
                print("Opção inválida. Tente novamente.")
                msvcrt.getch()
        

# def confirmar_retorno_menu():

    # contador_i = 0
    # while contador_i == 0:

    #     print('\nRetornar ao menu?\n')
    #     print('1 - (sim)')
    #     print('2 - (não)\n')

    #     print('pressione a tecla da opção desejada: ')
    #     tecla = msvcrt.getch()
    #     return_i = tecla.decode()

    #     if return_i == '1':
    #         contador_i = 1
    #         os.system('cls')
    #     elif return_i == '2':
    #         os.system('cls')
    #         contador_i = 0
    #     else:
    #         os.system('cls')
    #         print('\nOpção invalida!')