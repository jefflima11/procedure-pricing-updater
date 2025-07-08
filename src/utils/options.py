from src.utils.handling_of_zero_values import handlingOfZeroValues
import os
import msvcrt

# def opcaoDeValoresZerados(df):
#     os.system('cls')
#     print("\nExportar valores zerados?")
#     print("1 - Sim.")
#     print("2 - Não.")

#     options = msvcrt.getch().decode()
#     if options == '1':
#         handlingOfZeroValues(df)
        
#     elif options == '2':
#         os.system('cls')
#     else:
#         opcaoDeValoresZerados()

def confirmChosenOption(dfFilter):
        os.system('cls')
        print('Amostra de valores tratados:\n')
        print(dfFilter.head())

        print('\nConfirmar inserção de valores de-para?')           
        print('1 - Sim')
        print('2 - Não, retornar ao menu.\n')

        insertOption = msvcrt.getch().decode()
        if insertOption == '1':
            os.system('cls')

            from src.services.data_processor import insertFromTo
            insertFromTo(dfFilter)
        elif insertOption == '2':
            os.system('cls')
        else:
            confirmChosenOption()