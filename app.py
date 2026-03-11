"""
Root-level Flask entry point for Vercel.

Vercel looks for a Flask 'app' object in specific locations (app.py, index.py, etc.)
at the project root. This file simply re-exports the Flask app from backend/app.py
so that Vercel can discover it correctly.
"""

import os
import sys

# Add the project root to sys.path so 'backend.*' imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app  # noqa: F401  – Vercel imports 'app' from this module
