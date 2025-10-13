import multer from 'multer';
import { Router } from 'express';
import XLSX from 'xlsx';
import fs from 'fs';
import path from 'path';

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, './src/uploads');
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});

const upload = multer({
    storage: storage,
    fileFilter: function (req, file, cb) {
        if (file.mimetype === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
            file.mimetype == 'application/vnd.ms-execel') {
                cb(null, true);
            } else {
                cb(new Error('Apenas arquivos Excel são permitidos!'), false);
            }
        }
});

const router = Router();

router.post('/', upload.single('file'), (req, res) => {
    
    try {
        const filePath = req.file.path; 

        const workbook = XLSX.readFile(filePath);
    
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];

        console.log('Lendo dados do arquivo excel');
        const data = XLSX.utils.sheet_to_json(worksheet);

        console.log('Guardando dados tempoararios')
        const tempFilePath = path.join('./src/temp/data.json');

        fs.writeFileSync(tempFilePath, JSON.stringify(data, null, 2));

        console.log('Dados processados e armazenados temporariamente');
        
        res.status(200).send({
            message: 'Arquivo carregado e processado com sucesso!',
            fileName: req.file.originalname
        });

    } catch (err) {
        res.status(500).send({ error: err.message });
    }
});

export default router;