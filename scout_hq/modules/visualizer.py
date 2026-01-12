"""
Silent Scout HQ - Visualization Module
Handles UI rendering and interactive data charting.
"""

from typing import Any
import streamlit as st
import pandas as pd
import plotly.express as px
from config import CSS_STYLE_PATH
from .utils import get_ui_config


# --- PUBLIC VISUALIZATION FUNCTIONS ---

def inject_custom_css() -> None:
    """Injects external CSS styles into the Streamlit application."""
    if CSS_STYLE_PATH.exists():
        with open(CSS_STYLE_PATH, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_tactical_legends() -> None:
    """Renders signal distance and security standard legends from configuration."""
    ui = get_ui_config()
    
    # 1. Distance Legend (Signal Strength)
    dist_items = "".join([
        ui["templates"]["distance_item"].format(color=i["color"], label=i["label"]) 
        for i in ui["distance_legend"]
    ])
    st.markdown(ui["templates"]["distance_wrapper"].format(items=dist_items), unsafe_allow_html=True)

    # 2. Security Standards Legend
    with st.expander("ℹ️ Security Standards Glossary (Levels 0-6)"):
        sec_items = "".join([
            ui["templates"]["security_item"].format(label=v["label"], desc=v["desc"])
            for k, v in ui["security_standards"].items()
        ])
        st.markdown(ui["templates"]["security_grid_wrapper"].format(items=sec_items), unsafe_allow_html=True)

    # 3. Tactical Note
    with st.expander(ui["tactical_note"]["title"]):
        st.markdown(ui["tactical_note"]["content"])


def display_key_metrics(df: pd.DataFrame) -> None:
    """Displays high-level reconnaissance statistics."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Networks", len(df))
    with col2:
        hidden_count = len(df[df['hidden'] == 1])
        st.metric("Stealth (Hidden)", hidden_count)
    with col3:
        near_count = len(df[df['rssi'] > -50])
        st.metric("High Proximity", near_count, help="Devices likely within 5 meters")


def display_analytical_charts(df: pd.DataFrame) -> None:
    """Renders vendor distribution and channel load charts."""
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Manufacturer Distribution")
        v_counts = df['vendor'].value_counts().reset_index()
        v_counts.columns = ['Vendor', 'Count']
        fig_pie = px.pie(
            v_counts, values='Count', names='Vendor', 
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, width='content')
        
    with col_r:
        st.subheader("RF Channel Occupation")
        # Ensure all channels 1-13 are represented
        ch_counts = df['channel'].value_counts().reindex(range(1, 14), fill_value=0).reset_index()
        ch_counts.columns = ['Channel', 'Net Count']
        fig_bar = px.bar(
            ch_counts, x='Channel', y='Net Count', 
            color='Net Count',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))
        st.plotly_chart(fig_bar, width='content')


def _style_rssi_cells(val: Any) -> str:
    """Helper for dataframe styling based on signal strength."""
    if not isinstance(val, (int, float)):
        return ''
    if val > -50:
        return 'background-color: #ff4b4b; color: white; font-weight: bold'
    elif val > -75:
        return 'background-color: #ffa500; color: black'
    else:
        return 'background-color: #28a745; color: white'


def display_observation_table(df: pd.DataFrame) -> None:
    """Renders the main tactical observation data table with signal styling."""
    st.subheader("Tactical Observation Log")
    render_tactical_legends()
    
    # Selection and renaming for display
    df_display = df.sort_values(by='rssi', ascending=False)[
        ['ssid', 'mac', 'rssi', 'analysis', 'security_text', 'channel']
    ]
    df_display.columns = ['SSID', 'MAC Address', 'Signal (dBm)', 'Tactical Analysis', 'Security', 'Channel']
    
    # Applying visual styles to the dataframe
    st.dataframe(
        df_display.style.map(_style_rssi_cells, subset=['Signal (dBm)']), 
        width='content', 
        hide_index=True
    )


def render_footer() -> None:
    """Renders a footer with dynamic links from configuration."""
    ui = get_ui_config()
    
    link_items = [
        ui["templates"]["footer_link"].format(
            url=link["url"], 
            icon=link["icon"], 
            label=link["label"]
        ) for link in ui["footer"]["links"]
    ]
    
    content = f"{ui['footer']['text']}<br>{' '.join(link_items)}"
    footer_html = ui["templates"]["footer_wrapper"].format(content=content)
    
    st.markdown(footer_html, unsafe_allow_html=True)