# Technical Feasibility Report — Prospect Research & Sales Intelligence MVP

**Project:** The Solutionists  
**Issue:** #4 — Validate technical feasibility  
**Status:** Feasible for MVP  
**Recommendation:** Build a focused, evidence-first prospect research workflow rather than a full sales automation platform.

---

## 1. Executive Decision

The proposed MVP is **technically feasible with currently available APIs and models**.

The strongest architecture is:

```text
User ICP
  ↓
ICP → structured search criteria
  ↓
Prospect / company discovery
  ↓
Website + jobs + news + public-data research
  ↓
Entity resolution + deduplication
  ↓
AI qualification + evidence extraction
  ↓
Lead scoring
  ↓
Research brief
  ↓
Email/contact enrichment
  ↓
Personalised outreach draft
```

### Recommended MVP stack

| Layer | Recommendation | Why |
|---|---|---|
| Web discovery/research | **Tavily** | Search + extraction designed for AI workflows; simple credit model |
| Alternative research/search | **Exa** | Strong AI search and company/people research; useful if startup credits are available |
| Company/contact discovery | **Hunter Discover** | Company discovery is free on its Data Platform API |
| Email discovery | **Hunter Email Finder / Domain Search** | Clear API, verification, confidence scores, and public-source provenance |
| Public-company facts | **SEC EDGAR APIs** | Official, free, no API key |
| AI reasoning | **GPT-5 mini** | Good fit for high-volume structured classification and summarisation |
| Database | **PostgreSQL** | Reliable relational model for companies, prospects, evidence and scores |
| Backend | **Python + FastAPI** | Fast to build and well suited to data/AI workflows |
| Async jobs | **Redis + Celery/RQ** or a simple job queue | Prevent long research requests from blocking the API |
| Frontend | **Next.js** | Fast dashboard/prototype development |
| Initial deployment | **Vercel + managed Postgres + backend host** | Keep infrastructure simple |

**Important:** Apollo is useful technically, but it should **not be the core data provider for this MVP without confirming the applicable commercial/API agreement.** Apollo's current API terms restrict third-party integrations and prohibit using the API to replicate or compete with Apollo products unless authorized. Their developer FAQ also says sharing/exposing/reselling Apollo data to non-Apollo users requires a custom contract. See the legal section below.

---

# 2. What the MVP Should Actually Do

Do not attempt to build "an AI sales platform."

Build one very clear workflow:

> **Give us an ICP → get a ranked list of companies with evidence explaining why each company is a good prospect.**

For example:

### Input

```text
We sell an AI customer-support product.

Find:
- B2B SaaS companies
- 20–500 employees
- US/UK
- likely to have a customer-support team
- recently growing or hiring
- likely to benefit from AI automation
```

### Output

```text
1. Acme Software
   ICP Score: 91/100

   Why:
   ✓ B2B SaaS
   ✓ ~120 employees
   ✓ Hiring customer-support roles
   ✓ Has a large support/customer-success function
   ✓ Website describes a high-volume support workflow

   Evidence:
   - Company website
   - Careers page
   - Job posting
   - Recent company/news page

   Recommended contact:
   VP Customer Success

   Outreach angle:
   "You appear to be expanding your support team while..."
```

This is much more defensible than asking an LLM to invent a lead list.

---

# 3. Data Sources

## Tier 1 — Use First

### 3.1 Company websites

**Source:** The prospect's own website.

Use it for:

- Company description
- Product/service
- Industry
- Target customers
- Pricing
- Locations
- Contact pages
- Careers
- Customer stories
- Product changes
- Technology clues

This should be the **highest-priority evidence source** because it is directly controlled by the company.

---

### 3.2 Tavily

Tavily provides AI-oriented web search, extraction, mapping and crawling.

Current pricing includes:

- 1,000 free API credits/month
- Pay-as-you-go at $0.008/credit
- Basic search: 1 credit/request
- Advanced search: 2 credits/request
- Extraction is also credit-based

For an MVP, use Tavily mainly for:

```text
search → identify relevant pages
extract → retrieve page content
```

Do not crawl the entire internet. Search only for evidence relevant to the ICP.

Source:

https://www.tavily.com/pricing

https://docs.tavily.com/documentation/api-credits

---

### 3.3 Hunter

Hunter is a strong fit for the **contact-enrichment part** of the MVP.

Useful APIs:

- Discover
- Domain Search
- Email Finder
- Email Verifier
- Enrichment

Hunter's current documentation says its Discover API is free of charge on Data Platform plans. Domain Search costs 1 search credit for 1–10 returned emails, and Email Finder costs 1 search credit per email found.

Hunter also explicitly documents use of its API in third-party applications/SaaS.

Use it **after** a company has passed the qualification stage.

Do not spend enrichment credits on every discovered company.

Source:

https://hunter.io/api-documentation

https://help.hunter.io/en/articles/12149400-hunter-api-for-data-plans

https://hunter.io/pricing

---

### 3.4 SEC EDGAR

For US public companies, SEC EDGAR provides official submissions and XBRL company facts through APIs without authentication/API keys.

Useful signals:

- Revenue
- Financial statements
- Filings
- Company identifiers
- Filing dates
- Recent 10-K/10-Q/8-K activity

This is especially useful for larger prospects.

Source:

https://www.sec.gov/search-filings/edgar-application-programming-interfaces

---

## Tier 2 — Add Later

### 3.5 Exa

Exa is a strong alternative/addition for AI-oriented web research.

Current pricing includes:

- $20 signup credits
- $10/month free tier
- Search: $7/1,000 requests
- Contents: $1/1,000 pages
- Deep Search: $12–15/1,000 requests
- Startup/education grants may provide additional credits

Exa is particularly interesting if the team gets its startup grant.

Source:

https://exa.ai/pricing

---

### 3.6 Public government/company registries

Where useful, integrate official registries for the target geography.

Examples:

- SEC EDGAR — United States
- Companies House — United Kingdom
- Other national business registries where API access and licensing permit

These should be treated as structured verification sources, not the only discovery mechanism.

---

### 3.7 Google Places

Only use Google Places when location is actually part of the ICP.

For example:

```text
Find dental clinics in Bangalore
Find logistics companies in Mumbai
Find restaurants with multiple locations
```

It should **not** be the primary source for generic B2B SaaS prospect discovery.

Google's current pricing is SKU-based and field selection affects billing, so unnecessary fields should be avoided.

Source:

https://developers.google.com/maps/billing-and-pricing/pricing-india

---

# 4. Data Sources We Should NOT Make Core Dependencies

## LinkedIn scraping

Do **not** build the MVP around scraping LinkedIn.

LinkedIn's current User Agreement prohibits using software/scripts/crawlers to scrape or copy the service and also restricts unauthorized automated access.

LinkedIn's crawling terms state that automated crawling requires express permission.

Therefore:

```text
BAD:
Our system → browser bot → LinkedIn → scrape profiles
```

Prefer:

```text
Our system → licensed/API provider
                    ↓
              structured data
```

Source:

https://www.linkedin.com/legal/user-agreement

https://www.linkedin.com/legal/crawling-terms

---

## Apollo as a hidden backend

Apollo has excellent technical capabilities for company/person search and enrichment, but its current API terms are a major consideration.

Apollo states that:

- API access is licensed primarily for internal business purposes unless otherwise agreed.
- Third-party API credentials cannot be used without authorization.
- Integrating the API with your own product/service requires authorization.
- API use cannot be used to replicate or compete with Apollo products.
- Sharing/exposing/reselling data to non-Apollo users requires a custom contract.

Therefore:

### For the hackathon prototype

Apollo can be investigated as a **potential future licensed provider**.

### For the core MVP architecture

Do not make the product dependent on Apollo unless the team confirms the required authorization/contract.

Sources:

https://www.apollo.io/terms/api

https://docs.apollo.io/docs/developer-faqs

https://docs.apollo.io/docs/api-pricing

---

# 5. AI Architecture

The AI should **not** be responsible for discovering everything.

Use deterministic data collection first.

```text
SEARCH / API
    ↓
RAW EVIDENCE
    ↓
NORMALIZATION
    ↓
LLM EXTRACTION
    ↓
SCORING
    ↓
GENERATED SUMMARY
```

## Model responsibilities

### Task A — ICP parsing

Convert:

```text
B2B SaaS companies in US with 50–500 employees
that are hiring sales people
```

into structured criteria:

```json
{
  "business_model": "B2B SaaS",
  "locations": ["US"],
  "employees": {
    "min": 50,
    "max": 500
  },
  "signals": [
    "sales hiring"
  ]
}
```

### Task B — Evidence extraction

Give the model retrieved text and ask:

```text
Extract only claims supported by the supplied evidence.
Return:
- claim
- evidence
- source URL
- confidence
```

### Task C — Qualification

Example:

```text
Does this company match the ICP?

Return:
- score: 0–100
- matched criteria
- failed criteria
- uncertain criteria
- evidence IDs
```

### Task D — Outreach angle

Only generate an outreach angle from verified evidence.

Never let the model invent:

- funding
- employee count
- technology
- customer names
- business problems
- job openings
- personal details

---

# 6. Lead Scoring

Use a transparent score instead of a black-box "AI says this is good."

Suggested MVP score:

```text
ICP Match             30 points
Company Size          15 points
Industry Match        15 points
Intent/Growth Signals 20 points
Pain Signal           10 points
Contact Availability  10 points
--------------------------------
Total                 100 points
```

Example:

```text
Company: Acme

ICP match             28/30
Company size          13/15
Industry              15/15
Growth signals        18/20
Pain signal            8/10
Contact availability  10/10
--------------------------------
Score                 92/100
```

### Critical rule

Every score should have an explanation.

Bad:

```text
AI score: 92
```

Good:

```text
92/100

Evidence:
- 100–200 employees
- B2B SaaS
- Hiring 4 customer-support roles
- Recently launched enterprise plan
- Support-heavy product
```

---

# 7. Evidence Model

This is one of the most important parts of the product.

Store evidence separately.

Suggested schema:

```text
companies
---------
id
name
domain
industry
employee_range
location
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
type
claim
source_url
source_title
retrieved_at
confidence
raw_text_hash

scores
------
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

This gives us:

- traceability
- reproducibility
- debugging
- easier scoring changes
- better user trust

---

# 8. Deduplication

This will become a real technical problem.

The same company can appear as:

```text
Acme Inc.
Acme
Acme Technologies
acme.com
www.acme.com
```

Use:

### Primary identity

```text
normalized_domain
```

### Secondary identity

```text
normalized_company_name + country
```

### Contact identity

```text
normalized_email
```

Do not rely only on company names.

---

# 9. Caching and Cost Control

The system should avoid repeatedly researching the same company.

Use:

```text
domain → research cache
URL → extraction cache
company → enrichment cache
```

Example:

```text
User searches ICP #1
      ↓
Research Acme
      ↓
Cache Acme research

User searches ICP #2
      ↓
Acme appears again
      ↓
Reuse cached evidence
      ↓
Only recalculate ICP score
```

This can reduce API costs dramatically.

---

# 10. Estimated MVP API Cost

These are **illustrative estimates**, not vendor quotes for the entire workflow.

For 100 companies:

### Web research

Suppose:

```text
2 searches/company
1 extraction/company
```

At roughly 3 basic Tavily credits/company:

```text
100 × 3 = 300 credits
```

At $0.008/credit:

```text
≈ $2.40
```

Actual cost will depend on search depth, extraction depth and how many URLs are processed.

### Contact enrichment

If we attempt one Hunter email lookup for 100 qualified contacts:

```text
≈ 100 search credits
```

Hunter's paid plans currently include substantially more credits than this, while its free tier can be useful for initial testing.

### LLM

Use a small/cost-efficient model for:

- classification
- extraction
- scoring
- summarisation

Do not use a large model for every page.

Use the larger model only when the reasoning task genuinely requires it.

---

# 11. Cost Optimization Strategy

The order of operations matters.

### Expensive approach

```text
1000 companies
 ↓
LLM research
 ↓
email enrichment
 ↓
deep research
 ↓
scoring
```

### Better approach

```text
1000 discovered companies
 ↓
cheap deterministic filters
 ↓
200 companies
 ↓
web research
 ↓
100 qualified companies
 ↓
contact enrichment
 ↓
top 25
 ↓
deep research + outreach
```

The system should use **progressive enrichment**.

---

# 12. API Rate Limits

Every external provider should sit behind a provider abstraction.

Example:

```python
class SearchProvider:
    def search(self, query):
        ...

class EnrichmentProvider:
    def find_email(self, name, domain):
        ...
```

Then:

```text
Tavily
   ↓
SearchProvider

Exa
   ↓
SearchProvider
```

This prevents the application from becoming permanently coupled to one provider.

Implement:

- retries
- exponential backoff
- timeout
- rate limiting
- caching
- circuit breaking
- provider fallback
- request logging

Never retry a failed API request infinitely.

---

# 13. Legal / Data-Access Risks

This is one of the biggest risks.

The product will process both:

### Company data

Usually lower risk.

Examples:

- company name
- website
- industry
- public company information

### Personal data

Higher risk.

Examples:

- person's name
- professional email
- phone number
- job title
- social profile
- other identifiers

The team must understand the privacy requirements for the markets in which the product operates.

India's Digital Personal Data Protection Act, 2023 provides the statutory framework for processing digital personal data, and the Digital Personal Data Protection Rules, 2025 were notified in November 2025 with staged commencement provisions.

Do not treat "publicly visible on the internet" as automatically meaning "free to use for every purpose."

For the MVP:

- prefer licensed APIs
- store source/provenance
- minimize personal data
- avoid unnecessary phone numbers
- support deletion
- support correction
- keep retention limited
- document data providers
- provide a clear privacy policy before production launch
- do not scrape sites that prohibit automated access

Sources:

https://www.indiacode.nic.in/handle/123456789/22037

https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa

---

# 14. Major Technical Risks

| Risk | Probability | Impact | Mitigation |
|---|---:|---:|---|
| Search results are noisy | High | Medium | Multiple queries + domain filtering |
| AI hallucination | High | High | Evidence-grounded extraction |
| Duplicate companies | High | Medium | Domain-based identity |
| Stale company data | High | Medium | Retrieval timestamp + refresh |
| Email unavailable | Medium | Medium | Hunter + generic company contact |
| API rate limits | Medium | Medium | Queue + backoff + caching |
| API provider changes | Medium | High | Provider abstraction |
| Data licensing restrictions | Medium | High | Licensed APIs + legal review |
| LinkedIn access restrictions | High | High | Do not scrape LinkedIn |
| Research becomes expensive | Medium | High | Progressive enrichment |
| Incorrect lead scoring | Medium | High | Explainable score + human review |
| Personal-data compliance | Medium | High | Data minimization + privacy controls |

---

# 15. Build Difficulty

### Overall MVP difficulty: **7/10**

Not because the individual APIs are difficult.

The hard part is making the entire pipeline reliable.

### Individual components

| Component | Difficulty |
|---|---:|
| ICP form | 2/10 |
| Search integration | 3/10 |
| Website extraction | 4/10 |
| Company normalization | 5/10 |
| Evidence storage | 4/10 |
| AI extraction | 5/10 |
| Lead scoring | 4/10 |
| Email enrichment | 3/10 |
| Dashboard | 5/10 |
| Async pipeline | 6/10 |
| Data quality | 8/10 |
| Compliance/data licensing | 8/10 |

---

# 16. Recommended MVP Scope

## MUST HAVE

- [ ] ICP input
- [ ] Company discovery
- [ ] Company deduplication
- [ ] Website research
- [ ] Evidence extraction
- [ ] Explainable lead score
- [ ] Ranked prospect list
- [ ] Research brief
- [ ] Email/contact enrichment for qualified prospects
- [ ] Personalised outreach draft
- [ ] Source URLs for every important claim

## SHOULD HAVE

- [ ] Job-posting signals
- [ ] News/growth signals
- [ ] Research caching
- [ ] Export to CSV
- [ ] Provider fallback
- [ ] Refresh/re-research button

## DO NOT BUILD YET

- [ ] Automated cold-email sending
- [ ] Email sequences
- [ ] LinkedIn automation
- [ ] CRM integrations
- [ ] Autonomous browser agents
- [ ] Huge proprietary lead database
- [ ] Complex multi-agent architecture
- [ ] Fine-tuned model
- [ ] Custom vector database
- [ ] Mobile application

The product should prove **lead quality**, not automation breadth.

---

# 17. Proposed Backend Architecture

```text
                    ┌──────────────────┐
                    │     Next.js      │
                    │    Dashboard     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    FastAPI       │
                    │   API Gateway    │
                    └────────┬─────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
       ┌──────────┐    ┌──────────┐    ┌────────────┐
       │ Discovery│    │ Research │    │ Enrichment │
       │ Service  │    │ Service  │    │  Service   │
       └────┬─────┘    └────┬─────┘    └─────┬──────┘
            │               │                 │
            ▼               ▼                 ▼
         Tavily          Tavily/Exa         Hunter
         /Exa
             \              |                /
              \             |               /
               └────────────┼───────────────┘
                            ▼
                    ┌──────────────────┐
                    │  Qualification   │
                    │   + Scoring      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │ companies        │
                    │ prospects        │
                    │ evidence         │
                    │ scores           │
                    └──────────────────┘
```

---

# 18. Suggested Repository Structure

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
│   ├── discovery/
│   ├── scoring/
│   └── enrichment/
│
└── README.md
```

---

# 19. Provider Abstraction

Do this from day one.

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

The application should not contain code like:

```python
if tavily:
    ...
```

throughout the entire codebase.

Instead:

```python
research_provider.search(...)
```

This makes future provider replacement much easier.

---

# 20. Validation Experiment Before Full Build

Before implementing the entire product, run one controlled experiment.

### Test set

Take **50 real companies** from the target ICP.

Have the team manually label:

```text
GOOD
MAYBE
BAD
```

Then run the automated pipeline.

Measure:

### Precision@10

Of the top 10 AI-ranked prospects, how many are actually good?

```text
Precision@10 =
good top-10 prospects / 10
```

### Evidence accuracy

For each generated claim:

```text
Supported
Unsupported
Partially supported
```

### Contact success rate

```text
valid work emails / requested emails
```

### Research cost

```text
total API cost / qualified company
```

### Time saved

Compare:

```text
manual research time
vs
AI-assisted research time
```

This experiment will tell us whether the product is actually useful.

---

# 21. MVP Success Threshold

For the first prototype, target:

```text
≥ 70% Precision@10
≥ 90% evidence-supported claims
≥ 60% successful contact enrichment
≥ 50% reduction in manual research time
```

These are **internal engineering targets**, not guaranteed industry benchmarks.

If the system cannot hit these numbers on a controlled test set, adding more features is the wrong move.

Fix data quality first.

---

# 22. Final Technical Verdict

## Can we build it?

**Yes.**

The required building blocks already exist:

```text
Company discovery       → available
Web research            → available
Website extraction      → available
Contact enrichment      → available
LLM qualification       → available
Scoring                 → straightforward
Database                → straightforward
Dashboard               → straightforward
```

The difficult part is **data quality, evidence grounding, provider licensing, and cost control**, not AI model training.

### Recommended first implementation

```text
Tavily
  +
Hunter
  +
SEC/public sources where applicable
  +
GPT-5 mini
  +
PostgreSQL
  +
FastAPI
  +
Next.js
```

### Strategic principle

> **Do not build a database of everyone. Build a system that explains why a small number of companies are worth talking to.**

That is the strongest technical interpretation of the current Solutionists MVP hypothesis.

---

# Sources

- [Tavily Pricing](https://www.tavily.com/pricing)
- [Tavily API Credits](https://docs.tavily.com/documentation/api-credits)
- [Exa Pricing](https://exa.ai/pricing)
- [Hunter API Documentation](https://hunter.io/api-documentation)
- [Hunter API for Data Plans](https://help.hunter.io/en/articles/12149400-hunter-api-for-data-plans)
- [Hunter Pricing](https://hunter.io/pricing)
- [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [Google Maps India Pricing](https://developers.google.com/maps/billing-and-pricing/pricing-india)
- [Apollo API Terms](https://www.apollo.io/terms/api)
- [Apollo Developer FAQ](https://docs.apollo.io/docs/developer-faqs)
- [Apollo API Pricing](https://docs.apollo.io/docs/api-pricing)
- [LinkedIn User Agreement](https://www.linkedin.com/legal/user-agreement)
- [LinkedIn Crawling Terms](https://www.linkedin.com/legal/crawling-terms)
- [India DPDP Act, 2023](https://www.indiacode.nic.in/handle/123456789/22037)
- [MeitY — DPDP Rules 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa)
