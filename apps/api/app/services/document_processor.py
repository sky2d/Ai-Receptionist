import os
from pypdf import PdfReader
from sqlalchemy.orm import Session
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk
from sentence_transformers import SentenceTransformer

# Load the lightweight open-source embedding model (384 dimensions)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_file(file_path: str, filename: str) -> str:
    text = ""
    if filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file format. Use PDF or TXT.")
    return text

def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def process_and_store_document(db: Session, file_path: str, filename: str, business_id: str):
    # 1. Extract text
    text = extract_text_from_file(file_path, filename)
    if not text.strip():
        raise ValueError("No readable text found in file.")
        
    # 2. Chunk text
    chunks = split_text_into_chunks(text)
    
    # 3. Create Document Record
    doc = KnowledgeDocument(title=filename, business_id=business_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # 4. Generate Embeddings and Store Chunks
    # sentence-transformers returns a numpy array, we convert to list for pgvector
    embeddings = embedding_model.encode(chunks)
    
    knowledge_chunks = []
    for text_chunk, embedding in zip(chunks, embeddings):
        k_chunk = KnowledgeChunk(
            document_id=doc.id,
            content=text_chunk,
            embedding=embedding.tolist()
        )
        knowledge_chunks.append(k_chunk)
        
    db.add_all(knowledge_chunks)
    db.commit()
    return doc

def search_knowledge_base(db: Session, query: str, business_id: str, top_k: int = 3) -> list[str]:
    """
    Called by the AI Agent Tool to search the vector DB.
    """
    # 1. Embed the search query
    query_vector = embedding_model.encode(query).tolist()
    
    # 2. Perform Cosine Similarity Search using pgvector's cosine distance operator (<=>)
    results = db.query(KnowledgeChunk.content).join(KnowledgeDocument).filter(
        KnowledgeDocument.business_id == business_id
    ).order_by(
        KnowledgeChunk.embedding.cosine_distance(query_vector)
    ).limit(top_k).all()
    
    return [res[0] for res in results]
