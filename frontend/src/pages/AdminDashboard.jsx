import { useNavigate } from "react-router-dom";

export default function AdminDashboard({ stats, user }) {
  const navigate = useNavigate();
  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div>
        <p>Total Students: {stats.students}</p>
        <p>Total Logs: {stats.total_logs}</p>
        <p>Approved Logs: {stats.approved_logs}</p>
        <p>Pending Logs: {stats.pending_logs}</p>
      </div>

      <button onClick={() => navigate("/assign-placement")} >Assign Students</button>
      <button>Manage Users</button>
    </div>
  );
}