import { detectPlatform } from './sessionCache';

export function getYoutubeVideoId(url) {
  if (!url) return null;

  try {
    const parsed = new URL(url);

    if (parsed.hostname.includes('youtu.be')) {
      return parsed.pathname.slice(1).split('/')[0] || null;
    }

    if (parsed.pathname.includes('/shorts/')) {
      return parsed.pathname.split('/shorts/')[1]?.split('/')[0]?.split('?')[0] || null;
    }

    return parsed.searchParams.get('v');
  } catch {
    return null;
  }
}

export function getThumbnailFromUrl(url) {
  const platform = detectPlatform(url);

  if (platform === 'youtube') {
    const id = getYoutubeVideoId(url);
    if (id) {
      return `https://img.youtube.com/vi/${id}/hqdefault.jpg`;
    }
  }

  return null;
}

/** Build card props from URL + optional cached metadata from localStorage. */
export function buildVideoPreview(url, cached = null) {
  if (!url) return null;

  const platform = cached?.platform ?? detectPlatform(url);
  const thumbnail = cached?.thumbnail || getThumbnailFromUrl(url);

  return {
    platform,
    title: cached?.title || null,
    creator: cached?.creator || null,
    thumbnail,
    views: cached?.views,
    likes: cached?.likes,
    duration: cached?.duration,
  };
}
