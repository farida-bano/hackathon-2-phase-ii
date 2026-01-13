'use client'

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api'
import type { Todo } from '@/types'

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
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    )
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
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg shadow-indigo-500/30 flex items-center justify-center text-white hover:shadow-xl transition-all duration-300 z-10"
        aria-label="Add Todo"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
        </svg>
      </button>

      {/* Create Todo Form - Modal style */}
      {isFormVisible && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={() => setIsFormVisible(false)}
        >
          <div
            className="bg-white rounded-2xl shadow-xl p-6 max-w-md w-full mx-4 transform transition-all duration-300 scale-100 opacity-100"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="text-xl font-bold text-gray-900 mb-4">Add New Todo</h3>
            <form onSubmit={handleCreateTodo} className="space-y-4">
              <input
                type="text"
                value={newTodoDescription}
                onChange={(e) => setNewTodoDescription(e.target.value)}
                placeholder="What needs to be done?"
                maxLength={500}
                autoFocus
                className="input-field"
              />
              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={() => setIsFormVisible(false)}
                  className="btn btn-outline px-4 py-2"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary px-6 py-2"
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
        <div className="rounded-xl bg-red-50 p-4 border border-red-200">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex gap-2 bg-gray-100 p-1 rounded-xl w-fit">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'all'
              ? 'bg-white text-indigo-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'active'
              ? 'bg-white text-indigo-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Active
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'completed'
              ? 'bg-white text-indigo-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Completed
        </button>
      </div>

      {/* Todo List */}
      <div className="space-y-3">
        {todos.length === 0 ? (
          <div className="text-center py-16">
            <div className="inline-block p-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl mb-6">
              <svg className="w-16 h-16 mx-auto text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              {filter === 'all' ? 'Nothing to do!' : `No ${filter} todos`}
            </h3>
            <p className="text-gray-600 max-w-md mx-auto">
              {filter === 'all'
                ? "You're all caught up! Add a new task to get started."
                : `You don't have any ${filter} todos right now.`}
            </p>
          </div>
        ) : (
          todos.map((todo) => (
            <div
              key={todo.id}
              className={`flex items-center gap-4 p-4 bg-white rounded-xl border border-gray-200 transition-all duration-300 hover:shadow-md ${
                todo.completed ? 'opacity-70' : ''
              }`}
            >
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggleTodo(todo.id)}
                className="w-5 h-5 rounded-full border-2 border-gray-300 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-0"
              />
              <span className={`flex-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {todo.description}
              </span>
              <div className="flex gap-2">
                <button
                  onClick={() => handleDeleteTodo(todo.id)}
                  className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Stats */}
      <div className="flex justify-between items-center text-sm text-gray-600 bg-gray-50 p-3 rounded-xl">
        <span>
          {todos.filter(t => !t.completed).length} active {todos.filter(t => !t.completed).length === 1 ? 'task' : 'tasks'}
        </span>
        <span>
          {todos.length} {todos.length === 1 ? 'task' : 'tasks'} total
        </span>
      </div>
    </div>
  )
}
