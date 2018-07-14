import datetime as dt
import pandas as pd
import numpy as np

def PSAR_gen_df(df, step, ceiling):
	values = df.values
	num_candles = df.shape[0]
	open_idx = df.columns.get_loc("open")
	close_idx = df.columns.get_loc("close")
	high_idx = df.columns.get_loc("high")
	low_idx = df.columns.get_loc("low")
	ret = [[values[0][high_idx], values[0][high_idx], 0, values[0][low_idx], step]]
	ret[0].append((ret[0][1]-ret[0][3])*ret[0][4])
	# print(ret[0])
	# print(ret[0][1])
	# print(ret[0][3])
	# print(ret[0][4])
	for i in range(1, num_candles):
		curr_i_psar_p1 = max(ret[i-1][1]-ret[i-1][5], values[i-1][high_idx], values[max(i-2, 0)][high_idx])
		curr_i_psar_p2 = min(ret[i-1][1]-ret[i-1][5], values[i-1][low_idx], values[max(i-2, 0)][low_idx])
		curr_i_psar = (1-ret[i-1][2])*curr_i_psar_p1+ret[i-1][2]*curr_i_psar_p2
		
		psar = 0
		if ret[i-1][2]==0:
			if values[i][high_idx]<curr_i_psar:
				psar = curr_i_psar
			else:
				psar = ret[i-1][3]
		else:
			if values[i][low_idx]>curr_i_psar:
				psar = curr_i_psar
			else:
				psar = ret[i-1][3]

		rise = 1
		if(psar>values[i][close_idx]):
			rise = 0

		EP_p1 = min(ret[i-1][3], values[i][low_idx])
		EP_p2 = max(ret[i-1][3], values[i][high_idx])
		EP = (1-rise)*EP_p1+rise*EP_p2

		acc=0
		if ret[i-1][2]==rise and not EP==ret[i-1][3] and ret[i-1][4]<ceiling:
			acc = ret[i-1][4]+step
		else:
			if ret[i-1][2]==rise and EP==ret[i-1][3]:
				acc = ret[i-1][4]
			else:
				if not ret[i-1][2]==rise:
					acc = step
				else:
					acc = ceiling
		acc = min(acc, ceiling)


		psar_M_EP_T_acc = (psar-EP)*acc

		ret.append([curr_i_psar, psar, rise, EP, acc, psar_M_EP_T_acc])

	return pd.DataFrame(ret, columns=["initialPSAR", "PSAR", "Trend", "EP", "Acc", "Psar_M_EP_T_acc"])