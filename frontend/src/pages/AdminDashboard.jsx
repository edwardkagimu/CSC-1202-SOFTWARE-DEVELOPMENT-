import { useNavigate } from "react-router-dom";
import "../App.css";

export default function AdminDashboard({ stats, user }) {
  const navigate = useNavigate();
  const totalLogs =
    stats.total_logs || 0;

  const submittedPct =
    totalLogs > 0
      ? (stats.submitted_logs / totalLogs) * 100
      : 0;

  const approvedPct =
    totalLogs > 0
      ? (stats.approved_logs / totalLogs) * 100
      : 0;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
       <h1>Admin Dashboard</h1>
       <p>Welcome, {user.username}</p>
      </div> 

      <div className="stats-container">
        <div className="card"><h3>Students</h3><p>{stats.students}</p></div>
        <div className="card"><h3>Total Logs</h3><p>{stats.total_logs}</p></div>
        <div className="card"><h3>Submitted Logs</h3><p>{stats.submitted_logs}</p></div>
        <div className="card"><h3>Reviewed Logs</h3><p>{stats.reviewed_logs}</p></div>
        <div className="card"><h3>Approved Logs</h3><p>{stats.approved_logs}</p></div>
      </div>

      <div className="panel">

        <h2>Log Processing Flow</h2>

        <div className="flow-item">
          <div className="flow-label">Submitted</div>
          <div className="progress-bar">
            <div
              className="progress-fill blue"
              style={{ width: `${submittedPct}%` }}
            />
          </div>
          <span>{submittedPct.toFixed(0)}%</span>
        </div>

        <div className="flow-item">
          <div className="flow-label">Approved</div>
          <div className="progress-bar">
            <div
              className="progress-fill green"
              style={{ width: `${approvedPct}%` }}
            />
          </div>
          <span>{approvedPct.toFixed(0)}%</span>
        </div>

      </div>

      <div className="panel">

        <h2>Evaluations Overview</h2>

        <div className="eval-grid">

          <div className="eval-box purple">
            <h3>Workplace</h3>
            <p>{stats.workplace_evaluations}</p>
          </div>

          <div className="eval-box orange">
            <h3>Academic</h3>
            <p>{stats.academic_evaluations}</p>
          </div>

        </div>
      </div>

      <div className="actions-section">
       <div className="button-group">
         <button  className="action-btn" onClick={() => navigate("/assign-placement")} >Assign Students</button>
         <button  className="action-btn" onClick={() => navigate("/manage-users")}>Manage Users</button>
       </div>
      </div>
    </div>
  );
}