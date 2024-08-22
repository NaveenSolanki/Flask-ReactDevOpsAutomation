import React, { useEffect } from 'react';
import { displayChartYear } from './chart.js';
import '../CSS/Year_Data.css';

const YearDataComponent = ({ tableData, chartPattern, chartLocation }) => {
  useEffect(() => {
    const renderChart = async () => {
      try {
        let width, height;
                const viewportWidth = window.innerWidth;
                if (viewportWidth <= 576){
                    width = 300;
                    height = 300;
                } else if (viewportWidth <= 768) {
                    width = 500;
                    height = 350;
                } else if (viewportWidth <= 992) {
                    width = 600;
                    height = 400;
                } else {
                    width = 900;
                    height = 450;
                }
        await displayChartYear('chartYearOnYear', chartPattern, chartLocation, width, height);
      } catch (error) {
        console.error('Error displaying chart:', error);
      }
    };
    renderChart();
  }, [chartPattern, chartLocation]);

  // Extract column names dynamically from the keys of the first row in tableData
  const columnNames = tableData.length > 0 ? Object.keys(tableData[0]) : [];

  return (
    <div className="year-data-container">
      <div className="year-table-container">
        <h2 className="year_title">Year on Year View</h2>
        <table className="year_table">
          <thead className="year-thead-dark">
            <tr>
              {columnNames.map((columnName, index) => (
                <th key={index} scope="col">{columnName}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columnNames.map((columnName, colIndex) => (
                  <td key={colIndex}>{row[columnName]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="year-chart-container">
        <div className="chartForYear" id="chartYearOnYear"></div>
      </div>
    </div>
  );
}

export default YearDataComponent;
