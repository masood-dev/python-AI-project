// ChatInput component.
import React, { useState, useRef } from 'react'
import '../styles/ChatInput.css'

function ChatInput({ onSendMessage, onUploadFile }) {
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const fileInputRef = useRef(null)

  async function handleSend() {
    if (!input.trim() || sending) return
    setSending(true)
    try {
      await onSendMessage(input)
      setInput('')
    } catch (error) {
      console.error('Send failed:', error)
    } finally {
      setSending(false)
    }
  }

  async function handleFileSelect(e) {
    const file = e.target.files?.[0]
    if (file) {
      try {
        await onUploadFile(file)
      } catch (error) {
        console.error('Upload failed:', error)
      }
    }
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-input">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message... (Shift+Enter for new line)"
        disabled={sending}
        rows="3"
      />
      <div className="input-controls">
        <button
          className="upload-btn"
          onClick={() => fileInputRef.current?.click()}
          title="Upload document"
          disabled={sending}
        >
          📎
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        <button
          className="send-btn"
          onClick={handleSend}
          disabled={!input.trim() || sending}
        >
          {sending ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default ChatInput
