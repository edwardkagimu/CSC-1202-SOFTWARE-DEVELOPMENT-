import { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";
import '../App.css';
export default function Login() {
  const { login } = useContext(AuthContext);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      await login({ username, password });
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">

        <h1 className="app-title">Internship Learning Evaluation System</h1>

        <h2 className="login-title">Login</h2>

        <input
         placeholder="username"
         onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="login-btn" onClick={handleLogin}>Login</button>

        <p>Don`t have account?{" "}<Link to="/signup">Sign up</Link></p>
        </div> 
    </div>
  );
}