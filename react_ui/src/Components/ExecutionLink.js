import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Loading from './Loading';
import '../CSS/ExecutionLink.css';
import backendIP from '../BackendIP';

const ExecutionLink = () => {
  const [executionData, setExecutionData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${backendIP}/get_execution_result`);
        setExecutionData(response.data);
      } catch (error) {
        console.error('Error fetching execution result:', error);
        setError('Error fetching data');
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div className="execution-container">
      {loading && <Loading className="loading" />}
      {error && <div className="error">Error: {error}</div>}
      {executionData && (
        <div className="table-container">
          <div>{executionData.name}</div>
          <div className="scrollable-table">
            <table className="execution-table">
              <thead>
                <tr>
                  {Object.keys(executionData[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {executionData.map((row, index) => (
                  <tr key={index}>
                    {Object.keys(row).map((key) => (
                      <td key={key}>{row[key]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExecutionLink;
