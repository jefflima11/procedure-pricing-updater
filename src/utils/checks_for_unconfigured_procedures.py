from src.db.connection import get_connection
from src.queries.checks_for_unconfigured_procedures_queries import insertProceduresInLogMedSQL, proceduresUnconfiguredLogMedSQL, deleteProceduresInLogSQL, insertProceduresInLogMatSQL, proceduresUnconfiguredLogMatSQL
import pandas as pd
from openpyxl import load_workbook
import oracledb
import datetime

def checksForUnconfiguredProcedures(df, typeSpreadsheet, con):
    if typeSpreadsheet == 0:
        df = df.loc[(df['valor'] != 0) & (df['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'codigo_brasindice','valor', 'descricao']]
        insertProceduresInLogSQL = insertProceduresInLogMedSQL

    elif typeSpreadsheet == 1:
        df = df.loc[df['valor'] != 0, ['tuss','valor', 'descricao']]
        insertProceduresInLogSQL = insertProceduresInLogMatSQL

    data = df.to_dict(orient='records')
    
    try:
        cur = con.cursor()
        cur.executemany(insertProceduresInLogSQL, data)
        con.commit()
        msg = f"Procedimentos não configurados inseridos no log com sucesso. Total de registros: {len(data)}"
        return msg
    except oracledb.Error as e:
        erro = f"Erro ao inserir procedimentos no log: {e}"
        return erro

def exportForUnconfiguredProcedures(typeSpreadsheet, con):
    now = datetime.datetime.now()
    now_formated = now.strftime("%d%m%Y")

    if typeSpreadsheet == 0:
        proceduresUnconfiguredLogSQL = proceduresUnconfiguredLogMedSQL
        typeS = "medicamentos"
    elif typeSpreadsheet == 1:
        proceduresUnconfiguredLogSQL = proceduresUnconfiguredLogMatSQL
        typeS = "materiais"
    path = f'./src/resources/out/relatório-{typeS}{now_formated}.xlsx'
    
    # Carrega o arquivo existente
    book = load_workbook(path)

    # Verifica em consulta os procedimentos que não tem condiguração na M_BRASIND
    try:
        cur = con.cursor()
        cur.execute(proceduresUnconfiguredLogSQL)
        rows = cur.fetchall()
        columns = [col[0] for col in cur.description]
        df = pd.DataFrame(rows, columns=columns)
    except oracledb.Error as e:
        print('Error ao realizar consulta a tabela LOG_PROC_NAO_CONFIG_HUMS')
        print(e)
    # finally:
    #     cur.close()
    #     con.close()

    # Adiciona nova aba na planilha de pendencias sem sobrescrever as existentes
    with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name="Proced_nao_config", index=False)
    
    # Limpa a tabela de log de procedimentos
    try:
        cur = con.cursor()
        cur.execute(deleteProceduresInLogSQL)
        con.commit()
    except oracledb.Error as e:
        print('Erro ao realizar limpeza da tabela LOG_PROC_NAO_CONFIG_HUMS:')
        print(e)
    # finally:
    #     cur.close()
    #     con.close()
