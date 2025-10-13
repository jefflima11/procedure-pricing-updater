
import { cleaningDatas } from '../services/dataService.js';
import { insertDePara } from '../models/dataModel.js';
import fs from 'fs';  

export async function processData(req, res, next) {
    try {
        const rawData = fs.readFileSync('./src/temp/data.json');
        const data = JSON.parse(rawData);

        const processedData = await cleaningDatas(data);

        const result = await insertDePara(processedData.procedimentoVerificado);

        res.status(200).send(result);
    } catch(err) {
        next(err);
    }
};
