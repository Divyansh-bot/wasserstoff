

````markdown
# 📄 Documind AI – Ask Questions on Your Documents

**Documind AI** is an offline, privacy-first intelligent document question-answering system. It allows users to upload PDF documents and query them using natural language. Responses are generated based on document content using local LLMs like **Mistral** via **Ollama**.

---

## 🚀 Features

- 📁 Upload PDFs and parse all text, including scanned text (OCR).
- 🤖 Ask questions and get accurate, contextual answers from your own documents.
- 🔐 100% offline processing with no cloud or external dependencies.
- 🧠 Uses Ollama + Mistral for local inference.
- 📦 Lightweight vector database using FAISS and local JSON storage.

---

## 📂 Project Structure

```bash
documind/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   └── query.py
│   │   ├── embeddings/
│   │   │   └── mistral_embedder.py
│   │   ├── chunking/
│   │   │   └── text_splitter.py
│   │   ├── utils/
│   │   │   ├── document_parser.py
│   │   │   └── clean_text.py
│   │   ├── vector_store/
│   │   │   └── vector_store.py
│   │   ├── services/
│   │   │   └── query_service.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/ (optional: if using React or HTML frontend)
└── README.md
````

---

## 🛠️ Prerequisites

* Python 3.10 or 3.11
* [Ollama](https://ollama.com/) installed and running locally
* [Git](https://git-scm.com/) installed
* Visual C++ Build Tools (for PyMuPDF and FAISS on Windows)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/documind-ai.git
cd documind-ai/backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you get errors with `faiss`, run:

```bash
pip install faiss-cpu
```

---

## 🤖 Run Ollama (Mistral)

Start Ollama and pull the model:

```bash
ollama run mistral
```

This will start the local model server at `http://localhost:11434`.

---

## ▶️ Run the Backend Server

```bash
uvicorn app.main:app --reload
```

Server will run at `http://127.0.0.1:8000`.

---

## 🌐 Frontend Usage

Visit `http://localhost:3000` (if using React frontend), or use Postman/cURL:

### Upload a Document:

```http
POST /api/upload
Form-data: file=<your PDF>
```

### Ask a Question:

```http
POST /api/query
JSON body:
{
  "query": "What is the summary of the document?",
  "source": "filename.pdf"
}
```

---

## 🧪 Sample Queries

* "Summarise the whole document"
* "What is the CGPA mentioned?"
* "List key skills and experience"
* "Who is the author of this resume?"

---

## 💾 Data Storage

* Embeddings stored in: `app/vector_store/index.faiss`
* Metadata stored in: `app/vector_store/meta.pkl`

---

## 🔒 Privacy

This app runs entirely on your local machine. No data is sent to the cloud or third-party APIs.

---

## 🙋‍♂️ Troubleshooting

* ❗ **CropBox missing warning?**

  * Ignore, it comes from `pdfplumber`.

* ❗ **"I don't know" answers?**

  * Check if the chunking missed your content or your question is too generic.

* ❗ **FAISS errors?**

  * Ensure `backend/app/vector_store` directory exists.





