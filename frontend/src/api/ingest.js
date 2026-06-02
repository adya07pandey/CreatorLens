import { apiPost } from './client';
import { getUserId } from '../utils/userId';
import { normalizeVideoUrl } from '../utils/normalizeUrl';

/** No axios timeout — long YouTube + Whisper can exceed 30+ minutes. */
const INGEST_TIMEOUT_MS = 0;

export async function ingestVideos(urlA, urlB) {
  return apiPost(
    '/api/ingest',
    {
      user_id: getUserId(),
      url_a: normalizeVideoUrl(urlA),
      url_b: normalizeVideoUrl(urlB),
    },
    { timeout: INGEST_TIMEOUT_MS }
  );
}
