/**
 * Dedicated /chat page for the RAG chatbot.
 * Integrates with Docusaurus layout and styling.
 */

import React from "react";
import Layout from "@theme/Layout";
import RagChat from "@site/src/components/RagChat";
import styles from "./Chat.module.css";

export default function ChatPage(): JSX.Element {
  const apiEndpoint = process.env.REACT_APP_API_ENDPOINT || "http://localhost:8000";

  return (
    <Layout
      title="Ask About the Book"
      description="Ask questions about Physical AI & Humanoid Robotics using AI-powered RAG chatbot"
    >
      <main className={styles.chatContainer}>
        <div className={styles.contentWrapper}>
          <div className={styles.sidebar}>
            <h1>Chat with the Book</h1>
            <p>
              Ask any question about <em>Physical AI & Humanoid Robotics: The Rise of the Digital Human</em>
            </p>

            <h3>How to use:</h3>
            <ul>
              <li>
                <strong>General Questions:</strong> Ask anything about the book
                content
              </li>
              <li>
                <strong>Selection Mode:</strong> Select text on the page and ask
                a question about just that passage
              </li>
              <li>
                <strong>Citations:</strong> Every answer includes source references
                with chapter and lesson links
              </li>
            </ul>

            <div className={styles.features}>
              <h4>✨ Features:</h4>
              <ul>
                <li>Powered by OpenAI GPT-4 Turbo</li>
                <li>Real-time vector search</li>
                <li>Automatic source citations</li>
                <li>Confidence scoring</li>
                <li>Selection-based queries</li>
              </ul>
            </div>

            <div className={styles.tips}>
              <h4>💡 Tips for better answers:</h4>
              <ul>
                <li>Ask specific questions rather than vague ones</li>
                <li>Include context from the book when relevant</li>
                <li>Use selection mode for targeted questions</li>
                <li>Check the sources for full context</li>
              </ul>
            </div>
          </div>

          <div className={styles.chatWrapper}>
            <RagChat
              apiEndpoint={apiEndpoint}
              title="RAG Chatbot"
              placeholder="Ask a question about the book..."
            />
          </div>
        </div>
      </main>
    </Layout>
  );
}
