import os
import glob
import msvcrt
import pandas as pd

def importSpreadsheet(typeSpreadsheet):
    inputDir = os.path.join("src", "resources", "in")
    spreadsheets = glob.glob(os.path.join(inputDir, "*.xlsx"))

    # filtra por tipo no nome do arquivo
    typeFiltered = [p for p in spreadsheets if typeSpreadsheet.lower() in p.lower()]

    if not typeFiltered:
        print("Nenhuma planilha encontrada para esse tipo.")
        return None

    def loadSpreadsheetOptions():
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Selecione a planilha para carregar:\n")

            for i, spreadsheet in enumerate(typeFiltered):
                nome = os.path.basename(spreadsheet)
                print(f"{i+1} - {nome}")
            print('\n0 - Voltar ao menu.')

            chosenWorksheet = msvcrt.getch().decode()
            if chosenWorksheet == '0':
                return None

            try:
                idx = int(chosenWorksheet) - 1
                if 0 <= idx < len(typeFiltered):
                    return idx
                else:
                    raise ValueError
            except:
                print("\nOpção inválida. Pressione qualquer tecla para tentar novamente...")
                msvcrt.getch()

    idx = loadSpreadsheetOptions()
    if idx is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        return None

    chosenFile = typeFiltered[idx] 
    print(f"\nCarregando: {chosenFile}")

    try:
        df = pd.read_excel(chosenFile, sheet_name="Plan1")
        return df
    except Exception as e:
        print(f"Erro ao ler planilha: {e}")
        return None

