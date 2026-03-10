"""
Physics Motion Simulator — Flask Entry Point
Registers all API blueprints and serves the frontend as static files.
"""

import os
import sys

# Ensure the repo root is in sys.path so 'backend.*' package imports resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.api.projectile import projectile_bp
from backend.api.pendulum import pendulum_bp
from backend.api.presets import presets_bp

# Static folder points to ../frontend relative to this file
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# Register blueprints
app.register_blueprint(projectile_bp, url_prefix='/api/projectile')
app.register_blueprint(pendulum_bp,   url_prefix='/api/pendulum')
app.register_blueprint(presets_bp,    url_prefix='/api/presets')


# ── Static file serving ──────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main frontend page."""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve any other static asset (CSS, JS, images, etc.)."""
    return send_from_directory(FRONTEND_DIR, path)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    print("=" * 60)
    print("Physics Motion Simulator — Backend Starting")
    print("=" * 60)
    print(f"Frontend served from: {os.path.abspath(FRONTEND_DIR)}")
    print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
    print("Server running at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
