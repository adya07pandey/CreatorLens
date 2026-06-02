import { api, API_BASE } from './client';

export function getPdfUrl(sessionId) {
  return `${API_BASE}/api/${encodeURIComponent(sessionId)}/pdf`;
}

export async function downloadPdf(sessionId) {
  const { data } = await api.get(
    `/api/${encodeURIComponent(sessionId)}/pdf`,
    { responseType: 'blob' }
  );

  const objectUrl = URL.createObjectURL(data);
  const anchor = document.createElement('a');
  anchor.href = objectUrl;
  anchor.download = `comparison-${sessionId.slice(0, 8)}.pdf`;
  anchor.click();
  URL.revokeObjectURL(objectUrl);
}
