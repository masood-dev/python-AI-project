// Frontend root component.
import React, { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import Sidebar from './components/Sidebar'
import './App.css'

function App() {
  const [sessionId, setSessionId] = useState(null)

  return (
    <div className="app-container">
      <Sidebar onSelectSession={setSessionId} onNewChat={() => setSessionId(null)} />
      <ChatWindow sessionId={sessionId} onSessionCreated={setSessionId} />
    </div>
  )
}

export default App
