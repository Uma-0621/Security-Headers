import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [grade, setGrade] = useState('');
  const [missingHeaders, setMissingHeaders] = useState([]);
  const [reportUrl, setReportUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/evaluate/', { url });
      setGrade(response.data.grade);
      setMissingHeaders(response.data.missing_headers);
      setReportUrl(response.data.report_url);
    } catch (error) {
      console.error('Error evaluating headers:', error);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await axios.get(reportUrl, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'SecurityReport.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading PDF:', error);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif', background: '#f0f4f8', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'center', color: '#2c3e50' }}>🔒 Security Headers Evaluator</h1>
      <form onSubmit={handleSubmit} style={{ textAlign: 'center', marginTop: '2rem' }}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter website URL"
          required
          style={{
            padding: '0.5rem',
            width: '60%',
            maxWidth: '400px',
            border: '1px solid #ccc',
            borderRadius: '5px',
            marginRight: '1rem',
          }}
        />
        <button type="submit" style={{
          padding: '0.5rem 1rem',
          backgroundColor: '#3498db',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
        }}>
          Check
        </button>
      </form>

      {grade && (
        <div style={{ textAlign: 'center', marginTop: '3rem', background: '#fff', padding: '1rem', borderRadius: '10px', boxShadow: '0 4px 10px rgba(0,0,0,0.1)', width: '80%', maxWidth: '600px', margin: '3rem auto' }}>
          <h2 style={{ color: '#2ecc71' }}>Grade: {grade}</h2>
          {missingHeaders.length > 0 && (
            <div style={{ marginTop: '1rem' }}>
              <h3 style={{ color: '#e67e22' }}>Missing Headers:</h3>
              <ul style={{ listStyleType: 'circle', paddingLeft: '20px', textAlign: 'left' }}>
                {missingHeaders.map((header, index) => (
                  <li key={index}>{header}</li>
                ))}
              </ul>
            </div>
          )}
          {reportUrl && (
            <button onClick={handleDownload} style={{
              marginTop: '1.5rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#2ecc71',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
            }}>
              📥 Download PDF
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
