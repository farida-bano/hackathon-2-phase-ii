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

  return (
    <div className="space-y-6">
      {/* Create Todo Form */}
      <form onSubmit={handleCreateTodo} className="flex gap-2">
        <input
          type="text"
          value={newTodoDescription}
          onChange={(e) => setNewTodoDescription(e.target.value)}
          placeholder="What needs to be done?"
          maxLength={500}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
        />
        <button
          type="submit"
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Add
        </button>
      </form>

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
      <div className="space-y-2">
        {todos.length === 0 ? (
          <p className="text-center text-gray-500 py-8">
            {filter === 'all' ? 'No todos yet. Add one above!' : `No ${filter} todos.`}
          </p>
        ) : (
          todos.map((todo) => (
            <div
              key={todo.id}
              className="flex items-center gap-3 p-4 bg-white border border-gray-200 rounded-md hover:shadow-sm transition-shadow"
            >
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggleTodo(todo.id)}
                className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
              />
              <span
                className={`flex-1 ${
                  todo.completed ? 'line-through text-gray-500' : 'text-gray-900'
                }`}
              >
                {todo.description}
              </span>
              <button
                onClick={() => handleDeleteTodo(todo.id)}
                className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
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
