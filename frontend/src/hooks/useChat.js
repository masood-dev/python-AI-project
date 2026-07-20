// Custom hook for chat operations.
import { useState, useCallback } from 'react'

export function useChat(sessionId) {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchMessages = useCallback(async () => {
    if (!sessionId) return
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`/api/v1/sessions/${sessionId}/messages`)
      if (!response.ok) throw new Error('Failed to fetch messages')
      const data = await response.json()
      setMessages(data.messages || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [sessionId])

  const sendMessage = useCallback(
    async (content) => {
      if (!sessionId) return null
      try {
        setError(null)
        const response = await fetch(`/api/v1/sessions/${sessionId}/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content }),
        })
        if (!response.ok) throw new Error('Failed to send message')
        const data = await response.json()
        setMessages((prev) => [
          ...prev,
          data.user_message,
          data.assistant_message,
        ])
        return data
      } catch (err) {
        setError(err.message)
        throw err
      }
    },
    [sessionId]
  )

  const uploadDocument = useCallback(
    async (file) => {
      if (!sessionId) return null
      try {
        setError(null)
        const formData = new FormData()
        formData.append('file', file)
        const response = await fetch(`/api/v1/sessions/${sessionId}/documents`, {
          method: 'POST',
          body: formData,
        })
        if (!response.ok) throw new Error('Failed to upload document')
        return await response.json()
      } catch (err) {
        setError(err.message)
        throw err
      }
    },
    [sessionId]
  )

  return {
    messages,
    loading,
    error,
    fetchMessages,
    sendMessage,
    uploadDocument,
  }
}
