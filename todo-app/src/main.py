#!/usr/bin/env python3
"""Evolution of Todo - Phase I

A simple console-based todo application with in-memory storage.
Run this module directly or use 'python -m src.main'
"""

import sys
from pathlib import Path

# Ensure project root is in path regardless of CWD
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.cli.menu import Menu
from src.services.task_service import TaskService


def main():
    """Application entry point."""
    service = TaskService()
    menu = Menu(service)
    menu.run()


if __name__ == "__main__":
    main()
