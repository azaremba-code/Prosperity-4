from datamodel import TradingState, Order
from typing import List

class Trader:
	def run(self, state: TradingState):
		result = {}

		product = "INTARIAN_PEPPER_ROOT"
		LIMIT = 80

		orders: List[Order] = []

		pos = state.position.get(product, 0)
		traderData = state.traderData
		
		offset = 6
				
		buyPrices = sorted(state.order_depths[product].buy_orders)
		if buyPrices:
			bestBid = buyPrices[-1] + offset
			buyQuantity = LIMIT - pos
			orders.append(Order(product, bestBid, buyQuantity))

		sellPrices = sorted(state.order_depths[product].sell_orders)
		if False and sellPrices:
			bestAsk = sellPrices[0] - offset
			sellQuantity = LIMIT + pos
			orders.append(Order(product, bestAsk, -sellQuantity))

		result[product] = orders
		conversions = 0

		return result, conversions, traderData
