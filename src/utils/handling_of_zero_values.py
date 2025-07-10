import datetime

def handlingOfZeroValues(df):
    
    # Isola o Dataframe de valores zerados
    dfZeroValues = df.loc[(df['valor'] == 0.0000) & (df['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'codigo_brasindice','valor', 'descricao']]
    
    dataFrameZeroValues(dfZeroValues)

def handlingOfZeroValuesMat(df):
    
    # Isola o Dataframe de valores zerados
    dfZeroValues = df.loc[df['valor'] == 0.0000, ['tuss','valor', 'descricao']]
    
    dataFrameZeroValuesMat(dfZeroValues)

def dataFrameZeroValues(dfZeroValues):
    now = datetime.datetime.now()
    now_formated = now.strftime("%d%m%Y")
    dfZeroValues.to_excel(f"./src/resources/out/pendencias-{now_formated}.xlsx", sheet_name='Proced_zerados', index=False)

def dataFrameZeroValuesMat(dfZeroValues):
    now = datetime.datetime.now()
    now_formated = now.strftime("%d%m%Y")
    dfZeroValues.to_excel(f"./src/resources/out/relatório-materiais{now_formated}.xlsx", sheet_name='Proced_zerados', index=False)