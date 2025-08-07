import oracledb

def cleaner(con=None):
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM DBAHUMS.DE_PARA_HUMS")
        con.commit()
        msg = {
            'type': "S",
            'msg': "Logs de de-para limpos com sucesso!"
        }
    except oracledb.Error as e:
        msg = {
            'type': "E",
            'msg': f"Erro ao limpar logs de de-para: {e}"
        }
    return msg