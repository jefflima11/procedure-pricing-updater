import { Router } from 'express';
import { processData } from '../controllers/dataController.js';  


const router = Router();

router.get('/process-data', processData);

export default router;