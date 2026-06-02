import { API_BASE } from './client';
import { getUserId } from '../utils/userId';

/**
 * Stream chat via SSE (fetch — axios buffers the full body in the browser).
 */
export async function streamChat(sessionId, message, callbacks) {
  const { onToken, onSources, onDone, onError } = callbacks;

  let response;
  try {
    response = await fetch(`${API_BASE}/api/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: getUserId(),
        session_id: sessionId,
        message,
      }),
    });
  } catch {
    onError?.(
      'Cannot reach the backend. Start it with: uvicorn app.main:app --reload --port 8000'
    );
    return;
  }

  if (!response.ok) {
    let detail = response.statusText;
    if (response.status === 502) {
      detail = 'Bad gateway — backend not running on port 8000';
    } else {
      try {
        const body = await response.json();
        detail = body.detail ?? detail;
      } catch {
        /* ignore */
      }
    }
    onError?.(typeof detail === 'string' ? detail : 'Chat request failed');
    return;
  }

  const reader = response.body?.getReader();
  if (!reader) {
    onError?.('Streaming not supported');
    return;
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split('\n\n');
      buffer = parts.pop() ?? '';

      for (const part of parts) {
        const line = part.trim();
        if (!line.startsWith('data:')) continue;

        const jsonStr = line.replace(/^data:\s*/, '');
        if (!jsonStr) continue;

        let payload;
        try {
          payload = JSON.parse(jsonStr);
        } catch {
          continue;
        }

        if (payload.type === 'token') {
          onToken?.(payload.token);
        } else if (payload.type === 'sources') {
          onSources?.(payload.sources);
        } else if (payload.type === 'done') {
          onDone?.();
        } else if (payload.type === 'error') {
          onError?.(payload.message ?? 'Stream error');
        }
      }
    }
  } catch (err) {
    onError?.(err.message ?? 'Connection lost');
  }
}
