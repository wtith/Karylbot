# -*- coding: utf-8 -*-
"""

Originally made to parse the RSS feed of a vBulletin forum I use. As a result,
it's not particularly good at dealing with normal RSS feed uses.



"""

import os
import discord
from discord.ext import tasks, commands
import feedparser
import aiohttp
import json
import datetime
from dateutil import parser, tz
import nest_asyncio
from dotenv import load_dotenv


nest_asyncio.apply()

load_dotenv()
path = ".\json"
url = os.getenv('RSS_FEED')

try:  
    os.mkdir(path)  
except OSError as error:  
    print(error)   

"""
Grabs the list of posts from the RSS feed and links the latest one.
"""
async def post_grabber():

    feed = feedparser.parse(url)
    post = feed['entries'][0]
    
    date = str(post.published)
    print(date)
    dt = parser.parse(date)

    embed = discord.Embed(title="New post!", description=post.title)
    
    embed.url = await realURL(str(post.link))
    
    embed.timestamp = dt
    return embed, date

# Traverses the vBulletin newpost redirect in the RSS feed to grab the actual link to the post
async def realURL(url):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as r:
            assert r.status == 200
            return str(r.real_url)

class why(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        print('why loaded')
        self.index = 0
        self.timestamp = "filler"
        
        self.filename = path + "\\" + str('azn') + ".json"
        
        self.post_check.start()
        # self.printer.start()
    
    @tasks.loop(minutes=3.0)
    async def post_check(self):
        
        print("is anyone there")
        
        if (os.path.isfile(self.filename)):
            with open(self.filename, "r") as read_file:
                data = json.load(read_file)
                self.timestamp = data['timestamp']
                print("timestamp changed")
                
        embedRSS, dateRSS = await post_grabber()
        
        print(dateRSS)
        
        channelRSS = self.bot.get_channel(714290721485619281)
        
        if (self.timestamp != dateRSS):
            await channelRSS.send(content=None, embed=embedRSS)
            with open(self.filename, "w") as write_file:
                print("OK")
                data = {'timestamp': dateRSS}
                json.dump(data, write_file)
                        
            
    @post_check.before_loop
    async def before_post_check(self):
        print('waiting...')
        await self.bot.wait_until_ready()
    
    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.index)
        self.index += 1
    
def setup(bot):
    bot.add_cog(why(bot))