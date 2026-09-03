import { api, HoneyCompany } from "../../../lib/api";

export const dynamic = "force-dynamic";

function scoreClass(score: number | null): string {
  if (score === null) return "score-low";
  if (score >= 60) return "score-high";
  if (score >= 30) return "score-mid";
  return "score-low";
}

export default async function HoneyCompaniesPage() {
  let companies: HoneyCompany[] = [];
  let error: string | null = null;
  try {
    companies = await api<HoneyCompany[]>("/honey-companies/");
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load";
  }

  return (
    <>
      <h1 className="page-title">NZ Honey Companies</h1>
      <p className="page-subtitle">
        The NZ Honey Company Universe — candidates for India market entry.
      </p>

      {error && <div className="card" style={{ marginBottom: 16, color: "#f06161" }}>{error}</div>}

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Type</th>
              <th>Region</th>
              <th>Tier</th>
              <th>India Fit</th>
            </tr>
          </thead>
          <tbody>
            {companies.map((c) => (
              <tr key={c.id}>
                <td>{c.name}</td>
                <td>{c.company_type || "—"}</td>
                <td>{c.region || "—"}</td>
                <td>{c.export_tier || "—"}</td>
                <td>
                  <span className={`score-pill ${scoreClass(c.india_fit_score)}`}>
                    {c.india_fit_score === null ? "n/a" : c.india_fit_score.toFixed(0)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
