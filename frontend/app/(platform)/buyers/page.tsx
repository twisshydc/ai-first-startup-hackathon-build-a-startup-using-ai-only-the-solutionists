import { api, IndianCompany } from "../../../lib/api";

export const dynamic = "force-dynamic";

function scoreClass(score: number | null): string {
  if (score === null) return "score-low";
  if (score >= 60) return "score-high";
  if (score >= 30) return "score-mid";
  return "score-low";
}

export default async function BuyersPage() {
  let companies: IndianCompany[] = [];
  let error: string | null = null;
  try {
    companies = await api<IndianCompany[]>("/indian-companies/");
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load";
  }

  return (
    <>
      <h1 className="page-title">Indian Buyers</h1>
      <p className="page-subtitle">
        Importers, distributors, retailers, and manufacturers relevant to NZ honey.
      </p>

      {error && <div className="card" style={{ marginBottom: 16, color: "#f06161" }}>{error}</div>}

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Company</th>
              <th>Type</th>
              <th>City</th>
              <th>Buyer Score</th>
            </tr>
          </thead>
          <tbody>
            {companies.length === 0 ? (
              <tr>
                <td colSpan={4}>
                  No buyer companies yet. Run the buyer discovery agent to populate.
                </td>
              </tr>
            ) : (
              companies.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td>{c.company_type}</td>
                  <td>{c.city || "—"}</td>
                  <td>
                    <span className={`score-pill ${scoreClass(c.buyer_score)}`}>
                      {c.buyer_score === null ? "n/a" : c.buyer_score.toFixed(0)}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
