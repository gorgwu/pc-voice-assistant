import express from 'express';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const port = 3001;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootDir = path.resolve(__dirname, '..');

const configDir = path.join(rootDir, 'voice-assistant', 'configs');
const documentsDir = path.join(rootDir, 'voice-assistant', 'documents');
const distDir = path.join(__dirname, 'dist');

app.use(express.json());

async function ensureConfigDir() {
    await fs.mkdir(configDir, { recursive: true });
}

function safeFileName(name) {
    return name
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '_')
        .replace(/^_+|_+$/g, '') + '.json';
}

//
// CONFIGS
//

app.get('/api/configs', async (_, res) => {
    try {
        await ensureConfigDir();

        const files = (await fs.readdir(configDir))
            .filter((f) => f.endsWith('.json'))
            .sort();

        const configs = await Promise.all(
            files.map(async (file) => {
                const raw = await fs.readFile(
                    path.join(configDir, file),
                    'utf8'
                );

                const json = JSON.parse(raw);

                return {
                    file_name: file,
                    name: json.name ?? file.replace('.json', ''),
                    bot: json.bot ?? '',
                    pdf: json.pdf ?? '',
                    voice_accent: json.voice_accent ?? 'com',
                };
            })
        );

        res.json(configs);
    } catch (err) {
        console.error(err);

        res.status(500).json({
            error: 'Failed to load configurations.',
        });
    }
});

app.get('/api/configs/:name', async (req, res) => {
    try {
        const fileName = req.params.name.endsWith('.json')
            ? req.params.name
            : `${req.params.name}.json`;

        const raw = await fs.readFile(
            path.join(configDir, fileName),
            'utf8'
        );

        const json = JSON.parse(raw);

        res.json({
            file_name: fileName,
            name: json.name ?? fileName.replace('.json', ''),
            bot: json.bot ?? '',
            pdf: json.pdf ?? '',
            voice_accent: json.voice_accent ?? 'com',
        });
    } catch {
        res.status(404).json({
            error: 'Configuration not found.',
        });
    }
});

app.get('/api/documents', async (_, res) => {
    try {
        const files = await fs.readdir(documentsDir);

        res.json(
            files
                .filter((f) => f.toLowerCase().endsWith('.pdf'))
                .sort()
        );
    } catch {
        res.json([]);
    }
});

app.post('/api/configs', async (req, res) => {
    try {
        const {
            name,
            bot,
            pdf,
            voice_accent,
        } = req.body;

        if (!name || !bot || !voice_accent) {
            return res.status(400).json({
                error: 'Missing required fields.',
            });
        }

        await ensureConfigDir();

        const fileName = safeFileName(name);

        const payload = {
            name,
            bot,
            pdf: pdf || '',
            voice_accent,
        };

        await fs.writeFile(
            path.join(configDir, fileName),
            JSON.stringify(payload, null, 4),
            'utf8'
        );

        res.status(201).json({
            file_name: fileName,
            ...payload,
        });
    } catch (err) {
        console.error(err);

        res.status(500).json({
            error: 'Failed to create configuration.',
        });
    }
});

//
// UPDATE CONFIGURATION
//

app.put('/api/configs/:name', async (req, res) => {
    try {
        const originalFile = req.params.name.endsWith('.json')
            ? req.params.name
            : `${req.params.name}.json`;

        const {
            name,
            bot,
            pdf,
            voice_accent,
        } = req.body;

        if (!name || !bot || !voice_accent) {
            return res.status(400).json({
                error: 'Missing required fields.',
            });
        }

        const newFile = safeFileName(name);

        const oldPath = path.join(configDir, originalFile);
        const newPath = path.join(configDir, newFile);

        const payload = {
            name,
            bot,
            pdf: pdf || '',
            voice_accent,
        };

        if (originalFile !== newFile) {
            try {
                await fs.unlink(newPath);
            } catch {}

            await fs.rename(oldPath, newPath);
        }

        await fs.writeFile(
            newPath,
            JSON.stringify(payload, null, 4),
            'utf8'
        );

        res.json({
            file_name: newFile,
            ...payload,
        });
    } catch (err) {
        console.error(err);

        res.status(500).json({
            error: 'Failed to update configuration.',
        });
    }
});

//
// DELETE CONFIGURATION
//

app.delete('/api/configs/:name', async (req, res) => {
    try {
        const fileName = req.params.name.endsWith('.json')
            ? req.params.name
            : `${req.params.name}.json`;

        await fs.unlink(
            path.join(configDir, fileName)
        );

        res.json({
            deleted: fileName,
        });
    } catch {
        res.status(404).json({
            error: 'Configuration not found.',
        });
    }
});

//
// FRONTEND
//

app.use(express.static(distDir));

app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api')) {
        return next();
    }

    res.sendFile(
        path.join(distDir, 'index.html')
    );
});

app.listen(port, () => {
    console.log(
        `Config generator API listening on http://localhost:${port}`
    );
});