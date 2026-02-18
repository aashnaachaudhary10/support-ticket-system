import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css"; // Our new modern CSS

const API_BASE = "http://localhost:8000/api";

function App() {
  const [tickets, setTickets] = useState([]);
  const [stats, setStats] = useState({});
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [priority, setPriority] = useState("");
  const [loadingClassify, setLoadingClassify] = useState(false);
  const [classifyInput, setClassifyInput] = useState("");

  // Fetch tickets
  const fetchTickets = async () => {
    try {
      const res = await axios.get(`${API_BASE}/tickets/`);
      setTickets(res.data);
    } catch (err) {
      console.error("Error fetching tickets:", err);
    }
  };

  // Fetch stats
  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/tickets/stats/`);
      setStats(res.data);
    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  };

  useEffect(() => {
    fetchTickets();
    fetchStats();
  }, []);

  // Submit ticket
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/tickets/`, {
        title,
        description,
        category,
        priority,
      });
      setTitle("");
      setDescription("");
      setCategory("");
      setPriority("");
      fetchTickets();
      fetchStats();
    } catch (err) {
      console.error("Error creating ticket:", err);
    }
  };

  // AI classify
  const handleClassify = async () => {
    if (!classifyInput) return;
    setLoadingClassify(true);
    try {
      const res = await axios.post(`${API_BASE}/tickets/classify/`, {
        description: classifyInput,
      });
      setCategory(res.data.suggested_category);
      setPriority(res.data.suggested_priority);
    } catch (err) {
      console.error("AI classify failed:", err);
    } finally {
      setLoadingClassify(false);
    }
  };

  return (
    <div className="container">
      <h1>Support Ticket System</h1>

      {/* Create Ticket */}
      <div className="card form-card">
        <h2>Create Ticket</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength={200}
            required
          />
          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
          <input
            type="text"
            placeholder="Priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          />
          <button type="submit">Create Ticket</button>
        </form>
      </div>

      {/* AI Classify */}
      <div className="card classify-card">
        <h2>AI Ticket Classification</h2>
        <div className="ai-classify">
          <input
            type="text"
            placeholder="Enter ticket description"
            value={classifyInput}
            onChange={(e) => setClassifyInput(e.target.value)}
          />
          <button onClick={handleClassify}>
            {loadingClassify ? "Classifying..." : "Classify"}
          </button>
        </div>
      </div>

      {/* Tickets List */}
      <h2>Tickets</h2>
      <div className="tickets-list">
        {tickets.map((t) => (
          <div className="ticket-card" key={t.id}>
            <h3>{t.title}</h3>
            <p>{t.description}</p>
            <p>
              <strong>Category:</strong> {t.category} |{" "}
              <strong>Priority:</strong> {t.priority} |{" "}
              <strong>Status:</strong> {t.status}
            </p>
            <p>
              <small>{new Date(t.created_at).toLocaleString()}</small>
            </p>
          </div>
        ))}
      </div>

      {/* Stats */}
      <h2>Statistics Dashboard</h2>
      <div className="stats-container">
        <div className="stat-card">Total Tickets: {stats.total_tickets}</div>
        <div className="stat-card">Open Tickets: {stats.open_tickets}</div>
        <div className="stat-card">
          Average / Day: {stats.avg_tickets_per_day}
        </div>
        {stats.priority_breakdown &&
          Object.entries(stats.priority_breakdown).map(([k, v]) => (
            <div key={k} className="stat-card">
              Priority {k}: {v}
            </div>
          ))}
        {stats.category_breakdown &&
          Object.entries(stats.category_breakdown).map(([k, v]) => (
            <div key={k} className="stat-card">
              Category {k}: {v}
            </div>
          ))}
      </div>
    </div>
  );
}

export default App;
