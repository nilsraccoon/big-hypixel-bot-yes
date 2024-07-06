import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)