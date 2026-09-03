export const dynamic = "force-dynamic";

const AGENTS = [
  {
    key: "market_research",
    name: "Market Research Agent",
    desc: "Indian honey market, segments, cities, and trends.",
  },
  {
    key: "buyer_discovery",
    name: "Buyer Discovery Agent",
    desc: "Find importers, distributors, retailers, manufacturers.",
  },
  {
    key: "company_intelligence",
    name: "Company Intelligence Agent",
    desc: "Investigate an individual company and its strategic fit.",
  },
  {
    key: "trade_intelligence",
    name: "Trade Intelligence Agent",
    desc: "Import/export data, HS codes, volumes, pricing.",
  },
  {
    key: "regulatory",
    name: "Regulatory Agent",
    desc: "Indian import requirements, certifications, labelling.",
  },
  {
    key: "competitive_intelligence",
    name: "Competitive Intelligence Agent",
    desc: "Competing exporters, positioning, distribution.",
  },
  {
    key: "revenue",
    name: "Revenue Agent",
    desc: "Who to sell to, why, and what to do next.",
  },
  {
    key: "monitoring",
    name: "Monitoring Agent",
    desc: "Continuous watch for market and competitor changes.",
  },
];

export default async function IntelligencePage() {
  return (
    <>
      <h1 className="page-title">Intelligence</h1>
      <p className="page-subtitle">
        Specialised research agents that investigate the Indian honey market and
        NZ exporters. Each finding is evidence-backed.
      </p>

      <div className="grid grid-2">
        {AGENTS.map((agent) => (
          <div key={agent.key} className="card">
            <h3 style={{ marginBottom: 6 }}>{agent.name}</h3>
            <p className="page-subtitle" style={{ marginBottom: 0 }}>
              {agent.desc}
            </p>
            <span className="badge">{agent.key}</span>
          </div>
        ))}
      </div>
    </>
  );
}
