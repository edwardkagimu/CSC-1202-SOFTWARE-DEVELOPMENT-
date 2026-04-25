export default function AdminDashboard({ stats, user }) {
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

      <button>Assign Students</button>
      <button>Manage Users</button>
    </div>
  );
}