from src.db.connection import get_connection
import pandas as pd
import oracledb

connect = get_connection()

cursor = connect.cursor()

sql = """
    select 
        cd_atendimento,
        cd_paciente
    from 
        dbamv.atendime 
    where to_char(dt_atendimento,'dd/mm/yyyy') = to_char(sysdate,'dd/mm/yyyy') 
    and tp_atendimento = :tp_atendimento
"""

cursor.execute(sql, tp_atendimento = 'I')

if connect.is_healthy():
    rows = cursor.fetchall()

    colunas = []

    for coluna in cursor.description:
        colunas.append(coluna[0])

    print(colunas)
    # df = pd.DataFrame(rows, columns=columns)

    # print(df)
else:
    print("Conexão inacessivel. Por favor chque sua conexão com o banco e configurações.")

cursor.close()
connect.close()