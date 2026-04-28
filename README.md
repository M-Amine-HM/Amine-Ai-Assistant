# - AI Chatbot (React + FastAPI + Streamlit)

A modern AI chatbot experience powered by Groq + LangChain. The project includes:
- A React (Vite) frontend with a bold chat UI.
- A FastAPI backend that proxies requests to the Groq LLM.
- The original Streamlit app kept for reference or local demos.

## Project structure

- app.py - Streamlit UI (optional)
- api.py - FastAPI backend
- chatbot.py - Shared LangChain helpers
- web/ - React (Vite) frontend

## Requirements

- Python 3.9+
- Node.js 18+

## Environment variables

Create a .env file in the project root (see .env.example):

- GROQ_API_KEY
- GROQ_MODEL (optional)
- DEFAULT_SYSTEM_PROMPT (optional)
- DEFAULT_TEMPERATURE (optional)
- DEFAULT_MAX_TOKENS (optional)
- CORS_ORIGINS (optional)

Create a web/.env file for the frontend (see web/.env.example):

- VITE_API_URL (defaults to http://localhost:8000)

## Install and run

### Backend (FastAPI)

1) Install dependencies:

pip install -r requirements.txt

2) Start the API:

uvicorn api:app --reload --port 8000

### Frontend (React)

1) Install dependencies:

cd web
npm install

2) Start the dev server:

npm run dev

Open http://localhost:5173

## Optional: Streamlit UI

You can still run the Streamlit app:

streamlit run app.py

## Notes

- The backend uses Groq via LangChain.
- The frontend talks to the backend through VITE_API_URL.
- Keep secrets in .env and never commit them.
