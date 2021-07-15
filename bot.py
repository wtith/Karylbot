# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:09:52 2020

@author: William
"""
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()

roleDict = {704186768022569040: 'woop', 715435910568738836: 'birb'}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
"""

# on boot up
@bot.event
async def on_ready():
    testChan = bot.get_channel(714290721485619281)
    guild = testChan.guild
    message = await testChan.fetch_message(714660359360872458)
    
    reactionList = message.reactions
    
    for a in reactionList:
        if a.emoji.id in roleDict:
            
            print(a.emoji.name)
            
            role = discord.utils.get(guild.roles, name=roleDict[a.emoji.id])
            roleList = role.members
            
            print(roleList)
            
            reactList = await a.users().flatten()
            
            print(reactList)
            
            # for the users in the reaction
            for user in reactList:
                if user not in roleList:
                    try:
                        print(user.name + ' add')
                        await user.add_roles(role, reason='retroactive')
                    except discord.HTTPException as e:
                        print(e)
            # for the users in the role
            for roleMember in roleList:
                if roleMember not in reactList:
                    try:
                        print(roleMember.name + ' remove')
                        await roleMember.remove_roles(role, reason='retroactive')
                    except discord.HTTPException as e:
                        print(e)
    
# for assigning discord roles based on reaction
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    message = payload.message_id
    emojiID = payload.emoji.id
    print(message)
    if (message == 714660359360872458):
        if emojiID in roleDict:
            role = discord.utils.get(guild.roles, name=roleDict[emojiID])
            await member.add_roles(role, reason='test')

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    message = payload.message_id
    emojiID = payload.emoji.id
    print(message)
    if (message == 714660359360872458):
        if emojiID in roleDict:
            role = discord.utils.get(guild.roles, name=roleDict[emojiID])
            await member.remove_roles(role, reason='test')

@bot.command(name='69')
async def sixty_nine(ctx):
    await ctx.send('nice')
    
@bot.command(name='fuck')
async def fuck(ctx):
    await ctx.send('fuck')

@bot.command(name='test')
async def chantest(ctx):
    if str(ctx.channel) == 'test':
        await ctx.send('OK!')
        
@bot.command(name='yabai')
async def yabai(ctx):
    rand = random.randint(1, 2)
    if (rand) == 1:
        await ctx.send('https://www.youtube.com/watch?v=gxt6jf6FpRY')
    else:
        await ctx.send('https://www.youtube.com/watch?v=oN6LD7Ab4Qc')

@bot.command(name='woop')
async def woop(ctx):
    await ctx.send("<:woop:704186768022569040>")

# custom help command description here
@bot.command(name='help')
async def helper(ctx):
    embed = discord.Embed(title="Help using Karyl-chan!", description="The list of commands:")
    embed.add_field(name="!69", value="nice")
    embed.add_field(name="!fuck", value="fuck")
    embed.add_field(name="!test", value="should only work in #test")
    embed.add_field(name="!yabai", value="yabai")
    embed.add_field(name="!woop", value= "<:woop:704186768022569040>")
    await ctx.channel.send(content=None, embed=embed)
    
bot.run(TOKEN)