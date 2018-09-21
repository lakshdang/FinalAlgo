import datetime as dt
import pandas as pd
import numpy as np


#Generates renko blocks of given block size.
#@input - df: dataframe, containing canle data
#		- block_size: integer, % size of first candles opening price to be used as block size in renko
#
#@output - 	dataframe, containing corresponding candles Renkoblock opening price,
#			run of green blocks preceeding and run of red blocks preceeding
#			columns: RenkoBlockOpenPrice, RenkoGreenRun, RenkoRedRun
def renko_gen_blocks(df, block_size):
	numCandles = df.shape[0]
	renko = []
	block_open_price = df.ix[0].open
	block_size = (block_size*block_open_price)/100
	prev_green = True
	prev_red = True
	green_run = 0
	red_run = 0
	for index, candle in df.iterrows():
		if(candle.close-block_open_price>=block_size):
			num_blocks = int((candle.close-block_open_price)/block_size)
			if(prev_green or num_blocks>1):
				if(not prev_green):
					num_blocks-=1
					block_open_price+=block_size
				prev_green=True
				prev_red=False

			block_open_price+=(block_size*num_blocks)
			green_run+=num_blocks
			red_run=0

		elif(candle.close-block_open_price<=-block_size):
			num_blocks = int((candle.close-block_open_price)/-block_size)
			if(prev_red or num_blocks>1):
				if(not prev_red):
					num_blocks-=1
					block_open_price-=block_size
				prev_green=False
				prev_red=True
			block_open_price-=(block_size*num_blocks)
			red_run+=num_blocks
			green_run=0

		renko.append([block_open_price, green_run, red_run])	
	return pd.DataFrame(renko, columns=["RenkoBlockOpenPrice", "RenkoGreenRun", "RenkoRedRun"])


#Calculates EMA value of given period, EMA updated at every new renko block formation
#@input - renko: dataframe, containg candles and renko blocks columns
#		- EMA_len: integer, EMA period
#@output	- dataframe, containing 1 column for renko block EMA value corresponsding to each candle
#			  columns: RenkoEMAperRenko
def renko_EMA_per_Renko(renko, EMA_len):
	weight = 2/(EMA_len+1)
	prev_row = renko.ix[0]
	EMA = [prev_row.RenkoBlockOpenPrice]
	for i in range(1, renko.shape[0]):
		curr_row = renko.ix[i]
		if curr_row.RenkoBlockOpenPrice==prev_row.RenkoBlockOpenPrice:
			EMA.append(EMA[len(EMA)-1])
		else:
			new_EMA = (curr_row.RenkoBlockOpenPrice - EMA[len(EMA)-1])*weight+EMA[len(EMA)-1]
			EMA.append(new_EMA)
		prev_row = curr_row
	return pd.DataFrame(EMA, columns=["RenkoEMAperRenko"])