import os

from dotenv import load_dotenv
import voyageai

load_dotenv()

client = voyageai.Client(
    api_key=os.getenv("VOYAGE_API_KEY")
)


def get_embedding(text: str):

    result = client.embed(
        [text],
        model="voyage-3-lite"
    )

    return result.embeddings[0]


def get_document_embedding(text: str):

    return get_embedding(text)


def get_query_embedding(query: str):

    return get_embedding(query)