import { useState } from 'react';
import {
  detectPlatform,
  formatDuration,
  formatNumber,
} from '../../utils/sessionCache';
import { getThumbnailFromUrl } from '../../utils/videoPreview';
import styles from './VideoCard.module.css';

const PLATFORM_LABEL = {
  youtube: 'YouTube',
  instagram: 'Instagram',
  unknown: 'Video',
};

export default function VideoCard({ label, url, video }) {
  const platform = video?.platform ?? detectPlatform(url);
  const title = video?.title || `Video ${label}`;
  const creator = video?.creator;
  const thumbnail = video?.thumbnail || getThumbnailFromUrl(url);
  const [imgError, setImgError] = useState(false);

  const showThumb = thumbnail && !imgError;

  return (
    <article className={styles.card}>
      <div className={styles.labelRow}>
        <span className={styles.badge}>{label}</span>
        <span className={styles.platform}>
          {PLATFORM_LABEL[platform] ?? platform}
        </span>
      </div>

      {showThumb ? (
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className={styles.thumbWrap}
        >
          <img
            src={thumbnail}
            alt=""
            className={styles.thumb}
            loading="lazy"
            onError={() => setImgError(true)}
          />
        </a>
      ) : (
        <div className={styles.thumbPlaceholder} aria-hidden="true">
          <span className={styles.placeholderLabel}>
            {PLATFORM_LABEL[platform] ?? 'Video'}
          </span>
        </div>
      )}

      <h3 className={styles.title}>{title}</h3>
      {creator && <p className={styles.creator}>{creator}</p>}

      {video && (video.views != null || video.likes != null || video.duration) && (
        <dl className={styles.stats}>
          <div>
            <dt>Views</dt>
            <dd>{formatNumber(video.views)}</dd>
          </div>
          <div>
            <dt>Likes</dt>
            <dd>{formatNumber(video.likes)}</dd>
          </div>
          <div>
            <dt>Duration</dt>
            <dd>{formatDuration(video.duration)}</dd>
          </div>
        </dl>
      )}

      {url && (
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className={styles.link}
        >
          Open source ↗
        </a>
      )}
    </article>
  );
}
