from src.db.connection import get_connection
from src.services.data_processor import realizar_insert
from src.services.from_to_last_value import dataframe_export
from src.services.update import execute_update
import pandas as pd
import oracledb
import sys
import os

contador = 0

while contador == 0:
    selectOptions = int(input('\n Selecionar função: \n\n 1 - Tratamento de planilha e insercao na tabela de-para. \n 2 - Exibir De-Para de valores externos com internos. \n 3 - Update de valores internos. \n\n 0 - Fechar sistema \n\n'))
    
    if selectOptions == 1:
        realizar_insert()
    elif selectOptions == 2:
        os.system('cls')
        print_df = dataframe_export()
        print(print_df)
        contador_i = 0

        while contador_i == 0:
            return_i = input('\n\n Retornar ao menu? ')
            if return_i == 's':
                contador_i = 1
                os.system('cls')
            elif return_i == 'n':
                os.system('cls')
                contador_i = 0
            else:
                os.system('cls')
                print(print_df)
                print('\n Opção invalida!')
        

    elif selectOptions == 3: 
        execute_update()
    elif selectOptions == 0:
        os.system('cls')
        sys.exit()
        contador+=1
    else:
        print('Opção invalida')
        sys.exit()
