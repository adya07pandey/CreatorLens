import { useCallback, useRef, useState } from 'react';
import styles from './ChatInput.module.css';

export default function ChatInput({ onSend, disabled, placeholder }) {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);

  const submit = useCallback(() => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }, [value, disabled, onSend]);

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  const onInput = (e) => {
    setValue(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
  };

  return (
    <div className={styles.wrap}>
      <textarea
        ref={textareaRef}
        className={styles.input}
        value={value}
        onChange={onInput}
        onKeyDown={onKeyDown}
        placeholder={placeholder ?? 'Ask about these videos…'}
        disabled={disabled}
        rows={1}
        aria-label="Chat message"
      />
      <button
        type="button"
        className={styles.send}
        onClick={submit}
        disabled={disabled || !value.trim()}
        aria-label="Send message"
      >
        ↑
      </button>
    </div>
  );
}
