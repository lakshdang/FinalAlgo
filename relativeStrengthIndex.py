import datetime as dt
import pandas as pd
import numpy as np

def rsi_gen_df(df, period):
	candles = df.values
	num_candles = df.shape[0]
	open_idx = df.columns.get_loc("open")
	close_idx = df.columns.get_loc("close")
	high_idx = df.columns.get_loc("high")
	low_idx = df.columns.get_loc("low")
	net_gain = 0
	net_loss = 0
	
	ret = [[max(candles[0][close_idx]-candles[0][open_idx], 0), abs(min(candles[0][close_idx]-candles[0][open_idx], 0))]]
	for i in range(1, num_candles):
		avg_gain = (ret[i-1][0]*(period-1) + max(candles[i][close_idx]-candles[i-1][close_idx], 0))/period
		avg_loss = (ret[i-1][1]*(period-1) + abs(min(candles[i][close_idx]-candles[i-1][close_idx], 0)))/period
		ret.append([avg_gain, avg_loss])

	start = 0
	while(ret[start][1]==0):
		ret[start].append([None, None])
		start+=1

	for i in range(start, num_candles):
		rs = ret[i][0]/ret[i][1]
		rsi = 100 - (100/(1+rs))
		ret[i].extend([rs, rsi])

	ret = pd.DataFrame(ret, columns=["AvgGain", "AvgLoss", "RS", "RSI"])
	return ret