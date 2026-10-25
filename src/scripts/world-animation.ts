// Sources stay dormant until this below-the-fold scene approaches the viewport.
const scene = document.querySelector<HTMLElement>('[data-world-animation]');
const video = scene?.querySelector<HTMLVideoElement>('video');
if (scene && video) {
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const sources = Array.from(video.querySelectorAll<HTMLSourceElement>('source'));
  let visible = false;
  let loaded = false;
  let failed = false;
  let failedSources = 0;
  video.muted = true;
  video.defaultMuted = true;

  const fail = () => {
    failed = true;
    video.pause();
    scene.dataset.playback = 'failed';
  };
  const play = () => {
    if (failed || motion.matches || !visible || document.hidden) return;
    if (!loaded) {
      loaded = true;
      failedSources = 0;
      sources.forEach(source => { source.src = source.dataset.src!; });
      video.load();
    }
    video.play().catch((error: DOMException) => {
      if (motion.matches) return;
      if (error.name === 'NotSupportedError') fail();
      // Autoplay denial and interrupted loads leave the first-frame poster visible.
      else if (!failed && video.paused) scene.dataset.playback = 'poster';
    });
  };
  video.addEventListener('playing', () => {
    if (motion.matches || !visible || document.hidden) video.pause();
    else scene.dataset.playback = 'playing';
  });
  video.addEventListener('error', () => { if (loaded && !motion.matches) fail(); });
  sources.forEach(source => source.addEventListener('error', () => {
    if (!loaded || motion.matches) return;
    failedSources += 1;
    if (failedSources >= sources.length) fail();
  }));
  // Poster failure also restores the original scene image.
  const poster = scene.querySelector<HTMLImageElement>('.world-motion-poster');
  poster?.addEventListener('error', fail);
  if (poster?.complete && !poster.naturalWidth) fail();

  const sync = () => {
    if (motion.matches) {
      video.pause();
      if (!failed) scene.dataset.playback = 'poster';
      // Sources are never attached for initial reduced motion. For a live change,
      // pause without calling load(): an empty source list can emit a false error.

    } else if (visible && !document.hidden) play();
    else video.pause();
  };
  motion.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      sync();
    }, { rootMargin: '160px 0px' }).observe(scene);
  } else {
    visible = true;
    sync();
  }
}
