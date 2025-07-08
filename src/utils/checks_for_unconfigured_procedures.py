from src.db.connection import get_connection
from src.queries.checks_for_unconfigured_procedures_queries import insertProceduresInLogSQL, proceduresUnconfiguredLogSQL, deleteProceduresInLogSQL
import pandas as pd
from openpyxl import load_workbook
import oracledb

def checksForUnconfiguredProcedures(df):
    
    df = df.loc[(df['valor'] != 0) & (df['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'codigo_brasindice','valor', 'descricao']]

    data = df.to_dict(orient='records')

    try:
        con = get_connection()
        cur = con.cursor()
        cur.executemany(insertProceduresInLogSQL, data)
        con.commit()
        print('insert realizado!')
    except oracledb.Error as e:
        print('Erro ao executar insert:')
        print(e)
    finally:
        cur.close()
        con.close()
        print('sessao com banco encerrada!')

    

def exportForUnconfiguredProcedures():
    path = './src/resources/out/dados divergentes maio.xlsx'
    
    # Carrega o arquivo existente
    book = load_workbook(path)

    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(proceduresUnconfiguredLogSQL)
        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        df = pd.DataFrame(rows, columns=columns)
    except oracledb.Error as e:
        print('Error ao realizar consulta a tabela LOG_PROC_NAO_CONFIG_HUMS')
        print(e)
    finally:
        cur.close()
        con.close()
        print('sessao com banco encerrada')

    # Adiciona nova aba sem sobrescrever as existentes
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name="Proced_nao_config", index=False)
    
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute(deleteProceduresInLogSQL)
        print('exclusão realizada')
        con.commit()
    except oracledb.Error as e:
        print('Erro ao realizar limpeza da tabela LOG_PROC_NAO_CONFIG_HUMS')
        print(e)
    finally:
        cur.close()
        con.close()
        print('sessao com banco encerrada')
    
    exit()