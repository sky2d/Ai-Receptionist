# AI Receptionist Platform

An AI Receptionist platform capable of handling customers through Phone calls, SMS, Website chat, and WhatsApp.

## Architecture Overview

The system uses a highly decoupled architecture based on:
- **Next.js** Frontend
- **FastAPI** Python Backend
- **PostgreSQL** Database (with pgvector for future RAG)

For detailed architectural principles, read [ARCHITECTURE.md](ARCHITECTURE.md).

## Technology Stack

- **Frontend:** Next.js, TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** Python, FastAPI, Pydantic, SQLAlchemy
- **Database:** PostgreSQL, pgvector
- **Infrastructure:** Docker, Docker Compose

## Repository Structure

```text
ai-receptionist/
├── apps/
│   ├── web/         # Next.js frontend
│   └── api/         # FastAPI backend
├── packages/        # Shared packages and config
├── docs/            # Project documentation
├── infrastructure/  # Docker and deployment config
```

## Local Development Setup

1. Copy `.env.example` to `.env` and configure your Supabase `DATABASE_URL` and other variables.

### Running the Backend (FastAPI)
1. Navigate to the API directory:
   ```bash
   cd apps/api
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Running the Frontend (Next.js)
1. Navigate to the Web directory:
   ```bash
   cd apps/web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Environment Variables

See `.env.example` for required environment variables.

## Docker Instructions

The provided `docker-compose.yml` spins up PostgreSQL, Redis, the FastAPI backend, and the Next.js frontend. It is meant for local development only.

## Development Roadmap

- [x] **Phase 1:** Project architecture
- [ ] **Phase 2:** Database + business model
- [ ] **Phase 3:** AI agent foundation
- [ ] **Phase 4:** Tool calling
- [ ] **Phase 5:** Google Calendar
- [ ] **Phase 6:** Web chat
- [ ] **Phase 7:** SMS
- [ ] **Phase 8:** Voice
- [ ] **Phase 9:** RAG / Knowledge Base
- [ ] **Phase 10:** Human handoff
- [ ] **Phase 11:** Analytics and monitoring
- [ ] **Phase 12:** Production hardening

## Future Integrations

- [ ] Twilio (Voice/SMS)
- [ ] Vapi / Realtime voice providers
- [ ] Google Calendar
- [ ] Microsoft Outlook Calendar
- [ ] OpenAI / Anthropic / Local models
