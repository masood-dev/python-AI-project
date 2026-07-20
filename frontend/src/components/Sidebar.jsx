// Sidebar component for session list.
import React, { useState, useEffect } from 'react'
import '../styles/Sidebar.css'

function Sidebar({ onSelectSession, onNewChat }) {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchSessions()
  }, [])

  async function fetchSessions() {
    try {
      setLoading(true)
      const response = await fetch('/api/v1/sessions')
      const data = await response.json()
      setSessions(data.sessions || [])
    } catch (error) {
      console.error('Failed to fetch sessions:', error)
    } finally {
      setLoading(false)
    }
  }

  function handleNewChat() {
    onNewChat()
  }

  function handleSelectSession(sessionId) {
    onSelectSession(sessionId)
  }

  return (
    <div className="sidebar">
      <button className="new-chat-btn" onClick={handleNewChat}>
        + New Chat
      </button>

      <div className="sessions-list">
        <h3>Sessions</h3>
        {loading ? (
          <p className="loading-text">Loading...</p>
        ) : sessions.length === 0 ? (
          <p className="empty-text">No sessions yet</p>
        ) : (
          sessions.map((session) => (
            <div
              key={session.id || session._id}
              className="session-item"
              onClick={() => handleSelectSession(session.id || session._id)}
            >
              <span className="session-title">{session.title}</span>
              <span className="session-date">
                {new Date(session.created_at).toLocaleDateString()}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Sidebar
