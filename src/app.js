import express from 'express';
import routes from './routes/index.js';
import cors from 'cors';

const app = express();

app.use(cors());
app.use('/api', routes);
app.use(express.json());

export default app;