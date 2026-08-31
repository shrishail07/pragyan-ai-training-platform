import streamlit as st
import pandas as pd
from utils.db_helper import fetch_data

def render():
    st.title("🤝 Program Coordinators")
    st.write("Find the coordinator details for your specific programs below.")
    
    coordinators_data = fetch_data("coordinators")
    
    if not coordinators_data:
        st.info("Details will be coming soon...")
    else:
        df = pd.DataFrame(coordinators_data)
        st.dataframe(df, use_container_width=True)
