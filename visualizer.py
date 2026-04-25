def num_if_can(x):
	try:
		return int(x)
	except ValueError:
		pass

	try:
		return float(x)
	except ValueError:
		pass
	
	if not x:
		return None
	return x

def parseFile(fileName, name, maxTimestamp = 1_000_000) -> dict[str, list[dict]]:
	with open(fileName) as file:
		lines = file.read().split('\n')
	fields = lines[0].split(';')
	splitLines = [x.split(';') for x in lines[1:]]
	processedLines = [[num_if_can(x) for x in line] for line in splitLines]
	data = [{fields[i]: line[i] for i in range(len(line))} for line in processedLines if len(line) == len(fields)]

	productNames = list(set([x[name] for x in data])) # ['TOMATOES', 'EMERALDS']
	return {productName: [x for x in data if x[name] == productName and x['timestamp'] < maxTimestamp] for productName in productNames}
	

def getValueFromList(msg: str, possibleInputs: list | tuple, defaultValue = None) -> str:
	if not possibleInputs:
		raise ValueError
	if not defaultValue:
		defaultValue = possibleInput[0]
	inputMessage = msg + ' ('
	for possibleInput in possibleInputs:
		possibleLeftBracket = '[' if possibleInput == defaultValue else ''
		possibleRightBracket = ']' if possibleInput == defaultValue else ''
		inputMessage += possibleLeftBracket + str(possibleInput) + possibleRightBracket + '/'
	inputMessage = inputMessage[:-1]  # remove final slash
	inputMessage += '): '
	userInput = input(inputMessage)
	if not userInput:
		userInput = str(defaultValue)
	return userInput

currRound = int(getValueFromList('Enter round', validRounds := [0, 1, 2, 3], validRounds[-1]))

validDays = [-2, -1]
if currRound == 1 or currRound == 2:
	validDays = [-2, -1, 0]
if currRound >= 3:
	validDays = [0, 1, 2]
day = getValueFromList('Enter day', validDays, validDays[-1])

tickCount = input('Enter tick count (1-[10000]): ')
if not tickCount:
	tickCount = 10_000
tickCount = int(tickCount)

tickLength = 100
maxTimestamp = tickLength * tickCount
pricesFileName = f'data/round_{currRound}/prices_round_{currRound}_day_{day}.csv'
pricesData = parseFile(pricesFileName, 'product', maxTimestamp)

tradesFileName = f'data/round_{currRound}/trades_round_{currRound}_day_{day}.csv'
tradesData = parseFile(tradesFileName, 'symbol', maxTimestamp)


import matplotlib.pyplot as plt

plt.style.use('dark_background')

print('[Case-insensitive. First letter of product is sufficient. For Velvetfruit Vouchers (i.e. VEV_5400), v followed by first 2 digits is sufficient (i.e. v54).]')
validProducts = sorted(pricesData.keys())
symbol = getValueFromList('Product Name', validProducts, validProducts[0]).upper()
if symbol == 'E':
	symbol = 'EMERALDS'
elif symbol == 'T':
	symbol = 'TOMATOES'
elif symbol == 'I':
	symbol = 'INTARIAN_PEPPER_ROOT'
elif symbol == 'A':
	symbol = 'ASH_COATED_OSMIUM'
elif symbol == 'H':
	symbol = 'HYDROGEL_PACK'
elif symbol == 'V':
	symbol = 'VELVETFRUIT_EXTRACT'
elif symbol == 'V40':
	symbol = 'VEV_4000'
elif symbol == 'V45':
	symbol = 'VEV_4500'
elif symbol == 'V50':
	symbol = 'VEV_5000'
elif symbol == 'V51':
	symbol = 'VEV_5100'
elif symbol == 'V52':
	symbol = 'VEV_5200'
elif symbol == 'V53':
	symbol = 'VEV_5300'
elif symbol == 'V54':
	symbol = 'VEV_5400'
elif symbol == 'V55':
	symbol = 'VEV_5500'
elif symbol == 'V60':
	symbol = 'VEV_6000'
elif symbol == 'V65':
	symbol = 'VEV_6500'


pricesTimes = [x['timestamp'] for x in pricesData[symbol]]
bidPrices1 = [x['bid_price_1'] for x in pricesData[symbol]]
askPrices1 = [x['ask_price_1'] for x in pricesData[symbol]]

if True and symbol == 'INTARIAN_PEPPER_ROOT':  # this block was written by chatgpt. disable by changing True to False
	# ----------------------------------------------------------
	import numpy as np

	pricesTimesArr = np.array(pricesTimes, dtype=float)
	bidPrices1Arr = np.array([np.nan if v is None else v for v in bidPrices1], dtype=float)

	window = 30
	percentile = 90

	upperEnvelope = np.array([
	    np.nanpercentile(bidPrices1Arr[max(0, i-window):i+1], percentile)
	    for i in range(len(bidPrices1Arr))
	])

	# take only points where the envelope increases (staircase "tops")
	validMask = ~np.isnan(upperEnvelope)
	envelopeDiff = np.diff(upperEnvelope, prepend=np.nan)

	stairTopMask = validMask & (envelopeDiff > 0)

	# fit regression only on those points
	slope, intercept = np.polyfit(
	    pricesTimesArr[stairTopMask],
	    upperEnvelope[stairTopMask],
	    1
	)

	regressionLine = slope * pricesTimesArr + intercept

	col = 'white'
	line_width = 1
	
	plt.plot(pricesTimesArr, regressionLine + 0, color=col, linewidth=line_width)
	plt.plot(pricesTimesArr, regressionLine - 3, color=col, linewidth=line_width)
	plt.plot(pricesTimesArr, regressionLine + 13, color=col, linewidth=line_width)
	plt.plot(pricesTimesArr, regressionLine + 16, color=col, linewidth=line_width)

	plt.plot(pricesTimesArr, 0.001 * pricesTimesArr + 12_000, color=col, linewidth=line_width)

	print(slope, intercept)

	# plt.plot(pricesTimesArr, upperEnvelope, color="orange", linewidth=1, label=f"Rolling {percentile}th percentile (envelope)")
	# plt.scatter(pricesTimesArr[stairTopMask], upperEnvelope[stairTopMask], color="white", s=10, label="Stair top points used")

	# plt.legend()

	# --------------------------------------------



plt.plot(pricesTimes, bidPrices1, 'r', label = 'Bid Prices 1', linewidth = 0.5)
plt.plot(pricesTimes, askPrices1, 'g', label = 'Ask Prices 1', linewidth = 0.5)

try:
	tradesTimes = [x['timestamp'] for x in tradesData[symbol]]
	tradesPrices = [x['price'] for x in tradesData[symbol]]
except KeyError:
	tradesTimes = []
	tradesPrices = []

plt.plot(tradesTimes, tradesPrices, 'co', label = 'Trade Prices', ms = 2)


plt.xlabel("times")
plt.ylabel("prices")

plt.show()
