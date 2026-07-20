// ChatWindow component.
import React, { useState, useEffect } from 'react'
import MessageList from './MessageList'
import ChatInput from './ChatInput'
import { useChat } from '../hooks/useChat'
import '../styles/ChatWindow.css'

function ChatWindow({ sessionId, onSessionCreated }) {
  const [currentSessionId, setCurrentSessionId] = useState(sessionId)
  const { messages, loading, error, fetchMessages, sendMessage, uploadDocument } =
    useChat(currentSessionId)

  useEffect(() => {
    if (sessionId !== currentSessionId) {
      setCurrentSessionId(sessionId)
    }
  }, [sessionId])

  useEffect(() => {
    if (currentSessionId) {
      fetchMessages()
    }
  }, [currentSessionId, fetchMessages])

  async function handleNewSession(title) {
    try {
      const response = await fetch('/api/v1/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      })
      if (!response.ok) throw new Error('Failed to create session')
      const data = await response.json()
      const newSessionId = data.id || data._id
      setCurrentSessionId(newSessionId)
      onSessionCreated(newSessionId)
    } catch (err) {
      console.error('Failed to create session:', err)
    }
  }

  async function handleSendMessage(content) {
    if (!currentSessionId) {
      await handleNewSession('New Chat')
    } else {
      try {
        await sendMessage(content)
      } catch (err) {
        console.error('Failed to send message:', err)
      }
    }
  }

  async function handleUploadFile(file) {
    if (!currentSessionId) {
      await handleNewSession('Document Chat')
    }
    try {
      await uploadDocument(file)
    } catch (err) {
      console.error('Failed to upload document:', err)
    }
  }

  return (
    <div className="chat-window">
      {!currentSessionId ? (
        <div className="welcome-screen">
          <h1>StudyChat AI</h1>
          <p>Start a new chat or select a session from the sidebar</p>
          <button
            className="start-chat-btn"
            onClick={() => handleNewSession('New Chat')}
          >
            Start New Chat
          </button>
        </div>
      ) : (
        <>
          <MessageList messages={messages} loading={loading} />
          {error && <div className="error-message">{error}</div>}
          <ChatInput onSendMessage={handleSendMessage} onUploadFile={handleUploadFile} />
        </>
      )}
    </div>
  )
}

export default ChatWindow
