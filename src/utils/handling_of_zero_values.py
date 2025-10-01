import datetime
import streamlit as st

def handling_of_zero_values(df, typeSpreadsheet):
    now = datetime.datetime.now()
    now_formated = now.strftime("%d%m%Y")

    if typeSpreadsheet == 0:
        # Isola o Dataframe de valores zerados
        dfZeroValues = df.loc[(df['valor'] == 0.0000) & (df['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'codigo_brasindice','valor', 'descricao']]
        typeS = "medicamentos"
        
    elif typeSpreadsheet == 1:
        # Isola o Dataframe de valores zerados
        dfZeroValues = df.loc[df['valor'] == 0.0000, ['tuss','valor', 'descricao']]
        typeS = "materiais"

    try:
        dfZeroValues.to_excel(f"./src/resources/out/relatório-{typeS}{now_formated}.xlsx", sheet_name='Proced_zerados', index=False)
        msg = {
            'type': 'S',
            'msg': len(dfZeroValues)
        }
    except Exception as e:
        msg = {
            'type': 'E',
            'msg': f'Erro ao gerar relatório de valores zerados: {str(e)}'
        }
    return msg