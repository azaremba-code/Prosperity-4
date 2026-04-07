def num_if_can(x):
	try:
		return int(x)
	except ValueError:
		pass

	try:
		return float(x)
	except ValueError:
		return x

fileName = input('File name: ')
with open(fileName) as file:
	lines = file.read().split('\n')

fields = lines[0].split(';')
splitLines = [x.split(';') for x in lines[1:]]
processedLines = [[num_if_can(x) for x in line] for line in splitLines]
data = [{fields[i]: line[i] for i in range(len(line))} for line in processedLines if len(line) == len(fields)]

productNames = list(set([x['product'] for x in data])) # ['TOMATOES', 'EMERALDS']
data = {productName: [x for x in data if x['product'] == productName] for productName in productNames}


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

times = [x['timestamp'] for x in data[symbol]]
bidPrices1 = [x['bid_price_1'] for x in data[symbol]]
bidPrices2 = [x['bid_price_2'] for x in data[symbol]]
askPrices1 = [x['ask_price_1'] for x in data[symbol]]
askPrices2 = [x['ask_price_2'] for x in data[symbol]]

plt.plot(times, bidPrices1, 'r', label = 'Bid Prices 1', linewidth = 0.25)
# plt.plot(times, bidPrices2, 'tab:orange', label = 'Bid Prices 2', linewidth = 0.25, antialiased = False)
plt.plot(times, askPrices1, 'g', label = 'Ask Prices 1', linewidth = 0.25)
# plt.plot(times, askPrices2, 'c', label = 'Ask Prices 2', linewidth = 0.25, antialiased = False)

plt.xlabel("times")
plt.ylabel("prices")

plt.show()
