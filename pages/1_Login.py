import streamlit as st

st.title("🔐 Secure Access Portal")

roles = ["Admin", "Analyst", "Executive", "Policy Reviewer"]
selected_role = st.selectbox("Select Your Role", roles)

if st.button("Login"):
    st.session_state["role"] = selected_role
    st.success(f"Logged in as {selected_role}")