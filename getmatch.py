from osuapi import OsuApi, AHConnector
import asyncio, aiohttp
import datetime

async def getResult(id):
	api = OsuApi(open("key.txt", "r").read(), connector=AHConnector())
	result = await api.get_match(id)
	roundWinners = []
	trueGames = []
	rawGames = result.games
	for game in rawGames:
		userStats = game.scores
		if (userStats[0].score > userStats[1].score):
			roundWinners.append(userStats[0].user_id)
		elif (userStats[0].score < userStats[1].score):
			roundWinners.append(userStats[1].user_id)
		else:
			pass
	return (roundWinners)
result = asyncio.get_event_loop().run_until_complete(getResult(53793673))
print (result)
