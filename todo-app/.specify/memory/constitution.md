<!--
SYNC IMPACT REPORT
Generated: 2026-01-01
Version Change: 1.0.0 → 2.0.0 (MAJOR)

MODIFIED PRINCIPLES:
- Section 3.2 Phase Definitions:
  • Phase II: "Persistence & State" → "Full-Stack Web Application" (expanded scope)
  • Phase III: "API & Multi-User" → "Real-Time & Advanced Features" (scope shifted)
  • Phase IV: "Web UI & Real-Time" → "Cloud-Native & Scale" (scope shifted)
  • Phase V: "Cloud-Native & Scale" → "AI Agents & Advanced Orchestration" (new focus)

- Section 4.1 Core Technology Stack: Completely restructured to phase-specific breakdown
  • Phase I: Clarified as CLI-only with in-memory storage
  • Phase II: Added REST API, Next.js, Better Auth, Neon PostgreSQL
  • Phase III+: Real-time capabilities (WebSockets/SSE)
  • Phase IV: Cloud-native infrastructure
  • Phase V: AI/Agent frameworks

- Section 5.2 Testing Standards: Updated integration/E2E test requirements to Phase II+
- Section 5.4 Performance Standards: Reorganized by phase with Phase II including API and UI metrics
- Section 5.5 Security Standards: Consolidated web security into Phase II+
- Section 6.3 Deployment Strategy: Added Phase II web deployment requirements

ADDED SECTIONS:
- None (no new principle sections)

REMOVED SECTIONS:
- None

TEMPLATES REQUIRING UPDATES:
⚠ PENDING: .specify/templates/plan-template.md (verify Phase II technology alignment)
⚠ PENDING: .specify/templates/spec-template.md (verify scope constraints match new phases)
⚠ PENDING: .specify/templates/tasks-template.md (verify task categories for web development)

FOLLOW-UP TODOS:
1. Verify plan-template.md references correct Phase II technologies
2. Update any existing Phase II specifications to align with expanded scope
3. Review command files for phase-specific guidance accuracy
4. Consider creating ADR for this major architectural shift

RATIONALE FOR MAJOR VERSION BUMP:
This is a backward-incompatible change that fundamentally alters Phase II scope and complexity.
Projects mid-Phase II development would need significant replanning. Phase boundaries have been
materially redefined, affecting project planning and estimation across all phases.
-->

# Evolution of Todo: Global Constitution

## Preamble

This constitution governs the entire "Evolution of Todo" project across all phases (Phase I through Phase V). It establishes immutable principles, mandatory workflows, technology constraints, and quality standards that all agents, developers, and stakeholders must follow without exception.

**Supremacy Clause**: This constitution is the supreme governing document for the project. No specification, plan, task, or code may violate these principles. Any conflict must be resolved by amending this constitution first.

---

## I. Spec-Driven Development (SDD) Mandate

### 1.1 Mandatory Workflow

All development work MUST follow this exact sequence:

1. **Constitution** → Define or amend principles (requires explicit approval)
2. **Specification** → Define requirements and success criteria (requires approval)
3. **Plan** → Design architecture and approach (requires approval)
4. **Tasks** → Break down into testable units (requires approval)
5. **Implementation** → Execute approved tasks only

**Non-Negotiable Rules**:
- No agent may write code without approved specifications and tasks
- No manual coding by humans (agents execute all implementations)
- No feature invention or scope expansion beyond approved specs
- All refinements occur at spec level, never at code level
- Each step requires explicit user approval before proceeding

### 1.2 Documentation Requirements

Every feature must produce:
- `specs/<feature-name>/spec.md` - Requirements and acceptance criteria
- `specs/<feature-name>/plan.md` - Architecture decisions and design
- `specs/<feature-name>/tasks.md` - Testable implementation tasks
- `history/prompts/<feature-name>/` - Prompt History Records (PHRs)
- `history/adr/<decision-name>.md` - Architecture Decision Records (as needed)

### 1.3 Prompt History Records (PHR)

**Mandatory PHR Creation**:
- Every user interaction must generate a PHR
- PHRs must be created after completing requests
- PHRs capture verbatim user input and agent response
- No truncation or summarization of user prompts

**PHR Routing**:
- Constitution changes → `history/prompts/constitution/`
- Feature work (spec, plan, tasks, implementation) → `history/prompts/<feature-name>/`
- General queries → `history/prompts/general/`

**PHR Content Requirements**:
- Complete user prompt text (verbatim)
- Representative agent response
- Files created/modified
- Tests run/added
- Outcome and evaluation

---

## II. Agent Behavior Rules

### 2.1 Autonomy Boundaries

**Agents MUST**:
- Follow approved specifications exactly
- Execute only approved tasks
- Ask clarifying questions when ambiguous
- Report completion status and blockers
- Create PHRs for all interactions
- Suggest ADRs for significant decisions (never auto-create)

**Agents MUST NEVER**:
- Invent features not in specifications
- Deviate from approved technical approaches
- Make architectural decisions without user approval
- Skip testing requirements
- Modify code outside current task scope
- Auto-create Architecture Decision Records

### 2.2 Human-as-Tool Strategy

Agents must invoke the user for:
1. **Ambiguous Requirements** - Ask 2-3 targeted clarifying questions
2. **Unforeseen Dependencies** - Surface and ask for prioritization
3. **Architectural Uncertainty** - Present options with tradeoffs
4. **Completion Checkpoints** - Summarize work and confirm next steps

### 2.3 No Manual Coding by Humans

- All code implementation is performed by agents
- Humans provide specifications, approval, and guidance
- Humans may review and request changes via specs
- Humans do not write production code directly

---

## III. Phase Governance

### 3.1 Phase Isolation

**Strict Phase Boundaries**:
- Each phase is scoped by its approved specification
- Future-phase features MUST NOT leak into earlier phases
- Phase N+1 features are out-of-scope for Phase N
- Architecture evolves only through updated specs and plans

**Phase Progression**:
- Phase completion requires all tasks marked done
- Phase transition requires new constitution amendment (if needed)
- New phase begins with new specification
- Previous phase artifacts remain immutable (archive only)

### 3.2 Phase Definitions

**Phase I: Core CLI Foundation**
- In-memory todo CRUD operations
- Interactive CLI menu
- Pure Python implementation
- No persistence, no API, no UI

**Phase II: Full-Stack Web Application**
- Python REST API backend
- Database persistence (Neon Serverless PostgreSQL)
- SQLModel ORM integration
- Next.js frontend (React, TypeScript)
- Better Auth authentication (signup/signin)
- Full-stack web application architecture
- Data migration support

**Phase III: Real-Time & Advanced Features**
- Real-time updates (WebSockets/SSE)
- Advanced API features
- Enhanced user management
- Performance optimization

**Phase IV: Cloud-Native & Scale**
- Docker containerization
- Kubernetes orchestration
- Event-driven architecture (Kafka)
- Distributed tracing & observability
- Dapr integration

**Phase V: AI Agents & Advanced Orchestration**
- OpenAI Agents SDK integration
- Model Context Protocol (MCP)
- Advanced AI-driven features
- Multi-agent orchestration
- Intelligent automation

---

## IV. Technology Constraints

### 4.1 Core Technology Stack

**Phase I (CLI Only)**:
- Language: Python 3.11+
- Storage: In-memory (no persistence)
- Testing: pytest, pytest-cov

**Phase II (Full-Stack Web)**:
- Backend: Python 3.11+ REST API
- Framework: FastAPI or Flask
- ORM: SQLModel or equivalent
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (signup/signin)
- Frontend: Next.js (React, TypeScript)
- Styling: Tailwind CSS or CSS Modules
- State Management: React Context or Zustand
- Testing: pytest, pytest-cov, Jest/Vitest

**Phase III+ (Real-Time & Advanced)**:
- WebSockets/Server-Sent Events
- Advanced caching strategies
- Performance optimization tools

**Phase IV (Cloud-Native)**:
- Containerization: Docker
- Orchestration: Kubernetes
- Messaging: Apache Kafka
- Service Mesh: Dapr
- Observability: OpenTelemetry, Prometheus, Grafana

**Phase V (AI/Agents)**:
- OpenAI Agents SDK
- Model Context Protocol (MCP)
- Advanced AI frameworks

### 4.2 Technology Principles

- **Simplicity First**: Choose simplest solution for current phase
- **No Premature Optimization**: Optimize only when phase requires it
- **Standard Libraries**: Prefer standard/widely-adopted libraries
- **No Vendor Lock-in**: Maintain portability where feasible
- **Security by Default**: Follow security best practices from Phase I

### 4.3 Technology Evolution

- Technology changes require specification amendment
- Breaking technology changes require ADR
- Legacy technology must be migrated, not accumulated
- All technology choices must be justified in plan.md

---

## V. Quality Principles

### 5.1 Clean Architecture

**Layered Structure**:
- Presentation Layer (CLI, API, UI)
- Business Logic Layer (Services)
- Data Access Layer (Models, Repositories)
- Clear separation of concerns
- Dependency inversion (depend on abstractions)

**Code Organization**:
- Modular design with clear boundaries
- Single Responsibility Principle
- Interface segregation
- Composition over inheritance

### 5.2 Testing Standards

**Test Coverage Requirements**:
- Minimum 80% code coverage
- 100% coverage for business logic
- Unit tests for all services
- Integration tests for APIs (Phase II+)
- End-to-end tests for critical paths (Phase II+)
- Frontend component tests (Phase II+)

**Test-First Development**:
- Write tests before implementation (TDD)
- Tests define acceptance criteria
- Red-Green-Refactor cycle
- No untested code in production

**Test Organization**:
- `tests/` directory mirrors `src/` structure
- Test files named `test_<module>.py`
- Use fixtures for common setup
- Mock external dependencies

### 5.3 Code Quality Standards

**Code Style**:
- Follow PEP 8 (Python) and Airbnb style (JavaScript/TypeScript)
- Use type hints (Python) and TypeScript strict mode
- Meaningful variable and function names
- Self-documenting code (comments for "why", not "what")

**Code Review**:
- All code changes reviewed before merge
- Automated linting and formatting (black, ruff, eslint, prettier)
- Security scanning (bandit, safety)
- Dependency vulnerability checks

**Documentation**:
- Docstrings for all public functions/classes (Google style)
- README.md at project and feature level
- API documentation (OpenAPI/Swagger)
- Architecture diagrams for complex features

### 5.4 Performance Standards

**Phase I (CLI)**:
- CLI response time < 100ms for CRUD operations
- Startup time < 1 second

**Phase II (Full-Stack Web)**:
- API response time p95 < 200ms
- Throughput > 100 req/s for CRUD endpoints
- Time to Interactive < 3 seconds
- Lighthouse score > 90
- Database query optimization

**Phase III (Real-Time)**:
- WebSocket latency < 50ms
- SSE delivery < 100ms
- Concurrent connections > 1000

**Phase IV (Cloud-Native)**:
- Horizontal scaling to 10x load
- Zero-downtime deployments
- Fault tolerance and graceful degradation
- Auto-scaling based on load

### 5.5 Security Standards

**Phase I (CLI)**:
- No hardcoded secrets or credentials
- Use environment variables for configuration
- Input validation on all external data
- Error messages do not leak sensitive information

**Phase II+ (Web Application)**:
- SQL injection prevention (parameterized queries)
- Database connection encryption (TLS)
- Authentication and authorization (Better Auth, JWT)
- HTTPS only (TLS 1.2+)
- CORS configuration
- Rate limiting
- XSS prevention
- CSRF protection
- Content Security Policy
- Secure session management

**Phase III+**:
- Advanced threat detection
- Security monitoring and alerting

**Phase IV+ (Cloud-Native)**:
- Secret management (Vault, K8s secrets)
- Network policies and service mesh
- Regular security audits
- Compliance scanning

### 5.6 Cloud-Native Readiness

**Stateless Services**:
- No local state storage (use database or cache)
- Session data in distributed cache (Redis)
- Idempotent operations

**Observability**:
- Structured logging (JSON format)
- Distributed tracing (OpenTelemetry)
- Metrics collection (Prometheus)
- Health checks and readiness probes

**Resilience**:
- Graceful degradation
- Circuit breakers
- Retry with exponential backoff
- Timeout configuration

---

## VI. Development Workflow

### 6.1 Git Workflow

**Branch Strategy**:
- `main` - production-ready code
- `<phase-name>` - phase development branch (e.g., `001-core-cli`, `002-persistence`)
- Feature branches named: `<phase>-<feature-slug>`

**Commit Standards**:
- Conventional commits format
- Atomic commits (one logical change)
- Descriptive commit messages
- Sign-off required

**Pull Requests**:
- PR per feature or task group
- PR description references spec and tasks
- All tests pass before merge
- Code review approval required

### 6.2 Continuous Integration

**Automated Checks**:
- Linting and formatting
- Unit tests
- Integration tests (Phase III+)
- Code coverage
- Security scanning

**Quality Gates**:
- All tests pass
- Coverage threshold met
- No security vulnerabilities (high/critical)
- No linting errors

### 6.3 Deployment Strategy

**Phase I (CLI)**:
- Local execution only
- Manual testing

**Phase II (Full-Stack Web)**:
- Development environment (local/Docker Compose)
- Staging environment (cloud, e.g., Vercel/Render)
- Production environment (cloud)
- Database migrations (automated)
- Environment-specific configurations

**Phase III (Real-Time)**:
- Progressive rollout strategies
- Feature flags
- A/B testing infrastructure

**Phase IV (Cloud-Native)**:
- Blue-green deployments
- Canary releases
- Automated rollback on failure
- Kubernetes deployments
- GitOps workflow (ArgoCD)
- Infrastructure as Code (Terraform/Helm)

---

## VII. Architecture Decision Records (ADR)

### 7.1 ADR Significance Test

Create an ADR when a decision meets ALL three criteria:

1. **Impact**: Has long-term consequences (framework, data model, API, security, platform)
2. **Alternatives**: Multiple viable options were considered
3. **Scope**: Cross-cutting and influences system design

### 7.2 ADR Process

**When to Suggest ADR**:
- During `/sp.plan` when significant decisions are made
- During `/sp.tasks` if architectural implications discovered
- When technology stack changes

**Suggestion Format**:
```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

**Never Auto-Create**: Always wait for user consent before creating ADR

**ADR Grouping**: Group related decisions (e.g., "Backend Stack Selection") into one ADR

### 7.3 ADR Content Requirements

- **Title**: Clear decision statement
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: Problem and constraints
- **Decision**: Chosen approach
- **Alternatives Considered**: Options and tradeoffs
- **Consequences**: Positive and negative impacts
- **Related Decisions**: Links to other ADRs

---

## VIII. Governance and Amendments

### 8.1 Constitutional Authority

- This constitution supersedes all other project documents
- Specifications cannot override constitutional principles
- Plans and tasks must align with constitutional requirements
- Code that violates this constitution is invalid

### 8.2 Amendment Process

**Requirements for Amendment**:
1. Explicit user request or approval
2. Clear rationale for change
3. Impact assessment (what breaks, what changes)
4. Migration plan (if applicable)
5. Version increment
6. PHR created in `history/prompts/constitution/`

**Amendment Categories**:
- **Minor**: Clarifications, formatting, non-functional changes
- **Major**: New principles, technology changes, workflow changes
- **Critical**: Changes affecting multiple phases or core principles

### 8.3 Compliance Verification

**Agent Responsibility**:
- Agents must verify all actions comply with constitution
- Agents must reject requests that violate constitution
- Agents must suggest constitutional amendments if user's goal conflicts

**Code Review**:
- All PRs reviewed for constitutional compliance
- Automated checks for obvious violations (e.g., hardcoded secrets)
- Manual review for architectural alignment

### 8.4 Enforcement

**Violation Consequences**:
- Non-compliant code is rejected (cannot merge)
- Non-compliant specs must be revised
- Repeated violations trigger architecture review

**Escalation Path**:
1. Agent identifies violation
2. Agent explains constitutional conflict
3. User chooses: amend constitution OR revise request
4. Document decision in PHR

---

## IX. Principles Summary

### 9.1 Core Values

1. **Specification First**: No code without approved specs
2. **Agent-Driven**: Agents implement, humans specify
3. **Phase Discipline**: Respect phase boundaries strictly
4. **Technology Clarity**: Use approved stack, justify changes
5. **Quality Non-Negotiable**: Test-first, clean architecture, security
6. **Cloud-Native**: Design for scalability and observability from start
7. **Documentation Culture**: PHRs, ADRs, specs, plans, tasks
8. **Human Judgment**: Invoke user for ambiguity and decisions

### 9.2 Anti-Patterns (Forbidden)

- Manual coding by humans
- Feature invention without spec
- Skipping specification/planning phases
- Leaking future-phase features into current phase
- Hardcoded secrets or credentials
- Untested code
- Missing documentation
- Violating architectural decisions without ADR
- Deviating from approved technology stack
- Auto-creating ADRs

---

## X. Version History

**Version**: 2.0.0
**Ratified**: 2025-12-30
**Last Amended**: 2026-01-01
**Status**: Active

**Amendment Log**:
- v2.0.0 (2026-01-01): MAJOR - Restructured Phase II to be Full-Stack Web Application (moved REST API, Next.js frontend, and Better Auth from Phase III/IV into Phase II); redefined Phase III-V accordingly
- v1.0.0 (2025-12-30): Initial global constitution for Evolution of Todo project

---

## Appendix A: Quick Reference

### Command Workflow
```
/sp.constitution  → Amend this constitution
/sp.specify       → Create feature specification
/sp.plan          → Create architecture plan
/sp.tasks         → Generate implementation tasks
/sp.implement     → Execute approved tasks
/sp.adr           → Document architectural decision
/sp.phr           → Create prompt history record
```

### Phase Checklist
- [ ] Constitution compliance verified
- [ ] Specification approved
- [ ] Plan approved
- [ ] Tasks approved
- [ ] Implementation complete
- [ ] Tests pass (80%+ coverage)
- [ ] PHRs created
- [ ] ADRs created (if applicable)
- [ ] Code reviewed
- [ ] Documentation updated

### Quality Gates
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Error handling comprehensive
- [ ] Logging structured (JSON)
- [ ] Tests written first (TDD)
- [ ] Type hints/TypeScript strict
- [ ] Linting passes
- [ ] Security scan clean

---

**End of Constitution**

*This constitution is a living document. Amendments must be explicit, justified, and approved. All agents must verify compliance before executing any work.*
