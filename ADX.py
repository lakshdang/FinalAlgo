import datetime as dt
import pandas as pd
import numpy as np

def ADX_gen_df(df, period):
	candles = df.values
	num_candles = df.shape[0]
	open_idx = df.columns.get_loc("open")
	close_idx = df.columns.get_loc("close")
	high_idx = df.columns.get_loc("high")
	low_idx = df.columns.get_loc("low")
	prev_candle = candles[0]
	curr_candle = candles[0]
	ADX = [[0,0, (curr_candle[high_idx]-curr_candle[low_idx])]]
	for i in range(1, num_candles):
		prev_candle = curr_candle
		curr_candle = candles[i]
		mu = curr_candle[high_idx]-prev_candle[high_idx]
		md = prev_candle[low_idx]-curr_candle[low_idx]
		pdm=0
		ndm=0
		tr = max(curr_candle[high_idx]-curr_candle[low_idx], abs(curr_candle[high_idx]-prev_candle[close_idx]), abs(curr_candle[low_idx]-prev_candle[close_idx]))
		if(mu>0 and mu>md):
			pdm = mu

		if(md>0 and md>mu):
			ndm = md

		ADX.append([pdm, ndm, tr])

	ADX_df = pd.DataFrame(ADX, columns=["ADX_PDM", "ADX_NDM", "ADX_TR"])
	ADX_df = ADX_df.ewm(span=14).mean()
	ADX_df["ADX_PDI"] = ADX_df.apply(lambda row: 100*row.ADX_PDM/row.ADX_TR, axis=1)
	ADX_df["ADX_NDI"] = ADX_df.apply(lambda row: 100*row.ADX_NDM/row.ADX_TR, axis=1)
	ADX_df["ADX_diff"] = ADX_df.apply(lambda row: abs(row.ADX_PDI-row.ADX_NDI), axis=1).ewm(span=14).mean()
	ADX_df["ADX_diff"] = ADX_df.apply(lambda row: 100*row.ADX_diff/(row.ADX_PDI+row.ADX_NDI), axis=1).fillna(0)
	# ADX_df["ADX_diff"].fillna(value=0)
	# print(ADX_df)
	return(ADX_df)