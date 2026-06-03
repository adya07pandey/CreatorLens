import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    token=HF_TOKEN
)


def get_embedding(text: str):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


def get_document_embedding(text: str):

    return get_embedding(text)


def get_query_embedding(query: str):

    return get_embedding(query)