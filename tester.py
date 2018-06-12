import datetime as dt
import pandas as pd
import numpy as np
import fetchCandleData as fetchData
import renko
import HeikinAshi as heiken
import TimeConstraints as tc
import combiner_heikin_ashi_tail_basic_time_constrained as chatbtc

access_token = "Q6cx4PC21q9xeoUMIxdwL7la8umAlYoZ"
instruments = []
start_date = dt.datetime.strptime("2015-01-01 09:20:00", "%Y-%m-%d %H:%M:%S")
end_date = dt.datetime.strptime("2018-05-01 09:25:00", "%Y-%m-%d %H:%M:%S")
interval = "minute"

df = pd.read_excel('/Users/lakshdang/Desktop/AlgoTrading/KiteConnect/sub/HDFC_5_min_candles.xlsx')
df = chatbtc.combiner_heikin_ashi_tail_basic_time_constrained_gen_df(df,0,2,0.05,2,0.05,2,0.05,"09:20:00","09:25:00","15:00:00")
# print(df)
df.to_csv("/Users/lakshdang/Desktop/AlgoTrading/HeikinAshiTailTimeResults.csv")