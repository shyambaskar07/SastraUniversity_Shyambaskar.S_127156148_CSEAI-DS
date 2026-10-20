# Academic Integrity and AI-Tool Usage Declaration

## 1. Academic Integrity Declaration

I hereby declare that this capstone project entitled **"AUTOSAR High-Level Design (HLD) Document Analysis Assistant"** is my original work. All external libraries, frameworks, datasets, pre-trained models, and technical documentation have been properly cited and acknowledged. 

The experimental findings and evaluation results reported herein are genuine and reflect the actual performance of the implemented software. No results have been fabricated or manipulated.

- **Student Name**: Shyambaskar .S
- **Register Number**: 127156148
- **Degree / Branch**: B.Tech CSE(AI&DS)
- **Date**: 12-10-2026
- **Signature**: Shyambaskar.S

---

## 2. AI-Tool and Model Usage Declaration

In compliance with the project guidelines, the following table details all pre-trained models, AI APIs, and AI coding assistance utilized during the development of this project, along with their intended purposes and verification procedures:

| AI Model / Tool | Purpose | Artifact Affected | Verification Procedure by Student |
| :--- | :--- | :--- | :--- |
| **Llama 3.1 8B (`llama-3.1-8b-instant`)** | Primary conversational LLM for RAG response generation and page citations | `rag_pipeline.py`, runtime query answers | Verified model responses against ground-truth tables in the source PDF (`ADAS_AUTOSAR_HLD_v2.pdf`). |
| **Mixtral 8x7B (`mixtral-8x7b-32768`)** | High-availability fallback model in case of rate limits or service interruptions | `rag_pipeline.py` fallback chain | Tested automatic failover behavior by simulating high concurrency queries. |
| **Hugging Face `all-MiniLM-L6-v2`** | Local semantic text embedding model for document chunk representation | Local ChromaDB vector index (`chroma_db`) | Inspected vector dimensions (384-d) and verified semantic search ranking accuracy on test queries. |
| **AI Coding Assistant (Gemini/AntiGravity)** | Code scaffolding, documentation structuring, and debugging assistance | Application layout, requirements specification, and report scaffolding | Rigorously reviewed all code syntax, executed automated test scripts, eliminated deprecated endpoints, and verified full functionality. |

---

## 3. Student Accountability

I understand that I remain fully accountable for the correctness and architectural integrity of the entire project codebase. I am prepared to explain and defend every component, algorithm, prompt design, and configuration setting submitted in this repository during the evaluation viva.
