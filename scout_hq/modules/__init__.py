"""
Silent Scout HQ - Modules Package
Consolidates database management, analysis, and UI visualization 
into a unified API.
"""

# Database Management
from .db_manager import (
    get_connection,
    init_db,
    save_to_db,
    load_database
)

# Tactical Analysis Engine
from .analyser import (
    get_vendor,
    get_security_label,
    analyze_threat_tags
)

# UI Visualization and Rendering
from .visualizer import (
    inject_custom_css,
    display_key_metrics,
    display_analytical_charts,
    display_observation_table,
    render_footer
)

from .utils import setup_project_structure