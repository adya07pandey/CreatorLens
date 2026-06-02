import styles from './EmptyState.module.css';

export default function EmptyState({ title, description, action }) {
  return (
    <div className={styles.wrap}>
      <p className={styles.title}>{title}</p>
      {description && <p className={styles.desc}>{description}</p>}
      {action}
    </div>
  );
}
