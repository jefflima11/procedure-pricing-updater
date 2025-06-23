# %%
from dotenv import load_dotenv
import os
import cx_Oracle
import pandas as pd

# Carrega as variaveis do dotenv
load_dotenv()

# Vincula as variaveis de ambiente
usuario = os.getenv("DB_USER")
senha = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
porta = os.getenv("DB_PORT")
servico = os.getenv("DB_SERVICE")

dsn = cx_Oracle.makedsn(host, porta, service_name=servico)

con = cx_Oracle.connect(user=usuario, password=senha, dsn=dsn)

def get_conexao():
    return cx_Oracle.connect(user=usuario, password=senha, dsn=dsn)


