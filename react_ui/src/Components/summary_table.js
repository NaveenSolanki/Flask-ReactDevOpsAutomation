import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import Loading from './Loading';
import IndexTable from './IndexTable';
import OptionTable from './OptionTable';
import backendIP from '../BackendIP';
import '../CSS/summary_table.css'

const SummaryTable = () => {
    const [responseData, setResponseData] = useState([null]);
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
        source: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()
    async function handleSubmit(event) {
        event.preventDefault(); // Prevent default form submission
        setLoading(true);
        try {
            const response = await axios.post(`${backendIP}/summary_table_data`, formData);
            // console.log(response.data);
            setResponseData(response.data)
            navigate('/summary_table_data')

        } catch (Error) {
            console.error('Error submitting form:', Error);
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
        <div>
            <form onSubmit={handleSubmit} className="summary-input-form">
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
                <button type="submit">Submit</button>
            </form>
            {loading && <Loading />}
            {responseData !== null && (
                <>
                    <IndexTable indexData={responseData.index} />
                    <OptionTable optionData={responseData.option} />
                </>
            )}
        </div>
    );
};

export default SummaryTable;
