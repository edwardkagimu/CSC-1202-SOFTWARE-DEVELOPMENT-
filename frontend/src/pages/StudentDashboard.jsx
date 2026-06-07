import { useNavigate } from "react-router-dom";
import "../App.css"

export default function StudentDashboard({ stats, user }) {
  const navigate = useNavigate();
  
  const finalScore = stats.final_score || 0;
  const workplace = stats.workplace_score || 0;
  const academic = stats.academic_score || 0;  

  return (
    <div className="dashboard-container" >
      <div className="dashboard-header">
       <h1>Student Dashboard</h1>
       <p>Welcome, {user.username}</p>       <p>Registration No: {user.reg_no}</p>
      </div>
      <hr/>

      <div  className="stats-container">
        <div className="card"><h3>Total Logs</h3><p>{stats.logs}</p></div>
        <div className="card"><h3>Draft</h3><p>{stats.draft}</p></div>
        <div className="card"><h3>Reviewed</h3><p>{stats.reviewed}</p></div>
        <div className="card"><h3>Approved</h3><p>{stats.approved_logs}</p></div>
        
      </div>

      <hr />
      
        <div className="panel">

        <h2>Evaluation Scores</h2>

        <div className="score-grid">

          {/* WORKPLACE */}
          <div className="score-card">
            <h3>Workplace Score</h3>
            <p>{workplace}%</p>
          </div>

          {/* ACADEMIC */}
          <div className="score-card">
            <h3>Academic Score</h3>
            <p>{academic}%</p>
          </div>
      
           {/* FINAL SCORE */}
          <div className="score-card final">
            <h3>Final Score</h3>
            <div className="big-score">{finalScore}</div>

            <div className="grade">
              {finalScore >= 75
                ? "Excellent "
                : finalScore >= 60
                ? "Good "
                : finalScore >= 50
                ? "Average "
                : "Needs Improvement "}
            </div>
          </div>

        </div>
      </div>

      <hr />
      <div className="actions-section">
        <div className="button-group">
          <button  className="action-btn" onClick={() => navigate("/create-log")}> Weekly Log</button>
          <button  className="action-btn" onClick={() => navigate("/my-logs")}>View Logs</button>
        </div>
      </div>
    </div>
  );
}