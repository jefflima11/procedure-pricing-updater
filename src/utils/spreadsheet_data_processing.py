import pandas as pd
import os
import msvcrt
import glob

def importSpreadsheet():
    inputDir = os.path.join("src", "resources", "in")

    spreadsheets = glob.glob(os.path.join(inputDir, "*.xlsx"))

    if not spreadsheets:
        print("Nenhuma planilha encontrada.")
        exit()
    
    def loadSpreadsheetOptions():
        os.system('cls')
        print("Selecione a planilha para carregar:\n")
        for i, spreadsheet in enumerate(spreadsheets):
            nome = os.path.basename(spreadsheet)
            print(f"{i+1} - {nome}")
        

        chosenWorksheet = msvcrt.getch().decode()

        try:
            idx = int(chosenWorksheet) - 1
            if idx < 0 or idx >= len(spreadsheets):
                raise IndexError  
        except:
            loadSpreadsheetOptions()
        return idx
    
    idx = loadSpreadsheetOptions()    

    chosenFile = spreadsheets[idx]
    print(f"\nCarregando: {chosenFile}")
    
    # Leitura do arquivo excel
    df = pd.read_excel(chosenFile, sheet_name="Plan1")

    return df    
