// MessageList component.
import React, { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import '../styles/MessageList.css'

function MessageList({ messages, loading }) {
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>No messages yet. Start typing to begin!</p>
        </div>
      ) : (
        messages.map((msg) => (
          <MessageBubble
            key={msg.id || msg._id}
            role={msg.role}
            content={msg.content}
            timestamp={msg.created_at}
          />
        ))
      )}
      {loading && <div className="loading-indicator">Thinking...</div>}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default MessageList
