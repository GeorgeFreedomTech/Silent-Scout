"""
Silent Scout HQ - Main Application Entry Point
Orchestrates the Streamlit dashboard using a single-load cached database strategy.
"""

import streamlit as st
from config import PROJECT_NAME
from modules import (
    inject_custom_css,
    setup_project_structure,
    init_db, 
    load_database,
    get_vendor, 
    get_security_label, 
    analyze_threat_tags,
    display_key_metrics,
    display_analytical_charts,
    display_observation_table,
    render_footer
)

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title=PROJECT_NAME, page_icon="📡", layout="wide")


def main() -> None:
    """
    Main execution flow for the Silent Scout HQ Dashboard.
    """
    # --- SETUP & INITIALIZATION ---
    # Inject custom CSS styles
    inject_custom_css()

    # Automatically ensure environment readiness upon module import
    setup_project_structure()

    # --- APPLICATION ---
    st.title(f"📡 {PROJECT_NAME}")
    
    # Ensure database schema exists
    init_db()
    
    # 1. INITIAL DATABASE LOAD (One-time cached load)
    master_df = load_database()
    
    if master_df.empty: # Handle empty database case
        st.info("The data vault is currently empty. Please ingest Agent data to begin.")
        return

    # 2. SIDEBAR FILTERING (Handled entirely in RAM via Pandas)
    # Get unique localities sorted for selection
    unique_locs = sorted(master_df['id_loc'].unique(), reverse=True)
    selected_loc = st.sidebar.selectbox("Target Locality ID", unique_locs)
    
    # Filter available timestamps for the selected locality
    loc_mask = master_df['id_loc'] == selected_loc
    unique_times = sorted(master_df[loc_mask]['timestamp'].unique(), reverse=True)
    selected_time = st.sidebar.selectbox("Operation Scan (Timestamp)", unique_times)

    # 3. DATA SELECTION
    # Filter the master dataframe for the final mission view
    df = master_df[(loc_mask) & (master_df['timestamp'] == selected_time)].copy()

    # 4. DATA ENRICHMENT
    df['vendor'] = df['mac'].apply(get_vendor)
    df['security_text'] = df['security'].apply(get_security_label)
    df['analysis'] = df.apply(analyze_threat_tags, axis=1)

    # 5. UI RENDERING
    display_key_metrics(df) # High-level stats
    st.divider()
    display_analytical_charts(df) # Interactive charts
    st.divider()
    display_observation_table(df) # Detailed data table
    render_footer()

if __name__ == "__main__":
    main()