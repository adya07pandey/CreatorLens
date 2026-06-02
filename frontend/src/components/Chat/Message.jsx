import { memo } from 'react';
import RichText from '../Common/RichText';
import {
  extractEvidenceFromContent,
  mergeSources,
} from '../../utils/evidence';
import styles from './Message.module.css';

function Message({ role, content, streaming, sources }) {
  const isUser = role === 'user';

  const extracted =
    !isUser && !streaming
      ? extractEvidenceFromContent(content)
      : { cleaned: content, evidence: [] };

  const mergedSources = !isUser && !streaming
    ? mergeSources(extracted.evidence, sources)
    : [];

  return (
    <div
      className={`${styles.row} ${isUser ? styles.user : styles.assistant}`}
    >
      <div className={styles.bubble}>
        {isUser || streaming ? (
          <p className={styles.content}>
            {content || (streaming ? '' : '…')}
            {streaming && <span className={styles.cursor} aria-hidden="true" />}
          </p>
        ) : (
          <div className={styles.richContent}>
            <RichText content={extracted.cleaned} compact variant="chat" />
          </div>
        )}

        {mergedSources.length > 0 && (
          <div className={styles.sourcesBox}>
            <p className={styles.sourcesTitle}>Sources</p>
            <ul>
              {mergedSources.map((src) => (
                <li key={src.key}>{src.label}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default memo(Message);
