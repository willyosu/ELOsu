import discord, math, csv, os, asyncio, aiohttp, datetime, elosu
from osuapi import OsuApi, AHConnector
#nest_asyncio.apply()
client = discord.Client()
token = open("token.txt", "r").read()

@client.event
async def on_ready():
	print("Bot is up and running!")
@client.event
async def on_message(message):
	messageSplit = message.content.split(' ')
	command = messageSplit[0].lower()
	commandContent = " ".join(messageSplit[1:])
	def logCommand():
		print(message.author.name + " used " + command)
	if command == "!submit":
			logCommand()
			try:
				commandContent = int(commandContent)
			except:
				await message.channel.send("Error fetching match...")
			else:
				try:
					result = asyncio.get_event_loop().run_until_complete(elosu.getResult(open("key.txt", "r").read(), commandContent))
				except:
					await message.channel.send("Error fetching match...")
				else:
					not_duplicate = True
					with open("matches.csv", newline="\n") as csvfile:
						matches = csv.reader(csvfile, delimiter="\t")
						for row in matches:
							if (int(row[0]) == commandContent):
								not_duplicate = False
					if(not_duplicate):
						with open("matches.csv", newline="\n") as csvfile:
							matches = csv.writer(csvfile, delimiter="\t")
							matches.writerow(commandContent + "\t" + "\t".join(result.wins))
						await message.channel.send("Match submitted!")
					else:
						await message.channel.send("Could not submit, duplicate found.")
client.run(token)