import { useState } from "react";
import "../css/main.css";

export default function Home() {
  // State for form inputs
  const [form, setForm] = useState({
    fever: "",
    cough: "",
    headache: "",
    fatigue: "",
    nausea: "",
    soreThroat: "",
    runnyNose: "",
  });

  // State for backend response
  const [result, setResult] = useState(null);

  // Update form values as user types
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Submit form and send POST request to Flask
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:5000/ai/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        throw new Error(`HTTP Error! Status code: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setResult({ error: "Unable to connect to the server" });
    }
  };

  return (
    <>
      <div className="wrapper">
        <h1>Welcome to the Health App!</h1>
        <p>Please answer the questions below</p>

        <form className="symptom-form" onSubmit={handleSubmit}>
          {Object.keys(form).map((key) => (
            <label key={key}>
              {key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, " $1")}:
              <input
                type="number"
                name={key}
                min="0"
                max="9"
                placeholder="0-9"
                value={form[key]}
                onChange={handleChange}
                required
              />
            </label>
          ))}
          <button type="submit">Submit</button>
        </form>

        {result && (
          <div className="result">
            {result.error ? (
              <p style={{ color: "red" }}>{result.error}</p>
            ) : (
              <>
                <h3>Result:</h3>
                <p>
                  <strong>Score:</strong> {result.score}
                </p>
                <p>
                  <strong>Status:</strong> {result.status}
                </p>
              </>
            )}
          </div>
        )}
      </div>
    </>
  );
}
