import React, { useState } from 'react';
import axios from 'axios';

const Predictor = () => {
  const [data, setData] = useState({
    protocol_type: '',
    service: '',
    flag: '',
    // Add other necessary fields for prediction
  });
  
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    setData({
      ...data,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', data);
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <div>
      <h1>Network Threat Prediction</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Protocol Type</label>
          <input
            type="text"
            name="protocol_type"
            value={data.protocol_type}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Service</label>
          <input
            type="text"
            name="service"
            value={data.service}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Flag</label>
          <input
            type="text"
            name="flag"
            value={data.flag}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Get Prediction</button>
      </form>

      {prediction && <div>Prediction: {prediction}</div>}
    </div>
  );
};

export default Predictor;
