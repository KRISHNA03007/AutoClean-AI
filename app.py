import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Analytix AI",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
    <style>
    .main-title {
        background: linear-gradient(120deg, #1E3C72 0%, #2A5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        padding: 1rem 0;
    }

    .sub-title {
        font-size: 2rem;
        color: #2c3e50;
        text-align: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }

    .description-text {
        font-size: 1.2rem;
        color: #4A5568;
        text-align: center;
        line-height: 1.6;
        margin-bottom: 2rem;
        padding: 0 2rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 1.5rem;
    }

    .stButton > button {
        height: 50px;              /* keep vertical size */
        padding: 0 10px !important; /* reduce horizontal width */
        min-width: auto !important; /* allow it to shrink */
        border-radius: 25px;
        transition: all 0.3s ease;
        border: none;
        background-color: #ff6b6b !important;
        color: white !important;
        /* REMOVED font-size from here - this was causing the issue */
    } 

    .stButton > button:hover {
        transform: translateY(-3px);
        background-color: #ff5252 !important;
        color: white !important;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Custom card container for buttons */
    div[data-testid="column"] {
        background: white;
        border-radius: 12px;
        padding: 15px 10px 5px 10px;  /* Reduced bottom padding */
        margin: 0 20px;  /* Increased margin to 20px (approximately 1cm on most screens) */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }

    div[data-testid="column"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        border-color: #ff6b6b;
    }

    /* Adjust button inside column */
    div[data-testid="column"] .stButton {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;  /* Space between button and description */
    }

    /* FIXED: Extremely specific selector for buttons inside columns */
    div[data-testid="column"] .stButton > button {
        width: 70% !important;
        margin: 5px auto !important;
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%) !important;
        border-radius: 25px !important;
        letter-spacing: 1px;
        height: 105px !important;        /* TALLER BUTTON */
        /* FORCED font size with multiple properties */
        font-size: 2.2rem !important;    /* Even larger */
        font-weight: 900 !important;
        line-height: 1.2 !important;
        /* Additional properties to force the size */
        text-size-adjust: none !important;
        -webkit-text-size-adjust: none !important;
    }

    /* Target the button text specifically */
    div[data-testid="column"] .stButton > button p {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }

    /* Target any possible Streamlit-generated elements */
    div[data-testid="column"] .stButton > button span,
    div[data-testid="column"] .stButton > button div {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
    }

    /* Description box styling */
    .description-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #ff6b6b;
        border-radius: 8px;
        padding: 12px 10px;
        margin: 5px 5px 10px 5px;
        font-size: 0.85rem;
        color: #2c3e50;
        line-height: 1.5;
        text-align: left;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        min-height: 100px;  /* Ensure consistent height */
    }
    
    .description-title {
        font-weight: 700;
        color: #ff6b6b;
        margin-bottom: 5px;
        font-size: 0.95rem;
        border-bottom: 1px dashed #ff6b6b;
        padding-bottom: 3px;
    }

    /* Container for the columns */
    div.row-widget.stHorizontal {
        padding: 0 50px;
        gap: 20px;  /* Added gap of 20px between columns */
    }

    </style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown('<h1 class="main-title">Analytix AI</h1>', unsafe_allow_html=True)

# -------------------- DESCRIPTION --------------------
st.markdown(
    """
    <div class="sub-title">Intelligent Data Cleaning Assistant</div>
    <div class="description-text">
        Analyze, clean, and evaluate your datasets effortlessly with a smart, user-controlled workflow.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------- NAVIGATION BUTTONS WITH DESCRIPTIONS --------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Quick Insights", use_container_width=True):
        st.switch_page("pages/Quick_Insights.py")
    
    # Description box for Quick Insights (no heading, slightly bigger text)
    st.markdown("""
    <div class="description-box" style="font-size:0.95rem; line-height:1.7;">
        Explore your dataset at a glance. Get an overview of data, summary statistics, and data issues.
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Clean Data", use_container_width=True):
        st.switch_page("pages/Clean_Data.py")
    
    # Description box for Clean Data
    st.markdown("""
    <div class="description-box" style="font-size:0.95rem; line-height:1.7;">
        Advanced data cleaning module that transforms messy datasets into pristine, analysis-ready.
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("Visual Explorer", use_container_width=True):
        st.switch_page("pages/Visual_Explorer.py")
    
    # Description box for Quality Report
    st.markdown("""
    <div class="description-box" style="font-size:0.95rem; line-height:1.7;">
        Create dynamic visualizations to analyze distributions, trends, and feature relationships.
    </div>
    """, unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#555; padding:1rem;">
        Powered by AutoClean AI<br>Smart Data Preprocessing Made Simple
    </div>
    """,
    unsafe_allow_html=True
)