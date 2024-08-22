import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Loading from './Loading';
import backendIP from '../BackendIP';
import ShowComparisonTable from './ShowComparisonTable';
import '../CSS/ComparisonTableData.css'

const ComparisonTable = () => {
    const [responseData, setResponseData] = useState(null);
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
        trading_strategy_1: '',
        trading_strategy_2: '',
        trading_strategy_3: '',
        job_type: '',
        source: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    async function handleSubmit(event) {
        event.preventDefault(); // Prevent default form submission
        setLoading(true);
        try {
            const response = await axios.post(`${backendIP}/compare_table_data`, formData);
            const { trading_strategy_1, trading_strategy_2, trading_strategy_3 } = formData;
            const columns = [trading_strategy_1, trading_strategy_2, trading_strategy_3];
            setResponseData({ columns, data: response.data });
            navigate('/compare_table_data')

        } catch (Error) {
            console.error('Error submitting form:', Error);
        } finally {
            setLoading(false);
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
        <div>
            <form onSubmit={handleSubmit} className="comparison-input-form">
                <label htmlFor="trading_strategy_1">Strategy 1</label>
                <select name="trading_strategy_1" id="trading_strategy_1" value={formData.trading_strategy_1} onChange={handleChange} required>
                    <option value="" disabled>-- Select the strategy --</option>
                    {tradingStrategyList.map((strategy, index) => (
                        <option key={index} value={strategy}>{strategy}</option>
                    ))}
                </select>
                <br /><br />
                <label htmlFor="trading_strategy_2">Strategy 2</label>
                <select name="trading_strategy_2" id="trading_strategy_2" value={formData.trading_strategy_2} onChange={handleChange} required>
                    <option value="" disabled>-- Select the strategy --</option>
                    {tradingStrategyList.map((strategy, index) => (
                        <option key={index} value={strategy}>{strategy}</option>
                    ))}
                </select>
                <br /><br />
                <label htmlFor="trading_strategy_3">Strategy 3</label>
                <select name="trading_strategy_3" id="trading_strategy_3" value={formData.trading_strategy_3} onChange={handleChange} required>
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
                <label htmlFor="job_type">Job Type</label>
                <select name="job_type" id="job_type" value={formData.job_type} onChange={handleChange} required>
                    <option value="" disabled>-- Select the Location --</option>
                    <option value="index_algo">Index</option>
                    <option value="options_algo">Options</option>
                </select>
                <button type="submit">Submit</button>
            </form>
            {loading && <Loading />}
            <br /><br />
            {responseData !== null && (
                <ShowComparisonTable columns={responseData.columns} data={responseData.data} />
            )}
        </div>
    );
};

export default ComparisonTable;
