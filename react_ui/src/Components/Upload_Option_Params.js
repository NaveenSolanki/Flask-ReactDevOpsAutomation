import React, { useState } from 'react';
import axios from 'axios';
import LongPositionAction from './long_position_action';
import ShortPositionAction from './short_position_action';
import NeutralPositionAction from './neutral_position_action';
import Loading from './Loading';
import '../CSS/Upload_Option_Params.css'
import backendIP from '../BackendIP';

const UploadOptionParams = () => {
    const [longRows, setLongRows] = useState([]);
    const [shortRows, setShortRows] = useState([]);
    const [neutralRows, setNeutralRows] = useState([]);
    const [entryMetric, setEntryMetric] = useState('');
    const [strategyName, setStrategyName] = useState('');
    const [loading, setLoading] = useState(false);
    const [responseData, setResponseData] = useState(false);

    const handleSubmit = async () => {
        // Check if any row has empty values in LongPositionAction
        const hasEmptyValuesLong = longRows.some(row => (
            row.type === '' ||
            row.sel_criteria === '' ||
            row.itm_atm_otm === '' ||
            row.delta_strike_price === '' ||
            row.action_execution === ''
        ));

        // Check if any row has empty values in ShortPositionAction
        const hasEmptyValuesShort = shortRows.some(row => (
            row.type === '' ||
            row.sel_criteria === '' ||
            row.itm_atm_otm === '' ||
            row.delta_strike_price === '' ||
            row.action_execution === ''
        ));

        // Check if any row has empty values in NeutralPositionAction
        const hasEmptyValuesNeutral = neutralRows.some(row => (
            row.type === '' ||
            row.sel_criteria === '' ||
            row.itm_atm_otm === '' ||
            row.delta_strike_price === '' ||
            row.action_execution === ''
        ));

        if (hasEmptyValuesLong || hasEmptyValuesShort || hasEmptyValuesNeutral) {
            alert('Please fill in all the values for selected rows in all components.');
            return;
        }

        // Check if entry metric and strategy name are not empty
        if (!entryMetric || !strategyName) {
            alert('Please fill in the entry metric and strategy name.');
            return;
        }
        setLoading(true);
        try {
            // Construct the JSON payload with data from all three components, entry metric, and strategy name
            const payload = {
                longPositionAction: longRows,
                shortPositionAction: shortRows,
                neutralPositionAction: neutralRows,
                entryMetric: entryMetric,
                strategyName: strategyName
            };

            // Send the JSON payload to the Flask backend
            const response = await axios.post(`${backendIP}/upload_option_params`, payload);
            console.log(response.data); // Handle response from the backend
            setResponseData(response.data)
            setLongRows([]);
            setShortRows([]);
            setNeutralRows([]);
            setEntryMetric('');
            setStrategyName('');
            setTimeout(() => {
                setResponseData(false); // Reset responseData after 5 seconds
            }, 5000);

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false); // Reset loading to false after form submission
        }
    };

    return (
        <div className="upload-params-container">
            {responseData && <div className={`flash-message ${responseData === 'Success!' ? 'success-message' : 'failure-message'}`}>{responseData}</div>}
            <h2 className="upload-params-h2">Upload Option Parameters</h2>
            <div className="upload-params-form">
                <label className="upload-params-label" htmlFor="entryMetric">Entry Metric:</label>
                <select className="upload-params-select" id="entryMetric" value={entryMetric} onChange={e => setEntryMetric(e.target.value)}>
                    <option value="">--- Select ---</option>
                    <option value="SMA">SMA</option>
                    <option value="RSI">RSI</option>
                    <option value="morning entry">Morning Entry</option>
                </select>
            </div>
            <div className="upload-params-form">
                <label className="upload-params-label" htmlFor="strategyName">Strategy Name:</label>
                <input className="upload-params-input" type="text" id="strategyName" value={strategyName} onChange={e => setStrategyName(e.target.value)} />
            </div>
            <div className="upload-params-component upload-params-long-light-bg">
                <LongPositionAction rows={longRows} setRows={setLongRows} />
            </div>
            <div className="upload-params-component upload-params-short-light-bg">
                <ShortPositionAction rows={shortRows} setRows={setShortRows} />
            </div>
            <div className="upload-params-component upload-params-neutral-light-bg">
                <NeutralPositionAction rows={neutralRows} setRows={setNeutralRows} />
            </div>
            <br />
            <button className="upload-params-button upload-params-full-width" onClick={handleSubmit}>Submit</button>
            {loading && <div className="upload-params-loading"><Loading /></div>}
        </div>
    );
};

export default UploadOptionParams;