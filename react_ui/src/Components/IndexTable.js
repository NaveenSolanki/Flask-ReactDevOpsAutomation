import React from 'react';
import '../CSS/index_option_table.css';

const IndexTable = ({ indexData }) => {
  return (
    <div className="summary-table"> {/* Add the summary-table class here */}
      {indexData && indexData.length > 0 && (
        <>
          <h2>Index Table</h2>
          <div className="table-container"> {/* Add the table-container class here */}
            <table>
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Trade</th>
                  <th>Daily</th>
                  <th>Weekly</th>
                  <th>Monthly</th>
                  <th>Yearly</th>
                </tr>
              </thead>
              <tbody>
                {indexData.map((item, index) => (
                  <tr key={index}>
                    <td>{item['']}</td>
                    <td>{item.trade[Object.keys(item.trade)[0]]}</td>
                    <td>{item.daily[Object.keys(item.daily)[0]]}</td>
                    <td>{item.weekly[Object.keys(item.weekly)[0]]}</td>
                    <td>{item.monthly[Object.keys(item.monthly)[0]]}</td>
                    <td>{item.yearly[Object.keys(item.yearly)[0]]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};

export default IndexTable;
