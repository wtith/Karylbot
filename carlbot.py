# -*- coding: utf-8 -*-
"""
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import nest_asyncio

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

nest_asyncio.apply()

roleDict = {704186768022569040: 'woop', 715435910568738836: 'birb'}

load_dotenv()

"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
"""

# discord intents so it can read members
intents = discord.Intents.all()
intents.members = True

INITIAL_EXTENSIONS = [
    'cogs.misc',
    #'cogs.why',
    'cogs.quotes'
    ]

class CarlBot(commands.Bot):
    # on boot up
    
    def __init__(self, **attrs):
        super().__init__(command_prefix='!', intents=intents)
        self.remove_command('help')
        self.token = os.getenv('DISCORD_TOKEN')
        
        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))
    
    async def on_ready(self):
        '''testChan = self.get_channel(714290721485619281)
        guild = testChan.guild
        message = await testChan.fetch_message(714660359360872458)
        
        reactionList = message.reactions
        
        for a in reactionList:
            if a.emoji.id in roleDict:
                
                #print(a.emoji.name)
                
                role = discord.utils.get(guild.roles, name=roleDict[a.emoji.id])
                roleList = role.members
                
                #print(roleList)
                
                reactList = await a.users().flatten()
                
                #print(reactList)
                
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
                            print(e)'''
    
    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == '__main__':
   karyl = CarlBot()
   karyl.run()