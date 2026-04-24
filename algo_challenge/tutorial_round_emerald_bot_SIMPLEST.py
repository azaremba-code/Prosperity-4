from datamodel import OrderDepth, TradingState, Order
from typing import List

class Trader:
    def run(self, state: TradingState):
        result = {}

        product = "EMERALDS"
        BUY_PRICE = 9993
        SELL_PRICE = 10007
        LIMIT = 80

        orders: List[Order] = []

        # current position (default 0 if not present)
        pos = state.position.get(product, 0)

        # how much we are allowed to still buy/sell
        buy_qty = LIMIT - pos          # if pos=50, can buy 30 more
        sell_qty = LIMIT + pos         # if pos=-20, can sell 60 more

        # place buy order if we have room
        if buy_qty > 0:
            orders.append(Order(product, BUY_PRICE, buy_qty))

        # place sell order if we have room
        if sell_qty > 0:
            orders.append(Order(product, SELL_PRICE, -sell_qty))

        result[product] = orders

        traderData = state.traderData  # or whatever you want to store
        conversions = 0                # no conversions needed

        return result, conversions, traderData
