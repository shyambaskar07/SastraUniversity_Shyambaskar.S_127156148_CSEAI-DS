# Model and Prompt Configuration

This directory contains the configuration parameters, prompt engineering templates, and model orchestration specifications for the AUTOSAR High-Level Design (HLD) Document Analysis Assistant.

## 1. Large Language Model Configuration

- **Provider**: Groq Cloud Platform
- **Primary Model**: `qwen/qwen3.8-27b`
  - High inference throughput with fast response times.
  - Temperature: 0.0 (ensures deterministic, strictly factual responses).
- **Fallback Model**: `openai/gpt-oss-120b`
  - Deployed automatically via LangChain's `.with_fallbacks()` mechanism if the primary model experiences rate limits or service interruptions.
  - Temperature: 0.0.
- **Output Style**: Professional, humanized technical prose. Emojis and ungrounded conjectures are strictly filtered.

## 2. Embedding Model and Vector Store

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace
  - Local inference running entirely on CPU.
  - Vector dimensionality: 384 dimensions.
  - Offline capability ensuring engineering document privacy.
- **Vector Database**: ChromaDB
  - Local disk persistence in `chroma_db/`.
  - Ingestion strategy: PyMuPDFLoader extracting raw text and page metadata.
  - Splitting: RecursiveCharacterTextSplitter with chunk size of 1000 characters and 200 characters overlap.
  - Retrieval: Similarity search retrieving top `k=4` relevant document passages.

## 3. Prompt Engineering and Grounding Strategy

The prompt is structured to enforce grounded question answering and prevent hallucinations:

1. **Role Definition**: Directs the LLM to operate as an automotive software architecture specialist.
2. **Context Restriction**: Restricts answers strictly to the retrieved context chunks.
3. **Mandatory Citations**: Mandates explicit page number citations (e.g., `[Source: Page 2]`) for every factual assertion.
4. **Style Constraint**: Prohibits emojis and casual conversational tropes.
5. **Out-of-Domain Guardrail**: Forces the model to state `"I cannot find the answer in the approved architecture documents"` whenever the retrieved context does not contain sufficient information.

## 4. Responsible AI & Traceability

- **Traceability**: All responses are traceable back to the source PDF and specific page numbers.
- **Human Oversight**: The assistant acts as an engineering companion, providing references for human engineers to review rather than executing autonomous changes.
- **Privacy**: Proprietary documents remain in the local vector database. Only retrieved context chunks are transmitted to the LLM during query resolution.
