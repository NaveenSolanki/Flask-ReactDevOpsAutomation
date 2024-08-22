import React from 'react';
import DayDataComponent from './Day_Data';
import MonthDataComponent from './Month_Data';
import YearDataComponent from './Year_Data';
import '../CSS/Result.css';

const Result = ({ responseData, error }) => {
  return (
    <div className="result-container">
      <p className="result-subheading">Strategy Historical Performance</p>
      <div className="strategy-info">
        <p className="result-paragraph"><span className="key-name">Selected Strategy:</span> {responseData.strategy}</p>
        <p className="result-paragraph"><span className="key-name">Starting Date:</span> {responseData.start_date}</p>
        <p className="result-paragraph"><span className="key-name">Ending Date:</span> {responseData.end_date}</p>
        <p className="result-paragraph"><span className="key-name">Orderbook Location:</span> {responseData.source}</p>
        <p className="result-paragraph"><span className="key-name">Chart Pattern Selected:</span> {responseData.chart_pattern}</p>
      </div>
      <br /><br />
      {responseData.strategy && (
        <div className="data-component">
          <DayDataComponent tableData={responseData.table_data_day} chartPattern={responseData.chart_pattern} chartLocation={responseData.chart_data_location} />
        </div>
      )}
      <br /><br />
      {responseData.strategy && (
        <div className="data-component">
          <MonthDataComponent tableData={responseData.table_data_month} chartPattern={responseData.chart_pattern} chartLocation={responseData.chart_data_location} />
        </div>
      )}
      <br /><br />
      {responseData.strategy && (
        <div className="data-component">
          <YearDataComponent tableData={responseData.table_data_year} chartPattern={responseData.chart_pattern} chartLocation={responseData.chart_data_location} />
        </div>
      )}
    </div>
  );
}
export default Result;
