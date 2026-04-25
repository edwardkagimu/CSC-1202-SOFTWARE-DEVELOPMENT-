export default function SupervisorDashboard({ stats, user }) {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Supervisor Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div>
        <p>Pending Logs: {stats.pending_logs}</p>
        <p>Reviewed Logs: {stats.reviewed_logs}</p>
      </div>

      <button>View Logs</button>
      <button>Review Logs</button>
    </div>
  );
}