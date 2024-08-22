import axios from 'axios';
import { useNavigate ,Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Loading from './Loading';
import '../CSS/InputPage.css'
import backendIP from '../BackendIP';

function InputPage({ setResponseData, setError }) {
    const [tradingStrategyList, settradingStrategyList] = useState([]);
    useEffect(() => {
        fetchData();
        // console.log(tradingStrategyList)
    }, []);

    const fetchData = async () => {
        try {
            const response = await axios.get(`${backendIP}/home`);
            settradingStrategyList(response.data);
            // console.log(response.data)
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };
    const [formData, setFormData] = useState({
        trading_strategy: '',
        source: '',
        chart_pattern: '',
        chart_data_location: '',
        start_date: '',
        end_date: '',
        number_of_rows: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    async function handleSubmit(event) {
        event.preventDefault(); // Prevent default form submission
        setLoading(true);
        try {
            const response = await axios.post(`${backendIP}/home`, formData);
            // console.log(response.data);
            setResponseData(response.data)
            navigate('/result')

        } catch (Error) {
            console.error('Error submitting form:', Error);
            setError(Error)
        } finally {
            setLoading(false); // Reset loading to false after form submission
        }
    }

    async function handleChange(event) {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    }
    return (
        <div className="input-page-container">
            <form onSubmit={handleSubmit} className="input-form">
                <label htmlFor="trading_strategy">Name of the strategy</label>
                <select name="trading_strategy" id="trading_strategy" value={formData.trading_strategy} onChange={handleChange} required>
                    <option value="" disabled>-- Select the strategy --</option>
                    {tradingStrategyList.map((strategy, index) => (
                        <option key={index} value={strategy}>{strategy}</option>
                    ))}
                </select>
                <br /><br />
                <label htmlFor="source">Orderbook Location</label>
                <select name="source" id="source" value={formData.source} onChange={handleChange} required>
                    <option value="" disabled>-- Select the Location --</option>
                    <option value="local">Local</option>
                    <option value="gdrive">Google Drive</option>
                    <option value="s3">S3</option>
                    <option value="sql">SQL</option>
                </select>
                <br /><br />
                <label htmlFor="chart_pattern">Chart Metric Pattern</label>
                <select name="chart_pattern" id="chart_pattern" value={formData.chart_pattern} onChange={handleChange} required>
                    <option value="" disabled>-- Select the Metric --</option>
                    <option value="SMA">SMA</option>
                    <option value="CUSTOM_1">CUSTOM_1</option>
                    <option value="Supertrend">Supertrend</option>
                </select>
                <br /><br />
                <label htmlFor="chart_data_location">Chart Data Location</label>
                <select name="chart_data_location" id="chart_data_location" value={formData.chart_data_location} onChange={handleChange} required>
                    <option value="" disabled>-- Select the Location --</option>
                    <option value="local">Local</option>
                    <option value="gdrive">Google Drive</option>
                    <option value="s3">S3</option>
                    <option value="sql">SQL</option>
                </select>
                <br /><br />
                <h3>Timeframe of execution:</h3>
                <div>
                    <label htmlFor="start_date">Start Date:</label>
                    <input type="date" name="start_date" id="start_date" value={formData.start_date} onChange={handleChange} required />
                    <label htmlFor="end_date">End Date:</label>
                    <input type="date" name="end_date" id="end_date" value={formData.end_date} onChange={handleChange} required />
                </div>
                <br /><br />
                <label htmlFor="number_of_rows">Number Of Summary Table Rows To Be Displayed</label>
                <select name="number_of_rows" id="number_of_rows" value={formData.number_of_rows} onChange={handleChange} required>
                    <option value="" disabled>-- Select a Number --</option>
                    <option value="row_1">1</option>
                    <option value="row_2">2</option>
                    <option value="row_3">3</option>
                    <option value="row_4">4</option>
                    <option value="row_5">5</option>
                    <option value="row_6">6</option>
                    <option value="row_7">7</option>
                </select>
                <br /><br />
                <button type="submit">Submit</button>
            </form>
            {loading && <Loading />}
            <Link to="/summary_table_data">Get Summary Table</Link>
            <br /><br />
            <Link to="/compare_table_data">Compare Summary Table</Link>
        </div>
    )
}
export default InputPage;