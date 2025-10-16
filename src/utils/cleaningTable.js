import { getConnection } from '../config/db.js'

export async function cleaning() {
    const conn = await getConnection();

    try {
        const sql = `
            DELETE FROM DBAHUMS.DE_PARA_HUMS
        `;

        await conn.execute(sql);
        await conn.commit();
        console.log('Tabela temporaria limpa com sucesso!')
    } finally {
        await conn.close();
    }
}

