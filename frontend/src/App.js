import React, { useState } from 'react';
import './App.css';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from 'chart.js';
ChartJS.register(BarElement, CategoryScale, LinearScale);

function App() {
  const [protocolType, setProtocolType] = useState('');
  const [service, setService] = useState('');
  const [flag, setFlag] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [threatStats, setThreatStats] = useState({ normal: 0, anomaly: 0 });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      protocol_type: protocolType,
      service: service,
      flag: flag,
      duration: 0,
      src_bytes: 0,
      dst_bytes: 0
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (data.results) {
        setResult(data.results[0]);
        setThreatStats((prev) => ({
          ...prev,
          [data.results[0].prediction]: prev[data.results[0].prediction] + 1
        }));
        setError(null);
      } else {
        setError(data.error || 'Unexpected response');
        setResult(null);
      }
    } catch (err) {
      setError('Error: ' + err.message);
      setResult(null);
    }
  };

  const chartData = {
    labels: ['Normal', 'Anomaly'],
    datasets: [
      {
        label: 'Live Threat Count',
        data: [threatStats.normal, threatStats.anomaly],
        backgroundColor: ['#4CAF50', '#F44336'],
        borderRadius: 8
      }
    ]
  };

  return (
    <div className="App" style={{ fontFamily: 'Arial', padding: '20px' }}>
      <h1>Network Threat Detection</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <label>Protocol Type:</label>
        <input
          type="text"
          value={protocolType}
          onChange={(e) => setProtocolType(e.target.value)}
          placeholder="e.g., tcp"
        />
        <label>Service:</label>
        <input
          type="text"
          value={service}
          onChange={(e) => setService(e.target.value)}
          placeholder="e.g., http"
        />
        <label>Flag:</label>
        <input
          type="text"
          value={flag}
          onChange={(e) => setFlag(e.target.value)}
          placeholder="e.g., SF"
        />
        <button type="submit">Predict Threat</button>
      </form>

      {result && (
        <div
          style={{
            border: '1px solid #ccc',
            padding: '15px',
            borderRadius: '8px',
            backgroundColor: result.prediction === 'anomaly' ? '#ffe5e5' : '#e0ffe0',
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <span style={{ marginRight: '15px', fontSize: '2em' }}>
            {result.prediction === 'anomaly' ? (
              <i className="fas fa-exclamation-triangle" style={{ color: 'red' }}></i>
            ) : (
              <i className="fas fa-check-circle" style={{ color: 'green' }}></i>
            )}
          </span>
          <div>
            <h2>
              Prediction:{' '}
              <span style={{ color: result.prediction === 'anomaly' ? 'red' : 'green' }}>
                {result.prediction}
              </span>
            </h2>
            <p><strong>Threat:</strong> {result.threat_info.threat_name}</p>
            <p><strong>Prevention:</strong> {result.threat_info.prevention}</p>
            <p><strong>Confidence:</strong></p>
            <ul>
              <li><strong>Anomaly:</strong> {result.confidence.anomaly}</li>
              <li><strong>Normal:</strong> {result.confidence.normal}</li>
            </ul>
          </div>
        </div>
      )}

      {error && (
        <div style={{ color: 'red', marginTop: '20px' }}>
          {error}
        </div>
      )}

      <div className="chart-container" style={{ maxWidth: '400px', margin: '40px auto' }}>
        <h3>Live Threat Stats</h3>
        <Bar data={chartData} />
      </div>
    </div>
  );
}

export default App;
