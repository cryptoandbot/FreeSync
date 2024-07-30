import requests
import json
import arbFinder
import stakeCalc
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands, tasks
from copy import deepcopy

load_dotenv()

ODDS_API_KEY = os.getenv('ODDS_API_KEY')
DIS_API_KEY = os.getenv('DIS_API_KEY')
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())


SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'unix' # iso | unix

channel = {}
arbOpp = []

@bot.event
async def on_ready():
    print("Bot Deployed")
    guild = await bot.wait_for(
        "message")  # Sets the channel where the first message is sent since invite to send notifs. Use $setChannel to change
    if guild.guild.id not in channel.keys():
        channel[guild.guild.id] = guild.channel.id
    arbLoop.start()

@bot.command()
async def setChannel(ctx):
    global channel
    channel[ctx.guild.id] = ctx.channel.id
    await ctx.reply("The bot will be sending notifications through this channel " + str(channel[ctx.guild.id]) + " now")

@tasks.loop(seconds = 300) # repeat after every 5 minutes
async def arbLoop():
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={ODDS_API_KEY}&regions={REGIONS}&markets={MARKETS}',
        params={
            'api_key': ODDS_API_KEY
        }
    )


    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        print('Number of events:', len(odds_json))
        # pretty = json.dumps(odds_json, indent=4)
        # print(pretty)

        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])
        print('Requests used in last call', odds_response.headers['x-requests-last'])

    global arbOpp
    arbOpp = arbFinder.arbFinder(odds_json) # Returns list of arbitrage opportunities
    print(arbOpp)
    embedded_msg = discord.Embed(title="Upcoming Arbitrage Opportunities",
                                 description="Updated every 5 minutes. Please use the last one.",
                                 color=discord.Color.random())
    for game in arbOpp:
        n = 1
        s = "Game " + str(n)
        embedded_msg.add_field(name=s, value="")
        for outcome in game.keys():
            for book in game[outcome]:
                embedded_msg.add_field(name="Outcome: "+outcome, value="Odds: "+str(game[outcome][book])+"\nBookMaker: "+book, inline=False)
        n += 1
    global channel
    for cha in channel.keys():
        chan = bot.get_channel(channel[cha])
        await chan.send(embed=embedded_msg)


@bot.command()
async def stake(ctx, stake):
    embedded_msg = discord.Embed(title="Stake Based on Recent Arbitrage Opportunities",
                                 description="Recommended to round stakes to nearest multiple of 5. Round draws up to ensure profit.",
                                 color=discord.Color.random())
    global arbOpp

    stakeList = stakeCalc.stakeCalc(arbOpp, stake)
    copy = deepcopy(stakeList)
    payoutList = stakeCalc.payoutPerStake(arbOpp,copy)

    for game in range(len(stakeList)):
        for outcome in stakeList[game].keys():
            for book in stakeList[game][outcome]:
                embedded_msg.add_field(name="Outcome: "+outcome,
                                       value="Stake: "+str(stakeList[game][outcome][book])+
                                             "\nPayout: "+str(payoutList[game][outcome][book])+"\nBookMaker: "+book,
                                       inline=False)
    await ctx.reply(embed=embedded_msg)

bot.run(DIS_API_KEY)
