import streamlit as st

def render_instructions():
    """Renders the static instruction text."""
    st.header("📖 User Guide & Instructions")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Key Features")
        st.markdown("""
        - **Multi-Pollutant Analysis**: Calculate CO, CO₂, NOx, PM, VOC, and FC simultaneously
        - **International Standards**: COPERT IV, IPCC, EPA MOVES compliance
        - **Formula Transparency**: See exact mathematical formulas used
        - **Interactive Visualization**: Dynamic maps with live emission data
        - **Accuracy Controls**: Temperature, cold-start, and slope corrections
        - **Multi-Vehicle Support**: PC, Motorcycle, **LDV**, and **HDV** emissions
        """)

    with col2:
        st.subheader("📚 Standards Reference")
        st.markdown("""
        **COPERT IV (EU)**
        - European emission inventory standard
        - Accuracy: ~95% for European vehicles
        - Coverage: All vehicle types, Euro 1-6d

        **IPCC Guidelines**
        - Global greenhouse gas accounting
        - Focus: CO₂ and climate impacts
        - Used in: National inventories
        """)

    st.markdown("---")
    st.subheader("🚀 Quick Start Guide")
    st.markdown("""
    1. **Upload Files or Use Defaults**: The app pre-loads standard data. You can override specific files in the sidebar.
    2. **Select Metrics**: Choose pollutants (CO, NOx, etc.) in the sidebar.
    3. **Calculate**: Go to the **Calculate Emissions** tab and click the 'Run' button.
    4. **Analyze**: View results in the **Multi-Metric Analysis** and **Interactive Map** tabs.
    5. **Download**: Export the full results in the **Download Results** tab.
    """)

    st.markdown("---")
    st.info("💡 **Link Data Format**: Expected columns include `OSM_ID`, `Length_km`, `Flow`, `Speed`, and vehicle/fuel Proportions (e.g., `Gasoline_Prop`, `PC_Prop`, `4Stroke_Prop`).")


def render_formulas(accuracy_settings, pollutants_available):
    """
    Renders the mathematical formulas based on the selected accuracy settings.
    """
    st.header("🧮 Emission Formula Explanation")
    st.markdown("Review the mathematical models used for the calculation of each pollutant.")

    formula_pollutant = st.selectbox(
        "Select Pollutant Formula to View:",
        options=list(pollutants_available.keys()),
        format_func=lambda x: f"{x} ({pollutants_available[x]})"
    )

    st.markdown("---")
    
    if formula_pollutant == "CO":
        st.subheader("🔴 Carbon Monoxide (CO) Emission Formula")
        # Base emission formula (g/km)
        st.latex(r'E_{pollutant} = EF_{base}(V) \cdot E_{correction} \cdot M_{Flow} \cdot L_{km}')
        st.markdown(r"""
        Where:
        - $EF_{base}(V)$: Base Emission Factor (g/km) as a function of average speed ($V$), derived from COPERT IV polynomials.
        - $E_{correction}$: Total correction factor (Temp, Slope, Cold-Start).
        - $M_{Flow}$: Total vehicle flow on the link.
        - $L_{km}$: Link length in kilometers.
        """)

        # Conditional checks based on sidebar settings
        if accuracy_settings['include_cold_start']:
            st.markdown("### Cold Start Correction")
            # Formula for total emissions with cold start correction
            st.latex(r'E_{total} = E_{hot} \cdot (1 - \beta) + E_{cold} \cdot \beta')
            st.info(f"✅ Cold-Start enabled: Avg Trip Length = {accuracy_settings['trip_length']} km")

    elif formula_pollutant == "CO2":
        st.subheader("🔵 Carbon Dioxide (CO₂) Emission Formula")
        st.markdown("### Fuel-Based CO₂ Calculation (IPCC)")
        # Formula for CO2 (using Fuel Consumption FC, and Carbon Factor CF)
        st.latex(r'CO_2\ (kg) = \sum_{F} \left(FC_{F} \cdot Density_{F} \cdot C_{Fraction} \cdot \frac{44}{12} \cdot L_{km}\right)')
        st.markdown(r"""
        - $FC_{F}$: Fuel Consumption (L/km) for fuel type $F$.
        - $C_{Fraction}$: Carbon content fraction in fuel.
        - $\frac{44}{12}$: Ratio of molecular weight of CO₂ to C.
        """)

    elif formula_pollutant == "NOx":
        st.subheader("🟡 Nitrogen Oxides (NOx) Emission Formula")
        # Formula for NOx emission factor with temperature correction
        st.latex(r'EF_{NOx} = EF_{base}(V) \cdot \left(1 + k \cdot (T_{amb} - 20)\right)')
        
        # KEY FIX: Using the correct dictionary key 'include_temperature_correction'
        if accuracy_settings['include_temperature_correction']:
            t = accuracy_settings['ambient_temp']
            st.info(f"✅ Temperature correction enabled: $T_{{amb}}$ = {t}°C. (k is the pollutant-specific temp constant)")
            
    elif formula_pollutant == "PM":
        st.subheader("⚫ Particulate Matter (PM) Emission Formula")
        # Formula for PM (often includes a high-speed component and is less sensitive to cold start)
        st.latex(r'E_{PM} = EF_{base}(V) \cdot E_{Slope} \cdot M_{Flow} \cdot L_{km}')
        
        if accuracy_settings['include_slope_correction']:
            s = accuracy_settings['road_slope']
            st.info(f"✅ Slope correction enabled: $S$ = {s}%. PM is highly sensitive to road gradient.")

    elif formula_pollutant == "FC":
        st.subheader("🟠 Fuel Consumption Formula")
        st.markdown("### Vehicle Specific Power (VSP) Model")
        # Formula for instantaneous Fuel Consumption
        st.latex(r'FC = \alpha \cdot V^2 + \beta \cdot V + \gamma')
        st.markdown("Fuel consumption (L/km) is calculated using speed polynomials specific to the vehicle class and technology.")
