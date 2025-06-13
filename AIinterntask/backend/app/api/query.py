# backend/app/api/query.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.query_service import query_ollama_and_rank


router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    doc_id: str

@router.post("/query")
async def query_document(request: QueryRequest):
    try:
        answer = query_ollama_and_rank(request.query, request.doc_id)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
