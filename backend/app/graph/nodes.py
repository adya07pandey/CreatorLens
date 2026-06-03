from app.services.retrieval.retriever import retrieve_chunks
from app.services.retrieval.context_builder import build_context

from app.services.llm.qwen import call_qwen
from app.services.llm.prompts import build_rag_prompt

from app.db.database import SessionLocal
from app.db.crud import get_session_videos
from app.db.crud import (
    get_session_videos,
    get_session_insight,
    get_session_messages
)
import time


def retrieve_node(state):

    start = time.perf_counter()

    
    try:

        chunks = retrieve_chunks(
            query=state["query"],
            session_id=state["session_id"]
        )

    except Exception as e:

        print(
            f"[RETRIEVE ERROR] {e}"
        )

        chunks = []
    print(
        f"[LATENCY] Qdrant retrieval: "
        f"{time.perf_counter()-start:.3f}s"
    )

    db = SessionLocal()

    try:

        start = time.perf_counter()

        videos = get_session_videos(
            db,
            state["session_id"]
        )

        print(
            f"[LATENCY] Get videos: "
            f"{time.perf_counter()-start:.3f}s"
        )

        start = time.perf_counter()

        insight = get_session_insight(
            db,
            state["session_id"]
        )

        print(
            f"[LATENCY] Get insights: "
            f"{time.perf_counter()-start:.3f}s"
        )

        start = time.perf_counter()

        messages = get_session_messages(
            db,
            state["session_id"]
        )

        print(
            f"[LATENCY] Get messages: "
            f"{time.perf_counter()-start:.3f}s"
        )

    finally:

        db.close()

    history = []

    for msg in messages[-6:]:

        history.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )

    return {
        "retrieved_chunks": chunks,
        "video_metadata": videos,
        "insights": insight,
        "chat_history": history
    }

def answer_node(state):

    start = time.perf_counter()

    context = build_context(
        chunks=state["retrieved_chunks"],
        videos=state["video_metadata"],
        insight=state["insights"]
    )

    print(
        f"[LATENCY] Build context: "
        f"{time.perf_counter()-start:.3f}s"
    )

    history_text = ""

    for msg in state["chat_history"]:

        history_text += (
            f"{msg['role'].upper()}: "
            f"{msg['content']}\n"
        )

    start = time.perf_counter()

    prompt = build_rag_prompt(
        query=state["query"],
        context=context,
        history=history_text
    )

    print(
        f"[LATENCY] Build prompt: "
        f"{time.perf_counter()-start:.3f}s"
    )

    sources = []
    seen = set()

    for chunk in state["retrieved_chunks"]:

        key = (
            chunk["video_label"],
            chunk["start_time"],
            chunk["end_time"]
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "video": chunk["video_label"],
                "platform": chunk.get("platform"),
                "creator": chunk.get("creator"),
                "start": chunk["start_time"],
                "end": chunk["end_time"],
                "text": chunk.get("text", "")
            }
        )
    return {
        "prompt": prompt,
        "sources": sources
    }


    context = build_context(
        chunks=state["retrieved_chunks"],
        videos=state["video_metadata"],
        insight=state["insights"]
    )

    history_text = ""

    for msg in state["chat_history"]:

        history_text += (
            f"{msg['role'].upper()}: "
            f"{msg['content']}\n"
        )

    prompt = build_rag_prompt(
        query=state["query"],
        context=context,
        history=history_text
    )

    sources = []
    seen = set()

    for chunk in state["retrieved_chunks"]:

        key = (
            chunk["video_label"],
            chunk["start_time"],
            chunk["end_time"]
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "video": chunk["video_label"],
                "platform": chunk.get("platform"),
                "creator": chunk.get("creator"),
                "start": chunk["start_time"],
                "end": chunk["end_time"],
                "text": chunk.get("text", "")
            }
        )

    return {
        "prompt": prompt,
        "sources": sources
    }