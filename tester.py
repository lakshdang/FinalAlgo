import datetime as dt
import pandas as pd
import numpy as np
import os
import pathlib

import fetchCandleData as fetchData
import renko
import HeikinAshi as heiken
import TimeConstraints as tc
import ADX
import ParabolicSAR as psar
import relativeStrengthIndex as RSI

import stoploss_Trailing as sl_trail

import combiner_heikin_ashi_tail_basic_time_constrained as chatbtc

import analysis
import cleanData as cd

access_token = "Q6cx4PC21q9xeoUMIxdwL7la8umAlYoZ"
instruments = []
start_date = dt.datetime.strptime("2018-01-01 09:20:00", "%Y-%m-%d %H:%M:%S")
end_date = dt.datetime.strptime("2018-01-05 09:25:00", "%Y-%m-%d %H:%M:%S")
interval = "minute"
directory = "/Users/lakshdang/Desktop/AlgoTrading/CodeForAbbas/WorkingData/EQ/1minute/"
target_dir = "/Users/lakshdang/Desktop/AlgoTrading/CodeForAbbas/WorkingData/EQ/1hour/"
contents = os.listdir(directory)
file = "/Users/lakshdang/Desktop/AlgoTrading/CodeForAbbas/WorkingData/EQ/5minute/HDFC.csv"

# diff = end_date-start_date
# print((diff.days*86400 + diff.seconds)/60)
# df = pd.read_csv(file)
# df = chatbtc.combiner_heikin_ashi_tail_basic_time_constrained_gen_df(df, 0, 2, 0.2, 2, 0.2, 2, 0.2, "10:30:00", "14:30:00", "15:00:00")
# transactions = analysis.minuteDecisionsToTrasactionList(df, 1)
# analysis.basic_analysis(transactions)

print("Making Dir")
pathlib.Path('/Users/lakshdang/Desktop/AlgoTrading/CodeForAbbas/test').mkdir(parents=True, exist_ok=True)

# arr = [["File 1", [1,2,3,4]], ["File 2", [1,2,3,4,5,6]]]
# df = pd.DataFrame(arr, columns=["File", "List"])
# df.to_csv("/Users/lakshdang/Desktop/AlgoTrading/CodeForAbbas/test/listdf.csv")
df = pd.read_csv("/Users/lakshdang/Desktop/AlgoTrading/CodeForAbbas/test/listdf.csv")[1:]
# print(df.dtypes)
arr = df.values[0][2]
arr = arr[1:len(arr)-1]
arr = arr.split(',')
print(arr)
arr = list(map(int, arr))
print(arr)
# print(df)