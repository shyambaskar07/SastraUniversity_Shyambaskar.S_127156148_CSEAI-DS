from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import shutil
import os
from rag_pipeline import ingest_pdf, query_rag

app = FastAPI(title="AUTOSAR HLD Document Analysis API")

class QueryRequest(BaseModel):
    query: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Endpoint to upload a PDF and ingest it into the vector database."""
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks_created = ingest_pdf(temp_file_path)
        return {"status": "success", "message": f"Successfully ingested {file.filename} into {chunks_created} chunks."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/query")
async def ask_question(request: QueryRequest):
    """Endpoint to ask a question to the RAG system."""
    try:
        answer = query_rag(request.query)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "AUTOSAR HLD Analysis Backend is running."}
