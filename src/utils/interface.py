from src.db.connection import get_connection, user
from src.services.data_processor import confirmInsert
from src.services.update import executeUpdate
import sys
import os
import msvcrt


def menu_inicial():
    if get_connection():
        while True:
            print('Usuario: ', user)
            print('\nSelecionar função: \n')
            print('1 - Tratamento de planilha e insercao na tabela de-para.')
            print('2 - Update de valores internos.\n')
            print('0 - Fechar sistema\n')

            print('pressione a tecla da opção desejada: ')
            selectOptions = msvcrt.getch().decode()

            if selectOptions == '1':
                os.system('cls')
                confirmInsert()
                
            elif selectOptions == '2':
                os.system('cls')
                executeUpdate()

            elif selectOptions == '0':
                os.system('cls')
                sys.exit()
                break
            else:
                print("Opção inválida. Tente novamente.")
                msvcrt.getch()