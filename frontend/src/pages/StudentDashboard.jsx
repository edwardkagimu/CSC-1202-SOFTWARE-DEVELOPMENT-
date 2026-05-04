import { useNavigate } from "react-router-dom";

export default function StudentDashboard({ stats, user }) {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "20px" }}>
      <h1>Student Dashboard</h1>

      <p>Welcome, {user.username}</p>       <p>Registration No: {user.reg_no}</p>

      <hr/>

      <div style={{ display: "flex", gap: "10px" ,flexWrap: "wrap"}}>
        <div>Total Logs: {stats.logs}</div>
        <div>Draft: {stats.draft}</div>
        <div>Reviewed: {stats.reviewed}</div>
        <div>Approved: {stats.approved_logs}</div>
        
      </div>

      <hr />
      
      <h3>Evaluation Scores</h3>

       <p>
        Workplace Score:
        {" "}
        {stats.workplace_score}
      </p>

      <p>
        Academic Score:
        {" "}
        {stats.academic_score}
      </p>

      <p>
        <b>
          Final Score:
          {" "}
          {stats.final_score}
        </b>
      </p>

      <hr />

      <button onClick={() => navigate("/create-log")}> Weekly Log</button>
      <button onClick={() => navigate("/my-logs")}>View Logs</button>
      
    </div>
  );
}