import { useNavigate } from "react-router-dom";
import "../App.css"
export default function AcademicDashboard({ stats, user }) {
  const navigate = useNavigate();
  const totalLogs = stats.pending_logs + stats.approved_logs;
  const percentage = totalLogs > 0
    ? (stats.approved_logs / totalLogs) * 100
    : 0;
  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
       <h1>Academic Dashboard</h1>
       <p>Welcome, {user.username}</p>
      </div>

      <div className="stats-container">
        <div className="card">
          <h3>Pending Approval</h3>
          <p>{stats.pending_logs}</p>
        </div>

        <div className="card">
          <h3>Approved Logs</h3>
          <p>{stats.approved_logs}</p>
        </div>

        <div className="card">
          <h3>Evaluated Students</h3>
          <p>{stats.evaluated_students}</p>
        </div>

        <div className="progress-section">
         <h2>Log Approval Progress</h2>

         <div className="progress-bar">
           <div
             className="progress-fill"
             style={{ width: `${percentage}%` }}
           ></div>
         </div>
         <p>{percentage.toFixed(0)}% Approved</p>
        </div>
      </div>
      <div className="actions-section">
        <div className="button-group">
          <button className="action-btn" onClick={() => navigate("/academic/logs")}>Approve Logs</button>
          <button className="action-btn" onClick={() => navigate("/academic-students") }>Assigned Students</button>
        </div>
      </div>
    </div>
  );
}