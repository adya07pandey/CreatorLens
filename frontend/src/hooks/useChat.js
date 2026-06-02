import { useCallback, useRef, useState } from 'react';
import { streamChat } from '../api/chat';

let msgId = 0;
function nextId() {
  msgId += 1;
  return `msg_${msgId}`;
}

export function useChat(sessionId, initialMessages = []) {
  const [messages, setMessages] = useState(initialMessages);
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState(null);
  const abortRef = useRef(false);

  const setInitial = useCallback((msgs) => {
    setMessages(msgs);
    setError(null);
  }, []);

  const sendMessage = useCallback(
    async (text) => {
      const trimmed = text.trim();
      if (!trimmed || streaming || !sessionId) return;

      abortRef.current = false;
      setError(null);

      const userMsg = {
        id: nextId(),
        role: 'user',
        content: trimmed,
        timestamp: new Date().toISOString(),
      };

      const assistantId = nextId();
      const assistantPlaceholder = {
        id: assistantId,
        role: 'assistant',
        content: '',
        streaming: true,
        sources: null,
      };

      setMessages((prev) => [...prev, userMsg, assistantPlaceholder]);
      setStreaming(true);

      await streamChat(sessionId, trimmed, {
        onToken: (token) => {
          if (abortRef.current) return;
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? { ...m, content: m.content + token }
                : m
            )
          );
        },
        onSources: (sources) => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId ? { ...m, sources } : m
            )
          );
        },
        onDone: () => {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantId
                ? { ...m, streaming: false }
                : m
            )
          );
          setStreaming(false);
        },
        onError: (msg) => {
          setError(msg);
          setMessages((prev) =>
            prev.filter((m) => m.id !== assistantId || m.content)
          );
          setStreaming(false);
        },
      });
    },
    [sessionId, streaming]
  );

  return {
    messages,
    streaming,
    error,
    sendMessage,
    setInitial,
  };
}
