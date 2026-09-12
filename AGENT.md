# AI Agent Coding Rules

This document provides guidelines for future AI coding agents working in this repository.

## Project Rules

1. **Never mix frontend and backend responsibilities.**
2. **Never put business logic in route handlers.**
3. **Never allow the LLM to directly call external APIs.**
4. **Always use tools for external actions.**
5. **Always use service layers.**
6. **Always use integration adapters.**
7. **Never expose secrets.**
8. **Never bypass tenant isolation.**
9. **Never hardcode provider-specific logic into domain logic.**

## AI Agent Rules

1. Read `ARCHITECTURE.md` before making architectural changes.
2. Read `AGENT.md` before implementing features.
3. Follow existing abstractions.
4. Avoid unnecessary dependencies.
5. Avoid rewriting existing architecture without justification.
6. Keep provider-specific code inside integration adapters.
7. Keep AI provider logic behind an LLM interface.
8. Keep calendar providers behind a Calendar interface.
9. Keep communication channels behind channel interfaces.
10. Write tests for business logic.
11. Validate all external inputs.
12. Never expose API keys.
13. Never commit `.env`.
14. Never silently change database schemas.
15. Explain architectural changes before making major changes.

## Implementation Workflow

Future coding agents should follow this standard implementation workflow:

```text
Understand requirement
        ↓
Read architecture
        ↓
Identify affected domain
        ↓
Define/update interfaces
        ↓
Implement domain logic
        ↓
Implement provider adapter
        ↓
Add API layer
        ↓
Add tests
        ↓
Update documentation
```
