import { apiGet, apiDelete } from './client';
import { getUserId } from '../utils/userId';

export async function fetchSessions() {
  const userId = getUserId();
  return apiGet('/api/', { params: { user_id: userId } });
}

export async function fetchSessionDetails(sessionId) {
  const userId = getUserId();
  return apiGet(`/api/session/${encodeURIComponent(sessionId)}/details`, {
    params: { user_id: userId },
  });
}

export async function fetchMessages(sessionId) {
  const userId = getUserId();
  return apiGet(`/api/${encodeURIComponent(sessionId)}`, {
    params: { user_id: userId },
  });
}

export async function deleteSession(sessionId) {
  const userId = getUserId();
  return apiDelete(`/api/${encodeURIComponent(sessionId)}`, {
    params: { user_id: userId },
  });
}
