import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_URL = (
    "https://router.huggingface.co/"
    "hf-inference/models/"
    "BAAI/bge-small-en-v1.5/"
    "pipeline/feature-extraction"
)


def get_embedding(text):

    response = requests.post(
        MODEL_URL,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "inputs": text
        },
        timeout=60
    )

    response.raise_for_status()

    embedding = response.json()

    if isinstance(embedding[0], list):
        embedding = embedding[0]

    return embedding



def get_document_embedding(text):
    return get_embedding(text)


def get_query_embedding(query):
    return get_embedding(
        f"Represent this sentence for searching relevant passages: {query}"
    )