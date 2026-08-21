import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboard() {
      try {
        // Get analytics data
        const summaryResponse = await fetch(
          `${API_URL}/analytics/summary`
        );

        if (!summaryResponse.ok) {
          throw new Error("Unable to load analytics summary");
        }

        const summaryData = await summaryResponse.json();

        // Get fraud alerts
        const alertsResponse = await fetch(
          `${API_URL}/alerts?limit=10`
        );

        if (!alertsResponse.ok) {
          throw new Error("Unable to load fraud alerts");
        }

        const alertsData = await alertsResponse.json();

        setSummary(summaryData);
        setAlerts(alertsData.alerts || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="status-message">
        Loading PayGuard AI...
      </div>
    );
  }

  if (error) {
    return (
      <div className="status-message error">
        {error}
      </div>
    );
  }

  return (
    <div className="dashboard">

      <header className="dashboard-header">

        <div>
          <h1>PayGuard AI</h1>
          <p>Fraud Intelligence Dashboard</p>
        </div>

        <div className="system-status">
          ● System Online
        </div>

      </header>


      <section className="metrics">

        <div className="card">
          <span>Total Transactions</span>

          <strong>
            {summary.total_transactions.toLocaleString()}
          </strong>
        </div>


        <div className="card">
          <span>Fraud Alerts</span>

          <strong>
            {summary.fraud_alerts.toLocaleString()}
          </strong>
        </div>


        <div className="card">
          <span>Fraud Rate</span>

          <strong>
            {summary.fraud_rate_percent}%
          </strong>
        </div>


        <div className="card">
          <span>Average Transaction</span>

          <strong>
            ${summary.average_transaction_amount.toLocaleString()}
          </strong>
        </div>

      </section>


      <section className="alerts-section">

        <div className="section-header">

          <div>
            <h2>Recent Fraud Alerts</h2>

            <p>
              Transactions requiring analyst attention
            </p>
          </div>

        </div>


        <div className="table-wrapper">

          <table>

            <thead>

              <tr>
                <th>Transaction</th>
                <th>Risk</th>
                <th>Score</th>
                <th>Amount</th>
                <th>Country</th>
                <th>Status</th>
              </tr>

            </thead>


            <tbody>

              {alerts.map((alert) => (

                <tr key={alert.alert_id}>

                  <td>
                    {alert.transaction_id}
                  </td>

                  <td>
                    <span
                      className={`risk ${
                        alert.risk_level.toLowerCase()
                      }`}
                    >
                      {alert.risk_level}
                    </span>
                  </td>

                  <td>
                    {alert.risk_score}
                  </td>

                  <td>
                    ${alert.amount.toLocaleString()}
                  </td>

                  <td>
                    {alert.country}
                  </td>

                  <td>
                    {alert.alert_status}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </section>

    </div>
  );
}

export default App;