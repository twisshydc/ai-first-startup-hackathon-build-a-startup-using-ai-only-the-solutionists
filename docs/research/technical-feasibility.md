# Technical Feasibility Report — The Solutionists

**Issue:** #4 — Validate Technical Feasibility  
**Product Direction:** AI Revenue / Sales Intelligence  
**Phase:** MVP Validation  
**Status:** **Technically feasible, with data quality and provider constraints**

---

## 1. Executive Decision

### Verdict: YES — the proposed MVP is technically feasible.

The current product hypothesis is:

> Given a company's Ideal Customer Profile (ICP), discover relevant companies, research them using verifiable evidence, qualify and rank them, enrich relevant contacts, and prepare personalised outreach.

The core workflow can be built today using existing web-search, data-enrichment, LLM, database, and web-application infrastructure.

The important constraint is that **the MVP should not attempt to become a fully autonomous sales platform**.

The first version should prove one thing:

> **Can we consistently identify a small number of high-quality prospects and explain why they are worth contacting?**

The hardest problems are not model training or frontend development. They are:

1. Data quality and freshness
2. Evidence-grounded AI decisions
3. Provider/API limits and cost
4. Company deduplication and identity resolution
5. Contact-data availability
6. Data licensing, privacy, and permitted access
7. Measuring whether the ranking is actually useful

---

# 2. MVP Scope

## 2.1 User Input

The user provides an ICP in natural language.

Example:

```text
B2B SaaS companies in the US with 50–500 employees
that are currently hiring sales or customer-success roles.
```

The system converts this into structured criteria:

```json
{
  "business_model": "B2B SaaS",
  "location": ["US"],
  "employee_range": {
    "min": 50,
    "max": 500
  },
  "signals": [
    "sales hiring",
    "customer-success hiring"
  ]
}
```

---

## 2.2 MVP Workflow

```text
                 User ICP
                    │
                    ▼
            ICP Normalisation
                    │
                    ▼
            Prospect Discovery
                    │
                    ▼
          Company Deduplication
                    │
                    ▼
            Evidence Collection
             ┌──────┼──────┐
             ▼      ▼      ▼
          Website  Jobs   Public Data
             └──────┼──────┘
                    ▼
          AI Extraction + Qualification
                    │
                    ▼
          Explainable Lead Scoring
                    │
                    ▼
          Contact Enrichment (Top Leads)
                    │
                    ▼
          Personalised Outreach Draft
                    │
                    ▼
              User Review
```

---

# 3. What the MVP Should Produce

For every qualified company, the user should receive something similar to:

```text
Acme Software

ICP Score: 91/100

Why it qualifies:
✓ B2B SaaS
✓ US-based
✓ Fits target company size
✓ Relevant hiring signal
✓ Evidence of a potential business need

Evidence:
• Company website
• Careers page
• Relevant job posting
• Other permitted public/company sources

Recommended contact:
VP Customer Success

Outreach angle:
A short message based only on verified company evidence.
```

The important product principle is:

> **Every important AI-generated claim should be traceable to evidence.**

---

# 4. Recommended Architecture

```text
┌─────────────────────────────────────────────┐
│                 Next.js UI                  │
│  ICP Input → Prospect Table → Research UI  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                FastAPI Backend              │
│ Auth / API / Jobs / Scoring / Orchestration │
└───────────────┬───────────────┬─────────────┘
                │               │
                ▼               ▼
        ┌──────────────┐  ┌──────────────┐
        │ Job / Worker │  │ PostgreSQL   │
        │ Queue        │  │              │
        └──────┬───────┘  └──────────────┘
               │
      ┌────────┼─────────┐
      ▼        ▼         ▼
   Search   Enrichment  LLM
   Provider Provider    Layer
      │        │         │
      ▼        ▼         ▼
   Tavily    Hunter    GPT-5 mini
      │
      ▼
 Public / Company Sources
```

### Why this architecture?

- Frontend remains independent from providers.
- Long-running research does not block the API request.
- External providers can be replaced.
- Evidence and scores can be stored and audited.
- AI is used for extraction and reasoning rather than being treated as the source of truth.

---

# 5. Recommended Technology Stack

| Layer | Recommendation | Reason |
|---|---|---|
| Frontend | Next.js | Fast MVP dashboard development |
| Backend | Python + FastAPI | Good fit for AI/data workflows |
| Database | PostgreSQL | Structured company, evidence and scoring data |
| Queue | Redis + background worker | Handles asynchronous research jobs |
| LLM | GPT-5 mini | Cost-sensitive extraction, classification and generation |
| Web research | Tavily | Search and web extraction |
| Alternative research | Exa | Useful alternative for AI-oriented search |
| Contact enrichment | Hunter | Email finding and verification |
| Public US company data | SEC EDGAR | Official filings and XBRL data |
| Deployment | Vercel + managed backend/database | Simple MVP deployment |

The provider choices should remain behind interfaces so that the product is not permanently coupled to one vendor.

---

# 6. Data Sources

## 6.1 Company Websites — Primary Source

Company-owned websites should be treated as a primary evidence source.

Useful signals include:

- Company description
- Product/service information
- Industry
- Target market
- Locations
- Careers
- Job postings
- Customer stories
- Pricing
- Product announcements

The system should store the source URL and retrieval time for important evidence.

---

## 6.2 Tavily — Primary Web Research Provider

Tavily provides search and extraction capabilities designed for AI applications.

Current published pricing includes:

- 1,000 API credits/month on the free Researcher plan
- Pay-as-you-go pricing of $0.008 per credit
- Higher-volume plans with additional credits and rate limits

Reference: https://www.tavily.com/pricing

For the MVP, Tavily can be used for:

```text
ICP
 ↓
Search queries
 ↓
Relevant pages
 ↓
Extract useful content
 ↓
Evidence passed to AI layer
```

Important: API-credit usage depends on the request type, so actual cost must be measured during the validation experiment.

---

## 6.3 Hunter — Contact Enrichment

Hunter can be used after a company has already qualified.

Relevant functionality includes:

- Domain Search
- Email Finder
- Email Verification
- Enrichment

Hunter's API documentation states that Domain Search, Email Finder and enrichment calls consume credits according to the endpoint, and that API endpoints have rate limits.

Reference: https://hunter.io/api-documentation

Current pricing information:

https://hunter.io/pricing

### Architectural rule

Do **not** enrich every discovered company.

Use:

```text
1000 discovered
      ↓
Cheap filtering
      ↓
200 candidates
      ↓
Research
      ↓
50 qualified
      ↓
Contact enrichment
      ↓
Top prospects
```

This controls both cost and unnecessary processing of personal data.

---

## 6.4 Exa — Alternative / Secondary Research Provider

Exa is another possible web-search and research provider.

Its current pricing includes:

- Search pricing based on requests
- Page-content pricing
- Deep Search
- Agent-based research
- Company and people search use cases

Reference: https://exa.ai/pricing

For the MVP, Exa should be evaluated against Tavily rather than automatically added as a second dependency.

The team should choose based on:

- Search relevance
- Evidence quality
- Cost per qualified company
- Latency
- Rate limits
- Ease of integration

---

## 6.5 SEC EDGAR — Public Company Data

For US public companies, SEC EDGAR provides APIs for submissions and extracted XBRL data.

Reference:

https://www.sec.gov/search-filings/edgar-application-programming-interfaces

Potential signals include:

- Company filings
- Filing dates
- Financial information
- Corporate identifiers
- Recent public-company events

SEC data is especially useful for public companies but should not be treated as the primary source for the entire prospect universe.

---

# 7. AI Approach

## 7.1 Retrieval First, Generation Second

The LLM should not be asked:

```text
"Find good prospects and tell me why."
```

as a single unconstrained task.

Instead:

```text
External Sources
       ↓
Retrieved Evidence
       ↓
Structured Extraction
       ↓
Qualification
       ↓
Scoring
       ↓
Explanation
       ↓
Outreach Draft
```

The model should reason **over retrieved evidence**.

---

## 7.2 Evidence Object

A useful internal representation is:

```json
{
  "claim": "Company is hiring customer-success employees",
  "source_url": "https://example.com/careers",
  "source_title": "Careers",
  "retrieved_at": "2026-08-20T10:30:00Z",
  "confidence": 0.94
}
```

This allows the application to answer:

> Why did the system give this company a high score?

---

## 7.3 Hallucination Control

The system should explicitly prevent the model from inventing:

- Funding information
- Employee counts
- Customers
- Technologies
- Job openings
- Business problems
- Contact information
- Personal details

If evidence is missing, the system should say:

```text
Unknown / insufficient evidence
```

rather than guessing.

---

# 8. Lead Scoring

The first scoring system should be transparent.

Recommended starting model:

| Signal | Weight |
|---|---:|
| ICP Match | 30 |
| Company Size | 15 |
| Industry Match | 15 |
| Intent / Growth Signals | 20 |
| Problem/Pain Signal | 10 |
| Contact Availability | 10 |
| **Total** | **100** |

Example:

```text
Acme Software — 92/100

ICP Match              28/30
Company Size           13/15
Industry Match         15/15
Intent Signals         18/20
Pain Signal             8/10
Contact Availability   10/10
--------------------------------
Total                   92/100
```

The exact weights should be validated experimentally rather than treated as final.

---

# 9. Company Identity and Deduplication

A company may appear as:

```text
Acme Inc.
Acme
Acme Technologies
acme.com
www.acme.com
```

The primary identity should be based on a normalized domain where available.

Example:

```text
https://www.acme.com/
        ↓
acme.com
```

Secondary matching can use:

```text
normalized company name + country
```

Contact identity should use normalized email where available.

Deduplication is important because duplicate companies would:

- Waste API credits
- Distort ranking
- Produce duplicate outreach
- Make evaluation unreliable

---

# 10. Data Model

A minimal schema:

```text
companies
---------
id
name
domain
industry
location
employee_range
created_at
updated_at

prospects
---------
id
company_id
name
role
email
email_confidence
source

evidence
--------
id
company_id
claim
source_url
source_title
retrieved_at
confidence

scores
------
id
company_id
icp_score
size_score
industry_score
intent_score
pain_score
contact_score
total_score
explanation
created_at
```

The evidence table is especially important because it allows the team to inspect how the AI reached its conclusion.

---

# 11. Progressive Enrichment

This is one of the most important cost-control decisions.

### Bad

```text
1000 companies
      ↓
Deep research
      ↓
Contact enrichment
      ↓
LLM generation
```

### Recommended

```text
1000 discovered
      ↓
Cheap deterministic filtering
      ↓
200 candidates
      ↓
Web research
      ↓
50 qualified
      ↓
Contact enrichment
      ↓
Top 20–25
      ↓
Deep research + outreach
```

This reduces:

- Search cost
- LLM usage
- Enrichment cost
- Processing time
- Unnecessary personal-data processing

---

# 12. Caching

Research results should be cached.

Example:

```text
company domain
      ↓
research cache
      ↓
existing evidence
```

If the same company is evaluated against a different ICP:

```text
Existing company research
          ↓
Reuse evidence
          ↓
Recalculate qualification
          ↓
New ICP score
```

This prevents repeatedly paying to research the same company.

Evidence should still have a retrieval timestamp so that stale information can be detected.

---

# 13. Provider Abstraction

External providers should not be called directly throughout the application.

Recommended structure:

```text
providers/
├── search/
│   ├── base.py
│   ├── tavily.py
│   └── exa.py
│
├── enrichment/
│   ├── base.py
│   └── hunter.py
│
└── public_data/
    └── sec.py
```

Application code should call an internal interface such as:

```python
research_provider.search(...)
```

instead of depending everywhere on:

```python
tavily.search(...)
```

This makes it possible to replace a provider without rewriting the product.

---

# 14. Reliability Requirements

External API calls should include:

- Request timeouts
- Retries
- Exponential backoff
- Rate limiting
- Request logging
- Caching
- Failure handling
- Provider fallback where justified

Retries should be bounded.

Long-running research should be asynchronous:

```text
User starts research
        ↓
Create job
        ↓
Queue
        ↓
Worker
        ↓
Search / research
        ↓
Extract evidence
        ↓
Score
        ↓
Store results
        ↓
Dashboard
```

The user should not have to keep an HTTP request open while the entire research pipeline runs.

---

# 15. Cost Feasibility

The MVP is financially feasible for experimentation because the major providers offer free tiers or usage-based pricing.

Current published examples:

| Provider | Current published entry pricing |
|---|---|
| Tavily | 1,000 free API credits/month; $0.008/credit pay-as-you-go |
| Hunter | Free plan available; paid plans and API credits available |
| Exa | $20 signup credits and usage-based API pricing |
| GPT-5 mini | $0.25 / 1M input tokens; $2 / 1M output tokens |

Sources:

- https://www.tavily.com/pricing
- https://hunter.io/pricing
- https://exa.ai/pricing
- https://developers.openai.com/api/docs/models/gpt-5-mini

### Important

These numbers are **provider prices, not our final product cost**.

Actual cost depends on:

- Number of companies discovered
- Searches per company
- Pages extracted
- LLM tokens
- Contact enrichment rate
- Verification rate
- Retry rate
- Cache hit rate

Therefore the team should measure cost per qualified prospect during validation.

---

# 16. Cost-Control Strategy

The MVP should optimize for:

```text
Cost per qualified prospect
```

rather than:

```text
Cost per discovered company
```

Recommended controls:

1. Cheap filtering first
2. Research only promising candidates
3. Enrich only qualified prospects
4. Cache company research
5. Limit search depth
6. Limit LLM context to relevant evidence
7. Avoid unnecessary retries
8. Track provider usage per research job

---

# 17. API and Rate-Limit Risks

Potential failures include:

```text
Search provider
      ↓
Rate limit
      ↓
429 / temporary failure
```

The system should respond with:

```text
Retry with backoff
       ↓
Retry limit reached?
       ↓
Record failure
       ↓
Continue other jobs
```

One provider failure should not destroy the entire research job.

Provider-specific rate limits must be checked during implementation.

---

# 18. Data Freshness

Prospect data becomes stale.

Examples:

- Employees change roles
- Job postings close
- Companies change websites
- Contact emails become invalid
- Companies are acquired
- Business priorities change

Therefore each evidence record should have:

```text
retrieved_at
```

and the system should distinguish:

```text
Verified recently
Old evidence
Unknown / stale
```

A future version can implement scheduled re-research.

---

# 19. Legal, Privacy and Data-Access Considerations

This area requires special care before production use.

The system may process:

### Company information

Examples:

- Company name
- Domain
- Industry
- Public business information

### Personal data

Examples:

- Name
- Professional email
- Job title
- Other identifiers

For the MVP:

- Prefer licensed APIs and permitted sources
- Store provenance for important data
- Minimize personal data collection
- Do not collect fields that are unnecessary for the product
- Provide deletion/correction mechanisms where required
- Define retention rules
- Document data providers
- Review each provider's terms before integration

India's Digital Personal Data Protection Rules, 2025 are now published by MeitY, so privacy and data-processing requirements need to be considered for an India-based product handling personal data.

Reference:

https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa

This report is a technical feasibility assessment, **not legal advice**. Production launch should include an appropriate legal/privacy review.

---

# 20. LinkedIn and Restricted Sources

The architecture should **not depend on scraping websites whose terms prohibit the intended automated access**.

In particular, LinkedIn's User Agreement and Crawling Terms should be reviewed before any automated collection is considered.

References:

- https://www.linkedin.com/legal/user-agreement
- https://www.linkedin.com/legal/crawling-terms

Recommended architecture:

```text
Licensed / permitted provider
            ↓
         Our API
```

rather than:

```text
Browser automation
        ↓
Unauthorized scraping
        ↓
Our database
```

This reduces both technical and legal risk.

---

# 21. Major Technical Risks

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Poor search relevance | High | High | Multiple query strategies + evaluation |
| AI hallucination | Medium/High | High | Evidence-grounded generation |
| Duplicate companies | High | Medium | Domain-based identity |
| Stale information | High | Medium | Retrieval timestamps |
| Missing contact data | Medium | Medium | Multiple permitted providers |
| API rate limits | Medium | Medium | Queue + backoff |
| Provider outage | Medium | High | Provider abstraction |
| Unexpected API cost | Medium | High | Progressive enrichment + budgets |
| Data licensing restrictions | Medium | High | Provider/terms review |
| Privacy risk | Medium | High | Data minimization + retention controls |
| Weak lead ranking | High | High | Human-labelled validation set |

---

# 22. What We Should NOT Build in MVP

To keep the project focused, defer:

- Fully autonomous cold-email sending
- Automated email sequences
- LinkedIn automation
- CRM integrations
- Autonomous browser agents
- Huge proprietary lead database
- Fine-tuning a custom LLM
- Complex multi-agent architecture
- Mobile application
- Automatic sales execution

The MVP should prove **research and qualification quality** before expanding into sales automation.

---

# 23. MVP Implementation Plan

## Phase 1 — Discovery

Build:

```text
ICP input
   ↓
Structured ICP
   ↓
Search provider
   ↓
Company candidates
```

Goal:

> Produce relevant candidate companies.

---

## Phase 2 — Research

Build:

```text
Company
   ↓
Website / relevant pages
   ↓
Extract evidence
   ↓
Store evidence
```

Goal:

> Every important qualification claim has a source.

---

## Phase 3 — Qualification

Build:

```text
ICP + Evidence
       ↓
LLM extraction
       ↓
Qualification fields
       ↓
Explainable score
```

Goal:

> Rank companies consistently and explain the ranking.

---

## Phase 4 — Enrichment

For only the best candidates:

```text
Qualified company
       ↓
Contact search
       ↓
Email verification
       ↓
Contact record
```

Goal:

> Determine whether useful contact information can be obtained reliably.

---

## Phase 5 — Outreach Draft

```text
Verified company evidence
          +
Verified contact role
          ↓
Personalised draft
```

Goal:

> Generate a short outreach draft based only on evidence.

The system should require human review before any outreach is sent.

---

# 24. Validation Experiment

Before building the full product, create a labelled test set of **50 real companies** that match the intended ICP.

Manually label each company:

```text
GOOD
MAYBE
BAD
```

Then run the automated pipeline.

---

## 24.1 Precision@10

Measure:

```text
Good companies in top 10
------------------------
10
```

Example:

```text
7 good companies in top 10
→ Precision@10 = 70%
```

---

## 24.2 Evidence Accuracy

For generated claims, label:

```text
Supported
Partially Supported
Unsupported
```

Target:

```text
≥ 90% of important claims supported by evidence
```

This is an internal MVP target, not an industry benchmark.

---

## 24.3 Contact Enrichment Success

Measure:

```text
Valid useful contacts
---------------------
Contact requests
```

The team should track both successful and unsuccessful enrichment attempts.

---

## 24.4 Research Cost

Track:

```text
Total provider + LLM cost
-------------------------
Qualified companies
```

This gives us:

> Cost per qualified prospect.

---

## 24.5 Time Saved

Compare:

```text
Average manual research time
              vs.
Average AI-assisted research time
```

The product should only be considered useful if it meaningfully reduces research effort without destroying lead quality.

---

# 25. Initial Success Criteria

For the first prototype, use these as internal targets:

| Metric | Initial Target |
|---|---:|
| Precision@10 | ≥ 70% |
| Evidence-supported important claims | ≥ 90% |
| Successful contact enrichment | ≥ 60% |
| Manual research time reduction | ≥ 50% |
| Duplicate company rate | < 5% |

These targets are intended to guide our experiment. They are **not claims about industry-standard performance**.

If the system fails primarily because of poor data quality, improve the retrieval/data pipeline before adding more AI features.

---

# 26. Repository Structure

Recommended project structure:

```text
.
├── docs/
│   ├── decisions/
│   ├── meeting-notes/
│   └── research/
│       └── technical-feasibility.md
│
├── src/
│   ├── api/
│   ├── discovery/
│   ├── research/
│   ├── enrichment/
│   ├── scoring/
│   ├── llm/
│   ├── providers/
│   └── db/
│
├── tests/
│
└── README.md
```

---

# 27. Final Technical Verdict

## Feasibility: **YES**

The required building blocks are available:

| Capability | Feasibility |
|---|---|
| ICP parsing | High |
| Company discovery | High |
| Web research | High |
| Evidence extraction | High |
| AI qualification | High |
| Explainable scoring | High |
| Contact enrichment | High |
| Dashboard | High |
| Async processing | High |
| Data quality | Medium |
| Reliable ranking | Medium |
| Cost control | Medium |
| Data licensing/privacy | Medium |

### The product is technically feasible because:

- We do not need to train a new foundation model.
- We can use existing search and enrichment APIs.
- We can use an LLM for structured extraction and reasoning.
- Standard web/backend/database infrastructure is sufficient.
- The architecture can be built incrementally.

### The product is NOT automatically validated because:

Technical feasibility does not prove that the system will produce good leads.

That requires the 50-company validation experiment.

---

# 28. Recommended MVP Decision

Proceed with the MVP, but keep the first implementation narrow:

```text
ICP
 ↓
Discover
 ↓
Research
 ↓
Evidence
 ↓
Qualify
 ↓
Rank
 ↓
Enrich top prospects
 ↓
Generate outreach draft
 ↓
Human review
```

### Do not start with:

```text
Find everyone
 ↓
Enrich everyone
 ↓
Email everyone
```

The first version should optimize for:

> **Quality of qualified prospects + evidence + time saved**

rather than volume.

---

# 29. Bottom Line

> **The Solutionists can realistically build the proposed AI Revenue / Sales Intelligence MVP using existing technology.**

The key technical strategy is:

**Retrieve → Verify → Structure → Score → Explain → Enrich → Draft**

The largest risks are **data quality, provider constraints, cost, privacy/licensing, and ranking accuracy**, not the availability of AI technology.

Therefore:

> **Build the research-and-qualification engine first. Prove that it finds better prospects faster. Then expand into outreach automation and broader sales workflows.**

---

## References

### AI / LLM

- OpenAI GPT-5 mini: https://developers.openai.com/api/docs/models/gpt-5-mini
- OpenAI GPT-5 developer announcement: https://openai.com/index/introducing-gpt-5-for-developers/

### Web Research

- Tavily pricing: https://www.tavily.com/pricing
- Tavily API documentation: https://docs.tavily.com/
- Exa pricing: https://exa.ai/pricing

### Contact Enrichment

- Hunter pricing: https://hunter.io/pricing
- Hunter API documentation: https://hunter.io/api-documentation

### Public Company Data

- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

### Data Access / Privacy

- LinkedIn User Agreement: https://www.linkedin.com/legal/user-agreement
- LinkedIn Crawling Terms: https://www.linkedin.com/legal/crawling-terms
- MeitY — Digital Personal Data Protection Rules 2025: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
