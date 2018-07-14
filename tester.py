import datetime as dt
import pandas as pd
import numpy as np
import fetchCandleData as fetchData
import renko
import HeikinAshi as heiken
import TimeConstraints as tc
import combiner_heikin_ashi_tail_basic_time_constrained as chatbtc
import ADX
import ParabolicSAR as psar
import relativeStrengthIndex as RSI

access_token = "Q6cx4PC21q9xeoUMIxdwL7la8umAlYoZ"
instruments = []
start_date = dt.datetime.strptime("2015-01-01 09:20:00", "%Y-%m-%d %H:%M:%S")
end_date = dt.datetime.strptime("2018-05-01 09:25:00", "%Y-%m-%d %H:%M:%S")
interval = "minute"

df = pd.read_excel('/Users/lakshdang/Desktop/AlgoTrading/KiteConnect/sub/HDFC_5_min_candles.xlsx')
df = df.join(RSI.rsi_gen_df(df, 14))
print(df)