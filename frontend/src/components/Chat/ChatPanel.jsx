import { useEffect, useRef } from 'react';
import Message from './Message';
import ChatInput from './ChatInput';
import EmptyState from '../Common/EmptyState';
import styles from './ChatPanel.module.css';

export default function ChatPanel({
  messages,
  streaming,
  error,
  onSend,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streaming]);

  return (
    <section className={styles.panel}>
      <header className={styles.header}>
        <h2 className={styles.title}>Chat</h2>
        <span className={styles.hint}>Ask anything about both videos</span>
      </header>

      <div className={styles.messages}>
        {messages.length === 0 && (
          <EmptyState
            title="Start the conversation"
            description="Compare hooks, CTAs, pacing, or ask which video performs better."
          />
        )}
        {messages.map((m) => (
          <Message
            key={m.id ?? `${m.role}-${m.timestamp}`}
            role={m.role}
            content={m.content}
            streaming={m.streaming}
            sources={m.sources}
          />
        ))}
        <div ref={bottomRef} />
      </div>

      {error && <p className={styles.error}>{error}</p>}

      <ChatInput onSend={onSend} disabled={streaming} />
    </section>
  );
}
