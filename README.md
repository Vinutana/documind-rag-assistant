# 📄 DocuMind – RAG-Based PDF Assistant

**DocuMind** is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions in natural language.

Instead of manually searching through lengthy documents, users can retrieve relevant information and receive AI-generated answers complete with exact document and page references.

---

## ✨ Key Features

- **Multi-PDF Support:** Upload and process multiple PDF documents simultaneously.
- **Smart Text Chunking:** Extract text and split documents into manageable, overlapping chunks.
- **Semantic Search:** Generate high-dimensional vector embeddings for accurate context matching.
- **Fast Vector Retrieval:** Retrieve relevant document chunks rapidly using FAISS.
- **Context-Aware Answers:** Generate accurate, grounded answers using Google Gemini.
- **Source Citations:** Automatically display document names and page references for every response.
- **Conversational Memory:** Ask follow-up questions seamlessly using conversation history.
- **Session Management:** Create, switch between, and manage multiple independent chat sessions.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Programming Language** | Python |
| **PDF Processing** | PyMuPDF |
| **Text Chunking** | LangChain |
| **Embeddings** | Google Gemini Embeddings |
| **Vector Database** | FAISS |
| **Large Language Model** | Google Gemini Flash |
| **Environment Configuration** | Python Dotenv |

---

## 🏗️ Application Architecture

1. **Document Upload:** Users upload PDF documents through the Streamlit interface.
2. **Text Extraction:** PyMuPDF extracts raw text and page metadata from the uploaded PDFs.
3. **Chunking:** LangChain splits the extracted text into smaller, context-preserving chunks.
4. **Embedding Generation:** Google Gemini generates vector embeddings for the text chunks.
5. **Vector Storage:** FAISS stores the embeddings in a local index for fast similarity search.
6. **Retrieval:** Relevant document chunks are retrieved based on the semantic similarity to the user's question.
7. **Answer Generation:** Google Gemini Flash generates a grounded answer using the retrieved context and chat history.
8. **Source References:** The application displays the source document names and corresponding page numbers alongside the response.

---

## 📁 Project Structure

```text
documind-rag-assistant/
├── app.py                   # Main Streamlit web application
├── config.py                # Configuration and environment settings
├── rag_pipeline.py          # Core RAG embedding, retrieval, and generation logic
├── document_processor.py    # PDF text extraction and chunking utilities
├── chat_manager.py          # Multi-session chat history management
├── prompts.py               # System and RAG prompt templates
├── utils.py                 # Helper functions
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── .env.example             # Example environment variables template
├── .gitignore               # Git ignore rules
├── assets/
│   └── style.css            # Custom UI styling
├── data/
│   └── .gitkeep             # Directory for temporary uploaded files
└── vector_store/
    └── .gitkeep             # Directory for local FAISS vector indexes
```

---

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vinutana/documind-rag-assistant.git
cd documind-rag-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

* **Activate on Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

* **Activate on macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root directory (you can copy `.env.example` as a starting point) and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
EMBEDDING_MODEL=models/gemini-embedding-2
```

> **Note:** Use a model ID supported by your Google AI API account. Never share or commit your `.env` file or API key to version control.

### 5. Run the application

```bash
streamlit run app.py
```

The application will automatically open in your default web browser.

---

## 💡 Usage

1. Upload one or more PDF documents using the sidebar uploader.
2. Click **Process Documents** to extract text and build the vector index.
3. Enter a question related to the uploaded documents in the chat input.
4. Review the AI-generated answer.
5. Expand or check the **Source References** to verify document names and page numbers.
6. Ask follow-up questions to explore the documents further.

---

## ⚠️ Current Limitations

- FAISS vector storage is currently maintained locally in memory.
- Chat history is maintained using Streamlit session state.
- Vector indexes and chat sessions are not persisted across application restarts.
- Authentication and multi-user access are not implemented.
- The application is currently a prototype and is not deployed as a production service.

---

## 🔮 Future Enhancements

- [ ] Persistent vector database storage (e.g., ChromaDB, Qdrant, or Pinecone).
- [ ] Persistent chat history using a relational or NoSQL database.
- [ ] Document-level access control and user authentication.
- [ ] RAG evaluation pipelines and retrieval-quality improvements (e.g., hybrid search, re-ranking).
- [ ] Cloud deployment and production monitoring.

---

## 👤 Author

Developed as a hands-on Generative AI project to explore Retrieval-Augmented Generation, semantic search, document processing, and LLM application development.