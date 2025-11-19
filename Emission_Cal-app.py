import streamlit as st
from modules import ui, content, processing, calculator, visualization

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

# Tab 1: Instructions
with tab1:
    content.render_instructions()

# Tab 2: Data Preview
with tab2:
    processing.preview_data(inputs['link_osm'])

# Tab 3: Formulas
with tab3:
    content.render_formulas(inputs['accuracy'])

# Tab 4: Calculation (The Core Logic)
with tab4:
    # This function handles the button click and processing internally
    calculator.run_calculations(inputs)

# Tab 5: Analysis
with tab5:
    visualization.render_analysis()

# Tab 6: Map
with tab6:
    visualization.render_map(inputs['osm_file'], inputs['map_params'])

# Tab 7: Download
with tab7:
    visualization.render_downloads(inputs['methodology'])
