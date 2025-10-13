import { promises as fs } from "fs";
import path from "path";

export async function ensureDirs() {
    const dirs = [
        path.resolve('src/temp'),
        path.resolve('src/uploads')
    ];

    for (const dir of dirs) {
        try {
            await fs.access(dir);
            console.log(`Pasta já existe: ${dir}`);
        } catch {
            await fs.mkdir(dir, {recursive: true});
            console.log(`Pasta criada: ${dir}`);
        }
    }

    console.log('Todas as pastas estão garantidas.');
}