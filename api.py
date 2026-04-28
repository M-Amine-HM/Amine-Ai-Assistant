import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

from chatbot import build_messages

load_dotenv()


def get_env_float(name: str, fallback: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return fallback
    try:
        return float(raw)
    except ValueError:
        return fallback


def get_env_int(name: str, fallback: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "DEFAULT_SYSTEM_PROMPT",
    "You are a helpful AI assistant. Answer clearly and concisely.",
)
DEFAULT_TEMPERATURE = get_env_float("DEFAULT_TEMPERATURE", 0.7)
DEFAULT_MAX_TOKENS = get_env_int("DEFAULT_MAX_TOKENS", 1024)
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app = FastAPI(title="AI Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    temperature: float = Field(DEFAULT_TEMPERATURE, ge=0.0, le=2.0)
    max_tokens: int = Field(DEFAULT_MAX_TOKENS, ge=50, le=4096)


class ChatResponse(BaseModel):
    answer: str


def create_llm(temperature: float, max_tokens: int) -> ChatGroq:
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=os.getenv("GROQ_API_KEY"),
    )


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        llm = create_llm(request.temperature, request.max_tokens)
        messages = build_messages(
            [m.model_dump() for m in request.messages],
            request.system_prompt,
        )
        response = llm.invoke(messages)
        return ChatResponse(answer=response.content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
