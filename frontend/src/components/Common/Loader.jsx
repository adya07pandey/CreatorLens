import styles from './Loader.module.css';

export default function Loader({ label = 'Loading…', size = 'md' }) {
  return (
    <div className={styles.wrap} role="status" aria-live="polite">
      <span className={`${styles.spinner} ${styles[size]}`} aria-hidden="true" />
      {label && <span className={styles.label}>{label}</span>}
    </div>
  );
}
