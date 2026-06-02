import axios from 'axios';

/** Empty in dev → Vite proxies /api to the backend. Set VITE_API_BASE to call backend directly. */
export const API_BASE = import.meta.env.VITE_API_BASE ?? '';

export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 600_000,
});

function extractErrorMessage(error) {
  if (!error.response) {
    if (error.code === 'ECONNABORTED') {
      return (
        'Request timed out before the server finished. Long YouTube videos (30+ min) ' +
        'can take 20–60+ minutes if Whisper is used. Check the backend terminal for ' +
        '[INGEST] step timings, then try again or use shorter videos with captions.'
      );
    }
    return (
      'Cannot reach the backend API. Start it from the backend folder:\n' +
      'uvicorn app.main:app --reload --port 8000'
    );
  }

  const { status, data } = error.response;

  if (status === 502 || status === 503) {
    return (
      'Bad gateway — the API server is not reachable on port 8000. ' +
      'Start the backend, then try again.'
    );
  }

  const detail = data?.detail ?? data?.message;
  if (typeof detail === 'string') {
    if (
      detail.includes('psycopg2.') ||
      detail.includes('sqlalchemy') ||
      detail.includes('[SQL:')
    ) {
      return 'Database connection failed. Please try again.';
    }

    return detail;
  }
  if (Array.isArray(detail)) {
    return detail.map((d) => d.msg ?? JSON.stringify(d)).join(', ');
  }
  if (detail) return JSON.stringify(detail);

  return error.message || `Request failed (${status})`;
}

api.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(new Error(extractErrorMessage(error)))
);

export async function apiGet(url, config = {}) {
  const { data } = await api.get(url, config);
  return data;
}

export async function apiPost(url, body, config = {}) {
  const { data } = await api.post(url, body, config);
  return data;
}

export async function apiDelete(url, config = {}) {
  const { data } = await api.delete(url, config);
  return data;
}
