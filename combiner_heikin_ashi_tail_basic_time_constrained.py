import datetime as dt
import pandas as pd
import numpy as np
import HeikinAshi as heiken
import TimeConstraints as tc

def combiner_heikin_ashi_tail_basic_time_constrained_gen_df(df, tol, openRunLen, min_open_sum, open_prev_x_len, min_close_sum, close_prev_x_len, scso, open_start_time, open_end_time, close_time):
	ha = heiken.gen_Heikin_Ashi_candles(df)
	df = df.join(ha)
	haptr = heiken.Heikin_Ashi_pos_tail_run(ha, tol/100)
	df = df.join(haptr)
	df = df.join(heiken.Heikin_Ashi_tail_long_open_decision(df, openRunLen, min_open_sum/100, open_prev_x_len))
	df = df.join(heiken.Heikin_Ashi_tail_long_close_decision(df, min_close_sum/100, close_prev_x_len, scso/100))
	df = df.join(tc.set_allow_open_range(df, open_start_time, open_end_time))
	df = df.join(tc.set_close_time(df, close_time))
	df = df.join(combiner_heikin_ashi_tail_basic_time_constrained_gen_long_decisions(df))
	return df

def combiner_heikin_ashi_tail_basic_time_constrained_gen_long_decisions(df):
	num_candles = df.shape[0]
	candles = df.values
	close_idx = df.columns.get_loc("close")
	ha_open_dec_idx = df.columns.get_loc("HA_tail_body_open_decision")
	ha_close_dec_idx = df.columns.get_loc("HA_tail_body_close_decision")
	tc_open_dec_idx = df.columns.get_loc("TimeOpenDecision")
	tc_close_dec_idx = df.columns.get_loc("TimeCloseDecision")
	transaction_open = False
	open_decisions = []
	for i in range(0, num_candles):
		curr_candle = candles[i]
		open_decision = curr_candle[ha_open_dec_idx]+curr_candle[tc_open_dec_idx]>=2
		close_decision = curr_candle[ha_close_dec_idx]+curr_candle[tc_close_dec_idx]>=1 
		if not transaction_open and open_decision:
			open_decisions.append(-1)
			transaction_open = True
		elif transaction_open and close_decision:
			open_decisions.append(1)
			transaction_open = False
		else:
			open_decisions.append(0)
	if(transaction_open):
		open_decisions[len(open_decisions)-1] = 1
	return pd.DataFrame(open_decisions, columns=["LongDecisions"])