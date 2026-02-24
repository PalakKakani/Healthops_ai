import streamlit as st
from utils.rag_pipeline import ask_ai

st.set_page_config(page_title="HealthOps AI - AI Assistant", layout="wide")
st.title("💬 AI Policy Assistant")

st.markdown("""
Ask any question about your uploaded healthcare data.
Example: `Show all encounters for patient P0001.`
""")

question = st.text_input("Ask a question about your data:")

if question:
    response = ask_ai(question)
    st.subheader("Answer:")
    st.write(response)