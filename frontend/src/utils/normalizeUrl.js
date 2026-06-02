/** Strip tracking query params; keep canonical reel/video path. */
export function normalizeVideoUrl(url) {
  const trimmed = url.trim();
  if (!trimmed) return trimmed;

  try {
    const parsed = new URL(trimmed);

    if (parsed.hostname.includes('instagram.com')) {
      const path = parsed.pathname.replace(/\/+$/, '');
      return `https://www.instagram.com${path}/`;
    }

    if (
      parsed.hostname.includes('youtube.com') ||
      parsed.hostname === 'youtu.be'
    ) {
      return parsed.origin + parsed.pathname + parsed.search;
    }

    return trimmed;
  } catch {
    return trimmed;
  }
}
