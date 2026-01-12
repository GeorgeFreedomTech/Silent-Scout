"""
Silent Scout HQ - Configuration Module
Defines the project structure, project identity, and ensures environment readiness.
Optimized for local development and Streamlit Cloud deployment.
"""

from pathlib import Path

# --- PROJECT IDENTITY ---
PROJECT_NAME: str = "Silent Scout HQ"

# --- BASE DIRECTORIES ---

# Absolute path to the project root (scout-hq/)
ROOT_DIR: Path = Path(__file__).parent.absolute()

# Core directory mapping
ASSETS_DIR: Path = ROOT_DIR / "assets"
DATA_DIR: Path = ROOT_DIR / "data"

# Data sub-directory structure (Logical separation of concerns)
DATABASE_DIR: Path = DATA_DIR / "database"
INBOX_DIR: Path    = DATA_DIR / "inbox"
STATIC_DIR: Path   = DATA_DIR / "static"

# --- FILE PATHS ---

# Asset paths (UI styling)
CSS_STYLE_PATH: Path = ASSETS_DIR / "style.css"

# Storage and Database paths
DB_PATH: Path        = DATABASE_DIR / "scout.db"

# Source reference for the ingest process
SOURCE_CSV: Path     = INBOX_DIR / "scout_vault.csv"

# Static Reference Data (JSON intelligence layers)
VENDORS_JSON: Path    = STATIC_DIR / "vendors.json"
UI_CONTENT_JSON: Path = STATIC_DIR / "ui_content.json"
