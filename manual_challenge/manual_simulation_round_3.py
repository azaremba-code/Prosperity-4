import numpy as np

# Precompute static possible prices
POSSIBLE_RESERVE_PRICES = np.array([x for x in range(670, 921) if x % 5 == 0])
POSSIBLE_BIDS = np.arange(670, 921)

def getNPCReservePrices(count: int):
    prices = np.random.choice(POSSIBLE_RESERVE_PRICES, size=count)
    return prices

def getRandomPlayers(count: int):
    bids = np.random.choice(POSSIBLE_BIDS, size=(count, 2))
    players = np.sort(bids, axis=1)
    return players

def getRandomPlayersFixedBid1(count: int, fixed_bid1: int = 791):
    possible_bid2s = POSSIBLE_BIDS[POSSIBLE_BIDS >= fixed_bid1]
    bid1s = np.full(count, fixed_bid1)
    bid2s = np.random.choice(possible_bid2s, size=count)
    players = np.column_stack((bid1s, bid2s))
    return players

def getPlayerBid2Mean(players: np.ndarray):
    return np.mean(players[:, 1])

def getPNL(player: np.ndarray, npcReservePrices: np.ndarray, mean: float):
    bid1, bid2 = player
    # Vectorize the inner loop
    bid1_wins = (bid1 > npcReservePrices).sum()
    bid2_wins = (bid2 > npcReservePrices).sum()
    
    profit = bid1_wins * (920 - bid1)
    
    if bid2_wins > 0:
        if bid2 >= mean:
            profit += bid2_wins * (920 - bid2)
        else:
            profit += bid2_wins * (920 - bid2) * (((920 - mean) / (920 - bid2)) ** 3)
    
    return profit

def findBestPlayer(players: np.ndarray, npcReservePrices: np.ndarray, mean: float):
    profits = np.array([getPNL(player, npcReservePrices, mean) for player in players])
    best_idx = np.argmax(profits)
    return players[best_idx], profits[best_idx]


npcReservePrices = getNPCReservePrices(50_000)
# print(npcReservePrices)

players = getRandomPlayers(100_000)
# players = getRandomPlayersFixedBid1(50_000, fixed_bid1=791)

mean = getPlayerBid2Mean(players)
# print(mean)

bestPlayer, bestProfit = findBestPlayer(players, npcReservePrices, mean)
print(bestPlayer, bestProfit)
