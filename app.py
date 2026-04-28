
import os
import streamlit as st
from chatbot import get_response, llm


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


# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Chatbot — Groq + LangChain",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Powered by **Llama 3.3 70B** via Groq + LangChain")

# ── Sidebar settings ──────────────────────────────────────────
with st.sidebar:
    st.header("Settings")

    system_prompt = st.text_area(
        "System prompt",
        value=os.getenv(
            "DEFAULT_SYSTEM_PROMPT",
            "You are a helpful AI assistant. Answer clearly and concisely.",
        ),
        height=120,
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        2.0,
        get_env_float("DEFAULT_TEMPERATURE", 0.7),
        step=0.1,
    )
    max_tokens = st.slider(
        "Max tokens",
        50,
        2048,
        get_env_int("DEFAULT_MAX_TOKENS", 1024),
        step=50,
    )

    # Update LLM settings live
    llm.temperature = temperature
    llm.max_tokens = max_tokens

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Model: llama-3.3-70b-versatile")
    st.caption("Provider: Groq cloud")

# ── Session state — conversation history ─────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Display conversation history ──────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Chat input ────────────────────────────────────────────────
if user_input := st.chat_input("Type your message..."):

    # Show and save user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Call Groq via LangChain
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_response(
                    st.session_state.messages,
                    system_prompt
                )
                st.write(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")
