import { useNavigate } from "react-router-dom";

export default function AdminDashboard({ stats, user }) {
  const navigate = useNavigate();
  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div>
        <p>Students: {stats.students}</p>
        <p>Total Logs: {stats.total_logs}</p>
        <p>Submitted Logs: {stats.submitted_logs}</p>
        <p>Reviewed Logs: {stats.reviewed_logs}</p>
        <p>Approved Logs: {stats.approved_logs}</p>
        <p>Workplace Evaluations:{" "}{stats.workplace_evaluations}</p>
      <p>Academic Evaluations:{" "}{stats.academic_evaluations}</p>
      </div>

      <button onClick={() => navigate("/assign-placement")} >Assign Students</button>
      <button>Manage Users</button>
    </div>
  );
}