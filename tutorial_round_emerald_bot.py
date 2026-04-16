from datamodel import OrderDepth, TradingState, Order
from typing import List

class Trader:
	def run(self, state: TradingState):
		result = {}

		product = "EMERALDS"
		BUY_PRICE = 9993
		SELL_PRICE = 10007
		MID = 10000
		LIMIT = 80

		orders: List[Order] = []

		pos = state.position.get(product, 0)

		# how much we are allowed to still buy/sell
		buy_qty = LIMIT - pos  # if pos=50, can buy 30 more
		sell_qty = LIMIT + pos  # if pos=-20, can sell 60 more

		if pos > 0 and MID in state.order_depths[product].sell_orders:
			amount = min(-state.order_depths[product].sell_orders[MID], pos)
			if amount > 0:
				orders.append(Order(product, MID, -amount))
			# pos -= amount
		else:
			if sell_qty > 0:
				orders.append(Order(product, SELL_PRICE, -sell_qty))

		if pos < 0 and MID in state.order_depths[product].buy_orders:
			amount = min(state.order_depths[product].buy_orders[MID], -pos)
			if amount > 0:
				orders.append(Order(product, MID, amount))
			# pos += amount
		else:
			if buy_qty > 0:
				orders.append(Order(product, BUY_PRICE, buy_qty))
	
	
		result[product] = orders

		print("BUYS: ", state.order_depths[product].buy_orders)
		print("SELLS: ", state.order_depths[product].sell_orders)
		print("POS: ", pos, "CURRENT_RESULT: ", result)

		traderData = state.traderData  # or whatever you want to store
		conversions = 0  # no conversions needed

		return result, conversions, traderData
