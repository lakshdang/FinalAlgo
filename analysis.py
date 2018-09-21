import datetime as dt
import pandas as pd
import numpy as np

def basic_analysis(transactions):
	num_transactions = transactions.shape[0]
	values = transactions.values
	transaction_sign_idx = transactions.columns.get_loc("TransactionSign")
	open_time_idx = transactions.columns.get_loc("OpenTime")
	close_time_idx = transactions.columns.get_loc("CloseTime")
	open_price_idx = transactions.columns.get_loc("OpenPrice")
	close_price_idx = transactions.columns.get_loc("ClosePrice")
	
	num_winning_trades = 0
	num_losing_trades = 0
	mean_return = 0
	best_trade = 0
	worst_trade = 0
	return_standard_deviation = 0
	trade_avg_time = 0

	trade_returns = []

	for i in range (0, num_transactions):
		curr_open_time = dt.datetime.strptime(values[i][close_time_idx], "%Y-%m-%d %H:%M:%S")
		curr_close_time = dt.datetime.strptime(values[i][open_time_idx], "%Y-%m-%d %H:%M:%S")
		curr_profit = 100*values[i][transaction_sign_idx]*((values[i][close_price_idx]-values[i][open_price_idx])/values[i][open_price_idx])
		diff = curr_close_time - curr_open_time

		trade_avg_time+=(diff.days*86400 + diff.seconds)/60
		trade_returns.append(curr_profit)

		if(curr_profit>0):
			num_winning_trades+=1
		else:
			num_losing_trades+=1

		mean_return += curr_profit
		best_trade = max(best_trade, curr_profit)
		worst_trade = min(worst_trade, curr_profit)
	
	trade_returns = pd.Series(trade_returns)
	return_standard_deviation = trade_returns.std()
	maxDrawdown = calcMaxDrawdown(trade_returns)
	mean_return = mean_return/num_transactions
	risk_adjusted_return = mean_return/return_standard_deviation
	num_winning_trades = 100*(num_winning_trades/num_transactions)
	num_losing_trades = 100*(num_losing_trades/num_transactions)
	trade_avg_time = trade_avg_time/num_transactions

	print(num_transactions)
	print(num_winning_trades)
	print(num_losing_trades)
	print(risk_adjusted_return)
	print(mean_return)
	print(return_standard_deviation)
	print(best_trade)
	print(worst_trade)
	print(trade_avg_time)
	print(maxDrawdown)


def calcMaxDrawdown(transaction_returns):
	sum_left = [transaction_returns[0]]
	for i in range (1, transaction_returns.size):
		sum_left.append(min(transaction_returns[1], transaction_returns[1]+sum_left[i-1]))
	return min(sum_left)

def minuteDecisionsToTrasactionList(df, transaction_sign):
	values = df.values
	transaction_idx = close_idx = df.columns.get_loc("TradeDecisions")
	close_idx = df.columns.get_loc("close")
	date_idx = df.columns.get_loc("date")
	num_candles = df.shape[0]
	transaction_open = False
	transactions = []
	curr_transaction = []
	num_transactions = df.shape[0]
	for i in range(0, num_candles):
		if(not transaction_open and values[i][transaction_idx]==1):
			curr_transaction = [transaction_sign, values[i][date_idx], values[i][close_idx]]
			transaction_open = True
		
		elif(transaction_open and values[i][transaction_idx]==-1):
			curr_transaction.extend([values[i][date_idx], values[i][close_idx]])
			transaction_open = False
			transactions.append(curr_transaction)
			curr_transaction = []
	return pd.DataFrame(transactions, columns=["TransactionSign", "OpenTime", "OpenPrice", "CloseTime", "ClosePrice"])