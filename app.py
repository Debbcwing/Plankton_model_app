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

# RAG system imports moved to Home tab for lazy loading
# (Only loads when user visits Home tab)

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
sidebar_items = ["Home", "Data", "Model", "Manuscripts", "Planktoomics"]

with st.sidebar:
    selected = option_menu(
        None,                                       # Title at the top of sidebar
        sidebar_items,                              # Menu items
        icons=["house", "graph-up", "activity", "file-text", "book"],   # Matching icons
        # menu_icon="cast",                         # Icon for the menu title
        default_index=0,                            # Which tab opens first
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
                    "and Swiss National Science Foundation (SNF) as part of the project AQUASCOPE (grant No. 412375259).")



# ---------------------- HOME PAGE ----------------------
if selected == sidebar_items[0]:
    st.title("Hello👋🏼  Ask me anything about my PhD research on plankton modeling!")

    # Lazy import RAG libraries (only when Home tab is accessed)
    from rag_setup import RAGSystem
    from langchain_anthropic import ChatAnthropic
    from langchain.chains import RetrievalQA

    # Initialize RAG system
    @st.cache_resource(show_spinner=False)
    def load_rag_system():
        """Load RAG system (cached to avoid reloading)."""
        rag = RAGSystem()
        rag.setup(force_rebuild=False)
        return rag

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
        # Load RAG system
        try:
            with st.spinner("Loading..."):
                rag_system = load_rag_system()

            # Initialize Claude
            llm = ChatAnthropic(
                model="claude-3-5-haiku-20241022",
                anthropic_api_key=api_key,
                temperature=0.5,
                max_tokens=300
            )

            # Load custom prompt template from file
            from langchain.prompts import PromptTemplate

            with open("prompt_template.txt", "r") as f:
                prompt_template = f.read()

            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )

            # Create QA chain with custom prompt
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=rag_system.vectorstore.as_retriever(
                    search_kwargs={"k": 2}  # Return top 3 relevant chunks
                ),
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )

            # Show example Q&A pairs
            with st.expander("💡  Some common questions and answers"):
                # st.markdown("### Example 1")
                st.markdown("**Q: What is the main focus of your PhD research?**")
                st.markdown("**A:** My research is all about understanding how tiny organisms called plankton grow and interact in lakes! I built computer models to simulate how different types of phytoplankton (the plant-like plankton) compete for nutrients and respond to changes in their environment. Think of it like creating a virtual aquarium to study how different factors—like temperature, light, and nutrient availability—affect which species thrive and which ones struggle.")

                st.markdown("---")
                # st.markdown("### Example 2")
                st.markdown("**Q: How does your model handle nutrient dynamics?**")
                st.markdown("**A:** Great question! The model tracks how nutrients like nitrogen and phosphorus move through the water. Imagine nutrients as food for plankton—they get taken up by phytoplankton, then passed along when zooplankton eat the phytoplankton. The model also simulates how nutrients get recycled back into the water when organisms die or produce waste. It's like tracking a nutrient cycle in a mini ecosystem!")

                st.markdown("---")
                # st.markdown("### Example 3")
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
                    result = qa_chain.invoke({"query": user_question})

                    # Display answer
                    st.subheader("Answer:")
                    st.write(result["result"])

                    # Show sources
                    with st.expander("📚 View source documents"):
                        for i, doc in enumerate(result["source_documents"], 1):
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
            st.error(f"Error loading RAG system: {str(e)}")
            st.info(
                "If this is your first time running the app, you need to build the vector database:\n\n"
                "Run this command in your terminal:\n"
                "```bash\n"
                "python rag_setup.py\n"
                "```"
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
    st.header("📚 Publications")
    st.write("Explore my peer-reviewed research on phytoplankton size structure and community dynamics in lake ecosystems.")

    tab_names_ms = ["Manuscript 1 (2024)", "Manuscript 2 (2025)", "Manuscript 3 (Under Review)"]
    tab1, tab2, tab3 = st.tabs(tab_names_ms)

    # ========== Manuscript 1 (2024) ==========
    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Grazing strategies determine the size composition of phytoplankton in eutrophic lakes")
            st.markdown("**Authors:** Sze-Wing To, Esteban Acevedo-Trejos, Subhendu Chakraborty, Francesco Pomati, Agostino Merico")
            st.markdown("**Journal:** *Limnology and Oceanography*, 69:933–946 (2024)")
            st.markdown("**DOI:** [10.1002/lno.12538](https://doi.org/10.1002/lno.12538)")

        with col2:
            st.download_button(
                label="📄 Download PDF",
                data=open("MS/To et al. (2024).pdf", "rb"),
                file_name="To_et_al_2024.pdf",
                mime="application/pdf"
            )
            st.download_button(
                label="📊 Supplementary Material",
                data=open("MS/To et al. (2024)supp.pdf", "rb"),
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
            st.markdown("**Authors:** Sze-Wing To, Esteban Acevedo-Trejos, Sherwood Lan Smith, Subhendu Chakraborty, Agostino Merico")
            st.markdown("**Journal:** *Ecological Modelling*, 499:110936 (2025)")
            st.markdown("**DOI:** [10.1016/j.ecolmodel.2024.110936](https://doi.org/10.1016/j.ecolmodel.2024.110936)")

        with col2:
            st.download_button(
                label="📄 Download PDF",
                data=open("MS/To et al. (2025).pdf", "rb"),
                file_name="To_et_al_2025.pdf",
                mime="application/pdf"
            )
            st.download_button(
                label="📊 Supplementary Material",
                data=open("MS/To et al. (2025)supp.pdf", "rb"),
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



# ---------------------- Planktoomics ----------------------
if selected == sidebar_items[4]:
    st.header("🌊 Planktoomics: Stories of Phytoplankton")
    st.write("Dive into the fascinating world of phytoplankton through visual storytelling!")

    # Introduction image (optimized WebP format - 95% smaller!)
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
