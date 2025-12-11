/**
 * RAG Chatbot Component for Docusaurus
 *
 * Features:
 * - Chat interface with streaming responses
 * - Text selection mode for querying specific passages
 * - Source citations with links to chapters/lessons
 * - Confidence scores and processing metrics
 */

import React, { useState, useRef, useEffect } from "react";
import styles from "./RagChat.module.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  isSelectionMode?: boolean;
  sources?: SourceSnippet[];
  confidenceScore?: number;
  processingTime?: number;
}

interface SourceSnippet {
  chunk_id: string;
  doc_id: string;
  chapter?: string;
  lesson?: string;
  text: string;
  start_char: number;
  end_char: number;
  score: number;
}

interface RagChatProps {
  apiEndpoint?: string;
  title?: string;
  placeholder?: string;
}

const DEFAULT_API_ENDPOINT = "http://localhost:8000";

export const RagChat: React.FC<RagChatProps> = ({
  apiEndpoint = DEFAULT_API_ENDPOINT,
  title = "Ask about the Book",
  placeholder = "Ask a question about Physical AI & Humanoid Robotics...",
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState("");
  const [error, setError] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handle text selection for selection mode
  const handleTextSelection = () => {
    const selected = window.getSelection()?.toString() || "";
    if (selected) {
      setSelectedText(selected);
    }
  };

  // Send query to backend
  const sendQuery = async (
    query: string,
    useSelectionMode: boolean = false
  ) => {
    if (!query.trim()) {
      setError("Please enter a question");
      return;
    }

    setError("");
    setIsLoading(true);

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
      isSelectionMode: useSelectionMode && !!selectedText,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const endpoint = useSelectionMode
        ? `${apiEndpoint}/select-query`
        : `${apiEndpoint}/query`;

      const payload = useSelectionMode
        ? {
            query,
            selected_text: selectedText,
            user_id: "web-user",
          }
        : {
            query,
            user_id: "web-user",
          };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: data.short_answer,
        isSelectionMode: data.is_selection_mode,
        sources: data.sources,
        confidenceScore: data.confidence_score,
        processingTime: data.processing_time_ms,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setInput("");
      setSelectedText("");
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Unknown error occurred";
      setError(errorMessage);

      const errorMsg: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: `Sorry, I encountered an error: ${errorMessage}`,
      };

      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      sendQuery(input, false);
    }
  };

  const handleSendSelectionQuery = (e: React.MouseEvent) => {
    e.preventDefault();
    if (!selectedText) {
      setError("Please select text from the page first");
      return;
    }
    if (input.trim()) {
      sendQuery(input, true);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>{title}</h2>
        <p>
          {selectedText && (
            <span className={styles.selectionIndicator}>
              ✓ Text selected ({selectedText.length} chars)
            </span>
          )}
        </p>
      </div>

      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.emptyState}>
            <p>👋 Welcome! Ask me anything about the book.</p>
            <p className={styles.hint}>
              💡 Tip: Select text on the page and ask a question to query just
              that passage.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={styles.message}>
              <div className={`${styles.messageContent} ${styles[message.role]}`}>
                {message.role === "assistant" ? (
                  <>
                    <p>{message.content}</p>

                    {message.isSelectionMode && (
                      <div className={styles.badge}>
                        Answered from selected text
                      </div>
                    )}

                    {message.sources && message.sources.length > 0 && (
                      <div className={styles.sources}>
                        <h4>📚 Sources:</h4>
                        {message.sources.map((source, idx) => (
                          <div key={idx} className={styles.source}>
                            <div className={styles.sourceHeader}>
                              <span className={styles.sourceTitle}>
                                {source.chapter && source.lesson
                                  ? `${source.chapter} → ${source.lesson}`
                                  : source.chapter || "Document"}
                              </span>
                              <span className={styles.sourceScore}>
                                Relevance: {(source.score * 100).toFixed(0)}%
                              </span>
                            </div>
                            <p className={styles.sourceText}>
                              "{source.text.substring(0, 150)}..."
                            </p>
                          </div>
                        ))}
                      </div>
                    )}

                    {message.confidenceScore !== undefined && (
                      <div className={styles.metadata}>
                        <span>
                          Confidence: {(message.confidenceScore * 100).toFixed(0)}%
                        </span>
                        {message.processingTime && (
                          <span>Time: {message.processingTime.toFixed(0)}ms</span>
                        )}
                      </div>
                    )}
                  </>
                ) : (
                  <p>{message.content}</p>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && <div className={styles.error}>{error}</div>}

      <form onSubmit={handleSendMessage} className={styles.inputForm}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={placeholder}
          className={styles.input}
          rows={3}
          onMouseUp={handleTextSelection}
          disabled={isLoading}
        />

        <div className={styles.actions}>
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={styles.sendButton}
          >
            {isLoading ? "Processing..." : "Ask →"}
          </button>

          {selectedText && (
            <button
              type="button"
              onClick={handleSendSelectionQuery}
              disabled={isLoading || !input.trim()}
              className={`${styles.sendButton} ${styles.selectionMode}`}
              title="Query only the selected text"
            >
              Query Selection ✓
            </button>
          )}
        </div>
      </form>

      <div className={styles.footer}>
        <p>
          Powered by Ahad • Responses based on book content •{" "}
          <a href="/docs" target="_blank" rel="noopener noreferrer">
            View Book
          </a>
        </p>
      </div>
    </div>
  );
};

export default RagChat;
