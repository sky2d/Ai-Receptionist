import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.document_processor import process_and_store_document, search_knowledge_base

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    business_id: str = "00000000-0000-0000-0000-000000000000"

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    business_id: str = "00000000-0000-0000-0000-000000000000",
    db: Session = Depends(get_db)
):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
        
    # Save file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        doc = process_and_store_document(db, temp_path, file.filename, business_id)
        return {"status": "success", "document_id": doc.id, "filename": doc.title}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/query")
async def query_documents(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        results = search_knowledge_base(db, request.query, request.business_id)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
