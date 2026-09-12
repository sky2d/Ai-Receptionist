# Project Implementation Roadmap

This file tracks the implementation progress of the AI Receptionist platform.

## Phase 1: Project architecture
- [x] Initialize the monorepo structure.
- [x] Create root configuration files (`package.json`, `.env.example`, `docker-compose.yml`).
- [x] Document the architectural guidelines (`ARCHITECTURE.md`, `AGENT.md`).
- [x] Scaffold the backend (FastAPI) and frontend (Next.js) directories and placeholder files.

## Phase 2: Database + business model
- [x] Set up SQLAlchemy models (`User`, `Business`, `Service`, `Customer`, `Conversation`, `Message`, `Appointment`).
- [x] Configure Alembic for database migrations.
- [x] Establish multitenancy boundaries using `business_id`.

## Phase 3: AI agent foundation
- [x] Implement the core `AgentInterface` and the internal memory schema.
- [x] Integrate a base LLM provider (e.g., OpenAI/Anthropic) behind the abstraction layer (Skeleton manager created).
- [ ] Develop the Conversation Engine to handle message routing.

## Phase 4: Tool calling
- [x] Implement the Tool Registry.
- [x] Build core domain services (e.g., `AppointmentService`, `CustomerService`).
- [x] Map LLM function calls to tool execution logic.

## Phase 5: Frontend Dashboard Foundation
- [x] Set up Next.js app routing for the admin dashboard.
- [x] Implement core layout, navigation, and tenant selection UI.
- [x] Create shared components with shadcn/ui.

## Phase 6: Google Calendar
- [x] Implement the generic `CalendarProvider` interface.
- [x] Build the `GoogleCalendarAdapter` integration.
- [x] Enable the agent to check availability, book, and cancel appointments.

## Phase 7: Web chat
- [x] Build the Next.js chat interface for website embedding.
- [x] Implement the `WebChatChannel` adapter on the backend.
- [x] Set up real-time bidirectional communication (WebSockets).

## Phase 8: SMS
- [x] Implement the `SMSChannel` adapter.
- [x] Integrate with an SMS provider (e.g., Twilio) via webhooks.
- [x] Normalize incoming SMS payloads into the `NormalizedMessage` format.

## Phase 9: Voice
- [ ] Implement the Voice Gateway and Voice Provider integrations.
- [ ] Integrate Speech-to-Text (STT) and Text-to-Speech (TTS) logic.
- [ ] Ensure low latency in voice streaming to the Conversation Engine.

## Phase 10: RAG / Knowledge Base
- [ ] Set up `pgvector` for embedding storage.
- [ ] Implement a document ingestion and chunking pipeline.
- [ ] Provide the agent with a `SearchKnowledgeBase` tool.

## Phase 11: Human handoff
- [ ] Implement escalation rules.
- [ ] Create a portal view for human agents to intercept live conversations.
- [ ] Pause the AI agent during human intervention.

## Phase 12: Analytics and monitoring
- [ ] Track conversation logs, AI token usage, and latency metrics.
- [ ] Build out a frontend dashboard to visualize business performance and AI statistics.
- [ ] Instrument tool execution logs for error tracking.

## Phase 13: Production hardening
- [ ] Establish rate-limiting, strict input validation, and secure secrets management.
- [ ] Set up continuous integration and deployment pipelines.
- [ ] Provision production infrastructure (Vercel, containerized backend, managed Postgres).
