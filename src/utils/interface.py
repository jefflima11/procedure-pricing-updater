import os
import msvcrt

def confirmar_retorno_menu():

    contador_i = 0
    while contador_i == 0:

        print('\nRetornar ao menu?\n')
        print('1 - (sim)')
        print('2 - (não)\n')

        print('pressione a tecla da opção desejada: ')
        tecla = msvcrt.getch()
        return_i = tecla.decode()

        if return_i == '1':
            contador_i = 1
            os.system('cls')
        elif return_i == '2':
            os.system('cls')
            contador_i = 0
        else:
            os.system('cls')
            print('\nOpção invalida!')