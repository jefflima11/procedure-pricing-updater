import pandas as pd

# df = read

def handleZeroValues():
    df = pd.read_csv("./src/resources/log/procedimentos zerados.csv")
    df = pd.DataFrame(df)
    dfNAP = df.loc[df['tiss'] == 'NAO POSSUI BRASINDICE']
    print(dfNAP.count())