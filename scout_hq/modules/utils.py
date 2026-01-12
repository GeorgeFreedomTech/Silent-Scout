"""
Silent Scout HQ - Shared Utilities
Centralized logic for data loading, caching, and common I/O helpers.
Adheres to the DRY principle (Don't Repeat Yourself).
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any
import streamlit as st
from config import (
    UI_CONTENT_JSON, 
    VENDORS_JSON, 
    DATABASE_DIR, 
    INBOX_DIR, 
    STATIC_DIR, 
    ASSETS_DIR
    )


# --- GENERIC LOADERS ---

@lru_cache(maxsize=4)
def _load_json_file(path: Path) -> Dict[str, Any]:
    """
    Generic, cached loader for JSON files.
    Safely handles missing files by returning an empty dict.
    
    Args:
        path (Path): Path to the JSON file.

    Returns:
        Dict[str, Any]: Parsed JSON data or empty dict if file missing.
    """
    if not path.exists():
        return {}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {path}: {e}")
        return {}

# --- PUBLIC ACCESSORS ---

def get_ui_config() -> Dict[str, Any]:
    """
    Retrieves the UI configuration (texts, legends, templates).
    Cached via _load_json_file.
    """
    return _load_json_file(UI_CONTENT_JSON)


def get_vendors_db() -> Dict[str, str]:
    """
    Retrieves the MAC Address OUI database.
    Cached via _load_json_file.
    """
    return _load_json_file(VENDORS_JSON)

# --- ENVIRONMENT INITIALIZATION ---
@st.cache_resource
def setup_project_structure() -> None:
    """Ensures all required directory paths exist."""
    for folder in [DATABASE_DIR, INBOX_DIR, STATIC_DIR, ASSETS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)