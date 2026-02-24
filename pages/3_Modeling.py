import streamlit as st
import pandas as pd
from utils.modeling import train_model

st.set_page_config(page_title="HealthOps AI - Risk Modeling", layout="wide")
st.title("📊 Risk Modeling Dashboard")

st.warning("Upload and clean data first in the Data Ingestion page!")

# Get cleaned data from session state (set in ingestion page)
ehr_clean = st.session_state.get('ehr_clean')
claims_clean = st.session_state.get('claims_clean')

if ehr_clean is not None and claims_clean is not None:
    st.info("Training model...")

    # Combine datasets if needed
    data = ehr_clean.copy()
    
    # If risk_flag doesn't exist, generate synthetic target
    if 'risk_flag' not in data.columns:
        st.warning("No 'risk_flag' found — generating synthetic target.")
        median_amount = claims_clean['amount_billed'].median() if 'amount_billed' in claims_clean.columns else 1000
        data['risk_flag'] = (claims_clean['amount_billed'] > median_amount).astype(int) if 'amount_billed' in claims_clean.columns else pd.Series([0]*len(data))
    
    # Train model
    model, metrics = train_model(data)

    st.success("Model trained!")

    st.subheader("Metrics")
    for k, v in metrics.items():
        st.write(f"**{k}:** {v:.2f}")

else:
    st.warning("Please complete data ingestion first.")