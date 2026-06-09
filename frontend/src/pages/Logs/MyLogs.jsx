import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";
import "../../App.css";
export default function MyLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await axiosInstance.get("weekly-log/");
      console.log("LOGS:", res.data);
      setLogs(res.data);
    } catch (err) {
      console.log("ERROR FETCHING LOGS:", err.response?.data || err);
    }
  };

  const submitLog = async (id) => {
    try {
      await axiosInstance.patch(`submit-log/${id}/`);
      alert("Log submitted successfully");

      fetchLogs(); // refresh after submit
    } catch (err) {
      console.log("SUBMIT ERROR:", err.response?.data || err);
      alert("Error submitting log");
    }
  };

  const deleteLog = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this log?");
    if (!confirmDelete) return;

    try {await axiosInstance.delete(`delete-log/${id}/`);
      alert("Log deleted successfully");

      fetchLogs(); // refresh list
    } catch (err) {
      console.log("DELETE ERROR:", err.response?.data || err);
      alert("Error deleting log");
    }
  };

  return (
    <div style={{ padding: "20px", margin: "auto" }}>
      <h2 className="mylogs-title" >My Weekly Logs</h2>

      {logs.length === 0 ? (
        <p className="empty ">No logs found</p>
      ) : (
        logs.map((log) => (
          <div
            key={log.id}
            style={{
              border: "1px solid #ccc",
              margin: "10px",
              padding: "20px",
              background: "#fff",
            }}
          >
            <h4>Week {log.week_number}</h4>

            <p className="log-detail"><strong>Activities:</strong> {log.activities}</p>
            <p className="log-detail" ><strong>Challenges:</strong> {log.challenges}</p>
            <p className="log-detail" ><strong>Skills:</strong> {log.skills_learned}</p>

            <p>
              <b>Status:</b>{" "}
              <span style={{ color: log.status === "draft" ? "orange" : "green" }}>
                {log.status}
              </span>
            </p>

            {/*ONLY SHOW SUBMIT BUTTON FOR DRAFT */}
            {log.status === "draft" && (
              <>
              <button onClick={() => submitLog(log.id)}>
                Submit
              </button>
              </>
            )}

            {/*ONLY SHOW delete BUTTON FOR DRAFT */}
            {(log.status === "draft" || log.status === "submitted") && (
              <>

              <button onClick={() => deleteLog(log.id)}
                      style={{marginLeft: "10px",color:"red"}}
              > Delete

              </button>
              </>
            )}            
            
          </div>
        ))
      )}
    </div>
  );
}