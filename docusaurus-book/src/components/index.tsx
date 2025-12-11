
import React, { useState } from 'react';
import RagChat from '../RagChat';
import styles from './styles.module.css';

const ChatbotPopup = () => {
  const [isOpen, setIsOpen] = useState(true);

  if (!isOpen) {
    return (
      <button className={styles.openButton} onClick={() => setIsOpen(true)}>
        Chat
      </button>
    );
  }

  return (
    <div className={styles.popupContainer}>
      <div className={styles.popupHeader}>
        <h3>Your Study Assistant</h3>
        <button className={styles.closeButton} onClick={() => setIsOpen(false)}>
          &times;
        </button>
      </div>
      <div className={styles.chatWrapper}>
        <RagChat />
      </div>
    </div>
  );
};

export default ChatbotPopup;
