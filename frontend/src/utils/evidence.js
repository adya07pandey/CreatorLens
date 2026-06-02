function isEvidenceJsonLine(line) {
  const t = line.trim();
  return (
    t.startsWith('{') &&
    t.endsWith('}') &&
    t.includes('"video"') &&
    t.includes('"start"')
  );
}

function isNoiseLine(line) {
  const t = line.trim();
  if (!t) return true;
  if (/^sources?:?$/i.test(t)) return true;
  if (/^source$/i.test(t)) return true;
  return false;
}

function tryParse(line) {
  try {
    return JSON.parse(line);
  } catch {
    return null;
  }
}

export function secondsToMmSs(value) {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0) return '0:00';
  const m = Math.floor(n / 60);
  const s = Math.floor(n % 60);
  return `${m}:${String(s).padStart(2, '0')}`;
}

export function formatSourceItem(item) {
  if (!item || typeof item !== 'object') return null;

  const video = item.video ? `Video ${item.video}` : null;
  const creator = item.creator || null;
  const platform = item.platform || null;
  const start = secondsToMmSs(item.start ?? item.start_time);
  const end = secondsToMmSs(item.end ?? item.end_time);

  const head = [video, creator, platform].filter(Boolean).join(' • ');
  const time = `${start}–${end}`;

  const excerpt = item.text
    ? ` — "${String(item.text).slice(0, 100)}${String(item.text).length > 100 ? '…' : ''}"`
    : '';

  if (!head) return null;
  return `${head} — ${time}${excerpt}`;
}

export function sourceKey(item) {
  if (!item) return '';
  return `${item.video}-${item.start ?? item.start_time}-${item.end ?? item.end_time}`;
}

export function normalizeSources(sources) {
  if (!Array.isArray(sources)) return [];

  const out = [];
  for (const src of sources) {
    if (typeof src === 'string') {
      const parsed = tryParse(src.trim());
      if (parsed) out.push(parsed);
      continue;
    }
    if (src && typeof src === 'object') out.push(src);
  }
  return out;
}

export function mergeSources(extractedEvidence, apiSources) {
  const merged = [];
  const seen = new Set();

  for (const item of [...extractedEvidence, ...normalizeSources(apiSources)]) {
    const key = sourceKey(item);
    if (!key || seen.has(key)) continue;
    seen.add(key);
    const label = formatSourceItem(item);
    if (label) merged.push({ key, label, raw: item });
  }

  return merged;
}

/**
 * Removes raw JSON / placeholder "Source" lines from assistant text.
 */
export function extractEvidenceFromContent(content) {
  if (!content) return { cleaned: content, evidence: [] };

  const lines = String(content).split('\n');
  const evidence = [];
  const kept = [];

  for (const line of lines) {
    if (isEvidenceJsonLine(line)) {
      const parsed = tryParse(line.trim());
      if (parsed) evidence.push(parsed);
      continue;
    }
    if (isNoiseLine(line)) continue;
    kept.push(line);
  }

  const cleaned = kept
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return { cleaned, evidence };
}
