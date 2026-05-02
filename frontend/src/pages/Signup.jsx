import { useState } from "react";
import axiosInstance, { ENDPOINTS } from "../api/axiosInstance";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [reg_no,setReg_no] = useState("");

  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const res = await axiosInstance.post(ENDPOINTS.signup, {
        username,
        email,
        password,
        role,
        reg_no : role === "student" ? reg_no : null,
      });

      if (res.data) {
        alert("User created successfully");
        navigate("/login");
      }
    } catch (error) {
      console.log(error);
      alert("Signup failed");
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>

      <input
        placeholder="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        value={password}
        placeholder="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="student">Student</option>
        <option value="workplace_supervisor">Workplace Supervisor</option>
        <option value="academic_supervisor">Academic Supervisor</option>
      </select>

      {role === "student" && (
        <input
          placeholder="Registration Number"
          value={reg_no}
          onChange={(e) => setReg_no(e.target.value)}
        />
      )}

      <button onClick={handleSignup}>Sign Up</button>
      <p>Already have account?{" "}<Link to="/login">Login</Link></p>
    </div>
  );
}