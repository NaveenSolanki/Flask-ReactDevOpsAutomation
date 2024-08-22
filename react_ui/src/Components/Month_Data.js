import React, { useEffect } from 'react';
import { displayChartMonth } from './chart.js';
import '../CSS/Month_Data.css';

const MonthDataComponent = ({ tableData, chartPattern, chartLocation }) => {
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
        await displayChartMonth('chartMonthOnMonth', chartPattern, chartLocation, width, height);
      } catch (error) {
        console.error('Error displaying chart:', error);
      }
    };
    renderChart();
  }, [chartPattern, chartLocation]);

  // Extract column names dynamically from the keys of the first row in tableData
  const columnNames = tableData.length > 0 ? Object.keys(tableData[0]) : [];

  return (
    <div className="month-data-container">
      <div className="month-table-container">
        <h2 className="month_title">Month on Month View</h2>
        <table className="month_table">
          <thead className="month-thead-dark">
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
      <div className="month-chart-container">
        <div className="chartForMonth" id="chartMonthOnMonth"></div>
      </div>
    </div>
  );
}

export default MonthDataComponent;
