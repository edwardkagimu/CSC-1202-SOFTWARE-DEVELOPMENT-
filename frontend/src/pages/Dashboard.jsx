import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import axiosInstance, { ENDPOINTS } from "../api/axiosInstance";

export default function Dashboard() {
  const { user, logout } = useContext(AuthContext);
  const [stats, setStats] = useState({});
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const res = await axiosInstance.get(ENDPOINTS.dashboard);

      console.log("DASHBOARD DATA:", res.data); 
      console.log("USER FROM CONTEXT:", user);
      
      setUserInfo(res.data.user);
      setStats(res.data.data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Dashboard</h1>

      <p>Welcome, {userInfo?.username}</p>
      <p>Role: {userInfo?.role}</p>


      <hr />

      <h2></h2>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
        {Object.entries(stats).map(([key, value], index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ccc",
              padding: "15px",
              minWidth: "150px"
            }}
          >
            <h4>{key.replace("_", " ")}</h4>
            <p>
              {typeof value === "object"
                ? JSON.stringify(value)
                : value}  
            </p>
          </div>
        ))}
      </div>
      <br></br>
      <button onClick={logout}>Logout</button>
    </div>
  );
}