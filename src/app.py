import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

# Modern LangChain Imports
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURATION ---
st.set_page_config(page_title="Enterprise Dynamic RAG", layout="wide")
st.title("📄 Enterprise Document Analyzer")
st.markdown("Upload any report, policy, or manual (up to 100 pages) for instant Q&A.")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# --- SIDEBAR: UPLOAD & INGESTION ---
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Drop a PDF here", type="pdf")
    process_btn = st.button("Process Document")
    st.markdown("---")
    st.markdown("**Architecture Notes:**\n* Embeddings: HuggingFace (Local CPU)\n* LLM: Gemini 2.5 Flash\n* Vector Store: Ephemeral FAISS\n* Framework: LangChain LCEL")

# --- MAIN LOGIC: PROCESSING ---
if uploaded_file and process_btn:
    with st.spinner("Analyzing and chunking document... this takes a few seconds for large PDFs."):
        temp_path = "temp_upload.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        loader = PyPDFLoader(temp_path)
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = text_splitter.split_documents(data)
        
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embeddings)
        
        st.session_state.vector_db = vector_db
        st.session_state.file_name = uploaded_file.name
        
        os.remove(temp_path)
        st.success("✅ Document embedded successfully!")

# --- MAIN LOGIC: CHAT INTERFACE ---
if "vector_db" in st.session_state:
    st.subheader(f"💬 Chatting with: `{st.session_state.file_name}`")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
    
    # 1. Define the Prompt Template
    system_prompt = (
        "You are an expert analyst. Use the provided context to answer the user's question accurately. "
        "If you do not know the answer based on the context, state that you do not know. "
        "\n\n"
        "Context: {context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # 2. Create the Modern Retrieval Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(
        st.session_state.vector_db.as_retriever(search_kwargs={"k": 6}), 
        question_answer_chain
    )

    # Chat UI
    user_query = st.chat_input("Ask a question about the document...")
    
    if user_query:
        st.chat_message("user").write(user_query)
        
        with st.spinner("Searching document..."):
            # The modern chain uses 'input' instead of 'query'
            response = qa_chain.invoke({"input": user_query})
            
            with st.chat_message("assistant"):
                # The modern chain returns 'answer' instead of 'result'
                st.write(response["answer"])
                
                with st.expander("🔍 View Source Pages"):
                    # The modern chain stores source documents in 'context'
                    for doc in response["context"]:
                        st.info(f"**Page {doc.metadata.get('page', 'Unknown')}**: {doc.page_content[:300]}...")