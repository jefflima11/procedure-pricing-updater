from dotenv import load_dotenv
import os
import oracledb
import pandas as pd
from src.config.login import login

# Carrega as variaveis do dotenv
load_dotenv()

oracledb.init_oracle_client(lib_dir=os.getenv("LIB_DIR"))

user, pw, dsn = login()

def get_connection():
    return oracledb.connect(user=user, password=pw, dsn=dsn)