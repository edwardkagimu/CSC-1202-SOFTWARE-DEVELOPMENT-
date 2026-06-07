import { useNavigate } from "react-router-dom";
import "../App.css"
export default function SupervisorDashboard({ stats, user }) {
  const navigate = useNavigate();
  const totalLogs = stats.pending_logs + stats.reviewed_logs;

  const percentage =
    totalLogs > 0
      ? (stats.reviewed_logs / totalLogs) * 100
      : 0;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Supervisor Dashboard</h1>
        <p>Welcome, {user.username}</p>
      </div>
      <div className="stats-container">
        <div className="card">
         <h3>Pending Logs</h3>
         <p>{stats.pending_logs}</p>
        </div>

        <div className="card">
        <h3>Reviewed Logs</h3>
        <p>{stats.reviewed_logs}</p>
        </div>

        <div className="card">
         <h3>Evaluated Students</h3>
         <p>{stats.evaluated_students}</p>
        </div>

        <div className="progress-section">
         <h2>Log Review Progress</h2>

         <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${percentage}%` }}
          ></div>
         </div>

         <p>{percentage.toFixed(0)}% Reviewed</p>
        </div>
      </div>

      <div className="actions-section">
        <div className="button-group">
          <button className="action-btn" onClick={() => navigate("/workplace/logs")}>Review Logs</button>
          <button className="action-btn" onClick={() => navigate("/workplace-students") }>Assigned Students</button>
        </div>
      </div>
    </div>
  );
}