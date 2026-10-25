import { readdir, stat, rm, access } from 'node:fs/promises';
import { join } from 'node:path';
// Preserve the supplied file locally, but do not publish the unoptimized master.
await rm(new URL('../dist/media/lang_taylor_test02_00001_.mp4', import.meta.url), { force: true });
const root = new URL('../dist/', import.meta.url);
for (const file of ['videos/lang-taylor-hero.webm', 'videos/lang-taylor-hero.mp4', 'videos/lang-taylor-hero-poster.webp']) await access(new URL(file, root));
let count = 0;
async function check(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) await check(path);
    else {
      count++;
      const { size } = await stat(path);
      if (size > 25 * 1024 * 1024) throw new Error(`${path}: exceeds Cloudflare Pages 25 MiB/file limit. Compress it or host it on R2.`);
    }
  }
}
await check(root.pathname);
if (count > 20000) throw new Error('Build exceeds Cloudflare Pages Free limit of 20,000 files.');
console.log(`Static assets verified: ${count} files, all <=25 MiB; video derivatives included; master excluded.`);
