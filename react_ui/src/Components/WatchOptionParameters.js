import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Loading from './Loading';
import '../CSS/WatchOptionParameters.css';
import backendIP from '../BackendIP';

const WatchOptionParameters = () => {
  const [parameterData, setParameterData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${backendIP}/get_option_parameters`);
        setParameterData(response.data);
      } catch (error) {
        console.error('Error fetching execution result:', error);
        setError('Error fetching data');
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div className="watch-params-container">
      {loading && <Loading className="loading" />}
      {error && <div className="error">Error: {error}</div>}
      {parameterData && (
        <div className="watch-params-table-container">
          <div>{parameterData.name}</div>
          <div className="watch-option-scrollable-table">
            <table className="watch-params-table">
              <thead>
                <tr>
                  {Object.keys(parameterData[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {parameterData.map((row, index) => (
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

export default WatchOptionParameters;
