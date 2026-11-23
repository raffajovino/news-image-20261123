// news-image-20261123 entry (Node 22, standard library only).
// The front page is drawn by draw.py (Pillow) into entry.png beside this file;
// this program ships those exact bytes to /output/entry.png.
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const here = dirname(fileURLToPath(import.meta.url));
const bytes = readFileSync(join(here, 'entry.png'));
// The gate caps the artifact at 1 MiB and 1024x1024; refuse to ship an
// oversize file rather than let the grader reject it.
if (bytes.length > 1048576) throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
if (bytes[0] !== 0x89 || bytes[1] !== 0x50) throw new Error('entry.png is not a PNG');
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), bytes);
