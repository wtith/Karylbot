# -*- coding: utf-8 -*-
"""
Cog that handles quotes via SQLite. Quotes are messages that are saved and can be replayed
for the member's enjoyment.

SQL table format is as follows:

num_id || guild_id || user || message || marked
num_id: index of the quote
user: 

"""

import discord
from discord.ext import commands
import aiosqlite
import random

class quotes(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        print('quotes loaded')
    
    @commands.Cog.listener()
    async def on_ready(self):
        
        # set up the quote database tables
        async with aiosqlite.connect("discord_quotes.db") as db:
            cur = await db.cursor()
            sql_input ='''CREATE TABLE IF NOT EXISTS quotes
            (num_id integer, guild_id integer, user integer, message text, marked integer)'''
            await cur.execute(sql_input)
            await db.commit()
        
    
    @commands.group(name='quote', invoke_without_command=True)
    async def quote(self, ctx, number = None):
        
        guild_id = ctx.guild.id
        async with aiosqlite.connect("discord_quotes.db") as db:
            async with db.cursor() as cur:
                count_input = "SELECT COUNT(*) FROM quotes WHERE guild_id = ?"
                await cur.execute(count_input, (guild_id,))
                count = (await cur.fetchone())[0]
                
                if (count == 0):
                    await ctx.send('There aren\'t any quotes for this discord!')
                    return
                
                # if no argument select a random quote
                if (number == None):
                    sql_input = "SELECT message FROM quotes WHERE guild_id = ? AND marked = 0"
                    await cur.execute(sql_input, (guild_id,))
                    rows = await cur.fetchall()
                    message = random.choice(rows)[0]
                    await ctx.send(message)
                    return
                
                # otherwise we try to get the quote with the number specified
                try:
                    quote_val = int(number)
                    sql_input = "SELECT message FROM quotes WHERE guild_id = ? AND num_id = ? AND marked = 0"
                    
                    if (quote_val == 0):
                        await ctx.send('There\'s no quote zero, idiot.')
                        return
                    
                    elif (quote_val < 0):
                        await ctx.send('There\'s nothing here!')
                        return
                    
                    await cur.execute(sql_input, (guild_id, quote_val))
                    select = await cur.fetchone()
                    await cur.close()
                    
                    if (len(select) == 0):
                        await ctx.send('That quote can\'t be found!')
                        return
                    
                    await ctx.send(select[0])
                
                except ValueError: 
                    await ctx.send('Please submit a valid number for quotes!')
    
    # adds the content of a message to the quote database
    # 
    @quote.command(name='add')
    async def quote_add(self, ctx, *, text : str):
        
        count = 0
        guild_id = ctx.guild.id
        member_id = ctx.message.author.id
        
        async with aiosqlite.connect("discord_quotes.db") as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT * FROM quotes WHERE guild_id = ? AND marked = 1", (guild_id,))
                del_search = await cur.fetchone()
                
                if (del_search is None):
                    print('here')
                    count_input = "SELECT COUNT(*) FROM quotes WHERE guild_id = ?"
                    await cur.execute(count_input, (guild_id,))
                    count = (await cur.fetchone())[0] + 1
                    
                    insert_input = "INSERT INTO quotes VALUES (?,?,?,?, 0)"
                    await cur.execute(insert_input, (count, guild_id, member_id, text))
                else:
                    count = del_search[4]
                    update_input = "UPDATE quotes SET user = ? AND message = ? AND marked = 0 WHERE guild_id = ? AND num_id = ?"
                    await cur.execute(update_input, (member_id, text, guild_id, count))
                await db.commit()
                
        await ctx.send(f'Quote added as number {count}!')
    
    @quote.command(name='remove', aliases = ['del', 'delete'])
    async def quote_delete(self, ctx, number : int):
        return
    
    @quote.command(name='help')
    async def quote_help(self, ctx):
        embed = discord.Embed(title="Help using quotes!", description="The list of commands:")
        embed.add_field(name="!quote <number>", value="Returns the quote with the specified number. If there is no number, it's random.", inline=False)
        embed.add_field(name="!quote add <text>", value="Adds the selected quote to the list of quotes!", inline=False)
        embed.add_field(name="!quote remove <number>", value="Removes the selected quote to the list of quotes. Only works if you're the original submitter. Aliased to 'del' and 'delete.'", inline=False)
        embed.add_field(name="!quote edit <number> <text>", value="Replaces the text of the numbered quote. Only works if you're the original submitter.", inline=False)
        await ctx.channel.send(content=None, embed=embed)
    
def setup(bot):
    bot.add_cog(quotes(bot))