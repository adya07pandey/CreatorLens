const PREFIX = 'vcrag_session_';

export function saveSessionMeta(sessionId, meta) {
  try {
    localStorage.setItem(
      `${PREFIX}${sessionId}`,
      JSON.stringify({
        urlA: meta.urlA,
        urlB: meta.urlB,
        videoA: meta.videoA ?? null,
        videoB: meta.videoB ?? null,
        createdAt: meta.createdAt ?? Date.now(),
      })
    );
  } catch {
    /* quota exceeded */
  }
}

export function getSessionMeta(sessionId) {
  try {
    const raw = localStorage.getItem(`${PREFIX}${sessionId}`);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function detectPlatform(url) {
  if (!url) return 'unknown';
  const lower = url.toLowerCase();
  if (lower.includes('instagram.com')) return 'instagram';
  if (lower.includes('youtube.com') || lower.includes('youtu.be')) return 'youtube';
  return 'unknown';
}

export function formatDuration(seconds) {
  if (!seconds || seconds <= 0) return '—';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

export function formatNumber(n) {
  if (n == null || Number.isNaN(n)) return '—';
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}
export function getSessions() {
  try {
    return Object.keys(localStorage)
      .filter((key) => key.startsWith(PREFIX))
      .map((key) => {
        const sessionId = key.replace(PREFIX, '');

        return {
          sessionId,
          ...JSON.parse(localStorage.getItem(key)),
        };
      });
  } catch {
    return [];
  }
}