import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ingestVideos } from '../api/ingest';
import { saveSessionMeta, getSessions } from '../utils/sessionCache';
import styles from './Home.module.css';
export default function Home() {
  const navigate = useNavigate();
  const [urlA, setUrlA] = useState('');
  const [urlB, setUrlB] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const lastSessionId = localStorage.getItem('last_session_id');
  const hasSessions = getSessions().length > 0;
  const sessionCount = getSessions().length;

  const handleCompare = async (e) => {
    e.preventDefault();
    setError(null);
    const a = urlA.trim();
    const b = urlB.trim();

    if (!a || !b) {
      setError('Please enter both video URLs.');
      return;
    }

    if (a === b) {
      setError('Please enter two different videos.');
      return;
    }

    setLoading(true);

    try {
      const result = await ingestVideos(a, b);

      if (!result.success) {
        const which = result.failed_video === 'A' ? 'Video A' : 'Video B';
        setError(`${which}: ${result.error ?? 'Ingestion failed'}`);
        return;
      }

      saveSessionMeta(result.session_id, { urlA: a, urlB: b });

      localStorage.setItem('last_session_id', result.session_id);

      navigate(`/session/${result.session_id}`);
    } catch (err) {
      setError(err.message ?? 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={styles.lightBeam} aria-hidden="true" />
      <main className={styles.inner}>
        <section className={styles.comparePanel}>
          <div className={styles.panelHeader}>
            <div>
              <span className={styles.brand}>CreatorLens</span>

              <h1 className={styles.panelTitle}>
                Stop Guessing Why Videos Perform
              </h1>

              <p className={styles.panelText}>
                Compare two videos side-by-side and discover what made the winner stand out.
              </p>
            </div>

            <span className={styles.limitBadge}>
              5 comparisons/day
            </span>
          </div>

          {loading ? (
            <div className={styles.loadingBox} role="status" aria-live="polite">
              <div className={styles.loaderStage}>
                <span className={styles.loaderRing} />
                <span className={styles.loaderPulse} />
                <span className={styles.loaderOrbit} />
              </div>
              <div className={styles.loadingText}>
                <strong>Analyzing videos</strong>
                <span>Extracting transcripts, comparing performance, and generating insights.</span>
              </div>
            </div>
          ) : (
            <form className={styles.form} onSubmit={handleCompare}>
              <div className={styles.fields}>
                <label className={styles.field}>
                  <span className={styles.label}>Video A</span>
                  <input
                    type="url"
                    className={styles.input}
                    placeholder="https://youtube.com/watch?v=..."
                    value={urlA}
                    onChange={(e) => setUrlA(e.target.value)}
                    disabled={loading}
                    autoComplete="off"
                  />
                </label>

                <label className={styles.field}>
                  <span className={styles.label}>Video B</span>
                  <input
                    type="url"
                    className={styles.input}
                    placeholder="https://instagram.com/reel/..."
                    value={urlB}
                    onChange={(e) => setUrlB(e.target.value)}
                    disabled={loading}
                    autoComplete="off"
                  />
                </label>
              </div>

              {error && (
                <p className={styles.error} role="alert">
                  {error.split('\n').map((line, i) => (
                    <span key={i}>
                      {i > 0 && <br />}
                      {line}
                    </span>
                  ))}
                </p>
              )}

              <button
                type="submit"
                className={styles.submit}
                disabled={loading}
              >
                Compare videos
              </button>

              {lastSessionId && (
                <button
                  type="button"
                  className={styles.sessionsBtn}
                  onClick={() => navigate(`/session/${lastSessionId}`)}
                >
                  Resume Last Analysis
                </button>
              )}
            </form>
          )}

          <div className={styles.previewRow} aria-hidden="true">
            <span>
              <p><b>Performance Analysis</b></p>
              <p className="small">Understand why one video got more views, likes, and engagement.</p>
            </span>
            <span>
              <p><b>Content Breakdown</b></p>
              <p className="small">Compare openings, pacing, messaging, and audience appeal.</p>
            </span>
            <span>
              <p><b>Ask Follow-up Questions</b></p>
              <p className="small">Chat with both videos and get answers backed by transcripts and data.</p>
            </span>
          </div>
        </section>
      </main>
    </div>
  );
}
