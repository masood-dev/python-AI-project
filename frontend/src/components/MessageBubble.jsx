// MessageBubble component.
import React from 'react'
import '../styles/MessageBubble.css'

function MessageBubble({ role, content, timestamp }) {
  const isUser = role === 'user'

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        <p>{content}</p>
      </div>
      {timestamp && (
        <div className="message-timestamp">
          {new Date(timestamp).toLocaleTimeString()}
        </div>
      )}
    </div>
  )
}

export default MessageBubble
