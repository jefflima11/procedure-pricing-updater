import os
import oracledb
import pandas as pd
from src.config.login import login

oracledb.init_oracle_client(lib_dir=os.getenv("LIB_DIR"))

user, pw, dsn = login()

def get_connection():

    try:
        conn = oracledb.connect(user=user, password=pw, dsn=dsn)
        return conn
    except oracledb.DatabaseError as e:
        os.system('cls')
        error, = e.args
        print(f"\nErro de conexao: {error.message}")
        return None