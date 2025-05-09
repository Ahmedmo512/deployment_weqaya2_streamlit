import streamlit as st
from PIL import Image
import time

# Configure page settings (changed from wide to centered)
st.set_page_config(
    page_title="WEQAYA - Preventive Healthcare AI",
    page_icon="🩺",
    layout="centered",  # Changed from wide to centered
    initial_sidebar_state="expanded"
)

# Custom CSS styling with dark mode support
st.markdown("""
    <style>
    :root {
        --primary-color: #D71313;
        --text-color: #333333;
        --bg-color: #FFFFFF;
        --card-bg: #F8F9FA;
        --hover-bg: #F0F2F6;
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #F0F0F0;
            --bg-color: #121212;
            --card-bg: #1E1E1E;
            --hover-bg: #2D2D2D;
        }
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        color: var(--text-color);
    }
    .feature-card {
        transition: transform 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-card h3 {
        color: var(--primary-color);
    }
    .nav-item {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .nav-item:hover {
        background-color: var(--hover-bg);
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: var(--text-color);
        font-size: 0.9rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER SECTION ----------
st.markdown('<p class="main-title">WEQAYA وقاية</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-Powered Preventive Healthcare Platform</p>', unsafe_allow_html=True)

# Hero Image
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    hero_img = "https://www.aeologic.com/blog/wp-content/uploads/2023/09/Health-Care-with-Artificial-Intelligence.png"
    st.image(hero_img, caption="AI in Healthcare")

# ---------- KEY FEATURES ----------
st.markdown("## 🔍 Core Features")
features = st.columns(3)
with features[0]:
    st.markdown("""
    <div class="info-box feature-card">
        <h3>🧠 Stroke Prediction</h3>
        <p>Early warning system for stroke risk assessment</p>
    </div>
    """, unsafe_allow_html=True)

with features[1]:
    st.markdown("""
    <div class="info-box feature-card">
        <h3>❤️ Hypertension Analysis</h3>
        <p>Early warning system for hypertension risk</p>
    </div>
    """, unsafe_allow_html=True)

with features[2]:
    st.markdown("""
    <div class="info-box feature-card">
        <h3>🩸 Diabetes Detection</h3>
        <p>Early warning system for diabetes risk assessment</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- ABOUT SECTION ----------
with st.expander("ℹ️ About WEQAYA (وقاية)", expanded=True):
    about_content = """
    **WEQAYA** (meaning "Prevention" in Arabic) is an intelligent healthcare platform that leverages artificial intelligence to:

    - Detect chronic diseases at early stages (stroke, diabetes, hypertension)
    - Provide personalized risk assessments
    - Offer preventive care recommendations
    - Support healthcare decision-making

    Our mission is to bridge the gap between healthcare providers and patients through predictive analytics and early intervention.
    """
    st.markdown(about_content)

# ---------- PREDICTION MODULES ----------
st.markdown("## 🚀 Get Started")
pred_cols = st.columns(3)
with pred_cols[0]:
    if st.button("🧠 Stroke Risk Check", 
                use_container_width=True,
                help="Evaluate your stroke risk factors"):
        st.switch_page("pages/1_stroke.py")

with pred_cols[1]:
    if st.button("❤️ Hypertension Check", 
                use_container_width=True,
                help="Analyze your blood pressure patterns"):
        st.switch_page("pages/2_hypertension.py")

with pred_cols[2]:
    if st.button("🩸 Diabetes Check", 
                use_container_width=True,
                help="Check your diabetes risk profile"):
        st.switch_page("pages/3_diabetes.py")

# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.image("weqaya.jpg", width=200)
    st.title("Navigation")
    
    nav_options = {
        "🏠 Home": "home_page.py",
        "🧠 Stroke Prediction": "pages/1_stroke.py",
        "❤️ Hypertension Check": "pages/2_hypertension.py",
        "🩸 Diabetes Analysis": "pages/3_diabetes.py"
    }
    
    for label, page in nav_options.items():
        if st.button(label, key=label, use_container_width=True):
            st.switch_page(page)

    st.markdown("---")
    st.markdown("### Need Help?")
    st.markdown("📞 Contact our support team")
    st.markdown("📧 support@weqaya.ai")

# ---------- FOOTER ----------
with st.spinner("Loading health insights..."):
    time.sleep(1)
    st.toast("System ready!", icon="✅")

st.markdown("---")
st.markdown("""
<div class="footer">
    © 2025 WEQAYA Health Technologies | 
    <a href="#" style="color: var(--text-color);">Privacy Policy</a> | 
    <a href="#" style="color: var(--text-color);">Terms of Service</a>
</div>
""", unsafe_allow_html=True)