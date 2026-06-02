import { useCallback, useEffect, useState } from 'react';
import { fetchSessions, deleteSession as apiDelete } from '../api/sessions';

export function useSessions(activeSessionId) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSessions();
      setSessions(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
      setSessions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load, activeSessionId]);

  const remove = useCallback(
    async (sessionId) => {
      await apiDelete(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
    },
    []
  );

  return { sessions, loading, error, reload: load, remove };
}
