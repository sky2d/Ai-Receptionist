from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk

# Load model globally (will load into memory on startup)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

class RAGService:
    def __init__(self, db: Session):
        self.db = db

    def chunk_text(self, text: str, chunk_size: int = 500) -> list[str]:
        # Very naive chunking for simplicity.
        # In production, use LangChain's RecursiveCharacterTextSplitter
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i+chunk_size]))
        return chunks

    def ingest_document(self, business_id: str, title: str, content: str, description: str = None) -> KnowledgeDocument:
        # Create doc record
        doc = KnowledgeDocument(
            business_id=business_id,
            title=title,
            description=description
        )
        self.db.add(doc)
        self.db.flush()

        chunks = self.chunk_text(content)
        
        # Create embeddings and chunk records
        embeddings = embedding_model.encode(chunks)
        
        for i, chunk_text in enumerate(chunks):
            chunk = KnowledgeChunk(
                document_id=doc.id,
                content=chunk_text,
                embedding=embeddings[i].tolist()
            )
            self.db.add(chunk)
            
        self.db.commit()
        return doc
