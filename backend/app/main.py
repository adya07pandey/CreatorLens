import sys


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ingest import router as ingest_router
from app.api.chat_stream import router as chat_router
from app.api.chat_history import router as chat_history_router
from app.api.sessions import router as sessions_router
from app.api.pdf import router as pdf_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://creator-lens-seven.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(chat_history_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")
app.include_router(pdf_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "API is running"}  