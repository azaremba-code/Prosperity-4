import random
import numpy as np

def getPlayer1():
	while True:
		a = random.random()
		b = random.random()
		if a + b < 1:
			return (a, b, 1 - a - b)
   
def getPlayer():
	while True:
		a = random.random()
		b = random.random()
		c = random.random()
		if a + b + c < 1:
			return (a, b, c)
 
def getPlayers(count: int, percentage: int):
	result = [(0, 0, 0.05)] * int(count * (percentage / 100))
	count -= int(count * (percentage / 100))
	for i in range(count):
		result.append(getPlayer1())
	return sorted(result, key=lambda x: x[2])
		
def research(x: float):
	x *= 100
	return 200_000 * float(np.log(1 + x)) / float(np.log(1 + 100))
	
def scale(x: float):
	return 7 * x
	
def speed(x: float):
	return 0.1 + x * 0.8

def getScores(players: list[tuple]):
	result = []
	for i, player in enumerate(players):
		rank = i
		scaledRank = rank / (len(players) - 1)
		score = research(player[0]) * scale(player[1]) * speed(scaledRank)
		budgetPercent = player[0] + player[1] + player[2]
		score -= budgetPercent * 50_000
		result.append((player, score))
	return result

def printPlayers(players: list[tuple]):
	scores = getScores(players)
	for player, score in scores:
		print(player, score)

def getBestPlayer(count: int, percentage: int):
	players = getPlayers(count, percentage)
	scores = getScores(players)
	bestPlayer = sorted(scores, key=lambda x: x[1])[-1]
	return (bestPlayer, scores.index(bestPlayer))

def getAverageBestPlayer(bestPlayers: list[tuple]):
	researchSum = 0
	scaleSum = 0
	speedSum = 0
	scoreSum = 0
	for ((research, scale, speed), score), _ in bestPlayers:
		researchSum += research
		scaleSum += scale
		speedSum += speed
		scoreSum += score
	n = len(bestPlayers)
	return ((researchSum / n, scaleSum / n, speedSum / n), scoreSum / n)

playersPerGame = input("Players per game ([10_000]): ")
if not playersPerGame:
	playersPerGame = 10_000
playersPerGame = int(playersPerGame)

gameCount = input("Game count ([20]): ")
if not gameCount:
	gameCount = 20
gameCount = int(gameCount)

percentage = input("Percentage of 0's ([0]-100): ")
if not percentage:
	percentage = 0
percentage = int(percentage)

bestPlayers = []	
for i in range(gameCount):	
	bestPlayers.append(getBestPlayer(playersPerGame, percentage))

for player in bestPlayers:
	# print(player)
	pass

# print()
print(getAverageBestPlayer(bestPlayers))
