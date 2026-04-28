import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# ── LLM client ────────────────────────────────────────────────
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=float(os.getenv("DEFAULT_TEMPERATURE", "0.7")),
    max_tokens=int(os.getenv("DEFAULT_MAX_TOKENS", "1024")),
    api_key=os.getenv("GROQ_API_KEY")
)


def build_messages(history: list, system_prompt: str) -> list:
    """
    Convert Streamlit session history to LangChain message objects.
    history = [{"role": "user"|"assistant", "content": "..."}]
    """
    messages = [SystemMessage(content=system_prompt)]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages


def get_response(history: list, system_prompt: str) -> str:
    """Send conversation history to Groq and return the answer."""
    messages = build_messages(history, system_prompt)
    response = llm.invoke(messages)
    return response.content
