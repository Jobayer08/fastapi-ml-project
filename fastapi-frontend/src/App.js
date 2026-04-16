import React, { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const API = "https://fastapi-ml-project-gu9k.onrender.com";

  // 🔐 Auth
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  // 🤖 Form State
  const [form, setForm] = useState({});
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
    const res = await axios.post(`${API}/predict`, form, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setResult(res.data.predicted_group);
  };

  // 🔥 Reusable Field Component
  const Field = ({ label, name, type = "text", hint, options, min, max }) => (
    <div className="flex flex-col">
      <label className="font-semibold">{label}</label>

      {options ? (
        <select
          name={name}
          onChange={handleChange}
          className="border p-2 rounded"
        >
          <option value="">Select...</option>
          {options.map((op) => (
            <option key={op}>{op}</option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          name={name}
          min={min}
          max={max}
          placeholder={hint}
          onChange={handleChange}
          className="border p-2 rounded"
        />
      )}

      <small className="text-gray-500">{hint}</small>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        🎓 Student Group Prediction
      </h1>

      {/* AUTH */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="font-bold mb-2">Authentication</h2>
        <input
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2 mr-2"
        />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={register} className="bg-blue-500 text-white p-2 mr-2">
          Register
        </button>
        <button onClick={login} className="bg-green-500 text-white p-2">
          Login
        </button>
      </div>

      {/* FORM */}
      <div className="grid md:grid-cols-3 gap-4 bg-white p-6 rounded shadow">

        <Field label="Age" name="age" type="number" min="10" max="25" hint="Number (10-25)" />

        <Field label="Gender" name="gender" options={["Male", "Female"]} hint="Male / Female" />

        <Field label="Location" name="location" options={["Urban", "Rural", "City"]} hint="Urban / Rural / City" />

        <Field label="Family Size" name="family_size" type="number" min="1" max="10" hint="Number (1-10)" />

        <Field label="Mother Education" name="mother_education" options={["SSC", "HSC", "Diploma", "Honors", "Masters"]} hint="Education level" />

        <Field label="Father Education" name="father_education" options={["SSC", "HSC", "Diploma", "Honors", "Masters"]} />

        <Field label="Mother Job" name="mother_job" options={["Yes", "No"]} />

        <Field label="Father Job" name="father_job" options={["Yes", "No"]} />

        <Field label="Guardian" name="guardian" options={["Father", "Mother"]} />

        <Field label="Parental Involvement" name="parental_involvement" options={["Yes", "No"]} />

        <Field label="Internet Access" name="internet_access" options={["Yes", "No"]} />

        <Field label="Study Time (hours)" name="studytime" type="number" min="1" max="12" hint="1-12 hours" />

        <Field label="Tutoring" name="tutoring" options={["Yes", "No"]} />

        <Field label="School Type" name="school_type" options={["Govt", "Private", "Semi_Govt"]} />

        <Field label="Attendance %" name="attendance" type="number" min="0" max="100" hint="0-100" />

        <Field label="Extra Curricular" name="extra_curricular_activities" options={["Yes", "No"]} />

        <Field label="English" name="english" type="number" min="0" max="100" hint="0-100" />

        <Field label="Math" name="math" type="number" min="0" max="100" hint="0-100" />

        <Field label="Science" name="science" type="number" min="0" max="100" hint="0-100" />

        <Field label="Social Science" name="social_science" type="number" min="0" max="100" hint="0-100" />

        <Field label="Art & Culture" name="art_culture" type="number" min="0" max="100" hint="0-100" />

      </div>

      <button
        onClick={predict}
        className="mt-6 w-full bg-purple-600 text-white p-3 rounded text-lg"
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