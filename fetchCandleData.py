from kiteconnect import KiteConnect
import datetime as dt
import pandas as pd

polling_intervals = {
	"minute" :  30,
	"3minute" :  90,
	"5minute" :  90,
	"10minute" :  90,
	"15minute" : 180,
	"30minute" : 180,
	"60minute" : 365,
	"day" : 2000
}

# Get dataframe of all currently trading instruments
def fetch_all_instruments(access_token):
	kite = KiteConnect(access_token=access_token, api_key="wr4m14tgk52gn65y")
	instruments = kite.instruments()
	df = pd.DataFrame(instruments)
	return df

# Retrieve canle data for single token for any time range & candle interval
# returns dataframe
def fetch_data(access_token, instrument, start_date, end_date, interval):
	if(interval not in polling_intervals.keys()):
		print("Invalid Interval")
		return null

	max_days = polling_intervals[interval]
	historical_data = []
	kite = KiteConnect(access_token=access_token, api_key="wr4m14tgk52gn65y")
	while(start_date < end_date):
		historical_data.extend(kite.historical_data(instrument, start_date, min(start_date + dt.timedelta(days=max_days), end_date), interval));
		start_date += dt.timedelta(days=max_days)


	df = pd.DataFrame(historical_data);
	return df

# Retrieve candle data for multiple tokens for any time range & candle interval
# saves files in directory provided(Last parameter)
# return nothing
def fetch_data_multiple(access_token, instruments, start_date, end_date, interval, dir):
	for i in range(0, len(instruments)):
		instrument = instruments[i]
		t = dt.datetime.now().strftime("%I_%M_%p_%B%d_%Y")
		file = dir+str(instrument)+".csv"
		data = fetch_data(access_token, instrument, start_date, end_date, interval)
		data.to_csv(file)