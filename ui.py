import streamlit as st
import os
from io import BytesIO

def load_css():
    """
    Injects custom CSS for better styling of metrics and alerts.
    """
    st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        }
        .formula-box {
            background-color: #f0f2f6;
            padding: 15px;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
        }
        .stAlert {
            background-color: #e7f3ff;
        }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """
    Renders the main application header and title.
    """
    st.title("🚗 Advanced Traffic Emission Calculator")
    st.caption("Multi-Standard Emission Analysis with COPERT IV, IPCC, and EPA Methodologies")
    st.markdown("---")

def get_input_file(label, key, default_filename):
    """
    Creates a file uploader. If no file is uploaded, it loads the default
    file from the 'defaults' folder and returns it as a BytesIO object.
    """
    uploaded = st.file_uploader(label, key=key)
    
    if uploaded is not None:
        return uploaded
    
    # If nothing uploaded, look for default in the 'defaults' folder
    default_path = os.path.join("defaults", default_filename)
    
    if os.path.exists(default_path):
        # Display a subtle indicator that default data is being used
        st.caption(f"✅ *Using default: {default_filename}*")
        with open(default_path, "rb") as f:
            # Read into memory to mimic a Streamlit UploadedFile
            return BytesIO(f.read())
    else:
        # Default file missing - this will be caught during validation in calculator.py
        # You might want to log this or just return None
        return None

def render_sidebar():
    """
    Renders the sidebar components: Pollutant selection, Methodology, 
    Accuracy settings, File uploads, and Map parameters.
    Returns a dictionary containing all user inputs.
    """
    
    # ==================== EMISSION METRICS SELECTION ====================
    st.sidebar.header("📊 Emission Metrics Selection")
    st.sidebar.markdown("Select which pollutants to calculate and analyze")

    pollutants_available = {
        "CO": {"name": "Carbon Monoxide", "unit": "g/km", "standard": "COPERT IV", "color": "#ef4444"},
        "CO2": {"name": "Carbon Dioxide", "unit": "g/km", "standard": "IPCC", "color": "#3b82f6"},
        "NOx": {"name": "Nitrogen Oxides", "unit": "g/km", "standard": "COPERT IV", "color": "#f59e0b"},
        "PM": {"name": "Particulate Matter", "unit": "mg/km", "standard": "WHO", "color": "#8b5cf6"},
        "VOC": {"name": "Volatile Organic Compounds", "unit": "g/km", "standard": "COPERT IV", "color": "#10b981"},
        "FC": {"name": "Fuel Consumption", "unit": "L/100km", "standard": "NEDC/WLTP", "color": "#f97316"}
    }

    selected_pollutants = st.sidebar.multiselect(
        "Select Pollutants to Calculate",
        options=list(pollutants_available.keys()),
        default=["CO", "NOx", "PM"],
        help="Choose one or more pollutants for emission calculation"
    )

    # Display info about selected pollutants
    if selected_pollutants:
        st.sidebar.markdown("### Selected Metrics Info")
        for pollutant in selected_pollutants:
            info = pollutants_available[pollutant]
            st.sidebar.markdown(f"""
            <div style='background-color: {info['color']}22; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid {info["color"]}'>
                <strong>{pollutant}</strong>: {info['name']}<br>
                <small>Standard: {info['standard']}</small><br>
                <small>Unit: {info['unit']}</small>
            </div>
            """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # ==================== METHODOLOGY & ACCURACY ====================
    st.sidebar.header("⚙️ Methodology & Accuracy")
    
    calculation_method = st.sidebar.selectbox(
        "Select Calculation Standard",
        ["COPERT IV (EU)", "IPCC Tier 2", "EPA MOVES (US)", "Hybrid (Multi-standard)"],
        help="Choose the international standard for emission calculations"
    )

    st.sidebar.subheader("Correction Factors")
    include_temperature_correction = st.sidebar.checkbox("Temperature Correction", value=True)
    include_cold_start = st.sidebar.checkbox("Cold Start Emissions", value=True)
    include_slope_correction = st.sidebar.checkbox("Road Slope Correction", value=False)

    # Conditional Sliders
    if include_temperature_correction:
        ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", -10, 40, 25)
    else:
        ambient_temp = 20

    if include_cold_start:
        trip_length = st.sidebar.slider("Average Trip Length (km)", 1, 50, 10)
    else:
        trip_length = 10

    if include_slope_correction:
        road_slope = st.sidebar.slider("Road Slope (%)", -6, 6, 0)
    else:
        road_slope = 0

    st.sidebar.markdown("---")

    # ==================== FILE UPLOADS (WITH DEFAULTS) ====================
    st.sidebar.header("📂 Input Data")
    st.sidebar.info("ℹ️ Default data is pre-loaded. Upload files only if you wish to override specific data.")

    # Group 1: COPERT Parameters
    with st.sidebar.expander("COPERT Parameter Files", expanded=False):
        pc_param = get_input_file("PC Parameter CSV", 'pc', "PC_parameter.csv")
        ldv_param = get_input_file("LDV Parameter CSV", 'ldv', "LDV_parameter.csv")
        hdv_param = get_input_file("HDV Parameter CSV", 'hdv', "HDV_parameter.csv")
        moto_param = get_input_file("Moto Parameter CSV", 'moto', "Moto_parameter.csv")

    # Group 2: Network Data
    with st.sidebar.expander("Network Data Files", expanded=True):
        link_osm = get_input_file("Link OSM Data (.dat/.csv/txt)", 'link', "link_osm.dat") 
        osm_file = get_input_file("OSM Network File (.osm)", 'osm', "selected_zone-lagos.osm")

    # Group 3: Proportions
    with st.sidebar.expander("Proportion Data Files", expanded=False):
        engine_cap_gas = get_input_file("Engine Cap Gasoline", 'ecg', "engine_capacity_gasoline.dat")
        engine_cap_diesel = get_input_file("Engine Cap Diesel", 'ecd', "engine_capacity_diesel.dat")
        copert_class_gas = get_input_file("COPERT Class Gasoline", 'ccg', "copert_class_gasoline.dat")
        copert_class_diesel = get_input_file("COPERT Class Diesel", 'ccd', "copert_class_diesel.dat")
        copert_2stroke = get_input_file("2-Stroke Motorcycle", '2s', "copert_class_proportion_2_stroke_motorcycle_more_50.dat")
        copert_4stroke = get_input_file("4-Stroke Motorcycle", '4s', "copert_class_proportion_4_stroke_motorcycle_50_250.dat")

    st.sidebar.markdown("---")

    # ==================== MAP PARAMETERS ====================
    st.sidebar.header("🗺️ Map Parameters")
    st.sidebar.markdown("**Domain Boundaries**")
    col1, col2 = st.sidebar.columns(2)
    
    # Using keyword arguments to prevent ordering errors
    x_min = col1.number_input("X Min (Lon)", value=3.37310, format="%.5f")
    x_max = col2.number_input("X Max (Lon)", value=3.42430, format="%.5f")
    y_min = col1.number_input("Y Min (Lat)", value=6.43744, format="%.5f")
    y_max = col2.number_input("Y Max (Lat)", value=6.46934, format="%.5f")
    
    tolerance = st.sidebar.number_input("Tolerance", value=0.005, format="%.3f")
    
    # FIX: Explicitly setting min_value, max_value, and value to avoid StreamlitValueAboveMaxError
    ncore = st.sidebar.number_input("Number of Cores", min_value=1, max_value=16, value=8)

    # Return all gathered inputs as a dictionary
    return {
        "pollutants_available": pollutants_available,
        "selected_pollutants": selected_pollutants,
        "methodology": calculation_method,
        "accuracy": {
            "include_temperature_correction": include_temperature_correction,
            "include_cold_start": include_cold_start,
            "include_slope_correction": include_slope_correction,
            "ambient_temp": ambient_temp,
            "trip_length": trip_length,
            "road_slope": road_slope
        },
        "files": {
            "pc": pc_param,
            "ldv": ldv_param,
            "hdv": hdv_param,
            "moto": moto_param,
            "eng_gas": engine_cap_gas,
            "eng_dsl": engine_cap_diesel,
            "cls_gas": copert_class_gas,
            "cls_dsl": copert_class_diesel,
            "moto_2s": copert_2stroke,
            "moto_4s": copert_4stroke
        },
        "link_osm": link_osm,
        "osm_file": osm_file,
        "map_params": {
            "xmin": x_min,
            "xmax": x_max,
            "ymin": y_min,
            "ymax": y_max,
            "tol": tolerance,
            "ncore": ncore
        }
    }
