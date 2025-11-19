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
    3. **Calculate**: Go to the **Calculate Emissions** tab and click the button.
    4. **Analyze**: Use the Maps and Analysis tabs to view results.
    """)

# CRITICAL FIX: The function must accept two arguments to match the call in app.py.
def render_formulas(accuracy_settings, pollutants_available):
    """Renders mathematical formulas based on user selection."""
    st.header("🧮 Mathematical Formulas & Methodology")
    st.markdown("Detailed explanation of emission calculation formulas used in this calculator")

    # This selectbox uses the pollutants_available dictionary passed from app.py
    formula_pollutant = st.selectbox("Select Pollutant for Formula Details",
                                     list(pollutants_available.keys()))

    st.markdown("---")

    if formula_pollutant == "CO":
        st.subheader("🔴 Carbon Monoxide (CO) Emission Formula")
        st.markdown("### COPERT IV Hot Emission Factor")
        # Formula for hot emission factor (EF_hot)
        st.latex(r'EF_{hot} = \frac{a + c \cdot V + e \cdot V^2}{1 + b \cdot V + d \cdot V^2}')
        
        # KEY FIX: Using the correct dictionary key 'include_cold_start'
        if accuracy_settings['include_cold_start']:
            st.markdown("### Cold Start Correction")
            # Formula for total emissions with cold start correction
            st.latex(r'E_{total} = E_{hot} \cdot (1 - \beta) + E_{cold} \cdot \beta')

    elif formula_pollutant == "CO2":
        st.subheader("🔵 Carbon Dioxide (CO₂) Emission Formula")
        st.markdown("### Fuel-Based CO₂ Calculation (IPCC)")
        # Formula for CO2 (using Fuel Consumption FC, and Carbon Factor CF)
        st.latex(r'CO_2 = FC \cdot CF \cdot \frac{44}{12} \cdot 1000')

    elif formula_pollutant == "NOx":
        st.subheader("🟡 Nitrogen Oxides (NOx) Emission Formula")
        # Formula for NOx emission factor with temperature correction
        st.latex(r'EF_{NOx} = EF_{base}(V) \cdot \left(1 + k \cdot (T_{amb} - 20)\right)')
        
        # KEY FIX: Using the correct dictionary key 'include_temperature_correction'
        if accuracy_settings['include_temperature_correction']:
            t = accuracy_settings['ambient_temp']
            st.info(f"✅ Temperature correction enabled: T = {t}°C")

    elif formula_pollutant == "FC":
        st.subheader("🟠 Fuel Consumption Formula")
        # Formula for instantaneous Fuel Consumption
        st.latex(r'FC = a \cdot V^2 + b \cdot V + c')

    # Add other pollutants as needed...
    
    st.markdown("---")
    st.info("📚 **References:** EMEP/EEA Air Pollutant Emission Inventory Guidebook 2019")
