import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";
import { useNavigate } from "react-router-dom";

export default function WorkplaceLogs() {
  const [logs, setLogs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await axiosInstance.get("workplace_supervisor/logs/");
      console.log("FULL RESPONSE:", res.data); // for debug
      setLogs(res.data);
      
    } catch (err) {
      console.log("FETCH ERROR:", err.response?.data || err);
    }
  };

  const confirmReview = async (id) => {
    try {
      await axiosInstance.patch(`supervisor/${id}/approve/`);
      alert("Log reviewed successfully");

      fetchLogs(); // refresh
    } catch (err) {
      console.log("REVIEW ERROR:", err.response?.data || err);
      alert("Error reviewing log");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Submitted Logs (Workplace)</h2>

      {logs.length === 0 ? (
        <p>No logs to review</p>
      ) : (
        logs.map((log) => (
          <div key={log.id} style={{ border: "1px solid #ccc", padding: "10px", margin: "10px" }}>
            <h4>Week {log.week_number}</h4>
 
            <p><b>Name: </b>{log.student_username}</p>
            <p><b>Reg No:</b> {log.student_reg_no}</p>

            <p><b>Activities:</b> {log.activities}</p>
            <p><b>Challenges:</b> {log.challenges}</p>
            <p><b>Skills:</b> {log.skills_learned}</p>

            <button onClick={() => navigate(`/workplace-evaluation/${log.placement_id}`)}>
             Evaluate Intern
            </button>
            <button onClick={() => confirmReview(log.id)}>
              Confirm Review
            </button>

          </div>
        ))
      )}
    </div>
  );
}