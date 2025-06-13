# frontend/app.py

import streamlit as st
import requests
import os

BACKEND_URL = "http://localhost:8000"

st.title("📄 Documind AI - Ask Questions on Your Documents")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        res = requests.post(f"{BACKEND_URL}/api/upload", files=files)
        if res.status_code == 200:
            st.success("✅ File uploaded and processed!")
            doc_id = uploaded_file.name
        else:
            st.error("❌ Failed to upload file.")
            st.stop()

    st.markdown("---")
    query = st.text_input("Ask a question about the document")

    if query and doc_id:
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/api/query",
                json={"query": query, "doc_id": doc_id}
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown("### 🧠 Answer:")
                st.write(answer)
            else:
                st.error("Failed to retrieve answer.")
