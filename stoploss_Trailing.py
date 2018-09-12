def stoploss_trail_long(otp, low, high, cap):
	ret = [otp, 0]
	if(cap>otp-low):
		ret[1] = 1
	ret[0] += max(0, high-otp//cap)
	return ret

def stoploss_trail_short(otp, low, high, cap):
	ret = [otp, 0]
	if(cap>high-otp):
		ret[1] = 1
	ret[0] += min(0, otp-low//cap)
	return ret