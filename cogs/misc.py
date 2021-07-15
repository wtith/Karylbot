# -*- coding: utf-8 -*-
"""
"""

import discord
from discord.ext import commands
import random

roleDict = {704186768022569040: 'woop', 715435910568738836: 'birb'}

class misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        print('misc loaded')
    
    # for assigning discord roles based on reaction
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        message = payload.message_id
        emojiID = payload.emoji.id
        if (message == 714660359360872458):
            if emojiID in roleDict:
                role = discord.utils.get(guild.roles, name=roleDict[emojiID])
                await member.add_roles(role, reason='test')
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        message = payload.message_id
        emojiID = payload.emoji.id
        print(message)
        if (message == 714660359360872458):
            if emojiID in roleDict:
                role = discord.utils.get(guild.roles, name=roleDict[emojiID])
                await member.remove_roles(role, reason='test')
                
    @commands.command(name='69')
    async def sixty_nine(self, ctx):
        await ctx.send('nice')
        
    @commands.command(name='fuck')
    async def fuck(self, ctx):
        await ctx.send('fuck')
    
    @commands.command(name='test')
    async def chantest(self, ctx):
        print('read')
        if str(ctx.channel) == 'test':
            await ctx.send('OK!')
            
    @commands.command(name='yabai')
    async def yabai(self, ctx):
        rand = random.randint(1, 2)
        if (rand) == 1:
            await ctx.send('https://www.youtube.com/watch?v=gxt6jf6FpRY')
        else:
            await ctx.send('https://www.youtube.com/watch?v=oN6LD7Ab4Qc')
    
    @commands.command(name='woop')
    async def woop(self, ctx):
        await ctx.send("<:woop:704186768022569040>")
    
    # custom help command description here
    @commands.command(name='help')
    async def helper(self, ctx):
        embed = discord.Embed(title="Help using Karyl-chan!", description="The list of commands:")
        embed.add_field(name="!69", value="nice")
        embed.add_field(name="!fuck", value="fuck")
        embed.add_field(name="!test", value="should only work in #test")
        embed.add_field(name="!yabai", value="yabai")
        embed.add_field(name="!woop", value= "<:woop:704186768022569040>")
        await ctx.channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))