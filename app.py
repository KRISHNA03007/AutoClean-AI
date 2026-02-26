import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AutoClean AI",
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
        height: 45px;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        margin: 10px 0;
        background-color: #ff6b6b !important;
        color: white !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        background-color: #ff5252 !important;
        color: white !important;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    </style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown('<h1 class="main-title">AutoClean AI</h1>', unsafe_allow_html=True)

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

# -------------------- NAVIGATION BUTTONS --------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Quick Insights", use_container_width=True):
        st.switch_page("pages/Quick_Insights.py")

with col2:
    if st.button("Clean Data", use_container_width=True):
        st.switch_page("pages/Clean_Data.py")

with col3:
    if st.button("Quality Report", use_container_width=True):
        st.switch_page("pages/Quality_Report.py")

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#555; padding:1rem;">
        Powered by AutoClean AI | Smart Data Preprocessing Made Simple
    </div>
    """,
    unsafe_allow_html=True
)