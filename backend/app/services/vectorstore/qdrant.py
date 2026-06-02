from dotenv import load_dotenv
load_dotenv()
from qdrant_client import QdrantClient
import os
from qdrant_client.models import PointStruct
import uuid

from app.services.embeddings.embedder import (
    get_document_embedding
)
from qdrant_client.models import Filter
from qdrant_client.models import FieldCondition
from qdrant_client.models import MatchValue

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
print(client.get_collections())

COLLECTION_NAME = "video_chunks"
from qdrant_client.models import (
    VectorParams,
    Distance,
    PayloadSchemaType
)

def create_collection():

    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME in existing:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="session_id",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="video_label",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="platform",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="creator",
        field_schema=PayloadSchemaType.KEYWORD
    )
def store_chunks(
    chunks,
    session_id,
    video_label,
    creator,
    platform
):
    create_collection()
    points = []

    for chunk in chunks:

        vector = get_document_embedding(
            chunk["text"]
        )

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "session_id": session_id,
                    "video_label": video_label,
                    "creator": creator,
                    "platform": platform,
                    "text": chunk["text"],
                    "start_time": chunk["start_time"],
                    "end_time": chunk["end_time"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )



def delete_session_chunks(
    session_id
):

    client.delete(
        collection_name=COLLECTION_NAME,

        points_selector=Filter(
            must=[
                FieldCondition(
                    key="session_id",
                    match=MatchValue(
                        value=session_id
                    )
                )
            ]
        )
    )
