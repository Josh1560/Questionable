#Import standard libraries
import discord
from discord.ext import commands

#Import required libraries
from json import load
from datetime import datetime

#Import custom libraries

#Define variables
botSettings = load(open("./bot/data/botSettings.json"))

#Define functions
async def reply(message, string):
    await message.channel.send(f"{message.author.mention}, {string}")

class basic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            description = f"Response Time: `{round(self.bot.latency * 1000)}ms`",
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Ran by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "Pong!",
            icon_url = self.bot.user.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            description = f"""
                The current prefix is `{botSettings['prefix']}`.
                You can find a list of commands here:
                {botSettings['links']['website']}
            """,
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "Help",
            icon_url = self.bot.user.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            description = f"""
                You can invite me to your server here:
                {botSettings['links']['invite']}
                Make sure to join my server too:
                {botSettings['links']['server']}
            """,
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "Invite",
            icon_url = self.bot.user.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(
            description = f"""
                You can support me by voting for me here:
                {botSettings['links']['vote']}
            """,
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "Vote",
            icon_url = self.bot.user.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx):
        embed = discord.Embed(
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "User Information",
            icon_url = self.bot.user.avatar_url
        )
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author
        embed.set_thumbnail(
            url = user.avatar_url
        )
        embed.add_field(
            name = "Username",
            value = f"`{user.name}#{user.discriminator}`"
        )
        embed.add_field(
            name = "ID",
            value = f"`{user.id}`"
        )
        embed.add_field(
            name = "Nickname",
            value = f"`{user.nick}`"
        )
        embed.add_field(
            name = "Status",
            value = f"`{user.status}`"
        )
        embed.add_field(
            name = "Joined Discord",
            value = f"`{user.created_at.replace(microsecond=0)}`"
        )
        embed.add_field(
            name = "Joined Server",
            value = f"`{user.joined_at.replace(microsecond=0)}`"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "Server Information",
            icon_url = self.bot.user.avatar_url
        )
        embed.set_thumbnail(
            url = ctx.guild.icon_url
        )
        embed.add_field(
            name = "Name",
            value = f"`{ctx.guild.name}`"
        )
        embed.add_field(
            name = "ID",
            value = f"`{ctx.guild.id}`"
        )
        embed.add_field(
            name = "Region",
            value = f"`{ctx.guild.region}`"
        )
        embed.add_field(
            name = "Owner",
            value = f"`{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}`"
        )
        embed.add_field(
            name = "Members",
            value = f"`{ctx.guild.member_count}`"
        )
        embed.add_field(
            name = "Created",
            value = f"`{ctx.guild.created_at.replace(microsecond=0)}`"
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(
            timestamp = datetime.utcnow(),
            colour = discord.Colour(botSettings["embedColour"])
        )
        embed.set_footer(
            text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}",
            icon_url = ctx.author.avatar_url
        )
        embed.set_author(
            name = "Bot Information",
            icon_url = self.bot.user.avatar_url
        )
        embed.add_field(
            name = "Servers",
            value = f"`{len(self.bot.guilds)}`"
        )
        embed.add_field(
            name = "Users",
            value = f"`{len(self.bot.users)}`"
        )
        embed.add_field(
            name = "Uptime",
            value = f"`{datetime.now().replace(microsecond=0) - self.bot.startTime}`"
        )
        embed.add_field(
            name = "Shard",
            value = f"`{ctx.guild.shard_id + 1} of {self.bot.shard_count}`"
        )
        embed.add_field(
            name = "Prefix",
            value = f"`{botSettings['prefix']}`"
        )
        creator = await self.bot.application_info()
        embed.add_field(
            name = "Creator",
            value = f"`{creator.owner.name}#{creator.owner.discriminator}`"
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(basic(bot))
