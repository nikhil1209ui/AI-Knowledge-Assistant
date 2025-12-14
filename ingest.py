import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read data
with open("data/docs/sample.txt", "r", encoding="utf-8") as f:
    documents = f.readlines()

# Create embeddings
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index
os.makedirs("vector_store", exist_ok=True)
faiss.write_index(index, "vector_store/index.faiss")

# Save documents
with open("vector_store/index.pkl", "wb") as f:
    pickle.dump(documents, f)

print("✅ Ingestion complete. Vector store created.")
