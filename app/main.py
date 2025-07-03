from fastapi import FastAPI
from app.api.v1.endpoint import chat

app = FastAPI(
    title="FastAPI Best Practices",
    openapi_tags=[
        {"name": "chat", "description": "chat room for web application"},
    ],
)
app.include_router(chat.router, prefix="/chat", tags=["chat"])