import { promises as fs } from "fs";
import path from "path";

export async function ensureDirs() {
    const dirs = [
        path.resolve('temp'),
        path.resolve('uploads')
    ];

    for (const dir of dirs) {
        try {
            await fs.access(dir);
        } catch {
            await fs.mkdir(dir, {recursive: true});
        }
    }

    console.log('Todas as pastas estão garantidas.');
}