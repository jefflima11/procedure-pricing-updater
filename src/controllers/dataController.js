
import { cleaningDatas } from '../services/dataService.js';
import { insertDePara, unconfiguredProcedures } from '../models/dataModel.js';
import fs from 'fs';  

export async function processData(req, res, next) {
    try {
        let rawData

        try {
            rawData = fs.readFileSync('./src/temp/data.json', 'utf-8');
        } catch {
            return res.status(201).send('Não há dados a serem processados!');
        }

        const data = JSON.parse(rawData);

        // Tratamento inicial
        const processedData = await cleaningDatas(data);
        
        try {
            // Inserção dos procedimentos com valor > 0 na tabela de-para
            const r = await insertDePara(processedData.procedimentoVerificado);

        } catch(err) {
            return err 
        }

        res.status(200).send();
    } catch(err) {
        next(err);
    }
};


export async function unconfProced(req, res, next) {
    try {
        const r = await unconfiguredProcedures();
        res.status(200).send(r)
    } catch(err) {
        next(err);
    }
}