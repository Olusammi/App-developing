import streamlit as st
# Import your new split files directly
import ui
import content
import processing
import calculator
import visualization

st.set_page_config(page_title="Advanced Traffic Emission Calculator", layout="wide", initial_sidebar_state="expanded")

# 1. Load UI
ui.load_css()
ui.display_header()

# 2. Render Sidebar
inputs = ui.render_sidebar()

# 3. Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📖 Instructions", "📊 Data Preview", "🧮 Formula Explanation",
    "⚙️ Calculate Emissions", "📈 Multi-Metric Analysis", 
    "🗺️ Interactive Map", "📥 Download Results"
])

with tab1: content.render_instructions()
with tab2: processing.preview_data(inputs['link_osm'])
with tab3: content.render_formulas(inputs['accuracy'])
with tab4: calculator.run_calculations(inputs)
with tab5: visualization.render_analysis()
with tab6: visualization.render_map(inputs['osm_file'], inputs['map_params'])
with tab7: visualization.render_downloads(inputs['methodology'])
