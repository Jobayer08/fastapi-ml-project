import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [result, setResult] = useState("");

  // 🔐 Login Function
  const login = async () => {
    try {
      const res = await axios.post(
        "https://fastapi-ml-project-gu9k.onrender.com/login",
        new URLSearchParams({
          username: username,
          password: password,
        })
      );

      setToken(res.data.access_token);
      alert("✅ Login Successful");

    } catch (err) {
      alert("❌ Login Failed");
    }
  };

  // 🤖 Prediction Function
  const predict = async () => {
    try {
      const res = await axios.post(
        "https://fastapi-ml-project-gu9k.onrender.com/predict",
        {
          study_hours: 6,
          attendance: 70,
          previous_score: 60
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setResult(res.data.prediction);

    } catch (err) {
      alert("❌ Prediction Failed (Login first)");
    }
  };

  return (
    <div style={{ padding: 30, textAlign: "center" }}>

      <h1>🚀 Student Prediction App</h1>

      {/* 🔐 Login Section */}
      <h2>Login</h2>

      <input
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <br /><br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <br /><br />

      <button onClick={login}>Login</button>

      <p><b>Token:</b> {token}</p>

      <hr />

      {/* 🤖 Prediction Section */}
      <h2>Prediction</h2>

      <button onClick={predict}>Predict</button>

      <p><b>Result:</b> {result}</p>

    </div>
  );
}

export default App;