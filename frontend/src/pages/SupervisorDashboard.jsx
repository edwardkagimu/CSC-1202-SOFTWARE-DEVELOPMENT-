import { useNavigate } from "react-router-dom";
export default function SupervisorDashboard({ stats, user }) {
  const navigate = useNavigate();
  return (
    <div style={{ padding: "20px" }}>
      <h1>Supervisor Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div>
        <p>Pending Logs: {stats.pending_logs}</p>
        <p>Reviewed Logs: {stats.reviewed_logs}</p>
        <p>Evaluated Students: {stats.evaluated_students}</p>
      </div>
      
      <button onClick={() => navigate("/workplace/logs")}>Review Logs</button>
      <button onClick={() => navigate("/workplace-students") }>Assigned Students</button>
    </div>
  );
}