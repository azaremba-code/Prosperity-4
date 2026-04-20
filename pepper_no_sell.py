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

		if not state.traderData:
			if pos >= LIMIT:
				traderData = "FULL"
			else:
				sellPrices = sorted(state.order_depths[product].sell_orders)
				if sellPrices:
					cheapestAsk = sellPrices[0]
					buyQuantity = min(-state.order_depths[product].sell_orders[cheapestAsk], LIMIT - pos)
					orders.append(Order(product, cheapestAsk + 3, buyQuantity))

		result[product] = orders
		conversions = 0

		return result, conversions, traderData
