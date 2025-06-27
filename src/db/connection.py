# %%
from dotenv import load_dotenv
import os
import oracledb
import pandas as pd

# Carrega as variaveis do dotenv
load_dotenv()

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_12")

# Vincula as variaveis de ambiente
user = os.getenv("DB_USER")
pw = os.getenv("DB_PASS")
dsn = os.getenv("DB_STRING")

con = oracledb.connect(user=user, password=pw, dsn=dsn)

def get_connection():
    return oracledb.connect(user=user, password=pw, dsn=dsn)