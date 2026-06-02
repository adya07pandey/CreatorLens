/** Split stored messages into summary (first assistant) and chat thread. */
export function partitionMessages(messages) {
  if (!messages?.length) {
    return { summary: null, chatMessages: [] };
  }

  const firstAssistantIdx = messages.findIndex((m) => m.role === 'assistant');

  if (firstAssistantIdx === -1) {
    return { summary: null, chatMessages: messages };
  }

  const summary = messages[firstAssistantIdx].content;
  const chatMessages = messages.filter((_, i) => i !== firstAssistantIdx);

  return { summary, chatMessages };
}
