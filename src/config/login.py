from dotenv import load_dotenv
import getpass
import os
import msvcrt

load_dotenv()

def login():
    user = input("Usuário: ")
    pw = getpass.getpass(prompt="Senha: ")
    dsn = input("String de conexão exemplo(host:port/sid): ")
    
    return user, pw, dsn