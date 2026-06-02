from pydantic import BaseModel


class IngestRequest(BaseModel):

    user_id: str
    url_a: str
    url_b: str


class ChatRequest(BaseModel):

    user_id: str
    session_id: str
    message: str