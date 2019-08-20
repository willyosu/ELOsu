import asyncio, aiohttp, math
from osuapi import OsuApi, AHConnector

# Uses the osu! API to get the details of a given multiplayer match: getResult(key, id)
async def getResult(key, id):
	class Result:
		datetime = ""
		wins = []
		score = {}
	api = OsuApi(key, connector=AHConnector())
	Data = await api.get_match(id)
	Result.datetime = Data.match.end_time
	Games = Data.games
	for game in Games:
		stats = game.scores
		if (stats[0].score > stats[1].score):
			Result.wins.append(stats[0].user_id)
			Result.score[stats[0].user_id] = Result.score.get(stats[0].user_id, 0) + 1
		elif (stats[0].score < stats[1].score):
			Result.wins.append(stats[1].user_id)
			Result.score[stats[1].user_id] = Result.score.get(stats[1].user_id, 0) + 1
		else:
			pass
	return (Result)

# Calculates initial rating using BWS: initialRating(rank, badges)
def initialRating(rank, badges):
	return((-225)*math.log((rank**((159/160)**(badges**2)))+50)+3880.20518)

# Calculates the change in ratings from a match: doMatch([oldRatingA, scoreA], [oldRatingB, scoreB])
def doMatch(userA, userB):
	ratingA = (userA[0] + (100 * ((userA[1] / (userA[1] + userB[1]) - (1 / (1 + 10 ** ((userB[0] - userA[0]) / 500)))))))
	ratingB = (userB[0] + (100 * ((userB[1] / (userA[1] + userB[1]) - (1 / (1 + 10 ** ((userA[0] - userB[0]) / 500)))))))
	return(ratingA, ratingB)
