// import React, { useState } from 'react';
import '../CSS/position_action.css'

const ShortPositionAction = ({ rows, setRows }) => {
    const addRow = () => {
        const newRow = {
            id: rows.length + 1,
            type: '',
            sel_criteria: '',
            itm_atm_otm: '',
            delta_strike_price: '',
            action_execution: ''
        };
        setRows([...rows, newRow]);
    };

    const deleteRow = (id) => {
        const updatedRows = rows.filter(row => row.id !== id);
        setRows(updatedRows);
    };

    const handleInputChange = (id, value, column) => {
        const updatedRows = rows.map(row => {
            if (row.id === id) {
                return { ...row, [column]: value };
            }
            return row;
        });
        setRows(updatedRows);
    };

    return (
        <div className="position-action">
            <h2>Short Position Action</h2>

            <table>
                <thead>
                    <tr>
                        <th>type</th>
                        <th>sel_criteria</th>
                        <th>itm_atm_otm</th>
                        <th>delta_strike_price</th>
                        <th>action_execution</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {rows.map(row => (
                        <tr key={row.id}>
                            <td>
                                <select
                                    value={row.type}
                                    onChange={(e) => handleInputChange(row.id, e.target.value, 'type')} required
                                >
                                    <option value="" disabled>--- select ---</option>
                                    <option value="PE">PE</option>
                                    <option value="CE">CE</option>
                                </select>
                            </td>
                            <td>
                                <select
                                    value={row.sel_criteria}
                                    onChange={(e) => handleInputChange(row.id, e.target.value, 'sel_criteria')} required
                                >
                                    <option value="" disabled>--- select ---</option>
                                    <option value="Strike Price">Strike Price</option>
                                </select>
                            </td>
                            <td>
                                <select
                                    value={row.itm_atm_otm}
                                    onChange={(e) => handleInputChange(row.id, e.target.value, 'itm_atm_otm')} required
                                >
                                    <option value="" disabled>--- select ---</option>
                                    <option value="itm">ITM</option>
                                    <option value="atm">ATM</option>
                                    <option value="otm">OTM</option>
                                </select>
                            </td>
                            <td>
                                <input
                                    type="text"
                                    name="delta_strike_price"
                                    value={row.delta_strike_price}
                                    onChange={(e) => handleInputChange(row.id, e.target.value, 'delta_strike_price')} required
                                />
                            </td>
                            <td>
                                <select
                                    value={row.action_execution}
                                    onChange={(e) => handleInputChange(row.id, e.target.value, 'action_execution')} required
                                >
                                    <option value="" disabled>--- select ---</option>
                                    <option value="SELL">SELL</option>
                                    <option value="BUY">BUY</option>
                                </select>
                            </td>
                            <td>
                                <button onClick={() => deleteRow(row.id)} className="position-action__delete">Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={addRow} className='position-action__add-row'>Add Row</button>
        </div>

    );
};

export default ShortPositionAction;
