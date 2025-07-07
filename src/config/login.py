from dotenv import load_dotenv
import getpass
import os
import msvcrt

load_dotenv()

def login():
    # user = input("Usuário: ")
    # pw = getpass.getpass(prompt='Senha: ')

    print('\nEscolha o banco que deseja se conectar: ')
    print('1 - (sml)')
    print('2 - (prd)\n')

    tecla = msvcrt.getch().decode()

    if tecla == '1':
        dsn = os.getenv('DB_STRING_SML')
        user = os.getenv('DB_USER')
        pw = os.getenv('DB_PASS')

    elif tecla == '2':
        # dsn = os.getenv('DB_STRING_PRD')
        print()
    else:
        os.system('cls')
        print("\nOpção de banco inválida!")
        print("Tente novamente!\n")
        return login()  # chama de novo

    return user, pw, dsn