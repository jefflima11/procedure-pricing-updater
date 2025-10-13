import { getConnection } from '../config/db.js';

export async function insertDePara(dataList) {
    const conn = await getConnection();

    try {
            
        dataList.forEach(item => {
            const sql = `
                INSERT INTO DBAHUMS.DE_PARA_HUMS (
                    DT_VIGENCIA, 
                    VL_HONORARIO, 
                    VL_OPERACIONAL,
                    VL_TOTAL,
                    SN_ATIVO,
                    NM_USUARIO,
                    CD_TUSS
                ) VALUES (
                    SYSDATE, 
                    0, 
                    0,
                    :valor,
                    'S',
                    USER,
                    :tuss
                )`;
            
            conn.execute(
                sql, 
                { tuss: item.CodigoTuss, valor: item.Preco },
                { autoCommit: true},
                (err, result) => {
                    if (err) {
                        console.log('Erro ao inserir:', err);
                        return;
                    }
                })
        })
        return dataList;
    } finally {
        await conn.close();
    }
}