# for summarizing model data and phd works
# Layout
#   Sidebar:
#       Home - introduction
#       Data - physical, chemical, biological
#       Model - concepts, baselines, results, parametrization, sensitivity, forecast,
#       Manuscripts - 1, 2, 3, (highlights, links)
#   Home:    
#   Data: 
#   Model: 
#   Manuscripts:


import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy
import json
from streamlit_option_menu import option_menu

# --- Set page config ---
st.set_page_config(
    layout="wide",  # <-- sets wide mode
    initial_sidebar_state="expanded"
)

# Sidebar menu
sidebar_items = ["Home", "Data", "Model", "Manuscripts"]#

with st.sidebar:
    selected = option_menu(
        None,                                       # Title at the top of sidebar
        sidebar_items,                              # Menu items
        icons=["house", "graph-up", "activity", "file-text"],   # Matching icons
        # menu_icon="cast",                         # Icon for the menu title
        default_index=1,                            # Which tab opens first
        # orientation='horizontal'
        styles={
            "icon":{"color": "#00ffdf", "font-size": "25px"},
            "nav-link": {"font-size": "18px", "font-weight": "bold", "color": "#00ffdf"},
            "nav-link-selected": {"background-color": "gray"}
        })

# Middle section of sidebar
st.sidebar.markdown("---")  # horizontal line
# Reasons for this site
with st.sidebar.expander("More Info ℹ️"):
    st.write(
        "This content is hidden until you click.",
        styles={""}
        )
# My info
st.sidebar.write("💡 Tip: You can add instructions, links, or info here.")
st.sidebar.write(
    ""
)
st.sidebar.write(
    ""
)
# if st.sidebar.button("Connect with Debbie! ☕️"):
#     st.sidebar.markdown(
#         'https://www.linkedin.com/in/debbieszewingto/', unsafe_allow_html=True
#     )
st.sidebar.link_button("Connect with Debbie! ☕️", 
                       "https://www.linkedin.com/in/debbieszewingto/")

st.sidebar.markdown("---")  # horizontal line
# st.sidebar.selectbox("Go to", ["Home", "Analysis", "Settings"])
st.sidebar.segmented_control("Useful links 🔗", ["Data Storage", "Code Documentation", "Settings"])



# ---------------------- HOME PAGE ----------------------
if selected == sidebar_items[0]:
    st.header("Home")
    # st.subheader("Overview")
    st.write(
        ""
    )



# ---------------------- Data ----------------------
if selected == sidebar_items[1]:
    st.header("Data")
    # st.subheader("Overview")
    st.write(
        ""
    )
    tab_names_data = ["Physical", "Chemical", "Biological"]
    tab1, tab2, tab3 = st.tabs(tab_names_data)



# ---------------------- Model ----------------------
if selected == sidebar_items[2]:
    st.header("Model")
    # st.subheader("Overview")
    st.write(
        ""
    )

    tab_names_model = ["Concepts", "Baseline", "Reaction", "Forecast"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_names_model)




# ---------------------- Manuscript ----------------------
if selected == sidebar_items[3]:
    st.header("Manuscript")
    # st.subheader("Overview")
    st.write(
        ""
    )
    tab_names_ms = ["Manuscript 1", "Manuscript 2", "Manuscript 3"]
    tab1, tab2, tab3 = st.tabs(tab_names_ms)