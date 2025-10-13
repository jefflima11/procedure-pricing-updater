
import { cleaningDatas } from '../services/dataService.js';
import { insertDePara } from '../models/dataModel.js';
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

        const processedData = await cleaningDatas(data);

        const result = await insertDePara(processedData.procedimentoVerificado);

        res.status(200).send(result);
    } catch(err) {
        next(err);
    }
};
