from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from compute_table_values import DayOnDaySummary, MonthOnMonthSummary, YearOnYearSummary
from static.AzureSQLDatabase.read_table_from_sql import read_execution_record_sql_table, read_option_parameters_sql_table
from static.CosmosDB.OptionParameters.upload_parameters_to_cosmos import store_data_in_cosmos
from fetch_views import Metric
from fetch_chart_files import ChartData
from fetch_summary_table import SummaryTable, CompareSummaryTable
import pandas as pd
import numpy as np
import json
from flask_cors import CORS
import secrets, string

app = Flask(__name__)
CORS(app)
app.secret_key = 'naveensolanki'

@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        trading_strategies = Metric('','').get_trading_strategy()
        return jsonify(trading_strategies)
    
    if request.method == 'POST':
        data = request.json
        # print(data)
        strategy = data['trading_strategy']
        start_date = data['start_date']
        end_date = data['end_date']
        source = data['source']
        chart_pattern = data['chart_pattern']
        chart_data_location = data['chart_data_location']
        
        metric_results = Metric(strategy, source).execute()

        table_data_day = [
            {'': 'Total no. of win days', 'Index': metric_results['day_view']['index_algo']['total_wins'], 'Options': metric_results['day_view']['options_algo']['total_wins']},
            {'': 'Total no. of loss days', 'Index': metric_results['day_view']['index_algo']['total_losses'], 'Options': metric_results['day_view']['options_algo']['total_losses']},
            {'': 'Total PnL', 'Index': metric_results['day_view']['index_algo']['total_pnl'], 'Options': metric_results['day_view']['options_algo']['total_pnl']},
            {'': 'Average PnL', 'Index': metric_results['day_view']['index_algo']['avg_pnl'], 'Options': metric_results['day_view']['options_algo']['avg_pnl']},
            {'': 'Win Percent', 'Index': metric_results['day_view']['index_algo']['win_percent'], 'Options': metric_results['day_view']['options_algo']['win_percent']},
            {'': 'Avg PnL win', 'Index': metric_results['day_view']['index_algo']['avg_pnl_win'], 'Options': metric_results['day_view']['options_algo']['avg_pnl_win']},
            {'': 'Avg PnL loss', 'Index': metric_results['day_view']['index_algo']['avg_pnl_loss'], 'Options': metric_results['day_view']['options_algo']['avg_pnl_loss']},
        ]

        table_data_month = [
            {'': 'Total no. of win months', 'Index': metric_results['month_view']['index_algo']['total_wins'], 'Options': metric_results['month_view']['options_algo']['total_wins']},
            {'': 'Total no. of loss months', 'Index': metric_results['month_view']['index_algo']['total_losses'], 'Options': metric_results['month_view']['options_algo']['total_losses']},
            {'': 'Total PnL', 'Index': metric_results['month_view']['index_algo']['total_pnl'], 'Options': metric_results['month_view']['options_algo']['total_pnl']},
            {'': 'Average PnL', 'Index': metric_results['month_view']['index_algo']['avg_pnl'], 'Options': metric_results['month_view']['options_algo']['avg_pnl']},
            {'': 'Win Percent', 'Index': metric_results['month_view']['index_algo']['win_percent'], 'Options': metric_results['month_view']['options_algo']['win_percent']},
            {'': 'Avg PnL win', 'Index': metric_results['month_view']['index_algo']['avg_pnl_win'], 'Options': metric_results['month_view']['options_algo']['avg_pnl_win']},
            {'': 'Avg PnL loss', 'Index': metric_results['month_view']['index_algo']['avg_pnl_loss'], 'Options': metric_results['month_view']['options_algo']['avg_pnl_loss']},
        ]

        table_data_year = [
            {'': 'Total no. of win years', 'Index': metric_results['year_view']['index_algo']['total_wins'], 'Options': metric_results['year_view']['options_algo']['total_wins']},
            {'': 'Total no. of loss years', 'Index': metric_results['year_view']['index_algo']['total_losses'], 'Options': metric_results['year_view']['options_algo']['total_losses']},
            {'': 'Total PnL', 'Index': metric_results['year_view']['index_algo']['total_pnl'], 'Options': metric_results['year_view']['options_algo']['total_pnl']},
            {'': 'Average PnL', 'Index': metric_results['year_view']['index_algo']['avg_pnl'], 'Options': metric_results['year_view']['options_algo']['avg_pnl']},
            {'': 'Win Percent', 'Index': metric_results['year_view']['index_algo']['win_percent'], 'Options': metric_results['year_view']['options_algo']['win_percent']},
            {'': 'Avg PnL win', 'Index': metric_results['year_view']['index_algo']['avg_pnl_win'], 'Options': metric_results['year_view']['options_algo']['avg_pnl_win']},
            {'': 'Avg PnL loss', 'Index': metric_results['year_view']['index_algo']['avg_pnl_loss'], 'Options': metric_results['year_view']['options_algo']['avg_pnl_loss']},
        ]

        # Number of Table Data Rows to be Retrieved
        number_of_rows = int(data['number_of_rows'][-1])
        table_data_day = table_data_day[:number_of_rows]
        table_data_month = table_data_month[:number_of_rows]
        table_data_year = table_data_year[:number_of_rows]
        
        # print(table_data_day)
        result_data = {
            'strategy' : strategy,
            'start_date' : start_date,
            'end_date': end_date,
            'source' : source,
            'table_data_day' : table_data_day,
            'table_data_month' : table_data_month,
            'table_data_year' : table_data_year,
            'chart_pattern' : chart_pattern,
            'chart_data_location' : chart_data_location
        }
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NpEncoder, self).default(obj)
        json_result = json.dumps(result_data, cls=NpEncoder)
        # print(type(result_data))
        return json_result
        
    return render_template('index.html')

# Below route is to get the data for the chart to be displayed
@app.route('/get_chart_pattern', methods=['POST'])
def get_chart_pattern():
    chart_data_location = request.json['chart_location']
    chart_metric = request.json['metric']
    # print(chart_data_location,"========================================================================", chart_metric)
    df =  ChartData(chart_data_location, chart_metric).execute()
    # print(df,"---------------")
    return jsonify(df.to_dict(orient='records'))


# Below Route is to Get Execution Records from the Cosmos Database from table "execution_records"
def convert_to_serializable(data):
    for entry in data:
        entry['_id'] = str(entry['_id'])
    return data 
@app.route('/get_execution_result', methods=['GET'])
def get_execution_result():
    df = read_execution_record_sql_table()
    data = convert_to_serializable(df.to_dict(orient='records'))
    return jsonify(data)

# Below Route is to Get Execution Records from the Cosmos Database from table "option_parameters"
@app.route('/get_option_parameters', methods=['GET'])
def get_option_parameters():
    df = read_option_parameters_sql_table()
    data = convert_to_serializable(df.to_dict(orient='records'))
    return jsonify(data)

# Below is the route to take option parameters from webpage and store them to cosmosDB
@app.route('/upload_option_params', methods=['POST'])
def upload_option_params():
    try:
        data = request.json
        # print(data)
        # Extract rows from the payload
        long_position_rows = data.get('longPositionAction', [])
        short_position_rows = data.get('shortPositionAction', [])
        neutral_position_rows = data.get('neutralPositionAction', [])
        
        alphabet_num = string.ascii_letters + string.digits
        strategyID = ''.join(secrets.choice(alphabet_num) for i in range(15))
        
        parameters = {
            "status":"active",
            "entry_logic": data['entryMetric'],
            "strategy_name": data['strategyName'],
            "type": "",
            "sel_criteria": "",
            "itm_atm_otm": "",
            "delta_strike_price": "",
            "goal": "",
            "action_execution": "",
            "strategy_id": strategyID
        }
        
        
        # Process rows of long positions
        for row in long_position_rows:
            parameters['type'] = row['type']
            parameters['sel_criteria'] = row['sel_criteria']
            parameters['itm_atm_otm'] = row['itm_atm_otm']
            parameters['delta_strike_price'] = row['delta_strike_price']
            parameters['action_execution'] = row['action_execution']
            parameters['goal'] = 'long_position'
            store_data_in_cosmos(parameters)
        
        # Process rows of short positions
        for row in short_position_rows:
            parameters['type'] = row['type']
            parameters['sel_criteria'] = row['sel_criteria']
            parameters['itm_atm_otm'] = row['itm_atm_otm']
            parameters['delta_strike_price'] = row['delta_strike_price']
            parameters['action_execution'] = row['action_execution']
            parameters['goal'] = 'short_position'
            store_data_in_cosmos(parameters)
            
        # Process rows of neutral positions
        for row in neutral_position_rows:
            parameters['type'] = row['type']
            parameters['sel_criteria'] = row['sel_criteria']
            parameters['itm_atm_otm'] = row['itm_atm_otm']
            parameters['delta_strike_price'] = row['delta_strike_price']
            parameters['action_execution'] = row['action_execution']
            parameters['goal'] = 'neutral_position'
            store_data_in_cosmos(parameters)
        
        return jsonify('Success!')
    except Exception:    
        return jsonify('Error!')

# Below is the route to get summary table data
@app.route('/summary_table_data', methods=['POST'])
def summary_table_data():
    # if request.method == 'GET':
    #     trading_strategies = Metric('','').get_trading_strategy()
    #     return jsonify(trading_strategies)
    data = request.json
    
    trade_df, day_df, week_df, month_df, year_df = SummaryTable(data['trading_strategy'], data['source']).location()
    index_trade_df = trade_df[trade_df['job_type'] == 'index_algo']
    index_day_df = day_df[day_df['job_type'] == 'index_algo']
    index_week_df = week_df[week_df['job_type'] == 'index_algo']
    index_month_df = month_df[month_df['job_type'] == 'index_algo']
    index_year_df = year_df[year_df['job_type'] == 'index_algo']
    
    option_trade_df = trade_df[trade_df['job_type'] == 'options_algo']
    option_day_df = day_df[day_df['job_type'] == 'options_algo']
    option_week_df = week_df[week_df['job_type'] == 'options_algo']
    option_month_df = month_df[month_df['job_type'] == 'options_algo']
    option_year_df = year_df[year_df['job_type'] == 'options_algo']
    
    index_table = [
        {'': 'Total no. of win months', 'trade': index_trade_df['total_wins'], 'daily': index_day_df['total_wins'], 'weekly': index_week_df['total_wins'], 'monthly': index_month_df['total_wins'], 'yearly': index_year_df['total_wins']},
        {'': 'Total no. of loss months', 'trade': index_trade_df['total_losses'], 'daily': index_day_df['total_losses'], 'weekly': index_week_df['total_losses'], 'monthly': index_month_df['total_losses'], 'yearly': index_year_df['total_losses']},
        {'': 'Total PnL', 'trade': index_trade_df['total_pnl'], 'daily': index_day_df['total_pnl'], 'weekly': index_week_df['total_pnl'], 'monthly': index_month_df['total_pnl'], 'yearly': index_year_df['total_pnl']},
        {'': 'Average PnL', 'trade': index_trade_df['avg_pnl'], 'daily': index_day_df['avg_pnl'], 'weekly': index_week_df['avg_pnl'], 'monthly': index_month_df['avg_pnl'], 'yearly': index_year_df['avg_pnl']},
        {'': 'Win Percent', 'trade': index_trade_df['win_percent'], 'daily': index_day_df['win_percent'], 'weekly': index_week_df['win_percent'], 'monthly': index_month_df['win_percent'], 'yearly': index_year_df['win_percent']},
        {'': 'Avg PnL win', 'trade': index_trade_df['avg_pnl_win'], 'daily': index_day_df['avg_pnl_win'], 'weekly': index_week_df['avg_pnl_win'], 'monthly': index_month_df['avg_pnl_win'], 'yearly': index_year_df['avg_pnl_win']},
        {'': 'Avg PnL loss', 'trade': index_trade_df['avg_pnl_loss'], 'daily': index_day_df['avg_pnl_loss'], 'weekly': index_week_df['avg_pnl_loss'], 'monthly': index_month_df['avg_pnl_loss'], 'yearly': index_year_df['avg_pnl_loss']},
    ]
    
    option_table = [
        {'': 'Total no. of win months', 'trade': option_trade_df['total_wins'], 'daily': option_day_df['total_wins'], 'weekly': option_week_df['total_wins'], 'monthly': option_month_df['total_wins'], 'yearly': option_year_df['total_wins']},
        {'': 'Total no. of loss months', 'trade': option_trade_df['total_losses'], 'daily': option_day_df['total_losses'], 'weekly': option_week_df['total_losses'], 'monthly': option_month_df['total_losses'], 'yearly': option_year_df['total_losses']},
        {'': 'Total PnL', 'trade': option_trade_df['total_pnl'], 'daily': option_day_df['total_pnl'], 'weekly': option_week_df['total_pnl'], 'monthly': option_month_df['total_pnl'], 'yearly': option_year_df['total_pnl']},
        {'': 'Average PnL', 'trade': option_trade_df['avg_pnl'], 'daily': option_day_df['avg_pnl'], 'weekly': option_week_df['avg_pnl'], 'monthly': option_month_df['avg_pnl'], 'yearly': option_year_df['avg_pnl']},
        {'': 'Win Percent', 'trade': option_trade_df['win_percent'], 'daily': option_day_df['win_percent'], 'weekly': option_week_df['win_percent'], 'monthly': option_month_df['win_percent'], 'yearly': option_year_df['win_percent']},
        {'': 'Avg PnL win', 'trade': option_trade_df['avg_pnl_win'], 'daily': option_day_df['avg_pnl_win'], 'weekly': option_week_df['avg_pnl_win'], 'monthly': option_month_df['avg_pnl_win'], 'yearly': option_year_df['avg_pnl_win']},
        {'': 'Avg PnL loss', 'trade': option_trade_df['avg_pnl_loss'], 'daily': option_day_df['avg_pnl_loss'], 'weekly': option_week_df['avg_pnl_loss'], 'monthly': option_month_df['avg_pnl_loss'], 'yearly': option_year_df['avg_pnl_loss']},
    ]
    
    result_data = {
        "index" : index_table,
        "option" :  option_table
    }
    
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, pd.Series):
                return obj.to_dict()
            return super(NpEncoder, self).default(obj)
    json_result = json.dumps(result_data, cls=NpEncoder)
    # print(index_table)
    
    return json_result

# Below is the route to compare summary data    
@app.route('/compare_table_data', methods=['POST'])
def compare_table_data():
    data = request.json
    strategy_1 = data['trading_strategy_1']
    strategy_2 = data['trading_strategy_2']
    strategy_3 = data['trading_strategy_3']
    
    trade_df, day_df, week_df, month_df, year_df = CompareSummaryTable(strategy_1, strategy_2, strategy_3, data['source'], data['job_type']).location()
    
    trade_strategy_1 = trade_df[trade_df['Metric'] == strategy_1]
    trade_strategy_2 = trade_df[trade_df['Metric'] == strategy_2]
    trade_strategy_3 = trade_df[trade_df['Metric'] == strategy_3]
    
    day_strategy_1 = day_df[day_df['Metric'] == strategy_1]
    day_strategy_2 = day_df[day_df['Metric'] == strategy_2]
    day_strategy_3 = day_df[day_df['Metric'] == strategy_3]
    
    week_strategy_1 = week_df[week_df['Metric'] == strategy_1]
    week_strategy_2 = week_df[week_df['Metric'] == strategy_2]
    week_strategy_3 = week_df[week_df['Metric'] == strategy_3]
    
    month_strategy_1 = month_df[month_df['Metric'] == strategy_1]
    month_strategy_2 = month_df[month_df['Metric'] == strategy_2]
    month_strategy_3 = month_df[month_df['Metric'] == strategy_3]
    
    year_strategy_1 = year_df[year_df['Metric'] == strategy_1]
    year_strategy_2 = year_df[year_df['Metric'] == strategy_2]
    year_strategy_3 = year_df[year_df['Metric'] == strategy_3]
    
    table_trade_data = [
        {'': 'Total no. of win months', strategy_1: trade_strategy_1['total_wins'], strategy_2: trade_strategy_2['total_wins'], strategy_3: trade_strategy_3['total_wins']},
        {'': 'Total no. of loss months', strategy_1: trade_strategy_1['total_losses'], strategy_2: trade_strategy_2['total_losses'], strategy_3: trade_strategy_3['total_losses']},
        {'': 'Total PnL', strategy_1: trade_strategy_1['total_pnl'], strategy_2: trade_strategy_2['total_pnl'], strategy_3: trade_strategy_3['total_pnl']},
        {'': 'Average PnL', strategy_1: trade_strategy_1['avg_pnl'], strategy_2: trade_strategy_2['avg_pnl'], strategy_3: trade_strategy_3['avg_pnl']},
        {'': 'Win Percent', strategy_1: trade_strategy_1['win_percent'], strategy_2: trade_strategy_2['win_percent'], strategy_3: trade_strategy_3['win_percent']},
        {'': 'Avg PnL win', strategy_1: trade_strategy_1['avg_pnl_win'], strategy_2: trade_strategy_2['avg_pnl_win'], strategy_3: trade_strategy_3['avg_pnl_win']},
        {'': 'Avg PnL loss', strategy_1: trade_strategy_1['avg_pnl_loss'], strategy_2: trade_strategy_2['avg_pnl_loss'], strategy_3: trade_strategy_3['avg_pnl_loss']},
    ]
    
    table_day_data = [
        {'': 'Total no. of win months', strategy_1: day_strategy_1['total_wins'], strategy_2: day_strategy_2['total_wins'], strategy_3: day_strategy_3['total_wins']},
        {'': 'Total no. of loss months', strategy_1: day_strategy_1['total_losses'], strategy_2: day_strategy_2['total_losses'], strategy_3: day_strategy_3['total_losses']},
        {'': 'Total PnL', strategy_1: day_strategy_1['total_pnl'], strategy_2: day_strategy_2['total_pnl'], strategy_3: day_strategy_3['total_pnl']},
        {'': 'Average PnL', strategy_1: day_strategy_1['avg_pnl'], strategy_2: day_strategy_2['avg_pnl'], strategy_3: day_strategy_3['avg_pnl']},
        {'': 'Win Percent', strategy_1: day_strategy_1['win_percent'], strategy_2: day_strategy_2['win_percent'], strategy_3: day_strategy_3['win_percent']},
        {'': 'Avg PnL win', strategy_1: day_strategy_1['avg_pnl_win'], strategy_2: day_strategy_2['avg_pnl_win'], strategy_3: day_strategy_3['avg_pnl_win']},
        {'': 'Avg PnL loss', strategy_1: day_strategy_1['avg_pnl_loss'], strategy_2: day_strategy_2['avg_pnl_loss'], strategy_3: day_strategy_3['avg_pnl_loss']},
    ]
    
    table_week_data = [
        {'': 'Total no. of win months', strategy_1: week_strategy_1['total_wins'], strategy_2: week_strategy_2['total_wins'], strategy_3: week_strategy_3['total_wins']},
        {'': 'Total no. of loss months', strategy_1: week_strategy_1['total_losses'], strategy_2: week_strategy_2['total_losses'], strategy_3: week_strategy_3['total_losses']},
        {'': 'Total PnL', strategy_1: week_strategy_1['total_pnl'], strategy_2: week_strategy_2['total_pnl'], strategy_3: week_strategy_3['total_pnl']},
        {'': 'Average PnL', strategy_1: week_strategy_1['avg_pnl'], strategy_2: week_strategy_2['avg_pnl'], strategy_3: week_strategy_3['avg_pnl']},
        {'': 'Win Percent', strategy_1: week_strategy_1['win_percent'], strategy_2: week_strategy_2['win_percent'], strategy_3: week_strategy_3['win_percent']},
        {'': 'Avg PnL win', strategy_1: week_strategy_1['avg_pnl_win'], strategy_2: week_strategy_2['avg_pnl_win'], strategy_3: week_strategy_3['avg_pnl_win']},
        {'': 'Avg PnL loss', strategy_1: week_strategy_1['avg_pnl_loss'], strategy_2: week_strategy_2['avg_pnl_loss'], strategy_3: week_strategy_3['avg_pnl_loss']},
    ]
    
    table_month_data = [
        {'': 'Total no. of win months', strategy_1: month_strategy_1['total_wins'], strategy_2: month_strategy_2['total_wins'], strategy_3: month_strategy_3['total_wins']},
        {'': 'Total no. of loss months', strategy_1: month_strategy_1['total_losses'], strategy_2: month_strategy_2['total_losses'], strategy_3: month_strategy_3['total_losses']},
        {'': 'Total PnL', strategy_1: month_strategy_1['total_pnl'], strategy_2: month_strategy_2['total_pnl'], strategy_3: month_strategy_3['total_pnl']},
        {'': 'Average PnL', strategy_1: month_strategy_1['avg_pnl'], strategy_2: month_strategy_2['avg_pnl'], strategy_3: month_strategy_3['avg_pnl']},
        {'': 'Win Percent', strategy_1: month_strategy_1['win_percent'], strategy_2: month_strategy_2['win_percent'], strategy_3: month_strategy_3['win_percent']},
        {'': 'Avg PnL win', strategy_1: month_strategy_1['avg_pnl_win'], strategy_2: month_strategy_2['avg_pnl_win'], strategy_3: month_strategy_3['avg_pnl_win']},
        {'': 'Avg PnL loss', strategy_1: month_strategy_1['avg_pnl_loss'], strategy_2: month_strategy_2['avg_pnl_loss'], strategy_3: month_strategy_3['avg_pnl_loss']},
    ]
    
    table_year_data = [
        {'': 'Total no. of win months', strategy_1: year_strategy_1['total_wins'], strategy_2: year_strategy_2['total_wins'], strategy_3: year_strategy_3['total_wins']},
        {'': 'Total no. of loss months', strategy_1: year_strategy_1['total_losses'], strategy_2: year_strategy_2['total_losses'], strategy_3: year_strategy_3['total_losses']},
        {'': 'Total PnL', strategy_1: year_strategy_1['total_pnl'], strategy_2: year_strategy_2['total_pnl'], strategy_3: year_strategy_3['total_pnl']},
        {'': 'Average PnL', strategy_1: year_strategy_1['avg_pnl'], strategy_2: year_strategy_2['avg_pnl'], strategy_3: year_strategy_3['avg_pnl']},
        {'': 'Win Percent', strategy_1: year_strategy_1['win_percent'], strategy_2: year_strategy_2['win_percent'], strategy_3: year_strategy_3['win_percent']},
        {'': 'Avg PnL win', strategy_1: year_strategy_1['avg_pnl_win'], strategy_2: year_strategy_2['avg_pnl_win'], strategy_3: year_strategy_3['avg_pnl_win']},
        {'': 'Avg PnL loss', strategy_1: year_strategy_1['avg_pnl_loss'], strategy_2: year_strategy_2['avg_pnl_loss'], strategy_3: year_strategy_3['avg_pnl_loss']},
    ]
    
    result_data = {
        'trade_view': table_trade_data,
        'day_view': table_day_data,
        'week_view': table_week_data,
        'month_view': table_month_data,
        'year_view': table_year_data
    }
    
    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, pd.Series):
                return obj.to_dict()
            return super(NpEncoder, self).default(obj)
    json_result = json.dumps(result_data, cls=NpEncoder)
    print(json_result)
    return json_result

if __name__ == '__main__':
    app.run(debug=True)