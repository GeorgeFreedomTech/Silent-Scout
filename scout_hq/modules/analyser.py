"""
Silent Scout HQ - Analysis Engine
Provides vendor lookup, security standard mapping, and tactical risk classification.
"""

from typing import List
import sqlite3
from .utils import get_ui_config, get_vendors_db


# --- PUBLIC ANALYSIS FUNCTIONS ---

def get_vendor(mac: str) -> str:
    """
    Identifies the device manufacturer based on the MAC address OUI.
    
    Args:
        mac (str): The MAC address (BSSID) to look up.
        
    Returns:
        str: Vendor name or 'Unknown Vendor'.
    """
    vendors = get_vendors_db()
    # Normalize MAC to OUI format (first 6 hex chars, uppercase, no colons)
    oui = mac.replace(":", "").upper()[:6]
    return vendors.get(oui, "Unknown Vendor")


def get_security_label(code: int) -> str:
    """
    Maps a numeric security code to its descriptive label.
    
    Args:
        code (int): Security integer from the scan data.
        
    Returns:
        str: Human-readable security standard name.
    """
    ui_config = get_ui_config()
    standards = ui_config.get("security_standards", {})
    return standards.get(str(code), {}).get("label", f"Unknown ({code})")


def analyze_threat_tags(row: sqlite3.Row) -> str:
    """
    Analyzes an observation record and assigns tactical risk identifiers
    based on rules defined in the UI configuration JSON.
    
    Args:
        row (sqlite3.Row): A database row containing observation data.
        
    Returns:
        str: A string of pipe-separated tactical tags.
    """
    # Load analysis rules from shared configuration
    config = get_ui_config()
    rules = config.get("analysis_rules", {})
    tag_definitions = rules.get("threat_tags", {})
    
    # Prepare data for matching (normalization)
    ssid = str(row['ssid']).lower()
    vendor_name = get_vendor(row['mac']).lower()
    tags: List[str] = []

    # Dynamic Rule Processor
    for tag_id, cfg in tag_definitions.items():
        source = cfg.get("source")
        label = cfg.get("label")
        
        # 1. Keywords matching in SSID
        if source == "ssid":
            keywords = cfg.get("keywords", [])
            if any(keyword in ssid for keyword in keywords):
                tags.append(label)
        
        # 2. Keywords matching in Vendor name
        elif source == "vendor":
            keywords = cfg.get("keywords", [])
            if any(keyword in vendor_name for keyword in keywords):
                tags.append(label)
        
        # 3. Binary flag matching (Hidden, Security, etc.)
        elif source == "flag":
            field = cfg.get("field")
            expected_value = cfg.get("value")
            # Safe access to sqlite3.Row fields
            if field in row.keys() and row[field] == expected_value:
                tags.append(label)

    # Return joined tags or the default classification
    if tags:
        return " | ".join(tags)
    return rules.get("default_label", "Stationary AP")
