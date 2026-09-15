from sentence_transformers import SentenceTransformer
import traceback
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    res = embedding_model.encode(["hello world"])
    print("Encode success, shape:", res.shape)
except Exception as e:
    traceback.print_exc()
