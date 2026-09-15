# AI Receptionist

An advanced, AI-powered voice receptionist system capable of answering phone calls, handling natural conversations, retrieving information from custom documents, and taking smart actions like booking appointments.

## 🌟 Key Features
- **Real-Time Voice Calling:** Seamless integration with Twilio to handle live inbound and outbound phone calls.
- **Lightning-Fast STT (Speech-to-Text):** Uses Deepgram for real-time, highly accurate voice transcription with minimal latency.
- **Intelligent Conversational Agent:** Powered by OpenAI's LLMs for natural language understanding, context retention, and dynamic response generation.
- **Human-Like TTS (Text-to-Speech):** Utilizes Edge TTS for generating fluid, natural, and highly responsive voice replies.
- **Knowledge Base & RAG:** Integrates `pgvector` and `sentence-transformers` for embedding and retrieving knowledge from uploaded documents (PDFs), allowing the AI to answer specific business questions.
- **Smart Actions & Tool Calling:** The AI can execute dynamic functions during the call, such as checking calendar availability and booking appointments.
- **Interactive Dashboard:** A comprehensive Next.js web interface to manage AI settings, upload knowledge documents, view call logs, and analyze performance metrics.
- **Barge-In Support:** Users can interrupt the AI while it's speaking, creating a natural, human-like conversational flow.

## 🛠️ Tech Stack & Services

### Backend (`apps/api`)
- **Framework:** FastAPI (Python) - High performance, asynchronous API.
- **Database:** Supabase (PostgreSQL) - Managed database for relational data.
- **Vector Database:** `pgvector` extension in PostgreSQL for storing document embeddings.
- **Caching & Message Queue:** Redis - For high-speed data caching and background task management.
- **ORM & Migrations:** SQLAlchemy and Alembic.

### AI & Third-Party Services
- **Voice / Telephony:** Twilio
- **Speech-to-Text (STT):** Deepgram SDK
- **Text-to-Speech (TTS):** Edge TTS
- **LLM / Intelligence:** OpenAI (GPT Models)
- **Embeddings:** `sentence-transformers`
- **Document Processing:** PyPDF (for parsing knowledge base files)

### Frontend (`apps/web`)
- **Framework:** Next.js (React) - Built for speed, SEO, and server-side rendering.
- **Styling:** Tailwind CSS - Utility-first styling for a beautiful, responsive dashboard UI.

## 📁 Project Structure
```text
├── apps/
│   ├── api/          # FastAPI backend microservice (Python)
│   └── web/          # Next.js frontend dashboard (React)
├── .github/          # CI/CD workflows and actions
└── ...
```

## 🚀 Getting Started
1. Clone the repository.
2. Configure `.env` variables using `.env.example` as a template (requires keys for Twilio, Deepgram, OpenAI, and Supabase).
3. Start the backend with FastAPI / Uvicorn.
4. Start the frontend with Next.js development server.
