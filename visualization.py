import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from io import BytesIO
import zipfile

def render_analysis():
    """
    Renders the analysis tab, showing charts and key metrics.
    Uses st.session_state['results_df'] (created in calculator.py).
    """
    st.header("📈 Multi-Metric Analysis")
    st.markdown("Visualize emission results using interactive charts.")

    if 'results_df' in st.session_state and not st.session_state['results_df'].empty:
        df = st.session_state['results_df']
        
        # --- Key Metrics ---
        st.subheader("Global Emission Totals")
        metric_cols = st.columns(len(st.session_state['selected_pollutants']))
        
        for i, poll in enumerate(st.session_state['selected_pollutants']):
            # Assumes 'Total_{Pollutant}' columns are created in calculator.py
            col_name = f'Total_{poll}'
            if col_name in df.columns:
                total_emission = df[col_name].sum()
                unit = 'g' if poll != 'CO2' and poll != 'FC' else ('kg' if poll == 'CO2' else 'L')
                
                with metric_cols[i]:
                    st.metric(
                        label=f"Total {poll}",
                        value=f"{total_emission:.2f} {unit}"
                    )
        
        st.markdown("---")
        
        # --- Breakdown by Vehicle Type (Example Chart) ---
        st.subheader("Emission Breakdown by Vehicle Type")
        
        # Aggregate total emissions for each vehicle type/pollutant
        # Example: ['PC_CO', 'LDV_CO', 'HDV_CO', 'Moto_CO', 'Total_CO']
        
        # Filter for the relevant total columns
        cols_to_plot = [c for c in df.columns if any(vt in c for vt in ['PC_', 'LDV_', 'HDV_', 'Moto_']) and 'Total' in c]
        
        if cols_to_plot:
            emission_totals = df[cols_to_plot].sum().reset_index()
            emission_totals.columns = ['Metric', 'Value']
            
            # Parse the Metric name (e.g., 'PC_Total_CO' -> Type: PC, Pollutant: CO)
            emission_totals['Vehicle Type'] = emission_totals['Metric'].apply(lambda x: x.split('_')[0])
            emission_totals['Pollutant'] = emission_totals['Metric'].apply(lambda x: x.split('_')[-1])

            # Create an interactive stacked bar chart
            fig = px.bar(
                emission_totals,
                x='Pollutant',
                y='Value',
                color='Vehicle Type',
                title='Total Emissions Contribution by Vehicle Type and Pollutant',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("No calculated results found for vehicle type breakdown.")

    else:
        st.info("Calculate emissions first in the 'Calculate Emissions' tab to view analysis.")

def render_map(osm_file, map_params):
    """
    Renders the interactive map tab.
    Currently uses placeholder map logic since the full OSM processing is complex.
    """
    st.header("🗺️ Interactive Map Visualization")

    if osm_file is None:
        st.info("Please upload an OSM map file (.osm) in the sidebar to render the map.")
        return
    
    if 'results_df' not in st.session_state or st.session_state['results_df'].empty:
        st.info("Please run the calculation first to visualize link-specific emission data.")
        return

    st.subheader("Select Map Metric")
    
    # Allow user to select a total emission column to visualize on the map
    df = st.session_state['results_df']
    default_cols = [c for c in df.columns if c.startswith('Total_')]
    
    selected_metric = st.selectbox(
        "Metric to Display on Map:",
        options=default_cols,
        index=0 if default_cols else None
    )

    if selected_metric:
        st.warning(f"Map visualization is currently a placeholder. To integrate a real map, you need to process the OSM file ({osm_file.name}) and link the calculated {selected_metric} results back to the geographic coordinates (latitude/longitude) of each OSM_ID. This often requires libraries like OSMnx or custom GIS processing.")
        
        # --- Placeholder Map ---
        # Display a simple, non-functional placeholder to show the intent
        st.markdown("#### Placeholder Map Area")
        st.image("https://via.placeholder.com/800x400.png?text=Interactive+Map+Placeholder", use_container_width=True)
        st.caption("Imagine this map shows the road links colored by the selected emission metric's intensity.")
    else:
        st.info("No calculated metrics available to map.")


def render_downloads(methodology, selected_pollutants):
    """
    Creates the downloadable results package.
    """
    st.header("📥 Download Results")

    if 'results_df' in st.session_state and not st.session_state['results_df'].empty:
        df = st.session_state['results_df']
        
        st.subheader("Download CSV Results")
        
        # 1. Download CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Emission Results CSV",
            data=csv_data,
            file_name="emission_results.csv",
            mime="text/csv",
            key='download_csv',
            use_container_width=True
        )

        st.markdown("---")
        
        # 2. Create ZIP Package
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add the main CSV results
            zf.writestr("emission_results.csv", csv_data)

            # Add a metadata/report file
            summary = (
                f"Advanced Traffic Emission Analysis Report\n"
                f"Methodology: {methodology}\n"
                f"Pollutants Calculated: {', '.join(selected_pollutants)}\n"
                f"Number of Road Links: {len(df)}\n"
                f"Date Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"\n"
                f"Note: This file is a key to the data in 'emission_results.csv'.\n"
            )
            zf.writestr("report_metadata.txt", summary.encode('utf-8'))

        # Rewind the buffer to the start
        buffer.seek(0)

        st.markdown("### ⬇️ Download Package")
        
        # Download button for the ZIP file
        st.download_button(
            label="Download Complete ZIP Report",
            data=buffer,
            file_name="traffic_emission_analysis.zip",
            mime="application/zip",
            key='download_zip_complete',
            use_container_width=True
        )
        
        st.markdown("---")
        st.markdown("### 📚 Export Formats")
        st.info(f"""
        **Available Export Formats:**
        - **CSV**: Main results for spreadsheet applications (`emission_results.csv`)
        - **ZIP**: Complete analysis package (containing the CSV, metadata, and methodology details)
        
        **Methodology Used:**
        The current download package is based on the **{methodology}** standard and includes data for **{', '.join(selected_pollutants)}**.
        """)
    else:
        st.info("Calculate emissions first in the 'Calculate Emissions' tab to create download package.")
