import React, { useEffect } from 'react';
import { displayChartDay } from './chart.js';
import '../CSS/Day_Data.css';

const DayDataComponent = ({ tableData, chartPattern, chartLocation }) => {
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
                await displayChartDay('chartDayOnDay', chartPattern, chartLocation, width, height);
            } catch (error) {
                console.error('Error displaying chart:', error);
            }   
        };
        renderChart();
    }, [chartPattern, chartLocation]);

    // Extract column names dynamically from the keys of the first row in tableData
    const columnNames = tableData.length > 0 ? Object.keys(tableData[0]) : [];

    return (
        <div className="day-data-container">
            <div className="day-table-container">
                <h2 className="day_title">Day on Day View</h2>
                <table className="day_table">
                    <thead className="day-thead-dark">
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
            <div className="day-chart-container">
                <div className="chartForDay" id="chartDayOnDay"></div>
            </div>
        </div>
    );
}

export default DayDataComponent;
