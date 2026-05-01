import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";
import { useNavigate } from "react-router-dom";
export default function AcademicLogs() {
  const [logs, setLogs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await axiosInstance.get("academic_supervisor/logs/");
      setLogs(res.data);
    } catch (err) {
      console.log("FETCH ERROR:", err.response?.data || err);
    }
  };

  const confirmApproval = async (id) => {
    try {
      await axiosInstance.patch(`supervisor/${id}/approve/`);
      alert("Log approved successfully");

      fetchLogs();
    } catch (err) {
      console.log("APPROVAL ERROR:", err.response?.data || err);
      alert("Error approving log");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Reviewed Logs (Academic)</h2>

      {logs.length === 0 ? (
        <p>No logs to approve</p>
      ) : (
        logs.map((log) => (
          <div key={log.id} style={{ border: "1px solid #ccc", padding: "10px", margin: "10px" }}>
            <h4>Week {log.week_number}</h4>

            <p><b>Reg No:</b> {log.student_reg_no}</p>
            <p><b>Activities:</b> {log.activities}</p>
            <p><b>Challenges:</b> {log.challenges}</p>
            <p><b>Skills:</b> {log.skills_learned}</p>

            <button onClick={() => navigate(`/academic-evaluation/${log.placement_id}`)}>
             Evaluate 
            </button>            
            <button onClick={() => confirmApproval(log.id)}>
              Confirm Approval
            </button>
          </div>
        ))
      )}
    </div>
  );
}