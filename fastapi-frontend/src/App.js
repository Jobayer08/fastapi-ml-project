import React, { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {

  // 🔐 Auth States
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  // 🤖 Prediction States
  const [studyHours, setStudyHours] = useState("");
  const [attendance, setAttendance] = useState("");
  const [previousScore, setPreviousScore] = useState("");
  const [result, setResult] = useState("");

  const API = "https://fastapi-ml-project-gu9k.onrender.com";

  // 🔐 Register
  const register = async () => {
    if (!username || !password) {
      return alert("⚠️ Username & Password required");
    }

    try {
      await axios.post(`${API}/register`, { username, password });
      alert("✅ Registration Successful");
    } catch {
      alert("❌ Registration Failed");
    }
  };

  // 🔐 Login
  const login = async () => {
    if (!username || !password) {
      return alert("⚠️ Enter Username & Password");
    }

    try {
      const res = await axios.post(
        `${API}/login`,
        new URLSearchParams({ username, password })
      );

      setToken(res.data.access_token);
      alert("✅ Login Successful");
    } catch {
      alert("❌ Login Failed");
    }
  };

  // 🤖 Predict
  const predict = async () => {

    if (!token) {
      return alert("⚠️ Please login first");
    }

    if (!studyHours || !attendance || !previousScore) {
      return alert("⚠️ সব input fill করো");
    }

    try {
      const res = await axios.post(
        `${API}/predict`,
        {
          study_hours: Number(studyHours),
          attendance: Number(attendance),
          previous_score: Number(previousScore),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResult(res.data.prediction);

    } catch {
      alert("❌ Prediction Failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">

      <div className="grid md:grid-cols-2 gap-6 w-full max-w-5xl p-6">

        {/* 🔐 AUTH CARD */}
        <div className="bg-white p-6 rounded-2xl shadow-lg">

          <h2 className="text-xl font-bold mb-4 text-center">
            🔐 Authentication
          </h2>

          <input
            className="w-full p-2 border rounded mb-3"
            placeholder="Username"
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            className="w-full p-2 border rounded mb-3"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <div className="flex gap-2">
            <button
              onClick={register}
              className="flex-1 bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Register
            </button>

            <button
              onClick={login}
              className="flex-1 bg-green-500 text-white p-2 rounded hover:bg-green-600"
            >
              Login
            </button>
          </div>

          <p className="text-xs mt-4 break-all text-gray-500">
            Token: {token}
          </p>
        </div>

        {/* 🤖 PREDICTION CARD */}
        <div className="bg-white p-6 rounded-2xl shadow-lg">

          <h2 className="text-xl font-bold mb-4 text-center">
            🤖 Prediction
          </h2>

          <input
            className="w-full p-2 border rounded mb-3"
            placeholder="Study Hours"
            onChange={(e) => setStudyHours(e.target.value)}
          />

          <input
            className="w-full p-2 border rounded mb-3"
            placeholder="Attendance (%)"
            onChange={(e) => setAttendance(e.target.value)}
          />

          <input
            className="w-full p-2 border rounded mb-3"
            placeholder="Previous Score"
            onChange={(e) => setPreviousScore(e.target.value)}
          />

          <button
            onClick={predict}
            className="w-full bg-purple-500 text-white p-2 rounded hover:bg-purple-600"
          >
            Predict
          </button>

          <div className="mt-5 text-center">
            <p className="text-lg font-semibold">Result:</p>
            <p className="text-2xl font-bold text-green-600">
              {result}
            </p>
          </div>

        </div>

      </div>
    </div>
  );
}