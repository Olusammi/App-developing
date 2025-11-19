import streamlit as st

def render_instructions():
    st.header("📖 User Guide & Instructions")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Key Features")
        st.markdown("""
        - **Multi-Pollutant Analysis**: CO, CO₂, NOx, PM, VOC, FC
        - **Multi-Vehicle Support**: PC, LDV, HDV, Motorcycle
        """)
    with col2:
        st.subheader("📚 Standards Reference")
        st.markdown("References: **COPERT IV (EU)**, **IPCC Guidelines**, **EPA MOVES**")

def render_formulas(accuracy_settings):
    st.header("🧮 Mathematical Formulas")
    pollutant = st.selectbox("Select Pollutant", ["CO", "CO2", "NOx", "PM", "VOC", "FC"])
    
    st.markdown("---")
    
    if pollutant == "CO":
        st.subheader("Carbon Monoxide Formula")
        st.latex(r'EF_{hot} = \frac{a + c \cdot V + e \cdot V^2}{1 + b \cdot V + d \cdot V^2}')
        if accuracy_settings['include_cold_start']:
            st.latex(r'E_{total} = E_{hot} \cdot (1 - \beta) + E_{cold} \cdot \beta')
            
    elif pollutant == "NOx":
        st.subheader("NOx Formula")
        st.latex(r'EF_{NOx} = EF_{base}(V) \cdot (1 + k \cdot (T_{amb} - 20))')
    
    # ... Add other formulas here ...
