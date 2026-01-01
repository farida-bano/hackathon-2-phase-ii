export interface User {
  id: number
  email: string
}

export interface Todo {
  id: number
  description: string
  completed: boolean
  created_at: string
  updated_at: string | null
}

export interface AuthResponse {
  user_id: number
  email: string
  token: string
}

export interface TodoListResponse {
  todos: Todo[]
  total: number
}

export interface CreateTodoRequest {
  description: string
}

export interface UpdateTodoRequest {
  description?: string
  completed?: boolean
}
