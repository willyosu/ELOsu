# ELOsu
An attempt at making unofficial ratings for osu! matches using khazhyk's osuapi package. Uses modified ELO function to calculate ratings of users. Feel free to modify to your own discression and make different ranking systems using the classes set up when I make the API requests. If you would like an example of how to use the functions of just `elosu.py` then look at the Discord bot as an example for how to call and pass arguments easily.

### Requirements
Most obviously you will need **Python3**; the files have been tested using 3.7 and may work with prior versions.

*The Python3 standard lib should come with the following packages, but if you don't have them for some reason you can probably find them on pip:*

`math`, `os`, `csv`, `json`, `datetime`, `asyncio`

*And these packages are the ones you definitely need to download (see **Setup** below for easy install using pip).*

`aiohttp`, `discord`, `nest_asyncio`, `bs4`, `osuapi`

### Setup
***For normal use:***
1. Get all of the required packages by running `pip install -r requirements.txt` .
2. Use it.
***For use with the built in Discord bot:***
1. If you haven't already create a bot application on Discord and find out your token
2. Make two txt files; one called `token.txt` for your Discord bot token, and one called `key.txt` for your osu! API key.
3. Now you should be able to just run `python elosubot.py` to get the bot up and running.

*Rememeber kids: Don't **ever** share your bot token or your API key with anyone.*
