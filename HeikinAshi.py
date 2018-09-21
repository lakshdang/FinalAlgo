import datetime as dt
import pandas as pd
import numpy as np

#HA = Heikin Ashi

#Generates Heikin Ashi candles
#@input - df: dataframe, containing candle data
#
#@output - 	dataframe, containing corresponding candles HeikinAshi open, close, high, low
#			columns: HeikinAshiOpen, HeikinAshiClose, HeikinAshiHigh, HeikinAshiLow
def gen_Heikin_Ashi_candles(df):
	ha=[]
	if(df.shape[0]==0):
		return pd.DataFrame(ha,  columns=["HeikinAshiOpen", "HeikinAshiClose", "HeikinAshiHigh", "HeikinAshiLow"])

	ha_candles = df.values
	open_idx = df.columns.get_loc("open")
	close_idx = df.columns.get_loc("close")
	high_idx = df.columns.get_loc("high")
	low_idx = df.columns.get_loc("low")

	ha_open = (df.ix[0].open+df.ix[0].close)/2
	ha_close = (df.ix[0].open+df.ix[0].close+df.ix[0].high+df.ix[0].low)/4
	ha_high = df.ix[0].high
	ha_low = df.ix[0].low
	prev = [ha_open, ha_close, ha_high, ha_low]
	ha.append(prev)

	for i in range(1, df.shape[0]):
		curr_candle = ha_candles[i]
		ha_open = (prev[0]+prev[1])/2
		ha_close = (curr_candle[close_idx]+curr_candle[open_idx]+curr_candle[high_idx]+curr_candle[low_idx])/4
		ha_high = max(ha_open, curr_candle[high_idx])
		ha_low = min(ha_open, curr_candle[low_idx])
		prev = [ha_open, ha_close, ha_high, ha_low]
		ha.append(prev)
		
	return pd.DataFrame(ha, columns=["HeikinAshiOpen", "HeikinAshiClose", "HeikinAshiHigh", "HeikinAshiLow"])

#Generates HA candles' body size, cumulitive body size for all preceeding candles, 
#count of current run of HA candles whose HA tail size is within given tolerance
#@input - df: dataframe, containing HA candle data
#		- tol: Integer, % of body size which is acceptable limit for tail size 
#
#@output - 	dataframe, containing corresponding candles HeikinAshi pos tail run, curr candle HA body,
#			cumulative body size (inclusive of current candle)
#			columns: HeikinAshiPosRun, CurrCandleBody, BodyCumSum
def Heikin_Ashi_pos_tail_run(df, tol):
	ptrvo = []
	num_candles = df.shape[0]
	ha_candles = df.values
	ha_open_idx = df.columns.get_loc("HeikinAshiOpen")
	ha_close_idx = df.columns.get_loc("HeikinAshiClose")
	ha_high_idx = df.columns.get_loc("HeikinAshiHigh")
	ha_low_idx = df.columns.get_loc("HeikinAshiLow")

	curr_run = 0
	curr_sum = 0
	body_sum = 0

	for i in range(0, num_candles):
		curr_candle = ha_candles[i]
		curr_body = curr_candle[ha_close_idx]-curr_candle[ha_open_idx]
		body_sum += curr_body
		curr_tol = tol * (curr_body)
		
		if curr_tol+curr_candle[ha_low_idx]>=curr_candle[ha_open_idx]:
			curr_run+=1
			curr_sum+=curr_body
		else:
			curr_run = 0
			curr_sum = 0

		ptrvo.append([curr_run, curr_body, body_sum])

	return pd.DataFrame(ptrvo, columns=["HeikinAshiPosRun", "CurrCandleBody", "BodyCumSum"])

#Generate open decision for current candle(Assuming no transaction open at current candle open) 
#based on current HA candles pos tail run length and cumulative body sum for prev "x" candles meeting threshold
#@input - df: dataframe, containing HA candle data (gen_Heikin_Ashi_candles) + HA pos_tail_run data (Heikin_Ashi_pos_tail_run)
#		- runlen: Integer, threshold value for pos tail run length
#		- prev_x_len: Integer, number of previous candles we consider cumulative body sum for
#		- min_sum: Integer, cumulative body sum threshold for cumulative body sum of prev_x_len candles
#
#@output	- dataframe, containing long transaction open decision for current candle assuming no transaction open
# 			  columns: HA_tail_body_open_decision
def Heikin_Ashi_tail_long_open_decision(df, runlen, prev_x_len, min_sum):
	num_candles = df.shape[0]
	open_decision = []
	candles = df.values
	candle_close_idx = df.columns.get_loc("close")
	ha_posrunlen_idx = df.columns.get_loc("HeikinAshiPosRun")
	ha_bodysum_idx = df.columns.get_loc("BodyCumSum")

	for i in range(0, num_candles):
		curr_candle = candles[i]
		prev_x_sum = curr_candle[ha_bodysum_idx]
		curr_min_sum = min_sum*curr_candle[candle_close_idx]
		if(i>=prev_x_len):
			prev_x_sum-=candles[i-prev_x_len][ha_bodysum_idx]

		if curr_candle[ha_posrunlen_idx]>=runlen and prev_x_sum>=curr_min_sum:
			open_decision.append(1)
		else:
			open_decision.append(0)
	return pd.DataFrame(open_decision, columns=["HA_tail_body_open_decision"])

#Generate close decision for current candle(Assuming transaction is open at current candle open) 
#based on current HA candles cumulative body sum for prev "x" candles meeting threshold 
#or single candle body meeting separate threshold
#@input - df: dataframe, containing HA candle data (gen_Heikin_Ashi_candles) + HA pos_tail_run data (Heikin_Ashi_pos_tail_run)
#		- prev_x_len: Integer, number of previous candles we consider cumulative body sum for
#		- min_sum: Integer, cumulative body sum threshold for cumulative body sum of prev_x_len candles (must be less than negative of this value)
#		- single_candle_sell_off_threshold: Integer, self-explanatory
#
#@output	- dataframe, containing long transaction close decision for current candle assuming long transaction is open
# 			  columns: HA_tail_body_close_decision
def Heikin_Ashi_tail_long_close_decision(df, prev_x_len, min_sum, single_candle_sell_off_threshold):
	num_candles = df.shape[0]
	close_decision = []
	candles = df.values
	candle_close_idx = df.columns.get_loc("close")
	ha_bodysum_idx = df.columns.get_loc("BodyCumSum")
	ha_currbody_idx = df.columns.get_loc("CurrCandleBody")

	for i in range(0, num_candles):
		curr_candle = candles[i]
		prev_x_sum = curr_candle[ha_bodysum_idx]
		curr_min_sum = -min_sum*curr_candle[candle_close_idx]
		if(i>=prev_x_len):
			prev_x_sum-=candles[i-prev_x_len][ha_bodysum_idx]

		if curr_candle[ha_currbody_idx]<=-single_candle_sell_off_threshold*curr_candle[candle_close_idx] or prev_x_sum<=curr_min_sum:
			close_decision.append(1)
		else:
			close_decision.append(0)
	return pd.DataFrame(close_decision, columns=["HA_tail_body_close_decision"])