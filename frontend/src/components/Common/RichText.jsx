import styles from './RichText.module.css';

function stripBoldMarkers(text) {
  return text.replace(/\*\*/g, '');
}

function formatInline(text, variant) {
  if (!text) return null;

  if (variant === 'chat') {
    return stripBoldMarkers(text);
  }

  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

function isListLine(line) {
  return /^[-*•]\s+/.test(line.trim());
}

function isNumberedListLine(line) {
  return /^\d+\.\s+/.test(line.trim());
}

function stripListMarker(line) {
  return line
    .trim()
    .replace(/^[-*•]\s+/, '')
    .replace(/^\d+\.\s+/, '');
}

function isHeading(line) {
  return /^#{2,3}\s+/.test(line.trim());
}

function parseHeading(line) {
  const trimmed = line.trim();
  const level = trimmed.startsWith('###') ? 3 : 2;
  const text = trimmed.replace(/^#{2,3}\s+/, '');
  return { level, text };
}

function isSectionLabel(line) {
  return /^[A-Za-z][A-Za-z\s]+:\s*$/.test(line.trim());
}

function isTableLine(line) {
  const trimmed = line.trim();
  return trimmed.startsWith('|') && trimmed.endsWith('|');
}

function isTableSeparatorLine(line) {
  const trimmed = line.trim().replace(/^\|/, '').replace(/\|$/, '');
  const cells = trimmed.split('|').map((c) => c.trim());
  return cells.length >= 2 && cells.every((c) => /^:?-{3,}:?$/.test(c));
}

function parseTableRow(line) {
  const trimmed = line.trim().replace(/^\|/, '').replace(/\|$/, '');
  return trimmed.split('|').map((c) => c.trim());
}

function isListLikeLine(line) {
  return isListLine(line) || isNumberedListLine(line);
}

function normalizeTableSpacing(content) {
  const lines = content.split('\n');
  const normalized = [];

  for (let i = 0; i < lines.length; i += 1) {
    const previous = normalized[normalized.length - 1]?.trim();
    const current = lines[i].trim();
    const next = lines[i + 1]?.trim();

    if (!current && isTableLine(previous ?? '') && isTableLine(next ?? '')) {
      continue;
    }

    normalized.push(lines[i]);
  }

  return normalized.join('\n');
}

function extractTableBlocks(content) {
  const lines = normalizeTableSpacing(content).split("\n");

  const blocks = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trim();

    if (!line) {
      i++;
      continue;
    }

    if (
      isTableLine(line) &&
      i + 1 < lines.length &&
      isTableSeparatorLine(lines[i + 1])
    ) {
      const tableLines = [
        line,
        lines[i + 1].trim()
      ];

      i += 2;

      while (i < lines.length) {
        const current = lines[i].trim();

        if (!current) {
          i++;
          continue;
        }

        if (!isTableLine(current)) {
          break;
        }

        tableLines.push(current);
        i++;
      }

      blocks.push({
        type: "table",
        header: parseTableRow(tableLines[0]),
        rows: tableLines
          .slice(2)
          .map(parseTableRow)
      });

      continue;
    }

    blocks.push({
      type: "text",
      content: line
    });

    i++;
  }

  return blocks;
}

function parseBlocks(content, variant) {

  const normalizedContent = normalizeTableSpacing(content)
    .replace(/\n\s*\n(?=\|)/g, "\n")
    .replace(/(?<=\|)\n\s*\n/g, "\n");

  const paragraphs = normalizedContent
    .split(/\n\n+/)
    .map((p) => p.trim())
    .filter(Boolean);

  const blocks = [];

  for (const paragraph of paragraphs) {
    const lines = paragraph
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean);

    if (lines.length === 0) continue;
    if (
      lines.length >= 3 &&
      isHeading(lines[0]) &&
      isTableLine(lines[1]) &&
      isTableSeparatorLine(lines[2])
    ) {

      const h = parseHeading(lines[0]);

      blocks.push({
        type: "heading",
        level: h.level,
        text: h.text
      });

      blocks.push({
        type: "table",
        header: parseTableRow(lines[1]),
        rows: lines.slice(3).map(parseTableRow)
      });

      continue;
    }
    if (
      lines.length >= 2 &&
      lines.every(isTableLine) &&
      isTableSeparatorLine(lines[1])
    ) {
      blocks.push({
        type: 'table',
        header: parseTableRow(lines[0]),
        rows: lines.slice(2).filter(isTableLine).map(parseTableRow),
      });
      continue;
    }

    if (variant === 'summary' && lines.every(isHeading)) {
      for (const line of lines) {
        const h = parseHeading(line);
        blocks.push({ type: 'heading', level: h.level, text: h.text });
      }
      continue;
    }

    if (variant === 'chat' && lines.every(isSectionLabel)) {
      for (const line of lines) {
        blocks.push({ type: 'section', text: line.replace(/:$/, '') });
      }
      continue;
    }

    if (variant === 'chat' && lines.some(isSectionLabel) && lines.length <= 3) {
      for (const line of lines) {
        if (isSectionLabel(line)) {
          blocks.push({ type: 'section', text: line.replace(/:$/, '') });
        } else if (isListLikeLine(line)) {
          blocks.push({ type: 'list', items: [stripListMarker(line)] });
        } else {
          blocks.push({ type: 'paragraph', text: line });
        }
      }
      continue;
    }

    if (lines.every(isListLikeLine)) {
      blocks.push({ type: 'list', items: lines.map(stripListMarker) });
      continue;
    }

    if (lines.length === 1) {
      if (variant === 'chat' && isSectionLabel(lines[0])) {
        blocks.push({ type: 'section', text: lines[0].replace(/:$/, '') });
      } else if (variant === 'summary' && isHeading(lines[0])) {
        const h = parseHeading(lines[0]);
        blocks.push({ type: 'heading', level: h.level, text: h.text });
      } else {
        blocks.push({ type: 'paragraph', text: lines[0] });
      }
      continue;
    }

    if (variant === 'summary' && lines.some(isHeading)) {
      for (const line of lines) {
        if (isHeading(line)) {
          const h = parseHeading(line);
          blocks.push({ type: 'heading', level: h.level, text: h.text });
        } else if (isListLikeLine(line)) {
          blocks.push({ type: 'list', items: [stripListMarker(line)] });
        } else {
          blocks.push({ type: 'paragraph', text: line });
        }
      }
      continue;
    }

    if (variant === 'chat') {
      for (const line of lines) {
        if (isSectionLabel(line)) {
          blocks.push({ type: 'section', text: line.replace(/:$/, '') });
        } else if (isListLikeLine(line)) {
          blocks.push({ type: 'list', items: [stripListMarker(line)] });
        } else {
          blocks.push({ type: 'paragraph', text: line });
        }
      }
      continue;
    }

    blocks.push({ type: 'list', items: lines });
  }

  return blocks;
}

export default function RichText({ content, compact = false, variant = 'summary' }) {
  if (!content) return null;

  const blocks = parseBlocks(content, variant);
  const rootClass = compact ? `${styles.root} ${styles.compact}` : styles.root;

  return (
    <div className={rootClass}>
      {blocks.map((block, index) => {
        if (block.type === 'list') {
          return (
            <ul key={index} className={styles.list}>
              {block.items.map((item, i) => (
                <li key={i}>{formatInline(item, variant)}</li>
              ))}
            </ul>
          );
        }

        if (block.type === 'section') {
          return (
            <p key={index} className={styles.sectionLabel}>
              {formatInline(block.text, variant)}:
            </p>
          );
        }

        if (block.type === 'heading') {
          const Tag = block.level === 3 ? 'h3' : 'h2';
          return (
            <Tag key={index} className={styles.heading}>
              {formatInline(block.text, variant)}
            </Tag>
          );
        }

        if (block.type === 'table') {
          return (
            <div key={index} className={styles.tableWrap}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    {block.header.map((h, i) => (
                      <th key={i}>{formatInline(h, variant)}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {block.rows.map((row, r) => (
                    <tr key={r}>
                      {row.map((cell, c) => (
                        <td key={c}>{formatInline(cell, variant)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
        }

        return (
          <p key={index} className={styles.paragraph}>
            {formatInline(block.text, variant)}
          </p>
        );
      })}
    </div>
  );
}
