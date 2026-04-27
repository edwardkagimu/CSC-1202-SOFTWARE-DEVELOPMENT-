import { useNavigate } from "react-router-dom";

export default function StudentDashboard({ stats, user }) {
  const navigate = useNavigate();
  return (
    <div style={{ padding: "20px" }}>
      <h1>Student Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div style={{ display: "flex", gap: "10px" }}>
        <div>Total Logs: {stats.logs}</div>
        <div>Draft: {stats.draft}</div>
        <div>Reviewed: {stats.reviewed}</div>
        <div>Approved: {stats.approved_logs}</div>
      </div>

      <hr />

      <button onClick={() => navigate("/create-log")}>Create Weekly Log</button>
      <button onClick={() => navigate("/my-logs")}>View Logs</button>
      <button>Submit Log</button>
    </div>
  );
}