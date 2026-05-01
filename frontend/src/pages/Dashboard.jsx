import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import axiosInstance, { ENDPOINTS } from "../api/axiosInstance";

import StudentDashboard from "./StudentDashboard";
import SupervisorDashboard from "./SupervisorDashboard";
import AcademicDashboard from "./AcademicDashboard";
import AdminDashboard from "./AdminDashboard";

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

  //loading state
  if (!userInfo) return <p>Loading...</p>;

  const role = userInfo.role;

  let content;

  if (role === "student") {
    content = <StudentDashboard stats={stats} user={userInfo} />;
  } else if (role === "workplace_supervisor") {
    content = <SupervisorDashboard stats={stats} user={userInfo} />;
  } else if (role === "academic_supervisor") {
    content = <AcademicDashboard stats={stats} user={userInfo} />;
  } else if (role === "admin") {
    content = <AdminDashboard stats={stats} user={userInfo} />;
  } else {
    content = <p>No role found</p>;
  }


  return (
   <div style={{ padding: "20px" }}>
      
      {/*  HEADER */}
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <h2>Internship Learning Evaluation System (ILES) </h2>
          <p>
             <b>Welcome back, {user?.username}</b>
          </p>
        </div>

       
      </div>

      <hr />

      {/* ROLE-BASED DASHBOARD */}
      {content}  
      <button onClick={logout}>Logout</button>

    </div>
  );
}