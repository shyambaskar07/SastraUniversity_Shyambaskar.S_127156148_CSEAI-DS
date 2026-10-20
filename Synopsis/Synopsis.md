# Project Synopsis

## 1. Project Title
**AUTOSAR High-Level Design (HLD) Document Analysis Assistant**

## 2. Domain & Case Study Context
- **Domain**: Automotive Software Engineering & Embedded Systems
- **Industry Standard**: AUTOSAR (AUTomotive Open System ARchitecture) Classic Platform
- **Safety Standard**: ISO 26262 (ASIL D Functional Safety) & ISO 21434 (Automotive Cybersecurity)

## 3. Problem Statement
Automotive software architectures are described in dense, highly technical High-Level Design (HLD) specifications that can span hundreds of pages. Systems engineers, software developers, and safety assessors spend significant time cross-referencing:
- Component interfaces (RPorts and PPorts over the RTE)
- Basic Software (BSW) dependencies (DCM, NvM, CommStack)
- Functional safety signal mappings (E2E protection profiles)
- Cybersecurity requirements (SecOC protocols)

Manual interpretation often leads to misinterpretation, missed architectural constraints, and extended review cycles.

## 4. Proposed Solution
This project implements an AI-enabled **Domain-Specific RAG (Retrieval-Augmented Generation) Assistant** tailored specifically for automotive architecture documents. 

Key architectural components include:
1. **Document Ingestion & Semantic Chunking**: Parsing PDF architecture documents with page preservation.
2. **Local Dense Vector Embeddings**: Utilizing `sentence-transformers/all-MiniLM-L6-v2` locally to ensure data privacy of confidential automotive IP.
3. **Local Vector Database**: Vector storage and similarity retrieval via ChromaDB.
4. **Grounded LLM Reasoning Engine**: High-throughput inference powered by Groq (`llama-3.1-8b-instant`) with automatic failover to `mixtral-8x7b-32768`.
5. **Traceable Page Citations**: Strict prompt engineering mandating exact page citations (`[Source: Page X]`) for every technical response.
6. **Hallucination Defense**: Zero-hallucination constraint that explicitly refuses out-of-domain answers.

## 5. Technology Stack
- **User Interface**: Streamlit (Python)
- **Backend Service**: FastAPI with Uvicorn
- **AI / RAG Framework**: LangChain
- **Embeddings**: HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Storage**: ChromaDB
- **LLM Provider**: Groq Cloud Platform

## 6. Expected Outcomes
- Rapid retrieval of component ports, interfaces, and safety mappings in seconds.
- 100% traceable references linking answers to approved architectural documentation.
- Elimination of ungrounded hallucinated information in mission-critical automotive software design.
