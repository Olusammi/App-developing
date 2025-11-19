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
    Currently uses placeholder data; replace with actual calculation results
    from st.session_state['results_df'].
    """
    st.header("📈 Multi-Metric Analysis")
    st.markdown("Visualize emission results using interactive charts.")

    if 'results_df' in st.session_state and not st.session_state['results_df'].empty:
        df = st.session_state['results_df']
        
        st.subheader("Emission Heatmap by Vehicle Type")
        
        # Aggregate total emissions for simplicity (assuming 'Total' columns exist)
        emission_totals = df[['PC_Total_CO', 'LDV_Total_NOx', 'HDV_Total_PM', 'Moto_Total_FC']].sum().reset_index()
        emission_totals.columns = ['Metric', 'Value']
        emission_totals['Vehicle Type'] = emission_totals['Metric'].apply(lambda x: x.split('_')[0])
        emission_totals['Pollutant'] = emission_totals['Metric'].apply(lambda x: x.split('_')[-1])

        # Create a simple bar chart placeholder
        fig = px.bar(
            emission_totals,
            x='Vehicle Type',
            y='Value',
            color='Pollutant',
            title='Total Emissions Contribution by Vehicle Type',
            labels={'Value': 'Total Emission Value (Units)', 'Vehicle Type': 'Vehicle Category'},
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Raw Results Table")
        st.dataframe(df)

    else:
        st.info("Please run the emission calculation in the 'Calculate Emissions' tab first.")


def render_map(osm_file, map_params):
    """
    Renders the interactive map tab.
    Currently uses placeholder logic; actual implementation requires 
    processing the OSM file and calculated link emissions.
    """
    st.header("🗺️ Interactive Map")
    st.markdown("Visualize the calculated emissions overlaid on the road network map.")

    if osm_file is None:
        st.warning("Please upload or ensure the default OSM network file (`selected_zone-lagos.osm`) is available in the sidebar.")
        return

    # Placeholder Map Rendering Logic (using st.map for simplicity)
    st.markdown("### Emission Hotspot Preview (Placeholder)")
    
    # Placeholder data for map (a small area in Lagos, based on map_params)
    map_data = pd.DataFrame({
        'lat': np.linspace(map_params['ymin'], map_params['ymax'], 100),
        'lon': np.linspace(map_params['xmin'], map_params['xmax'], 100),
        'emission_intensity': np.random.rand(100) * 100 
    })
    
    # Use a scatter mapbox for better visualization if needed, but st.map is simple.
    # For a real application, you'd use folium or plotly.express.scatter_mapbox
    st.map(map_data, latitude='lat', longitude='lon', color='emission_intensity')
    
    st.caption("Note: This map uses placeholder data. Real emission data visualization will be added upon successful calculation.")
    st.markdown("---")
    st.json(map_params) # Show map parameters for verification


# CRITICAL FIX: Ensure this function accepts exactly two arguments.
def render_downloads(methodology, selected_pollutants):
    """
    Renders the download tab, creating and offering a zip file of results.
    It relies on st.session_state['results_df'] being populated.
    """
    st.header("📥 Download Results")
    st.markdown("Package and download the calculated emission data and associated documentation.")

    if 'results_df' in st.session_state and not st.session_state['results_df'].empty:
        df = st.session_state['results_df']
        
        st.success("Results are ready for download!")

        # Create a ZIP file in memory
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zf:
            # 1. Add the main results CSV
            csv_data = df.to_csv(index=False).encode('utf-8')
            zf.writestr("emission_results.csv", csv_data)

            # 2. Add a summary/metadata file
            summary = (
                f"Emission Calculation Report Summary\n"
                f"-----------------------------------\n"
                f"Methodology Used: {methodology}\n"
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
            key='download_zip',
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
        st.info("Calculate emissions first in the 'Calculate Emissions' tab to create the download package.")
