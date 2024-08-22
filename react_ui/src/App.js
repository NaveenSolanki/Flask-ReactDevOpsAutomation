import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import InputPage from './Components/Input_Page.js';
import Result from './Components/Result.js';
import Header from './Components/Header.js';
import ExecutionLink from './Components/ExecutionLink.js';
import UploadOptionParams from './Components/Upload_Option_Params.js';
import SummaryTable from './Components/summary_table.js';
import ComparisonTable from './Components/ComparisonTableData.js';
import WatchOptionParameters from './Components/WatchOptionParameters.js';

const App = () => {
  const [responseData, setResponseData] = useState({});
  const [error, setError] = useState({});
  const [dataProcessed, setDataProcessed] = useState(false);
  const [accessedData, setAccessedData] = useState(false); // Track whether data is accessed

  const handleDataProcessed = () => {
    setDataProcessed(true);
  };

  // Simulate data access delay
  setTimeout(() => {
    if (!accessedData) {
      setDataProcessed(true); // Assume data is processed after delay
    }
  }, 3000); // Adjust the delay time as needed (in milliseconds)

  return (
    <>
      <div>
        <BrowserRouter>
          <Header />  
          <Routes>
            <Route path="/option_parameters" element={<WatchOptionParameters />} />
            <Route path="/execution_result" element={<ExecutionLink />} />
            <Route path="/upload_option_parameters" element={<UploadOptionParams />}/>
            <Route
              exact
              path="/"
              element={
                <InputPage
                  setResponseData={setResponseData}
                  setError={setError}
                  onDataProcessed={handleDataProcessed}
                  onDataAccessed={() => setAccessedData(true)} // Set accessedData to true when data is accessed
                />
              }
            />
            {/* Only navigate to Result if data processing is complete */}
            {dataProcessed && (
              <Route path="/result" element={<Result responseData={responseData} error={error} />} />
            )}
            {/* Redirect to InputPage if data processing is not complete */}
            {!dataProcessed && <Route path="/result" element={<Navigate to="/" replace />} />}
            <Route path="/summary_table_data" element={<SummaryTable />} />
            <Route path="/compare_table_data" element={<ComparisonTable />} />
          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
};

export default App;


