from app.db.session import SessionLocal
from app.models.knowledge import KnowledgeDocument
import logging

try:
    db = SessionLocal()
    business_id = "00000000-0000-0000-0000-000000000000"
    doc = KnowledgeDocument(title="test.txt", business_id=business_id)
    db.add(doc)
    db.commit()
    print("Success inserting document")
except Exception as e:
    print(f"Error inserting: {e}")
finally:
    db.close()
