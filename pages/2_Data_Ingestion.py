import streamlit as st
import pandas as pd
from utils.data_cleaning import clean_healthcare_data
from utils.rag_pipeline import ingest_data_for_rag

st.set_page_config(page_title="HealthOps AI - Data Ingestion", layout="wide")
st.title("📂 Data Ingestion & Standardization")

st.markdown("""
Upload your healthcare datasets (EHR and Claims).  
We'll clean, normalize, and prepare the data for AI retrieval.
""")

# -------------------------
# File Upload
# -------------------------
ehr_file = st.file_uploader("Upload EHR CSV", type=["csv"])
claims_file = st.file_uploader("Upload Claims CSV", type=["csv"])

# -------------------------
# Process files if both uploaded
# -------------------------
if ehr_file and claims_file:
    ehr_df = pd.read_csv(ehr_file, dtype=str)
    claims_df = pd.read_csv(claims_file, dtype=str)

    # Clean data
    st.info("Cleaning and normalizing data...")
    ehr_clean, claims_clean = clean_healthcare_data(ehr_df, claims_df)

    # Force all columns to string
    ehr_clean = ehr_clean.astype(str)
    claims_clean = claims_clean.astype(str)

    # Store in session_state
    st.session_state['ehr_clean'] = ehr_clean
    st.session_state['claims_clean'] = claims_clean

    st.success("✅ Data ingestion and cleaning complete!")

    # -------------------------
    # Auto-ingest for RAG
    # -------------------------
    st.info("Ingesting data into FAISS for AI...")
    message = ingest_data_for_rag()
    st.success(message)

# -------------------------
# Display Metrics if data exists
# -------------------------
if 'ehr_clean' in st.session_state and 'claims_clean' in st.session_state:
    ehr_clean = st.session_state['ehr_clean']
    claims_clean = st.session_state['claims_clean']

    st.subheader("📊 Data Quality Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("EHR Missing %", f"{ehr_clean.isna().mean().mean()*100:.2f}%")
    col2.metric("Claims Missing %", f"{claims_clean.isna().mean().mean()*100:.2f}%")

    # # Optional: Top 5 diagnoses
    # if 'primary_diagnosis' in ehr_clean.columns:
    #     diag_counts = ehr_clean['primary_diagnosis'].fillna("Unknown").value_counts().head(5)
    #     col3.write("**Top 5 Diagnoses**")
    #     col3.bar_chart(diag_counts)

# -------------------------
# Warn user if files not uploaded
# -------------------------
else:
    st.warning("Please upload both EHR and Claims CSV files to continue.")