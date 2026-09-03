# Restructuring Plan & Classification

Product pivot: **AI Revenue / Customer Acquisition Agent** →
**NZ → India Honey Trade Intelligence & Operations Platform**.

## Audit result

The repository was pre-development: research docs, a single lead list, and a
data-generation script. No application code existed to port.

## Classification

| Component | Verdict | Rationale |
|---|---|---|
| `README.md` | **REPLACE** | Described the old product. Rewritten for the new dashboard/threshold. |
| `generate_master_leads.py` | **REMOVE** | Hardcoded 105-company list superseded by the CMS/seed DB. Kept only as historical reference (data already exported). |
| `nz_honey_master_leads.csv` | **KEEP** | Initial seed dataset. Migrated to `data/` and consumed by `src/db/seed.py`. |
| `docs/Research/Analysing_Competitors.md` | **KEEP** | Market research remains valid context. |
| `docs/research/technical-feasibility.md` | **KEEP** | Evidence-first, provider-abstraction, cost-control guidance retained as foundation. |
| `docs/meeting-notes/` | **KEEP** | Historical record. |
| `docs/Research/Validating Target Profile.md` | **KEEP (dedupe)** | Duplicate of the meeting-notes copy; kept for reference. |
| `.gitignore` | **KEEP** | Extend for Python/Node. |

### New architecture (built from scratch)

| Layer | Component | Location |
|---|---|---|
| Core objects | SQLAlchemy models: HoneyCompany, IndianCompany, Contact, HoneyProduct, Market, MarketSegment, TradeFlow, Regulation, Certification, Tariff, Competitor, Evidence, DataSource, ResearchReport, AgentRun, Opportunity, Recommendation, Outreach, Conversation | `src/models/` |
| Database | Engine, session, seed | `src/db/` |
| Migrations | Alembic | `alembic/` |
| API | FastAPI routes | `src/api/` |
| Agents | 8 specialized agents + registry | `src/agents/` |
| Providers | LLM / search / enrichment abstractions | `src/providers/` |
| Services | Scoring (NZ + buyer), evidence, intelligence | `src/services/` |
| Frontend | Next.js dashboard | `frontend/` |
| Tests | pytest | `tests/` |

## Alignment with the brief

- **Core product objects** (section 6): designed as distinct models, no giant
  `Lead` object.
- **Intelligence graph** (section 7): supported via foreign keys /
  relationships between entities.
- **Multi-agent architecture** (section 8): eight modular agents, each
  independently testable.
- **Evidence-first design** (section 9): `Evidence` + `DataSource` models;
  claims carry source, type, retrieved-at, confidence.
- **Data pipeline** (section 10): ingestion/seed → normalization → scoring
  separated from AI generation.
- **NZ honey lead DB** (section 11): migrated as the seed "NZ Honey Company
  Universe" with enrichment fields.
- **Company scoring** (section 12) and **buyer scoring** (section 13):
  explainable, configurable weights in `services/scoring.py`.
- **MVP** (section 15): India Market Entry Intelligence focus.
- **UI/UX** (section 16): structured dashboard, tables, intelligence reports —
  not a chatbot.

## Principles respected

- Modular architecture, providers behind interfaces (`providers/`).
- Data ingestion separated from intelligence generation.
- Agents independently testable.
- Scoring deterministic and inspectable.
- Evidence tracked with provenance.
- LLM calls behind clear interfaces.
- No speculative features beyond the MVP skeleton.

## Future phases (beyond MVP)

- Trade Operations (transaction workflow, documentation, logistics).
- Monitoring agent scheduled runs.
- Contact enrichment provider wiring.
- Full regulation/tariff data ingestion.
