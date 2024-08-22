import React from 'react';
import '../CSS/ShowComparisonTableData.css'
const ShowComparisonTable = ({ columns, data }) => {
    if (!data || !columns) return null;

    return (
        <div className="ComparisonTable">
            <div className='trade-table'>
                <h2>Trade View</h2>
                <table className="TradeViewTable">
                    <thead>
                        <tr>
                            <th></th>
                            {columns.map((columnName, index) => (
                                <th key={index}>{columnName}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.trade_view.map((item, index) => (
                            <tr key={index}>
                                <td>{item['']}</td>
                                {columns.map((column, columnIndex) => (
                                    <td key={columnIndex}>{item[column][Object.keys(item[column])[0]]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className='day-table'>
                <h2>Day View</h2>
                <table className="DayViewTable">
                    <thead>
                        <tr>
                            <th></th>
                            {columns.map((columnName, index) => (
                                <th key={index}>{columnName}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.day_view.map((item, index) => (
                            <tr key={index}>
                                <td>{item['']}</td>
                                {columns.map((column, columnIndex) => (
                                    <td key={columnIndex}>{item[column][Object.keys(item[column])[0]]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className='week-table'>
                <h2>Week View</h2>
                <table className="WeekViewTable">
                    <thead>
                        <tr>
                            <th></th>
                            {columns.map((columnName, index) => (
                                <th key={index}>{columnName}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.week_view.map((item, index) => (
                            <tr key={index}>
                                <td>{item['']}</td>
                                {columns.map((column, columnIndex) => (
                                    <td key={columnIndex}>{item[column][Object.keys(item[column])[0]]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className='month-table'>
                <h2>Month View</h2>
                <table className="MonthViewTable">
                    <thead>
                        <tr>
                            <th></th>
                            {columns.map((columnName, index) => (
                                <th key={index}>{columnName}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.month_view.map((item, index) => (
                            <tr key={index}>
                                <td>{item['']}</td>
                                {columns.map((column, columnIndex) => (
                                    <td key={columnIndex}>{item[column][Object.keys(item[column])[0]]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className='year-table'>
                <h2>Year View</h2>
                <table className="YearViewTable">
                    <thead>
                        <tr>
                            <th></th>
                            {columns.map((columnName, index) => (
                                <th key={index}>{columnName}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.year_view.map((item, index) => (
                            <tr key={index}>
                                <td>{item['']}</td>
                                {columns.map((column, columnIndex) => (
                                    <td key={columnIndex}>{item[column][Object.keys(item[column])[0]]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ShowComparisonTable;
