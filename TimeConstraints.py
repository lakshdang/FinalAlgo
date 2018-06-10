import pandas as pd
import numpy as np
from dateutil.parser import parse

def set_allow_open_range(df, start_time, end_time):
	num_candles = df.shape[0]
	candles = df.values
	date_idx = df.columns.get_loc('date')
	time_open_decision = []
	start_time = parse(start_time).time()
	end_time = parse(end_time).time()
	for i in range(0, num_candles):
		curr_time = parse(candles[i][date_idx]).time()
		if(curr_time>=start_time and curr_time<end_time):
			time_open_decision.append(1)
		else:
			time_open_decision.append(0)

	return pd.DataFrame(time_open_decision, columns=["TimeOpenDecision"])


def set_close_time(df, close_time):
	num_candles = df.shape[0]
	candles = df.values
	date_idx = df.columns.get_loc('date')
	time_close_decision = []
	close_time = parse(close_time).time()
	for i in range(0, num_candles):
		curr_time = parse(candles[i][date_idx]).time()
		if(curr_time>=close_time):
			time_close_decision.append(1)
		else:
			time_close_decision.append(0)

	return pd.DataFrame(time_close_decision, columns=["TimeCloseDecision"])
