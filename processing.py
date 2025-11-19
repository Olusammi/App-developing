import streamlit as st
import pandas as pd
import plotly.express as px

def preview_data(link_osm):
    st.header("📊 Data Preview & Validation")

    if link_osm is not None:
        st.subheader("🔗 Link OSM Data")
        try:
            link_osm.seek(0)
            # Read space-separated file, assuming no header
            data_link = pd.read_csv(link_osm, sep=r'\s+', header=None, engine='python')
            
            # Logic for column naming based on column count
            if data_link.shape[1] == 7:
                data_link.columns = ['OSM_ID', 'Length_km', 'Flow', 'Speed', 'Gasoline_Prop', 'PC_Prop', '4Stroke_Prop']
                st.info("Detected 7 columns: Assumed a simplified structure (PC/Moto only).")
            elif data_link.shape[1] == 9:
                data_link.columns = ['OSM_ID', 'Length_km', 'Flow', 'Speed', 'Gasoline_Prop', 'PC_Prop', '4Stroke_Prop', 'LDV_Prop', 'HDV_Prop']
                st.success("Detected 9 columns: Assumed full structure (PC, LDV, HDV, Moto).")
            else:
                data_link.columns = [f'Column_{i}' for i in range(data_link.shape[1])]
                st.warning(f"Detected {data_link.shape[1]} columns. Defaulting to generic column names.")

            st.dataframe(data_link.head(20), use_container_width=True)

            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Links", len(data_link))
            col2.metric("Total Length (km)", f"{data_link['Length_km'].sum():.2f}")
            col3.metric("Avg Speed (km/h)", f"{data_link['Speed'].mean():.2f}")
            col4.metric("Avg Flow (veh)", f"{data_link['Flow'].mean():.0f}")

            # Plots
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(px.histogram(data_link, x='Speed', nbins=30, title="Speed Distribution"), use_container_width=True)
            with c2:
                st.plotly_chart(px.scatter(data_link, x='Length_km', y='Flow', log_y=True, title="Flow vs. Link Length"), use_container_width=True)


        except Exception as e:
            st.error(f"Error reading or processing link data file: {e}")
            st.warning("Please ensure the file is a space-separated (.txt or .csv) file with no header.")
    else:
        st.info("Upload the Link Data file in the sidebar to view the preview and validation statistics.")
