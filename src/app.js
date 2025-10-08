import express from 'express';
import routes from './routes/index.js';

const app = express();

app.use('/api', routes);
app.use(express.json());

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});

export default app;

