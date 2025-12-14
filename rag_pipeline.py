import faiss
import pickle
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load embeddings model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("vector_store/index.faiss")

# Load documents
with open("vector_store/index.pkl", "rb") as f:
    documents = pickle.load(f)

def retrieve_context(query, k=2):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, k)
    return "\n".join([documents[i] for i in indices[0]])

def generate_answer(query):
    context = retrieve_context(query)

    prompt = f"""
You are an AI assistant. Answer based ONLY on the context.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

