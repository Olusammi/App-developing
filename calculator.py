import streamlit as st
import numpy as np
import pandas as pd
import tempfile
import os
# Import your existing local copert file
import copert 

def run_calculations(inputs):
    st.header("⚙️ Calculate Emissions")

    # 1. Unpack inputs for easier reading
    files = inputs['files']
    link_osm = inputs['link_osm']
    selected_pollutants = inputs['selected_pollutants']
    accuracy = inputs['accuracy'] # Contains: temp_corr, cold_start, temp, trip, slope
    
    # 2. Validation
    required_files = [files['pc'], files['ldv'], files['hdv'], files['moto'], link_osm,
                      files['eng_gas'], files['eng_dsl'], files['cls_gas'], 
                      files['cls_dsl'], files['moto_2s'], files['moto_4s']]
                      
    if not selected_pollutants:
        st.warning("⚠️ Please select at least one pollutant from the sidebar")
        return

    if not all(f is not None for f in required_files):
        st.info("Please ensure all required files (Parameters, Link Data, and Proportions) are uploaded.")
        return

    st.success("✅ All required files uploaded!")

    # 3. The Calculation Button
    if st.button("🚀 Calculate Multi-Pollutant Emissions", type="primary", use_container_width=True):
        with st.spinner("Computing emissions..."):
            try:
                # Create a temp directory to store the parameter CSVs so Copert class can read them
                with tempfile.TemporaryDirectory() as tmpdir:
                    pc_path = os.path.join(tmpdir, "PC_parameter.csv")
                    ldv_path = os.path.join(tmpdir, "LDV_parameter.csv")
                    hdv_path = os.path.join(tmpdir, "HDV_parameter.csv")
                    moto_path = os.path.join(tmpdir, "Moto_parameter.csv")

                    # Write uploaded bytes to temp files
                    files['pc'].seek(0); open(pc_path, 'wb').write(files['pc'].read())
                    files['ldv'].seek(0); open(ldv_path, 'wb').write(files['ldv'].read())
                    files['hdv'].seek(0); open(hdv_path, 'wb').write(files['hdv'].read())
                    files['moto'].seek(0); open(moto_path, 'wb').write(files['moto'].read())

                    # Initialize the existing COPERT logic
                    cop = copert.Copert(pc_path, ldv_path, hdv_path, moto_path)

                    # Load Data Tables
                    link_osm.seek(0)
                    # Reset all file pointers to 0 before reading
                    for key, file_obj in files.items():
                        if file_obj: file_obj.seek(0)

                    # Load Link Data
                    data_link = pd.read_csv(link_osm, sep=r'\s+', header=None, engine='python').values
                    Nlink = data_link.shape[0]

                    # Load Proportions
                    d_eng_gas = np.loadtxt(files['eng_gas'])
                    d_eng_dsl = np.loadtxt(files['eng_dsl'])
                    d_cls_gas = np.loadtxt(files['cls_gas'])
                    d_cls_dsl = np.loadtxt(files['cls_dsl'])
                    d_moto_2s = np.loadtxt(files['moto_2s'])
                    d_moto_4s = np.loadtxt(files['moto_4s'])

                    # --- LOGIC REPLICATION FROM YOUR ORIGINAL FILE ---
                    # Handle Link Columns (7 vs 9)
                    if data_link.shape[1] == 7:
                        P_ldv, P_hdv = np.zeros(Nlink), np.zeros(Nlink)
                    elif data_link.shape[1] == 9:
                        P_ldv, P_hdv = data_link[:, 7], data_link[:, 8]
                    else:
                        st.error("Link data must have 7 or 9 columns.")
                        return

                    # Setup Defaults for LDV/HDV
                    d_ldv_cls = d_cls_gas # Proxy
                    # HDV 100% Euro VI (Index 5) / Type 0
                    d_hdv_reshaped = np.zeros((Nlink, 6, 15))
                    d_hdv_reshaped[:, 5, 0] = 1.0 

                    # Initialize Emission Arrays
                    emissions_data = {}
                    pollutant_mapping = {
                        "CO": cop.pollutant_CO, "CO2": cop.pollutant_FC, 
                        "NOx": cop.pollutant_NOx, "PM": cop.pollutant_PM, 
                        "VOC": cop.pollutant_VOC, "FC": cop.pollutant_FC
                    }

                    for poll in selected_pollutants:
                        emissions_data[poll] = {
                            'pc': np.zeros(Nlink), 'ldv': np.zeros(Nlink),
                            'hdv': np.zeros(Nlink), 'moto': np.zeros(Nlink),
                            'total': np.zeros(Nlink)
                        }

                    # Progress Bar
                    prog_bar = st.progress(0)
                    
                    # --- THE LOOP ---
                    # (I am summarizing the loop here. In your actual file, 
                    # copy lines 488 to 644 from your original file exactly)
                    
                    # ... [INSERT YOUR ORIGINAL LOOP LOGIC HERE] ...
                    # Ensure you replace `ambient_temp` with `accuracy['temp']`
                    # Ensure you replace `include_cold_start` with `accuracy['cold_start']`
                    
                    # DUMMY FILLER FOR EXAMPLE (Delete this in production)
                    for poll in selected_pollutants:
                        emissions_data[poll]['total'] = np.random.rand(Nlink) * 100
                    prog_bar.progress(100)
                    
                    # --- SAVE RESULTS ---
                    st.session_state.emissions_data = emissions_data
                    st.session_state.data_link = data_link
                    st.session_state.selected_pollutants = selected_pollutants
                    
                    st.success("Calculation Finished!")

            except Exception as e:
                st.error(f"Calculation Error: {e}")
