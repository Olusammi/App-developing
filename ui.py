import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 10px 0; }
        .formula-box { background-color: #f0f2f6; padding: 15px; border-left: 4px solid #667eea; border-radius: 5px; font-family: 'Courier New', monospace; }
        .stAlert { background-color: #e7f3ff; }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    st.title("🚗 Advanced Traffic Emission Calculator")
    st.caption("Multi-Standard Emission Analysis with COPERT IV, IPCC, and EPA Methodologies")
    st.markdown("---")

def render_sidebar():
    st.sidebar.header("📊 Emission Metrics Selection")
    
    pollutants_available = {
        "CO": {"name": "Carbon Monoxide", "unit": "g/km", "standard": "COPERT IV", "color": "#ef4444"},
        "CO2": {"name": "Carbon Dioxide", "unit": "g/km", "standard": "IPCC", "color": "#3b82f6"},
        "NOx": {"name": "Nitrogen Oxides", "unit": "g/km", "standard": "COPERT IV", "color": "#f59e0b"},
        "PM": {"name": "Particulate Matter", "unit": "mg/km", "standard": "WHO", "color": "#8b5cf6"},
        "VOC": {"name": "Volatile Organic Compounds", "unit": "g/km", "standard": "COPERT IV", "color": "#10b981"},
        "FC": {"name": "Fuel Consumption", "unit": "L/100km", "standard": "NEDC/WLTP", "color": "#f97316"}
    }

    selected_pollutants = st.sidebar.multiselect(
        "Select Pollutants", list(pollutants_available.keys()), default=["CO", "NOx", "PM"]
    )

    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Calculation Methodology")
    calc_method = st.sidebar.selectbox("Select Standard", ["COPERT IV (EU)", "IPCC Tier 2", "EPA MOVES (US)", "Hybrid"])

    st.sidebar.markdown("---")
    st.sidebar.header("🎯 Accuracy Settings")
    temp_corr = st.sidebar.checkbox("Temperature Correction", value=True)
    cold_start = st.sidebar.checkbox("Cold Start Emissions", value=True)
    slope_corr = st.sidebar.checkbox("Road Slope Correction", value=False)
    
    ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", -10, 40, 25) if temp_corr else 20
    trip_length = st.sidebar.slider("Trip Length (km)", 1, 50, 10) if cold_start else 10
    road_slope = st.sidebar.slider("Road Slope (%)", -6, 6, 0) if slope_corr else 0

    # File Uploads
    st.sidebar.header("📂 Upload Input Files")
    with st.sidebar.expander("COPERT Parameters", expanded=True):
        pc = st.file_uploader("PC Param CSV", key='pc')
        ldv = st.file_uploader("LDV Param CSV", key='ldv')
        hdv = st.file_uploader("HDV Param CSV", key='hdv')
        moto = st.file_uploader("Moto Param CSV", key='moto')

    with st.sidebar.expander("Data Files", expanded=True):
        link_osm = st.file_uploader("Link OSM Data", key='link')
        osm_file = st.file_uploader("OSM Network File", key='osm')

    with st.sidebar.expander("Proportions", expanded=False):
        eng_gas = st.file_uploader("Engine Cap Gas", key='ecg')
        eng_dsl = st.file_uploader("Engine Cap Diesel", key='ecd')
        cls_gas = st.file_uploader("Class Gas", key='ccg')
        cls_dsl = st.file_uploader("Class Diesel", key='ccd')
        moto_2s = st.file_uploader("2-Stroke", key='2s')
        moto_4s = st.file_uploader("4-Stroke", key='4s')
    
    # Map Params
    st.sidebar.header("🗺️ Map Parameters")
    c1, c2 = st.sidebar.columns(2)
    x_min = c1.number_input("X Min", 3.37310, format="%.5f")
    x_max = c2.number_input("X Max", 3.42430, format="%.5f")
    y_min = c1.number_input("Y Min", 6.43744, format="%.5f")
    y_max = c2.number_input("Y Max", 6.46934, format="%.5f")
    tol = st.sidebar.number_input("Tolerance", 0.005, format="%.3f")
    ncore = st.sidebar.number_input("Number of Cores", min_value=1, max_value=16, value=8)

    return {
        "pollutants_available": pollutants_available,
        "selected_pollutants": selected_pollutants,
        "methodology": calc_method,
        "accuracy": {"temp_corr": temp_corr, "cold_start": cold_start, "temp": ambient_temp, "trip": trip_length},
        "files": {
            "pc": pc, "ldv": ldv, "hdv": hdv, "moto": moto, 
            "eng_gas": eng_gas, "eng_dsl": eng_dsl, "cls_gas": cls_gas, "cls_dsl": cls_dsl, 
            "moto_2s": moto_2s, "moto_4s": moto_4s
        },
        "link_osm": link_osm,
        "osm_file": osm_file,
        "map_params": {"xmin": x_min, "xmax": x_max, "ymin": y_min, "ymax": y_max, "tol": tol, "ncore": ncore}
    }
