import { spawnSync } from 'node:child_process';
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const ffmpeg = process.env.FFMPEG_PATH || 'ffmpeg';
const input = 'assets/video/lang_taylor_test02_00001_.mp4';
mkdirSync(new URL('../public/videos/', import.meta.url), { recursive: true });
function run(args) {
  const result = spawnSync(ffmpeg, ['-hide_banner', '-loglevel', 'warning', '-y', '-i', input, '-map_metadata', '-1', ...args], { cwd: root, stdio: 'inherit' });
  if (result.error) throw new Error(`FFmpeg is required only to regenerate video assets: ${result.error.message}`);
  if (result.status !== 0) process.exit(result.status || 1);
}
// Preserve source resolution (640×656), 16 fps and all 81 frames; no scale/FPS filter.
run(['-map', '0:v:0', '-an', '-c:v', 'libvpx-vp9', '-crf', '28', '-b:v', '0', '-deadline', 'good', '-cpu-used', '2', '-row-mt', '1', '-g', '32', '-pix_fmt', 'yuv420p', 'public/videos/lang-taylor-hero.webm']);
run(['-map', '0:v:0', '-an', '-c:v', 'libx264', '-crf', '21', '-preset', 'slow', '-profile:v', 'high', '-level:v', '3.1', '-g', '32', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', 'public/videos/lang-taylor-hero.mp4']);
const frame = spawnSync(ffmpeg, ['-hide_banner', '-loglevel', 'error', '-i', input, '-map', '0:v:0', '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', 'pipe:1'], { cwd: root, maxBuffer: 10 * 1024 * 1024 });
if (frame.status !== 0 || frame.error) throw new Error('Could not extract the first video frame.');
await sharp(frame.stdout).webp({ quality: 88 }).toFile(new URL('../public/videos/lang-taylor-hero-poster.webp', import.meta.url).pathname);
