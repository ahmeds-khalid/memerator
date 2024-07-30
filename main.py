import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import aiohttp
import logging

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@bot.event
async def on_ready():
    logging.info(f'Bot is ready. Logged in as {bot.user.name}')

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def meme(ctx, subreddit: str = None):
    """Fetch a random meme, optionally from a specific subreddit"""
    await fetch_meme(ctx, subreddit)

@bot.slash_command(name="meme", description="Get a random meme")
async def slash_meme(interaction: Interaction, subreddit: str = SlashOption(required=False, description="Specify a subreddit")):
    """Slash command to fetch a random meme, optionally from a specific subreddit"""
    await fetch_meme(interaction, subreddit)

async def fetch_meme(ctx, subreddit: str = None):
    url = 'https://meme-api.com/gimme'
    if subreddit:
        url += f'/{subreddit}'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    meme_url = data['url']
                    meme_title = data['title']
                    subreddit = data['subreddit']
                    post_link = data['postLink']
                    upvotes = data['ups']
                    
                    embed = nextcord.Embed(title=meme_title, color=nextcord.Color.random())
                    embed.set_image(url=meme_url)
                    embed.set_footer(text=f"From r/{subreddit} | ⬆ {upvotes}")
                    
                    if isinstance(ctx, Interaction):
                        await ctx.response.send_message(embed=embed)
                    else:
                        await ctx.send(embed=embed)
                else:
                    error_message = f"Error: Unable to fetch meme. Status code: {response.status}"
                    if isinstance(ctx, Interaction):
                        await ctx.response.send_message(error_message, ephemeral=True)
                    else:
                        await ctx.send(error_message)
        except Exception as e:
            logging.error(f"Error fetching meme: {str(e)}")
            error_message = "Sorry, I encountered an error while fetching the meme. Please try again later."
            if isinstance(ctx, Interaction):
                await ctx.response.send_message(error_message, ephemeral=True)
            else:
                await ctx.send(error_message)

@bot.slash_command(name="help", description="Get help on how to use the Memerator")
async def slash_help(interaction: Interaction):
    """Slash command to provide help information about the Memerator"""
    embed = nextcord.Embed(title="Memerator Help", description="Here's how to use Memerator:", color=nextcord.Color.blue())
    embed.add_field(name="Get a random meme:", value="Use `/meme` or `!meme`", inline=False)
    embed.add_field(name="Get a meme from a specific subreddit:", value="Use `/meme [subreddit]` or `!meme [subreddit]`\nFor example: `/meme dankmemes` or `!meme dankmemes`", inline=False)
    embed.add_field(name="Note:", value="The bot has a 30-second cooldown between requests to prevent spam.", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@meme.error
async def meme_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Slow down! Try again in {error.retry_after:.0f} seconds.")

bot.run('MTI2NzIwMTM0MzA2MDQ0NzI2Mg.GsCdjJ.GkjeG5I-Br6g1-rhzxpJ5fZ0RT8Cnvcvi5p8pk')