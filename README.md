# Solutionists

**The operating system for New Zealand honey companies entering India.**

An AI-first trading, intelligence, and operations platform built for the
NZ honey → India trade corridor.

> "Give us your honey company. We'll tell you how to enter India."

---

## The Thesis

Think **Stripe + Shopify + Palantir for NZ → India trade** — focused first on
the New Zealand honey industry.

We are not building another honey brand. We are building **infrastructure**
that helps New Zealand honey businesses enter, sell into, operate in, and
scale within India. The platform is the operating layer between NZ honey
exporters and the Indian market.

```
NZ Honey Company
        ↓
Solutionsists Platform
        ↓
┌───────────────────────────────┐
│ India Market Intelligence     │
│ Buyer Intelligence            │
│ Trade Intelligence            │
│ Regulatory Intelligence       │
│ Competitive Intelligence      │
│ AI Research Agents            │
│ Revenue Intelligence          │
│ Outreach                      │
│ CRM / Pipeline                │
│ Trade Operations              │
└───────────────────────────────┘
        ↓
Indian Market → Buyers / Distributors / Retailers
```

## Beachhead

- **Vertical:** New Zealand honey
- **Destination market:** India
- Do not generalize into global trade yet. Become extremely good at this
  corridor first.

---

## Product Philosophy

The product answers:

> **What should I know?** → **Who should I contact?** → **What should I say?**

```
INTELLIGENCE → DECISION → ACTION
```

Not: `LEADS → AI EMAIL → SPAM`.

## Evidence-First Design

Every important intelligence claim is backed by **evidence**:

- source URL
- source type
- date discovered
- extracted content
- confidence

AI never fabricates facts. When evidence is missing, the system says
"insufficient evidence."

## Data Pipeline

```
Sources
   ↓
Ingestion
   ↓
Normalization
   ↓
Entity Resolution
   ↓
Knowledge Store
   ↓
AI Research
   ↓
Intelligence
   ↓
Recommendations
   ↓
Revenue Actions
```

The system separates **raw data**, **normalized data**, **AI-derived
intelligence**, and **user-generated data**.

---

## MVP

**"India Market Entry Intelligence for NZ Honey Companies"**

Input: an NZ honey company.

Output:
1. Company intelligence report
2. India market overview
3. Recommended market segments
4. Top Indian buyers
5. Buyer/company intelligence
6. Contact discovery
7. Buyer scoring
8. Evidence for recommendations
9. Recommended outreach
10. Next actions

---

## Architecture

```
frontend/          Next.js business intelligence dashboard
src/
  api/             FastAPI routes
  models/          SQLAlchemy domain models
  schemas/         Pydantic API schemas
  agents/          Specialized research agents
  providers/       LLM / search / enrichment abstractions
  services/        Scoring, evidence, intelligence services
  db/              Database engine, session, seed
alembic/           Database migrations
data/              Seed datasets (NZ honey company universe)
tests/             Test suite
```

### Specialized agents

| Agent | Answers |
|---|---|
| Market Research | What's happening in the Indian honey market? |
| Buyer Discovery | Finds importers, distributors, retailers, manufacturers |
| Company Intelligence | Investigates an individual company |
| Trade Intelligence | Import/export data, HS codes, volumes, pricing |
| Regulatory | Indian import / NZ export requirements |
| Competitive Intelligence | Competing exporters and positioning |
| Revenue | Who to sell to, why, and what to do next |
| Monitoring | Continuous watch for changes |

The Revenue Agent consumes intelligence from the rest of the platform. It
is downstream, not a generic cold-outreach bot.

---

## Getting Started

### Backend

```bash
cp .env.example .env   # add API keys
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m src.db.seed  # seed NZ honey company universe
uvicorn src.api.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Tests

```bash
pytest
```

---

## Team

| Member | Role |
|---|---|
| Aayush | Team Lead |
| Adarsh | Team Member |
| Trish | Team Member |
| Varun | Team Member |
| Srikar | Team Member |
| Harshith | Team Member |
