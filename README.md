# Lang Taylor

Korean creator landing page built with Astro and static HTML/CSS. Supplied artwork appears throughout the page. No client framework or tracking script.

## Local development

Requires Node.js 20.19+ (tested with 20.20.2).

```sh
npm install
npm run dev
```

## Build and preview

```sh
npm run build
npm run preview
```

The static site is generated in `dist/`. These commands do not deploy. For future Cloudflare Pages hosting, set the build command to `npm run build` and output directory to `dist`. No adapter or server runtime is required.

## Content

- `src/pages/index.astro`: content, SEO metadata, semantic markup.
- `src/styles/global.css`: responsive styles and reduced-motion support.
- `src/data/site.ts`: destination links and typed `episodes` array. Add real published videos to show video cards. An empty array shows the YouTube channel feature without fabricated episodes.
- `public/images/`: original supplied artwork; preserved unchanged.
- `scripts/prepare-images.mjs`: creates compressed WebP images and character crops in `public/media/`, before development and production builds.

Navigation and contacts use native anchors. External links use a new tab with `noopener noreferrer`. Email links open the visitor's mail app; mailbox creation and routing are not configured by the site.

Fonts load from Google Fonts with system fallbacks. Canonical URLs and the social preview image use `https://langtaylor.com`; update these if the production domain changes.

## Dependency notes

Astro 5 is retained for the supplied Node 20 environment. `sharp` is overridden to 0.35.5 or newer, and `unifont` is pinned to 0.7.0 to avoid a dependency requiring Node 22. The lockfile records the verified versions. `npm audit` still reports advisories in Astro 5 and its dependency tree; the suggested major upgrade requires Node 22.23.4 or newer. This site builds only static markup, with no server runtime, interactive islands, or user-submitted content. Revisit the Astro major version when upgrading Node.

In restricted development environments, set `ASTRO_TELEMETRY_DISABLED=1` before running Astro commands to avoid writing telemetry preferences outside the workspace.

## Workshop scene animation

The `#world .world-image` scene uses the supplied animation. The first-page comic poster, all scene copy, CTA links and surrounding layout remain unchanged. Desktop ratio stays `1.84`; mobile stays `1.24`. The entire 640×656 frame is centered over a blurred/darkened copy of the existing workshop image, with soft edges. The video is capped at native pixel dimensions, never cropped or enlarged. Original artwork remains the fallback.

- Master: `assets/video/lang_taylor_test02_00001_.mp4` (byte-identical copy of the supplied `public/media/lang_taylor_test02_00001_.mp4`). The supplied file is preserved locally. The tracked master is outside `public/` and excluded from deployment; the build also removes the ignored original from `dist/media/`.
- Deployable files: `public/videos/lang-taylor-hero.webm` (VP9), `lang-taylor-hero.mp4` (H.264 High, yuv420p, faststart), `lang-taylor-hero-poster.webp` (first source frame).
- Both videos: 640×656, 16 fps, 81 frames, approximately 5.06 seconds, no audio or generation-workflow metadata. No resize, timing changes, or interpolated frames.
- Playback: muted, inline, looped. Sources are attached only near the viewport, preserving initial hero loading priority. Offscreen/background playback pauses. Reduced-motion visitors see the static poster and make zero video requests; preference changes are handled live. Autoplay denial leaves the poster; failure of both video sources restores the original workshop image. No client framework or animation library is used.

To regenerate (local only; FFmpeg with libvpx-vp9 and libx264 required):

```sh
npm run video:prepare
# If ffmpeg is not on PATH:
FFMPEG_PATH=/opt/homebrew/bin/ffmpeg npm run video:prepare
```

The first-frame PNG is piped into the existing Sharp dependency to produce WebP. FFmpeg is **not** needed in Cloudflare's build environment: the three generated assets must be committed with the code. Do not rely on ignored `public/media/` video files for deployment.

`npm run build` keeps the existing static Astro output in `dist/` and now checks that all three video assets exist, every asset is at most 25 MiB, and the file count is within the Pages Free limit of 20,000. Oversized assets stop the build with a compression/R2 recommendation. No wrangler, adapter, deployment credentials, or hosting identity is added or changed.

Keep Cloudflare Pages' default ETag/revalidation cache behavior for these stable filenames; do not mark them immutable without versioning them. Pages provides Content-Type from extensions. Local production preview verified `video/webm`, `video/mp4`, and `image/webp`. References: [Pages limits](https://developers.cloudflare.com/pages/platform/limits/), [serving and caching](https://developers.cloudflare.com/pages/configuration/serving-pages/).

Local QA: Chrome/Playwright on production preview confirmed muted inline autoplay, a complete loop, 1440/768/390/320px viewports with original scene ratios and no overflow/upscaling, no video requests before the scene approaches, zero video requests under reduced motion, MP4 playback when WebM fails, original-image fallback when both fail, and poster fallback under simulated autoplay denial. Safari/iOS/Firefox devices and deployed URLs have not been tested. The source's final and first character poses differ; native looping retains that movement boundary rather than inventing reverse/crossfaded frames. No production deployment or push was performed.
