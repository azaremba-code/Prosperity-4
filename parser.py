fileName = input('File name: ')
with open(fileName) as file:
	lines = file.read().split('\n')

fields = lines[0].split(';')
splitLines = [x.split(';') for x in lines[1:]]
data = [{fields[i]: line[i] for i in range(len(line))} for line in splitLines if len(line) == len(fields)]

productNames = list(set([x['product'] for x in data])) # ['TOMATOES', 'EMERALDS']
data = {productName: [x for x in data if x['product'] == productName] for productName in productNames}


import matplotlib.pyplot as plt

symbol = 'TOMATOES'
symbol = 'EMERALDS'

times = [int(x['timestamp']) for x in data[symbol]]
bidPrices1 = [int(x['bid_price_1']) for x in data[symbol]]
bidPrices2 = [int(x['bid_price_2']) for x in data[symbol]]
askPrices1 = [int(x['ask_price_1']) for x in data[symbol]]
askPrices2 = [int(x['ask_price_2']) for x in data[symbol]]

plt.plot(times, bidPrices1, 'r', label = 'Bid Prices 1', linewidth = 0.25)
# plt.plot(times, bidPrices2, 'tab:orange', label = 'Bid Prices 2', linewidth = 0.25, antialiased = False)
plt.plot(times, askPrices1, 'g', label = 'Ask Prices 1', linewidth = 0.25)
# plt.plot(times, askPrices2, 'c', label = 'Ask Prices 2', linewidth = 0.25, antialiased = False)

plt.xlabel("times")
plt.ylabel("prices")

plt.show()
