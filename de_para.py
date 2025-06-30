import cx_Oracle
from connection_oracle import get_conexao
import pandas as pd

query_sql = """
    SELECT  
        CD_TISS, CD_TAB_FAT, DT_VIGENCIA, VL_HONORARIO, VL_OPERACIONAL, VL_TOTAL, SN_ATIVO, NM_USUARIO
    FROM DBAHUMS.DE_PARA_HUMS
"""

con = get_conexao()
cur = con.cursor()

cur.execute(query_sql)
rows = cur.fetchall() # Pega os dados

columns = [desc[0] for desc in cur.description]

cur.close()
con.close()

df_result = pd.DataFrame(rows, columns=columns)

df_result


