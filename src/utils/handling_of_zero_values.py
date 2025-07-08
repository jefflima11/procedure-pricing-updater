
def handlingOfZeroValues(df):
    
    # Isola o Dataframe de valores zerados
    dfZeroValues = df.loc[df['valor'] == 0.0000, ['tiss', 'codigo_brasindice','valor', 'descricao']]
    
    dataFrameZeroValues(dfZeroValues)

def dataFrameZeroValues(dfZeroValues):
    dfZeroValues.to_excel("./src/resources/out/dados divergentes maio.xlsx", sheet_name='Proced_zerados', index=False)