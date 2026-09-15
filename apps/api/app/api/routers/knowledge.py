from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.document_processor import process_and_store_document
import shutil
import os

router = APIRouter(tags=["knowledge"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not file.filename.endswith((".pdf", ".txt")):
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
            
        # Default business ID for the prototype
        business_id = "00000000-0000-0000-0000-000000000000"
        
        # Save file temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process and store in Vector DB
        doc = process_and_store_document(db, temp_path, file.filename, business_id)
        
        # Cleanup temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return {"status": "success", "message": f"Document {file.filename} processed successfully", "document_id": doc.id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/")
async def list_documents(db: Session = Depends(get_db)):
    from app.models.knowledge import KnowledgeDocument
    business_id = "00000000-0000-0000-0000-000000000000"
    docs = db.query(KnowledgeDocument).filter(KnowledgeDocument.business_id == business_id).all()
    return {"documents": [{"id": d.id, "title": d.title, "created_at": d.created_at} for d in docs]}

@router.delete("/{document_id}")
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    from app.models.knowledge import KnowledgeDocument
    business_id = "00000000-0000-0000-0000-000000000000"
    
    doc = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.id == document_id,
        KnowledgeDocument.business_id == business_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    db.delete(doc)
    db.commit()
    return {"status": "success", "message": "Document deleted"}
