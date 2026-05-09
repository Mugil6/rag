Enterprise Document Intelligence (RAG)

An advanced Retrieval-Augmented Generation (RAG) pipeline designed to ingest, analyze, and summarize large-scale enterprise documents (up to 100+ pages) in real-time. Built specifically to demonstrate the application of Generative AI in processing complex corporate reports and technical manuals.

Access the app here - https://u9rw8uwgfypfig2gqqrget.streamlit.app/

✨ Features

    Dynamic Ingestion: Upload any PDF (tested up to 120 pages) for instant processing.

    Intelligent Chunking: Uses RecursiveCharacterTextSplitter to maintain semantic context across tables and long-form prose.

    Privacy-First Embeddings: Generates embeddings locally on the CPU using Hugging Face, reducing API latency and cost.

    Advanced Reasoning: Powered by Gemini 3.1 Flash-Lite for high-speed, high-accuracy summarization and Q&A.

    Source Attribution: Every response includes direct citations and page references to prevent hallucinations and ensure auditability.

🛠️ Tech Stack

    Orchestration: LangChain (LCEL)

    LLM: Google Gemini (Generative AI)

    Embeddings: HuggingFace (all-MiniLM-L6-v2)

    Vector Store: FAISS (Facebook AI Similarity Search)

    Frontend: Streamlit
⚙️ Installation & Setup
1. Clone the Repository
   git clone https://github.com/Mugil6/rag.git
   cd rag
2. Create and Activate Virtual Environment
   python -m venv venv
   Set-ExecutionPolicy Unrestricted -Scope CurrentUser
   .\venv\Scripts\activate
3. Install Dependencies
   pip install -r requirements.txt
🔐 Configuration (Secrets)

To keep API keys secure, this project uses Streamlit's Secret Management.

    Create a folder named .streamlit in the root directory.

    Create a file named secrets.toml inside that folder.

    Add your Google API Key
🏗️ Architecture Highlights
Hybrid Processing Strategy

To optimize for a professional environment, this pipeline uses a hybrid approach:

    **Local Processing**: Tokenization and Vectorization are handled locally on the host machine. This demonstrates a cost-effective architecture that minimizes data egress.

    **Global Reasoning**: Only the most relevant text chunks (Top-K) are sent to the LLM. This allows the system to process a 118-page document (like the Apple Environmental Report) while remaining well within the model's context limits.
Session State Management

The vector database is stored in the st.session_state. This ensures that once a large document is processed, it remains available for the duration of the user's session without needing to re-ingest the data for every follow-up question.

👨‍💻 Developed By
Mugilan M | Data Engineer | 

MIT License

Copyright (c) 2026 Mugilan M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
