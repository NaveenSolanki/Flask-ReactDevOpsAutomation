//const file_name = './/data_creation//trading_view_input_data//sma_trading_view_data.csv'
// const file_name = 'C:\Users\navee\OneDrive\Desktop\Naveen\BhaviAI\WebDev\entry_flag__sma_ptn_trading_view_data.csv'
//const file_name = './/data_creation//trading_view_input_data//entry_flag__supertrend_ptn_trading_view_data.csv'
// const file_name = './/data_creation//trading_view_input_data//entry_flag__rsi_ptn_trading_view_data.csv'
// const file_name = 'static//Data//entry_flag__sma_ptn_trading_view_data.csv'
// const file_name = 'static//chart_csv//metric_for_chart.csv'
// import { createChart } from 'lightweight-charts';
const getData = async (metric) => {
  //const res = await fetch('.//data_creation//trading_view_input_data//sma_trading_view_data.csv');
  // const res = await fetch(file_name);
  const res = await fetch('/get_chart_pattern');
  const resp = await res.json();
  console.log(resp);
  const cdata = resp.map((row) => {
    // const [Day, Time, Open, High, Low, Close, sma_40, sma_80, bull_trade_entry_price, bull_trade_exit_price, bear_trade_entry_price,bear_trade_exit_price, Metric] = row.split(',');
    return {
      time: new Date(`${row.Day}, ${row.Time}`).getTime() / 1000,
      open: row.Open * 1,
      high: row.High * 1,
      low: row.Low * 1,
      close: row.Close * 1,
      Metric: row.Metric.trim()
    };
  });
  // Filter out the dataset with the selected metric
  // console.log(cdata);
  const filteredData = cdata.filter((item) => item.Metric.toLowerCase() === metric.toLowerCase());
  // console.log(filteredData)
  return filteredData;
  // return cdata;
};

const getData_sma_40 = async (metric) => {
  //const res = await fetch('sma_trading_view_data.csv');
  // const res = await fetch(file_name);
  const res = await fetch('/get_chart_pattern');
  const resp = await res.json();
  //   console.log(resp);
  const cdata = resp.map((row) => {
    // const [Day, Time, Open, High, Low, Close, sma_40, sma_80, bull_trade_entry_price, bull_trade_exit_price, bear_trade_entry_price,bear_trade_exit_price,Metric] = row.split(',');
    return {
      time: new Date(`${row.Day}, ${row.Time}`).getTime() / 1000,
      value: row.sma_40,
      Metric: row.Metric.trim()
    };
  });
  const filteredData = cdata.filter((item) => item.Metric.toLowerCase() === metric.toLowerCase());

  return filteredData;
  // return cdata;
  //   console.log(cdata);
};

const getData_sma_80 = async (metric) => {
  //const res = await fetch('sma_trading_view_data.csv');
  // const res = await fetch(file_name);
  const res = await fetch('/get_chart_pattern');
  const resp = await res.json();
  //   console.log(resp);
  const cdata = resp.map((row) => {
    // const [Day, Time, Open, High, Low, Close, sma_40, sma_80, bull_trade_entry_price, bull_trade_exit_price, bear_trade_entry_price,bear_trade_exit_price,Metric] = row.split(',');
    return {
      time: new Date(`${row.Day}, ${row.Time}`).getTime() / 1000,
      value: row.sma_80,
      Metric: row.Metric.trim()
    };
  });
  const filteredData = cdata.filter((item) => item.Metric.toLowerCase() === metric.toLowerCase());

  return filteredData;
  // return cdata;
  //   console.log(cdata);
};

const getData_buy_entry = async () => {
  //const res = await fetch('sma_trading_view_data.csv');
  // const res = await fetch(file_name);
  // const resp = await res.text();
  const res = await fetch('/get_chart_pattern');
  const resp = await res.json();
  //   console.log(resp);
  const cdata = resp.map((row) => {
    // const [Day, Time, Open, High, Low, Close, sma_40, sma_80, bull_trade_entry_price, bull_trade_exit_price, bear_trade_entry_price,bear_trade_exit_price] = row.split(',');
    return {
      time: new Date(`${row.Day}, ${row.Time}`).getTime() / 1000,
      value: row.bull_trade_entry_price
    };
  });
  return cdata;
  //   console.log(cdata);
};

// getData();

const displayChartDay = async (chartContainerId, metric) => {
  const chartProperties = {
    width: 900,
    height: 450,
    timeScale: {
      timeVisible: true,
      secondsVisible: true,
    },
  };
  
  const domElement = document.getElementById(chartContainerId);
  domElement.classList.add('chartForDay');
  // console.log('domElement:', domElement);
  const chart = LightweightCharts.createChart(domElement, chartProperties);
  const candleseries = chart.addCandlestickSeries();
  const klinedata = await getData(metric);

  candleseries.setData(klinedata);
  // console.log(typeof(metric));
  if (metric === 'sma') {
    const smaline = chart.addLineSeries({ lineWidth: 1, title: 'sma_40' });
    const smalinedata = await getData_sma_40(metric);
    smaline.setData(smalinedata);
  
    const smaline_80 = chart.addLineSeries({ lineWidth: 1, title: 'sma_80', color: 'orange' });
    const smalinedata_80 = await getData_sma_80(metric);
    smaline_80.setData(smalinedata_80);    
  }else if (metric === 'supertrend'){
    const smaline = chart.addLineSeries({ lineWidth: 1, title: 'sma_40' });
    const smalinedata = await getData_sma_40(metric);
    smaline.setData(smalinedata);
  
    const smaline_80 = chart.addLineSeries({ lineWidth: 1, title: 'sma_80', color: 'orange' });
    const smalinedata_80 = await getData_sma_80(metric);
    smaline_80.setData(smalinedata_80); 
  }


//  const buy_entry_line = chart.addLineSeries({lineWidth:2, title: 'buy_entry', color: 'green'});
//  const buy_entry_line_data = await getData_buy_entry();
//  buy_entry_line.setData(buy_entry_line_data);

const data = await getData_buy_entry();
// determining the dates for the 'buy' and 'sell' markers added below.
//const datesForMarkers = [data[data.length - 39], data[data.length - 19]];
//let indexOfMinPrice = 0;
//for (let i = 0; i < data.length; i++) {
//    if (datesForMarkers[i].high < datesForMarkers[indexOfMinPrice].high) {
//        indexOfMinPrice = i;
//    }
//}

const markers = [
	{
		time: data[data.length - 48].time,
		position: 'aboveBar',
		color: '#f68410',
		shape: 'circle',
		text: 'D',
	},
];
for (let i = 0; i < data.length; i++) {
	if (data[i].value > 1) {
		markers.push({
			time: data[i].time,
			position: 'belowBar',
			color: '#2196F3',
			shape: 'arrowUp',
			text: 'B',// + Math.floor(data[i].value + 2),
		});
	}
}
candleseries.setMarkers(markers);

};
const displayChartMonth = async (chartContainerId, metric) => {
  const chartProperties = {
    width: 900,
    height: 450,
    timeScale: {
      timeVisible: true,
      secondsVisible: true,
    },
  };
  
  const domElement = document.getElementById(chartContainerId);
  domElement.classList.add('chartForMonth');
  // console.log('domElement:', domElement);
  const chart = LightweightCharts.createChart(domElement, chartProperties);
  const candleseries = chart.addCandlestickSeries();
  const klinedata = await getData(metric);
  candleseries.setData(klinedata);

  if (metric === 'sma') {
    const smaline = chart.addLineSeries({ lineWidth: 1, title: 'sma_40' });
    const smalinedata = await getData_sma_40(metric);
    smaline.setData(smalinedata);
  
    const smaline_80 = chart.addLineSeries({ lineWidth: 1, title: 'sma_80', color: 'orange' });
    const smalinedata_80 = await getData_sma_80(metric);
    smaline_80.setData(smalinedata_80);    
  }else if (metric === 'supertrend'){
    const smaline = chart.addLineSeries({ lineWidth: 1, title: 'sma_40' });
    const smalinedata = await getData_sma_40(metric);
    smaline.setData(smalinedata);
  
    const smaline_80 = chart.addLineSeries({ lineWidth: 1, title: 'sma_80', color: 'orange' });
    const smalinedata_80 = await getData_sma_80(metric);
    smaline_80.setData(smalinedata_80); 
  }


//  const buy_entry_line = chart.addLineSeries({lineWidth:2, title: 'buy_entry', color: 'green'});
//  const buy_entry_line_data = await getData_buy_entry();
//  buy_entry_line.setData(buy_entry_line_data);

const data = await getData_buy_entry();
// determining the dates for the 'buy' and 'sell' markers added below.
//const datesForMarkers = [data[data.length - 39], data[data.length - 19]];
//let indexOfMinPrice = 0;
//for (let i = 0; i < data.length; i++) {
//    if (datesForMarkers[i].high < datesForMarkers[indexOfMinPrice].high) {
//        indexOfMinPrice = i;
//    }
//}

const markers = [
	{
		time: data[data.length - 48].time,
		position: 'aboveBar',
		color: '#f68410',
		shape: 'circle',
		text: 'D',
	},
];
for (let i = 0; i < data.length; i++) {
	if (data[i].value > 1) {
		markers.push({
			time: data[i].time,
			position: 'belowBar',
			color: '#2196F3',
			shape: 'arrowUp',
			text: 'B',// + Math.floor(data[i].value + 2),
		});
	}
}
candleseries.setMarkers(markers);

};
const displayChartYear = async (chartContainerId, metric) => {
  const chartProperties = {
    width: 900,
    height: 450,
    timeScale: {
      timeVisible: true,
      secondsVisible: true,
    },
  };
  
  const domElement = document.getElementById(chartContainerId);
  domElement.classList.add('chartForYear');
  // console.log('domElement:', domElement);
  const chart = LightweightCharts.createChart(domElement, chartProperties);
  const candleseries = chart.addCandlestickSeries();
  const klinedata = await getData(metric);
  candleseries.setData(klinedata);

  if (metric === 'sma') {
    const smaline = chart.addLineSeries({ lineWidth: 1, title: 'sma_40' });
    const smalinedata = await getData_sma_40(metric);
    smaline.setData(smalinedata);
  
    const smaline_80 = chart.addLineSeries({ lineWidth: 1, title: 'sma_80', color: 'orange' });
    const smalinedata_80 = await getData_sma_80(metric);
    smaline_80.setData(smalinedata_80);    
  }else if (metric === 'supertrend'){
    const smaline = chart.addLineSeries({ lineWidth: 1, title: 'sma_40' });
    const smalinedata = await getData_sma_40(metric);
    smaline.setData(smalinedata);
  
    const smaline_80 = chart.addLineSeries({ lineWidth: 1, title: 'sma_80', color: 'orange' });
    const smalinedata_80 = await getData_sma_80(metric);
    smaline_80.setData(smalinedata_80); 
  }


//  const buy_entry_line = chart.addLineSeries({lineWidth:2, title: 'buy_entry', color: 'green'});
//  const buy_entry_line_data = await getData_buy_entry();
//  buy_entry_line.setData(buy_entry_line_data);

const data = await getData_buy_entry();
// determining the dates for the 'buy' and 'sell' markers added below.
//const datesForMarkers = [data[data.length - 39], data[data.length - 19]];
//let indexOfMinPrice = 0;
//for (let i = 0; i < data.length; i++) {
//    if (datesForMarkers[i].high < datesForMarkers[indexOfMinPrice].high) {
//        indexOfMinPrice = i;
//    }
//}

const markers = [
	{
		time: data[data.length - 48].time,
		position: 'aboveBar',
		color: '#f68410',
		shape: 'circle',
		text: 'D',
	},
];
for (let i = 0; i < data.length; i++) {
	if (data[i].value > 1) {
		markers.push({
			time: data[i].time,
			position: 'belowBar',
			color: '#2196F3',
			shape: 'arrowUp',
			text: 'B',// + Math.floor(data[i].value + 2),
		});
	}
}
candleseries.setMarkers(markers);

};
// displayChart();
export {displayChartDay, displayChartMonth, displayChartYear}