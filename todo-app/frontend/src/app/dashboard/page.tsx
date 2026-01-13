'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import TodoList from '@/components/TodoList'

export default function DashboardPage() {
  const router = useRouter()
  const { user, signout, isLoading } = useAuth()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/signin')
    }
  }, [user, isLoading, router])

  const handleSignout = async () => {
    await signout()
    router.push('/')
  }

  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome back, {user.email.split('@')[0]}!</h1>
          <p className="text-gray-600">Manage your tasks and boost your productivity</p>
        </div>

        <div className="card max-w-4xl mx-auto p-8 slide-up">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">My Todos</h2>
              <p className="text-gray-600">Stay organized and get things done</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
                {user.email}
              </span>
              <button
                onClick={handleSignout}
                className="btn btn-outline px-4 py-2"
              >
                Sign Out
              </button>
            </div>
          </div>

          <div className="mt-6">
            <TodoList />
          </div>
        </div>
      </div>
    </div>
  )
}
