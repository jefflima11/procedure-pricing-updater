from src.db.connection import get_connection
import glob
import pandas as pd
import os
import msvcrt
import sys



def realizar_insert(df_filter=None):

    def verifica_insercao():
        connect = get_connection()
        cursor = connect.cursor()

        verifica_insercao_sql = """
            SELECT DISTINCT 0 FROM DBAHUMS.DE_PARA_HUMS            
        """

        cursor.execute(verifica_insercao_sql)
        rows = cursor.fetchall()

        if not rows:
            verificado = 0
        else:
            verificado = 1

        cursor.close()
        connect.close()
        return verificado
    
    if verifica_insercao() == 0:
        os.system('cls')
        print('\n1 - Tratar planilha.')
        print('0 - Sair do programa.\n')

        # print('Pressione a tecla da opção desejada:')
        tecla = msvcrt.getch().decode()

        if tecla == '1':
            tipo_da_planilha()
            
        elif tecla == '0':
            sys.exit()
    else:
        def verifica_limpeza_de_para(msg=None):
            print('Já existe atualização para vigencia atual!\n')
            print('Deseja limpar a tabela de de-para?\n')
            print('1 - Sim.')
            print('2 - Não, retornar ao menu.\n')

            clean_de_para = msvcrt.getch().decode()
            if clean_de_para == '1':
                
                clean_sql = """
                    DELETE FROM DBAHUMS.DE_PARA_HUMS WHERE DT_VIGENCIA = TO_DATE(SYSDATE,'DD/MM/YY')
                """
                connect = get_connection()
                cursor = connect.cursor()
                cursor.execute(clean_sql)
                connect.commit()
                cursor.close()
                connect.close()

                os.system('cls')
                print('Limpeza de de-para realizada!')
            elif clean_de_para == '2':
                os.system('cls')
                # print(msg)
            else:
                os.system('cls')
                print('Opção inválida. Tente novamente!')
                verifica_limpeza_de_para()

        verifica_limpeza_de_para()

    verifica_insercao()

def tipo_da_planilha():
        os.system('cls')
        print('Por favor informe o tipo da planilha:\n')
        print('1 - Medicamentos')
        print('2 - Materiais\n')

        tpPlanilhaOption = msvcrt.getch().decode()

        if tpPlanilhaOption == '1':
            med()
            sys.exit()
        elif tpPlanilhaOption =='2':
            print('tab')
            sys.exit()
        else:
            print('Parametro incorreto informado, tente novamente!')
            tipo_de_planilha()

def med():
    input_dir = os.path.join("src", "resources", "in")

    planilhas = glob.glob(os.path.join(input_dir, "*.xlsx"))

    if not planilhas:
        print("Nenhuma planilha encontrada.")
        exit()
    
    os.system('cls')
    print("Selecione a planilha para carregar:\n")
    for i, planilha in enumerate(planilhas):
        nome = os.path.basename(planilha)
        print(f"{i+1} - {nome}")
    print('')

    tabOption = msvcrt.getch().decode()

    try:
        idx = int(tabOption) - 1
        if idx < 0 or idx >= len(planilhas):
            raise IndexError
    except:
        print("Opção inválida.")
        exit()
    
    arquivo_escolhido = planilhas[idx]
    print(f"\nCarregando: {arquivo_escolhido}")
    
    df = pd.read_excel(arquivo_escolhido, sheet_name="Plan1")
    df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor'})
    df0 = df0[['tiss','valor']]

    df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    df0['tiss'] = df0['tiss'].astype(str)

    # Dataframe de valores zerados
    df_zero_values = df0.loc[df0['valor'] == 0.0000, ['tiss','valor']]

    # Dataframe de valore não zerados e que possuem código brasindice
    df_filter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    df_filter['vl_honorario'] = 0
    df_filter['vl_operacional'] = 0

    os.system('cls')
    print('Amostra de valores tratados:\n')
    print(df_filter.head())

    print('\nConfirmar inserção de valores de-para?')           
    print('1 - Sim')
    print('2 - Não\n')

    insertOption = msvcrt.getch().decode()
    if insertOption == '1':
        inserir_de_para(df_filter)
    elif insertOption == '2':
        os.system('cls')
        print('')

def mat():
    print()
    # input_dir = os.path.join("src", "resources", "in")

    # planilhas = glob.glob(os.path.join(input_dir, "*.xlsx"))

    # if not planilhas:
    #     print("Nenhuma planilha encontrada.")
    #     exit()
    
    # print("Selecione a planilha para carregar:\n")
    # for i, planilha in enumerate(planilhas):
    #     nome = os.path.basename(planilha)
    #     print(f"{i+1} - {nome}")

    # tabOption = msvcrt.getch().decode()

    # try:
    #     idx = int(tabOption) - 1
    #     if idx < 0 or idx >= len(planilhas):
    #         raise IndexError
    # except:
    #     print("Opção inválida.")
    #     exit()
    
    # arquivo_escolhido = planilhas[idx]
    # print(f"\nCarregando: {arquivo_escolhido}")
    
    # df = pd.read_excel(arquivo_escolhido, sheet_name="Plan1")
    # df0 = df.rename(columns={'Cod TISS Brasindice': 'tiss', 'Preço Máximo Intercâmbio Nacional': 'valor'})
    # df0 = df0[['tiss','valor']]

    # df0['valor'] = df0['valor'].astype(str).str.strip().str.replace(',','.', regex=False).astype(float)
    # df0['tiss'] = df0['tiss'].astype(str)

    # # Dataframe de valores zerados
    # df_zero_values = df0.loc[df0['valor'] == 0.0000, ['tiss','valor']]

    # # Dataframe de valore não zerados e que possuem código brasindice
    # df_filter = df0.loc[(df0['valor'] != 0) & (df0['tiss'] != 'NAO POSSUI BRASINDICE'), ['tiss', 'valor']]
    # df_filter['vl_honorario'] = 0
    # df_filter['vl_operacional'] = 0

    # os.system('cls')
    # print('Amostra de valores tratados:\n')
    # print(df_filter.head())

    # print('\nConfirmar inserção de valores de-para?')           
    # print('1 - Sim')
    # print('2 - Não\n')
    # print('Pressione a tecla da opção desejada:')
    # insertOption = msvcrt.getch().decode()
    # if insertOption == '1':
    #     inserir_de_para(df_filter)
    # elif insertOption == '2':
    #     os.system('cls')
    #     print('')

def inserir_de_para(df_filter):
        dados = df_filter.to_dict(orient='records')

        insert_de_para = """
            insert into dbahums.de_para_hums(
                cd_tiss, 
                dt_vigencia, 
                vl_honorario,
                vl_operacional,
                vl_total,
                sn_ativo,
                nm_usuario)
            values (
                :tiss,
                to_date(sysdate,'dd/mm/yy'),
                :vl_honorario,
                :vl_operacional,
                :valor,
                'S',
                user
            )
        """

        connect = get_connection()
        cursor = connect.cursor()

        cursor.executemany(insert_de_para, dados)
        connect.commit()

        cursor.close()
        connect.close()

        print("Tratamento de dados e inserção realizada na tabela de De-Para!")