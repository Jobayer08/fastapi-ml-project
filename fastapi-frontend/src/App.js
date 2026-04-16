import React, { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const API = "https://fastapi-ml-project-gu9k.onrender.com";

  // 🔐 Auth
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  // 🤖 Student Form (ALL DATASET FIELDS)
  const [form, setForm] = useState({
    age: "",
    gender: "",
    location: "",
    family_size: "",
    mother_education: "",
    father_education: "",
    mother_job: "",
    father_job: "",
    guardian: "",
    parental_involvement: "",
    internet_access: "",
    studytime: "",
    tutoring: "",
    school_type: "",
    attendance: "",
    extra_curricular_activities: "",
    english: "",
    math: "",
    science: "",
    social_science: "",
    art_culture: "",
  });

  const [result, setResult] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // 🔐 Register
  const register = async () => {
    await axios.post(`${API}/register`, { username, password });
    alert("Registered ✅");
  };

  // 🔐 Login
  const login = async () => {
    const res = await axios.post(
      `${API}/login`,
      new URLSearchParams({ username, password })
    );
    setToken(res.data.access_token);
    alert("Login Success ✅");
  };

  // 🤖 Predict
  const predict = async () => {
    const payload = {
      ...form,
      age: Number(form.age),
      family_size: Number(form.family_size),
      studytime: Number(form.studytime),
      attendance: Number(form.attendance),
      english: Number(form.english),
      math: Number(form.math),
      science: Number(form.science),
      social_science: Number(form.social_science),
      art_culture: Number(form.art_culture),
    };

    const res = await axios.post(`${API}/predict`, payload, {
      headers: { Authorization: `Bearer ${token}` },
    });

    setResult(res.data.predicted_group);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        🎓 Student Group Prediction
      </h1>

      {/* AUTH */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="font-bold mb-2">Authentication</h2>
        <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} className="border p-2 mr-2"/>
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} className="border p-2 mr-2"/>
        <button onClick={register} className="bg-blue-500 text-white p-2 mr-2">Register</button>
        <button onClick={login} className="bg-green-500 text-white p-2">Login</button>
      </div>

      {/* FORM */}
      <div className="grid grid-cols-2 gap-3 bg-white p-4 rounded shadow">
        {Object.keys(form).map((key) => (
          <input
            key={key}
            name={key}
            placeholder={key.replaceAll("_", " ")}
            onChange={handleChange}
            className="border p-2"
          />
        ))}
      </div>

      <button
        onClick={predict}
        className="mt-4 w-full bg-purple-600 text-white p-3 rounded"
      >
        Predict Group
      </button>

      {result && (
        <div className="mt-6 text-center text-2xl font-bold text-green-600">
          Predicted Group: {result}
        </div>
      )}
    </div>
  );
}