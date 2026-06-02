const STORAGE_KEY = 'vcrag_user_id';

function createId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `user_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
}

export function getUserId() {
  let id = localStorage.getItem(STORAGE_KEY);
  if (!id) {
    id = createId();
    localStorage.setItem(STORAGE_KEY, id);
  }
  return id;
}
