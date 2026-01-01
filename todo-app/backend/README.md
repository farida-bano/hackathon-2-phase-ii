# Evolution of Todo - Backend API (Phase II)

Backend REST API for the Evolution of Todo full-stack web application.

## Technology Stack

- **Framework**: FastAPI 0.109+
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel 0.0.14+
- **Authentication**: JWT with passlib (bcrypt)
- **Migrations**: Alembic 1.13+
- **Testing**: pytest with pytest-cov
- **Code Quality**: ruff, black

## Prerequisites

- Python 3.11+
- PostgreSQL database (Neon Serverless recommended)
- pip or uv package manager

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt

# Or with development dependencies
pip install -e ".[dev]"
```

### 2. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
NEON_DATABASE_URL=postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
AUTH_SECRET=your-secret-key-here-change-in-production
FRONTEND_URL=http://localhost:3000
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
SESSION_DURATION_DAYS=7
```

**Generate AUTH_SECRET**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Run Database Migrations

```bash
# Apply migrations to create tables
alembic upgrade head
```

### 4. Start Development Server

```bash
# Using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m src.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Register new user | No |
| POST | `/auth/signin` | Sign in user | No |
| POST | `/auth/signout` | Sign out user | Yes |

### Todos

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/todos` | List user's todos | Yes |
| POST | `/todos` | Create new todo | Yes |
| PUT | `/todos/{todo_id}` | Update todo | Yes |
| POST | `/todos/{todo_id}/toggle` | Toggle completion | Yes |
| DELETE | `/todos/{todo_id}` | Delete todo | Yes |

### Query Parameters

- `GET /todos?completed=true` - Filter by completion status (true/false)

### Authentication

All protected endpoints require a Bearer token in the Authorization header:

```bash
Authorization: Bearer <jwt_token>
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run and watch for changes
pytest --watch
```

View coverage report: `open htmlcov/index.html`

## Code Quality

```bash
# Format code with black
black src tests

# Lint with ruff
ruff check src tests

# Auto-fix linting issues
ruff check --fix src tests
```

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current revision
alembic current
```

## Project Structure

```
backend/
├── alembic/                  # Database migrations
│   ├── versions/            # Migration files
│   └── env.py               # Alembic environment
├── src/
│   ├── auth/                # Authentication utilities
│   │   ├── password.py      # Password hashing
│   │   ├── token.py         # JWT token management
│   │   └── dependencies.py  # Auth dependencies
│   ├── models/              # SQLModel database models
│   │   ├── user.py          # User model
│   │   └── todo.py          # Todo model
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Auth endpoints
│   │   └── todos.py         # Todo CRUD endpoints
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── auth.py          # Auth schemas
│   │   ├── todo.py          # Todo schemas
│   │   └── error.py         # Error schemas
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   └── main.py              # FastAPI application
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_models.py       # Model tests
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_auth_utils.py   # Auth utility tests
│   └── test_todos.py        # Todo endpoint tests
├── .env.example             # Environment template
├── alembic.ini              # Alembic configuration
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
└── README.md                # This file
```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and write tests**
   - Follow TDD approach: write tests first
   - Maintain 80%+ code coverage

3. **Run tests and linting**
   ```bash
   pytest --cov=src
   black src tests
   ruff check src tests
   ```

4. **Create database migration if needed**
   ```bash
   alembic revision --autogenerate -m "Add new field"
   alembic upgrade head
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push origin feature/your-feature-name
   ```

## Security Considerations

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens with expiration (7 days default)
- ✅ User isolation enforced (users can only access their own todos)
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLModel parameterized queries)
- ✅ CORS configured for specific frontend origin
- ✅ Environment secrets (.env not committed)

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
python -c "from src.database import engine; engine.connect()"
```

### Migration Issues

```bash
# Reset database (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## Production Deployment

1. **Set production environment variables**
   - Use strong `AUTH_SECRET` (32+ characters)
   - Set `API_RELOAD=false`
   - Configure production `NEON_DATABASE_URL`
   - Update `FRONTEND_URL` to production domain

2. **Run migrations**
   ```bash
   alembic upgrade head
   ```

3. **Start with production server**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Use a process manager** (e.g., systemd, supervisor, or PM2)

5. **Set up reverse proxy** (e.g., nginx) for HTTPS

## API Documentation

Interactive API documentation is available when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contributing

1. Follow the established code style (black + ruff)
2. Write tests for all new features
3. Maintain 80%+ code coverage
4. Update documentation as needed
5. Create meaningful commit messages

## License

Part of the Evolution of Todo project - Phase II Full-Stack Web Application.

## Support

For issues or questions, please refer to the main project repository.
