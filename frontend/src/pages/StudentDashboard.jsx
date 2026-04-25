export default function StudentDashboard({ stats, user }) {
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

      <button>Create Log</button>
      <button>View Logs</button>
      <button>Submit Log</button>
    </div>
  );
}