"""
API route handlers.
"""

from src.routers.auth import router as auth_router
from src.routers.todos import router as todos_router

__all__ = ["auth_router", "todos_router"]
