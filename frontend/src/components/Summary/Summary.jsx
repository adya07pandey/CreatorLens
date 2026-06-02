import { useState } from 'react';
import RichText from '../Common/RichText';
import styles from './Summary.module.css';

export default function Summary({
  content,
  onExportPdf,
  exporting
}) {
  const [open, setOpen] = useState(false);

  if (!content) {
    return (
      <section className={styles.card}>
        <h2 className={styles.heading}>Comparison Summary</h2>
        <p className={styles.empty}>
          Summary will appear after ingestion completes.
        </p>
      </section>
    );
  }

  return (
    <section className={styles.card}>
      <div
        className={styles.header}
        onClick={() => setOpen(!open)}
      >
        <div className={styles.title}>
          {open ? '▼' : '▶'} Comparison Summary
        </div>

        {onExportPdf && (
          <button
            type="button"
            className={styles.exportBtn}
            onClick={(e) => {
              e.stopPropagation();
              onExportPdf();
            }}
            disabled={exporting}
          >
            {exporting ? 'Exporting…' : 'Export PDF'}
          </button>
        )}
      </div>

      {open && (
        <div className={styles.body}>
          <RichText
            content={content}
            variant="summary"
          />
        </div>
      )}
    </section>
  );
}