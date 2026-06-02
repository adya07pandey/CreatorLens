import os
import requests

JINA_API_KEY = os.getenv(
    "JINA_API_KEY"
)

def get_embedding(text):

    response = requests.post(
        "https://api.jina.ai/v1/embeddings",

        headers={
            "Authorization":
                f"Bearer {JINA_API_KEY}",
            "Content-Type":
                "application/json"
        },

        json={
            "model":
                "jina-embeddings-v3",

            "input":
                [text]
        }
    )

    response.raise_for_status()

    return (
        response.json()
        ["data"][0]
        ["embedding"]
    )


def get_document_embedding(text):
    return get_embedding(text)


def get_query_embedding(query):
    return get_embedding(
        f"Represent this sentence for searching relevant passages: {query}"
    )

