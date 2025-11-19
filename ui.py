import streamlit as st
import os
from io import BytesIO
import pandas as pd

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
    
    ***FIXED: Uses st.sidebar.file_uploader to ensure widget stays in the sidebar.***
    """
    uploaded = st.sidebar.file_uploader(label, key=key) # <--- THIS IS THE CRITICAL CHANGE
    
    if uploaded is not None:
        return uploaded
    else:
        # Since we can't access local files, we return None and let the app
        # handle the 'use defaults' logic by checking for None.
        st.sidebar.info(f"Using default file for: **{default_filename}**")
        return None


def render_sidebar():
    """
    Renders the entire sidebar and gathers all user inputs and settings.
    """
    st.sidebar.header("🛠️ Input & Settings")

    # --- 1. File Uploads (Parameters) ---
    st.sidebar.subheader("1. Emission Parameter Files (.csv)")
    st.sidebar.info("Upload your COPERT-like parameter files or use defaults.")
    
    # All these calls will now correctly place the uploader in the sidebar
    pc_param = get_input_file("PC Parameters", "pc_param_key", "PC_Params.csv")
    ldv_param = get_input_file("LDV Parameters", "ldv_param_key", "LDV_Params.csv")
    hdv_param = get_input_file("HDV Parameters", "hdv_param_key", "HDV_Params.csv")
    moto_param = get_input_file("Motorcycle Parameters", "moto_param_key", "Moto_Params.csv")
    
    # Engine & Class Proportions
    engine_cap_gas = get_input_file("Gasoline Engine Capacity Proportions", "eng_gas_key", "Engine_Gas.csv")
    engine_cap_diesel = get_input_file("Diesel Engine Capacity Proportions", "eng_dsl_key", "Engine_Diesel.csv")
    copert_class_gas = get_input_file("Gasoline COPERT Class Proportions", "cls_gas_key", "Class_Gas.csv")
    copert_class_diesel = get_input_file("Diesel COPERT Class Proportions", "cls_dsl_key", "Class_Diesel.csv")
    copert_2stroke = get_input_file("2-Stroke Moto Proportions", "moto_2s_key", "Moto_2Stroke.csv")
    copert_4stroke = get_input_file("4-Stroke Moto Proportions", "moto_4s_key", "Moto_4Stroke.csv")

    st.sidebar.markdown("---")
    
    # --- 2. Traffic Data Uploads ---
    st.sidebar.subheader("2. Traffic and Link Data (.txt)")
    # These still use st.sidebar.file_uploader directly, which is correct
    link_osm = st.sidebar.file_uploader("Upload Link Data (OSM_ID, Length, Flow, Speed, Proportions...)", key="link_data_key")
    osm_file = st.sidebar.file_uploader("Upload OSM Map File (.osm)", key="osm_map_key")
    st.sidebar.markdown("---")

    # --- 3. Pollutant Selection ---
    st.sidebar.subheader("3. Calculation Metrics")
    pollutants_available = {
        "CO": "Carbon Monoxide",
        "CO2": "Carbon Dioxide",
        "NOx": "Nitrogen Oxides",
        "PM": "Particulate Matter",
        "VOC": "Volatile Organic Compounds",
        "FC": "Fuel Consumption (L/km)"
    }
    
    selected_pollutants = st.sidebar.multiselect(
        "Select Pollutants to Calculate",
        options=list(pollutants_available.keys()),
        default=["CO2", "NOx", "FC", "PM"],
        format_func=lambda x: f"{x} ({pollutants_available[x]})"
    )
    
    calculation_method = st.sidebar.selectbox(
        "Select Base Methodology",
        options=["COPERT IV Standard", "IPCC Fuel-Based (CO2 only)", "EPA MOVES Hybrid"],
        index=0
    )

    st.sidebar.markdown("---")

    # --- 4. Accuracy Settings ---
    st.sidebar.subheader("4. Accuracy Corrections")
    
    include_temperature_correction = st.sidebar.checkbox("Include Temperature Correction", value=True)
    ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", min_value=-10.0, max_value=40.0, value=20.0, step=0.5, disabled=not include_temperature_correction)
    
    include_cold_start = st.sidebar.checkbox("Include Cold Start Emissions", value=False)
    trip_length = st.sidebar.number_input("Average Trip Length (km)", min_value=1.0, value=7.0, disabled=not include_cold_start)
    
    include_slope_correction = st.sidebar.checkbox("Include Road Slope Correction", value=False)
    road_slope = st.sidebar.slider("Average Road Slope (%)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1, disabled=not include_slope_correction)

    st.sidebar.markdown("---")
    
    # --- 5. Advanced Settings ---
    st.sidebar.subheader("5. Advanced Solver Settings")
    
    tolerance = st.sidebar.number_input("Tolerance", value=0.005, format="%.3f")
    
    # Explicitly setting min_value, max_value, and value to avoid StreamlitValueAboveMaxError
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
            "ncore": ncore,
            "tolerance": tolerance
        }
    }
