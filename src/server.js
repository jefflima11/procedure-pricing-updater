import app from "./app.js";
import dotenv from 'dotenv';
import { initDB } from "./config/db.js";
import { ensureDirs } from "./utils/ensureDirs.js";
import { cleaning } from './utils/cleaningTable.js';

dotenv.config();

const PORT = process.env.PORT || 3006;

await ensureDirs();

app.listen(PORT, async() => {
  await initDB();
  await cleaning();
  console.log(`Server is running on http://localhost:${PORT}`);
});