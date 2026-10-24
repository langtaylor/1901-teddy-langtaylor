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
