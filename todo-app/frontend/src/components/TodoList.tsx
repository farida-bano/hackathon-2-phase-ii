'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import type { Todo } from '@/types'
import '@/styles/todo-components.css'

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [newTodoDescription, setNewTodoDescription] = useState('')
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [isFormVisible, setIsFormVisible] = useState(false)

  const fetchTodos = async () => {
    try {
      setError('')
      const filterValue = filter === 'all' ? undefined : filter === 'completed'
      const response = await apiClient.getTodos(filterValue)
      setTodos(response.todos)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch todos')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchTodos()
  }, [filter])

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTodoDescription.trim()) return

    try {
      setError('')
      await apiClient.createTodo({ description: newTodoDescription })
      setNewTodoDescription('')
      setIsFormVisible(false)
      await fetchTodos()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create todo')
    }
  }

  const handleToggleTodo = async (id: number) => {
    try {
      setError('')
      await apiClient.toggleTodo(id)
      await fetchTodos()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to toggle todo')
    }
  }

  const handleDeleteTodo = async (id: number) => {
    try {
      setError('')
      await apiClient.deleteTodo(id)
      await fetchTodos()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo')
    }
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading todos...</div>
  }

  // Helper to determine priority (mock - you can make this dynamic later)
  const getPriority = (todo: Todo): 'high' | 'medium' | 'low' | 'none' => {
    // For demo: you could add priority field to Todo model
    // For now, using a simple rule based on description keywords
    const desc = todo.description.toLowerCase()
    if (desc.includes('urgent') || desc.includes('asap') || desc.includes('important')) return 'high'
    if (desc.includes('soon') || desc.includes('meeting')) return 'medium'
    if (desc.includes('later') || desc.includes('someday')) return 'low'
    return 'none'
  }

  return (
    <div className="space-y-6">
      {/* Floating Add Button */}
      <button
        onClick={() => setIsFormVisible(!isFormVisible)}
        className="floating-add-btn"
        aria-label="Add Todo"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
        </svg>
      </button>

      {/* Create Todo Form - Modal style */}
      {isFormVisible && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[999]" onClick={() => setIsFormVisible(false)}>
          <div className="bg-white rounded-lg shadow-2xl p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Add New Todo</h3>
            <form onSubmit={handleCreateTodo} className="space-y-4">
              <input
                type="text"
                value={newTodoDescription}
                onChange={(e) => setNewTodoDescription(e.target.value)}
                placeholder="What needs to be done?"
                maxLength={500}
                autoFocus
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-900"
              />
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setIsFormVisible(false)}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition"
                >
                  Add Todo
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-gray-200">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 font-medium ${
            filter === 'all'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 font-medium ${
            filter === 'active'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Active
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 font-medium ${
            filter === 'completed'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Completed
        </button>
      </div>

      {/* Todo List */}
      <div className="space-y-3">
        {todos.length === 0 ? (
          <div className="empty-state">
            <svg className="empty-state-icon" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#4F46E5" />
                  <stop offset="100%" stopColor="#7C3AED" />
                </linearGradient>
              </defs>
              <circle className="empty-state-svg" cx="100" cy="100" r="80" strokeWidth="3"/>
              <path className="empty-state-svg" d="M70 100 L90 120 L130 80" strokeWidth="4"/>
              <circle className="empty-state-svg" cx="100" cy="40" r="8" fill="url(#gradient)"/>
              <circle className="empty-state-svg" cx="100" cy="160" r="8" fill="url(#gradient)"/>
              <circle className="empty-state-svg" cx="40" cy="100" r="8" fill="url(#gradient)"/>
              <circle className="empty-state-svg" cx="160" cy="100" r="8" fill="url(#gradient)"/>
            </svg>
            <h3 className="empty-state-title">
              {filter === 'all' ? 'Nothing to do!' : `No ${filter} todos`}
            </h3>
            <p className="empty-state-subtitle">
              {filter === 'all'
                ? "You're all caught up! Click the button below to add your first task."
                : `You don't have any ${filter} todos right now.`}
            </p>
            <p className="empty-state-encouragement">
              {filter === 'all' ? "Every great journey starts with a single task." : "Keep up the great work!"}
            </p>
          </div>
        ) : (
          todos.map((todo) => (
            <div
              key={todo.id}
              className={`todo-card ${todo.completed ? 'completed' : ''}`}
              data-priority={getPriority(todo)}
            >
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggleTodo(todo.id)}
                className="todo-checkbox"
              />
              <span className="todo-text">
                {todo.description}
              </span>
              <button
                onClick={() => handleDeleteTodo(todo.id)}
                className="todo-delete-btn"
              >
                Delete
              </button>
            </div>
          ))
        )}
      </div>

      {/* Stats */}
      <div className="text-sm text-gray-600 text-center">
        {todos.length} {todos.length === 1 ? 'todo' : 'todos'}
      </div>
    </div>
  )
}
