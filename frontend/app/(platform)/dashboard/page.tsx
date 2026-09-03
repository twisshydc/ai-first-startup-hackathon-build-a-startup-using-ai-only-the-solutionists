import { api, HoneyCompany, IndianCompany, AgentRun } from "../../../lib/api";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  let honeyCompanies: HoneyCompany[] = [];
  let indianCompanies: IndianCompany[] = [];
  let agentRuns: AgentRun[] = [];
  let error: string | null = null;

  try {
    [honeyCompanies, indianCompanies, agentRuns] = await Promise.all([
      api<HoneyCompany[]>("/honey-companies/"),
      api<IndianCompany[]>("/indian-companies/"),
      api<AgentRun[]>("/research/runs"),
    ]);
  } catch (e) {
    error = e instanceof Error ? e.message : "Failed to load data";
  }

  return (
    <>
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">
        NZ → India honey trade intelligence. Understand what to know, decide who
        to pursue, then act.
      </p>

      {error && (
        <div className="card" style={{ marginBottom: 16, color: "#f06161" }}>
          {error}
        </div>
      )}

      <div className="grid grid-3" style={{ marginBottom: 28 }}>
        <div className="card">
          <div className="stat-label">NZ Honey Companies</div>
          <div className="stat-value">{honeyCompanies.length}</div>
        </div>
        <div className="card">
          <div className="stat-label">Indian Buyers</div>
          <div className="stat-value">{indianCompanies.length}</div>
        </div>
        <div className="card">
          <div className="stat-label">Agent Runs</div>
          <div className="stat-value">{agentRuns.length}</div>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h2 style={{ marginBottom: 12 }}>Get Started</h2>
          <ol style={{ paddingLeft: 18 }}>
            <li>Select your NZ honey company from the honey companies list.</li>
            <li>Run market and buyer research agents.</li>
            <li>Review evidence-backed intelligence.</li>
            <li>Generate personalised outreach for ranked buyers.</li>
          </ol>
        </div>
        <div className="card">
          <h2 style={{ marginBottom: 12 }}>Recent Agent Activity</h2>
          {agentRuns.length === 0 ? (
            <p className="page-subtitle">No agent runs yet.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Agent</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {agentRuns.slice(0, 8).map((run) => (
                  <tr key={run.id}>
                    <td>{run.agent_type}</td>
                    <td>
                      <span className={`badge`}>{run.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </>
  );
}
