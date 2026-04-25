export default function AcademicDashboard({ stats, user }) {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Academic Dashboard</h1>

      <p>Welcome, {user.username}</p>

      <div>
        <p>Pending Approval: {stats.pending_logs}</p>
        <p>Approved Logs: {stats.approved_logs}</p>
      </div>

      <button>Approve Logs</button>
    </div>
  );
}