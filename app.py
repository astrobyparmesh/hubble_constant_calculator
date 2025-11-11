import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt

# --- Page setup ---
st.set_page_config(page_title="Hubble Constant Calculator 💫", page_icon="🌌", layout="centered")
st.title("Hubble Constant Calculator")
st.write("Estimate the Hubble constant using observed spectral line shifts and apparent magnitudes.")

# --- Input section ---
st.subheader("🔭 Enter Observation Data")

if "df" not in st.session_state:
    st.session_state.df=pd.DataFrame(columns=["Galaxy","Object","App. Mag (m)","ΔK(Å)","ΔH(Å)","Velocity(km/s)","Distance(Mpc)"])
# --- Calculation section ---
with st.form("row"):
    galaxy = st.text_input("Galaxy Name", "")
    object_name = st.text_input("Object Name", "")
    m = st.number_input("Apparent Magnitude (m)", min_value=-30.0, max_value=50.0, value=15.0)
    k_measured = st.number_input("K-line (Measured, Å)", min_value=0000.0, max_value=6000.0, value=3950.0)
    h_measured = st.number_input("H-line (Measured, Å)", min_value=0000.0, max_value=6000.0, value=3985.0)
# Constants
    M = -22  # Absolute magnitude
    k_rest = 3933.7
    h_rest = 3968.47
    c = 3e5  # km/s
    delk = k_measured - k_rest
    delh = h_measured - h_rest
    distance = 10 ** ((m - M + 5) / 5) / 1e6  # Mpc
    velocity = c * (delk / k_rest + delh / h_rest) / 2  # km/s
    submit=st.form_submit_button("Submit")
    # --- Data Table ---
if submit:
    st.session_state.df.loc[len(st.session_state.df)]=[galaxy,object_name,m,delk,delh,velocity,distance]
    st.success(f"✅submitted Distance= {distance:.2f}, Velocity= {velocity:.2f}")
    csv = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Download Results as CSV", csv, "hubble_results.csv", "text/csv")
    st.subheader("📊 Observation Summary")
   
st.dataframe(st.session_state.df)

st.subheader("Get Hubble Constant and Age of the Universe")
if not st.session_state.df.empty:
    if st.button("Click Hear"):
        D=st.session_state.df["Distance(Mpc)"]
        V=st.session_state.df["Velocity(km/s)"]
        H,intercept=np.polyfit(D,V,1)
        c = (3.171/3.241)*pow(10,12)
        life_uni=(1/H)*c
        st.write(f"Hubble Constant= {H:.2f}, Age of Universe= {life_uni:.2f}")
    else:
        st.write(f"Please fill the data")
        


    # --- Plot Section ---
st.subheader("📈 Hubble Relation")
if not st.session_state.df.empty:
    m,intercept=np.polyfit(st.session_state.df["Distance(Mpc)"], st.session_state.df["Velocity(km/s)"],1)
    y_fit=m*st.session_state.df["Distance(Mpc)"]+intercept
    fig, ax = plt.subplots()
    ax.scatter(st.session_state.df["Distance(Mpc)"], st.session_state.df["Velocity(km/s)"], color='blue', s=80,label="points")
    ax.plot(st.session_state.df["Distance(Mpc)"], y_fit, color='red', label="best fit line")
    ax.legend()
    ax.set_xlabel("Distance (Mpc)")
    ax.set_ylabel("Velocity (km/s)")
    ax.set_title("Hubble Relation: Velocity vs Distance")
    #ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    st.download_button(
    label="⬇️ Download Plot as PNG",
    data=buf,
    file_name="plot.png",
    mime="image/png"
)


    # Option to download CSV





