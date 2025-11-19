import streamlit as st
import ui
import content
import processing
import calculator
import visualization
import numpy as np # Keep necessary imports for potential use in other modules
import matplotlib # Keep necessary imports for potential use in other modules

# Set Matplotlib backend (good practice for Streamlit)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.colorbar
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import tempfile
import os
import zipfile
from io import BytesIO

# Page Config
st.set_page_config(page_title="Advanced Traffic Emission Calculator", layout="wide", initial_sidebar_state="expanded")

# 1. Load UI & CSS
ui.load_css()
ui.display_header()

# 2. Render Sidebar & Get Inputs
inputs = ui.render_sidebar()

# 3. Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📖 Instructions",
    "📊 Data Preview",
    "🧮 Formula Explanation",
    "⚙️ Calculate Emissions",
    "📈 Multi-Metric Analysis",
    "🗺️ Interactive Map",
    "📥 Download Results"
])

# --- TAB LOGIC ---

# Tab 1: Instructions
with tab1:
    content.render_instructions()

# Tab 2: Data Preview
with tab2:
    # We pass the file object for the Link Data for preview
    # NOTE: 'link_osm' is the key we used in ui.py to capture the Link data file object
    processing.preview_data(inputs['link_osm'])

# Tab 3: Formulas
with tab3:
    # FIX: We now pass BOTH the 'accuracy' settings AND the 'pollutants_available'
    # dictionary, as required by the updated content.render_formulas function.
    content.render_formulas(inputs['accuracy'], inputs['pollutants_available'])

# Tab 4: Calculation (The Core Logic)
with tab4:
    calculator.run_calculations(inputs)

# Tab 5: Analysis
with tab5:
    visualization.render_analysis()

# Tab 6: Map
with tab6:
    visualization.render_map(inputs['osm_file'], inputs['map_params'])

# Tab 7: Download
with tab7:
    visualization.render_downloads(inputs['methodology'], inputs['selected_pollutants'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Advanced Traffic Emission Calculator v2.0</strong></p>
    <p>Built with COPERT IV, IPCC, and EPA MOVES methodologies</p>
</div>
""", unsafe_allow_html=True)
