import asyncio, aiohttp, math, json
from osuapi import OsuApi, AHConnector
from bs4 import BeautifulSoup

# Uses the osu! API to get the details of a given multiplayer match: getResult(key, id, maps[])
async def getResult(key, id, maps):
	class Result:
		datetime = ""
		users = []
		wins = []
		score = {}
		totalScore = {}
		scoreDiff = {}
	api = OsuApi(key, connector=AHConnector())
	Data = await api.get_match(id)
	Result.datetime = Data.match.end_time
	Games = Data.games
	Result.users = [(Games[0].scores[0].user_id), (Games[0].scores[1].user_id)]
	for game in Games:
		if str(game.beatmap_id) in maps:
			stats = game.scores
			Result.score[stats[0].user_id] = Result.score.get(stats[0].user_id, 0)
			Result.score[stats[1].user_id] = Result.score.get(stats[1].user_id, 0)
			Result.totalScore[stats[0].user_id] = Result.totalScore.get(stats[0].user_id, 0) + stats[0].score
			Result.totalScore[stats[1].user_id] = Result.totalScore.get(stats[1].user_id, 0) + stats[1].score
			if (stats[0].score > stats[1].score):
				Result.wins.append(stats[0].user_id)
				Result.score[stats[0].user_id] = Result.score.get(stats[0].user_id, 0) + 1
				Result.scoreDiff[stats[0].user_id] = Result.scoreDiff.get(stats[0].user_id, 0) + (stats[0].score - stats[1].score)
			elif (stats[0].score < stats[1].score):
				Result.wins.append(stats[1].user_id)
				Result.score[stats[1].user_id] = Result.score.get(stats[1].user_id, 0) + 1
				Result.scoreDiff[stats[1].user_id] = Result.scoreDiff.get(stats[1].user_id, 0) + (stats[1].score - stats[0].score)
			else:
				pass
		else:
			pass
	api.close()
	return(Result)

async def getStats(key, userid):
	class Stats:
		username = ""
		rank = 0
	api = OsuApi(key, connector=AHConnector())
	Data = await api.get_user(userid)
	Stats.username = Data[0].username
	Stats.rank = Data[0].pp_rank
	api.close()
	return(Stats)

# Gets the number of user badges from a given userid (since there is no API request for it yet): getBadges(userid)
async def getBadges(userid):
	url = "https://osu.ppy.sh/users/" + str(userid)
	badges = 0
	async with aiohttp.ClientSession() as session:
		async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as page:
			soup = BeautifulSoup(await page.text(), "html.parser")
			data = json.loads(soup.find("script", {"id": "json-user"}).text)
			return(len(data["badges"]))
	session.close()
	
# Calculates initial rating using BWS: initialRating(rank, badges)
def initialRating(rank, badges):
	return(round((-225)*math.log((rank**((159/160)**(badges**2)))+50)+3880.20518, 5))

# Calculates the change in ratings from a match: doMatch([oldRatingA, scoreA], [oldRatingB, scoreB])
def calcMatch(userA, userB):
	ratingA = round(userA[0] + (100 * ((userA[1] / (userA[1] + userB[1]) - (1 / (1 + 10 ** ((userB[0] - userA[0]) / 500)))))), 5)
	ratingB = round(userB[0] + (100 * ((userB[1] / (userA[1] + userB[1]) - (1 / (1 + 10 ** ((userA[0] - userB[0]) / 500)))))), 5)
	return(ratingA, ratingB)
 
