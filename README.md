# 🚀 CreatorLens

> AI-powered video comparison platform that analyzes two YouTube Shorts or Instagram Reels and explains **why one performed better**.

CreatorLens combines transcript analysis, video metadata, vector search, and conversational RAG to generate creator-friendly insights instead of raw analytics.

---

##  Features

###  Video Comparison

- Compare two YouTube Shorts or Instagram Reels
- Generate AI-powered performance summaries
- Identify the stronger-performing video
- Explain why it likely outperformed the other

###  AI Insights

- Opening hook comparison
- Speaking pace analysis
- Content structure breakdown
- Audience appeal evaluation
- Actionable improvement suggestions

###  Conversational RAG Chat

- Ask follow-up questions about both videos
- Chat directly with video transcripts
- Session-aware conversations with memory
- Source citations with timestamps

###  Session Management

- Persistent chat history
- Session retrieval
- PDF export support
- Daily usage limits

---

##  Tech Stack

### Frontend

- React
- Vite
- CSS Modules

### Backend

- FastAPI
- LangGraph
- OpenRouter (Qwen 3 32B)

### Database

- PostgreSQL (Neon)

### Vector Database

- Qdrant Cloud

### Video Processing

- yt-dlp
- Apify
- Faster Whisper

### Deployment

- Vercel
- Render

---

##  System Architecture

```text
User URLs
    │
    ▼
Video Ingestion
    │
    ▼
Metadata Extraction
    │
    ▼
Transcript Extraction
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
Qdrant Storage
    │
    ▼
Summary Generation
    │
    ▼
RAG Chat
```

---

##  Workflow

### Video Ingestion Pipeline

1. User submits two video URLs
2. Metadata is extracted
3. Transcripts are collected
4. Transcript chunks are embedded
5. Chunks are stored in Qdrant
6. Comparison summary is generated
7. Session is saved to PostgreSQL

### Chat Workflow

1. User asks a question
2. Relevant transcript chunks are retrieved
3. Previous conversation history is loaded
4. Context is assembled
5. Qwen generates a response
6. Sources are returned with timestamps

---

##  API Endpoints

### Compare Videos

```http
POST /api/ingest
```

Compare two videos and create a new analysis session.

---

### Streaming Chat

```http
POST /api/chat/stream
```

Stream AI responses token-by-token.

---

### Session History

```http
GET /api/{session_id}
```

Retrieve all session messages.

---

### User Sessions

```http
GET /api/sessions
```

List all available user sessions.

---

### PDF Export

```http
GET /api/pdf/{session_id}
```

Export session summary as a PDF document.

---

##  Performance Benchmarks

### YouTube Shorts

| Stage | Time |
|---------|---------|
| Metadata + Transcript Extraction | ~3.5–5.2s/video |
| Video Processing | ~3.7–5.3s |
| Qwen Summary Generation | ~14s |
| PostgreSQL Save | ~0.6–0.9s |
| Qdrant Storage | ~2.8–23s |
| Total Ingestion Time | ~22–46s |

**Observed Runs**

- 22.15s total ingestion (youtube shorts)
- 46.33s total ingestion (youtube 30min videos)

---

### Instagram Reels

| Stage | Time |
|---------|---------|
| Apify Reel Scraper | 32.40s |
| Follower Scraper | 17.22s |
| Video Processing | 49.64s |
| Qwen Summary Generation | 8.24s |
| PostgreSQL Save | 0.71s |
| Qdrant Storage | 2.96s |
| Total Ingestion Time | 62.78s |

> Instagram ingestion is slower because metadata extraction, transcript generation, and creator statistics require multiple external services.

---

##  Local Setup

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

##  Environment Variables

### Backend

```env
DATABASE_URL=

OPENROUTER_API_KEY=

QDRANT_URL=
QDRANT_API_KEY=

APIFY_TOKEN=

HF_TOKEN=
```

### Frontend

```env
VITE_API_URL=
```

---

##  Future Improvements

- Multi-video comparison
- Viral pattern detection
- Creator benchmarking
- Trend discovery
- Team workspaces
- Analytics dashboard
- Batch processing

---
