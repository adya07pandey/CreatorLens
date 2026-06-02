import { Link, useNavigate, useParams } from 'react-router-dom';
import styles from './Sidebar.module.css';

function truncate(text, max = 42) {
  if (!text) return '';
  return text.length > max ? `${text.slice(0, max)}…` : text;
}

export default function Sidebar({
  sessions,
  loading,
  onDelete,
  mobileOpen,
  onClose,
}) {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const handleDelete = async (e, id) => {
    e.preventDefault();
    e.stopPropagation();
    if (!window.confirm('Delete this session?')) return;
    await onDelete(id);
    if (sessionId === id) navigate('/');
  };

  return (
    <>
      <div
        className={`${styles.backdrop} ${mobileOpen ? styles.backdropVisible : ''}`}
        onClick={onClose}
        aria-hidden="true"
      />
      <aside
        className={`${styles.sidebar} ${mobileOpen ? styles.sidebarOpen : ''}`}
      >
        <div className={styles.header}>
          <Link to="/" className={styles.brand} onClick={onClose}>
            CreatorLens
          </Link>
          <Link to="/" className={styles.newBtn} onClick={onClose}>
            + New
          </Link>
        </div>

        <div className={styles.listLabel}>Sessions</div>

        <nav className={styles.list} aria-label="Previous sessions">
          {loading && (
            <p className={styles.hint}>Loading sessions…</p>
          )}
          {!loading && sessions.length === 0 && (
            <p className={styles.hint}>No comparisons yet</p>
          )}
          {sessions.map((s) => (
            <div key={s.id} className={styles.itemWrap}>
              <Link
                to={`/session/${s.id}`}
                className={`${styles.item} ${sessionId === s.id ? styles.itemActive : ''}`}
                onClick={onClose}
              >
                <span className={styles.itemTitle}>
                  {truncate(s.label ?? `${s.title_a ?? 'Video A'} vs ${s.title_b ?? 'Video B'}`)}
                </span>
              </Link>
              <button
                type="button"
                className={styles.deleteBtn}
                onClick={(e) => handleDelete(e, s.id)}
                aria-label="Delete session"
                title="Delete"
              >
                ×
              </button>
            </div>
          ))}
        </nav>
      </aside>
    </>
  );
}
