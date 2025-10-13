import app from "./app.js";
import dotenv from 'dotenv';
import { initDB } from "./config/db.js";
import { ensureDirs } from "./utils/ensureDirs.js";

dotenv.config();

const PORT = process.env.PORT || 3006;

await ensureDirs();

app.listen(PORT, async() => {
  await initDB()
  console.log(`Server is running on http://localhost:${PORT}`);
});