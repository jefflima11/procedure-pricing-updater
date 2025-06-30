from connection_oracle import get_conexao
import pandas as pd
import os

# file_name = input("Digite o nome do arquivo Excel (com extensão): ")

# file_path = os.path.join("src", "data", "in", file_name)

file_path = os.path.join("src","data", "in", "tab_med_maio.xlsx")

if not os.path.isfile(file_path):
    print("Arquivo não encontrado!")
    raise SystemExit()

try:
    df = pd.read_excel(file_path, sheet_name="Plan1")
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    df = None
    raise SystemExit()

expected_cols = ["Código", "Preço Máximo Intercâmbio Nacional"]
if not all(col in df.columns for col in expected_cols):
    print("As colunas esperadas não foram encontradas na planilha.")
    raise SystemExit()

# df.dropna(inplace=True)
df.rename(columns={
    "Cod TISS Brasindice": "cod_tiss",
    "Preço Máximo Intercâmbio Nacional": "valor"
}, inplace=True)

df.to_excel("./src/data/out/teste.xlsx", sheet_name="Plan1", index=False)

result = df[["cod_tiss", "valor"]][df["cod_tiss"] == "0000025776"]

print(result)

print(df.columns)

resultado = df[df["cod_tiss"] == "0000025776"][["cod_tiss", "valor"]]
print(resultado)

df = df[["cod_tiss", "valor"]]
df["valor"] = df["valor"].str.replace(",", ".", regex=False)
df["vl_honorario"] = 0
df["vl_operacional"] = 0
df["dt_vigencia"] = "2025-06-18"

df["vl_honorario"] = pd.to_numeric(df["vl_honorario"], errors="coerce").fillna(0)
df["vl_operacional"] = pd.to_numeric(df["vl_operacional"], errors="coerce").fillna(0)
df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)

df= df[df["cod_tiss"].str.upper() != "NAO POSSUI BRASINDICE"]

vigencia_date = input("Informe a data no formato (dia/mês/ano):")

sql = """
    INSERT INTO DBAHUMS.DE_PARA_HUMS (
        CD_TISS, CD_TAB_FAT, DT_VIGENCIA, VL_HONORARIO, VL_OPERACIONAL, VL_TOTAL, SN_ATIVO, NM_USUARIO
    )
    VALUES (
        :cd_tiss, :cd_tab_fat, to_date(:dt_vigencia, 'dd/mm/yyyy'), :vl_honorario, :vl_operacional, :vl_total, :sn_ativo, USER
    )
"""

con = get_conexao()
cur = con.cursor()

dados = [
    {
        "cd_tiss": str(row["cod_tiss"]),
        "cd_tab_fat": 1,
        "dt_vigencia": vigencia_date,
        "vl_honorario": float(row["vl_honorario"]),
        "vl_operacional": float(row["vl_operacional"]),
        "vl_total": float(row["valor"]),
        "sn_ativo": "S"
    }
    for idx, row in df.iterrows()
]

cur.executemany(sql, dados)
con.commit()
cur.close()
con.close()


