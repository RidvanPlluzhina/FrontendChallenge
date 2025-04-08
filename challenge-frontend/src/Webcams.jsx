import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Webcams() {
  const [webcams, setWebcams] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:3000/api/webcams') // replace with your real backend URL
      .then((res) => {
        setWebcams(res.data); // or res.data.Items if needed
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Webcams</h2>
      {webcams.map((cam) => (
        <div key={cam.Id} style={{ marginBottom: '20px' }}>
          <h4>{cam.Webcamname?.de}</h4>
          <img
            src={cam.ImageGallery?.[0]?.ImageUrl}
            alt={cam.Webcamname?.de}
            style={{ maxWidth: '100%', borderRadius: '8px' }}
          />
        </div>
      ))}
    </div>
  );
}

export default Webcams;
