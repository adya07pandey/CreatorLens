from qdrant_client.models import Filter
from qdrant_client.models import FieldCondition
from qdrant_client.models import MatchValue

from app.services.vectorstore.qdrant import (
    client,
    COLLECTION_NAME
)

from app.services.embeddings.embedder import (
    get_query_embedding
)

def retrieve_chunks(
    query,
    session_id,
    limit=5
):

    query_vector = get_query_embedding(
        query
    )

    if query_vector is None:

        print(
            "[RETRIEVAL] Embedding failed"
        )

        return []

    results = client.query_points(
        collection_name=COLLECTION_NAME,

        query=query_vector,

        query_filter=Filter(
            must=[
                FieldCondition(
                    key="session_id",
                    match=MatchValue(
                        value=session_id
                    )
                )
            ]
        ),

        limit=limit
    )
    
    return [
        hit.payload
        for hit in results.points
    ]
