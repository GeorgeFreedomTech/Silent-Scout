"""
Silent Scout HQ - Database Management Module
Handles SQLite operations and provides cached data for the Streamlit UI.
"""

import sqlite3
import pandas as pd
import streamlit as st
from typing import List, Tuple, Any
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_resource
def init_db() -> None:
    """Initializes the local database schema and performance indices."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                id_loc INTEGER,
                ssid TEXT,
                mac TEXT,
                rssi INTEGER,
                channel INTEGER,
                hidden INTEGER,
                security INTEGER
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_mac ON observations (mac)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ssid ON observations (ssid)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_id_loc ON observations (id_loc)')
        conn.commit()
    print("[DB] Database initialized and performance indices verified.")


def save_to_db(data_list: List[Tuple[Any, ...]]) -> int:
    """Saves a batch of scan results into the database (Used by ingest.py)."""
    if not data_list:
        return 0

    query = '''
        INSERT INTO observations (timestamp, id_loc, ssid, mac, rssi, channel, hidden, security)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, data_list)
            conn.commit()
            return len(data_list)
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to batch insert records: {e}")
        return 0


@st.cache_data
def load_database() -> pd.DataFrame:
    """
    Loads the entire observations table into a Pandas DataFrame.
    Cached to ensure single-time disk access for optimal performance in environments.
    """
    with get_connection() as conn:
        return pd.read_sql("SELECT * FROM observations", conn)