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

1. Copy `.env.example` to `.env` and fill in required variables.
2. Run Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Access the API at http://localhost:8000
4. Access the Web app at http://localhost:3000

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
