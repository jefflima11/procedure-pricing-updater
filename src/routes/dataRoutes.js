import { Router } from 'express';
import { processData, unconfProced } from '../controllers/dataController.js';  


const router = Router();

router.get('/process-data', processData);
router.get('/unconf-proced', unconfProced);

export default router;