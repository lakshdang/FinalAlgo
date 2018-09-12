import datetime as dt
import pandas as pd
import numpy as np

def remove_double_candles(df, tol):
	# initialize variables
	candles = df.values
	num_candles = df.shape[0]
	date_idx = df.columns.get_loc("date")
	open_idx = df.columns.get_loc("open")
	close_idx = df.columns.get_loc("close")
	high_idx = df.columns.get_loc("high")
	low_idx = df.columns.get_loc("low")
	vol_idx = df.columns.get_loc("volume")
	curr_time = dt.datetime.strptime(candles[0][date_idx][0:19], "%Y-%m-%d %H:%M:%S").replace(second=0)
	ret = [[candles[0][close_idx], curr_time, candles[0][high_idx], candles[0][low_idx], candles[0][open_idx], candles[0][vol_idx]]]
	start_date = dt.datetime.strptime("2015-01-01 09:20:00", "%Y-%m-%d %H:%M:%S")
	end_date = dt.datetime.strptime("2018-05-01 09:20:00", "%Y-%m-%d %H:%M:%S")
	count = 0

	for i in range(1, num_candles):
		prev_time = curr_time
		curr_time = dt.datetime.strptime(candles[i][date_idx][0:19], "%Y-%m-%d %H:%M:%S").replace(second=0)
		if(curr_time.year<2016):
			continue
		if(curr_time==prev_time):
			continue

		ret.append([candles[i][close_idx], curr_time, candles[i][high_idx], candles[i][low_idx], candles[i][open_idx], candles[i][vol_idx]])
	return pd.DataFrame(ret, columns=['close', 'date', 'high', 'low', 'open', 'volume'])

def merge_minute_candles(df, size):
	candles = df.values
	num_candles = df.shape[0]
	date_idx = df.columns.get_loc("date")
	open_idx = df.columns.get_loc("open")
	close_idx = df.columns.get_loc("close")
	high_idx = df.columns.get_loc("high")
	low_idx = df.columns.get_loc("low")
	vol_idx = df.columns.get_loc("volume")
	curr_candle = candles[0]
	ret=[]
	start_date = dt.datetime.strptime(curr_candle[date_idx], "%Y-%m-%d %H:%M:%S")
	merged_candle = [start_date, curr_candle[open_idx], curr_candle[vol_idx], curr_candle[high_idx], curr_candle[low_idx]]

	for i in range(1, num_candles):
		curr_candle = candles[i]
		curr_date = dt.datetime.strptime(curr_candle[date_idx], "%Y-%m-%d %H:%M:%S")

		diff = curr_date - merged_candle[0]
		if diff>=dt.timedelta(minutes=size):
			merged_candle.append(candles[i-1][close_idx])
			ret.append(merged_candle)
			merged_candle = None


		if merged_candle==None:
			merged_candle = [curr_date, curr_candle[open_idx], curr_candle[vol_idx], curr_candle[high_idx], curr_candle[low_idx]]
			continue

		merged_candle[2]+=curr_candle[vol_idx]
		merged_candle[3] = max(merged_candle[3], curr_candle[high_idx])
		merged_candle[4] = min(merged_candle[4], curr_candle[low_idx])

	return pd.DataFrame(ret, columns=['date', 'open', 'volume', 'high', 'low', 'close'])