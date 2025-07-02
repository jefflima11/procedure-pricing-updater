from src.db.connection import get_connection
from src.services.data_processor import realizar_insert
from src.services.from_to_last_value import dataframe_export
from src.services.update import execute_update
import pandas as pd
import oracledb
import sys
import os

# print()
selectOptions = int(input('\n Selecionar função: \n\n 1 - Tratamento de planilha e insercao na tabela de-para. \n 2 - Exibir De-Para de valores externos com internos. \n 3 - Update de valores internos. \n\n 0 - Fechar sistema \n\n'))

if selectOptions == 1:
    realizar_insert()
elif selectOptions == 2:
    print_df = dataframe_export()
    print(print_df)
elif selectOptions == 3: 
    execute_update()
elif selectOptions == 0:
    os.system('cls')
    sys.exit()
else:
    print('Opção invalida')
    sys.exit()

