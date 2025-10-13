import oracledb from 'oracledb';
import dotenv from 'dotenv';

dotenv.config();

let pool;

export async function initDB() {
    try {
        oracledb.initOracleClient({ libDir: process.env.DB_DIR });

        pool = await oracledb.createPool({
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
            connectString: process.env.DB_CONNECT,
            poolMin: 1,
            poolMax: 20,
            poolIncrement: 2,
            queueTimeout: 10000
        });
        console.log('Pool de conexões criado com sucesso.');
    } catch (err) {
        console.error('Erro ao inicializar o pool de conexões:', err);
        process.exit(1);
    }
};

export async function closeDB() {
    try {
        if (pool) {
            await pool.close(10);
            console.log('Pool de conexões fechado com sucesso.');
        }
    } catch (error) {
        console.error('Erro ao fechar o pool de conexões:', error);
    }
};

export async function getConnection() {
    if (!pool) {
        throw new Error('Pool de conexões não foi inicializado. Chame initDB() primeiro.');
    }

    return await pool.getConnection();
};