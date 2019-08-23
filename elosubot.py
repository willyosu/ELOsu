import discord, math, csv, os, asyncio, aiohttp, datetime, elosu, nest_asyncio
from osuapi import OsuApi, AHConnector
nest_asyncio.apply()

client = discord.Client()
token = open("token.txt", "r").read()
@client.event
async def on_ready():
	files = ["maps.csv", "matches.csv", "users.csv"]
	for file in files:
		if (not os.path.isfile(file)):
			(open(file, "w")).close()
	print("Bot is up and running!")
@client.event
async def on_message(message):
	messageSplit = message.content.split(' ')
	command = messageSplit[0].lower()
	commandContent = " ".join(messageSplit[1:])
	def logCommand():
		print(message.author.name + " used " + command)
	if command == "!hi":
		logCommand()
		await message.channel.send("hi")
		
	if command == "!badge":
		logCommand()
		try:
			int(commandContent)
		except:
			await message.channel.send("Error finding user...")
		else:
			badges = asyncio.get_event_loop().run_until_complete(elosu.getBadges(commandContent))
			await message.channel.send(str(badges))
	if command == "!rating":
		logCommand()
		stats = []
		with open("users.csv", newline="\n") as csvusers:
			users = csv.reader(csvusers, delimiter=",")
			for row in users:
				try:
					if (str(row[1]) == str(commandContent)):
						stats.append(row[1])
						stats.append(row[2])
					elif (str(row[0]) == str(commandContent)):
						stats.append(row[1])
						stats.append(row[2])
				except:
					await message.channel.send("User not found...")
				else:
					await message.channel.send(stats[0] + " is rated " + str(round(float(stats[1]))) + "!")
	if command == "!submit":
		logCommand()
		files = ["maps.csv", "matches.csv", "users.csv"]
		for file in files:
			if (not os.path.isfile(file)):
				(open(file, "w")).close()
		try:
			int(commandContent)
		except:
			await message.channel.send("Error finding match...")
		else:
			with open("maps.csv", newline="\n") as csvmaps:
				rankedMaps = []
				maps = csv.reader(csvmaps, delimiter=",")
				for map in maps:
					rankedMaps = map
				try:
					result = asyncio.get_event_loop().run_until_complete(elosu.getResult(open("key.txt", "r").read(), commandContent, rankedMaps))
				except:
					await message.channel.send("Error fetching match...")
				else:
					not_duplicate = True
					matchContent = [commandContent, result.users[0], result.score[result.users[0]], result.users[1], result.score[result.users[1]]]
					with open("matches.csv", newline="\n") as csvmatches:
						matches = csv.reader(csvmatches, delimiter=",")
						for row in matches:
							if (row[0] == commandContent):
								not_duplicate = False
					if(not_duplicate):
						finalList = [commandContent]
						for i in range(len(result.wins)):
							result.wins[i] = str(result.wins[i])
							finalList.append(result.wins[i])
						with open("matches.csv", "a", newline="\n") as csvmatches:
							matches = csv.writer(csvmatches, delimiter=",")
							matches.writerow(matchContent)
						userA_exists = False
						userB_exists = False
						userA = []
						userB = []
						with open("users.csv", newline="\n") as csvusers:
							users = csv.reader(csvusers, delimiter=",")
							for row in users:
								if (str(row[0]) == str(result.users[0])):
									userA_exists = True
									userA = [int(row[2]), result.score[int(row[0])]]
								elif (str(row[0]) == str(result.users[1])):
									userB_exists = True
									userB = [int(row[2]), result.score[int(row[0])]]
						with open("users.csv", "a", newline="\n") as csvausers:
							ausers = csv.writer(csvausers, delimiter=",")
							userStats = []
							if (not userA_exists):
								stats = asyncio.get_event_loop().run_until_complete(elosu.getStats(open("key.txt", "r").read(), result.users[0]))
								badges = asyncio.get_event_loop().run_until_complete(elosu.getBadges(result.users[0]))
								userStats = [result.users[0]]
								userStats.append(stats.username)
								rating = elosu.initialRating(int(stats.rank), int(badges))
								userStats.append(rating)
								ausers.writerow(userStats)
								userA = [int(rating), int(result.score[result.users[0]])]
							if (not userB_exists):
								stats = asyncio.get_event_loop().run_until_complete(elosu.getStats(open("key.txt", "r").read(), result.users[1]))
								badges = asyncio.get_event_loop().run_until_complete(elosu.getBadges(result.users[1]))
								userStats = [result.users[1]]
								userStats.append(stats.username)
								rating = elosu.initialRating(int(stats.rank), int(badges))
								userStats.append(rating)
								userStats.append(elosu.initialRating(int(stats.rank), int(badges)))
								ausers.writerow(userStats)
								userB = [int(rating), int(result.score[result.users[1]])]
						print(userA, userB)
						ratings = elosu.calcMatch(userA, userB)
						rusers = csv.reader(open("users.csv", newline="\n"), delimiter=",")
						rows = list(rusers)
						for row in rows:
							if (str(row[0]) == str(result.users[0])):
								row[2] = ratings[0]
							elif (str(row[0]) == str(result.users[1])):
								row[2] = ratings[0]
						wusers = csv.writer(open("users.csv", "w", newline="\n"), delimiter=",")
						wusers.writerows(rows)
						await message.channel.send("Match submitted!")
					else:
						await message.channel.send("Could not submit, duplicate found.")
client.run(token)
