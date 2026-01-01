# Evolution of Todo - Phase II: Full-Stack Web Application

A modern, full-stack todo application with user authentication and persistent storage, built as Phase II of the Evolution of Todo project.

## Project Overview

**Phase II** transforms the CLI-only Phase I into a complete web application with:
- Backend REST API (Python/FastAPI)
- Database persistence (Neon PostgreSQL)
- Frontend web interface (Next.js/React)
- User authentication (JWT)
- Full CRUD operations for todos

## Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │  HTTP   │                 │  SQL    │                 │
│  Next.js 14     │ ◄─────► │  FastAPI        │ ◄─────► │  Neon           │
│  Frontend       │  JSON   │  Backend        │ Query   │  PostgreSQL     │
│                 │         │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
     Port 3000                   Port 8000                   Cloud hosted
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109+ (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel 0.0.14+
- **Authentication**: JWT with passlib (bcrypt)
- **Migrations**: Alembic 1.13+
- **Testing**: pytest + pytest-cov (48 tests, 80%+ coverage)

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **UI Library**: React 18+
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4+
- **Testing**: Jest + React Testing Library

## Features

### Phase II - Current Features

✅ **User Authentication**
- User signup with email validation
- Secure signin with bcrypt password hashing
- JWT token-based sessions (7-day expiration)
- Signout functionality

✅ **Todo Management**
- Create new todos (max 500 characters)
- View all todos for authenticated user
- Filter todos by completion status
- Update todo description
- Toggle todo completion status
- Delete todos

✅ **Security**
- User isolation (users can only access their own todos)
- Password hashing with bcrypt
- JWT authentication on all protected endpoints
- Input validation with Pydantic
- SQL injection prevention
- CORS configuration

✅ **Data Persistence**
- PostgreSQL database with Alembic migrations
- User and Todo entities with proper relationships
- CASCADE delete (deleting user removes their todos)
- Timestamps (created_at, updated_at, last_login_at)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon Serverless recommended)
- npm 9+ or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and secrets

# Run migrations
alembic upgrade head

# Start backend server
uvicorn src.main:app --reload
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with backend API URL

# Start development server
npm run dev
```

Frontend runs at: http://localhost:3000

### Running Tests

**Backend:**
```bash
cd backend
pytest --cov=src --cov-report=html
```

**Frontend:**
```bash
cd frontend
npm test
```

## Project Structure

```
todo-app/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── auth/           # Authentication utilities
│   │   ├── models/         # Database models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Request/response schemas
│   │   └── main.py         # FastAPI application
│   ├── tests/              # Backend tests (48 tests)
│   ├── alembic/            # Database migrations
│   └── README.md           # Backend documentation
│
├── frontend/               # Next.js React frontend
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and API client
│   │   └── contexts/      # React contexts (auth, todos)
│   ├── tests/             # Frontend tests
│   └── README.md          # Frontend documentation
│
├── specs/                  # Phase II specifications
│   └── 002-phase-ii-fullstack-web/
│       ├── spec.md        # Requirements specification
│       ├── plan.md        # Technical plan
│       └── tasks.md       # Implementation tasks
│
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Sign in user
- `POST /auth/signout` - Sign out user

### Todos (Protected)
- `GET /todos` - List user's todos (optional ?completed filter)
- `POST /todos` - Create new todo
- `PUT /todos/{id}` - Update todo
- `POST /todos/{id}/toggle` - Toggle completion
- `DELETE /todos/{id}` - Delete todo

### Health
- `GET /` - Health check

Full API documentation: http://localhost:8000/docs

## Development Workflow

### Backend Development

```bash
cd backend

# Run tests
pytest -v

# Format code
black src tests

# Lint code
ruff check --fix src tests

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Frontend Development

```bash
cd frontend

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format

# Build for production
npm run build
```

## Configuration

### Backend Environment Variables

```env
NEON_DATABASE_URL=postgresql://...
AUTH_SECRET=<generate-with-secrets-module>
FRONTEND_URL=http://localhost:3000
API_HOST=0.0.0.0
API_PORT=8000
SESSION_DURATION_DAYS=7
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing

### Backend Tests (48 total)
- ✅ 8 model tests (User, Todo relationships)
- ✅ 13 auth endpoint tests (signup, signin, signout)
- ✅ 9 auth utility tests (password hashing, JWT)
- ✅ 25 todo endpoint tests (CRUD, user isolation)

### Frontend Tests (To be implemented)
- Component tests
- Integration tests
- E2E tests

Coverage target: 80%+

## Deployment

### Backend Deployment

1. Set production environment variables
2. Use production-grade PostgreSQL (Neon recommended)
3. Run migrations: `alembic upgrade head`
4. Start with multiple workers: `uvicorn src.main:app --workers 4`
5. Use reverse proxy (nginx) with HTTPS

### Frontend Deployment

1. Build production bundle: `npm run build`
2. Deploy to Vercel/Netlify or self-host
3. Configure production API URL
4. Enable HTTPS

## Phase Roadmap

### ✅ Phase I: CLI Application (Completed)
- Basic todo operations via command line
- In-memory storage
- Python standard library only

### ✅ Phase II: Full-Stack Web Application (Current)
- REST API backend
- Database persistence
- Web frontend
- User authentication

### 🔮 Phase III+: Advanced Features (Future)
- Real-time collaboration
- Todo categories and tags
- Due dates and reminders
- Search and filtering
- Mobile app
- Team workspaces

## Documentation

- [Backend README](./backend/README.md) - Detailed backend documentation
- [Frontend README](./frontend/README.md) - Detailed frontend documentation
- [Specification](./specs/002-phase-ii-fullstack-web/spec.md) - Requirements
- [Technical Plan](./specs/002-phase-ii-fullstack-web/plan.md) - Architecture
- [Tasks](./specs/002-phase-ii-fullstack-web/tasks.md) - Implementation tasks

## Contributing

1. Follow established code style (black, ruff, prettier, eslint)
2. Write tests for new features (80%+ coverage)
3. Update documentation
4. Create meaningful commits
5. Test both backend and frontend

## Security

- Passwords hashed with bcrypt
- JWT tokens with expiration
- User isolation enforced at API level
- Input validation on all endpoints
- CORS properly configured
- Environment secrets not committed

## Support

For issues or questions:
1. Check documentation in README files
2. Review API docs at /docs endpoint
3. Check test files for usage examples

## License

Part of the Evolution of Todo project.

---

**Status**: Phase II Backend Complete ✅ | Frontend In Progress 🚧
