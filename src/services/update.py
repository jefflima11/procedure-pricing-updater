from src.db.connection import get_connection
from src.services.from_to_last_value import dataframe_export

def execute_update():
  # Verifica se a tabela de de-para esta vazia
  if dataframe_export().empty:
    print('Não existe atualização na tabela DBAHUMS.DE_PARA_HUMS')
  else:
    df = dataframe_export()
    df_new_value = df.copy()

    df_new_value = df_new_value[['CD_PRO_FAT', 'NEW_VALUE']]
    dados = df_new_value.to_dict(orient='records')

    sql_insert_new_values = """
      INSERT INTO DBAMV.VAL_PRO(
        CD_TAB_FAT,
        CD_PRO_FAT,
        DT_VIGENCIA,
        VL_HONORARIO,
        VL_OPERACIONAL,
        VL_TOTAL,
        SN_ATIVO,
        NM_USUARIO
      ) VALUES (
        1,
        :CD_PRO_FAT,
        TO_DATE(SYSDATE,'DD/MM/YY'),
        0,
        0,
        :NEW_VALUE,
        'S',
        USER
      )
    """
    connect = get_connection()
    cursor = connect.cursor()

    cursor.executemany(sql_insert_new_values, dados)
    connect.commit()

    cursor.close()
    connect.close()    
    print('Valores de produtos atualizados!')