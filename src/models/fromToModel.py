import oracledb
import src.queries.data_processor_queries as sql

def checkFromTo(con=None):
    try:
        cur = con.cursor()
        cur.execute(sql.checkExistsFromTo)
        rows = cur.fetchall()

        if rows[0][0] == 1:
            return 1
        elif rows[0][0] == 2:
            return 2
        else:
            return 3
    except oracledb.Error as e:
        return (e)

def insertFromTo(dfFilter, typeSpreadsheet, con):
    data = dfFilter.to_dict(orient='records')
    
    if typeSpreadsheet == 0:
        insertFromToSQL = sql.insert_from_to_medSQL
    elif typeSpreadsheet == 1:
        insertFromToSQL = sql.insert_from_to_matSQL

    try:
        cur = con.cursor()
        batch_size = 10000

        total = 0
        for i in range(0, len(data), batch_size):
                chunk = data[i:i+batch_size]
                cur.executemany(insertFromToSQL, chunk)
                total += len(chunk)

        con.commit()

        print(f'Total de {total} registros inseridos na tabela de de-para.')

    except oracledb.Error as e:       
        print(f'Erro ao inserir dados na tabela de de-para: {e}')
