import pandas as pd
from src.db.connection import get_connection

df = pd.read_excel('./src/resources/in/tab_med_maio.xlsx')
df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor'})
df0 = df0[['tiss','valor']]

df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.').astype(float)
df0['tiss'] = df0['tiss'].astype(str)

# Dataframe de valores zerados
df_zero_values = df0.loc[df0['valor'] == 0.0000, ['tiss','valor']]

# Dataframe de valore não zerados e que possuem código brasindice
df_filter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
df_filter['vl_honorario'] = 0
df_filter['vl_operacional'] = 0

dados = df_filter.to_dict(orient='records')

insert_sql = """
    insert into dbahums.de_para_hums(
        cd_tiss, 
        dt_vigencia, 
        vl_honorario,
        vl_operacional,
        vl_total,
        sn_ativo,
        nm_usuario)
    values (
        :tiss,
        to_date(sysdate,'dd/mm/yy'),
        :vl_honorario,
        :vl_operacional,
        :valor,
        'S',
        user
    )
"""

connect = get_connection()
cursor = connect.cursor()

cursor.executemany(insert_sql, dados)
connect.commit()

cursor.close()
connect.close()

def insert_realizado():
  print("Tratamento de dados e inserção realizada na tabela DBAHUMS.DE_PARA_HUMS")