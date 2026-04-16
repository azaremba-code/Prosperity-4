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

def parseFile(fileName, name, maxTimestamp = 1_000_000):
	with open(fileName) as file:
		lines = file.read().split('\n')

	fields = lines[0].split(';')
	splitLines = [x.split(';') for x in lines[1:]]
	processedLines = [[num_if_can(x) for x in line] for line in splitLines]
	data = [{fields[i]: line[i] for i in range(len(line))} for line in processedLines if len(line) == len(fields)]

	productNames = list(set([x[name] for x in data])) # ['TOMATOES', 'EMERALDS']
	return {productName: [x for x in data if x[name] == productName and x['timestamp'] < maxTimestamp] for productName in productNames}
	

curr_round = input('Enter round (0/[1]/2)')
if not curr_round:
	curr_round = '1'

day = input('Enter day ([0]/-1/-2): ')
if not day:
	day = '0'

tickCount = input('Enter tick count (1-[10000]): ')
if not tickCount:
	tickCount = 10_000
tickCount = int(tickCount)

tickLength = 1_00
maxTimestamp = tickLength * tickCount
pricesFileName = f'data/prices_round_{curr_round}_day_{day}.csv'
pricesData = parseFile(pricesFileName, 'product', maxTimestamp)

tradesFileName = f'data/trades_round_{curr_round}_day_{day}.csv'
tradesData = parseFile(tradesFileName, 'symbol', maxTimestamp)


import matplotlib.pyplot as plt

symbol = 'INTARIAN_PEPPER_ROOT'
# symbol = 'EMERALDS'

userSymbol = input('Product Name ((T)OMATOES/(E)MERALDS/[(I)NTARIAN_PEPPER_ROOT]/(A)SH_COATED_OSMIUM): ').upper()
if userSymbol == 'E':
	symbol = 'EMERALDS'
elif userSymbol == 'T':
	symbol = 'TOMATOES'
elif userSymbol == 'I':
	symbol = 'INTARIAN_PEPPER_ROOT'
elif userSymbol == 'A':
	symbol = 'ASH_COATED_OSMIUM'
elif userSymbol:
	symbol = userSymbol

pricesTimes = [x['timestamp'] for x in pricesData[symbol]]
bidPrices1 = [x['bid_price_1'] for x in pricesData[symbol]]
askPrices1 = [x['ask_price_1'] for x in pricesData[symbol]]

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
