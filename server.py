import discord
import requests
from discord import client
from discord.ext import commands
TOKEN = "PUT YOUR TOKEN HERE"
client = commands.Bot(command_prefix="!", activity=discord.Streaming(name='Apex Legends', url='https://www.twitch.tv/greg_coooper'))


@client.event
async def on_ready():
    print("All set")


@client.command(name='map', help='type(current, next) \nShows current or the next map')
async def roll(ctx, type):
    reques = requests.get("https://api.mozambiquehe.re/maprotation?auth=T1TwYEvZX6LlKruNlVwH")
    rqs = reques.json()
    if type == "next":
        response = rqs["next"]
        embed = discord.Embed(title=f"{response['map']}", url="https://apexlegendsstatus.com/current-map", description=f"The next map is {response['map']}. Coming in {rqs['current']['remainingTimer']}", color=discord.Color.red())
        await ctx.send(embed=embed)
    if type == "current":
        response = rqs["current"]
        embed = discord.Embed(title=f"{response['map']}", url="https://apexlegendsstatus.com/current-map", description=f"The current map is {response['map']}. The next map is {rqs['next']['map']}, it is coming in {response['remainingTimer']}", color=discord.Color.red())
        await ctx.send(embed=embed)


@client.command(name='origin', help='username(text) - Username of the person you want to search \nSearches the Origin API for some techical information')
async def roll(ctx, username):
    reques = requests.get(f"https://api.mozambiquehe.re/origin?player={username}&auth=T1TwYEvZX6LlKruNlVwH")
    rqs = reques.json()
    response = rqs
    embed = discord.Embed(title=f"Origin readouts for {username}", url="https://apexlegendsstatus.com/", description=f"The {username} UID is {response['uid']}. The {username} PID is {response['pid']}.", color=discord.Color.red())
    embed.set_thumbnail(url=f"{response['avatar']}")
    await ctx.send(embed=embed)


@client.command(name='news', help='num(integer) \nShows the number of links to the Apex website')
async def roll(ctx, num):
    for a in range(int(num)):
        reques = requests.get("https://api.mozambiquehe.re/news?lang=en-us&auth=T1TwYEvZX6LlKruNlVwH")
        rqs = reques.json()
        response = rqs[a]
        embed = discord.Embed(title=response["title"], url=response["link"], description=response["short_desc"], color=discord.Color.red())
        embed.set_thumbnail(url=response["img"])
        await ctx.send(embed=embed)


@client.command(name='stats', help='platform(PC, PS4, X1) - The platform the player plays on \nusername(text) - Username of the person you want to search \ntype(global, legend) - The type of statistic you want to show \nlegend(text) - Only for use if you set the type to legend \nReturns the global or an individual legends statistic')
async def roll(ctx, platform, username, type, legend="None"):
    reques = requests.get(f"https://api.mozambiquehe.re/bridge?version=5&platform={platform}&player={username}&auth=T1TwYEvZX6LlKruNlVwH")
    rqs = reques.json()
    if type == "global":
        response = rqs["global"]
        embed = discord.Embed(title=f"Global stats for {username}", url="https://apexlegendsstatus.com/", description="", color=discord.Color.red())
        embed.add_field(name="Name", value=response["name"], inline=False)
        embed.add_field(name="UID", value=response["uid"], inline=False)
        embed.add_field(name="Platform", value=response["platform"], inline=False)
        embed.add_field(name="Level", value=response["level"], inline=False)
        embed.add_field(name="Rank", value=response["rank"]["rankName"], inline=False)
        embed.add_field(name="Battlepass level", value=response["battlepass"]["level"], inline=False)
        await ctx.send(embed=embed)
    if type == "legend":
        if legend != "None":
            embed = discord.Embed(title=f"Stats on {legend} for {username}", url="https://apexlegendsstatus.com/", description="", color=discord.Color.red())
            try:
                response = rqs["legends"]["all"][legend]["data"]
                for a in response:
                    embed.add_field(name=a["name"], value=a["value"], inline=False)
                await ctx.send(embed=embed)
            except KeyError:
                embed.set_footer(text="Nothing tracked here")
                await ctx.send(embed=embed)


@client.command(name='server_status', help='Displayes the status of all servers that apex currently uses')
async def roll(ctx):
    reques = requests.get("https://api.mozambiquehe.re/servers?auth=T1TwYEvZX6LlKruNlVwH")
    rqs = reques.json()
    for a in ["Origin_login", "EA_novafusion", "EA_accounts", "ApexOauth_Crossplay"]:
        embed = discord.Embed(title=f"Server stasus for {a}", url="https://apexlegendsstatus.com/", description="", color=discord.Color.red())
        for b in ["EU-West", "EU-East", "US-West", "US-Central", "US-East", "SouthAmerica", "Asia"]:
            embed.add_field(name=b, value=f"Status:{rqs[a][b]['Status']}. Ping:{rqs[a][b]['ResponseTime']}")
        embed.set_footer(text="Made posible by https://apexlegendsstatus.com")
        await ctx.send(embed=embed)
client.run(TOKEN)