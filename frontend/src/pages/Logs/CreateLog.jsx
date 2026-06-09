import { useState } from "react";
import axiosInstance from "../../api/axiosInstance";
import "../../App.css";
export default function CreateLog() {
  const [week, setWeek] = useState("");
  const [activities, setActivities] = useState("");
  const [challenges, setChallenges] = useState("");
  const [skills, setSkills] = useState("");

  const handleSubmit = async () => {
    console.log("BUTTON CLICKED");
    if (!week || !activities || !challenges || !skills ) {
      alert("All fields are required");
      return;
    }

    try {
      await axiosInstance.post("weekly-log/", {
        week_number: Number(week),
        activities,
        challenges,
        skills_learned: skills,
      });

      alert("Log created successfully");
      window.location.href = "/dashboard"; // force refresh
    } catch (err) {
      console.log("FULL ERROR:", err);
      console.log("RESPONSE:", err.response);
      console.log("DATA:", err.response?.data);

      alert(JSON.stringify(err.response?.data));  
      console.log(err.response?.data || err);
      alert("Error creating log");
    }
  };

  return (
    <div className="create-log-container">
      <h2 className="mylogs-title">Create Weekly Log</h2>
      <div className="form-group">
        <input
          className="form-input"
          type="number"
          placeholder="Week Number"
          onChange={(e) => setWeek(e.target.value)}
        />
      </div>
      
      <div className="form-group">
        <input
          className="form-input"
          type="text"
          placeholder="Activities"
          onChange={(e) => setActivities(e.target.value)}
        />
      </div> 
      
      <div className="form-group">
        <input
         className="form-input"
         type="text"
         placeholder="Challenges"
         onChange={(e) => setChallenges(e.target.value)}
        />
      </div>
      
      <div className="form-group">
       <input
         className="form-input"
         type="text"
         placeholder="Skills Learned"
         onChange={(e) => setSkills(e.target.value)}
       />
      </div>

      <button className="save-btn" onClick={handleSubmit}>Save Log</button>
    </div>
  );
}