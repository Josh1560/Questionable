#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from datetime import datetime
from inspect import isawaitable

#Import custom libraries

#Define variables
botSettings = load(open("./bot/data/botSettings.json"))

#Define functions
async def reply(ctx, string):
    await ctx.send(f"{ctx.author.mention}, {string}")
def isDeveloper(ctx):
    return(ctx.author.id in botSettings["developers"])

class developer:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(isDeveloper)
    async def restart(self, ctx):
        await reply(ctx, "Restarting... :arrows_counterclockwise:")
        print("Restarting...")
        try:
            await self.bot.get_cog("search").session.close()
        except:
            pass
        await self.bot.close()

    @commands.command()
    @commands.check(isDeveloper)
    async def reload(self, ctx, arg=None):
        if arg:
            arg = f"extensions.{arg.lower()}"
            if arg == "extensions.search":
                try:
                    await self.bot.get_cog("search").session.close()
                except:
                    pass
            self.bot.unload_extension(arg)
            self.bot.load_extension(arg)
            embed = discord.Embed(
                description = f"Successfully reloaded extension `{arg}`.",
                timestamp = datetime.utcnow(),
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_footer(
                text = f"Ran by {ctx.author.name}#{ctx.author.discriminator}",
                icon_url = ctx.author.avatar_url
            )
            embed.set_author(
                name = "Reload",
                icon_url = self.bot.user.avatar_url
            )
            await ctx.send(embed=embed)
        else:
            await reply(ctx, "Please specify the extension to reload! :warning:")

    @commands.command()
    @commands.check(isDeveloper)
    async def eval(self, ctx, *, args=None):
        if args:
            embed = discord.Embed(
                timestamp = datetime.utcnow(),
                color = discord.Colour(botSettings["embedColour"])
            )
            embed.set_footer(
                text = f"Ran by {ctx.author.name}#{ctx.author.discriminator}",
                icon_url = ctx.author.avatar_url
            )
            embed.set_author(
                name = "Debug",
                icon_url = self.bot.user.avatar_url
            )
            embed.add_field(
                name = "Input",
                value = f"```python\n{args}```",
                inline = False
            )
            cmd = eval(args)
            if isawaitable(cmd):
                output = await cmd
            else:
                output = cmd
            embed.add_field(
                name = "Output",
                value = f"```{output}```",
                inline = False
            )
            await ctx.send(embed=embed)
        else:
            await reply(ctx, "Tell me what to evaluate! :warning:")

    """@commands.command()
    @commands.check(isDeveloper)
    async def sysinfo(self, ctx):"""

def setup(bot):
    bot.add_cog(developer(bot))
