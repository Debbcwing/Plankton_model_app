import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from copy import deepcopy
import json
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Set page config (must be first Streamlit command) ---
st.set_page_config(
    page_title="Plankton Model App",
    page_icon="🌊",
    layout="wide",  # Wide layout
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Plankton Model App\nExplore PhD research on plankton ecology and lake ecosystems."
    }
)

# Hide hamburger menu and GitHub icon
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar menu
sidebar_items = ["Home", "Manuscripts", "Data", "Model", "Planktoomics"]

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
with st.sidebar.expander("More about Debbie 🇭🇰"):
        st.write(
        """
        - Nature lover
        - Data storyteller
        - Model enthusiast
        - Modeling plankton
        """,
        styles={""})
        st.write(
            "**I am fascinated not just by models but also the stories data tell.**",
        styles={""})
        st.write(
            "**While models themselves can be complex, their output can be distilled into insightful patterns!**",
        styles={""})


# connect
st.sidebar.link_button("Connect with Debbie ☕️", 
                       "https://www.linkedin.com/in/debbieszewingto/")
# email
# if st.sidebar.button("Email Debbie  📧"):
#    st.markdown('<a href="mailto:toszewingdebbie@gmail.com">Click here if nothing opens</a>', unsafe_allow_html=True)

st.sidebar.markdown("""
    <a href="mailto:toszewingdebbie@gmail.com">
        <button style="padding:7.5px 35px; 
                       font-size:16px; 
                       cursor:pointer; 
                       background-color:#FFBF00;
                       color:black;
                       border:none;
                       ">Email Debbie 📧</button>
    </a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")  # horizontal line
# st.sidebar.selectbox("Go to", ["Home", "Analysis", "Settings"])
# st.sidebar.segmented_control("Useful links 🔗", ["Data Storage", "Code Documentation", "Settings"])

st.sidebar.markdown("## Useful links 🔗")
st.sidebar.markdown("[Data Repository](https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22To%2C%20Sze%20Wing%22&l=list&p=1&s=10&sort=bestmatch)")
st.sidebar.markdown("[Code Documentation](https://github.com/Debbcwing)")
st.sidebar.markdown("[ResearchGate](https://www.researchgate.net/profile/Sze-Wing-To)")
st.sidebar.markdown("[PhD Dissertation](https://opus.constructor.university/frontdoor/index/index/docId/1282)")

st.sidebar.markdown("---")  # horizontal line
st.sidebar.caption("This PhD project received funding from the German Research Foundation (DFG) "
                    "and Swiss National Science Foundation (SNF) as part of the project AQUASCOPE (grant No. 412375259)."
                    "The project was hosted at institute [Leibniz Center for Tropical Marine Research (ZMT)](https://leibniz-zmt.de/en/), Bremen.")



# ---------------------- HOME PAGE ----------------------
if selected == sidebar_items[0]:
    st.title("Hello👋🏼  Ask me anything about my PhD research on plankton modeling!")

    # Check if API key is set
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        st.warning("⚠️ Anthropic API key not found!")
        st.info(
            "To use the Q&A system:\n\n"
            "1. Add your API key to `.env` file:\n"
            "   ```\n"
            "   ANTHROPIC_API_KEY=your-key-here\n"
            "   ```\n"
            "2. Restart the Streamlit app"
        )
    else:
        # Load RAG system and dependencies only when needed
        try:
            # Lazy imports - only load when API key exists
            from config.rag_setup import RAGSystem
            from langchain_anthropic import ChatAnthropic
            from langchain.chains.combine_documents import create_stuff_documents_chain
            from langchain.chains import create_retrieval_chain
            from langchain_core.prompts import ChatPromptTemplate

            def load_rag_system():
                """Load RAG system."""
                rag = RAGSystem()
                rag.setup(force_rebuild=False)
                return rag

            def load_qa_chain(_api_key):
                """Initialize QA chain."""
                # Load RAG system
                rag_system = load_rag_system()

                # Initialize Claude
                llm = ChatAnthropic(
                    model="claude-3-5-haiku-20241022",
                    anthropic_api_key=_api_key,
                    temperature=0.5,
                    max_tokens=300
                )

                # Load custom prompt template from file
                with open("config/prompt_template.txt", "r") as f:
                    prompt_template = f.read()

                # Create prompt using ChatPromptTemplate
                prompt = ChatPromptTemplate.from_template(prompt_template)

                # Create the document chain
                document_chain = create_stuff_documents_chain(llm, prompt)

                # Create retrieval chain
                retriever = rag_system.vectorstore.as_retriever(search_kwargs={"k": 2})
                qa_chain = create_retrieval_chain(retriever, document_chain)

                return qa_chain

            with st.spinner("Loading..."):
                qa_chain = load_qa_chain(api_key)

            # Show example Q&A pairs
            with st.expander("💡  Some common questions and answers"):
                st.markdown("**Q: What is the main focus of your PhD research?**")
                st.markdown("**A:** My research is all about understanding how tiny organisms called plankton grow and interact in lakes! I built computer models to simulate how different types of phytoplankton (the plant-like plankton) compete for nutrients and respond to changes in their environment. Think of it like creating a virtual aquarium to study how different factors—like temperature, light, and nutrient availability—affect which species thrive and which ones struggle.")

                st.markdown("---")
                st.markdown("**Q: How does your model handle nutrient dynamics?**")
                st.markdown("**A:** Great question! The model tracks how nutrients like nitrogen and phosphorus move through the water. Imagine nutrients as food for plankton—they get taken up by phytoplankton, then passed along when zooplankton eat the phytoplankton. The model also simulates how nutrients get recycled back into the water when organisms die or produce waste. It's like tracking a nutrient cycle in a mini ecosystem!")

                st.markdown("---")
                st.markdown("**Q: What are the key findings from your simulations?**")
                st.markdown("**A:** One cool finding is that size really matters! Larger phytoplankton tend to dominate in nutrient-rich waters, while smaller ones do better when nutrients are scarce. I also found that grazing pressure from zooplankton can completely flip which phytoplankton species wins the competition. It's fascinating how these tiny interactions shape entire lake ecosystems!")

                st.markdown("---")
                st.markdown("**Q: How do environmental factors influence plankton populations?**")
                st.markdown("**A:** Environmental factors are like the control knobs for plankton communities! Temperature affects how fast plankton grow—warmer water speeds things up. Light is crucial since phytoplankton need it for photosynthesis, just like plants. Mixing in the water column affects nutrient availability, and seasonal changes can totally reshape which species dominate. My research shows that even small shifts in these factors can lead to big changes in who wins the competition!")

                st.markdown("---")
                st.markdown("**Q: Can you explain the role of phytoplankton in aquatic ecosystems?**")
                st.markdown("**A:** Phytoplankton are basically the invisible heroes of lakes and oceans! They're microscopic algae that produce oxygen through photosynthesis—think of them as the 'plants' of the water. They're also the foundation of the food web, feeding everything from tiny zooplankton to fish. Plus, they play a huge role in the carbon cycle by absorbing CO2. Without them, aquatic ecosystems would collapse!")

                st.markdown("---")
                st.markdown("**Q: What are the future directions of your research?**")
                st.markdown("**A:** I'm excited to explore how climate change might affect plankton communities in the future! Specifically, I want to study how warming waters and changing nutrient patterns could shift which species dominate. Another cool direction is looking at harmful algal blooms—understanding what triggers them could help us predict and prevent toxic blooms. There's still so much to discover about these tiny but mighty organisms!")

            # Chat interface
            user_question = st.text_input(
                "",
                placeholder="e.g., What surprised you most in your research?"
            )


            if user_question:
                with st.spinner("Searching through documents..."):
                    result = qa_chain.invoke({"input": user_question})

                    # Display answer
                    st.subheader("Answer:")
                    st.write(result["answer"])

                    # Show sources
                    with st.expander("📚 View source documents"):
                        for i, doc in enumerate(result["context"], 1):
                            source_file = doc.metadata.get('source', 'Unknown')
                            page = doc.metadata.get('page', 'Unknown')

                            # Map filenames to friendly names
                            filename = os.path.basename(source_file)
                            if 'Dissert' in filename:
                                doc_name = "PhD Dissertation"
                            elif 'Defense' in filename:
                                doc_name = "PhD Defense Presentation"
                            else:
                                doc_name = "Research Document"

                            st.markdown(f"**Source {i}:** {doc_name}, Page {page}")
                            st.text(doc.page_content[:300] + "...")
                            st.markdown("---")
            
            st.write("")
            st.write("")

        except Exception as e:
            error_msg = str(e)

            # Show cleaner error message
            if "corrupted or empty" in error_msg.lower() or "embeddings" in error_msg.lower():
                st.error("⚠️ Vector database is corrupted or empty")
                st.info(
                    "**To fix this issue:**\n\n"
                    "Run this command in your terminal to rebuild the database:\n"
                    "```bash\n"
                    "python config/rag_setup.py\n"
                    "```\n\n"
                    "This will process your PhD documents and create the searchable database."
                )
            else:
                st.error(f"Error loading RAG system: {error_msg}")
                st.info(
                    "**Troubleshooting:**\n\n"
                    "If this is your first time running the app, you need to build the vector database:\n\n"
                    "Run this command in your terminal:\n"
                    "```bash\n"
                    "python config/rag_setup.py\n"
                    "```"
                )

# ---------------------- Manuscript ----------------------
if selected == sidebar_items[1]:
    st.title("📚 Publications")
    st.write("Explore my peer-reviewed research on phytoplankton size structure and community dynamics in lake ecosystems.")

    tab_names_ms = ["Manuscript 1 (2024)", "Manuscript 2 (2025)", "Manuscript 3 (Under Review)"]
    tab1, tab2, tab3 = st.tabs(tab_names_ms)

    # ========== Manuscript 1 (2024) ==========
    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Grazing strategies determine the size composition of phytoplankton in eutrophic lakes")
            st.markdown("**Authors:** Sze-Wing To, "
                        "[Esteban Acevedo-Trejos](https://www.leibniz-zmt.de/en/marine-tropics-research/who-we-are/esteban-acevedo-trejos-en.html), "
                        "[Subhendu Chakraborty](https://www.leibniz-zmt.de/en/marine-tropics-research/who-we-are/subhendu-chakraborty.html), "
                        "[Francesco Pomati](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/francesco-pomati/show/), "
                        "[Agostino Merico](https://www.leibniz-zmt.de/en/marine-tropics-research/who-we-are/agostino-merico.html)")
            st.markdown("**Journal:** *Limnology and Oceanography*, 69:933–946 (2024)")
            st.markdown("**DOI:** [10.1002/lno.12538](https://doi.org/10.1002/lno.12538)")

        with col2:
            with open("MS/To et al. (2024).pdf", "rb") as f:
                st.download_button(
                    label="📄 Download PDF",
                    data=f,
                    file_name="To_et_al_2024.pdf",
                    mime="application/pdf"
                )
            with open("MS/To et al. (2024)supp.pdf", "rb") as f:
                st.download_button(
                    label="📊 Supplementary Material",
                    data=f,
                    file_name="To_et_al_2024_supplement.pdf",
                    mime="application/pdf"
                )

        st.markdown("---")

        # Abstract
        with st.expander("📖 Abstract", expanded=True):
            st.write("""
            Although the general impacts of zooplankton grazing on phytoplankton communities are clear, we know comparatively
            less about how specific grazing strategies interact with environmental conditions to shape the size structure of
            phytoplankton communities. Here, we present a new data-driven, size-based model that describes changes in the size
            composition of lake phytoplankton under various environmental constraints. The model includes an ecological trade-off
            emerging from observed allometric relationships between (1) phytoplankton cell size and phytoplankton growth and
            (2) phytoplankton cell size and zooplankton grazing. In our model, phytoplankton growth is nutrient-dependent and
            zooplankton grazing varies according to specific grazing strategies, namely, specialists (targeting a narrow range of
            the size-feeding spectrum) vs. generalists (targeting a wide range of the size-feeding spectrum). Our results indicate
            that grazing strategies shape the size composition of the phytoplankton community in nutrient-rich conditions, whereas
            inorganic nutrient concentrations govern phytoplankton size structure under nutrient-poor conditions.
            """)

        # Key Findings
        st.success("🎯 **Key Findings**")
        st.markdown("""
        - **Grazing strategies** (specialist vs. generalist) significantly shape phytoplankton size composition in eutrophic lakes
        - **Nutrient availability** is the dominant driver in oligotrophic conditions
        - **Size-based trade-offs** between growth rate and grazing vulnerability determine competitive outcomes
        - Model predictions align with empirical observations from Swiss lakes
        """)

    # ========== Manuscript 2 (2025) ==========
    with tab2:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Ecological and environmental factors influencing exclusion patterns of phytoplankton size classes in lake systems")
            st.markdown("**Authors:** Sze-Wing To, "
                        "[Esteban Acevedo-Trejos](https://www.leibniz-zmt.de/en/marine-tropics-research/who-we-are/esteban-acevedo-trejos-en.html), "
                        "[Sherwood Lan Smith](https://wpi-aimec.jp/en/member/Smith-SherwoodLan.html), "
                        "[Subhendu Chakraborty](https://www.leibniz-zmt.de/en/marine-tropics-research/who-we-are/subhendu-chakraborty.html), "
                        "[Francesco Pomati](https://www.eawag.ch/en/about-us/portrait/organisation/staff/profile/francesco-pomati/show/), "
                        "[Agostino Merico](https://www.leibniz-zmt.de/en/marine-tropics-research/who-we-are/agostino-merico.html)")            
            st.markdown("**Journal:** *Ecological Modelling*, 499:110936 (2025)")
            st.markdown("**DOI:** [10.1016/j.ecolmodel.2024.110936](https://doi.org/10.1016/j.ecolmodel.2024.110936)")

        with col2:
            with open("MS/To et al. (2025).pdf", "rb") as f:
                st.download_button(
                    label="📄 Download PDF",
                    data=f,
                    file_name="To_et_al_2025.pdf",
                    mime="application/pdf"
                )
            with open("MS/To et al. (2025)supp.pdf", "rb") as f:
                st.download_button(
                    label="📊 Supplementary Material",
                    data=f,
                    file_name="To_et_al_2025_supplement.pdf",
                    mime="application/pdf"
                )

        st.markdown("---")

        # Abstract
        with st.expander("📖 Abstract", expanded=True):
            st.write("""
            For decades, ecologists have been intrigued by the paradoxical coexistence of a wide range of phytoplankton
            types on a seemingly limited number of resources. The interactions between environmental conditions and trade-offs
            emerging from eco-physiological traits of phytoplankton are typically proposed to explain coexistence. The number
            of coexisting types over ecological time scales reflects what we call here 'exclusion patterns', that is, the
            temporal removal of certain phytoplankton types due to competition. Despite many observational and mathematical
            modelling efforts over the last two decades, we still know surprisingly little, in quantitative terms, about
            how the interplay of nutrient regimes and specific zooplankton grazing strategies affects the exclusion patterns
            of competing phytoplankton types. Here we use a size-based plankton model to investigate how environmental factors
            and ecological trade-offs influence phytoplankton diversity and competitive exclusion patterns.
            """)

        # Key Findings
        st.info("🎯 **Key Findings**")
        st.markdown("""
        - **Competitive exclusion patterns** are shaped by the interplay of nutrient regimes and grazing strategies
        - **Size-based trade-offs** create niches that allow for phytoplankton coexistence
        - **Environmental variability** (mixing, seasonality) promotes diversity by preventing competitive exclusion
        - Framework helps explain the "paradox of the plankton" through quantitative modeling
        """)

    # ========== Manuscript 3 (Under Review) ========== 
    with tab3:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("*Under Review* - Future inorganic nutrient and plankton dynamics in a temperate lake")
            st.markdown("**Journal:** *Limnology and Oceanography*")
            st.markdown("**Status:** 🔄 Final review")

        st.markdown("---")

        st.warning("📋 **Status Update**")
        st.write("""
        This manuscript is currently under final review at *Limnology and Oceanography*.
        Details will be available upon publication.
        """)

        st.info("💡 **Research Focus**")
        st.write("""
        This work builds on the previous two manuscripts to explore how climate change and environmental
        stressors might affect phytoplankton community structure in future lake ecosystems.
        """)


# ---------------------- Data ----------------------
if selected == sidebar_items[2]:
    st.title("📊 Data")
    st.write(
        "Have a look at the real lake data collected between years 2019 and 2022 by the state-of-art "
        "underwater microscope placed at [Greifensee](https://www.myswitzerland.com/de-ch/reiseziele/greifensee/),"
        " Switzerland🇨🇭"
    )
    tab_names_data = ["Meterological", "Physical", "Chemical", "Biological"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_names_data)

    with tab1:
        st.subheader("🌡️ Temperature & ☀️ Solar Radiation (2019-2022)")
        st.write("Explore how temperature and solar radiation change throughout the seasons at Greifensee!")

        # Load physical data
        try:
            @st.cache_data(show_spinner=False)
            def load_physical_data():
                """Load and preprocess physical data (cached)."""
                df = pd.read_csv("data/RawData_Temp+PAR.csv", index_col=0)
                df['date'] = pd.to_datetime(df['date'])
                df['water_temp'] = pd.to_numeric(df['water_temp'], errors='coerce')
                df['global_radiation'] = pd.to_numeric(df['global_radiation'], errors='coerce')
                return df

            df_physical = load_physical_data()

            # Create dual-axis interactive plot
            fig = go.Figure()

            # Add temperature trace (left y-axis)
            fig.add_trace(go.Scatter(
                x=df_physical['date'],
                y=df_physical['water_temp'],
                name='Temperature',
                line=dict(color='#FF6B6B', width=2),
                yaxis='y1',
                hovertemplate='<b>Temperature</b><br>%{y:.1f}°C<br><extra></extra>'
            ))

            # Add solar radiation trace (right y-axis)
            fig.add_trace(go.Scatter(
                x=df_physical['date'],
                y=df_physical['global_radiation'],
                name='Solar Radiation',
                line=dict(color='#FFA500', width=2),
                yaxis='y2',
                hovertemplate='<b>Solar Radiation</b><br>%{y:.1f} W/m²<br><extra></extra>'
            ))

            # Update layout with dual axes and range slider
            fig.update_layout(
                xaxis=dict(
                    title='Date',
                    rangeslider=dict(visible=True),
                    type='date'
                ),
                yaxis=dict(
                    title=dict(text='Temperature (°C)', font=dict(color='#FF6B6B')),
                    tickfont=dict(color='#FF6B6B')
                ),
                yaxis2=dict(
                    title=dict(text='Solar Radiation (W/m²)', font=dict(color='#FFA500')),
                    tickfont=dict(color='#FFA500'),
                    overlaying='y',
                    side='right'
                ),
                hovermode='x unified',
                template='plotly_dark',
                height=600,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # Add insights
            with st.expander("💡 What patterns do you see?"):
                st.markdown("""
                **Seasonal Patterns:**
                - 🌞 **Solar radiation peaks in summer** (June-August) with the longest days and strongest sunlight
                - ❄️ **Winter brings low radiation** (December-February) with short days and low sun angles
                - 🌡️ **Temperature follows solar radiation** but with a slight delay (thermal inertia)

                **Key Observations:**
                - Temperature ranges from ~4°C in winter to ~20°C in summer
                - Solar radiation can vary dramatically day-to-day due to cloud cover
                - The relationship between sunlight and temperature drives the entire lake ecosystem!

                **Try this:** Use the range selector to zoom into a specific season and see daily variations!
                """)

        except FileNotFoundError:
            st.warning("⚠️ Data file not found. Please add your data file as `data/physical_data.csv`")
            st.info("""
            **Expected CSV format:**
            ```
            date,temperature_C,solar_radiation_W_m2
            2019-01-01,4.2,45.3
            2019-01-02,4.1,52.1
            ...
            ```
            """)

    with tab2:
        st.subheader("🌀 Lake mixing in the water column (1972-2015)")
        st.write("Lake mixing is a key physical process that influences nutrient distribution and plankton dynamics.")
        st.write("Explore Lake mixing patterns at Greifensee over four decades!")

        # Load MLD data
        @st.cache_data(show_spinner=False)
        def load_mix_data():
            """Load and preprocess physical data (cached)."""
            df = pd.read_csv("data/RawData_MLD.csv", index_col=0)
            df['date'] = pd.to_datetime(df['date'])
            df['thermocl'] = pd.to_numeric(df['thermocl'], errors='coerce')
            return df

        df_mix = load_mix_data()

        # Identify fully mixed periods (30m = lake bottom)
        df_mix['fully_mixed'] = df_mix['thermocl'] >= 29.5

        fig = go.Figure()

        # Add seasonal background shading
        years = pd.date_range(start=df_mix['date'].min(), end=df_mix['date'].max(), freq='YS').year
        for year in years:
            # Winter (Dec-Feb): light blue
            fig.add_vrect(x0=f"{year}-01-01", x1=f"{year}-03-01",
                         fillcolor="lightblue", opacity=0.1, layer="below", line_width=0)
            # Summer (Jun-Aug): light yellow
            fig.add_vrect(x0=f"{year}-06-01", x1=f"{year}-09-01",
                         fillcolor="lightyellow", opacity=0.1, layer="below", line_width=0)

        # Add MLD trace with area fill (inverted to show depth)
        fig.add_trace(go.Scatter(
            x=df_mix['date'],
            y=df_mix['thermocl'],
            name='Mixed Layer Depth',
            mode='lines',
            line=dict(color='rgb(8, 48, 107)', width=1.5),  # Deep ocean blue
            fill='tozeroy',
            fillcolor='rgba(8, 81, 156, 0.4)',  # Ocean blue with transparency
            hovertemplate='<b>MLD</b><br>%{y:.1f} m<br>%{x|%Y-%m-%d}<extra></extra>'
        ))

        # Highlight fully mixed periods with markers
        df_fully_mixed = df_mix[df_mix['fully_mixed']]
        fig.add_trace(go.Scatter(
            x=df_fully_mixed['date'],
            y=df_fully_mixed['thermocl'],
            name='Fully Mixed (to bottom)',
            mode='markers',
            marker=dict(color='rgb(220, 50, 50)', size=6, symbol='diamond'),
            hovertemplate='<b>Fully Mixed</b><br>%{y:.1f} m (lake bottom)<br>%{x|%Y-%m-%d}<extra></extra>'
        ))

        # Add reference line for average MLD
        avg_mld = df_mix['thermocl'].mean()
        fig.add_hline(y=avg_mld, line_dash="dash", line_color="gray",
                     annotation_text=f"Average: {avg_mld:.1f}m",
                     annotation_position="right")

        # Update layout with inverted y-axis
        fig.update_layout(
            yaxis=dict(
                title="Mixed Layer Depth (m)",
                autorange="reversed",  # Invert y-axis so depth goes down
                gridcolor='lightgray'
            ),
            xaxis=dict(
                title="Date",
                gridcolor='lightgray',
                rangeslider=dict(visible=True),
                type='date'
            ),
            hovermode='x unified',
            plot_bgcolor='white',
            height=500,
            showlegend=True,
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)', font=dict(color='black')),
            font=dict(color='black')
        )

        st.plotly_chart(fig, use_container_width=True)

        # Add explanation text
        st.info("""
        **Try this:** Use the range selector to zoom into a specific season and see daily variations!
        
        **Reading the chart:**
        - **Deeper colors** = deeper mixed layer (more mixing)
        - **Red diamonds** = fully mixed to lake bottom (~30m)
        - **Seasonal patterns**: Winter mixing (blue background) vs. summer stratification (yellow background)
        - **Average depth** shown as dashed gray line
        """)

    with tab3:
        st.subheader("💧 Nutrient Concentrations (2019-2022)")
        st.write("Nutrients like phosphate, nitrate, and ammonium are essential for plankton growth and lake health.")
        st.write("Explore how nutrient levels relate to eutrophication (nutrient enrichment) status!")

        # Load nutrient data
        @st.cache_data(show_spinner=False)
        def load_nutrient_data():
            """Load and preprocess nutrient data (cached)."""
            df = pd.read_csv("data/GRE_raw_plankton_ab_size.csv")
            df['date'] = pd.to_datetime(df['date'])

            # Select relevant columns
            df = df[['date', 'phosphate_ug', 'nitrate_mg', 'ammonium_ug']].copy()

            # Convert nitrate from mg/L to µg/L (multiply by 1000)
            df['nitrate_ug'] = df['nitrate_mg'] * 1000

            # Add season column
            df['season'] = df['date'].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            })

            return df

        df_nutrient = load_nutrient_data()

        # Checkboxes for nutrient selection with info-style background
        container = st.container(border=True)
        with container:
            col1, col2, col3 = st.columns(3)
            with col1:
                show_phosphate = st.checkbox("Phosphate (µg/L)", value=True, key="phosphate_check")
            with col2:
                show_nitrate = st.checkbox("Nitrate (µg/L)", value=False, key="nitrate_check")
            with col3:
                show_ammonium = st.checkbox("Ammonium (µg/L)", value=False, key="ammonium_check")

        # Create subplot: 2/3 for time series, 1/3 for boxplot
        from plotly.subplots import make_subplots

        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.7, 0.3],
            subplot_titles=('Nutrient Concentrations Over Time', 'Seasonal Distribution'),
            horizontal_spacing=0.1,
            specs=[[{"secondary_y": True}, {"secondary_y": True}]]  # Enable secondary y-axis for left plot
        )

        # Nutrient configurations
        nutrients = {
            'phosphate': {
                'show': show_phosphate,
                'column': 'phosphate_ug',
                'name': 'Phosphate',
                'color': 'rgb(106, 13, 173)',
                'unit': 'µg/L',
                'secondary_y': False,  # Left y-axis
                'thresholds': [10, 30]  # Oligotrophic, Mesotrophic, Eutrophic
            },
            'nitrate': {
                'show': show_nitrate,
                'column': 'nitrate_ug',
                'name': 'Nitrate',
                'color': 'rgb(0, 102, 204)',
                'unit': 'µg/L',
                'secondary_y': True,  # Right y-axis
                'thresholds': None
            },
            'ammonium': {
                'show': show_ammonium,
                'column': 'ammonium_ug',
                'name': 'Ammonium',
                'color': 'rgb(255, 140, 0)',
                'unit': 'µg/L',
                'secondary_y': False,  # Left y-axis with phosphate
                'thresholds': None
            }
        }

        # Add eutrophication zones for phosphate (only if phosphate is selected)
        if show_phosphate:
            df_p = df_nutrient.dropna(subset=['phosphate_ug'])
            max_val = max(df_p['phosphate_ug'].max() * 1.2, 50)  # Ensure visible range

            fig.add_hrect(y0=0, y1=10, fillcolor="green", opacity=0.25, layer="below",
                         annotation_text="Oligotrophic", annotation_position="top left",
                         annotation=dict(font_size=9, font_color="darkgreen"),
                         row=1, col=1, secondary_y=False)
            fig.add_hrect(y0=10, y1=30, fillcolor="yellow", opacity=0.25, layer="below",
                         annotation_text="Mesotrophic", annotation_position="top left",
                         annotation=dict(font_size=9, font_color="darkorange"),
                         row=1, col=1, secondary_y=False)
            fig.add_hrect(y0=30, y1=max_val, fillcolor="red", opacity=0.25, layer="below",
                         annotation_text="Eutrophic", annotation_position="top left",
                         annotation=dict(font_size=9, font_color="darkred"),
                         row=1, col=1, secondary_y=False)

        # Plot selected nutrients
        seasons_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_colors = {'Spring': 'rgba(144, 238, 144, 0.6)', 'Summer': 'rgba(255, 215, 0, 0.6)',
                        'Fall': 'rgba(255, 165, 0, 0.6)', 'Winter': 'rgba(173, 216, 230, 0.6)'}

        for nutrient_key, config in nutrients.items():
            if config['show']:
                df_filtered = df_nutrient.dropna(subset=[config['column']])

                # Time series (left panel) with secondary_y support
                fig.add_trace(
                    go.Scatter(
                        x=df_filtered['date'],
                        y=df_filtered[config['column']],
                        name=config['name'],
                        line=dict(color=config['color'], width=2),
                        yaxis='y2' if config['secondary_y'] else 'y',
                        hovertemplate=f'<b>{config["name"]}</b><br>%{{y:.2f}} {config["unit"]}<br>%{{x|%Y-%m-%d}}<extra></extra>'
                    ),
                    row=1, col=1, secondary_y=config['secondary_y']
                )

                # Seasonal boxplot (right panel)
                # for season in seasons_order:
                #     season_data = df_filtered[df_filtered['season'] == season]
                #     if len(season_data) > 0:
                #         fig.add_trace(
                #             go.Box(
                #                 y=season_data[config['column']],
                #                 name=season,
                #                 marker_color=season_colors[season],
                #                 boxmean='sd',
                #                 legendgroup=season,
                #                 showlegend=False,
                #                 hovertemplate=f'<b>{{fullData.name}}</b><br>{config["name"]}: %{{y:.2f}} {config["unit"]}<extra></extra>'
                #             ),
                #             row=1, col=2    #
                #         )
                for i, season in enumerate(seasons_order):
                    season_data = df_filtered[df_filtered['season'] == season]
                    if len(season_data) > 0:
                        # put the season as the categorical x value, and name as the nutrient so boxes for
                        # different nutrients appear side-by-side per season
                        fig.add_trace(
                            go.Box(
                                x=[season] * len(season_data),            # categorical x => 'Spring','Summer',...
                                y=season_data[config['column']],
                                name=config['name'],                      # name = nutrient (Phosphate/Nitrate/...)
                                marker_color=config['color'],             # use nutrient color (no alpha)
                                boxmean='sd',
                                legendgroup=config['name'],
                                showlegend=(i == 0),                      # show legend once per nutrient
                                hovertemplate=f'<b>{config["name"]}</b><br>{season}: %{{y:.2f}} {config["unit"]}<extra></extra>',
                                line=dict(width=0.8)                       # thinner box lines
                            ),
                            row=1, col=2, secondary_y=config['secondary_y']  # Use same y-axis as time series
                        )

                # after building traces: enable grouped box mode
                fig.update_layout(boxmode='group')

        # Update axes
        fig.update_xaxes(title_text="Date", gridcolor='lightgray', row=1, col=1)
        fig.update_xaxes(title_text="Season", gridcolor='lightgray', row=1, col=2)

        # Update y-axes for time series (left panel) with dual y-axis
        fig.update_yaxes(
            title_text="Phosphate & Ammonium (µg/L)",
            title_font=dict(color='rgb(106, 13, 173)'),
            tickfont=dict(color='rgb(106, 13, 173)'),
            gridcolor='lightgray',
            row=1, col=1,
            secondary_y=False
        )
        fig.update_yaxes(
            title_text="Nitrate (µg/L)",
            title_font=dict(color='rgb(0, 102, 204)'),
            tickfont=dict(color='rgb(0, 102, 204)'),
            showgrid=False,  # Remove gridlines from secondary y-axis
            row=1, col=1,
            secondary_y=True
        )

        # Update y-axes for boxplot (right panel) with dual y-axis
        fig.update_yaxes(
            title_text="Phosphate & Ammonium (µg/L)",
            title_font=dict(color='rgb(106, 13, 173)'),
            tickfont=dict(color='rgb(106, 13, 173)'),
            gridcolor='lightgray',
            row=1, col=2,
            secondary_y=False
        )
        fig.update_yaxes(
            title_text="Nitrate (µg/L)",
            title_font=dict(color='rgb(0, 102, 204)'),
            tickfont=dict(color='rgb(0, 102, 204)'),
            showgrid=False,  # Remove gridlines from secondary y-axis
            row=1, col=2,
            secondary_y=True
        )

        # Update layout with title padding
        fig.update_layout(
            height=500,
            plot_bgcolor='white',
            hovermode='closest',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255,255,255,0.8)',
                font=dict(color='black')),
            font=dict(color='white'),
            margin=dict(t=80)  # Add top margin for title padding
            )

        # Add padding between subplot titles and plots
        for annotation in fig['layout']['annotations']:
            annotation['y'] = annotation['y'] + 0.02  # Move titles slightly up

        st.plotly_chart(fig, use_container_width=True)

        # Add explanation
        st.info("""
        **Understanding the visualization:**
        - **Left panel**: Time series showing nutrient trends over time
        - **Right panel**: Seasonal patterns (boxplots show median, quartiles, and outliers)
        - **Select multiple nutrients** using checkboxes above to compare patterns
        """)
        # - **Phosphate zones**:
        #   - Green (0-10 µg/L) = Oligotrophic (nutrient-poor, clear water)
        #   - Yellow (10-30 µg/L) = Mesotrophic (moderate nutrients)
        #   - Red (>30 µg/L) = Eutrophic (nutrient-rich, potential algal blooms)
    with tab4:
        st.write(
            "In working progress.."
        )

# ---------------------- Model ----------------------
if selected == sidebar_items[3]:
    st.title("🖥️ Model")
    # st.subheader(
    #         "A simplified lake ecosystem"
    #     )

    tab_names_model = ["Concepts", "Baseline", "Reaction", "Forecast"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_names_model)

    with tab1:
        st.write(
            "In a simplified lake ecosystem model, there are five main components: Nutrients, Phytoplankton, Zooplankton, Detritus, and Fish. "
            "Nutrients are essential for phytoplankton growth, while zooplankton feed on phytoplankton. "
            "Fish can prey on zooplankton, affecting their population dynamics. "
            "Detritus consists of dead organic matter, which can be decomposed back into nutrients. "
            "Apart from these biotic interactions, physical factors such as temperature and light availability also play crucial roles in shaping the ecosystem. "
            "Physical processes like mixing and stratification influence nutrient distribution and organism interactions. "
            "Lastly, external inputs such as nutrient runoff from human settlements can alter nutrient levels in the lake. "
            "The interactions among all these components create a complex web of relationships that drive the ecosystem's dynamics."
        )
        col1, col2, col3 = st.columns([1, 5, 1])
        with col2:
            st.image("lake-fig.webp", use_container_width=True)
    
    with tab2:
        st.write(
            "In working progress.."
        )

    with tab3:
        st.write(
            "In working progress.."
        )
    
    with tab4:
        st.write(
            "In working progress.."
        )    




# ---------------------- Planktoomics ----------------------
if selected == sidebar_items[4]:
    st.header("🌊 Planktoomics: Stories of Phytoplankton")
    st.write("Dive into the fascinating world of phytoplankton through visual storytelling!")

    # Introduction image
    st.image("Planktoomics/StoryIntro.webp", use_container_width=True)

    st.markdown("---")

    # Story navigation using expanders (better UX than checkboxes)
    with st.expander("🏞️ The habitat of phytoplankton", expanded=False):
        st.markdown("""
        Discover where phytoplankton live and thrive! From sun-drenched surface waters to the mysterious depths below,
        phytoplankton inhabit diverse aquatic environments. Explore how light, nutrients, and mixing shape their habitat.
        """)
        st.image("Planktoomics/Phyto_1.webp", use_container_width=True)

    with st.expander("❄️ Algae bloom under lake ice", expanded=False):
        st.markdown("""
        Think lakes are lifeless in winter? Think again! Under the ice, fascinating phytoplankton blooms can occur,
        challenging our understanding of aquatic ecosystems. Learn how these tiny organisms survive and thrive in
        seemingly harsh winter conditions.
        """)
        st.image("Planktoomics/Phyto_2.webp", use_container_width=True)

    with st.expander("☀️ The life of the aquatic photosynthesis machine", expanded=False):
        st.markdown("""
        Phytoplankton are nature's oxygen factories! Just like land plants, they harness sunlight to produce energy
        through photosynthesis. Follow the amazing journey of these microscopic powerhouses as they fuel aquatic
        food webs and produce half of Earth's oxygen.
        """)
        st.image("Planktoomics/Phyto_3.webp", use_container_width=True)

    st.markdown("---")
    st.info("💡 **Did you know?** Phytoplankton produce approximately 50% of the oxygen we breathe, rivaling all terrestrial plants combined!")
