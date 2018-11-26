#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from urllib.parse import quote
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime

#Import custom libraries

#Define variables
engineSettings = load(open("./bot/data/engineSettings.json"))
botSettings = load(open("./bot/data/botSettings.json"))

#Define functions
async def reply(ctx, string):
    await ctx.send(f"{ctx.author.mention}, {string}")

class search:
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession(loop=bot.loop)

    async def scrape(self, ctx, engine, query):
        if query:
            url = f"{engine['queryURL']}{quote(query)}"
            links = list()
            async with self.session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                selection = soup.select(engine["selection"])[:5]
                prefixUrl = engine["prefixUrl"]
                for i in selection:
                    links.append(f"[{i.text}]({prefixUrl}{i['href']})")
            embed = discord.Embed(
                timestamp = datetime.utcnow(),
                colour = discord.Colour(botSettings["embedColour"])
            )
            embed.set_footer(
                text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
                icon_url = ctx.author.avatar_url
            )
            embed.set_author(
                name = f"Search ({engine['name']})",
                icon_url = self.bot.user.avatar_url
            )
            embed.add_field(
                name = "Search Query",
                value = f"```{query}```",
                inline = False
            )
            embed.add_field(
                name = "Results",
                value = "\n".join(links),
                inline = False
            )
            await ctx.send(embed=embed)
        else:
            await reply(ctx, "Please input a search term! :warning:")

    @commands.command()
    async def search(self, ctx, *, args=None):
        #Get server's default engine
        await self.scrape(ctx, engineSettings["duckduckgo"], args)

    @commands.command(aliases=["bing", "yahoo", "ask"])
    async def duckduckgo(self, ctx, *, query=None):
        await self.scrape(ctx, engineSettings[ctx.invoked_with.lower()], query)

    @commands.command()
    async def google(self, ctx):
        await reply(ctx, "Google is not supported. :information_source:")

    @commands.command()
    async def youtube(self, ctx):
        await reply(ctx, "YouTube is not supported, yet. :information_source:")

def setup(bot):
    bot.add_cog(search(bot))
