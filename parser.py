def num_if_can(x):
	try:
		return int(x)
	except ValueError:
		pass

	try:
		return float(x)
	except ValueError:
		return x

def parseFile(fileName, name, maxTimestamp = 1_000_000):
	with open(fileName) as file:
		lines = file.read().split('\n')

	fields = lines[0].split(';')
	splitLines = [x.split(';') for x in lines[1:]]
	processedLines = [[num_if_can(x) for x in line] for line in splitLines]
	data = [{fields[i]: line[i] for i in range(len(line))} for line in processedLines if len(line) == len(fields)]

	productNames = list(set([x[name] for x in data])) # ['TOMATOES', 'EMERALDS']
	return {productName: [x for x in data if x[name] == productName and x['timestamp'] < maxTimestamp] for productName in productNames}
	

day = input('Enter day ([-1]/-2): ')
if not day:
	day = -1

tickCount = input('Enter tick count ([1000]): ')
if not tickCount:
	tickCount = 1_000
tickCount = int(tickCount)

tickLength = 1_000
maxTimestamp = tickLength * tickCount
pricesFileName = f'prices_round_0_day_{day}.csv'
pricesData = parseFile(pricesFileName, 'product', maxTimestamp)

tradesFileName = f'trades_round_0_day_{day}.csv'
tradesData = parseFile(tradesFileName, 'symbol', maxTimestamp)



import matplotlib.pyplot as plt

symbol = 'TOMATOES'
# symbol = 'EMERALDS'

userSymbol = input('Product Name ([TOMATOES]/EMERALDS): ').upper()
if userSymbol == 'E':
	symbol = 'EMERALDS'
elif userSymbol == 'T':
	symbol = 'TOMATOES'
elif userSymbol:
	symbol = userSymbol

pricesTimes = [x['timestamp'] for x in pricesData[symbol]]
bidPrices1 = [x['bid_price_1'] for x in pricesData[symbol]]
bidPrices2 = [x['bid_price_2'] for x in pricesData[symbol]]
askPrices1 = [x['ask_price_1'] for x in pricesData[symbol]]
askPrices2 = [x['ask_price_2'] for x in pricesData[symbol]]

plt.plot(pricesTimes, bidPrices1, 'r', label = 'Bid Prices 1', linewidth = 0.5)
# plt.plot(pricesTimes, bidPrices2, 'tab:orange', label = 'Bid Prices 2', linewidth = 0.25, antialiased = False)
plt.plot(pricesTimes, askPrices1, 'g', label = 'Ask Prices 1', linewidth = 0.5)
# plt.plot(pricesTimes, askPrices2, 'c', label = 'Ask Prices 2', linewidth = 0.25, antialiased = False)

tradesTimes = [x['timestamp'] for x in tradesData[symbol]]
tradesPrices = [x['price'] for x in tradesData[symbol]]

plt.plot(tradesTimes, tradesPrices, 'co', label = 'Trade Prices', ms = 2)


plt.xlabel("times")
plt.ylabel("prices")

plt.show()
