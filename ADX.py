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
	c1 = [[0,0, (curr_candle[high_idx]-curr_candle[low_idx])]]
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
		c1.append([pdm, ndm, tr])

	c2=[[100*c1[0][0]/c1[0][2], 100*c1[0][1]/c1[0][2]]]
	c2[0].append(c1[0][2])
	
	prev = c1[0]
	for i in range(1, len(c1)):
		apdm = (prev[0]*(period-1)+c1[i][0])/period
		andm = (prev[1]*(period-1)+c1[i][1])/period
		atr = (prev[2]*(period-1)+c1[i][2])/period
		prev = [apdm, andm, atr]
		PDMI = 100*(apdm/atr)
		NDMI = 100*(andm/atr)
		DX=0
		if(PDMI+NDMI>0):
			DX = 100*abs(PDMI-NDMI)/(PDMI+NDMI)
		c2.append([PDMI, NDMI, DX])

	c1=[]
	adx=[]
	adx.append(c2[0])
	prev_adx = c2[0][2]
	for i in range(1, len(c2)):
		curr_adx = (prev_adx*(period-1)+c2[i][2])/period
		adx.append([c2[i][0], c2[i][1], curr_adx])
		prev_adx=curr_adx

	arr = [0]*(len(c1)+1)
	return(pd.DataFrame(adx, columns=['ADX_PDMI', 'ADX_NDMI','ADX_ADX']))