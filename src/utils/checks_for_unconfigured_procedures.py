from src.queries import checks_for_unconfigured_procedures_queries
from openpyxl import load_workbook
import pandas as pd
import oracledb
import datetime
import streamlit as st  

def checks_for_unconfigured_procedures(df, typeSpreadsheet, con):
    if typeSpreadsheet == 0:
        df = df.loc[(df['valor'] != 0) & (df['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'codigo_brasindice','valor', 'descricao']]
        insertProceduresInLogSQL = checks_for_unconfigured_procedures_queries.insert_procedures_in_log_medSQL
    elif typeSpreadsheet == 1:
        df = df.query("valor > 0.000")
        insertProceduresInLogSQL = checks_for_unconfigured_procedures_queries.insertProceduresInLogMatSQL
    
    data = df.to_dict(orient='records')

    try:
        cur = con.cursor()
        batch_size = 10000

        total = 0

        for i in range(0, len(data), batch_size):
            chunk =data[i:i+batch_size]
            cur.executemany(insertProceduresInLogSQL, chunk)
            total += len(chunk)

        con.commit()
        msg = {
            'type': 'S',
            'msg': len(data)
        }
    except oracledb.Error as e:
        msg = {
            'type': 'E',
            'msg': f'Erro ao inserir procedimentos não configurados no log: {e}'
        }
    return msg


def exportForUnconfiguredProcedures(typeSpreadsheet, con):
    now = datetime.datetime.now()
    now_formated = now.strftime("%d%m%Y")

    if typeSpreadsheet == 0:
        procedures_unconfigured_logSQL = checks_for_unconfigured_procedures_queries.procedures_unconfigured_log_medSQL
        typeS = "medicamentos"
    elif typeSpreadsheet == 1:
        procedures_unconfigured_logSQL = checks_for_unconfigured_procedures_queries.procedures_unconfigured_log_matSQL
        typeS = "materiais"
    path = f'./src/resources/out/relatório-{typeS}{now_formated}.xlsx'
    
    # Carrega o arquivo existente
    book = load_workbook(path)

    # Verifica em consulta os procedimentos que não tem condiguração na M_BRASIND
    try:
        cur = con.cursor()
        cur.execute(procedures_unconfigured_logSQL)
        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        msg = {
            'type': 'S',
            'msg': len(df)
        }
    except oracledb.Error as e:
        msg = {
            'type': 'E',
            'msg': f'Erro ao realizar consulta de procedimentos não configurados: {e}'
        }
    return msg

    # Adiciona nova aba na planilha de pendencias sem sobrescrever as existentes
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name="Proced_nao_config", index=False)
    
    # Limpa a tabela de log de procedimentos
    try:
        cur = con.cursor()
        cur.execute(checks_for_unconfigured_procedures_queries.delete_procedures_in_logSQL)
        con.commit()
    except oracledb.Error as e:
        msg = {
            'type': 'E',
            'msg': f'Erro ao limpar tabela de log de procedimentos: {e}'
        }
    return msg