from typing import TypedDict

class GraphState(TypedDict, total=False):

    session_id: str

    query: str

    retrieved_chunks: list

    video_metadata: list

    insights: dict

    chat_history: list

    prompt: str

    sources: list