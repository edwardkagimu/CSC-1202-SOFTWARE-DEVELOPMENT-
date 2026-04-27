import { useState } from "react";
import axiosInstance from "../../api/axiosInstance";

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
    <div style={{ padding: "20px" }}>
      <h2>Create Weekly Log</h2>

      <input
        type="number"
        placeholder="Week Number"
        onChange={(e) => setWeek(e.target.value)}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Activities"
        onChange={(e) => setActivities(e.target.value)}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Challenges"
        onChange={(e) => setChallenges(e.target.value)}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Skills Learned"
        onChange={(e) => setSkills(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSubmit}>Save Log</button>
    </div>
  );
}