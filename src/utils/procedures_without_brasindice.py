from src.services.from_to_last_value import updatedProcedures
from openpyxl import load_workbook
import datetime
import pandas as pd

def proceduresWithoutBrasindice(df):
    df = df.loc[df['tiss'] == 'NAO POSSUI BRASINDICE', ['tiss', 'codigo_brasindice', 'valor', 'descricao']]

    data = df.to_dict(orient='records')

    now = datetime.datetime.now()
    now_formated = now.strftime('%d%m%Y')

    path = f'./src/resources/out/relatório-medicamentos{now_formated}.xlsx'

    try:
        with pd.ExcelWriter(path, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name='Proced_sem_brasindice', index=False)
    except:
        print('Erro na importação os procedimentos sem brasindice')
