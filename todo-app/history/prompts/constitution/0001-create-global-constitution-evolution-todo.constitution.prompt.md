---
id: 0001
title: Create Global Constitution Evolution Todo
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 005-persistence
user: sarosh
command: /sp.constitution
labels: ["constitution", "governance", "sdd", "phase-management", "global-principles"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/0001-create-global-constitution-evolution-todo.constitution.prompt.md
tests:
  - N/A (constitutional document)
---

## Prompt

/sp.constitution Create a single global constitution for the entire "Evolution of Todo" project
covering Phase I through Phase V.

This constitution must define:

1. Spec-Driven Development as mandatory
   - No agent may write code without approved specs and tasks
   - All work must follow: Constitution → Specs → Plan → Tasks → Implement

2. Agent Behavior Rules
   - No manual coding by humans
   - No feature invention
   - No deviation from approved specifications
   - Refinement must occur at spec level, not code level

3. Phase Governance
   - Each phase is strictly scoped by its specification
   - Future-phase features must never leak into earlier phases
   - Architecture may evolve only through updated specs and plans

4. Technology Constraints
   - Python for backend
   - Next.js for frontend (later phases)
   - FastAPI, SQLModel, Neon DB
   - OpenAI Agents SDK, MCP
   - Docker, Kubernetes, Kafka, Dapr (later phases)

5. Quality Principles
   - Clean architecture
   - Stateless services where required
   - Clear separation of concerns
   - Cloud-native readiness

This constitution must remain stable across all phases
and act as the supreme governing document for all agents.

## Response snapshot

Created comprehensive global constitution at `.specify/memory/constitution.md` (v1.0.0).

**Key Sections Implemented**:

I. **Spec-Driven Development Mandate**
   - Mandatory workflow: Constitution → Spec → Plan → Tasks → Implementation
   - No code without approved specs and tasks
   - PHR creation requirements and routing rules
   - Documentation requirements for every feature

II. **Agent Behavior Rules**
   - Clear boundaries for agent autonomy
   - Human-as-tool strategy for ambiguity resolution
   - Strict prohibition on feature invention and scope expansion
   - ADR suggestion protocol (never auto-create)

III. **Phase Governance**
   - Phase isolation and boundaries
   - Detailed definitions for Phases I-V
   - Phase progression requirements
   - Prevention of future-phase feature leakage

IV. **Technology Constraints**
   - Complete technology stack defined (backend, frontend, infrastructure, AI/agents)
   - Technology principles (simplicity first, no premature optimization)
   - Technology evolution requirements (spec amendments, ADRs)

V. **Quality Principles**
   - Clean architecture (layered structure, SOLID principles)
   - Testing standards (80% coverage, TDD, test organization)
   - Code quality standards (style, review, documentation)
   - Performance standards per phase
   - Security standards per phase
   - Cloud-native readiness requirements

VI. **Development Workflow**
   - Git workflow (branching, commits, PRs)
   - CI/CD requirements
   - Deployment strategy per phase

VII. **Architecture Decision Records**
   - ADR significance test (3 criteria)
   - ADR process and suggestion format
   - ADR content requirements

VIII. **Governance and Amendments**
   - Constitutional authority and supremacy
   - Amendment process and categories
   - Compliance verification and enforcement

IX. **Principles Summary**
   - Core values (8 principles)
   - Anti-patterns (10 forbidden practices)

X. **Version History & Appendices**
   - Version tracking and amendment log
   - Quick reference guide
   - Phase checklist and quality gates

## Outcome

- ✅ Impact: Established supreme governing document for all phases; all future work must comply with these principles
- 🧪 Tests: N/A (constitutional document, not code)
- 📁 Files: Created constitution.md (548 lines), created PHR 0001
- 🔁 Next prompts: Begin Phase II specification using `/sp.specify` or amend constitution if adjustments needed
- 🧠 Reflection: Constitution provides clear governance, prevents scope creep, enforces SDD workflow, and maintains phase discipline. All architectural decisions now require explicit justification against these principles.

## Evaluation notes (flywheel)

- Failure modes observed: None (initial creation)
- Graders run and results (PASS/FAIL): N/A (constitutional document)
- Prompt variant (if applicable): N/A (initial version)
- Next experiment (smallest change to try): Monitor compliance during Phase II work; adjust if principles too rigid or too permissive
