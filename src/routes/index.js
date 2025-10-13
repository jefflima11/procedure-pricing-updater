import { Router } from 'express';
import uploadRoutes from "./uploadRoutes.js";
import dataRoutes from "./dataRoutes.js";


const router = Router();

router.get('/', (req, res) => {
  res.send('Hello World!');
});

router.use('/upload', uploadRoutes);

router.use('/data', dataRoutes);


export default router;
