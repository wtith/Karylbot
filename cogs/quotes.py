# -*- coding: utf-8 -*-
"""
Cog that handles quotes via mongoDB.

Quotes are structured as follows:
    example = {"guild_id": <guild_id>,
           "message": <text>,
           "member_id": <member_id>,
           "quote_number": <number>}
"""

import discord
from discord.ext import commands
from pymongo import ReturnDocument
from lib.database import db

class quotes(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.collection = db.quotations
        self.counter = db.counter_collection
        print('quotes loaded')
    
    # code to check if the quote selected is valid for the database
    async def quote_modify(self, ctx, number: int):
        if (number < 1):
            await ctx.send('Use a number above zero, dumbass.')
            return False
            
        select = self.collection.find_one({'guild_id': ctx.guild.id, 'quote_number': number})
            
        if select is None:
            await ctx.send('That quote can\'t be found!')
            return False
        
        if select['member_id'] != ctx.message.author.id:
            await ctx.send('You can\'t modify quotes that aren\'t your own, moron.')
            return False
        
        return True
        
    # default picks a random quote from the database
    @commands.group(name='quote', invoke_without_command=True)
    async def quote(self, ctx, number = None):
        
        count = self.collection.count_documents({'guild_id': ctx.guild.id})
        
        if (count == 0):
            await ctx.send('There aren\'t any quotes for this discord!')
            return
        
        # if no argument select a random quote
        if (number == None):
            random_quote = self.collection.aggregate([{ '$match': {'guild_id': ctx.guild.id, 'quote_number': {'$gt': 0}}},
                                       { '$sample': {'size': 1}}])
            
            for item in random_quote:
                await ctx.send(item['message'])
            return
        
        # otherwise we try to get the quote with the number specified
        try:
            quote_val = int(number)
            
            if (quote_val == 0):
                await ctx.send('There\'s no quote zero, idiot.')
                return
            
            elif (quote_val < 0):
                await ctx.send('There\'s nothing here!')
                return
            
            select = self.collection.find_one({'guild_id': ctx.guild.id, 'quote_number': quote_val})
            
            if select is None:
                await ctx.send('That quote can\'t be found!')
                return
            
            await ctx.send(select['message'])
            
        except ValueError: 
            await ctx.send('Please submit a valid number for quotes!')
        
    # adds the content of a message to the quote database
    # awkward because it's two insertions/updates per quote
    @quote.command(name='add')
    async def quote_add(self, ctx, *, text : str):
        
        count = 0
        
        # see if there are any empty spots in the db
        filler = self.counter.find_one_and_update({'guild_id': ctx.guild.id, 'empty_slots': { '$exists': True}},
                                            {'$pop': {'empty_slots': -1}})
        
        # if there are no empty spots/counter collection
        if filler is None:
            # implement a counter collection to keep track of quote # per discord
            filler = self.counter.find_one_and_update({'guild_id': ctx.guild.id}, 
                                             {'$inc': {'counter': 1}}, upsert = True, 
                                             return_document=ReturnDocument.AFTER)    
            
            count = filler['counter']
        
        else:
            
            count = filler['empty_slots'][0]
        
        select = {'guild_id': ctx.guild.id, 
                  'message': text, 
                  'member_id': ctx.message.author.id, 
                  'quote_number': count}
        
        self.collection.insert(select)
        
        await ctx.send(f'Quote added as number {count}!')
        
    # 'deletes' a quote but making sure it can't be searched
    # will work on a real deletion option that doesn't require me to refactor the entire list
    @quote.command(name='remove', aliases = ['del', 'delete'])
    async def quote_delete(self, ctx, number : int):
        
        validity = await self.quote_modify(ctx, number)
        
        if (not(validity)):
            return
        
        # try to edit quote if it's a valid number
        self.collection.delete_one({'guild_id': ctx.guild.id, 'quote_number': number})
        self.counter.find_one_and_update({'guild_id': ctx.guild.id}, {'$push': {'empty_slots': number}})
        
        await ctx.send(f'Quote {number} has been deleted!')
        
    # adds the content of a message to the quote database
    @quote.command(name='edit')
    async def quote_edit(self, ctx, number: int, *, text : str):
        
        validity = await self.quote_modify(ctx, number)
        
        if (not(validity)):
            return
        
        # try to edit quote if it's a valid number
            
        self.collection.update_one({'guild_id': ctx.guild.id, 'quote_number': number}, {'$set': {'message': text}})
        
        await ctx.send('Your quote has been edited!')
    
    @quote.command(name='help')
    async def quote_help(self, ctx):
        embed = discord.Embed(title="Help using quotes!", description="The list of commands:")
        embed.add_field(name="!quote <number>", value="Returns the quote with the specified number. If there is no number, it's random.", inline=False)
        embed.add_field(name="!quote add <text>", value="Adds the selected quote to the list of quotes!", inline=False)
        embed.add_field(name="!quote remove <number>", value="Removes the selected quote to the list of quotes. Only works if you're the original submitter. Aliased to 'del' and 'delete.'", inline=False)
        embed.add_field(name="!quote edit <number> <text>", value="Replaces the text of the numbered quote. Only works if you're the original submitter.", inline=False)
        await ctx.channel.send(content=None, embed=embed)
 
    @quote_delete.error
    async def delete_error(self, ctx, error):
            
        if isinstance (error, commands.BadArgument):
            await ctx.send('Please submit a valid number for deleting quotes!')
    
    @quote_edit.error
    async def edit_error(self, ctx, error):
        
        if isinstance(error, commands.BadArgument):
            await ctx.send('Please format as !quote edit <number> <text>!')

    
def setup(bot):
    bot.add_cog(quotes(bot))