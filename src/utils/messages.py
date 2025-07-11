import os

def terminalCleaning():
    os.system('cls' if os.name == 'nt' else 'clear')

def homeMenu(user):
    terminalCleaning()
    print('Usuario: ', user)
    print('\nSelecionar função: \n')
    print('1 - Tratamento de planilha e insercao na tabela de-para.')
    print('2 - Update de valores internos.\n')
    print('0 - Fechar sistema\n')
    print('pressione a tecla da opção desejada: ')

def chooseSpreadsheetType():
    terminalCleaning()
    print('Por favor informe o tipo da spreadsheet:\n')
    print('1 - Medicamentos')
    print('2 - Materiais\n')
    print('0 - Voltar ao menu.\n')

def confirmChosenOption():
    terminalCleaning()
    print('\nConfirmar inserção de valores de-para?')           
    print('1 - Sim')
    print('0 - Não, retornar ao menu.\n')

def checkCleanlinessFromTo():
    print('Já existe atualização para vigencia atual!\n')
    print('Deseja limpar a tabela de de-para?\n')
    print('1 - Sim.')
    print('2 - Não, retornar ao menu.\n')

def checkTheUpdateType():
    print('Qual tipo de atualização deseja realizar?\n')
    print('1 - Brasindice.')
    print('2 - Simpro.\n')
    print('\n0 - Retornar ao menu.')