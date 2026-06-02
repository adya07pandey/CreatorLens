import { useCallback, useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchMessages, fetchSessionDetails } from '../api/sessions';
import { downloadPdf } from '../api/pdf';
import { useSessions } from '../hooks/useSessions';
import { useChat } from '../hooks/useChat';
import { partitionMessages } from '../utils/messages';
import { getSessionMeta, saveSessionMeta } from '../utils/sessionCache';
import { buildVideoPreview } from '../utils/videoPreview';
import Sidebar from '../components/Sidebar/Sidebar';
import VideoCard from '../components/VideoCard/VideoCard';
import Summary from '../components/Summary/Summary';
import ChatPanel from '../components/Chat/ChatPanel';
import Loader from '../components/Common/Loader';
import styles from './Session.module.css';

function normalizeMessages(raw) {
  const list = Array.isArray(raw)
    ? raw
    : raw?.messages ?? [];

  return list.map((m, i) => ({
    id: m.id ?? `hist_${i}`,
    role: m.role,
    content: m.content,
    timestamp: m.timestamp,
  }));
}

export default function Session() {
  const { sessionId } = useParams();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [pageError, setPageError] = useState(null);
  const [summary, setSummary] = useState(null);
  const [exporting, setExporting] = useState(false);

  const { sessions, loading: sessionsLoading, remove } =
    useSessions(sessionId);

  const meta = useMemo(() => getSessionMeta(sessionId), [sessionId]);
  const [details, setDetails] = useState(null);

  const {
    messages: chatMessages,
    streaming,
    error: chatError,
    sendMessage,
    setInitial,
  } = useChat(sessionId, []);

  const loadSession = useCallback(async () => {
    if (!sessionId) return;
    setPageLoading(true);
    setPageError(null);

    try {
      const [sessionDetails, raw] = await Promise.all([
        fetchSessionDetails(sessionId),
        fetchMessages(sessionId),
      ]);

      setDetails(sessionDetails);
      saveSessionMeta(sessionId, {
        urlA: sessionDetails.url_a,
        urlB: sessionDetails.url_b,
        videoA: sessionDetails.video_a,
        videoB: sessionDetails.video_b,
      });

      const all = normalizeMessages(raw);
      const { summary: sum, chatMessages: chat } = partitionMessages(all);
      setSummary(sum);
      setInitial(
        chat.map((m, i) => ({
          id: `loaded_${i}`,
          role: m.role,
          content: m.content,
          timestamp: m.timestamp,
        }))
      );
    } catch (err) {
      setPageError(err.message ?? 'Failed to load session');
    } finally {
      setPageLoading(false);
    }
  }, [sessionId, setInitial]);

  useEffect(() => {
    loadSession();
  }, [loadSession]);

  const handleExportPdf = async () => {
    setExporting(true);
    try {
      await downloadPdf(sessionId);
    } catch {
      setPageError('PDF export failed');
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className={styles.layout}>
      <Sidebar
        sessions={sessions}
        loading={sessionsLoading}
        onDelete={remove}
        mobileOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      <main className={styles.main}>
        <header className={styles.topBar}>
          <button
            type="button"
            className={styles.menuBtn}
            onClick={() => setSidebarOpen(true)}
            aria-label="Open sessions"
          >
            ☰
          </button>
          <span className={styles.sessionTag}>
            {(details?.video_a?.title && details?.video_b?.title)
              ? `${details.video_a.title} vs ${details.video_b.title}`
              : `Session ${sessionId?.slice(0, 8)}…`}
          </span>
        </header>

        {pageLoading ? (
          <Loader label="Loading comparison…" />
        ) : pageError ? (
          <p className={styles.pageError}>{pageError}</p>
        ) : (
          <div className={styles.content}>
            <div className={styles.videos}>
              <VideoCard
                label="A"
                url={details?.url_a ?? meta?.urlA}
                video={buildVideoPreview(
                  details?.url_a ?? meta?.urlA,
                  details?.video_a ?? meta?.videoA
                )}
              />
              <VideoCard
                label="B"
                url={details?.url_b ?? meta?.urlB}
                video={buildVideoPreview(
                  details?.url_b ?? meta?.urlB,
                  details?.video_b ?? meta?.videoB
                )}
              />
            </div>

            <Summary
              content={summary}
              onExportPdf={handleExportPdf}
              exporting={exporting}
            />

            <ChatPanel
              messages={chatMessages}
              streaming={streaming}
              error={chatError}
              onSend={sendMessage}
            />
          </div>
        )}
      </main>
    </div>
  );
}
