# app.py
import streamlit as st

st.set_page_config(
    page_title="HealthOps AI",
    page_icon="🏥",
    layout="wide"
)

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
<style>
.big-title {
    font-size: 48px;
    font-weight: 700;
    color: #0E1117;
}

.subtitle {
    font-size: 20px;
    color: #4F4F4F;
}

.feature-card {
    padding: 25px;
    border-radius: 15px;
    background-color: #F7F9FC;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    text-align: center;
}

.cta-button {
    background-color: #0066FF;
    color: white;
    padding: 10px 25px;
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Hero Section
# -------------------------
st.markdown('<p class="big-title">HealthOps AI</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">AI-Powered Healthcare Analytics Platform for Smarter Clinical & Financial Decisions</p>',
    unsafe_allow_html=True
)

st.write("")
st.write("")

col1, col2 = st.columns([1,1])

with col1:
    st.markdown("### 🚀 Transform Healthcare Data into Insights")
    st.write("""
    HealthOps AI helps hospitals and healthcare providers:
    - Analyze EHR and Claims data
    - Detect financial inefficiencies
    - Understand patient risk patterns
    - Make data-driven decisions
    """)

    if st.button("Get Started →"):
        st.switch_page("pages/1_Login.py")


st.write("---")

# -------------------------
# Features Section
# -------------------------
st.markdown("## 🔍 Platform Capabilities")

col1, col2, col3 = st.columns(3)

with col1:
    
    st.markdown("### 📂 Data Ingestion")
    st.write("Upload and standardize EHR and Claims datasets with automated cleaning.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    
    st.markdown("### 📊 Risk & Cost Modeling")
    st.write("Identify high-cost patients and financial risk trends.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    
    st.markdown("### 🤖 AI Insights Assistant")
    st.write("Ask natural language questions about your healthcare data.")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# -------------------------
# Why It Matters
# -------------------------
st.markdown("## 💡 Why HealthOps AI?")

st.write("""
Healthcare data is complex, fragmented, and difficult to analyze.  
HealthOps AI centralizes and simplifies your operational data, helping you:

- Reduce operational inefficiencies  
- Improve financial transparency  
- Support better patient outcomes  
- Enable AI-driven decision making  
""")

st.write("---")

# -------------------------
# Footer
# -------------------------
st.markdown("""
<center>
© 2026 HealthOps AI • Intelligent Healthcare Analytics
</center>
""", unsafe_allow_html=True)