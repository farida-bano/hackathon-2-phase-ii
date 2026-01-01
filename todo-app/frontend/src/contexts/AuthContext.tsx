'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { apiClient } from '@/lib/api'
import type { User } from '@/types'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  signin: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string) => Promise<void>
  signout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = apiClient.getToken()
    if (token) {
      setUser({ id: 0, email: '' })
    }
    setIsLoading(false)
  }, [])

  const signup = async (email: string, password: string) => {
    const response = await apiClient.signup(email, password)
    apiClient.setToken(response.token)
    setUser({ id: response.user_id, email: response.email })
  }

  const signin = async (email: string, password: string) => {
    const response = await apiClient.signin(email, password)
    apiClient.setToken(response.token)
    setUser({ id: response.user_id, email: response.email })
  }

  const signout = async () => {
    await apiClient.signout()
    apiClient.setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, signin, signup, signout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
