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
sidebar_items = ["Home", "Data", "Model", "Manuscripts", "Planktoomics"]

with st.sidebar:
    selected = option_menu(
        None,                                       # Title at the top of sidebar
        sidebar_items,                              # Menu items
        icons=["house", "graph-up", "activity", "file-text", "book"],   # Matching icons
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
with st.sidebar.expander("More about this app ℹ️"):
    st.write(
        "This is a scientific dashboard to showcase the results of my PhD research "
        "in ecological modeling. The dashboard aims to make complex graphs more "
        "accessible to a broader audience.",
        styles={""}
        )
# My info
with st.sidebar.expander("Something about me 👤"):
    st.write(
        "I am a model enthusiast who did a PhD in modeling lake phytoplankton communities "
        "- the tiny, drifting organism that is very important in ecosystems. While the model "
        "itself is complex, the output can be distilled into insightful patterns by reducing "
        "dimensionality. I was fascinated not just by the model but also the stories the data told.",
        styles={""}
        )
# connect
st.sidebar.link_button("Connect with Debbie ☕️", 
                       "https://www.linkedin.com/in/debbieszewingto/")
# email
if st.sidebar.button("Email Debbie  📧"):
   st.markdown('<a href="mailto:toszewingdebbie@gmail.com">Click here if nothing opens</a>', unsafe_allow_html=True)

st.sidebar.markdown("---")  # horizontal line
# st.sidebar.selectbox("Go to", ["Home", "Analysis", "Settings"])
# st.sidebar.segmented_control("Useful links 🔗", ["Data Storage", "Code Documentation", "Settings"])

st.sidebar.markdown("## Useful links 🔗")
st.sidebar.markdown("[Data Repository](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22To%2C%20Sze%20Wing%22&l=list&p=1&s=10&sort=bestmatch)")
st.sidebar.markdown("[Code Documentation](https://github.com/Debbcwing)")
# st.sidebar.markdown("[Settings](https://your-settings-link.com)")

# ---------------------- HOME PAGE ----------------------
if selected == sidebar_items[0]:
    st.header("Welcome!")
    # st.subheader("Welcome!")
    st.write(
        "Here you can submit any questions you have about my PhD research:"
    )



# ---------------------- Data ----------------------
if selected == sidebar_items[1]:
    st.header("Data 📊📈")
    # st.subheader("Overview")
    st.write(
        "Have a look at the real lake data collected between years 2019 and 2022 by the state-of-art "
        "underwater microscope placed at Greifensee, Switzerland🇨🇭"
    )
    tab_names_data = ["Physical", "Chemical", "Biological"]
    tab1, tab2, tab3 = st.tabs(tab_names_data)

    with tab1:
        st.write(
            ""
        )

    with tab2:
        st.write(
            ""
        )

    with tab3:
        st.write(
            "X"
        )



# ---------------------- Model ----------------------
if selected == sidebar_items[2]:
    st.header("Model")
    # st.subheader("Overview")
    st.write(
        ""
    )

    tab_names_model = ["Concepts", "Baseline", "Reaction", "Forecast"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_names_model)

    with tab1:
        st.subheader(
            "A simplified lake ecosystem"
        )
        # @st.cache_data
        st.image("Fig1.1_v2.png")
    
    with tab2:
        st.write(
            ""
        )

    with tab3:
        st.write(
            ""
        )
    
    with tab4:
        st.write(
            ""
        )    

# ---------------------- Manuscript ----------------------
if selected == sidebar_items[3]:
    st.header("Manuscript")
    # st.subheader("Overview")
    st.write(
        ""
    )
    tab_names_ms = ["Manuscript 1", "Manuscript 2", "Manuscript 3"]
    tab1, tab2, tab3 = st.tabs(tab_names_ms)



# ---------------------- Planktoomics ----------------------
if selected == sidebar_items[4]:
    st.header("Stories of phytoplankton")
    # @st.cache_data
    st.image("StoryIntro.png")
    # st.subheader("**Go to**")
    if st.checkbox("The habitat of phytoplankton"):
        st.image("Phyto_1.png")
    if st.checkbox("Algae bloom under lake ice"):
        st.image("Phyto_2.png")
    if st.checkbox("The life of the aquatic photosynthesis machine"):
        st.image("Phyto_3.png")
    # st.selectbox("**Go to**", 
    #             ["The habitat of phytoplankton", 
    #              "Algae bloom under lake ice", 
    #              "The life of the aquatic photosynthesis machine"])
    # if "The habitat of phytoplankton":
    #     st.image("Phyto_1.png")
    # if "Algae bloom under lake ice":
    #     st.image("Phyto_2.png")
    # if "The life of the aquatic photosynthesis machine":
    #     st.image("Phyto_3.png")
    # tab_names_ms = ["Manuscript 1", "Manuscript 2", "Manuscript 3"]
    # tab1, tab2, tab3 = st.tabs(tab_names_ms)