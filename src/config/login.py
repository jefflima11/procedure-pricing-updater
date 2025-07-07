from dotenv import load_dotenv
import getpass
import os
import msvcrt

load_dotenv()

def login():
    # user = input("Usuário: ")
    # pw = getpass.getpass(prompt="Senha: ")
    # dsn = input("String de conexão exemplo(host:port/sid): ")
    user = os.getenv('DB_USER')
    pw = os.getenv('DB_PASS')
    dsn = os.getenv('DB_STRING_SML')
    
    return user, pw, dsn