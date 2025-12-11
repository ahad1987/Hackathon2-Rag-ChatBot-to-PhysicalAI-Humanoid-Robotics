
import React from 'react';
import Root from '@theme-original/Root';
import ChatbotPopup from '@site/src/components/ChatbotPopup';

export default function RootWrapper(props) {
  return (
    <>
      <Root {...props} />
      <ChatbotPopup />
    </>
  );
}
