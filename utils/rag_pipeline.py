# utils/rag_pipeline.py
import streamlit as st
from openai import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from dotenv import load_dotenv
load_dotenv() 

# -------------------------
# Hard-coded OpenAI API key
# -------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Embeddings for FAISS
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
)

# Initialize FAISS session state
if "faiss_index" not in st.session_state:
    st.session_state["faiss_index"] = None
    st.session_state["faiss_docs"] = None


# -------------------------
# Ingest EHR + Claims into FAISS
# -------------------------
def ingest_data_for_rag():
    if "ehr_clean" not in st.session_state or "claims_clean" not in st.session_state:
        return "Upload and clean EHR & Claims data first."

    ehr = st.session_state["ehr_clean"]
    claims = st.session_state["claims_clean"]

    docs = []

    # Determine the correct patient ID column
    patient_col = "_id" if "_id" in ehr.columns else "patient_id"

    # Convert EHR rows to documents
    for _, row in ehr.iterrows():
        text = (
            f"Patient {row[patient_col]}, Age {row['age']}, Gender {row['gender']}, "
            f"Primary Diagnosis {row.get('primary_diagnosis','Unknown')}, "
            f"Secondary Diagnosis {row.get('secondary_diagnosis','Unknown')}, "
            f"Encounter Date {row.get('encounter_date','Unknown')}, "
            f"Notes: {row.get('notes','')}, Amount Paid: {row.get('amount_paid','0')}"
        )
        docs.append(Document(page_content=text, metadata={"patient_id": row[patient_col]}))

    # Claims -> documents
    for _, row in claims.iterrows():
        text = (
            f"Claim {row['claim_id']} for Patient {row['patient_id']}, "
            f"Procedure Code {row.get('procedure_code','Unknown')}, "
            f"Diagnosis Code {row.get('diagnosis_code','Unknown')}, "
            f"Amount Billed: {row.get('amount_billed','0')}, "
            f"Amount Paid: {row.get('amount_paid','0')}, "
            f"Claim Date: {row.get('claim_date','Unknown')}"
        )
        docs.append(Document(page_content=text, metadata={"patient_id": row["patient_id"]}))

    # Build FAISS index
    faiss_index = FAISS.from_documents(docs, embeddings)

    st.session_state["faiss_index"] = faiss_index
    st.session_state["faiss_docs"] = docs

    return f"Ingested {len(docs)} documents into FAISS for RAG retrieval."


# -------------------------
# Ask AI using FAISS + LLM
# -------------------------
def ask_ai(question, k=5):
    if st.session_state.get("faiss_index") is None:
        ingest_data_for_rag()  # auto-ingest if missing

    faiss_index = st.session_state.get("faiss_index")
    if faiss_index is None:
        return "Failed to ingest data. Please re-upload CSVs."

    # Retrieve top-k relevant documents
    results = faiss_index.similarity_search(question, k=k)
    context = "\n".join([doc.page_content for doc in results])

    system_prompt = f"""
You are a healthcare data assistant. Use ONLY the following retrieved data to answer the user's question:

{context}

If the question cannot be answered with this data, respond:
"This information is not available in the uploaded dataset."
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content