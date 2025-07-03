import pandas as pd
from src.db.connection import get_connection
import os

def verifica_insercao():
    connect = get_connection()
    cursor = connect.cursor()

    verifica_insercao_sql = """
        SELECT DISTINCT 0 FROM DBAHUMS.DE_PARA_HUMS            
    """

    cursor.execute(verifica_insercao_sql)
    rows = cursor.fetchall()

    if not rows:
        verificado = 0
    else:
        verificado = 1

    cursor.close()
    connect.close()
    return verificado

# print(verifica_insercao())
def realizar_insert():

    if verifica_insercao() == 0:
        df = pd.read_excel('./src/resources/in/tab_med.xlsx')
        df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor'})
        df0 = df0[['tiss','valor']]

        df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
        df0['tiss'] = df0['tiss'].astype(str)

        # Dataframe de valores zerados
        df_zero_values = df0.loc[df0['valor'] == 0.0000, ['tiss','valor']]

        # Dataframe de valore não zerados e que possuem código brasindice
        df_filter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
        df_filter['vl_honorario'] = 0
        df_filter['vl_operacional'] = 0

        dados = df_filter.to_dict(orient='records')

        insert_de_para = """
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

        cursor.executemany(insert_de_para, dados)
        connect.commit()

        cursor.close()
        connect.close()

        print("Tratamento de dados e inserção realizada na tabela de De-Para!")
    else:
        print('Já existe atualização para vigencia atual\n')
        clean_de_para = input('Deseja limpar a tabela de de-para? ')

        if clean_de_para == 's':
            print()
            

            clean_sql = """
                DELETE FROM DBAHUMS.DE_PARA_HUMS WHERE DT_VIGENCIA = TO_DATE(SYSDATE,'DD/MM/YY')
            """
            connect = get_connection()
            cursor = connect.cursor()
            cursor.execute(clean_sql)
            connect.commit()
            cursor.close()
            connect.close()

            os.system('cls')
            print('Limpeza de de-para realizada!')