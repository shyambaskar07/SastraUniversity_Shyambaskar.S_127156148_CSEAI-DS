import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CHROMA_PATH = "chroma_db"
GROQ_API_KEY = "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"

def get_embeddings():
    # Local embeddings model, fast and runs offline
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_pdf(file_path: str):
    """Loads a PDF, chunks it, and saves embeddings to local ChromaDB."""
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # Store locally
    vectorstore = Chroma.from_documents(documents=splits, embedding=get_embeddings(), persist_directory=CHROMA_PATH)
    return len(splits)

def query_rag(query: str):
    """Retrieves relevant chunks and generates a cited response using Groq."""
    
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # Primary model: Qwen 3.8 27B on Groq
    llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0, api_key=GROQ_API_KEY)
    # Fallback model: OpenAI GPT-OSS 120B on Groq
    fallback_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=GROQ_API_KEY)
    llm_with_fallback = llm.with_fallbacks([fallback_llm])
    
    prompt_file = os.path.join(os.path.dirname(__file__), "..", "..", "Model_Prompts_Config", "system_prompt.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            template = f.read().strip()
    else:
        template = """You are an AI assistant for Automotive Engineering, specifically analyzing AUTOSAR High-Level Design (HLD) documents.
Answer the question based only on the following context. You MUST cite the exact page number(s) where you found the information.
If the answer is not in the context, say "I cannot find the answer in the approved architecture documents."

Context: {context}

Question: {question}

Answer: """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        # Format the context so the LLM can see the page numbers for citation
        formatted = []
        for doc in docs:
            page = doc.metadata.get('page', 'Unknown')
            # PyMuPDF pages are 0-indexed, so we add 1 for user-friendly page numbers
            if isinstance(page, int):
                page += 1
            formatted.append(f"[Source: Page {page}]:\n{doc.page_content}")
        return "\n\n".join(formatted)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_with_fallback
        | StrOutputParser()
    )
    
    try:
        return rag_chain.invoke(query)
    except Exception as e:
        return f"Error: Groq API failed after attempting fallbacks. Details: {str(e)}"
