import { useNavigate } from "react-router-dom";
export default function AcademicDashboard({ stats, user }) {
  const navigate = useNavigate();
  return (
    <div style={{ padding: "20px" }}>
      <h1>Academic Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div>
        <p>Pending Approval: {stats.pending_logs}</p>
        <p>Approved Logs: {stats.approved_logs}</p>
      </div>

      <button onClick={() => navigate("/academic/logs")}>Approve Logs</button>
    </div>
  );
}