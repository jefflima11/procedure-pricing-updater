from src.db.connection import get_connection
from src.services.data_processor import insert_realizado
from src.services.from_to_last_value import imprimir_dataframe, dataframe_export
# from src.services.update import imprimir_mensagem
import pandas as pd
import oracledb
import sys
import os

# print()
selectOptions = int(input('\n Selecionar função: \n\n 1 - Tratamento de planilha e insercao na tabela de-para. \n 2 - Exibir De-Para de valores externos com internos. \n 3 - Update de valores internos. \n\n 0 - Fechar sistema \n\n'))

if selectOptions == 1:
    teste = insert_realizado()
    teste()
elif selectOptions == 2:
    df = dataframe_export()
    print(df)
    print('ok!')
elif selectOptions == 3: 
    # imprimir_mensagem()
    print('teste')
elif selectOptions == 0:
    os.system('cls')
    sys.exit()
else:
    print('Opção invalida')
    sys.exit()

