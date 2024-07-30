import nextcord
from nextcord.ext import commands
import aiohttp
import random

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

@bot.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://meme-api.com/gimme') as response:
            if response.status == 200:
                data = await response.json()
                meme_url = data['url']
                meme_title = data['title']
                subreddit = data['subreddit']
                
                embed = nextcord.Embed(title=meme_title, color=nextcord.Color.random())
                embed.set_image(url=meme_url)
                embed.set_footer(text=f"From r/{subreddit}")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Sorry, I couldn't fetch a meme at the moment. Please try again later.")

bot.run('MTI2NzIwMTM0MzA2MDQ0NzI2Mg.GsCdjJ.GkjeG5I-Br6g1-rhzxpJ5fZ0RT8Cnvcvi5p8pk')