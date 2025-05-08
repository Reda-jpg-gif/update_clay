
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Base data (per 100% additive, to allow proportional mixing)
additives_data = {
    "Cork":       {"k": 0.326, "strength": 3.4, "absorption": 18.5, "co2": 82, "energy": 1180, "cost": 832},
    "Quicklime":  {"k": 0.490, "strength": 4.8, "absorption": 20.1, "co2": 130, "energy": 1536, "cost": 288},
    "Wool":       {"k": 0.420, "strength": 3.7, "absorption": 19.3, "co2": 121, "energy": 1600, "cost": 1600},
    "Almond husk":{"k": 0.552, "strength": 2.9, "absorption": 22.0, "co2": 92, "energy": 1120, "cost": 120},
    "Typha":      {"k": 0.292, "strength": 3.2, "absorption": 17.4, "co2": 75, "energy": 1020, "cost": 96},
    "Dry grass":  {"k": 0.338, "strength": 2.8, "absorption": 18.9, "co2": 80, "energy": 1080, "cost": 48},
    "Bentonite":  {"k": 0.659, "strength": 3.6, "absorption": 23.8, "co2": 110, "energy": 1360, "cost": 288},
    "Wood ash":   {"k": 0.484, "strength": 3.1, "absorption": 19.5, "co2": 90, "energy": 1056, "cost": 16},
    "Olive ash":  {"k": 0.457, "strength": 3.3, "absorption": 20.3, "co2": 88, "energy": 1048, "cost": 16},
    "OPBA":       {"k": 0.430, "strength": 3.5, "absorption": 19.0, "co2": 85, "energy": 1040, "cost": 32}
}

st.title("🧪 Custom Mix Designer – Clay + Additive Bricks")
st.markdown("Create a custom mix with up to 3 additives and see its estimated performance.")

additive_names = list(additives_data.keys())

# User selects up to 3 additives
selected = st.multiselect("Select up to 3 additives", additive_names, max_selections=3)

if selected:
    cols = st.columns(len(selected))
    proportions = []

    st.subheader("🔧 Set proportions (% of total additive content):")
    for i, name in enumerate(selected):
        pct = cols[i].slider(f"{name} (%)", 0, 100, 33)
        proportions.append(pct)

    total_pct = sum(proportions)
    if total_pct == 0:
        st.warning("Please set at least one proportion > 0.")
    else:
        weights = [p / total_pct for p in proportions]

        # Weighted average for each property
        result = {"k": 0, "strength": 0, "absorption": 0, "co2": 0, "energy": 0, "cost": 0}
        for i, name in enumerate(selected):
            for key in result:
                result[key] += weights[i] * additives_data[name][key]

        st.subheader("📊 Estimated Performance of Your Custom Mix")
        st.metric("Thermal Conductivity (W/m·K)", f"{result['k']:.3f}")
        st.metric("Compressive Strength (MPa)", f"{result['strength']:.2f}")
        st.metric("Water Absorption (%)", f"{result['absorption']:.1f}")
        st.metric("CO₂ Emissions (kg/m³)", f"{result['co2']:.0f}")
        st.metric("Embodied Energy (MJ/m³)", f"{result['energy']:.0f}")
        st.metric("Cost (MAD/m³)", f"{result['cost']:.0f}")
else:
    st.info("Please select at least one additive to begin.")
